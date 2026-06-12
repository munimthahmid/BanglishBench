# Script Matters — Thesis Defense Slides

**Build (must use LuaLaTeX for fontspec + Bengali script):**

```bash
lualatex main.tex
lualatex main.tex      # run twice so the frame count in the footer settles
```

Output: `main.pdf` — 26 pages, 16:9, ~11 min talk + 2 min Q&A.

## Files
- `main.tex` — all slide content (one file).
- `theme.tex` — custom navy/teal beamer theme, palette, fonts, helper boxes.

## Requirements
- LuaLaTeX with: `beamer`, `tikz`, `pgfplots`, `tcolorbox`, `booktabs`, `pifont`, `fontspec`.
- Fonts: **Liberation Sans** (body), **DejaVu Sans Mono** (code), **Noto Sans Bengali** (the `\bn{...}` Bengali text).

## Slide map (20 content slides)
1 Title · 2 Motivation · 3 Hidden access gap · 4 Framing · 5 Prior-work positioning ·
6 Contributions · [Benchmark] 7 Pipeline · 8 Protocol · [Results] 9 Main table ·
10 Main chart · 11 McNemar · 12 Robustness battery · 13 Tokenization · 14 Spelling ·
[Why] 15 Recoverability · 16 Error taxonomy · [Frontier] 17 Scaling · 18 Frontier+974 ·
[Mitigation] 19 Mitigation · 20 Conclusion · Thank-you.

Section dividers are auto-numbered between groups.

## Editing tips
- Change a data series colour once in `theme.tex` (`cBangla`, `cBanglish`, `cEnglish`).
- Bengali text: wrap in `\bn{...}`.
- Frames containing a `pgfplots` axis are marked `[fragile]` — keep that if you add charts.
