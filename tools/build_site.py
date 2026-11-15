"""Build the GitHub Pages site into docs/.

    python tools/build_site.py            (after building the example families into build/)

Pages come from site/content/*.md. Colours, type and the mark come from
pc/brand.py, the same source the Studio, proofs and sheets use.
"""
import base64
import html
import os
import re
import shutil
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "punchcutter", "scripts"))
from pc import brand  # noqa: E402

OUT = os.path.join(ROOT, "docs")
CONTENT = os.path.join(ROOT, "site", "content")
REPO = "https://github.com/byrishi/punchcutter"

NAV = [("Start", [("getting-started", "Getting started"), ("routes", "The six routes")]),
       ("Guides", [("handwriting", "Handwriting and photos"), ("parameters", "Design parameters"),
                   ("drawing", "Drawing letters"), ("critique", "Critique checklist")]),
       ("Reference", [("agents", "Claude, MCP and agents"), ("cli", "CLI reference"), ("brand", "Brand"), ("privacy", "Privacy and usage stats"), ("faq", "FAQ and limits")])]
PAGES = [slug for _, items in NAV for slug, _ in items]
TITLES = {slug: t for _, items in NAV for slug, t in items}
FAMILIES = [("Burin Grotesk", "BurinGrotesk", "A calm neo-grotesque", 800), ("Pomelo Round", "PomeloRound", "Soft and friendly", 700),
            ("Quarry Slab", "QuarrySlab", "Sturdy slab serif", 700), ("Semaphore Condensed", "SemaphoreCondensed", "Tall, narrow, loud", 800),
            ("Lumen Contrast", "LumenContrast", "High-contrast display sans", 700),
            ("Kiln Sans", "KilnSans", "Open-base remix of Roboto Flex (OFL)", 800)]

