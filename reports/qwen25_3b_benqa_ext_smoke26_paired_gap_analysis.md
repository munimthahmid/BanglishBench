# Qwen2.5-3B BEnQA Extension Smoke26 Paired Gap Analysis

Updated: 2026-06-05

## Inputs

- Result rows: `results/runs/qwen25_3b_benqa_ext_smoke26/results/runs/qwen25_3b_benqa_ext_smoke26.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_benqa_ext_smoke26_paired_gaps.csv`
- Item matrix CSV: `results/analysis/qwen25_3b_benqa_ext_smoke26_item_matrix.csv`
- Bootstrap iterations: 10000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 8 | 26 | 30.77% | 0 |
| banglish_clean | 11 | 26 | 42.31% | 0 |
| english | 20 | 26 | 76.92% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 26 | 11.54% | [-11.54%, 34.62%] | 7 | 4 | 4 | 11 |
| banglish_minus_english | 26 | -34.62% | [-57.69%, -7.69%] | 3 | 12 | 8 | 3 |
| english_minus_bangla | 26 | 46.15% | [23.08%, 69.23%] | 14 | 2 | 6 | 4 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
