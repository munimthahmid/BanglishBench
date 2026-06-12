# V5 BEnQA Option Lexical Coverage Audit

Updated: 2026-06-11

## Scope

This no-spend audit separates BEnQA reviewed-Banglish prompt text into
question stem, all answer options, and the gold answer option. It compares
each surface with BanglaTLit exact Latin-token coverage and then checks the
frozen-v5 three-Qwen correctness gap inside coverage quartiles.

- Frozen-v5 slice: `data/slices/validation_200_v5.jsonl`
- Fragility items: `results/analysis/v5_banglish_fragility_items.csv`
- BanglaTLit files: `literature/code/BanglaTLit/data/BanglaTLiT_val.csv`, `literature/code/BanglaTLit/data/BanglaTLiT_test.csv`
- Item-level output: `results/analysis/v5_benqa_option_lexical_coverage_items.csv`
- Summary table: `results/analysis/v5_benqa_option_lexical_coverage_summary.csv`
- BanglaTLit rows used: 4000
- BanglaTLit exact Latin vocabulary size: 7215

## Headline

- BEnQA reviewed-Banglish stem coverage is 31.3%; all-option coverage is lower at 18.5%, and gold-option coverage is 17.3%.
- Even in the highest all-option coverage quartile, reviewed Banglish is 40/108 correct slots versus Bangla 50/108 (-9.3 pts, CI [-21.3,+2.8]).
- The highest gold-option coverage quartile is also negative: reviewed Banglish 47/108 versus Bangla 56/108 (-8.3 pts).
- Option parsing is complete for 144/144 BEnQA rows.
- Treat this as descriptive evidence about answer-choice lexical exposure, not
  as a causal option-token mechanism.

## Surface-Level Coverage

| Surface | Bucket | Items | Mean coverage | Pooled coverage | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla | Fragility events |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `stem` | `all` | 144 | 31.3% | 32.1% | 185/432 | 135/432 | 234/432 | -11.6 pts, CI [-16.9,-6.2] | 164 |
| `options_all` | `all` | 144 | 18.5% | 21.1% | 185/432 | 135/432 | 234/432 | -11.6 pts, CI [-17.1,-6.2] | 164 |
| `gold_option` | `all` | 144 | 17.3% | 20.9% | 185/432 | 135/432 | 234/432 | -11.6 pts, CI [-16.9,-6.2] | 164 |

## Coverage Quartiles

Quartiles are sorted separately for each surface. Each BEnQA quartile has
36 items and 108 model-item slots.

### Question Stem

| Surface | Bucket | Items | Mean coverage | Pooled coverage | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla | Fragility events |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `stem` | `q1` | 36 | 10.8% | 12.6% | 45/108 | 27/108 | 53/108 | -16.7 pts, CI [-28.7,-5.6] | 48 |
| `stem` | `q2` | 36 | 26.0% | 26.7% | 43/108 | 29/108 | 47/108 | -13.0 pts, CI [-24.1,-1.8] | 37 |
| `stem` | `q3` | 36 | 35.8% | 35.3% | 50/108 | 43/108 | 72/108 | -6.5 pts, CI [-17.6,+3.7] | 39 |
| `stem` | `q4` | 36 | 52.5% | 50.3% | 47/108 | 36/108 | 62/108 | -10.2 pts, CI [-18.5,-1.8] | 40 |

### All Answer Options

| Surface | Bucket | Items | Mean coverage | Pooled coverage | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla | Fragility events |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `options_all` | `q1` | 36 | 0.0% | 0.0% | 49/108 | 32/108 | 54/108 | -15.7 pts, CI [-25.9,-6.5] | 43 |
| `options_all` | `q2` | 36 | 0.0% | 0.0% | 44/108 | 31/108 | 57/108 | -12.0 pts, CI [-21.3,-2.8] | 38 |
| `options_all` | `q3` | 36 | 12.5% | 15.2% | 42/108 | 32/108 | 69/108 | -9.3 pts, CI [-20.4,+1.8] | 47 |
| `options_all` | `q4` | 36 | 61.5% | 58.6% | 50/108 | 40/108 | 54/108 | -9.3 pts, CI [-21.3,+2.8] | 36 |

### Gold Answer Option

| Surface | Bucket | Items | Mean coverage | Pooled coverage | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla | Fragility events |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gold_option` | `q1` | 36 | 0.0% | 0.0% | 48/108 | 32/108 | 57/108 | -14.8 pts, CI [-25.0,-6.5] | 42 |
| `gold_option` | `q2` | 36 | 0.0% | 0.0% | 42/108 | 24/108 | 65/108 | -16.7 pts, CI [-25.0,-8.3] | 51 |
| `gold_option` | `q3` | 36 | 0.0% | 0.0% | 39/108 | 32/108 | 53/108 | -6.5 pts, CI [-17.6,+4.6] | 35 |
| `gold_option` | `q4` | 36 | 69.2% | 53.6% | 56/108 | 47/108 | 59/108 | -8.3 pts, CI [-22.2,+4.6] | 36 |

## Interpretation

- BEnQA answer options have substantially lower exact overlap with
  BanglaTLit than the stems, which is an important naturalness limitation:
  many answer choices are curriculum terms rather than chat-style Banglish.
- The highest option-coverage and gold-option-coverage quartile point
  estimates are still negative, although their intervals cross zero.
  This weakens a simple explanation that the main BEnQA gap is only
  caused by completely unattested answer-choice strings.
- The stem quartiles reproduce the existing lexical-coverage pattern; the
  highest stem quartile is 36/108
  reviewed-Banglish slots versus 47/108
  Bangla slots.
- Use this audit in the limitations and failure-analysis chapters: it
  acknowledges option lexical exposure while preserving the controlled
  paired-script result.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_option_lexical_coverage.py`
- Item rows: 144
- Summary rows: 15
- Token rule: Latin alphabetic tokens of length at least 2.
- Bootstrap: item-cluster resampling within each bucket, 5,000 samples.
