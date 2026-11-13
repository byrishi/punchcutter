"""Render the repo banner and logo from Burin Grotesk (built by Punchcutter itself)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "punchcutter", "scripts"))
from pc.proof import Face, Sheet  # noqa: E402


def main(build_dir, assets):
    base = os.path.join(build_dir, "BurinGrotesk", "fonts", "ttf")
    heavy, reg = Face(os.path.join(base, "BurinGrotesk-ExtraBold.ttf")), Face(os.path.join(base, "BurinGrotesk-Regular.ttf"))
    light = Face(os.path.join(base, "BurinGrotesk-Light.ttf"))
    sh = Sheet(width=1600, margin=96, bg="#121212", fg="#f1efe9")
    sh.gap(30)
    sh.line(reg, "OPEN SOURCE TYPE FOUNDRY FOR CLAUDE", 22, color="#e5482d", tracking=0.12)
    sh.gap(26)
    sh.line(heavy, "Punchcutter", 236, tracking=-0.012)
    sh.gap(18)
    sh.line(light, "Describe a typeface. Get a font family.", 62)
    sh.gap(40)
    sh.line(reg, "Brief  >  Drawing  >  Spacing  >  Kerning  >  Features  >  QA  >  Release", 26, color="#8f8b82")
    sh.gap(30)
    sh.save(os.path.join(assets, "banner.svg"))
    # square mark
    s = 512
    f = Face(os.path.join(base, "BurinGrotesk-ExtraBold.ttf"))
    infos, pos = f.shape("P")
    adv = pos[0].x_advance
    k = 330 / f.upm
    x = (s - adv * k) / 2
    y = s / 2 + 714 * k / 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">'
           f'<rect width="{s}" height="{s}" rx="96" fill="#e5482d"/>'
           f'<g fill="#121212" transform="translate({x:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})"><path d="{f.path(infos[0].codepoint)}"/></g></svg>')
    with open(os.path.join(assets, "logo.svg"), "w") as fh:
        fh.write(svg)
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(assets, "logo.png"))
    except Exception:
        pass


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
