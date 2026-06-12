# Qwen2.5-3B BEnQA Extension Pilot130 Paired Gap Analysis

Updated: 2026-06-05

## Inputs

- Result rows: `results/runs/qwen25_3b_benqa_ext_pilot130/results/runs/qwen25_3b_benqa_ext_pilot130.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_benqa_ext_pilot130_paired_gaps.csv`
- Item matrix CSV: `results/analysis/qwen25_3b_benqa_ext_pilot130_item_matrix.csv`
- Bootstrap iterations: 10000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 53 | 130 | 40.77% | 0 |
| banglish_clean | 42 | 130 | 32.31% | 0 |
| english | 71 | 130 | 54.62% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 130 | -8.46% | [-16.92%, 0.00%] | 12 | 23 | 30 | 65 |
| banglish_minus_english | 130 | -22.31% | [-33.08%, -11.54%] | 14 | 43 | 28 | 45 |
| english_minus_bangla | 130 | 13.85% | [3.85%, 23.85%] | 32 | 14 | 39 | 45 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
