# Qwen2.5-3B Banglish Variant Sensitivity

Updated: 2026-05-28

## Inputs

- Baseline `v4`: `results/runs/qwen2_5_3b_validation200_v4_banglish/results/runs/qwen2_5_3b_validation200_v4_banglish.jsonl`
- Candidate `v5_reviewed`: `results/runs/qwen2_5_3b_validation200_v5_banglish/results/runs/qwen2_5_3b_validation200_v5_banglish.jsonl`
- Summary CSV: `results/analysis/qwen25_validation200_v5_vs_v4_banglish_summary.csv`
- Item CSV: `results/analysis/qwen25_validation200_v5_vs_v4_banglish_items.csv`

## Overall

| Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| ---: | ---: | ---: | --- | ---: | ---: |
| 39/200 | 41/200 | +1.0 pts | [-1.0, +3.0] | 3 | 1 |

## Groups

| Group | n | Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| split=test | 150 | 31 | 32 | +0.7 pts | [-1.3, +3.3] | 2 | 1 |
| dataset=banglamath | 56 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=test;dataset=banglamath | 42 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=dev | 50 | 8 | 9 | +2.0 pts | [+0.0, +6.0] | 1 | 0 |
| split=dev;dataset=banglamath | 14 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| dataset=benqa | 144 | 39 | 41 | +1.4 pts | [-1.4, +4.2] | 3 | 1 |
| split=dev;dataset=benqa | 36 | 8 | 9 | +2.8 pts | [+0.0, +8.3] | 1 | 0 |
| split=test;dataset=benqa | 108 | 31 | 32 | +0.9 pts | [-1.8, +4.6] | 2 | 1 |

## Changed Items

- `loss` `benqa_10th-Physics_0280` `test` `benqa` gold=`B` v4=`B` v5_reviewed=`A`
- `gain` `benqa_12th-Biology-II_0287` `test` `benqa` gold=`B` v4=`D` v5_reviewed=`B`
- `gain` `benqa_12th-Chemistry-II_0235` `test` `benqa` gold=`A` v4=`C` v5_reviewed=`A`
- `gain` `benqa_12th-Physics-I_0106` `dev` `benqa` gold=`D` v4=`B` v5_reviewed=`D`
