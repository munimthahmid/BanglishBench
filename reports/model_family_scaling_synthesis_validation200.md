# Model-Family and Scaling Synthesis: Validation-200

Updated: 2026-05-28

## Purpose

This report consolidates the scaling and model-family evidence that is currently
spread across the Qwen scaling, Qwen3-1.7B, and Phi-3.5-mini reports. The goal
is to make the thesis claim precise: clean Banglish creates a real script gap,
but the exact ordering depends on model competence and model family.

## Consolidated Results

| Model | Family | Slice | Thinking mode | Bangla | Clean Banglish | English | Banglish - Bangla | Banglish - English |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-0.5B-Instruct | Qwen2.5 | v3 | n/a | 40/200 | 44/200 | 40/200 | +2 pts, CI [-2.5, +7] | +2 pts, CI [-3, +7.5] |
| Qwen2.5-1.5B-Instruct | Qwen2.5 | v3 | n/a | 46/200 | 38/200 | 72/200 | -4 pts, CI [-10, +2] | -17 pts, CI [-24.5, -9.5] |
| Qwen2.5-3B-Instruct | Qwen2.5 | v3 | n/a | 54/200 | 38/200 | 71/200 | -8 pts, CI [-14, -2] | -16.5 pts, CI [-24, -9] |
| Qwen2.5-7B-Instruct 8-bit | Qwen2.5 | v4 | n/a | 65/200 | 48/200 | 94/200 | -8.5 pts, CI [-15.5, -1.5] | -23 pts, CI [-30.5, -15.5] |
| Qwen3-1.7B | Qwen3 | v4 | disabled | 34/200 | 36/200 | 61/200 | +1 pt, CI [-6, +7.5] | -12.5 pts, CI [-20, -5] |
| Qwen3-4B-Instruct-2507 | Qwen3 | v3 | not separately controlled | 80/200 | 46/200 | 88/200 | -17 pts, CI [-23.5, -10.5] | -21 pts, CI [-28.5, -13.5] |
| Phi-3.5-mini-instruct | Phi | v4 | n/a | 38/200 | 40/200 | 80/200 | +1 pt, CI [-4, +6] | -20 pts, CI [-28, -11.5] |

Structured artifact:

- `results/analysis/model_family_scaling_synthesis_validation200.csv`

## Dataset Split

| Model | Dataset | Bangla | Clean Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-0.5B | BEnQA | 40/144 | 43/144 | 37/144 |
| Qwen2.5-0.5B | BanglaMATH | 0/56 | 1/56 | 3/56 |
| Qwen2.5-1.5B | BEnQA | 44/144 | 38/144 | 67/144 |
| Qwen2.5-1.5B | BanglaMATH | 2/56 | 0/56 | 5/56 |
| Qwen2.5-3B | BEnQA | 49/144 | 38/144 | 66/144 |
| Qwen2.5-3B | BanglaMATH | 5/56 | 0/56 | 5/56 |
| Qwen2.5-7B 8-bit | BEnQA | 60/144 | 48/144 | 86/144 |
| Qwen2.5-7B 8-bit | BanglaMATH | 5/56 | 0/56 | 8/56 |
| Qwen3-1.7B no-thinking | BEnQA | 30/144 | 36/144 | 56/144 |
| Qwen3-1.7B no-thinking | BanglaMATH | 4/56 | 0/56 | 5/56 |
| Qwen3-4B | BEnQA | 76/144 | 45/144 | 82/144 |
| Qwen3-4B | BanglaMATH | 4/56 | 1/56 | 6/56 |
| Phi-3.5-mini | BEnQA | 37/144 | 40/144 | 67/144 |
| Phi-3.5-mini | BanglaMATH | 1/56 | 0/56 | 13/56 |

## Interpretation

The cleanest thesis narrative is a competence-threshold account.

First, the Banglish-vs-English gap is broad. It appears for Qwen2.5-1.5B,
Qwen2.5-3B, Qwen3-1.7B no-thinking, Qwen3-4B, and Phi-3.5-mini. This means
Latin-script Banglish is not simply being treated like English text by these
models, even though it is also Latin-script.

Second, the stronger Banglish-below-Bangla claim should be anchored in the
competent Qwen runs. Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B all show clean
Banglish below native Bangla with confidence intervals below zero. The Qwen3-4B
effect is the largest current Banglish-vs-Bangla result.

Third, weak or different-family models add nuance rather than contradiction.
Qwen2.5-0.5B is too weak/noisy. Qwen3-1.7B no-thinking and Phi-3.5-mini both
show a large English advantage over Banglish, but their Banglish-vs-Bangla
intervals cross zero. This says the thesis should not claim that Banglish is
always below native Bangla for every compact open model.

## Qwen3 Thinking Mode Caveat

Qwen3-1.7B default-thinking dev50 was not a valid baseline for this answer-only
protocol: outputs were dominated by truncated `<think>` traces. The corrected
Qwen3-1.7B results in this synthesis use `--disable-thinking`.

This caveat should be reported in any future Qwen3-family experiment. For
Qwen3-style models, thinking mode is part of the experimental condition.

## Thesis Claim To Use

The evidence supports this version:

> For competent Qwen models, the same Bangla content becomes substantially
> harder when written as clean Latin-script Banglish than when written in native
> Bengali script. Across several compact open models, Banglish is also much
> harder than English despite using Latin characters. The exact Banglish-vs-
> Bangla ordering is model-dependent, so the thesis should frame the result as
> a script-conditioned robustness gap, not as a universal ranking over all
> models.

## Thesis Claim To Avoid

Avoid saying:

- Banglish is universally harder than native Bangla for all LLMs.
- Smaller models prove the same effect as Qwen3-4B.
- Phi-3.5-mini replicates the Qwen result.
- Qwen3-family results are comparable unless thinking mode is controlled.

## Source Artifacts

- `reports/qwen_scaling_validation200.md`
- `reports/qwen25_7b_8bit_validation200_v4.md`
- `reports/qwen3_1_7b_nothink_validation200_v4.md`
- `reports/phi35_mini_validation200_v4.md`
- `results/runs/validation200_v3_qwen_scaling_by_variant_reparsed_rescored.csv`
- `results/runs/qwen25_7b_8bit_validation200_v4_full200_by_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_full200_by_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_full200_by_variant_reparsed_rescored.csv`
- `results/analysis/qwen25_0_5b_validation200_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen25_1_5b_validation200_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen25_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen25_7b_8bit_validation200_v4_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen25_7b_8bit_validation200_v4_banglish_minus_english_bootstrap.csv`
- `results/analysis/qwen3_1_7b_nothink_validation200_v4_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen3_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/phi35_validation200_v4_banglish_minus_bangla_bootstrap.csv`
