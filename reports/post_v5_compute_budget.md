# Post-v5 Compute Budget

Updated: 2026-06-11

This budget estimates Kaggle GPU time for the readiness-gated post-v5
reruns. It does not launch or prepare jobs.

Machine-readable budget: `results/analysis/post_v5_compute_budget.csv`.

## Summary

- Available Kaggle budget assumption: 4 accounts x 30h = 120 GPU-hours.
- Required post-v5 reruns, conservative: 0.89 GPU-hours.
- Required plus conditional 7B rerun, conservative: 1.51 GPU-hours.
- Required budget share: 0.74% of assumed Kaggle hours.
- Required plus conditional budget share: 1.26% of assumed Kaggle hours.

## Job Budget

| Priority | Run id | Condition | Status | Planned outputs | Estimate h | Conservative h | Evidence |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| 1 | `qwen25_3b_validation200_v5_banglish` | `required_after_readiness` | `ready_to_prepare` | 200 | 0.176 | 0.352 | qwen2_5_3b_validation200_v4_banglish Kaggle log ended at about 334 seconds |
| 2 | `qwen3_4b_validation200_v5_banglish` | `required_after_readiness` | `ready_to_prepare` | 200 | 0.270 | 0.540 | qwen3_4b_validation200_v4_banglish Kaggle log ended at about 672 seconds |
| 3 | `qwen25_7b_8bit_validation200_v5_banglish` | `conditional_if_v5_changes_main_table_or_7b_remains_primary` | `conditional_manual_decision` | 200 | 0.308 | 0.616 | qwen25_7b_8bit_validation200_v4_test150 triad log ended at about 1144 seconds |

## Interpretation

- The required v5 reruns are small relative to the available Kaggle budget.
- The gating issue is not GPU-hour scarcity; it is the manual v5 review and
  freeze/readiness path.
- Keep Qwen2.5-7B 8-bit conditional unless v5 materially changes held-out
  rows or the 7B result remains thesis-critical.
- Do not use this budget as permission to launch jobs while
  `reports/post_v5_kaggle_job_plan.md` is still `not_ready`.

