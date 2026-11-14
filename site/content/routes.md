---
title: The five routes
lede: Five ways into the foundry. Each ends with the same finished family and its Studio.
---

When you open Punchcutter without saying what you want, it shows a menu:

```
✦ punchcutter  ·  type foundry

  1  Describe it        One sentence about the feeling you want. Get a full family.
  2  Your handwriting   Print the sheet, write on it, send a photo. The best photo route.
  3  Quick photo        A photo of any writing or lettering. No sheet needed.
  4  Match a mood       Send a picture you love. Get an original family with that feeling.
  5  Remix              Change a Punchcutter font: weight, width, spacing, single letters.
```

Pick a number, or just say what you want. If you attach a photo or write a brief, Punchcutter skips the menu.

## 1. Describe it

Write one sentence. Name the feeling, the use and, if you like, the name.

```
> condensed and loud, for a music festival poster, called Riot
> a soft rounded font for a kids' reading app
> something technical and squared-off for a hardware brand
```

Punchcutter turns the sentence into three adjectives, picks the closest of eight presets, sets the design parameters, and draws the family. It looks at the proof, fixes weak letters and redraws a few signature characters before it ships. You see each stage as it happens.

## 2. Your handwriting

The best way to turn your own writing into a font.

1. Ask for the sheet, or download it: [punchcutter-handwriting-sheets.pdf](assets/punchcutter-handwriting-sheets.pdf).
2. Print it. Write each character once, with a dark pen, sitting on the red line.
3. Photograph each page flat, with all four black corner squares in view. Any angle is fine.
4. Send the photos.

Punchcutter squares up the photo from the corner squares, removes the red guides, traces each letter, and measures your x-height and stroke weight. Anything you did not write (accents, symbols, currency) is drawn at your stroke weight, so the font is complete. Page 1 is enough; page 2 adds figures and punctuation.

You can then ask for changes in plain words: "neater", "keep it messy", "thicker", "add a bold". The full guide is [Handwriting](handwriting.html).

## 3. Quick photo

For a photo you already have: a note, a sign you painted, a whiteboard.

Punchcutter finds the characters, numbers them on an image, reads which is which, and traces them. The fewer letters in the photo, the more of the font is drawn by the engine, and it tells you how much came from your writing. The sentence "Sphinx of black quartz, judge my vow" covers a to z.

Only use lettering you made or own.

## 4. Match a mood

Send a picture you love: a place, a poster, a product, a painting. Punchcutter reads it for weight, width, contrast, roundness and energy, writes the brief, and designs an original family with that feeling. It never traces letters from the image.

## 5. Remix

Change a font made with Punchcutter.

| Say | What changes |
| --- | --- |
| bolder, lighter | stem weight, or another weight in the family |
| tighter, looser | spacing |
| friendlier, softer | roundness, round stroke ends |
| sharper, more serious | flat cuts, closed apertures, lower roundness |
| narrower, wider | width |
| redo the g | a custom drawing of that letter |

For handwriting fonts, remixing changes neatness and ink weight.

## What you get every time

| File | What it is |
| --- | --- |
| `studio.html` | the font's own app: tester, glyph inspector, install guide, download |
| `variable/` | one variable font with a weight axis (drawn fonts) |
| `ttf/`, `otf/` | desktop fonts |
| `webfonts/`, `<Family>.css` | WOFF2 and ready `@font-face` rules |
| `proof.png` | the proof sheet |
| `report.md` | every stage and every quality check |
| `sources/` | UFO masters for Glyphs, FontLab or RoboFont |
