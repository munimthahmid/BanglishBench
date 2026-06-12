# Main Results: Validation 200 v3

Updated: 2026-05-28

## Slice

- File: `data/slices/validation_200_v3.jsonl`
- Size: 200 English-matched items.
- Composition: 144 BEnQA MCQ items, 56 BanglaMATH short-answer items.
- Variants evaluated: native Bangla, clean Banglish, English.
- Prompt mode: baseline.
- Max new tokens: 128.

## Overall Accuracy

| Model | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B-Instruct | 54/200 | 38/200 | 71/200 |
| Qwen3-4B-Instruct-2507 | 80/200 | 46/200 | 88/200 |

## Dataset Split

| Model | Dataset | Bangla | Clean Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B-Instruct | BEnQA | 49/144 | 38/144 | 66/144 |
| Qwen2.5-3B-Instruct | BanglaMATH | 5/56 | 0/56 | 5/56 |
| Qwen3-4B-Instruct-2507 | BEnQA | 76/144 | 45/144 | 82/144 |
| Qwen3-4B-Instruct-2507 | BanglaMATH | 4/56 | 1/56 | 6/56 |

## Paired Bootstrap Deltas

Right minus left, matched by item id.

| Model | Comparison | Delta | 95% CI |
| --- | --- | ---: | --- |
| Qwen2.5-3B-Instruct | Banglish - Bangla | -8.0 points | [-14.0, -2.0] |
| Qwen2.5-3B-Instruct | Banglish - English | -16.5 points | [-24.0, -9.0] |
| Qwen3-4B-Instruct-2507 | Banglish - Bangla | -17.0 points | [-23.5, -10.5] |
| Qwen3-4B-Instruct-2507 | Banglish - English | -21.0 points | [-28.5, -13.5] |

## Item-Level Patterns

Qwen2.5-3B:

- BEnQA all correct: 17 items.
- BEnQA all wrong: 52 items.
- BEnQA Banglish-drop cases where Bangla and English are correct: 13 items.
- BEnQA English-only correct: 30 items.
- BanglaMATH is mostly unsolved across scripts: 49/56 all wrong.

Qwen3-4B:

- BEnQA all correct: 29 items.
- BEnQA all wrong: 42 items.
- BEnQA Banglish-drop cases where Bangla and English are correct: 32 items.
- BEnQA English-only correct: 18 items.
- BanglaMATH is mostly unsolved across scripts: 50/56 all wrong.

## Interpretation

Validation-200 converts the main script-gap claim from a promising pilot result
into stronger evidence. Both tested open models are worse on clean Banglish than
on native Bangla, and the paired confidence intervals are clearly negative.

The BEnQA split carries most of the signal because BanglaMATH accuracy is low
for all scripts. This means the thesis should use BanglaMATH as hard-task
stress evidence, while using BEnQA for the clearest matched-item script-gap
analysis.

The result does not yet prove that noisy user Banglish is worse than clean
Banglish on the larger slice. That is the purpose of the active validation-200
noisy Banglish runs.

## Primary Artifacts

- `results/runs/validation200_v3_128_model_comparison_by_variant_reparsed_rescored.csv`
- `results/runs/validation200_v3_128_model_comparison_by_dataset_variant_reparsed_rescored.csv`
- `results/analysis/qwen25_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen3_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen25_validation200_v3_script_gap_summary_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_script_gap_summary_reparsed.csv`
- `reports/qwen2_5_3b_validation200_v3_banglish_drop_examples_reparsed.md`
- `reports/qwen3_4b_validation200_v3_banglish_drop_examples_reparsed.md`
