# Validation-200 v4 Auto-Suggested Banglish Candidate

Updated: 2026-05-28

## Purpose

This file documents a heuristic, unreviewed candidate slice created by applying the conservative Banglish replacement map already used for the human-review suggestion packet. It is intended for data QA and reviewer triage, not as a thesis-grade frozen v5 benchmark.

## Artifacts

- Input: `data/slices/validation_200_v4.jsonl`
- Output: `data/slices/validation_200_v4_auto_suggested.jsonl`
- Audit CSV: `results/analysis/validation200_v4_auto_suggested_audit.csv`
- Manifest: `data/slices/validation_200_v4_auto_suggested.manifest.json`
- Fields edited: `banglish_clean, banglish_noisy`
- Output quality status: `auto_suggested_unreviewed_v4_1`

## Counts

- Items: 200
- Items with any text change: 140
- Items without text change: 60
- Changed `banglish_clean` rows: 140
- Changed `banglish_noisy` rows: 138

## Replacement Counts

| Field / replacement | Rows affected |
| --- | ---: |
| `banglish_clean:achhe->ache` | 6 |
| `banglish_clean:ayotakar->ayotokar` | 7 |
| `banglish_clean:choora->chowra` | 4 |
| `banglish_clean:doirghy->doirgho` | 11 |
| `banglish_clean:ekoti->ekti` | 37 |
| `banglish_clean:konoti->konti` | 56 |
| `banglish_clean:korote->korte` | 7 |
| `banglish_clean:kot->koto` | 72 |
| `banglish_clean:kshetre->khetre` | 5 |
| `banglish_clean:kshetrofol->khetrofol` | 13 |
| `banglish_clean:penyaj->peyaj` | 1 |
| `banglish_clean:prosth->prostho` | 9 |
| `banglish_clean:thakole->thakle` | 5 |
| `banglish_clean:uchchota->ucchota` | 2 |
| `banglish_noisy:ayotakar->ayotokar` | 7 |
| `banglish_noisy:choora->chowra` | 4 |
| `banglish_noisy:ekoti->ekti` | 37 |
| `banglish_noisy:konoti->konti` | 56 |
| `banglish_noisy:korote->korte` | 7 |
| `banglish_noisy:kot->koto` | 72 |
| `banglish_noisy:penyaj->peyaj` | 1 |
| `banglish_noisy:prosth->prostho` | 9 |
| `banglish_noisy:thakole->thakle` | 5 |
| `banglish_noisy:uchchota->ucchota` | 2 |

## Caveats

- These edits are automatic spelling-normalization suggestions.
- They are not human-reviewed labels or final Banglish gold text.
- The candidate may be useful for a sensitivity rerun, but any v5 benchmark claim still needs the human-review workflow.
- The replacement map is intentionally narrow; it does not solve broader naturalness, dialect, or spelling-variation coverage.

## Changed Examples

### 1. benqa_12th-Biology-I_0265 / `banglish_clean`

- Dataset: `benqa`
- Suggestions: achhe->ache (1); ekoti->ekti (1); konoti->konti (1)

Before:

```text
mi. 'k' byoboharik klase ekoti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom achhe. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khaddo prostut kore nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

After:

```text
mi. 'k' byoboharik klase ekti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom ache. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khaddo prostut kore nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

### 2. benqa_12th-Biology-I_0265 / `banglish_noisy`

- Dataset: `benqa`
- Suggestions: ekoti->ekti (1); konoti->konti (1)

Before:

```text
mi. 'k' byoboharik klase ekoti nomunar poryobekson kore dekolo metajailem kendrer dike, vaskular bandol 9ti ebong kichu ekokosi rom ache. poryobeksit boysistyogulo kivabe udvidoke banchiye rakote sahajy kore? i. pani o konij lobon poribohon kore ii. prostutokrit kabar poribohon kore iii. kaddo prostut kore nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

After:

```text
mi. 'k' byoboharik klase ekti nomunar poryobekson kore dekolo metajailem kendrer dike, vaskular bandol 9ti ebong kichu ekokosi rom ache. poryobeksit boysistyogulo kivabe udvidoke banchiye rakote sahajy kore? i. pani o konij lobon poribohon kore ii. prostutokrit kabar poribohon kore iii. kaddo prostut kore nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

