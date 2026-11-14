---
title: CLI reference
lede: Every command, for scripts, CI and people who prefer a terminal.
---

Run `punchcutter <command>` after installing with pip, or `python skills/punchcutter/scripts/punchcutter.py <command>` from a clone.

## Making fonts from a brief

| Command | What it does |
| --- | --- |
| `menu` | print the five routes |
| `presets` | list presets and every design parameter with its default |
| `new "Family" --preset P --weights 300,400,700` | write a starter spec |
| `build spec.json` | the full pipeline: fonts, CSS, Studio, QA report |
| `build spec.json --draft` | fast pass: static TTFs and the proof only |
| `build spec.json --out DIR` | choose the output folder (default `build/<Family>`) |
| `glyph spec.json a g R` | close-up image of letters at every master weight |
| `glyph spec.json Q --outline` | outlines instead of filled shapes |

`build` exits with status 1 if a quality check fails, so it can gate a CI job.

## Making fonts from photos

| Command | What it does |
| --- | --- |
| `sheet --out DIR` | write the printable handwriting sheets (PDF plus PNG previews) |
| `read-sheet p1.jpg p2.jpg --family "Name"` | photos of filled sheets to a font project |
| `segment photo.jpg --out DIR` | find characters in any photo; writes a numbered `segments.png` |
| `label DIR --family "Name" --text "Hamburg"` | name every box in order and make the project |
| `label DIR --family "Name" --map '{"1":"H","2":"a"}'` | name only some boxes |

Both `read-sheet` and `label` accept:

| Option | Effect |
| --- | --- |
| `--weights 400,700` | extra weights, grown from the same strokes |
| `--neat 0..1` | 0 keeps every wobble, 1 lines letters up like type (default 0.5) |
| `--ink N` | heavier (+) or lighter (-) strokes, in font units |
| `--designer "Name"` | written into the font's name table |
| `--out DIR` | project folder (default: the family name) |

Then build the project's spec like any other.

## Running as a server

| Command | What it does |
| --- | --- |
| `mcp` | run the MCP server on stdio |

## The spec file

```json
{
  "family": "Ledger",
  "version": "1.000",
  "designer": "Your Name",
  "description": "A calm grotesque for interfaces.",
  "license": "SIL Open Font License 1.1",
  "preset": "grotesque",
  "weights": [300, 400, 700],
  "glyphs": "ledger_glyphs.py",
  "design": { "xh": 530, "aperture": 0.3, "spacing": 0.97 }
}
```

Every key under `design` is listed in [Design parameters](parameters.html). `glyphs` points at an optional file of custom drawings; see [Drawing letters](drawing.html).
