"""Punchcutter Studio: one self-contained HTML file that is the font's home.

Type tester, weight slider, feature switches, waterfall, glyph inspector,
install instructions and a download of the whole family. Every font is
embedded, so the file works offline, as an email attachment, or published
as an app inside Claude.
"""
from __future__ import annotations

import base64
import io
import json
import os
import zipfile

from . import brand
from .presets import WEIGHT_NAME


def _b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _zip(fonts_dir, fid):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(fonts_dir):
            for fn in files:
                if fn == "studio.html":
                    continue
                full = os.path.join(root, fn)
                z.write(full, os.path.join(fid, os.path.relpath(full, fonts_dir)))
    return base64.b64encode(buf.getvalue()).decode()


def _field_b64(meadow=False):
    from PIL import Image
    buf = io.BytesIO()
    Image.fromarray(brand.field(1400, 640, "meadow" if meadow else "haze", seed=4, grain=14)).save(buf, "JPEG", quality=78)
    return base64.b64encode(buf.getvalue()).decode()


def glyph_table(ttf):
    from fontTools.ttLib import TTFont
    import unicodedata
    f = TTFont(ttf)
    cmap = f.getBestCmap()
    out = []
    for cp, name in sorted(cmap.items()):
        if cp <= 0x20 or cp == 0xA0:
            continue
        try:
            uname = unicodedata.name(chr(cp)).title()
        except ValueError:
            uname = name
        out.append([chr(cp), f"U+{cp:04X}", uname, f["hmtx"][name][0]])
    os2 = f["OS/2"]
    metrics = dict(upm=f["head"].unitsPerEm, asc=os2.sTypoAscender, desc=os2.sTypoDescender,
                   cap=getattr(os2, "sCapHeight", 700), xh=getattr(os2, "sxHeight", 500))
    feats = set()
    for tag in ("GSUB", "GPOS"):
        if tag in f:
            feats |= {r.FeatureTag for r in f[tag].table.FeatureList.FeatureRecord}
    return out, metrics, sorted(feats)


