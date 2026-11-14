"""Render the repo's brand assets: banner, social card, logo, sheet preview.
Everything is generated: the fields are procedural, the type is Punchcutter's own."""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "punchcutter", "scripts"))
from pc import brand  # noqa: E402


def _card(w, h, scene, body):
    import cv2
    img = brand.field(w, h, scene)
    ok, buf = cv2.imencode(".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<image width="{w}" height="{h}" xlink:href="data:image/jpeg;base64,{base64.b64encode(buf.tobytes()).decode()}"/>'
            f'<rect width="{w}" height="{h}" fill="#141810" opacity="0.16"/>{body}</svg>')


def _save(svg, path, width):
    import cairosvg
    from PIL import Image
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path[:-4] + ".png", output_width=width)
    Image.open(path[:-4] + ".png").convert("RGB").save(path, quality=88)
    os.remove(path[:-4] + ".png")


def main(assets):
    os.makedirs(assets, exist_ok=True)
    W, H = 1600, 760
    body = (brand.mark(W / 2 - 62, 196, 124, bg=None)
            + brand.wordmark(W / 2, 452, 104, anchor="middle")[0]
            + brand.text(brand.TAGLINE, W / 2, 522, 34, "Regular", "#ffffff", anchor="middle")[0]
            + brand.text("A TYPE FOUNDRY FOR CLAUDE AND OTHER AI AGENTS", W / 2, 700, 17, "Regular", "#ffffff", tracking=0.14, anchor="middle")[0])
    _save(_card(W, H, "haze", body), os.path.join(assets, "banner.jpg"), W)
    body = (brand.mark(640 - 70, 150, 140, bg=None) + brand.wordmark(640, 420, 92, anchor="middle")[0]
            + brand.text(brand.TAGLINE, 640, 482, 30, "Regular", "#ffffff", anchor="middle")[0])
    _save(_card(1280, 640, "meadow", body), os.path.join(assets, "social.jpg"), 1280)
    logo = f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">{brand.mark(0, 0, 512)}</svg>'
    with open(os.path.join(assets, "logo.svg"), "w") as f:
        f.write(logo)
    import cairosvg
    cairosvg.svg2png(bytestring=logo.encode(), write_to=os.path.join(assets, "logo.png"))
    lock = (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220">{brand.mark(20, 30, 160)}'
            + brand.wordmark(215, 142, 96, fill=brand.INK)[0] + "</svg>")
    with open(os.path.join(assets, "lockup.svg"), "w") as f:
        f.write(lock)
    dark = (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220">{brand.mark(20, 30, 160)}'
            + brand.wordmark(215, 142, 96, fill=brand.CREAM)[0] + "</svg>")
    with open(os.path.join(assets, "lockup-dark.svg"), "w") as f:
        f.write(dark)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets"))
