# Qwen3-4B Banglish Variant Sensitivity

Updated: 2026-05-28

## Inputs

- Baseline `v4`: `results/runs/qwen3_4b_validation200_v4_banglish/results/runs/qwen3_4b_validation200_v4_banglish.jsonl`
- Candidate `auto_suggested`: `results/runs/qwen3_4b_validation200_v4_auto_suggested_banglish/results/runs/qwen3_4b_validation200_v4_auto_suggested_banglish.jsonl`
- Summary CSV: `results/analysis/qwen3_validation200_v4_auto_suggested_generic_summary.csv`
- Item CSV: `results/analysis/qwen3_validation200_v4_auto_suggested_generic_items.csv`

## Overall

| Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| ---: | ---: | ---: | --- | ---: | ---: |
| 47/200 | 48/200 | +0.5 pts | [+0.0, +1.5] | 1 | 0 |

## Groups

| Group | n | Baseline | Candidate | Delta | 95% CI | Gains | Losses |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| split=test | 150 | 32 | 33 | +0.7 pts | [+0.0, +2.0] | 1 | 0 |
| dataset=banglamath | 56 | 1 | 1 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=test;dataset=banglamath | 42 | 1 | 1 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=dev | 50 | 15 | 15 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=dev;dataset=banglamath | 14 | 0 | 0 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| dataset=benqa | 144 | 46 | 47 | +0.7 pts | [+0.0, +2.1] | 1 | 0 |
| split=dev;dataset=benqa | 36 | 15 | 15 | +0.0 pts | [+0.0, +0.0] | 0 | 0 |
| split=test;dataset=benqa | 108 | 31 | 32 | +0.9 pts | [+0.0, +2.8] | 1 | 0 |

## Changed Items

- `gain` `benqa_10th-Math-II_0326` `test` `benqa` gold=`C` v4=`A` auto_suggested=`C`
