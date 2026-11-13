#!/usr/bin/env python3
"""Punchcutter: cut an original typeface from a design spec.

  punchcutter.py presets                       list the style presets
  punchcutter.py new "Family Name" --preset P  write a starter spec
  punchcutter.py build spec.json               run the full pipeline
  punchcutter.py glyph spec.json a g R         close-up of single glyphs
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser(prog="punchcutter", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("presets")
    n = sub.add_parser("new")
    n.add_argument("family")
    n.add_argument("--preset", default="geometric")
    n.add_argument("--weights", default="300,400,700")
    n.add_argument("--out", default=None)
    b = sub.add_parser("build")
    b.add_argument("spec")
    b.add_argument("--out", default=None, help="output folder (default: build/<Family>)")
    b.add_argument("--draft", action="store_true", help="fast pass: static TTFs and proof only")
    b.add_argument("--no-proof", action="store_true")
    g = sub.add_parser("glyph")
    g.add_argument("spec")
    g.add_argument("names", nargs="+")
    g.add_argument("--weight", type=int)
    g.add_argument("--outline", action="store_true")
    g.add_argument("--out", default="glyphs.png")
    a = ap.parse_args()

    if a.cmd == "presets":
        from pc.presets import PRESETS
        from pc.context import DEFAULTS
        for name, p in PRESETS.items():
            print(f"{name:10s} " + ", ".join(f"{k}={v}" for k, v in p.items()))
        print("\nAll parameters and defaults:")
        print(json.dumps(DEFAULTS, indent=2))
        return
    if a.cmd == "new":
        from pc.presets import PRESETS
        if a.preset not in PRESETS:
            sys.exit(f"Unknown preset. Choose from: {', '.join(PRESETS)}")
        spec = {"family": a.family, "version": "1.000", "designer": "", "description": "", "license": "",
                "preset": a.preset, "weights": [int(w) for w in a.weights.split(",")], "design": {}}
        path = a.out or (a.family.replace(" ", "") + ".json")
        with open(path, "w") as f:
            json.dump(spec, f, indent=2)
        print(f"wrote {path}")
        return
    if a.cmd == "glyph":
        from pc.inspect_glyph import render
        names = []
        for nme in a.names:
            names.extend(_names(nme))
        print("wrote", render(a.spec, names, a.out, a.weight, outline=a.outline))
        return
    if a.cmd == "build":
        from pc.build import build, load_spec
        from pc.release import release
        fam = load_spec(a.spec)["family"].replace(" ", "")
        out = a.out or os.path.join("build", fam)
        result = build(a.spec, out, formats=("ttf",) if a.draft else ("variable", "ttf", "otf", "woff2"))
        fails = 0
        if a.draft:
            result["log"].n = 7
        else:
            fails, warns = release(result)
        if not a.no_proof:
            from pc.proof import proof
            p = proof(result, os.path.join(out, "proof.svg"))
            print(f"\nproof: {p[:-4]}.png  (look at it before calling the font done)")
        print(f"output: {out}")
        sys.exit(1 if fails else 0)


def _names(token):
    """Accept glyph names (a, zero, ampersand) or a literal string of characters."""
    from pc.glyphs_latin import GLYPHS
    from pc import glyphs_extra  # noqa: F401
    if token in GLYPHS:
        return [token]
    by_uni = {v[1]: k for k, v in GLYPHS.items() if v[1]}
    out = [by_uni[ord(c)] for c in token if ord(c) in by_uni]
    if not out:
        sys.exit(f"no such glyph: {token}")
    return out


if __name__ == "__main__":
    main()