CSS = """
@font-face{font-family:Burin;src:url(assets/fonts/BurinGrotesk-Regular.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:Burin;src:url(assets/fonts/BurinGrotesk-ExtraBold.woff2) format("woff2");font-weight:800;font-display:swap}
@font-face{font-family:Pomelo;src:url(assets/fonts/PomeloRound-Bold.woff2) format("woff2");font-display:swap}
__VARS__
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 Burin,system-ui,sans-serif}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;background:__GRAIN__;mix-blend-mode:multiply;opacity:.5}
a{color:inherit;text-decoration-color:var(--sage);text-underline-offset:3px}a:hover{text-decoration-color:var(--acc)}
img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(18px,4vw,40px)}
nav.top{position:sticky;top:0;z-index:40;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
nav.top .wrap{display:flex;align-items:center;gap:22px;height:64px}
nav.top .logo{display:flex;align-items:center;gap:10px;text-decoration:none;font:22px Pomelo;letter-spacing:-.01em}
nav.top .logo svg{width:30px;height:30px}nav.top .sp{flex:1}
nav.top a.l{text-decoration:none;color:var(--mute);font-size:15px}nav.top a.l:hover,nav.top a.l.on{color:var(--fg)}
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:12px 22px;text-decoration:none;font-weight:800;font-size:16px;border:1px solid var(--line);background:var(--card);color:var(--fg)}
.btn.pri{background:var(--acc);border-color:var(--acc);color:var(--acc_fg)}.btn:hover{border-color:var(--fg)}
.btn.sm{padding:7px 14px;font-size:14px}
.cap{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:0 0 14px}
h1,h2,h3{line-height:1.12;letter-spacing:-.015em;font-weight:800}
.hero{margin:22px 0 0;border-radius:var(--r);overflow:hidden;position:relative;color:#fff;text-align:center;
 background:linear-gradient(rgba(20,24,12,.16),rgba(20,24,12,.30)),var(--olive,#5f6b2f) url(assets/field-haze.jpg) center/cover;
 padding:clamp(80px,14vw,170px) 24px clamp(60px,10vw,120px)}
.hero svg.m{width:clamp(64px,8vw,96px);height:auto;margin:0 auto 18px;display:block}
.hero h1{font:400 clamp(44px,13vw,168px)/0.95 Pomelo;margin:0;letter-spacing:-.02em}
.hero p{font-size:clamp(18px,2.2vw,24px);margin:18px auto 30px;max-width:30em;opacity:.95}
.hero .btn{border-color:rgba(255,255,255,.5);background:rgba(255,255,255,.12);color:#fff;backdrop-filter:blur(6px)}
.hero .btn.pri{background:#fff;color:#1d2416;border-color:#fff}
.hero .row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.hero small{display:block;margin-top:clamp(40px,7vw,80px);font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.85}
section.s{padding:clamp(56px,8vw,96px) 0;border-bottom:1px solid var(--line)}
section.s h2{font-size:clamp(32px,4.4vw,52px);margin:0 0 14px;max-width:16em}
section.s .lead{font-size:clamp(17px,1.8vw,20px);color:var(--mute);max-width:36em;margin:0 0 36px}
.grid{display:grid;gap:18px}.g5{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.g3{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}.g2{grid-template-columns:repeat(auto-fit,minmax(380px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:24px}
.card .n{font:28px Pomelo;color:var(--acc)}.card h3{font-size:20px;margin:10px 0 6px}.card p{margin:0;color:var(--mute);font-size:15px}
figure{margin:0}figure img{border-radius:var(--r);border:1px solid var(--line)}figcaption{font-size:13px;color:var(--mute);margin-top:10px}
.fam{display:block;text-decoration:none;border-top:1px solid var(--line);padding:22px 0}
.fam .t{font-size:clamp(40px,7vw,88px);line-height:1.02;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fam .m{display:flex;justify-content:space-between;color:var(--mute);font-size:14px;margin-top:6px}
.fam:hover .m b{color:var(--acc)}
.tester{width:100%;font:inherit;font-size:16px;padding:14px 20px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--fg);margin-bottom:10px}
ol.stages{list-style:none;padding:0;margin:0;counter-reset:s;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:0 28px}
ol.stages li{counter-increment:s;border-top:1px solid var(--line);padding:16px 0}
ol.stages li:before{content:counter(s) "/9";font:15px Pomelo;color:var(--acc);margin-right:12px}ol.stages b{font-weight:800}ol.stages span{display:block;color:var(--mute);font-size:14px;margin-top:4px}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}.tabs button{font:inherit;font-size:15px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:999px;padding:8px 16px;cursor:pointer}
.tabs button.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}.pane{display:none}.pane.on{display:block}
pre{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 20px;overflow:auto;font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;margin:0 0 18px}
code{font:.88em ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:1px 6px}pre code{border:0;padding:0;background:none;font-size:inherit}
footer.f{padding:48px 0 70px;color:var(--mute);font-size:14px}footer.f .wrap{display:flex;gap:24px;flex-wrap:wrap;align-items:center;justify-content:space-between}
footer.f .logo{display:flex;gap:10px;align-items:center;font:20px Pomelo;color:var(--fg)}footer.f svg{width:26px;height:26px}
/* docs */
.doc{display:grid;grid-template-columns:230px minmax(0,1fr);gap:56px;padding:40px 0 80px}
.side{position:sticky;top:88px;align-self:start;font-size:15px}.side h4{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:22px 0 8px;font-weight:400}
.side a{display:block;text-decoration:none;color:var(--mute);padding:5px 0}.side a.on,.side a:hover{color:var(--fg)}.side a.on{font-weight:800}
.prose{max-width:760px}.prose h1{font-size:clamp(36px,5vw,56px);margin:0 0 12px}.prose .lede{font-size:20px;color:var(--mute);margin:0 0 34px}
.prose h2{font-size:28px;margin:48px 0 12px;padding-top:12px}.prose h3{font-size:20px;margin:30px 0 8px}
.prose table{width:100%;border-collapse:collapse;margin:0 0 22px;font-size:15px}.prose th,.prose td{text-align:left;padding:10px 12px 10px 0;border-bottom:1px solid var(--line);vertical-align:top}
.prose th{font-weight:800}.prose li{margin:4px 0}
.pn{display:flex;justify-content:space-between;gap:16px;margin-top:56px;border-top:1px solid var(--line);padding-top:22px}
.pn a{text-decoration:none}.pn small{display:block;color:var(--mute);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.swatches{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:0 0 28px}
.swatches div{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:var(--card);font-size:14px}
.swatches div:before{content:"";display:block;height:84px;background:var(--c)}.swatches b,.swatches span,.swatches em{display:block;padding:0 14px}
.swatches b{padding-top:10px}.swatches span{color:var(--mute);font-family:ui-monospace,monospace;font-size:13px}.swatches em{font-style:normal;color:var(--mute);padding-bottom:12px;font-size:13px}
.theme{cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:999px;width:36px;height:36px;display:grid;place-items:center;padding:0}
@media(max-width:860px){.doc{grid-template-columns:1fr}.side{position:static;display:flex;flex-wrap:wrap;gap:0 18px}.side h4{width:100%}nav.top a.l.hide{display:none}.g2{grid-template-columns:1fr}}
"""