### 3. banglamath_0234 / `banglish_clean`

- Dataset: `banglamath`
- Suggestions: ekoti->ekti (1); kot->koto (1)

Before:

```text
ekoti kaj k 10 dine o kh 15 dine korole tara ekotre kot dine korobe
Return only the final answer.
```

After:

```text
ekti kaj k 10 dine o kh 15 dine korole tara ekotre koto dine korobe
Return only the final answer.
```

### 4. banglamath_0234 / `banglish_noisy`

- Dataset: `banglamath`
- Suggestions: ekoti->ekti (1); kot->koto (1)

Before:

```text
ekoti kaj k 10 dine o k 15 dine korole tara ekotre kot dine korobe
Return only the final answer.
```

After:

```text
ekti kaj k 10 dine o k 15 dine korole tara ekotre koto dine korobe
Return only the final answer.
```

### 5. banglamath_0522 / `banglish_clean`

- Dataset: `banglamath`
- Suggestions: choora->chowra (1); kot->koto (1); kshetrofol->khetrofol (1); thakole->thakle (1)

Before:

```text
jomir bhitore 2 mitar choora rasta thakole rastabade jomir kshetrofol kot
Return only the final answer.
```

After:

```text
jomir bhitore 2 mitar chowra rasta thakle rastabade jomir khetrofol koto
Return only the final answer.
```

### 6. banglamath_0522 / `banglish_noisy`

- Dataset: `banglamath`
- Suggestions: choora->chowra (1); kot->koto (1); thakole->thakle (1)

Before:

```text
jomir vitore 2 mitar choora rasta thakole rastabade jomir ksetrofol kot
Return only the final answer.
```

After:

```text
jomir vitore 2 mitar chowra rasta thakle rastabade jomir ksetrofol koto
Return only the final answer.
```

### 7. benqa_10th-Math_0271 / `banglish_clean`

- Dataset: `benqa`
- Suggestions: kot->koto (1)

Before:

```text
sthulokoni tribhujer sthulokon chhara baki kon duti kot hole tribhuj ongkon sombhob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

After:

```text
sthulokoni tribhujer sthulokon chhara baki kon duti koto hole tribhuj ongkon sombhob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

### 8. benqa_10th-Math_0271 / `banglish_noisy`

- Dataset: `benqa`
- Suggestions: kot->koto (1)

Before:

```text
sthulokoni trivujer sthulokon chara baki kon duti kot hole trivuj ongkon somvob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

After:

```text
sthulokoni trivujer sthulokon chara baki kon duti koto hole trivuj ongkon somvob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

### 9. benqa_10th-Physics_0045 / `banglish_clean`

- Dataset: `benqa`
- Suggestions: kot->koto (1)

Before:

```text
kon nirdisht bhorer kono bostur beg dwigun korole gotishokti kot gun hobe?
A. charogun
B. dwigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

After:

```text
kon nirdisht bhorer kono bostur beg dwigun korole gotishokti koto gun hobe?
A. charogun
B. dwigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

### 10. benqa_10th-Physics_0045 / `banglish_noisy`

- Dataset: `benqa`
- Suggestions: kot->koto (1)

Before:

```text
kon nirdist vorer kono bostur beg dwigun korole gotisokti kot gun hobe?
A. charogun
B. dwigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

After:

```text
kon nirdist vorer kono bostur beg dwigun korole gotisokti koto gun hobe?
A. charogun
B. dwigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

### 11. benqa_10th-Math-II_0139 / `banglish_clean`

- Dataset: `benqa`
- Suggestions: kot->koto (1)

Before:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... onukromotir 10 tom pod kot?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

After:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... onukromotir 10 tom pod koto?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

### 12. benqa_10th-Math-II_0139 / `banglish_noisy`

- Dataset: `benqa`
- Suggestions: kot->koto (1)

Before:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... onukromotir 10 tom pod kot?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

After:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... onukromotir 10 tom pod koto?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

