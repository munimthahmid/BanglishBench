# Validation 100 v3 Romanizer Audit

Updated: 2026-05-27

Input:

- `data/slices/validation_100_v3_banglish_review.csv`

Purpose:

- Identify remaining systematic artifacts after the v2 nukta cleanup and v3
  conjunct-য/y cleanup.
- Do not mutate v3 while v3 experiments are running; use this audit for a later
  v4 or human-review pass.

## Heuristic Counts

| Pattern | Count | Interpretation |
| --- | ---: | --- |
| `tb` | 5 | Likely virama-ব artifact, especially words such as `দূরত্ব` and `রোধকত্ব`. |
| `boij`/old j-like artifact | 1 | `বৈজ্ঞানিক` currently appears as `boijnanik`; likely should be closer to `boigganik` or `boigyanik`. |
| `oja` | 3 | Mostly from `অ্যা`/technical loanword handling, e.g. `ojasitalodihaid`, `ojamailej`, `enojaim`. |
| `khady` | 3 | Acceptable as a Sanskritized transliteration but not natural Banglish; could become `khabar` only with lexical rewriting, not pure transliteration. |
| `ksh` | 25 | Usually valid for ক্ষ/ক্ষেত্র-type words, but may be heavy for everyday Banglish. |

## Examples

### Virama-ব / `tb`

- `tamar rodhokotb konoti?`
- `otikrant durotber-`
- `dui bondhur ... durotb ... dbitiy bondhur durotb kot`

Possible later fix:

- Add special handling for common `ত্ব` endings, mapping toward `tto` or
  `tto/ttwo` depending on the chosen romanization style.

### Scientific Loanword `অ্যা`

- `ojasitalodihaid`
- `ojamailej`
- `enojaim`

Possible later fix:

- Add special handling for অ্যা/্যা-like loanword clusters, likely mapping
  closer to `a`, `ae`, or `ya` depending on context.

### `বৈজ্ঞানিক`

- Current: `boijnanik`
- More natural candidates: `boigganik`, `boigyanik`

Possible later fix:

- Add a lexical override table for frequent academic terms rather than trying to
  solve every case with character-level rules.

## Decision

Keep v3 as the active controlled-clean dataset because it already removes the
large nukta and conjunct-য artifacts. Use this audit to plan either:

1. `validation_100_v4` with targeted romanizer overrides, or
2. a human-reviewed Banglish subset where annotators directly normalize the
   remaining awkward romanizations.

