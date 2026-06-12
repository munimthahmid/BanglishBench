# Qwen2.5-3B BEnQA Human-Reviewed Gold 974

Updated: 2026-06-07

## Inputs

- Result rows: `results/runs/qwen25_3b_benqa_human_gold_974/qwen25_3b_benqa_human_gold_974.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_benqa_human_gold_974_summary.csv`
- Item matrix CSV: `results/analysis/qwen25_3b_benqa_human_gold_974_item_matrix.csv`
- Bootstrap iterations: 2000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 323 | 974 | 33.16% | 0 |
| banglish_clean | 285 | 974 | 29.26% | 0 |
| english | 490 | 974 | 50.31% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 974 | -3.90% | [-7.19%, -0.51%] | 115 | 153 | 170 | 536 |
| banglish_minus_english | 974 | -21.05% | [-24.64%, -17.35%] | 91 | 296 | 194 | 393 |
| english_minus_bangla | 974 | 17.15% | [13.76%, 20.64%] | 254 | 87 | 236 | 397 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
