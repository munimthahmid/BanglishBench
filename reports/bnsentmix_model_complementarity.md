# BnSentMix Model Complementarity

Updated: 2026-06-11

## Scope

This no-spend analysis asks whether the three BnSentMix model rows fail
on the same natural code-mixed sentiment items, or whether their errors
are complementary. It uses the existing 200-row balanced BnSentMix slice
and the already completed Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B
Kaggle outputs.

- Source item rows: `results/analysis/bnsentmix_external_validation_items.csv`
- Complementarity items: `results/analysis/bnsentmix_model_complementarity_items.csv`
- Complementarity summary: `results/analysis/bnsentmix_model_complementarity_summary.csv`

## Headline

| Result | Count | Interpretation |
| --- | ---: | --- |
| Best single model | 99/200 | Qwen3-4B is the strongest single row. |
| Any-model oracle | 154/200 | Diagnostic upper bound: at least one of the three models is correct. |
| Oracle minus best single | +27.5 pts | CI [+21.5, +34.0]. |

The natural code-mixed layer is therefore not just a single-model ranking:
many items are recoverable by another model even when the strongest single
row fails. This is diagnostic complementarity, not deployable accuracy.

## Single Models

| Model | Correct | Accuracy | Positive pred | Negative pred | Neutral pred | Mixed pred |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 89/200 | 44.5% | 59 | 66 | 15 | 60 |
| Qwen2.5-7B 8-bit | 98/200 | 49.0% | 38 | 42 | 92 | 28 |
| Qwen3-4B | 99/200 | 49.5% | 106 | 32 | 43 | 19 |

## Correct-Model Count

| Correct models on an item | Items |
| ---: | ---: |
| 0 | 46/200 |
| 1 | 66/200 |
| 2 | 44/200 |
| 3 | 44/200 |

## Pairwise Complementarity

| Pair | Left | Right | Delta right-left | Left only | Right only | Both correct | Neither | Pair oracle | Agreement correct | Sign p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B vs Qwen2.5-7B 8-bit | 89/200 | 98/200 | +4.5 pts [-4.0, +13.0] | 34 | 43 | 55 | 68 | 132/200 | 55/89 | 0.3620 |
| Qwen2.5-3B vs Qwen3-4B | 89/200 | 99/200 | +5.0 pts [-3.0, +13.5] | 32 | 42 | 57 | 69 | 131/200 | 57/88 | 0.2954 |
| Qwen2.5-7B 8-bit vs Qwen3-4B | 98/200 | 99/200 | +0.5 pts [-7.5, +9.0] | 34 | 35 | 64 | 67 | 133/200 | 64/103 | 1.0000 |

## Majority Vote

| Strategy | Correct | Detail |
| --- | ---: | --- |
| Majority only | 88/158 covered rows | Covers 79.0%; 55.7% accuracy on covered rows. |
| majority_with_Qwen2.5-3B_fallback | 94/200 | Fallback rows 42; delta vs fallback model +2.5 pts [-3.5, +8.0]. |
| majority_with_Qwen2.5-7B 8-bit_fallback | 106/200 | Fallback rows 42; delta vs fallback model +4.0 pts [0.0, +8.0]. |
| majority_with_Qwen3-4B_fallback | 102/200 | Fallback rows 42; delta vs fallback model +1.5 pts [-3.0, +5.5]. |

## Label-Level Oracle Coverage

| Gold label | Any model correct | At least two correct | All wrong | All correct |
| --- | ---: | ---: | ---: | ---: |
| positive | 45/50 | 29/50 | 5/50 | 19/50 |
| negative | 35/50 | 23/50 | 15/50 | 10/50 |
| neutral | 41/50 | 20/50 | 9/50 | 8/50 |
| mixed | 33/50 | 16/50 | 17/50 | 7/50 |

## Interpretation Contract

- The any-model oracle is diagnostic. It uses gold labels to choose the
  successful model after the fact and is not a deployable method.
- Pairwise and majority-vote rows are behavioral evidence about error
  overlap on the same natural items.
- BnSentMix remains unpaired by script, so this report does not estimate
  a Bangla-vs-Banglish script penalty.
