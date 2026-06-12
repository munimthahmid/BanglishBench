# Qwen2.5-3B BEnQA Extension Full851 Paired Gap Analysis

Updated: 2026-06-05

## Inputs

- Result rows: `results/runs/qwen25_3b_benqa_ext_full851/results/runs/qwen25_3b_benqa_ext_full851.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_benqa_ext_full851_paired_gaps.csv`
- Item matrix CSV: `results/analysis/qwen25_3b_benqa_ext_full851_item_matrix.csv`
- Bootstrap iterations: 10000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 291 | 851 | 34.20% | 0 |
| banglish_clean | 248 | 851 | 29.14% | 0 |
| english | 437 | 851 | 51.35% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 851 | -5.05% | [-8.46%, -1.65%] | 93 | 136 | 155 | 467 |
| banglish_minus_english | 851 | -22.21% | [-26.20%, -18.10%] | 82 | 271 | 166 | 332 |
| english_minus_bangla | 851 | 17.16% | [13.28%, 20.92%] | 224 | 78 | 213 | 336 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
