# DeepSeek V4 Flash BEnQA Extension Full851 Paired Gap Analysis

Updated: 2026-06-05

## Inputs

- Result rows: `results/analysis/deepseek_v4_flash_benqa_ext_full851_imported.jsonl`
- Summary CSV: `results/analysis/deepseek_v4_flash_benqa_ext_full851_paired_gaps.csv`
- Item matrix CSV: `results/analysis/deepseek_v4_flash_benqa_ext_full851_item_matrix.csv`
- Bootstrap iterations: 10000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 665 | 851 | 78.14% | 0 |
| banglish_clean | 376 | 851 | 44.18% | 0 |
| english | 697 | 851 | 81.90% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 851 | -33.96% | [-37.84%, -30.08%] | 40 | 329 | 336 | 146 |
| banglish_minus_english | 851 | -37.72% | [-41.36%, -33.96%] | 31 | 352 | 345 | 123 |
| english_minus_bangla | 851 | 3.76% | [1.29%, 6.35%] | 75 | 43 | 622 | 111 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