# Privacy-friendly analytics: no cookies, no session recording, no personal data.
POSTHOG_KEY = "phc_OP89N6nuHWu48k3n7j2fhFcA2y51GODeJGMJgRZgPbv"
ANALYTICS = r"""<script>
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init("__KEY__",{api_host:"https://us.i.posthog.com",persistence:"memory",disable_session_recording:true,person_profiles:"identified_only",autocapture:true});
posthog.register({app:"punchcutter",surface:"docs"});
(function(){var q=new URLSearchParams(location.search),r=q.get("ref")||q.get("utm_source");if(r)posthog.capture("pc_docs_arrival",{ref:r,campaign:q.get("utm_campaign")||""});})();
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a");if(!a)return;var h=a.getAttribute("href")||"";
if(/\.(skill|pdf|zip)$|studio\.html|github\.com/.test(h))posthog.capture("pc_docs_link",{href:h,kind:/github/.test(h)?"github":/studio/.test(h)?"studio":"download"});});
document.addEventListener("copy",function(){var s=String(getSelection()||"").slice(0,80);if(/punchcutter|pip install|claude |npx |mcp/.test(s))posthog.capture("pc_docs_install_copied",{snippet:s.split("\n")[0]});});
</script>""".replace("__KEY__", POSTHOG_KEY)

THEME_JS = """<script>
(function(){var d=document.documentElement,t=null;try{t=localStorage.getItem('pc-theme')}catch(e){}if(t)d.dataset.theme=t;
window.pcTheme=function(){var dark=d.dataset.theme?d.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
d.dataset.theme=dark?'light':'dark';try{localStorage.setItem('pc-theme',d.dataset.theme)}catch(e){}}})();
</script>"""


def mark_svg(color="currentColor", tile=True, cls=""):
    inner = brand.mark(0, 0, 100) if tile else brand.mark(0, 0, 100, color=color, bg=None)
    return f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true">{inner}</svg>'


