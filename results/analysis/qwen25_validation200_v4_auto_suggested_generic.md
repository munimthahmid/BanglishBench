# Qwen2.5-3B Banglish Variant Sensitivity

Updated: 2026-05-28

## Inputs

- Baseline `v4`: `results/runs/qwen2_5_3b_validation200_v4_banglish/results/runs/qwen2_5_3b_validation200_v4_banglish.jsonl`
- Candidate `auto_suggested`: `results/runs/qwen2_5_3b_validation200_v4_auto_suggested_banglish/results/runs/qwen2_5_3b_validation200_v4_auto_suggested_banglish.jsonl`
- Summary CSV: `results/analysis/qwen25_validation200_v4_auto_suggested_generic_summary.csv`
- Item CSV: `results/analysis/qwen25_validation200_v4_auto_suggested_generic_items.csv`

## Overall

| Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| ---: | ---: | ---: | --- | ---: | ---: |
| 39/200 | 40/200 | +0.5 pts | [-1.5, +2.5] | 3 | 2 |

## Groups

| Group | n | Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| split=test | 150 | 31 | 32 | +0.7 pts | [-1.3, +3.3] | 2 | 1 |
| dataset=banglamath | 56 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=test;dataset=banglamath | 42 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=dev | 50 | 8 | 8 | +0.0 pts | [-6.0, +6.0] | 1 | 1 |
| split=dev;dataset=banglamath | 14 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| dataset=benqa | 144 | 39 | 40 | +0.7 pts | [-2.1, +3.5] | 3 | 2 |
| split=dev;dataset=benqa | 36 | 8 | 8 | +0.0 pts | [-8.3, +8.3] | 1 | 1 |
| split=test;dataset=benqa | 108 | 31 | 32 | +0.9 pts | [-1.8, +4.6] | 2 | 1 |

## Changed Items

- `loss` `benqa_10th-Physics_0280` `test` `benqa` gold=`B` v4=`B` auto_suggested=`A`
- `gain` `benqa_12th-Biology-II_0287` `test` `benqa` gold=`B` v4=`D` auto_suggested=`B`
- `gain` `benqa_12th-Chemistry-II_0235` `test` `benqa` gold=`A` v4=`C` auto_suggested=`A`
- `loss` `benqa_12th-Physics-II_0131` `dev` `benqa` gold=`B` v4=`B` auto_suggested=`A`
- `gain` `benqa_12th-Physics-I_0106` `dev` `benqa` gold=`D` v4=`B` auto_suggested=`D`
