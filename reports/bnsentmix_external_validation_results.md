# BnSentMix External-Validation Results

Updated: 2026-06-11

## Scope

This ecological-validity layer measures zero-shot four-way sentiment
classification on naturally occurring Bengali-English code-mixed text.
It is separate from the paired cross-script knowledge benchmark.

- Slice: `data/slices/bnsentmix_balanced200_v1.jsonl`
- Item analysis: `results/analysis/bnsentmix_external_validation_items.csv`
- Summary analysis: `results/analysis/bnsentmix_external_validation_summary.csv`
- `Qwen2.5-3B` output: `results/runs/qwen25_3b_bnsentmix_full200/results/runs/qwen25_3b_bnsentmix_full200.jsonl`
- `Qwen2.5-7B 8-bit` output: `results/runs/qwen25_7b_8bit_bnsentmix_full200/results/runs/qwen25_7b_8bit_bnsentmix_full200.jsonl`
- `Qwen3-4B` output: `results/runs/qwen3_4b_bnsentmix_full200/results/runs/qwen3_4b_bnsentmix_full200.jsonl`

## Headline

| Model | Rows | Valid outputs | Accuracy | Macro-F1 | Balanced accuracy | Majority baseline |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 200 | 200/200 | 44.5% | 0.431 | 44.5% | 25.0% |
| Qwen2.5-7B 8-bit | 200 | 200/200 | 49.0% | 0.479 | 49.0% | 25.0% |
| Qwen3-4B | 200 | 200/200 | 49.5% | 0.486 | 49.5% | 25.0% |

## Per-Label Recall

| Model | Label | Support | Predicted | Recall | F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | positive | 50 | 59 | 60.0% | 0.550 |
| Qwen2.5-3B | negative | 50 | 66 | 56.0% | 0.483 |
| Qwen2.5-3B | neutral | 50 | 15 | 20.0% | 0.308 |
| Qwen2.5-3B | mixed | 50 | 60 | 42.0% | 0.382 |
| Qwen2.5-7B 8-bit | positive | 50 | 38 | 40.0% | 0.455 |
| Qwen2.5-7B 8-bit | negative | 50 | 42 | 44.0% | 0.478 |
| Qwen2.5-7B 8-bit | neutral | 50 | 92 | 78.0% | 0.549 |
| Qwen2.5-7B 8-bit | mixed | 50 | 28 | 34.0% | 0.436 |
| Qwen3-4B | positive | 50 | 106 | 86.0% | 0.551 |
| Qwen3-4B | negative | 50 | 32 | 36.0% | 0.439 |
| Qwen3-4B | neutral | 50 | 43 | 40.0% | 0.430 |
| Qwen3-4B | mixed | 50 | 19 | 36.0% | 0.522 |

## Scaling Note

- Qwen2.5 scaling improves this natural code-mixed sentiment slice from 89/200 to 98/200 (+4.5 points) and macro-F1 from 0.431 to 0.479 (+0.049).
- Qwen2.5-7B nearly matches Qwen3-4B on the headline score (98/200 vs 99/200), but their label priors differ.
- Qwen2.5-7B overpredicts neutral labels (92/200 predictions), while Qwen3-4B overpredicts positive labels (106/200 predictions).

## Interpretation Contract

- This layer broadens ecological validity with natural code-mixed text.
- It does not estimate the paired script penalty because there is no
  matched Bangla-script or English translation for each item.
- Compare model behavior within this task. Do not directly compare
  absolute accuracy against the core knowledge benchmark.
- Public-dataset contamination remains an open threat.
