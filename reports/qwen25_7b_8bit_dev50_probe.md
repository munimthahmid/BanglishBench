# Qwen2.5-7B 8-bit Dev50 Probe

Updated: 2026-05-28

## Purpose

This run tests whether a stronger Qwen2.5 checkpoint can be evaluated on Kaggle
P100 using bitsandbytes 8-bit loading, and whether the dev50 signal justifies a
held-out test150 run.

## Setup

- Model: `Qwen/Qwen2.5-7B-Instruct`
- Slice: `data/slices/validation_200_v4_dev50.jsonl`
- Variants: Bangla, clean Banglish, English.
- Prompt mode: baseline.
- Max new tokens: 128.
- Quantization: bitsandbytes 8-bit.
- Package pins used for successful version:
  `transformers==4.43.4`, `accelerate==0.33.0`, `bitsandbytes==0.43.3`.

## Operational Note

The first attempt failed before evaluation rows because latest Transformers on
the Torch 2.4.1 P100 stack called `Qwen2ForCausalLM.set_submodule`, which was
not available. The successful rerun pinned Transformers/Accelerate/bitsandbytes
to the stack above.

## Dev50 Result

| Variant | Correct |
| --- | ---: |
| Bangla | 13/50 |
| Clean Banglish | 13/50 |
| English | 20/50 |

By dataset:

| Dataset | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 13/36 | 13/36 | 19/36 |
| BanglaMATH | 0/14 | 0/14 | 1/14 |

## Comparison To Existing Dev50

| Model | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 11/50 | 7/50 | 18/50 |
| Qwen2.5-7B 8-bit | 13/50 | 13/50 | 20/50 |
| Qwen3-4B | 19/50 | 14/50 | 21/50 |

Interpretation:

- The run is operationally valid and non-degenerate.
- Compared with Qwen2.5-3B on the same dev50 split, Qwen2.5-7B improves
  Banglish substantially and ties Bangla on dev.
- English remains stronger than Banglish.
- This is useful enough to run test150 unchanged before making a scaling claim.

## Artifacts

- `results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50.jsonl`
- `results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/summary_by_variant_reparsed_rescored.csv`
- `results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/summary_by_dataset_variant_reparsed_rescored.csv`
- `results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/qwen25-7b-8bit-validation200-v4-dev50.log`

## Decision

Run Qwen2.5-7B 8-bit on validation-200 v4 test150 unchanged.
