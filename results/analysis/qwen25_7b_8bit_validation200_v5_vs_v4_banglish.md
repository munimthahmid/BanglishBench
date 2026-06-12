# Qwen2.5-7B-8bit Banglish Variant Sensitivity

Updated: 2026-05-30

## Inputs

- Baseline `v4`: `results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50.jsonl`, `results/runs/qwen25_7b_8bit_validation200_v4_test150/results/runs/qwen25_7b_8bit_validation200_v4_test150.jsonl`
- Candidate `v5-reviewed`: `results/runs/qwen25_7b_8bit_validation200_v5_banglish_pinned/results/runs/qwen2_5_7b_8bit_validation200_v5_banglish_pinned.jsonl`
- Summary CSV: `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish_summary.csv`
- Item CSV: `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish_items.csv`

## Overall

| Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| ---: | ---: | ---: | --- | ---: | ---: |
| 48/200 | 47/200 | -0.5 pts | [-3.5, +2.5] | 4 | 5 |

## Groups

| Group | n | Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| split=test | 150 | 35 | 35 | +0.0 pts | [-4.0, +3.3] | 4 | 4 |
| dataset=banglamath | 56 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=test;dataset=banglamath | 42 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=dev | 50 | 13 | 12 | -2.0 pts | [-6.0, +0.0] | 0 | 1 |
| split=dev;dataset=banglamath | 14 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| dataset=benqa | 144 | 48 | 47 | -0.7 pts | [-4.9, +3.5] | 4 | 5 |
| split=dev;dataset=benqa | 36 | 13 | 12 | -2.8 pts | [-8.3, +0.0] | 0 | 1 |
| split=test;dataset=benqa | 108 | 35 | 35 | +0.0 pts | [-5.6, +5.6] | 4 | 4 |

## Changed Items

- `loss` `benqa_10th-Chemistry_0280` `dev` `benqa` gold=`A` v4=`A` v5-reviewed=`B`
- `gain` `benqa_12th-Biology-II_0122` `test` `benqa` gold=`A` v4=`C` v5-reviewed=`A`
- `gain` `benqa_12th-Biology-II_0247` `test` `benqa` gold=`B` v4=`A` v5-reviewed=`B`
- `loss` `benqa_12th-Biology-II_0287` `test` `benqa` gold=`B` v4=`B` v5-reviewed=`D`
- `loss` `benqa_12th-Chemistry-II_0117` `test` `benqa` gold=`C` v4=`C` v5-reviewed=`B`
- `loss` `benqa_12th-Chemistry-II_0235` `test` `benqa` gold=`A` v4=`A` v5-reviewed=`B`
- `gain` `benqa_12th-Physics-II_0037` `test` `benqa` gold=`B` v4=`D` v5-reviewed=`B`
- `gain` `benqa_12th-Physics-I_0254` `test` `benqa` gold=`B` v4=`A` v5-reviewed=`B`
- `loss` `benqa_8th-Math_0167` `test` `benqa` gold=`C` v4=`C` v5-reviewed=`B`
