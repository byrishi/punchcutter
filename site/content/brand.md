---
title: Brand
lede: A small hand-drawn mark in a wide, grainy, sun-washed field. Warm, plain, generous.
---

Everything Punchcutter makes uses these rules: the Studio, proof sheets, the handwriting sheet, this site and the repository images. They live in one place, [`pc/brand.py`](https://github.com/byrishi/punchcutter/blob/main/skills/punchcutter/scripts/pc/brand.py), and every output reads them from there.

## Colour

<div class="swatches">
<div style="--c:#5f6b2f"><b>Meadow</b><span>#5f6b2f</span><em>the accent: actions, the mark tile, baselines</em></div>
<div style="--c:#a9ae86"><b>Sage</b><span>#a9ae86</span><em>soft green, guides and link lines</em></div>
<div style="--c:#d8cc98"><b>Straw</b><span>#d8cc98</span><em>pale dry grass, warmth in fields</em></div>
<div style="--c:#cdd9dc"><b>Sky</b><span>#cdd9dc</span><em>haze at the top of fields</em></div>
<div style="--c:#f4efe4"><b>Cream</b><span>#f4efe4</span><em>paper, light background</em></div>
<div style="--c:#171612"><b>Ink</b><span>#171612</span><em>text</em></div>
<div style="--c:#161b10"><b>Night meadow</b><span>#161b10</span><em>dark background</em></div>
<div style="--c:#8b8578"><b>Stone</b><span>#8b8578</span><em>captions, quiet text</em></div>
</div>

Meadow is the only accent. Use it for one thing per view: the main button, the mark tile, the baseline in a glyph close-up. In dark mode the accent lifts to `#b5c27a`.

No orange or red in the brand. The one exception is functional: the guides on the handwriting sheet are printed in a pale red because that colour disappears when a photo is read, leaving only the ink.

## Type

| Role | Typeface | Notes |
| --- | --- | --- |
| Wordmark, display | Pomelo Round | always lowercase: punchcutter |
| Text, interface | Burin Grotesk | Regular for text, ExtraBold for emphasis |
| Captions | Burin Grotesk | uppercase, letter-spaced 0.12em, Stone |

Both typefaces were made with Punchcutter.

## The mark

A lowercase p drawn by hand, its stem long and leaning like the steel punch a punchcutter strikes, with a small spark where it cuts. It is drawn by the font engine's own pen, with a little wobble.

- White on fields and photographs, small, with lots of space around it.
- On Meadow as a rounded tile for app icons and favicons.
- In Ink on Cream for print.
- Never stretched, outlined, recoloured in other hues, or placed on a busy area of a field.

## Fields

The backgrounds are soft, out-of-focus landscapes with film grain: wild grass under a hazy sky, and olive hills in mist. They are generated from noise by `brand.field()`, not photographs, so there are no rights to clear. Put white type on them and keep it small and centred.

## Space and shape

- Generous margins. One idea per view.
- Corners: 26 px on cards and panels, fully round on buttons and chips.
- Lines: hairlines in Line `#ddd5c4`; no shadows.
- Grain: a light film grain over pages, never over text-heavy areas at full strength.

## Voice

Plain and warm, like a craftsperson talking. Short sentences. Name the stage, the number and the next step. No hype.
