"""Anonymous usage statistics, so the project can tell real use from stars.

What is sent: an event name ("installed", "build_completed" ...), a random install id
made on this machine, the Punchcutter version, the surface (cli, mcp, studio), the AI
client name the MCP server reports, the route (describe, handwriting, photo, remix),
build outcome and duration, OS family and Python version. Never: font names, text,
images, file paths, prompts, IP-based location or anything about you.

Turn it off with any of:
    PUNCHCUTTER_TELEMETRY=0      DO_NOT_TRACK=1      punchcutter telemetry off
It is also off in CI and in the test suite.
"""
from __future__ import annotations

import json
import os
import platform
import sys
import threading
import time
import urllib.request
import uuid

KEY = "phc_OP89N6nuHWu48k3n7j2fhFcA2y51GODeJGMJgRZgPbv"   # public, write-only project key
HOST = "https://us.i.posthog.com"
_DIR = os.path.join(os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config"), "punchcutter")
_ID = os.path.join(_DIR, "install.json")
_threads: list[threading.Thread] = []
_client = {"name": "", "version": ""}
SURFACE = {"name": "cli"}


def _falsy(v):
    return str(v).strip().lower() in ("0", "false", "no", "off")


def enabled():
    if _falsy(os.environ.get("PUNCHCUTTER_TELEMETRY", "1")) or os.environ.get("DO_NOT_TRACK") not in (None, "", "0"):
        return False
    if os.environ.get("CI") or os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("PUNCHCUTTER_TESTING"):
        return False
    return not _state().get("off", False)


def _state():
    try:
        with open(_ID) as f:
            return json.load(f)
    except Exception:
        return {}


def _save(st):
    try:
        os.makedirs(_DIR, exist_ok=True)
        with open(_ID, "w") as f:
            json.dump(st, f)
    except Exception:
        pass


def set_enabled(on: bool):
    st = _state()
    st["off"] = not on
    st.setdefault("id", uuid.uuid4().hex)
    _save(st)


def install_id():
    """The random id for this machine, creating it (and recording the install) on first use."""
    st = _state()
    if st.get("id"):
        return st["id"]
    st = {"id": uuid.uuid4().hex, "first_seen": int(time.time()), "ref": os.environ.get("PUNCHCUTTER_REF", "")}
    _save(st)
    if enabled():
        sys.stderr.write("punchcutter shares anonymous usage counts (no fonts, text or files) to measure adoption. "
                         "Opt out: PUNCHCUTTER_TELEMETRY=0 or `punchcutter telemetry off`.\n")
        _send("installed", {"ref": st["ref"]}, st["id"])
    return st["id"]


def set_client(name, version=""):
    _client["name"], _client["version"] = (name or "")[:60], (version or "")[:30]


def _send(event, props, distinct):
    from . import brand
    body = {"api_key": KEY, "event": f"pc_{event}", "distinct_id": distinct, "properties": {
        "app": "punchcutter", "version": brand.VERSION, "os": platform.system().lower(), "python": platform.python_version(),
        "client": _client["name"] or props.get("client", ""), "client_version": _client["version"],
        "ref": os.environ.get("PUNCHCUTTER_REF") or _state().get("ref", ""),
        "$process_person_profile": False, "$geoip_disable": True, "$lib": "punchcutter", **props}}

    def post():
        try:
            req = urllib.request.Request(HOST + "/i/v0/e/", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=3).read()
        except Exception:
            pass

    t = threading.Thread(target=post, daemon=True)
    t.start()
    _threads.append(t)


def track(event, **props):
    """Record one anonymous event. Never raises, never blocks a build."""
    try:
        if not enabled():
            return
        _send(event, {k: v for k, v in props.items() if v is not None}, install_id())
    except Exception:
        pass


def flush(timeout=3.0):
    """Give pending events a moment to leave before a short-lived CLI process exits."""
    end = time.time() + timeout
    for t in list(_threads):
        t.join(max(0, end - time.time()))


def route_of(spec: dict) -> str:
    if spec.get("mode") == "remix":
        return "open_base"
    if spec.get("mode") == "handwriting":
        return spec.get("route") or "handwriting"
    return "describe"


def studio_snippet():
    """JS for the Studio page: reports that it was opened and which actions were used, tied to the
    install id that built it. Empty when telemetry is off at build time."""
    if not enabled():
        return ""
    from . import brand
    return ("<script>(function(){var K='%s',D='%s',V='%s';function t(e,p){try{var b=JSON.stringify({api_key:K,event:'pc_'+e,distinct_id:D,"
            "properties:Object.assign({app:'punchcutter',version:V,surface:'studio',$process_person_profile:false,$geoip_disable:true},p||{})});"
            "if(navigator.sendBeacon)navigator.sendBeacon('%s/i/v0/e/',new Blob([b],{type:'application/json'}));"
            "else fetch('%s/i/v0/e/',{method:'POST',body:b,keepalive:true})}catch(e){}}"
            "window.pcTrack=t;t('studio_opened',{online:navigator.onLine});})();</script>"
            % (KEY, install_id(), brand.VERSION, HOST, HOST))
