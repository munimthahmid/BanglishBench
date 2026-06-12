# Qwen2.5-7B 8-bit Validation-200 v4

Updated: 2026-05-28

## Purpose

This report summarizes the Qwen2.5-7B-Instruct baseline on validation-200 v4.
The run was split into dev50 and test150, with test150 launched only after the
dev probe completed successfully.

## Setup

- Model: `Qwen/Qwen2.5-7B-Instruct`
- Quantization: bitsandbytes 8-bit.
- Package pins: `transformers==4.43.4`, `accelerate==0.33.0`,
  `bitsandbytes==0.43.3`.
- Prompt mode: baseline.
- Variants: Bangla, clean Banglish, English.
- Max new tokens: 128.
- Slice: `data/slices/validation_200_v4.jsonl` via dev50/test150.

## Operational Note

The first dev attempt failed before evaluation rows with a latest
Transformers/Torch compatibility issue. The pinned package stack above completed
both dev50 and test150 on Kaggle P100.

## Dev/Test Results

| Split | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| Dev50 | 13/50 | 13/50 | 20/50 |
| Test150 | 52/150 | 35/150 | 74/150 |
| Full200 | 65/200 | 48/200 | 94/200 |

By dataset, full200:

| Dataset | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 60/144 | 48/144 | 86/144 |
| BanglaMATH | 5/56 | 0/56 | 8/56 |

## Paired Bootstrap

| Comparison | Delta | 95% CI |
| --- | ---: | --- |
| Banglish - Bangla | -8.5 points | [-15.5, -1.5] |
| Banglish - English | -23.0 points | [-30.5, -15.5] |

## Interpretation

Qwen2.5-7B improves over Qwen2.5-3B in all three scripts, especially English,
but it does not remove the clean Banglish deficit. On full validation-200 v4,
Banglish remains below native Bangla with a negative paired confidence interval.

The dev split alone looked like Bangla and Banglish were tied, but test150
revealed the same directional gap as the earlier Qwen2.5-3B result. This is a
useful dev/test lesson: do not infer the script hierarchy from dev50 alone.

For the thesis, Qwen2.5-7B strengthens the scaling result:

- The Banglish-vs-English gap grows as English competence improves.
- The Banglish-below-Bangla gap persists at 7B.
- BanglaMATH remains too hard for detailed claims; BEnQA carries most of the
  evidence.

## Artifacts

- `results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/`
- `results/runs/qwen25_7b_8bit_validation200_v4_test150/`
- `results/runs/qwen25_7b_8bit_validation200_v4_full200_by_variant_reparsed_rescored.csv`
- `results/runs/qwen25_7b_8bit_validation200_v4_full200_by_dataset_variant_reparsed_rescored.csv`
- `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_by_split_variant_reparsed_rescored.csv`
- `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_by_split_dataset_variant_reparsed_rescored.csv`
- `results/analysis/qwen25_7b_8bit_validation200_v4_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen25_7b_8bit_validation200_v4_banglish_minus_english_bootstrap.csv`
