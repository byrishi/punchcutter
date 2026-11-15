"""Make realistic test photos: a filled-in handwriting sheet shot at an angle
under uneven light, and a freeform line of writing. Used by the tests."""
import os
import random
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "punchcutter", "scripts"))

from pc import brand, handwriting as hw  # noqa: E402


def _ink(ch, x, y, cap_mm, rot, font, color):
    f = brand.face(font)
    infos, pos = f.shape(ch)
    k = cap_mm / 700.0
    d = "".join(f.path(i.codepoint) for i in infos[:1])
    return (f'<g fill="{color}" transform="translate({x:.2f} {y:.2f}) rotate({rot:.2f}) scale({k:.5f} {-k:.5f})">'
            f'<path d="{d}"/></g>')


def filled_sheet_svg(page, font="Bold", seed=1, color="#1b2a6b", ink_only=False):
    rnd = random.Random(seed)
    svg = hw.sheet_svg(page)
    ink = []
    for idx, ch in enumerate(hw.PAGES[page]):
        x, y = hw._cell_origin(idx)
        cap = hw.CAP_MM * rnd.uniform(1.0, 1.18)
        ink.append(_ink(ch, x + hw.CELL_W * rnd.uniform(0.3, 0.38), y + hw.BASE + rnd.uniform(-0.6, 0.4),
                        cap, rnd.uniform(-4, 4), font, color))
    if ink_only:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{hw.PAGE_W}mm" height="{hw.PAGE_H}mm" '
                f'viewBox="0 0 {hw.PAGE_W} {hw.PAGE_H}">' + "".join(ink) + "</svg>")
    return svg.replace("</svg>", "".join(ink) + "</svg>")


def handwritten_sheet(page, seed=1, px_mm=8.0, font="Round", color=(32, 44, 92)):
    """A filled sheet that looks written by hand: letters from a rounded face,
    then every stroke bent by a smooth random warp, like a marker on paper.
    Returns an RGB array at px_mm resolution."""
    import cairosvg
    import cv2
    W, H = int(hw.PAGE_W * px_mm), int(hw.PAGE_H * px_mm)
    base = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=hw.sheet_svg(page).encode(), output_width=W), np.uint8), cv2.IMREAD_COLOR)
    inkpng = cairosvg.svg2png(bytestring=filled_sheet_svg(page, font, seed, "#000", ink_only=True).encode(), output_width=W)
    ink = cv2.imdecode(np.frombuffer(inkpng, np.uint8), cv2.IMREAD_UNCHANGED)[:, :, 3].astype(np.float32) / 255
    rng = np.random.default_rng(seed)
    disp = []
    for _ in range(2):
        f = rng.normal(0, 1, (H // 24 + 2, W // 24 + 2)).astype(np.float32)
        f = cv2.resize(cv2.GaussianBlur(f, (0, 0), 1.2), (W, H), interpolation=cv2.INTER_CUBIC)
        disp.append(f * px_mm * 0.55)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ink = cv2.remap(ink, xx + disp[0], yy + disp[1], cv2.INTER_LINEAR)
    ink = cv2.GaussianBlur(ink, (0, 0), 0.6)
    tone = 0.82 + 0.18 * cv2.resize(rng.random((H // 40 + 1, W // 40 + 1)).astype(np.float32), (W, H))
    a = np.clip(ink * tone, 0, 1)[..., None]
    out = base.astype(np.float32) * (1 - a) + np.array(color[::-1], np.float32) * a
    return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)


def photograph_array(rgb, out, seed=2, size=(2200, 2900)):
    import cv2
    ok, buf = cv2.imencode(".png", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    return _shoot(cv2.imdecode(buf, cv2.IMREAD_COLOR), out, seed, size)


def photograph(svg, out, seed=2, px_mm=7.0, size=(2200, 2900)):
    import cairosvg
    import cv2
    rnd = random.Random(seed)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=int(hw.PAGE_W * px_mm))
    page = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
    return _shoot(page, out, seed, size)


def _shoot(page, out, seed, size):
    import cv2
    rnd = random.Random(seed)
    h, w = page.shape[:2]
    W, H = size
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    j = lambda: rnd.uniform(-90, 90)  # noqa: E731
    dst = np.float32([[180 + j(), 160 + j()], [W - 200 + j(), 220 + j()], [W - 150 + j(), H - 180 + j()], [230 + j(), H - 220 + j()]])
    M = cv2.getPerspectiveTransform(src, dst)
    table = np.full((H, W, 3), (150, 168, 160), np.uint8)  # sage desk (BGR)
    shot = cv2.warpPerspective(page, M, (W, H), dst=table, borderMode=cv2.BORDER_TRANSPARENT)
    yy, xx = np.mgrid[0:H, 0:W]
    light = 0.62 + 0.38 * (xx / W * 0.6 + (1 - yy / H) * 0.4)
    shot = shot.astype(np.float32) * light[..., None] * np.array([0.93, 0.98, 1.0])
    shot += np.random.default_rng(seed).normal(0, 5, shot.shape)
    shot = cv2.GaussianBlur(np.clip(shot, 0, 255).astype(np.uint8), (0, 0), 1.1)
    cv2.imwrite(out, shot, [cv2.IMWRITE_JPEG_QUALITY, 86])
    return out


def freeform_svg(text="Hamburgefonstiv quick jumps 2026", font="Bold", seed=3):
    rnd = random.Random(seed)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="80mm" viewBox="0 0 210 80"><rect width="210" height="80" fill="#fffdf7"/>']
    x = 10.0
    f = brand.face(font)
    for ch in text:
        if ch == " ":
            x += 6
            continue
        infos, pos = f.shape(ch)
        cap = 12 * rnd.uniform(0.95, 1.05)
        o.append(_ink(ch, x, 40 + rnd.uniform(-0.5, 0.5), cap, rnd.uniform(-2, 2), font, "#141414"))
        x += pos[0].x_advance * cap / 700 + 1.2
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for p in range(2):
        print(photograph(filled_sheet_svg(p, seed=p + 1), os.path.join(out, f"sheet{p + 1}.jpg"), seed=p + 5))
    print(photograph(freeform_svg(), os.path.join(out, "freeform.jpg"), seed=9, size=(2400, 1100)))
