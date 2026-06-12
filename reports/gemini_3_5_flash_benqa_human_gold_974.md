# Gemini 3.5 Flash BEnQA Human-Reviewed Gold 974

Updated: 2026-06-07

## Inputs

- Result rows: `results/analysis/gemini_3_5_flash_benqa_human_gold_974_imported.jsonl`
- Summary CSV: `results/analysis/gemini_3_5_flash_benqa_human_gold_974_summary.csv`
- Item matrix CSV: `results/analysis/gemini_3_5_flash_benqa_human_gold_974_item_matrix.csv`
- Bootstrap iterations: 2000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 743 | 974 | 76.28% | 176 |
| banglish_clean | 633 | 974 | 64.99% | 263 |
| english | 680 | 974 | 69.82% | 211 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 974 | -11.29% | [-13.66%, -8.93%] | 21 | 131 | 612 | 210 |
| banglish_minus_english | 974 | -4.83% | [-7.39%, -2.05%] | 68 | 115 | 565 | 226 |
| english_minus_bangla | 974 | -6.47% | [-8.93%, -4.11%] | 43 | 106 | 637 | 188 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
