# V5 BanglaTLit Lexical Coverage Audit

Updated: 2026-06-11

This no-spend audit compares frozen-v5 controlled Banglish prompts with
BanglaTLit's naturally written Romanized Bangla. It is a conservative
exact-token overlap check, not a semantic naturalness score.

## Inputs And Outputs

- Frozen-v5 slice: `data/slices/validation_200_v5.jsonl`
- BanglaTLit files: `literature/code/BanglaTLit/data/BanglaTLiT_val.csv`, `literature/code/BanglaTLit/data/BanglaTLiT_test.csv`
- Item-level output: `results/analysis/v5_banglatlit_lexical_coverage_items.csv`
- Summary table: `results/analysis/v5_banglatlit_lexical_coverage_summary.csv`
- BanglaTLit rows used: 4000
- BanglaTLit exact Latin vocabulary size: 7215 token types

## Headline

- Frozen-v5 content Banglish has low exact overlap with BanglaTLit: mean
  token coverage is 36.8% overall,
  31.3% for BEnQA, and
  50.8% for BanglaMATH.
- This reinforces the current limitation: the benchmark is controlled
  educational Banglish, not a sample of naturally occurring chat Banglish.
- The script gap is not confined to the least-attested lexical items.
  In the highest-coverage all-200 quartile, reviewed Banglish has
  28/150 correct slots
  versus Bangla 40/150
  (-8.0 pts, CI [-15.3,-1.3]).
- The lowest-coverage all-200 quartile has reviewed Banglish
  31/150 versus Bangla
  52/150 (-14.0 pts, CI [-22.7,-5.3]).
- In the highest-coverage BEnQA quartile, reviewed Banglish has
  36/108 correct slots
  versus Bangla 47/108
  (-10.2 pts, CI [-18.5,-1.8]).

## Coverage By Dataset

| Dataset | Items | Mean exact token coverage | Pooled token coverage | Bangla slots | Reviewed Banglish slots | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | 200 | 36.8% | 38.5% | 199/600 (33.2%) | 137/600 (22.8%) | -10.3 pts, CI [-14.5,-6.2] |
| benqa | 144 | 31.3% | 32.1% | 185/432 (42.8%) | 135/432 (31.2%) | -11.6 pts, CI [-17.1,-6.5] |
| banglamath | 56 | 50.8% | 49.0% | 14/168 (8.3%) | 2/168 (1.2%) | -7.1 pts, CI [-13.1,-2.4] |

## Coverage Quartiles

Quartiles are sorted by exact token coverage against BanglaTLit. The
all-200 quartiles have 50 items each; BEnQA quartiles have 36 items
each. The confidence intervals resample validation items within the
bucket.

### All 200 Items

| Bucket | Items | Mean coverage | Bangla slots | Reviewed Banglish slots | English slots | Fragility events | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `q1` | 50 | 13.7% | 52/150 (34.7%) | 31/150 (20.7%) | 64/150 (42.7%) | 56 | -14.0 pts, CI [-22.7,-5.3] |
| `q2` | 50 | 29.5% | 60/150 (40.0%) | 44/150 (29.3%) | 65/150 (43.3%) | 45 | -10.7 pts, CI [-20.7,-2.0] |
| `q3` | 50 | 40.8% | 47/150 (31.3%) | 34/150 (22.7%) | 66/150 (44.0%) | 45 | -8.7 pts, CI [-16.7,-1.3] |
| `q4` | 50 | 63.0% | 40/150 (26.7%) | 28/150 (18.7%) | 58/150 (38.7%) | 39 | -8.0 pts, CI [-15.3,-1.3] |

### BEnQA

| Bucket | Items | Mean coverage | Bangla slots | Reviewed Banglish slots | English slots | Fragility events | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `q1` | 36 | 10.8% | 45/108 (41.7%) | 27/108 (25.0%) | 53/108 (49.1%) | 48 | -16.7 pts, CI [-28.7,-4.6] |
| `q2` | 36 | 26.0% | 43/108 (39.8%) | 29/108 (26.9%) | 47/108 (43.5%) | 37 | -13.0 pts, CI [-25.0,-1.8] |
| `q3` | 36 | 35.8% | 50/108 (46.3%) | 43/108 (39.8%) | 72/108 (66.7%) | 39 | -6.5 pts, CI [-17.6,+3.7] |
| `q4` | 36 | 52.5% | 47/108 (43.5%) | 36/108 (33.3%) | 62/108 (57.4%) | 40 | -10.2 pts, CI [-18.5,-1.8] |

### BanglaMATH

| Bucket | Items | Mean coverage | Bangla slots | Reviewed Banglish slots | English slots | Fragility events | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `q1` | 14 | 27.1% | 2/42 (4.8%) | 0/42 (0.0%) | 3/42 (7.1%) | 3 | -4.8 pts, CI [-14.3,0.0] |
| `q2` | 14 | 42.3% | 1/42 (2.4%) | 0/42 (0.0%) | 0/42 (0.0%) | 1 | -2.4 pts, CI [-7.1,0.0] |
| `q3` | 14 | 58.6% | 6/42 (14.3%) | 0/42 (0.0%) | 4/42 (9.5%) | 7 | -14.3 pts, CI [-30.9,-2.4] |
| `q4` | 14 | 75.3% | 5/42 (11.9%) | 2/42 (4.8%) | 12/42 (28.6%) | 10 | -7.1 pts, CI [-21.4,0.0] |

## Interpretation

- The low exact overlap is useful limitations evidence. Controlled
  curriculum Banglish contains technical vocabulary, formulas, and
  romanization choices that are not frequent in BanglaTLit.
- The high-coverage quartiles remaining negative weakens a simple
  explanation that the Banglish deficit is only out-of-vocabulary
  conversational-naturalness mismatch.
- Exact token matching is deliberately conservative. It misses related
  spellings and morphology, and BanglaTLit is conversational rather than
  educational. Use this audit as a bridge between benchmark naturalness
  and failure analysis, not as a causal lexical mechanism.

## Reproducibility

- Builder: `scripts/analyze_v5_banglatlit_lexical_coverage.py`
- Input items: 200
- Summary rows: 15
- Token rule: Latin alphabetic tokens of length at least 2 after removing
  answer instructions and MCQ option lines.
- Bootstrap: item-cluster resampling within each bucket, 5,000 samples.
