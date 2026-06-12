# Mistral-7B 8-bit Validation-200 v4 Pilot20

Updated: 2026-05-28

## Purpose

This pilot tests whether `mistralai/Mistral-7B-Instruct-v0.3` is a useful
non-Qwen 7B-class model-family breadth point for Script Matters on Kaggle P100.

## Setup

- Model: `mistralai/Mistral-7B-Instruct-v0.3`
- Quantization: bitsandbytes 8-bit
- Package pins: `transformers==4.43.4`, `accelerate==0.33.0`,
  `bitsandbytes==0.43.3`
- Slice: first 20 items from `data/slices/validation_200_v4_dev50.jsonl`
- Variants: Bangla, clean Banglish, English
- Prompt mode: baseline
- Max new tokens: 128
- Kaggle kernel: `munimthahmid3/mistral7b-8bit-v4-dev50-p20`

## Result

| Variant | Correct | Parsed empty | Mean seconds |
| --- | ---: | ---: | ---: |
| Bangla | 3/20 | 1 | 32.7293 |
| Clean Banglish | 4/20 | 0 | 23.3058 |
| English | 4/20 | 0 | 35.5865 |

By dataset:

| Dataset | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 3/15 | 4/15 | 4/15 |
| BanglaMATH | 0/5 | 0/5 | 0/5 |

The run completed, but it is slow: 60 generations took about 1,832 model-output
seconds, and the Kaggle log finished around 2,148 seconds after start.

## Interpretation

Mistral-7B is feasible on P100 with the pinned Qwen2.5-7B-compatible 8-bit
stack, but this pilot does not justify immediate full dev/test spend:

- Accuracy is low across all scripts.
- Banglish is not below Bangla on the 20-item pilot, but the sample is too small
  for a thesis-facing ordering claim.
- Runtime is high enough that full validation-200 would be expensive relative
  to likely evidence value.

Decision: keep this as a diagnostic breadth result. Do not launch full dev50 or
test150 until higher-priority runs are exhausted or a specific model-family
comparison question requires Mistral.

## Artifacts

- Output directory:
  `results/runs/mistral7b_8bit_validation200_v4_dev50_pilot20/`
- JSONL outputs:
  `results/runs/mistral7b_8bit_validation200_v4_dev50_pilot20/results/runs/mistral7b_8bit_validation200_v4_dev50_pilot20.jsonl`
- Variant summary:
  `results/runs/mistral7b_8bit_validation200_v4_dev50_pilot20/summary_by_variant_reparsed_rescored.csv`
- Dataset summary:
  `results/runs/mistral7b_8bit_validation200_v4_dev50_pilot20/summary_by_dataset_variant_reparsed_rescored.csv`
