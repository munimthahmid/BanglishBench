# GPT-5.5 None BEnQA Human-Reviewed Gold 974

Updated: 2026-06-07

## Inputs

- Result rows: `results/analysis/openai_gpt55_none_benqa_human_gold_974_imported.jsonl`
- Summary CSV: `results/analysis/openai_gpt55_none_benqa_human_gold_974_summary.csv`
- Item matrix CSV: `results/analysis/openai_gpt55_none_benqa_human_gold_974_item_matrix.csv`
- Bootstrap iterations: 2000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 820 | 974 | 84.19% | 0 |
| banglish_clean | 699 | 974 | 71.77% | 0 |
| english | 825 | 974 | 84.70% | 0 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 974 | -12.42% | [-15.09%, -9.75%] | 38 | 159 | 661 | 116 |
| banglish_minus_english | 974 | -12.94% | [-15.91%, -9.86%] | 53 | 179 | 646 | 96 |
| english_minus_bangla | 974 | 0.51% | [-1.64%, 2.67%] | 60 | 55 | 765 | 94 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
