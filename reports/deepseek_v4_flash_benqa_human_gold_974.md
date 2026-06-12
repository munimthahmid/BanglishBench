# DeepSeek V4 Flash BEnQA Human-Reviewed Gold 974

Updated: 2026-06-07

## Inputs

- Result rows: `results/analysis/deepseek_v4_flash_benqa_human_gold_974_imported.jsonl`
- Summary CSV: `results/analysis/deepseek_v4_flash_benqa_human_gold_974_summary.csv`
- Item matrix CSV: `results/analysis/deepseek_v4_flash_benqa_human_gold_974_item_matrix.csv`
- Bootstrap iterations: 2000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 756 | 974 | 77.62% | 0 |
| banglish_clean | 438 | 974 | 44.97% | 0 |
| english | 791 | 974 | 81.21% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 974 | -32.65% | [-36.04%, -29.26%] | 43 | 361 | 395 | 175 |
| banglish_minus_english | 974 | -36.24% | [-39.73%, -32.96%] | 39 | 392 | 399 | 144 |
| english_minus_bangla | 974 | 3.59% | [1.13%, 6.06%] | 91 | 56 | 700 | 127 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
