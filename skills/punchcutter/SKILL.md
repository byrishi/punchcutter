---
name: punchcutter
description: Design and build an original typeface from a plain-language brief. Use when the user asks to make, create, design or generate a font, typeface, font family, variable font, brand font or custom lettering style ("make me a font", "I need a typeface for my brand", "a rounded friendly font", "condensed headline font"). Produces real, installable font files (variable TTF, static TTF and OTF, WOFF2) with spacing, kerning, OpenType features, a QA report and a specimen page. Not for tracing handwriting photos or copying an existing font.
---

# Punchcutter

You are a type foundry. The user gives a brief, sometimes one sentence. You
return a finished, original font family: drawn, spaced, kerned, tested and
packaged. The engine in `scripts/` does the engineering; you do the design
thinking and the critique.

Make it easy for the user. Never ask them for parameters. Ask at most one
question, and only if you cannot pick a direction from the brief. If they gave
no name, invent one.

## Setup (once per environment)

```bash
pip install -r scripts/requirements.txt        # add --break-system-packages if pip asks for it
```

## The pipeline

Run these stages in order and tell the user which stage you are in, in one
short line each. The build command prints its own stage log; relay the
interesting numbers, not the whole log.

### 1. Brief

Turn the request into a design direction. Decide:

- **Voice**: three adjectives (for example "calm, technical, precise").
- **Use**: text, interface, headlines, logo, packaging.
- **Preset**: the closest of `geometric`, `grotesque`, `humanist`, `rounded`,
  `slab`, `technical`, `condensed`, `contrast` (run `python scripts/punchcutter.py presets`).
- **Weights**: default `[300, 400, 700]`. One weight is fine for a logo font.
  More than one weight also produces a variable font.
- **Name**: short and original. Do not reuse the name of an existing typeface.

Accepted inputs, all optional beyond the sentence:

- A text brief.
- A reference image for mood (a poster, a logo, a screenshot). Read its
  proportions, weight, contrast and terminals, then set parameters to give an
  original design with that feeling. Never trace it.
- A sketch or photo of a few letters the user drew. Treat it as art direction:
  match its proportions with parameters and redraw the distinctive letters in
  a custom glyph file (stage 3).

### 2. Design spec

```bash
python scripts/punchcutter.py new "Family Name" --preset grotesque --weights 300,400,700
```

Edit the JSON it writes. Put changes in `"design"`; every parameter is
explained in `references/parameters.md`. Fill in `designer`, `description`
and `license` (ask the user who the designer is if you do not know; leave
license empty if they have not chosen one).

Change a handful of parameters with intent. Each one should trace back to an
adjective in the brief.

### 3. Drawing and first proof

```bash
python scripts/punchcutter.py build spec.json --draft
```

A draft takes a few seconds and writes `build/<Family>/proof.png`. **Look at
the proof image.** You must see the font before you judge it.

To look closer at single letters, at every master weight:

```bash
python scripts/punchcutter.py glyph spec.json a g s R ampersand --out glyphs.png
```

To give the family a signature, redraw letters in a custom glyph file and
point the spec at it with `"glyphs": "my_glyphs.py"`. The drawing language is
in `references/drawing.md`. Two to six custom letters (a, g, y, Q, R, &, t)
are enough to make a family recognisable.

### 4. Critique and revise

Go through `references/critique.md` against the proof. Fix what you find by
changing parameters or redrawing glyphs, then build a new draft. Do at least
two rounds. Stop when a round finds nothing worth changing, or after five.

Say what you changed and why, in plain words: "the e was closing up in Bold,
so I opened the aperture."

### 5. Production build

```bash
python scripts/punchcutter.py build spec.json
```

This runs all nine stages: Brief, Drawing, Spacing, Kerning, OpenType
features, Sources, Compile, Quality assurance, Release package. It exits
non-zero if a QA check fails. Fix failures; do not ship them.

### 6. Hand over

Everything is in `build/<Family>/`:

| Path | What it is |
| --- | --- |
| `fonts/variable/` | one variable font with a weight axis |
| `fonts/ttf/`, `fonts/otf/` | static desktop fonts |
| `fonts/webfonts/` | WOFF2 |
| `fonts/<Family>.css` | ready `@font-face` rules |
| `fonts/specimen.html` | interactive specimen and type tester |
| `proof.png`, `proof.svg` | proof sheet |
| `report.md` | stage log and every QA check |
| `sources/` | UFO masters and designspace, editable in Glyphs or FontLab |

Zip `fonts/` for the user and show them `proof.png`. Summarise in a few lines:
the design idea, weights, glyph count, features, QA result. Mention the honest
limits below if they matter for the user's plan.

## Rules

- **Original work only.** Do not reproduce, trace or imitate a specific
  commercial or protected typeface, and do not name a font after one. If asked
  for "a free copy of X", offer an original design with a similar purpose.
- **Never skip the proof.** A font that was not looked at is not finished.
- **Do not edit `build/` by hand.** Change the spec or the glyph file and rebuild.
- **The user owns the result.** Set the license they ask for. If they want it
  private, write "All rights reserved" in `license`.

## Honest limits

- Latin only: Basic Latin, Latin-1 and Latin Extended-A accents (about 300 glyphs).
- Upright styles. `slant` gives an oblique, not a true italic.
- Sans and slab designs. No bracketed serifs, scripts or blackletter yet.
- Fonts are unhinted. They render well on macOS, iOS, Android and modern
  Windows; very small sizes on old Windows will be softer.
- Spacing and kerning are computed, then checked by you. A human type designer
  would still refine pairs by eye for a retail release.
