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
                  "fonts/webfonts/SmokeTest[wght].woff2", "fonts/SmokeTest.css", "fonts/studio.html", "report.md"):
            assert os.path.exists(os.path.join(out, p)), p


def _cli(*args, cwd=None):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "punchcutter.py"), *args], capture_output=True, text=True, cwd=cwd)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def test_handwriting_sheet_photo_to_font():
    """A filled sheet, photographed at an angle in uneven light, becomes a font with the written letters."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fake_photo
    with tempfile.TemporaryDirectory() as tmp:
        photo = fake_photo.photograph(fake_photo.filled_sheet_svg(0), os.path.join(tmp, "p1.jpg"), seed=5)
        out = _cli("read-sheet", photo, "--family", "Hand Test", "--out", os.path.join(tmp, "proj"))
        assert "56 of 56 characters" in out, out
        _cli("build", os.path.join(tmp, "proj", "HandTest.json"), "--out", os.path.join(tmp, "out"), "--no-proof")
        assert os.path.exists(os.path.join(tmp, "out", "fonts", "ttf", "HandTest-Regular.ttf"))
        assert os.path.getsize(os.path.join(tmp, "out", "fonts", "studio.html")) > 100_000


def test_quick_photo_to_font():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fake_photo
    with tempfile.TemporaryDirectory() as tmp:
        svg = fake_photo.freeform_svg("Hamburgefonstiv")
        photo = fake_photo.photograph(svg, os.path.join(tmp, "f.jpg"), seed=9, size=(2400, 1100))
        out = _cli("segment", photo, "--out", os.path.join(tmp, "seg"))
        assert "found 15 characters" in out, out
        _cli("label", os.path.join(tmp, "seg"), "--text", "Hamburgefonstiv", "--family", "Quick Test", "--out", os.path.join(tmp, "proj"))
        _cli("build", os.path.join(tmp, "proj", "QuickTest.json"), "--draft", "--no-proof", "--out", os.path.join(tmp, "out"))
        assert os.path.exists(os.path.join(tmp, "out", "fonts", "ttf", "QuickTest-Regular.ttf"))


def test_mcp_server_lists_tools():
    try:
        import mcp  # noqa: F401
    except ImportError:
        return
    import asyncio
    from pc.mcp_server import make_server
    names = {t.name for t in asyncio.run(make_server().list_tools())}
    assert {"menu", "new_font", "build_font", "handwriting_sheet", "read_sheet_photos", "find_letters", "label_letters"} <= names


if __name__ == "__main__":
    test_every_preset_draws_every_master()
    test_full_build_passes_qa()
    test_handwriting_sheet_photo_to_font()
    test_quick_photo_to_font()
    test_mcp_server_lists_tools()
    print("ok")
