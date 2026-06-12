# Qwen3-4B Banglish Variant Sensitivity

Updated: 2026-05-28

## Inputs

- Baseline `v4`: `results/runs/qwen3_4b_validation200_v4_banglish/results/runs/qwen3_4b_validation200_v4_banglish.jsonl`
- Candidate `v5_reviewed`: `results/runs/qwen3_4b_validation200_v5_banglish/results/runs/qwen3_4b_validation200_v5_banglish.jsonl`
- Summary CSV: `results/analysis/qwen3_validation200_v5_vs_v4_banglish_summary.csv`
- Item CSV: `results/analysis/qwen3_validation200_v5_vs_v4_banglish_items.csv`

## Overall

| Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| ---: | ---: | ---: | --- | ---: | ---: |
| 47/200 | 49/200 | +1.0 pts | [+0.0, +2.5] | 2 | 0 |

## Groups

| Group | n | Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| split=test | 150 | 32 | 34 | +1.3 pts | [+0.0, +3.3] | 2 | 0 |
| dataset=banglamath | 56 | 1 | 2 | +1.8 pts | [+0.0, +5.4] | 1 | 0 |
| split=test;dataset=banglamath | 42 | 1 | 2 | +2.4 pts | [+0.0, +7.1] | 1 | 0 |
| split=dev | 50 | 15 | 15 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=dev;dataset=banglamath | 14 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| dataset=benqa | 144 | 46 | 47 | +0.7 pts | [+0.0, +2.1] | 1 | 0 |
| split=dev;dataset=benqa | 36 | 15 | 15 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=test;dataset=benqa | 108 | 31 | 32 | +0.9 pts | [+0.0, +2.8] | 1 | 0 |

## Changed Items

- `gain` `banglamath_1697` `test` `banglamath` gold=`70` v4=`600` v5_reviewed=`70`
- `gain` `benqa_10th-Math-II_0326` `test` `benqa` gold=`C` v4=`A` v5_reviewed=`C`
