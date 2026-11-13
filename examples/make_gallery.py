"""Render one image showing every example family. Run after building them."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "punchcutter", "scripts"))
from pc.proof import Face, Sheet  # noqa: E402

FAMS = [("Burin Grotesk", "BurinGrotesk", "ExtraBold", "Regular"), ("Pomelo Round", "PomeloRound", "Bold", "Regular"),
        ("Quarry Slab", "QuarrySlab", "Bold", "Regular"), ("Semaphore Condensed", "SemaphoreCondensed", "ExtraBold", "Regular"),
        ("Lumen Contrast", "LumenContrast", "Bold", "Regular")]
LINE = "Quick wafting zephyrs vex bold Jim. 0123456789 &?!"


def main(build_dir, out, dark=False):
    sh = Sheet(width=1600, margin=80, bg="#121212" if dark else "#f6f4ef", fg="#f1efe9" if dark else "#141414")
    for name, fid, heavy, reg in FAMS:
        base = os.path.join(build_dir, fid, "fonts", "ttf")
        if not os.path.exists(os.path.join(base, f"{fid}-{heavy}.ttf")):
            continue
        sh.label(name.upper(), color="#e5482d", size=16)
        sh.gap(4)
        sh.line(Face(os.path.join(base, f"{fid}-{heavy}.ttf")), name, 118)
        sh.line(Face(os.path.join(base, f"{fid}-{reg}.ttf")), LINE, 44)
        sh.gap(34)
    sh.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], dark=len(sys.argv) > 3)
