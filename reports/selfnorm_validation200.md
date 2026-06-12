# Self-Normalization: Validation 200 v3

Updated: 2026-05-28

## Purpose

Validation-100 showed a model-dependent mitigation result:

- Qwen2.5-3B improved from 18/100 to 26/100 on Banglish.
- Qwen3-4B worsened from 18/100 to 11/100 on Banglish.

The validation-200 self-normalization runs test whether that model dependence
holds on the larger confirmation slice.

## Baselines

| Model | Clean Banglish Baseline |
| --- | ---: |
| Qwen2.5-3B | 38/200 |
| Qwen3-4B | 46/200 |

## Qwen2.5-3B

Artifacts:

- `results/runs/qwen2_5_3b_validation200_v3_selfnorm/`
- `results/analysis/qwen25_validation200_v3_baseline_vs_selfnorm_items_reparsed.csv`
- `results/analysis/qwen25_validation200_v3_baseline_vs_selfnorm_summary_reparsed.csv`
- `results/analysis/qwen25_validation200_v3_selfnorm_bootstrap.csv`
- `results/analysis/qwen25_validation200_v3_selfnorm_rewrite_quality_summary_reparsed.csv`
- `reports/qwen2_5_3b_validation200_v3_selfnorm_examples_reparsed.md`

Accuracy:

| Condition | Overall | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| Clean Banglish baseline | 38/200 | 38/144 | 0/56 |
| Self-normalized | 51/200 | 46/144 | 5/56 |

Paired result:

- Self-normalized minus baseline: +6.5 points.
- 95% CI: [+0.5, +13.0].
- Item flips: 27 gains and 14 losses.

Rewrite quality:

| Dataset | Mean Bengali Ratio | Mean Latin Ratio | Options Not Preserved | Digit Counts Not Preserved | Formulas Not Preserved |
| --- | ---: | ---: | ---: | ---: | ---: |
| BEnQA | 0.2907 | 0.3402 | 19/144 | 28/144 | 9/144 |
| BanglaMATH | 0.7862 | 0.0061 | 0/56 | 14/56 | 0/56 |

Interpretation:

- The validation-100 Qwen2.5 self-normalization gain transfers to
  validation-200.
- The gain is real but still brittle: there are 14 BEnQA losses and measurable
  option/digit/formula preservation errors.

## Qwen3-4B

Artifacts:

- `results/runs/qwen3_4b_validation200_v3_selfnorm/`
- `results/analysis/qwen3_validation200_v3_baseline_vs_selfnorm_items_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_baseline_vs_selfnorm_summary_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_selfnorm_bootstrap.csv`
- `results/analysis/qwen3_validation200_v3_selfnorm_rewrite_quality_summary_reparsed.csv`
- `reports/qwen3_4b_validation200_v3_selfnorm_examples_reparsed.md`

Accuracy:

| Condition | Overall | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| Clean Banglish baseline | 46/200 | 45/144 | 1/56 |
| Self-normalized | 21/200 | 17/144 | 4/56 |

Paired result:

- Self-normalized minus baseline: -12.5 points.
- 95% CI: [-19.5, -5.5].
- Item flips: 13 gains and 38 losses.

Rewrite quality:

| Dataset | Mean Bengali Ratio | Mean Latin Ratio | Options Not Preserved | Digit Counts Not Preserved | Formulas Not Preserved |
| --- | ---: | ---: | ---: | ---: | ---: |
| BEnQA | 0.4222 | 0.1733 | 3/144 | 14/144 | 1/144 |
| BanglaMATH | 0.7464 | 0.0180 | 0/56 | 1/56 | 0/56 |

Interpretation:

- The validation-100 negative Qwen3 self-normalization result also transfers to
  validation-200.
- Qwen3 rewrites preserve surface structure better than Qwen2.5 by these simple
  counters, but answer accuracy collapses on BEnQA. The failure is therefore
  not just option/digit corruption; the rewrite-and-answer procedure changes
  the model's decision behavior.

## Combined Takeaway

| Model | Baseline | Self-Normalized | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +6.5 points |
| Qwen3-4B | 46/200 | 21/200 | -12.5 points |

Self-normalization is a real mitigation for Qwen2.5 on this slice, but it is
not a general Banglish solution. The same intervention strongly hurts Qwen3,
which makes model-dependent mitigation a central thesis result rather than a
minor implementation detail.

## Planned Analysis

- Reparse and rescore generated outputs.
- Compare self-normalized answers against clean Banglish baseline.
- Bootstrap paired deltas.
- Audit `rewrite_output` to measure Bengali-script ratio and preservation of
  options, digits, and formulas.
- Export example reports for gains and losses.