def build_studio(result, qa=None):
    fam, fid = result["family"], result["family_id"]
    fonts = os.path.join(result["out"], "fonts")
    ws = result["weights"]
    reg = 400 if 400 in ws else ws[len(ws) // 2]
    faces = []
    if result["variable"]:
        vf = os.path.join(fonts, "webfonts", f"{fid}[wght].woff2")
        faces.append(dict(src=_b64(vf), weight=f"{min(result['masters'])} {max(result['masters'])}"))
    else:
        for w in ws:
            p = os.path.join(fonts, "webfonts", f"{fid}-{WEIGHT_NAME.get(w, w)}.woff2")
            if os.path.exists(p):
                faces.append(dict(src=_b64(p), weight=str(w)))
    ttf = os.path.join(fonts, "ttf", f"{fid}-{WEIGHT_NAME.get(reg, reg)}.ttf")
    glyphs, metrics, feats = glyph_table(ttf)
    spec = result["spec"]
    data = dict(family=fam, id=fid, version=spec.get("version", "1.000"), designer=spec.get("designer", ""),
                description=spec.get("description") or "An original typeface.", license=spec.get("license") or "All rights reserved",
                weights=[[w, WEIGHT_NAME.get(w, str(w))] for w in ws], variable=result["variable"],
                range=[min(result["masters"]), max(result["masters"])], regular=reg, glyphs=glyphs, metrics=metrics,
                features=feats, qa=qa or "", source=("handwriting" if spec.get("mode") == "handwriting" else spec.get("preset", "custom")),
                tool=f"{brand.NAME} {brand.VERSION}")
    face_css = "\n".join(
        f'@font-face{{font-family:"PCX";src:url(data:font/woff2;base64,{f["src"]}) format("woff2");font-weight:{f["weight"]};font-display:block}}'
        for f in faces)
    page = STUDIO.replace("/*FACES*/", face_css).replace("__DATA__", json.dumps(data))
    page = page.replace("__ZIP__", _zip(fonts, fid)).replace("__MARK__", brand.mark(0, 0, 32))
    word, ww = brand.wordmark(0, 17, 21, fill="currentColor")
    page = page.replace("__WORD__", word).replace("__WMW__", f"{ww:.0f}")
    page = page.replace("__GRAIN__", brand.grain_css(0.14)).replace("__FIELD__", _field_b64(spec.get("mode") == "handwriting"))
    page = page.replace("/*VARS*/", brand.css_vars()).replace("__SITE__", brand.SITE)
    page = page.replace("__FAVICON__", base64.b64encode(brand.favicon_svg().encode()).decode())
    page = page.replace("__TITLE__", brand.esc(fam)).replace("__BRANDFONT__", _b64(brand.font_path("Regular")))
    page = page.replace("__BRANDBOLD__", _b64(brand.font_path("ExtraBold")))
    path = os.path.join(fonts, "studio.html")
    with open(path, "w") as f:
        f.write(page)
    return path


STUDIO = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · Punchcutter Studio</title>
<link rel="icon" href="data:image/svg+xml;base64,__FAVICON__">
<style>
/*FACES*/
@font-face{font-family:"PCUI";src:url(data:font/ttf;base64,__BRANDFONT__);font-weight:400}
@font-face{font-family:"PCUI";src:url(data:font/ttf;base64,__BRANDBOLD__);font-weight:800}
/*VARS*/
*{box-sizing:border-box;margin:0}html{-webkit-text-size-adjust:100%}
body{background:var(--bg) __GRAIN__;color:var(--fg);font:15px/1.45 PCUI,system-ui,sans-serif;transition:background .25s,color .25s}
button,select,input{font:inherit;color:inherit}
.pc{font-family:"PCX",sans-serif;font-weight:var(--w,400)}
header{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:12px;padding:12px clamp(16px,4vw,40px);background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header svg{width:30px;height:30px;flex:none}header .sub{color:var(--mute)}
header .sp{flex:1}.btn{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:9px 18px;cursor:pointer;white-space:nowrap}
.btn.pri{background:var(--acc);border-color:var(--acc);color:var(--acc_fg);font-weight:800}.btn:hover{border-color:var(--fg)}
main{max-width:1240px;margin:0 auto;padding:0 clamp(16px,4vw,40px) 80px}
.hero{margin:clamp(16px,3vw,28px) 0 10px;border-radius:var(--r);overflow:hidden;position:relative;min-height:min(72vh,620px);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px 24px;background:linear-gradient(rgba(20,24,12,.18),rgba(20,24,12,.28)),#5f6b2f url(data:image/jpeg;base64,__FIELD__) center/cover;color:#fff;text-shadow:0 1px 18px rgba(20,24,12,.25)}
.hero h1{font-size:clamp(56px,12vw,170px);line-height:.95;letter-spacing:-.01em;overflow-wrap:anywhere;text-shadow:0 2px 30px rgba(0,0,0,.18)}
.hero p{max-width:30em;font-size:clamp(16px,1.8vw,20px);opacity:.92;margin-top:18px}
.hero .chips{justify-content:center}.hero .chip{border-color:rgba(255,255,255,.55);background:rgba(255,255,255,.08);backdrop-filter:blur(6px)}
.hero .chip.ok{border-color:#fff;color:#fff}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}.chip{border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:13px}
.chip.ok{border-color:var(--olive);color:var(--olive)}
section{border-top:1px solid var(--line);padding:clamp(40px,6vw,64px) 0}
h2{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);font-weight:400;margin-bottom:20px}
.ctl{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center;margin-bottom:22px;font-size:13px;color:var(--mute)}
.ctl label{display:flex;align-items:center;gap:8px}.ctl input[type=range]{accent-color:var(--acc);width:130px}
.tog{border:1px solid var(--line);border-radius:999px;padding:4px 11px;cursor:pointer;user-select:none}.tog.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
#t{outline:none;font-size:96px;line-height:1.08;min-height:1.1em;overflow-wrap:anywhere}
.wf div{white-space:nowrap;overflow:hidden;text-overflow:clip;line-height:1.25;padding:3px 0}.wf span{font:12px PCUI;color:var(--mute);display:inline-block;width:46px}
.wt{display:flex;align-items:baseline;gap:20px;border-bottom:1px solid var(--line);padding:10px 0;white-space:nowrap;overflow:hidden}
.wt span{font-size:12px;color:var(--mute);width:120px;flex:none}.wt div{font-size:clamp(28px,5vw,60px)}
.gl{display:grid;grid-template-columns:repeat(auto-fill,minmax(58px,1fr));border-left:1px solid var(--line);border-top:1px solid var(--line)}
.gl div{aspect-ratio:1;display:grid;place-items:center;font-size:28px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);cursor:pointer}
.gl div:hover,.gl div.sel{background:var(--fg);color:var(--bg)}
.insp{display:grid;grid-template-columns:minmax(260px,1fr) 1fr;gap:28px;margin-bottom:26px}
.big{position:relative;height:340px;background:var(--card);border:1px solid var(--line);border-radius:24px;overflow:hidden}
.big .g{position:absolute;left:50%;transform:translateX(-50%);line-height:1}.big i{position:absolute;left:0;right:0;border-top:1px dashed var(--line)}
.big i b{position:absolute;right:8px;top:-17px;font:11px PCUI;color:var(--mute);font-style:normal;font-weight:400}.big i.bl{border-top:1px solid var(--acc)}
.meta{font-size:14px}.meta div{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding:9px 0}.meta span{color:var(--mute)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:30px}.cols p{line-height:1.5}
pre{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;overflow:auto;font:13px/1.5 ui-monospace,Menlo,monospace}
.use{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}.use h3{font-size:18px;margin-bottom:8px}.use ol{padding-left:18px;color:var(--mute)}
footer{border-top:1px solid var(--line);padding:26px 0;color:var(--mute);font-size:13px;display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between}
@media(max-width:720px){.insp{grid-template-columns:1fr}#t{font-size:56px}header .sub{display:none}}
</style></head><body>
<header><svg viewBox="0 0 32 32">__MARK__</svg><svg viewBox="0 0 __WMW__ 22" style="height:19px;width:auto">__WORD__</svg><span class="sub">studio</span><span class="sp"></span>
<button class="btn" id="theme">Dark</button><button class="btn pri" id="dl">Download family</button></header>
<main>
<div class="hero"><h1 class="pc" id="name"></h1><p id="desc"></p><div class="chips" id="chips"></div></div>
<section><h2>Type tester</h2><div class="ctl" id="ctl"></div>
<div id="t" class="pc" contenteditable spellcheck="false">Quick wafting zephyrs vex bold Jim. 0123456789</div></section>
<section><h2>Waterfall</h2><div class="wf pc" id="wf"></div></section>
<section><h2>Weights</h2><div id="wts"></div></section>
<section><h2>Text</h2><div class="cols pc" id="txt"></div></section>
<section><h2>Glyphs</h2><div class="insp"><div class="big" id="big"></div><div class="meta" id="meta"></div></div><div class="gl pc" id="gl"></div></section>
<section><h2>Use it</h2><div class="use">
<div><h3>On your computer</h3><ol><li>Download the family and unzip it.</li><li>Open <code>ttf</code> (or <code>otf</code>) and double-click each file.</li><li>Click Install. It appears in every app.</li></ol></div>
<div><h3>On a website</h3><ol><li>Copy the <code>webfonts</code> folder and the CSS file to your site.</li><li>Add the rules below, then set <code>font-family</code>.</li></ol><pre id="css"></pre><button class="btn" id="copy" style="margin-top:10px">Copy CSS</button></div>
</div></section>
<footer><span id="foot"></span><span>Cut with Punchcutter · __SITE__</span></footer>
</main>
<script>
const D=__DATA__, Z="__ZIP__";
const $=s=>document.querySelector(s), el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const topW=D.weights[D.weights.length-1][0];
$('#name').textContent=D.family;$('#name').style.setProperty('--w',topW);$('#desc').textContent=D.description;
[[D.glyphs.length+' glyphs'],[D.weights.length+(D.weights.length>1?' weights':' weight')],[D.variable?'Variable font':'Static fonts'],[D.features.length+' OpenType features'],[D.source==='handwriting'?'From handwriting':'Preset: '+D.source],[D.qa,'ok']]
 .filter(c=>c[0]).forEach(c=>$('#chips').append(el('span','chip '+(c[1]||''),esc(c[0]))));
const st={size:96,w:D.regular,track:0,lh:1.08,f:new Set(),kern:true};
const t=$('#t');
function apply(){t.style.fontSize=st.size+'px';t.style.setProperty('--w',st.w);t.style.letterSpacing=st.track/1000+'em';t.style.lineHeight=st.lh;
 const fs=[...st.f].map(f=>'"'+f+'" 1');if(!st.kern)fs.push('"kern" 0');t.style.fontFeatureSettings=fs.join(',')||'normal';
 document.querySelectorAll('#wf div').forEach(d=>d.style.setProperty('--w',st.w))}
function range(label,min,max,step,key,fmt){const l=el('label');const i=el('input');Object.assign(i,{type:'range',min,max,step,value:st[key]});
 const v=el('b','',fmt(st[key]));i.oninput=()=>{st[key]=+i.value;v.textContent=fmt(st[key]);apply()};l.append(label,i,v);$('#ctl').append(l)}
range('Size',12,220,1,'size',v=>v+'px');
if(D.variable)range('Weight',D.range[0],D.range[1],1,'w',v=>v);
else{const l=el('label','', 'Weight ');const s=el('select');D.weights.forEach(([w,n])=>{const o=el('option','',n);o.value=w;if(w==D.regular)o.selected=true;s.append(o)});s.onchange=()=>{st.w=+s.value;apply()};l.append(s);$('#ctl').append(l)}
range('Tracking',-80,200,1,'track',v=>v);range('Line',0.8,1.8,0.01,'lh',v=>v.toFixed(2));
const names={tnum:'Tabular figures',zero:'Slashed zero',ss01:'Alternate a',case:'Case forms'};
Object.keys(names).filter(f=>D.features.includes(f)).forEach(f=>{const b=el('span','tog',names[f]);b.onclick=()=>{st.f.has(f)?st.f.delete(f):st.f.add(f);b.classList.toggle('on');apply()};$('#ctl').append(b)});
const kb=el('span','tog on','Kerning');kb.onclick=()=>{st.kern=!st.kern;kb.classList.toggle('on');apply()};$('#ctl').append(kb);
[72,48,36,24,18,14,12].forEach(s=>{const d=el('div','','<span>'+s+'px</span>'+esc('The five boxing wizards jump quickly. Sphinx of black quartz, judge my vow.'));d.style.fontSize=s+'px';$('#wf').append(d)});
D.weights.forEach(([w,n])=>{const r=el('div','wt');r.append(el('span','',n+' '+w));const g=el('div','pc','Hamburgefonstiv 0123');g.style.setProperty('--w',w);r.append(g);$('#wts').append(r)});
const TX='Type is the clothing words wear. A good typeface disappears while you read and leaves only the voice of the writer. Spacing is half of that work: the white between letters must feel as even as the black of the strokes.';
[[22,1.45],[17,1.5],[14,1.5]].forEach(([s,l])=>{const p=el('p','',TX);p.style.fontSize=s+'px';p.style.lineHeight=l;$('#txt').append(p)});
const M=D.metrics,span=(M.asc-M.desc)*1.18,big=$('#big');
function inspect(g,node){document.querySelectorAll('.gl .sel').forEach(n=>n.classList.remove('sel'));if(node)node.classList.add('sel');
 const h=big.clientHeight,px=h/span,base=h-(-M.desc*1.09)*px;big.innerHTML='';
 [['Ascender',M.asc],['Cap height',M.cap],['x-height',M.xh],['Baseline',0,'bl'],['Descender',M.desc]].forEach(([n,v,c])=>{const i=el('i',c||'','<b>'+n+'</b>');i.style.top=(base-v*px)+'px';big.append(i)});
 const s=el('div','g pc',esc(g[0]));s.style.fontSize=(M.upm*px)+'px';s.style.setProperty('--w',st.w);s.style.top=(base-(M.asc+(M.upm-(M.asc-M.desc))/2)*px)+'px';
 s.style.lineHeight=(M.asc-M.desc)/M.upm;s.style.top=(base-M.asc*px)+'px';big.append(s);
 $('#meta').innerHTML=[['Character',esc(g[0])],['Unicode',g[1]],['Name',esc(g[2])],['Advance width',g[3]+' units']].map(([a,b])=>'<div><span>'+a+'</span><b>'+b+'</b></div>').join('')}
D.glyphs.forEach(g=>{const c=el('div','',esc(g[0]));c.title=g[1]+' '+g[2];c.onclick=()=>inspect(g,c);$('#gl').append(c)});
const css=D.variable?'@font-face {\n  font-family: "'+D.family+'";\n  src: url("webfonts/'+D.id+'[wght].woff2") format("woff2");\n  font-weight: '+D.range[0]+' '+D.range[1]+';\n  font-display: swap;\n}'
 :D.weights.map(([w,n])=>'@font-face {\n  font-family: "'+D.family+'";\n  src: url("webfonts/'+D.id+'-'+n+'.woff2") format("woff2");\n  font-weight: '+w+';\n  font-display: swap;\n}').join('\n\n');
$('#css').textContent=css+'\n\nbody { font-family: "'+D.family+'", sans-serif; }';
$('#copy').onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText($('#css').textContent);$('#copy').textContent='Copied'};
$('#dl').onclick=()=>{const b=atob(Z),a=new Uint8Array(b.length);for(let i=0;i<b.length;i++)a[i]=b.charCodeAt(i);
 const u=URL.createObjectURL(new Blob([a],{type:'application/zip'}));const l=el('a');l.href=u;l.download=D.id+'.zip';document.body.append(l);l.click();l.remove()};
const isDark=()=>{const t=document.documentElement.dataset.theme;return t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches};
const setTheme=t=>{document.documentElement.dataset.theme=t;$('#theme').textContent=t==='dark'?'Light':'Dark';try{localStorage.setItem('pc-theme',t)}catch(e){}};
$('#theme').onclick=()=>setTheme(isDark()?'light':'dark');
try{const t=localStorage.getItem('pc-theme');if(t)setTheme(t);else $('#theme').textContent=isDark()?'Light':'Dark'}catch(e){}
$('#foot').textContent=D.family+' v'+D.version+(D.designer?' · '+D.designer:'')+' · '+D.license+' · '+D.tool;
apply();document.fonts.ready.then(()=>inspect(D.glyphs.find(g=>g[0]==='g')||D.glyphs[0],null));
window.addEventListener('resize',()=>{const s=document.querySelector('.gl .sel');inspect(D.glyphs.find(g=>g[0]===(s?s.textContent:'g'))||D.glyphs[0],s)});
</script></body></html>
"""