def head(title, desc, depth=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://byrishi.github.io/punchcutter/assets/social.jpg"><meta property="og:url" content="https://byrishi.github.io/punchcutter/"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{brand.CREAM}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css">{THEME_JS}{ANALYTICS}</head><body>"""


def topnav(active=""):
    def link(href, label, key, extra=""):
        return f'<a class="l {extra}{" on" if key == active else ""}" href="{href}">{label}</a>'
    return (f'<nav class="top"><div class="wrap"><a class="logo" href="index.html">{mark_svg()}punchcutter</a><span class="sp"></span>'
            + link("getting-started.html", "Docs", "docs") + link("index.html#gallery", "Gallery", "gallery", "hide")
            + link("brand.html", "Brand", "brand", "hide") + link(REPO, "GitHub", "gh")
            + '<button class="theme" onclick="pcTheme()" aria-label="Switch light and dark"><svg viewBox="0 0 20 20" width="16" height="16">'
            '<circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M10 2.5a7.5 7.5 0 0 1 0 15z" fill="currentColor"/></svg></button></div></nav>')


def footer():
    return (f'<footer class="f"><div class="wrap"><span class="logo">{mark_svg()}punchcutter</span>'
            f'<span>A type foundry for Claude and other AI agents · v{brand.VERSION}</span>'
            f'<span><a href="getting-started.html">Docs</a> · <a href="{REPO}">GitHub</a> · MIT license</span></div></footer></body></html>')


def page(slug):
    with open(os.path.join(CONTENT, slug + ".md")) as f:
        src = f.read()
    meta = {}
    if src.startswith("---"):
        _, fm, src = src.split("---", 2)
        for line in fm.strip().splitlines():
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    title = meta.get("title") or re.search(r"^# (.+)$", src, re.M).group(1)
    src = re.sub(r"^# .+\n", "", src, count=1, flags=re.M) if "title" not in meta else src
    body = markdown.markdown(src, extensions=["tables", "fenced_code", "toc", "md_in_html"])
    body = re.sub(r'href="(?!https?:|#|assets/)([a-z-]+)\.md"', r'href="\1.html"', body)
    i = PAGES.index(slug)
    prev = f'<a href="{PAGES[i - 1]}.html"><small>Previous</small>{TITLES[PAGES[i - 1]]}</a>' if i else "<span></span>"
    nxt = f'<a href="{PAGES[i + 1]}.html" style="text-align:right"><small>Next</small>{TITLES[PAGES[i + 1]]}</a>' if i + 1 < len(PAGES) else "<span></span>"
    side = "".join(f"<h4>{g}</h4>" + "".join(f'<a href="{s}.html" class="{"on" if s == slug else ""}">{t}</a>' for s, t in items) for g, items in NAV)
    lede = f'<p class="lede">{html.escape(meta["lede"])}</p>' if meta.get("lede") else ""
    out = (head(f"{title} · Punchcutter", meta.get("lede", brand.TAGLINE)) + topnav("brand" if slug == "brand" else "docs")
           + f'<div class="wrap doc"><aside class="side">{side}</aside><main class="prose"><h1>{html.escape(title)}</h1>{lede}{body}'
           + f'<div class="pn">{prev}{nxt}</div>'
           + f'<p style="margin-top:28px;font-size:14px;color:var(--mute)"><a href="{REPO}/edit/main/site/content/{slug}.md">Edit this page</a></p></main></div>' + footer())
    with open(os.path.join(OUT, slug + ".html"), "w") as f:
        f.write(out)


def index(families):
    routes = "".join(f'<div class="card"><div class="n">{i}</div><h3>{t}</h3><p>{html.escape(d)}</p></div>'
                     for i, (_, t, d) in enumerate(brand.MENU, 1))
    faces = "".join(f'@font-face{{font-family:"F{fid}";src:url(fonts/{fid}/webfonts/{fid}[wght].woff2) format("woff2");font-weight:100 900}}'
                    for _, fid, _, _ in families)
    fams = "".join(f'<a class="fam" href="fonts/{fid}/studio.html"><div class="t" style="font-family:F{fid};font-weight:{w}" data-t>{html.escape(name)}</div>'
                   f'<div class="m"><span>{html.escape(name)} · {html.escape(desc)}</span><b>Open its Studio →</b></div></a>'
                   for name, fid, desc, w in families)
    stages = [("Brief", "a sentence becomes adjectives, a preset and a plan"), ("Drawing", "every letter built from pen strokes, or traced from your writing"),
              ("Spacing", "sidebearings from the white space around each shape"), ("Kerning", "every pair measured in 2D, merged into classes"),
              ("OpenType features", "kerning, tabular figures, slashed zero, case forms"), ("Sources", "UFO masters and a designspace"),
              ("Compile", "variable TTF, static TTF and OTF, WOFF2"), ("Quality assurance", "coverage, metrics, names and features checked on every file"),
              ("Release package", "Studio, CSS, README and report")]
    st = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in stages)
    install = {
        "Claude Code": "/plugin marketplace add byrishi/punchcutter\n/plugin install punchcutter@punchcutter\n\n# then\n/punchcutter",
        "Claude app": "1. Download punchcutter.skill\n2. Settings → Skills → upload it (code execution on)\n3. Say: make me a font",
        "ChatGPT": 'pip install "punchcutter[mcp] @ git+https://github.com/byrishi/punchcutter"\ncloudflared tunnel --url http://localhost:8000\npunchcutter mcp --http --public-url https://YOUR-TUNNEL\n\n# ChatGPT → Settings → Apps & Connectors → Advanced\n# → Developer mode → Create → https://YOUR-TUNNEL/mcp',
        "Codex": "npx skills add byrishi/punchcutter --agent codex\n\n# then in Codex\n$punchcutter\n\n# or as an MCP server\ncodex mcp add punchcutter -- punchcutter mcp",
        "MCP clients": 'pip install "punchcutter[mcp] @ git+https://github.com/byrishi/punchcutter"\n\n{\n  "mcpServers": {\n    "punchcutter": { "command": "punchcutter", "args": ["mcp"] }\n  }\n}',
        "Other agents": "git clone https://github.com/byrishi/punchcutter && cd punchcutter\npip install -r skills/punchcutter/scripts/requirements.txt\n\n# then ask your agent:\n# Follow AGENTS.md and make me a rounded friendly font",
        "Terminal": 'pip install "git+https://github.com/byrishi/punchcutter"\npunchcutter new "My Sans" --preset humanist\npunchcutter build MySans.json',
    }
    tabs = "".join(f'<button class="{"on" if i == 0 else ""}" data-p="{i}">{k}</button>' for i, k in enumerate(install))
    panes = "".join(f'<pre class="pane{" on" if i == 0 else ""}" data-p="{i}"><code>{html.escape(v)}</code></pre>' for i, v in enumerate(install.values()))
    out = head("Punchcutter · " + brand.TAGLINE, "A type foundry for Claude and other AI agents. Describe a typeface or send a photo of your handwriting; get a real font family.") + topnav()
    out += f"""<style>{faces}</style>
<div class="wrap"><header class="hero">{mark_svg("#fff", tile=False, cls="m")}<h1>punchcutter</h1>
<p>{brand.TAGLINE} Or write on paper and send a photo. A type foundry that lives inside Claude, ChatGPT, Codex and other AI agents.</p>
<div class="row"><a class="btn pri" href="getting-started.html">Get started</a><a class="btn" href="fonts/PomeloRound/studio.html">See a Studio</a><a class="btn" href="{REPO}">GitHub</a></div>
<small>Every letter on this page was cut by Punchcutter</small></header></div>

<section class="s"><div class="wrap"><p class="cap">Six ways in</p><h2>Start with a sentence, a sheet of paper or a picture.</h2>
<p class="lead">Open it and pick a route, or just say what you want. Every route ends with the same finished family and its Studio.</p>
<div class="grid g5">{routes}</div></div></section>

<section class="s" id="handwriting"><div class="wrap"><p class="cap">Your handwriting</p><h2>Write it. Photograph it. Type with it.</h2>
<p class="lead">Print the sheet and fill it in with a dark pen. Take a phone photo at any angle. Corner markers square it up, the red guides drop out, every letter is traced, and your x-height and stroke weight are measured. Anything you did not write is drawn to match.</p>
<div class="grid g3">
<figure><img src="assets/sheet-blank.png" alt="The blank Punchcutter handwriting sheet" loading="lazy"><figcaption>1 · Print the sheet. <a href="assets/punchcutter-handwriting-sheets.pdf">Download the PDF</a> (A4 and US Letter).</figcaption></figure>
<figure><img src="assets/demo-sheet-filled.jpg" alt="A filled-in handwriting sheet" loading="lazy"><figcaption>2 · Fill it in: one character per box, sitting on the red line. Page 1 is enough.</figcaption></figure>
<figure><img src="assets/demo-sheet-photo.jpg" alt="A phone photo of the filled sheet" loading="lazy"><figcaption>3 · Photograph it flat with all four corner squares in view, and send it.</figcaption></figure>
</div>
<figure style="margin-top:22px"><img src="assets/photo-to-font.jpg" alt="The photographed sheet and the font made from it" loading="lazy"><figcaption>4 · The result: a two-weight family with spacing, kerning and about 280 glyphs. (Demo writing is simulated.)</figcaption></figure>
<div class="grid g2" style="margin-top:56px;align-items:center">
<div><p class="cap">No printer?</p><h2 style="font-size:clamp(28px,3.4vw,40px)">Any paper works.</h2>
<p class="lead" style="margin-bottom:18px">Write on a notebook page, a napkin or a whiteboard and send the photo. Punchcutter finds and numbers each character, reads them, and traces them. "Sphinx of black quartz, judge my vow" covers a to z. The sheet still gives the cleanest result.</p>
<a class="btn sm" href="handwriting.html">Handwriting guide</a></div>
<figure><img src="assets/demo-plain-paper-found.jpg" alt="Characters found and numbered on a photo of plain paper" loading="lazy"><figcaption>Plain notebook paper, every character found and numbered.</figcaption></figure></div>
</div></section>

<section class="s" id="gallery"><div class="wrap"><p class="cap">Gallery</p><h2>Five families, each made from one sentence.</h2>
<p class="lead">Type below to set it in all five. Open any family to try its Studio: the app every Punchcutter font ships with.</p>
<input class="tester" id="tt" value="" placeholder="Type something…" aria-label="Sample text">{fams}</div></section>

<section class="s"><div class="wrap"><p class="cap">How it works</p><h2>The stages of a real type foundry, in a minute or two.</h2>
<p class="lead">Each stage reports what it did. Between drafts the AI looks at the proof, finds weak letters and fixes them, at least twice, before anything ships.</p>
<ol class="stages">{st}</ol></div></section>

<section class="s"><div class="wrap grid g2" style="align-items:center"><div><p class="cap">Studio</p><h2>Every font comes with its own app.</h2>
<p class="lead">Type tester, weight slider, feature switches, glyph inspector, install guide and a download button, in one file that works offline. In Claude it opens right in the chat.</p>
<a class="btn pri" href="fonts/PomeloRound/studio.html">Open a Studio</a></div>
<figure><img src="assets/studio.jpg" alt="Punchcutter Studio" loading="lazy"></figure></div></section>

<section class="s" id="install"><div class="wrap"><p class="cap">Install</p><h2>Works where you already work.</h2>
<p class="lead">A Claude skill, a Codex skill, an MCP server for ChatGPT, Claude Desktop, Cursor, Windsurf and VS Code, a guide for other agents, and a plain command line tool.</p>
<div class="tabs">{tabs}</div>{panes}<a class="btn sm" href="getting-started.html">Full install guide</a></div></section>
<script>
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button,.pane').forEach(e=>e.classList.toggle('on',e.dataset.p===b.dataset.p))}});
const tt=document.getElementById('tt'),names=[...document.querySelectorAll('[data-t]')].map(e=>e.textContent);
tt.oninput=()=>document.querySelectorAll('[data-t]').forEach((e,i)=>e.textContent=tt.value||names[i]);
</script>""" + footer()
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(out)


