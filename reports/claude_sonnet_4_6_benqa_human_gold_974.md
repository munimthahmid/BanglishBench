# Claude Sonnet 4.6 BEnQA Human-Reviewed Gold 974

Updated: 2026-06-07

## Inputs

- Result rows: `results/analysis/claude_sonnet_4_6_benqa_human_gold_974_imported.jsonl`
- Summary CSV: `results/analysis/claude_sonnet_4_6_benqa_human_gold_974_summary.csv`
- Item matrix CSV: `results/analysis/claude_sonnet_4_6_benqa_human_gold_974_item_matrix.csv`
- Bootstrap iterations: 2000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 764 | 974 | 78.44% | 108 |
| banglish_clean | 524 | 974 | 53.80% | 118 |
| english | 771 | 974 | 79.16% | 74 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 974 | -24.64% | [-27.82%, -21.25%] | 41 | 281 | 483 | 169 |
| banglish_minus_english | 974 | -25.36% | [-28.64%, -21.87%] | 49 | 296 | 475 | 154 |
| english_minus_bangla | 974 | 0.72% | [-1.64%, 3.08%] | 73 | 66 | 698 | 137 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
