"""Close-up renders of single glyphs, for the design-critique loop."""
from __future__ import annotations

from .build import load_overrides, load_spec, master_designs, resolve_design
from .context import G
from .glyphs_latin import GLYPHS


def _path(con):
    d = f"M{con.start[0]:.1f} {con.start[1]:.1f}"
    for s in con.segs:
        d += ("L%.1f %.1f" % s[1]) if s[0] == "l" else "C" + " ".join("%.1f %.1f" % p for p in s[1:])
    return d + "Z"


def render(spec_path, names, out, weight=None, cell=420, outline=False):
    spec = load_spec(spec_path)
    design = resolve_design(spec)
    load_overrides(spec)
    masters, _ = master_designs(spec, design)
    ws = [weight] if weight else list(masters)
    cols = len(names)
    W, H = cols * cell, len(ws) * cell * 1.15
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}"><rect width="100%" height="100%" fill="white"/>']
    for r, w in enumerate(ws):
        d = masters[w]
        sc = cell / 1250
        base = r * cell * 1.15 + cell * 0.86
        for y, c in ((0, "#e5482d"), (d["xh"], "#9cc"), (d["cap"], "#9cc"), (d["asc"], "#ddd"), (d["desc"], "#ddd")):
            o.append(f'<rect x="0" y="{base - y * sc:.1f}" width="{W}" height="1" fill="{c}"/>')
        o.append(f'<text x="8" y="{base - cell * 0.72:.0f}" font-family="monospace" font-size="15" fill="#888">wght {w}</text>')
        for i, n in enumerate(names):
            fn, uni, case = GLYPHS[n]
            g = G(d, case)
            fn(g)
            xs = [p[0] for c in g.shape.contours for p in c.flat(4)] or [0]
            cx = (min(xs) + max(xs)) / 2
            ox = i * cell + cell / 2
            style = 'fill="#e5482d22" stroke="#111" stroke-width="3"' if outline else 'fill="#111"'
            o.append(f'<g transform="translate({ox:.1f},{base:.1f}) scale({sc:.4f},{-sc:.4f}) translate({-cx:.1f},0)">'
                     f'<path d="{" ".join(_path(c) for c in g.shape.contours)}" fill-rule="nonzero" {style}/></g>')
    o.append("</svg>")
    import cairosvg
    cairosvg.svg2png(bytestring="".join(o).encode(), write_to=out, output_width=min(int(W), 1800))
    return out
