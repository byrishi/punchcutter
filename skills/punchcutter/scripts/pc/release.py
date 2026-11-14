"""Release package: CSS, the Studio app, the QA report and a font README."""
from __future__ import annotations

import datetime
import html
import json
import os

from . import brand
from .check import check_all
from .presets import WEIGHT_NAME


def css(result):
    fam, fid = result["family"], result["family_id"]
    ws = result["weights"]
    out = []
    if result["variable"]:
        out.append(f"""@font-face {{
  font-family: "{fam}";
  src: url("webfonts/{fid}[wght].woff2") format("woff2-variations"), url("webfonts/{fid}[wght].woff2") format("woff2");
  font-weight: {min(result['masters'])} {max(result['masters'])};
  font-style: normal;
  font-display: swap;
}}""")
    else:
        for w in ws:
            style = WEIGHT_NAME.get(w, str(w))
            out.append(f"""@font-face {{
  font-family: "{fam}";
  src: url("webfonts/{fid}-{style}.woff2") format("woff2");
  font-weight: {w};
  font-style: normal;
  font-display: swap;
}}""")
    return "\n\n".join(out) + "\n"


def release(result):
    """Write CSS, specimen, QA report and README next to the fonts. Returns (fails, warns)."""
    from fontTools.ttLib import TTFont
    out = result["out"]
    fonts = os.path.join(out, "fonts")
    log = result["log"]
    ttf = next(f for f in result["fonts"] if f.endswith(".ttf"))
    cps = sorted(TTFont(ttf).getBestCmap())
    chars = [chr(c) for c in cps if c > 0x20 and c != 0xA0]  # noqa: F841

    log.stage("Quality assurance")
    lines, fails, warns = check_all(result)
    n = sum(1 for ln in lines if ln.startswith("- "))
    log.note(f"{n} checks on {sum(1 for ln in lines if ln.startswith('###'))} files: {n - fails - warns} pass, {warns} warn, {fails} fail")
    for ln in lines:
        if ln.startswith("- FAIL") or ln.startswith("- WARN"):
            log.note(ln[2:])

    log.stage("Release package")
    with open(os.path.join(fonts, f"{result['family_id']}.css"), "w") as f:
        f.write(css(result))
    from .studio import build_studio
    n = sum(1 for ln in lines if ln.startswith("- "))
    build_studio(result, qa=f"QA {n - fails - warns}/{n} pass")
    spec = result["spec"]
    ws = result["weights"]
    readme = [f"# {result['family']}", "", spec.get("description", "An original typeface."), "",
              f"- Weights: {', '.join(f'{WEIGHT_NAME.get(w, w)} ({w})' for w in ws)}" + (" plus a variable font (wght axis)" if result["variable"] else ""),
              f"- {len(chars)} characters: Basic Latin, Latin-1 and Latin Extended-A accents, punctuation, currency",
              "- OpenType features: kerning, tabular figures (tnum), slashed zero (zero), case-sensitive forms (case)" + (", alternate a (ss01)" if spec.get("mode") != "handwriting" else ""),
              "", "## Files", "", "- `variable/` one file, every weight (best for the web)" if result["variable"] else "",
              "- `ttf/`, `otf/` desktop fonts: install these", "- `webfonts/` WOFF2 for websites",
              f"- `{result['family_id']}.css` ready-made @font-face rules", "- `studio.html` the font's app: test it, inspect glyphs, download (works offline)", "",
              "## Use on a website", "", "```html", f'<link rel="stylesheet" href="{result["family_id"]}.css">',
              f"<style>body {{ font-family: \"{result['family']}\", sans-serif; }}</style>", "```", "",
              "## License", "", spec.get("license") or "No license set. All rights reserved by the designer until one is added.", "",
              f"Cut {datetime.date.today().isoformat()} with Punchcutter ({brand.SITE})."]
    with open(os.path.join(fonts, "README.md"), "w") as f:
        f.write("\n".join(x for x in readme if x is not None))
    rep = [f"# {result['family']} build report", "", f"Built {datetime.date.today().isoformat()}.", ""]
    for st in log.report:
        rep.append(f"## {st['stage']}")
        rep.extend(f"- {n_}" for n_ in st["notes"])
        rep.append("")
    rep.append("## Checks")
    rep.append("")
    rep.extend(lines)
    with open(os.path.join(out, "report.md"), "w") as f:
        f.write("\n".join(rep))
    with open(os.path.join(out, "design.json"), "w") as f:
        json.dump({k: v for k, v in result["design"].items()}, f, indent=2)
    log.note("fonts/studio.html, fonts/%s.css, fonts/README.md, report.md, design.json" % result["family_id"])
    return fails, warns
