---
title: FAQ and limits
lede: What Punchcutter is good at, what it is not, and who owns what.
---

## Who owns the fonts I make?

You do. Set any license you like in the spec's `license` field; it is written into the font. Leave it empty or write "All rights reserved" to keep a font private. The Punchcutter code is MIT licensed. The example families are released under the SIL Open Font License 1.1.

## Can it copy a commercial font so I don't have to buy it?

No, and it will decline. Punchcutter designs original typefaces. Asking for a font "like" a famous one gets you an original design for the same job, never a copy.

## How good are the fonts?

Solid, usable families: consistent weight and proportions, computed spacing and class kerning, real OpenType features, and every file passes the same sanitizer browsers use. A professional type designer would still refine individual curves and pairs by eye before a retail release. The UFO sources are included for that.

## Which languages are covered?

Latin: Basic Latin, Latin-1 and Latin Extended-A accents, which covers most European languages. Cyrillic, Greek, Devanagari and Gujarati are on the roadmap.

## Italics, serifs, monospace?

Not yet. Styles are upright; `slant` gives an oblique. Designs are sans and slab serif. True italics, bracketed serifs and monospace are on the roadmap.

## Will my handwriting font join up like cursive?

No. Handwriting fonts are print-style: each letter stands alone. Joined scripts are on the roadmap.

## Why is my handwriting font not variable?

Traced outlines cannot be interpolated reliably, so handwriting families ship as static weights. Drawn families ship as variable fonts.

## Do the fonts work on every system?

Yes: TTF and OTF for desktop apps, WOFF2 for the web. Outlines are unhinted, which is sharp on phones, macOS and modern Windows, and softer at very small sizes on old Windows.

## Does anything get uploaded?

Your fonts, text and photos never leave your machine, or Claude's own sandbox when you use the Claude app. Punchcutter sends a few anonymous usage counts (a build started, a Studio opened) with no content in them. [Privacy and usage stats](privacy.html) lists every one; `punchcutter telemetry off` stops them.

## How do I update Punchcutter?

Run the same install command again: `/plugin update punchcutter` in Claude Code, `npx skills add byrishi/punchcutter` for the skill, or `pip install -U "git+https://github.com/byrishi/punchcutter"` for the CLI and MCP server. In the Claude app, download the latest `punchcutter.skill` and upload it again. `punchcutter --version` shows what you have.

## Where do I report a bug?

[Open an issue](https://github.com/byrishi/punchcutter/issues) with the spec, the proof and `report.md`.