def assets(families):
    from fontTools.ttLib import TTFont
    a = os.path.join(OUT, "assets")
    os.makedirs(os.path.join(a, "fonts"), exist_ok=True)
    for style, name in (("Regular", "BurinGrotesk-Regular"), ("ExtraBold", "BurinGrotesk-ExtraBold"), ("RoundBold", "PomeloRound-Bold")):
        f = TTFont(brand.font_path(style))
        f.flavor = "woff2"
        f.save(os.path.join(a, "fonts", name + ".woff2"))
    css = CSS.replace("__VARS__", brand.css_vars()).replace("__GRAIN__", brand.grain_css(0.14))
    css = css.replace("url(assets/", "url(")
    with open(os.path.join(a, "site.css"), "w") as f:
        f.write(css)
    with open(os.path.join(a, "favicon.svg"), "w") as f:
        f.write(brand.favicon_svg())
    from PIL import Image
    Image.fromarray(brand.field(1800, 900, "haze", seed=4, grain=10)).save(os.path.join(a, "field-haze.jpg"), quality=80)
    for fn in ("social.jpg", "studio.jpg", "photo-to-font.jpg", "demo-sheet-filled.jpg", "demo-sheet-photo.jpg",
               "demo-plain-paper-found.jpg", "punchcutter-handwriting-sheets.pdf", "logo.svg", "logo.png"):
        shutil.copy(os.path.join(ROOT, "assets", fn), a)
    from pc.handwriting import sheet_svg
    import cairosvg
    cairosvg.svg2png(bytestring=sheet_svg(0).encode(), write_to=os.path.join(a, "sheet-blank.png"), output_width=1200)
    for _, fid, _, _ in families:
        src = os.path.join(ROOT, "build", fid, "fonts")
        dst = os.path.join(OUT, "fonts", fid)
        os.makedirs(os.path.join(dst, "webfonts"), exist_ok=True)
        shutil.copy(os.path.join(src, "studio.html"), dst)
        shutil.copy(os.path.join(src, "webfonts", f"{fid}[wght].woff2"), os.path.join(dst, "webfonts"))


def main():
    families = [f for f in FAMILIES if os.path.exists(os.path.join(ROOT, "build", f[1], "fonts", "studio.html"))]
    if len(families) < len(FAMILIES):
        sys.exit("Build the example families first: python skills/punchcutter/scripts/punchcutter.py build examples/<name>.json")
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    assets(families)
    index(families)
    for slug in PAGES:
        page(slug)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"site written to {OUT}: {len(PAGES) + 1} pages, {len(families)} Studios")


if __name__ == "__main__":
    main()
