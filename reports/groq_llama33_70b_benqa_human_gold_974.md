# Groq Llama 3.3 70B BEnQA Human-Reviewed Gold 974

Updated: 2026-06-07

## Inputs

- Result rows: `results/analysis/groq_llama33_70b_benqa_human_gold_974_imported.jsonl`
- Summary CSV: `results/analysis/groq_llama33_70b_benqa_human_gold_974_summary.csv`
- Item matrix CSV: `results/analysis/groq_llama33_70b_benqa_human_gold_974_item_matrix.csv`
- Bootstrap iterations: 2000

## Variant Accuracy

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| bangla | 547 | 974 | 56.16% | 2 |
| banglish_clean | 333 | 974 | 34.19% | 0 |
| english | 622 | 974 | 63.86% | 7 |

## Paired Gaps

Positive gaps mean the first named variant is more accurate than the second
on the same paired items.

| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| banglish_minus_bangla | 974 | -21.97% | [-25.67%, -18.17%] | 88 | 302 | 245 | 339 |
| banglish_minus_english | 974 | -29.67% | [-33.26%, -26.08%] | 66 | 355 | 267 | 286 |
| english_minus_bangla | 974 | 7.70% | [4.72%, 10.78%] | 151 | 76 | 471 | 276 |

## Interpretation Boundary

Use this report as paired descriptive evidence for the extension run. For a
26-row smoke, use only the operational/parser result and treat paired gaps
as exploratory. For the 130-row pilot or 851-row full pass-only extension,
the paired gaps become the scale-check evidence for the BEnQA component.
