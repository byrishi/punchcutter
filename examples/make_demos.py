"""Render the demo images for the README and site: a filled-in handwriting
sheet, its phone photo, the font made from it, and the plain-paper route.
The handwriting is simulated (a rounded face bent by a random warp), and is
labelled as such wherever it is shown."""
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tests"))
sys.path.insert(0, os.path.join(ROOT, "skills", "punchcutter", "scripts"))
import fake_photo as fp  # noqa: E402
from pc import brand  # noqa: E402

CLI = [sys.executable, os.path.join(ROOT, "skills", "punchcutter", "scripts", "punchcutter.py")]


def warp(rgb_ink_alpha, px, seed, amount=0.55):
    import cv2
    H, W = rgb_ink_alpha.shape
    rng = np.random.default_rng(seed)
    d = []
    for _ in range(2):
        f = rng.normal(0, 1, (H // 24 + 2, W // 24 + 2)).astype(np.float32)
        d.append(cv2.resize(cv2.GaussianBlur(f, (0, 0), 1.2), (W, H), interpolation=cv2.INTER_CUBIC) * px * amount)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return cv2.GaussianBlur(cv2.remap(rgb_ink_alpha, xx + d[0], yy + d[1], cv2.INTER_LINEAR), (0, 0), 0.6)


def plain_paper(text, seed=21, px=8.0):
    """Lined notebook paper with a line of hand-printed writing."""
    import cairosvg
    import cv2
    Wmm, Hmm = 230.0, 90.0
    W, H = int(Wmm * px), int(Hmm * px)
    lines = "".join(f'<line x1="0" y1="{y}" x2="{Wmm}" y2="{y}" stroke="#b9cdd6" stroke-width="0.35"/>' for y in range(14, 90, 9))
    paper = f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wmm}mm" height="{Hmm}mm" viewBox="0 0 {Wmm} {Hmm}"><rect width="{Wmm}" height="{Hmm}" fill="#fbf9f2"/>{lines}</svg>'
    base = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=paper.encode(), output_width=W), np.uint8), cv2.IMREAD_COLOR)
    import random
    rnd = random.Random(seed)
    f = brand.face("Round")
    ink, x, y = [], 12.0, 41.0
    for word in text.split(" "):
        if x > Wmm - 60:
            x, y = 12.0, y + 27
        for ch in word:
            infos, pos = f.shape(ch)
            cap = 11.5 * rnd.uniform(0.94, 1.06)
            ink.append(fp._ink(ch, x, y + rnd.uniform(-0.5, 0.5), cap, rnd.uniform(-3, 3), "Round", "#000"))
            x += pos[0].x_advance * cap / 700 + 1.6
        x += 6
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wmm}mm" height="{Hmm}mm" viewBox="0 0 {Wmm} {Hmm}">{"".join(ink)}</svg>'
    a = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=svg.encode(), output_width=W), np.uint8), cv2.IMREAD_UNCHANGED)[:, :, 3]
    a = warp(a.astype(np.float32) / 255, px, seed)[..., None]
    out = base.astype(np.float32) * (1 - a) + np.array([30, 30, 28], np.float32) * a
    return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)


def side_by_side(left, right, out, h=760, gap=28, caption=None):
    from PIL import Image
    a, b = Image.open(left).convert("RGB"), Image.open(right).convert("RGB")
    a = a.resize((int(a.width * h / a.height), h))
    b = b.resize((int(b.width * h / b.height), h))
    c = Image.new("RGB", (a.width + b.width + gap, h), brand.CREAM)
    c.paste(a, (0, 0))
    c.paste(b, (a.width + gap, 0))
    c.save(out, quality=86)


def main(assets):
    from PIL import Image
    tmp = tempfile.mkdtemp()
    flats, photos = [], []
    for p in (0, 1):
        rgb = fp.handwritten_sheet(p, seed=p + 3)
        flat = os.path.join(tmp, f"flat{p + 1}.jpg")
        Image.fromarray(rgb).save(flat, quality=90)
        flats.append(flat)
        photos.append(fp.photograph_array(rgb, os.path.join(tmp, f"photo{p + 1}.jpg"), seed=p + 11))
    Image.open(flats[0]).save(os.path.join(assets, "demo-sheet-filled.jpg"), quality=86)
    Image.open(photos[0]).resize((1100, 1450)).save(os.path.join(assets, "demo-sheet-photo.jpg"), quality=84)
    proj = os.path.join(tmp, "proj")
    subprocess.run(CLI + ["read-sheet", *photos, "--family", "Marker Hand", "--weights", "400,700", "--out", proj], check=True, capture_output=True)
    out = os.path.join(tmp, "out")
    subprocess.run(CLI + ["build", os.path.join(proj, "MarkerHand.json"), "--out", out], check=True, capture_output=True)
    proof = Image.open(os.path.join(out, "proof.png"))
    proof.crop((0, 0, 1500, 1060)).save(os.path.join(tmp, "proof.png"))
    side_by_side(photos[0], os.path.join(tmp, "proof.png"), os.path.join(assets, "photo-to-font.jpg"))
    # plain paper route
    pp = os.path.join(tmp, "paper.jpg")
    Image.fromarray(plain_paper("Sphinx of black quartz judge my vow")).save(pp, quality=90)
    shot = fp.photograph_array(np.array(Image.open(pp)), os.path.join(tmp, "paper_photo.jpg"), seed=31, size=(2400, 1150))
    Image.open(shot).resize((1600, 767)).save(os.path.join(assets, "demo-plain-paper.jpg"), quality=84)
    seg = os.path.join(tmp, "seg")
    subprocess.run(CLI + ["segment", shot, "--out", seg], check=True, capture_output=True)
    found = Image.open(os.path.join(seg, "segments.png")).convert("RGB")
    arr = np.array(found).astype(int)
    ys, xs = np.nonzero(np.abs(arr - np.array([244, 239, 228])).sum(axis=2) > 40)
    m = 60
    found.crop((max(xs.min() - m, 0), max(ys.min() - m, 0), min(xs.max() + m, found.width), min(ys.max() + m, found.height))) \
        .save(os.path.join(assets, "demo-plain-paper-found.jpg"), quality=86)
    return out


if __name__ == "__main__":
    print(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets")))
