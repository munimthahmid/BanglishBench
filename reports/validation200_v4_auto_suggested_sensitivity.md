# Auto-Suggested Banglish Sensitivity Results

Updated: 2026-05-28

## Artifacts

- Summary CSV: `results/analysis/validation200_v4_auto_suggested_sensitivity_summary.csv`
- Item CSV: `results/analysis/validation200_v4_auto_suggested_sensitivity_items.csv`

## Main Table

| Model | v3 | v4 | auto-suggested | auto-v4 delta | 95% CI | gains | losses |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | 38/200 | 39/200 | 40/200 | +0.0050 | [-0.0150, +0.0250] | 3 | 2 |
| Qwen3-4B | 46/200 | 47/200 | 48/200 | +0.0050 | [+0.0000, +0.0150] | 1 | 0 |

## Caveat

The auto-suggested slice is heuristic and unreviewed. Use this only as a sensitivity analysis until the human-review workflow freezes a v5 slice.

## Auto-v4 Changed Items

- `Qwen2.5-3B` `benqa_10th-Physics_0280` `benqa` loss: v4=`B`, auto=`A`, gold=`B`
- `Qwen2.5-3B` `benqa_12th-Biology-II_0287` `benqa` gain: v4=`D`, auto=`B`, gold=`B`
- `Qwen2.5-3B` `benqa_12th-Chemistry-II_0235` `benqa` gain: v4=`C`, auto=`A`, gold=`A`
- `Qwen2.5-3B` `benqa_12th-Physics-II_0131` `benqa` loss: v4=`B`, auto=`A`, gold=`B`
- `Qwen2.5-3B` `benqa_12th-Physics-I_0106` `benqa` gain: v4=`B`, auto=`D`, gold=`D`
- `Qwen3-4B` `benqa_10th-Math-II_0326` `benqa` gain: v4=`A`, auto=`C`, gold=`C`
