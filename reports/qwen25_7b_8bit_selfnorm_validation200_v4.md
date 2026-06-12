# Qwen2.5-7B 8-bit Self-Normalization Validation-200 v4

Updated: 2026-05-28

## Purpose

This report tests whether the Qwen2.5-3B self-normalization gain scales to
Qwen2.5-7B 8-bit under the validation-200 v4 dev/test protocol.

## Setup

- Model: `Qwen/Qwen2.5-7B-Instruct`
- Quantization: bitsandbytes 8-bit
- Package pins: `transformers==4.43.4`, `accelerate==0.33.0`,
  `bitsandbytes==0.43.3`
- Slice: `data/slices/validation_200_v4.jsonl`
- Split protocol: dev50 for go/no-go, test150 held out
- Variant: clean Banglish only
- Prompt mode: `banglish_self_normalize`
- Max new tokens: 128

## Operational Note

The first dev50 attempt failed before evaluation rows because the generated
Kaggle asset used an unpinned Transformers stack and hit the known
`Qwen2ForCausalLM.set_submodule` 8-bit error. The pinned retry completed, and
the same pinned stack was used for the held-out test150 run.

## Main Result

| Split | Baseline | Self-normalized | Delta | 95% CI | Direction p |
| --- | ---: | ---: | ---: | --- | ---: |
| Dev50 | 13/50 | 18/50 | +10.0 pts | [-2.0, +22.0] | 0.0598 |
| Test150 | 35/150 | 29/150 | -4.0 pts | [-12.0, +4.0] | 0.1882 |
| Full200 | 48/200 | 47/200 | -0.5 pts | [-7.0, +6.5] | 0.4699 |

The dev split was positive enough to justify test150, but the held-out result
did not replicate. On the full 200 items, self-normalization is effectively
flat for Qwen2.5-7B 8-bit.

## Dataset Breakdown

| Split | Dataset | Baseline | Self-normalized | Net |
| --- | --- | ---: | ---: | ---: |
| Dev50 | BEnQA | 13/36 | 16/36 | +3 |
| Dev50 | BanglaMATH | 0/14 | 2/14 | +2 |
| Test150 | BEnQA | 35/108 | 26/108 | -9 |
| Test150 | BanglaMATH | 0/42 | 3/42 | +3 |
| Full200 | BEnQA | 48/144 | 42/144 | -6 |
| Full200 | BanglaMATH | 0/56 | 5/56 | +5 |

The intervention helps the very low BanglaMATH baseline slightly, but loses too
many BEnQA items on held-out test150.

## Item Changes

| Split | Dataset | Gains | Losses | Same Correct | Same Wrong |
| --- | --- | ---: | ---: | ---: | ---: |
| Dev50 | BEnQA | 5 | 2 | 11 | 18 |
| Dev50 | BanglaMATH | 2 | 0 | 0 | 12 |
| Test150 | BEnQA | 13 | 22 | 13 | 60 |
| Test150 | BanglaMATH | 3 | 0 | 0 | 39 |
| Full200 | BEnQA | 18 | 24 | 24 | 78 |
| Full200 | BanglaMATH | 5 | 0 | 0 | 51 |

## Rewrite Quality

| Split | Dataset | n | Empty rewrites | Options not preserved | Digit count not preserved | Formulas not preserved |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dev50 | BEnQA | 36 | 0 | 1 | 6 | 3 |
| Dev50 | BanglaMATH | 14 | 0 | 0 | 0 | 0 |
| Test150 | BEnQA | 108 | 0 | 9 | 19 | 2 |
| Test150 | BanglaMATH | 42 | 0 | 0 | 6 | 0 |

Rewrite preservation is not clean enough for self-normalization to be treated
as a reliable answer-preserving preprocessing step. BEnQA option preservation
and numeric preservation errors are the most visible risk.

## Interpretation

This result changes the mitigation story in a useful way:

- Qwen2.5-3B self-normalization remains a real positive result on
  validation-200 v3: 38/200 -> 51/200.
- Qwen2.5-7B 8-bit does not show the same gain on validation-200 v4:
  48/200 -> 47/200 overall.
- A dev50-only signal would have been misleading. The dev/test protocol
  prevented overclaiming a mitigation that failed on held-out data.
- The safest thesis claim is now that same-model self-normalization is brittle
  across model scale, model family, and task mix. It is a useful diagnostic, not
  a general solution.

Decision: do not spend more GPU on plain Qwen2.5-7B self-normalization under
this prompt. Future mitigation work should focus on stronger routing,
answer-agreement signals, or a higher-quality normalizer rather than repeating
the same prompt at 7B.

## Routing Follow-Up

A local routing scan over the completed baseline and self-normalized outputs
found the same dev/test warning. Dev-best answer-signal rules tied always
self-normalize at 18/50 on dev but dropped to 29/150 on test. A conservative
task-aware route, self-normalize only BanglaMATH, reached 38/150 on test versus
35/150 baseline, but this is exploratory and modest.

Follow-up report:
`reports/qwen25_7b_8bit_selfnorm_routing_devtest.md`.

## Artifacts

- Dev50 output:
  `results/runs/qwen25_7b_8bit_validation200_v4_dev50_selfnorm_v2/`
- Test150 output:
  `results/runs/qwen25_7b_8bit_validation200_v4_test150_selfnorm/`
- Dev50 compare:
  `results/analysis/qwen25_7b_8bit_validation200_v4_dev50_baseline_vs_selfnorm_items_reparsed.csv`
- Test150 compare:
  `results/analysis/qwen25_7b_8bit_validation200_v4_test150_baseline_vs_selfnorm_items_reparsed.csv`
- Full200 compare:
  `results/analysis/qwen25_7b_8bit_validation200_v4_full200_baseline_vs_selfnorm_items_reparsed.csv`
- Full200 bootstrap:
  `results/analysis/qwen25_7b_8bit_validation200_v4_full200_selfnorm_bootstrap.csv`
- Rewrite quality:
  `results/analysis/qwen25_7b_8bit_validation200_v4_test150_selfnorm_rewrite_quality_summary_reparsed.csv`
- Routing follow-up:
  `reports/qwen25_7b_8bit_selfnorm_routing_devtest.md`
