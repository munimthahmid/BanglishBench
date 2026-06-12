# Oracle Routing: Baseline vs Self-Normalization

Updated: 2026-05-28

## Purpose

Self-normalization creates both gains and losses. This analysis computes an
oracle upper bound: how many items would be correct if a perfect router could
choose the direct Banglish answer when it is right and the self-normalized
answer when that is right.

This is not a deployable method. It estimates the value of future uncertainty
routing or consistency checks.

## Artifacts

- `scripts/oracle_union_from_compare.py`
- `results/analysis/qwen25_validation200_v3_baseline_selfnorm_oracle_union.csv`
- `results/analysis/qwen25_validation200_v3_baseline_selfnorm_oracle_union_overall.csv`
- `results/analysis/qwen3_validation200_v3_baseline_selfnorm_oracle_union.csv`
- `results/analysis/qwen3_validation200_v3_baseline_selfnorm_oracle_union_overall.csv`

## Overall Oracle Results

| Model | Baseline | Self-Normalized | Oracle Union | Oracle Gain vs Baseline |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | 65/200 | +13.5 points |
| Qwen3-4B | 46/200 | 21/200 | 59/200 | +6.5 points |

## Dataset Split

| Model | Dataset | Baseline | Self-Normalized | Oracle Union |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | BEnQA | 38/144 | 46/144 | 60/144 |
| Qwen2.5-3B | BanglaMATH | 0/56 | 5/56 | 5/56 |
| Qwen3-4B | BEnQA | 45/144 | 17/144 | 55/144 |
| Qwen3-4B | BanglaMATH | 1/56 | 4/56 | 4/56 |

## Interpretation

For Qwen2.5, self-normalization is directly useful and also complementary: it
adds 27 gains but introduces 14 losses.

For Qwen3, self-normalization is harmful as a direct strategy, but still creates
13 gains. The problem is routing: 38 baseline-correct BEnQA items become wrong
after self-normalization.

This suggests a future mitigation direction:

- Do not always normalize.
- Generate both direct and normalized answers.
- Route only when confidence, agreement, or rewrite-quality checks suggest the
  normalized path is safer.

The thesis should present this as an upper-bound analysis, not as achieved
accuracy.
