# Qwen2.5-7B 8-bit Self-Normalization Dev50 Probe

Updated: 2026-05-28

## Purpose

This probe tests whether the positive Qwen2.5-3B self-normalization signal
persists at the stronger Qwen2.5-7B 8-bit point before spending GPU on a
held-out test150 run.

## Setup

- Model: `Qwen/Qwen2.5-7B-Instruct`
- Quantization: bitsandbytes 8-bit
- Slice: `data/slices/validation_200_v4_dev50.jsonl`
- Variant: clean Banglish only
- Prompt mode: `banglish_self_normalize`
- Max new tokens: 128
- Successful package pins: `transformers==4.43.4`, `accelerate==0.33.0`,
  `bitsandbytes==0.43.3`

## Operational Note

The first attempt failed before evaluation rows with the known unpinned
Transformers 8-bit error:

```text
AttributeError: 'Qwen2ForCausalLM' object has no attribute 'set_submodule'
```

The retry succeeded after pinning the same stack used by the successful 7B
baseline/test runs.

## Result

| Condition | Correct |
| --- | ---: |
| Baseline dev50 clean Banglish | 13/50 |
| Self-normalized dev50 clean Banglish | 18/50 |

By dataset:

| Dataset | Baseline | Self-normalized | Delta |
| --- | ---: | ---: | ---: |
| BEnQA | 13/36 | 16/36 | +3 |
| BanglaMATH | 0/14 | 2/14 | +2 |

Paired bootstrap:

- Delta: +10 points.
- 95% CI: [-2, +22] points.
- Direction p: 0.0598.

Item changes:

- Gains: 7.
- Losses: 2.
- Net: +5.

Rewrite-quality audit:

| Dataset | n | Correct | Empty rewrites | Options not preserved | Digit count not preserved | Formulas not preserved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BEnQA | 36 | 16 | 0 | 1 | 6 | 3 |
| BanglaMATH | 14 | 2 | 0 | 0 | 0 | 0 |

## Decision

The dev result is positive enough to justify a held-out test150
self-normalization run. The claim should still be cautious until test150
finishes because the dev confidence interval is wide.

## Artifacts

- Output directory:
  `results/runs/qwen25_7b_8bit_validation200_v4_dev50_selfnorm_v2/`
- Item compare:
  `results/analysis/qwen25_7b_8bit_validation200_v4_dev50_baseline_vs_selfnorm_items_reparsed.csv`
- Summary compare:
  `results/analysis/qwen25_7b_8bit_validation200_v4_dev50_baseline_vs_selfnorm_summary_reparsed.csv`
- Bootstrap:
  `results/analysis/qwen25_7b_8bit_validation200_v4_dev50_selfnorm_bootstrap.csv`
- Rewrite quality:
  `results/analysis/qwen25_7b_8bit_validation200_v4_dev50_selfnorm_rewrite_quality_summary_reparsed.csv`
