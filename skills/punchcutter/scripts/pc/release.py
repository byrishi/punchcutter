"""Release package: CSS, a specimen page, the QA report and a font README."""
from __future__ import annotations

import datetime
import html
import json
import os

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


SPECIMEN = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__FAM__ specimen</title>
<style>
__CSS__
:root{--bg:#f6f4ef;--fg:#141414;--mute:#8a867d;--line:#d9d5cb;--acc:#e5482d}
@media(prefers-color-scheme:dark){:root{--bg:#121212;--fg:#f1efe9;--mute:#8f8b82;--line:#2c2b28}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:"__FAM__",system-ui,sans-serif;font-weight:__REG__}
main{max-width:1180px;margin:0 auto;padding:6vw 5vw 10vw}
.k{font:500 12px/1 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:0 0 18px}
section{border-top:1px solid var(--line);padding:44px 0}
h1{font-size:clamp(64px,15vw,220px);line-height:.9;margin:0 0 28px;font-weight:__MAX__;letter-spacing:-.02em;overflow-wrap:anywhere}
.lede{font-size:clamp(20px,2.6vw,34px);line-height:1.3;max-width:26em;margin:0}
.w{display:flex;align-items:baseline;gap:24px;border-bottom:1px solid var(--line);padding:10px 0;overflow:hidden;white-space:nowrap}
.w span{font:500 12px/1 ui-monospace,monospace;color:var(--mute);width:110px;flex:none}.w b{font-size:clamp(30px,6vw,72px);font-weight:inherit}
#try{font-size:clamp(40px,9vw,128px);line-height:1.02;outline:none;min-height:1.1em;overflow-wrap:anywhere}
.ctl{display:flex;flex-wrap:wrap;gap:18px 28px;align-items:center;font:500 13px/1 ui-monospace,monospace;color:var(--mute);margin-bottom:26px}
.ctl label{display:flex;gap:8px;align-items:center}input[type=range]{accent-color:var(--acc);width:180px}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:36px}.cols p{margin:0;line-height:1.5}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));border-left:1px solid var(--line);border-top:1px solid var(--line)}
.grid div{aspect-ratio:1;display:grid;place-items:center;font-size:30px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.grid div:hover{background:var(--fg);color:var(--bg)}
footer{font:500 12px/1.6 ui-monospace,monospace;color:var(--mute);border-top:1px solid var(--line);padding-top:24px}
</style></head><body><main>
<p class="k">__FAM__ / __COUNT__ glyphs / __STYLES__</p>
<h1>__FAM__</h1>
<p class="lede">__DESC__</p>
<section><p class="k">Type tester</p>
<div class="ctl">__SLIDER__
<label><input type="checkbox" data-f="ss01"> alternate a</label><label><input type="checkbox" data-f="tnum"> tabular figures</label>
<label><input type="checkbox" data-f="zero"> slashed zero</label><label><input type="checkbox" data-f="case"> case-sensitive forms</label></div>
<div id="try" contenteditable spellcheck="false">Quick wafting zephyrs vex bold Jim 0123456789</div></section>
<section><p class="k">Weights</p>__WEIGHTS__</section>
<section><p class="k">Text</p><div class="cols">
<p style="font-size:22px">__TEXT__</p><p style="font-size:17px">__TEXT__</p><p style="font-size:14px">__TEXT__</p></div></section>
<section><p class="k">Glyphs</p><div class="grid">__GLYPHS__</div></section>
<footer>__FOOT__</footer>
</main><script>
const t=document.getElementById('try'),on=new Set();
document.querySelectorAll('[data-f]').forEach(c=>c.onchange=()=>{c.checked?on.add(c.dataset.f):on.delete(c.dataset.f);
t.style.fontFeatureSettings=[...on].map(f=>'"'+f+'"').join(',')||'normal'});
const s=document.getElementById('wght');if(s)s.oninput=()=>{t.style.fontWeight=s.value;document.getElementById('wv').textContent=s.value};
</script></body></html>
"""

TEXT = ("Type is the clothing words wear. A good typeface disappears while you read and leaves only the voice of "
        "the writer. Spacing is half of that work: the white between letters must feel as even as the black of "
        "the strokes, so a line of text keeps one steady rhythm from the first word to the last.")


def specimen(result, glyph_chars):
    fam = result["family"]
    ws = result["weights"]
    reg = 400 if 400 in ws else ws[len(ws) // 2]
    lo, hi = min(result["masters"]), max(result["masters"])
    slider = (f'<label>weight <input id="wght" type="range" min="{lo}" max="{hi}" value="{reg}"> <span id="wv">{reg}</span></label>'
              if result["variable"] else "")
    weights = "".join(f'<div class="w" style="font-weight:{w}"><span>{WEIGHT_NAME.get(w, w)} {w}</span><b>Hamburgefonstiv</b></div>' for w in ws)
    glyphs = "".join(f"<div>{html.escape(c)}</div>" for c in glyph_chars)
    spec = result["spec"]
    foot = f"{fam} v{spec.get('version', '1.000')}. {html.escape(spec.get('copyright', '') or ('Designed by ' + spec['designer'] if spec.get('designer') else ''))} Cut with Punchcutter."
    page = SPECIMEN
    for k, v in {"__CSS__": css(result), "__FAM__": html.escape(fam), "__REG__": str(reg), "__MAX__": str(ws[-1]),
                 "__COUNT__": str(len(glyph_chars)), "__STYLES__": f"{len(ws)} weight{'s' if len(ws) > 1 else ''}" + (" + variable" if result["variable"] else ""),
                 "__DESC__": html.escape(spec.get("description") or "An original typeface."), "__SLIDER__": slider,
                 "__WEIGHTS__": weights, "__TEXT__": TEXT, "__GLYPHS__": glyphs, "__FOOT__": foot}.items():
        page = page.replace(k, v)
    return page


def release(result):
    """Write CSS, specimen, QA report and README next to the fonts. Returns (fails, warns)."""
    from fontTools.ttLib import TTFont
    out = result["out"]
    fonts = os.path.join(out, "fonts")
    log = result["log"]
    ttf = next(f for f in result["fonts"] if f.endswith(".ttf"))
    cps = sorted(TTFont(ttf).getBestCmap())
    chars = [chr(c) for c in cps if c > 0x20 and c != 0xA0]

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
    with open(os.path.join(fonts, "specimen.html"), "w") as f:
        f.write(specimen(result, chars))
    spec = result["spec"]
    ws = result["weights"]
    readme = [f"# {result['family']}", "", spec.get("description", "An original typeface."), "",
              f"- Weights: {', '.join(f'{WEIGHT_NAME.get(w, w)} ({w})' for w in ws)}" + (" plus a variable font (wght axis)" if result["variable"] else ""),
              f"- {len(chars)} characters: Basic Latin, Latin-1 and Latin Extended-A accents, punctuation, currency",
              "- OpenType features: kerning, tabular figures (tnum), slashed zero (zero), alternate a (ss01), case-sensitive forms (case)",
              "", "## Files", "", "- `variable/` one file, every weight (best for the web)" if result["variable"] else "",
              "- `ttf/`, `otf/` desktop fonts: install these", "- `webfonts/` WOFF2 for websites",
              f"- `{result['family_id']}.css` ready-made @font-face rules", "- `specimen.html` open in a browser to test the fonts", "",
              "## Use on a website", "", "```html", f'<link rel="stylesheet" href="{result["family_id"]}.css">',
              f"<style>body {{ font-family: \"{result['family']}\", sans-serif; }}</style>", "```", "",
              "## License", "", spec.get("license") or "No license set. All rights reserved by the designer until one is added.", "",
              f"Built {datetime.date.today().isoformat()} with Punchcutter."]
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
    log.note("fonts/specimen.html, fonts/%s.css, fonts/README.md, report.md, design.json" % result["family_id"])
    return fails, warns
