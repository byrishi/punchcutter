"""Smoke tests: every preset draws, a family compiles, QA passes."""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "punchcutter", "scripts")
sys.path.insert(0, SCRIPTS)


def test_every_preset_draws_every_master():
    from pc.build import draw_master, master_designs, resolve_design
    from pc.presets import PRESETS
    for preset in PRESETS:
        spec = {"family": "T", "preset": preset, "weights": [200, 400, 900]}
        masters, _ = master_designs(spec, resolve_design(spec))
        counts = set()
        for d in masters.values():
            glyphs, _ = draw_master(d)
            counts.add(tuple((n, len(g.contours), sum(len(c.segs) for c in g.contours)) for n, g in glyphs.items()))
            assert all(g.advance > 0 for g in glyphs.values())
        assert len(counts) == 1, f"{preset}: masters are not point-compatible"


def test_full_build_passes_qa():
    with tempfile.TemporaryDirectory() as tmp:
        spec = os.path.join(tmp, "s.json")
        with open(spec, "w") as f:
            json.dump({"family": "Smoke Test", "preset": "humanist", "weights": [400, 700], "design": {"slant": 8}}, f)
        out = os.path.join(tmp, "out")
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "punchcutter.py"), "build", spec, "--out", out, "--no-proof"],
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        for p in ("fonts/variable/SmokeTest[wght].ttf", "fonts/ttf/SmokeTest-Regular.ttf", "fonts/otf/SmokeTest-Bold.otf",
                  "fonts/webfonts/SmokeTest[wght].woff2", "fonts/SmokeTest.css", "fonts/specimen.html", "report.md"):
            assert os.path.exists(os.path.join(out, p)), p


if __name__ == "__main__":
    test_every_preset_draws_every_master()
    test_full_build_passes_qa()
    print("ok")
