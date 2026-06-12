# API Audit Smoke Subset

Updated: 2026-06-11

## Inputs

- Items: `data/slices/validation_200_v5.jsonl`
- Impact ranking: `results/analysis/validation200_v5_review_impact_ranking.csv`
- Output JSONL: `data/slices/api_audit_smoke_10_v5.jsonl`

This subset is for paid-API prompt/token/cost smoke testing only. It is
not a replacement for full validation-200 reporting.

## Selected Items

| # | ID | Dataset | Split | Impact rank | Tier | Score | Reasons |
| ---: | --- | --- | --- | ---: | --- | ---: | --- |
| 1 | `benqa_10th-Math_0044` | benqa | test | 1 | `tier_1_review_first` | 177 | priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 2_suggested_replacements |
| 2 | `benqa_12th-Chemistry-II_0228` | benqa | test | 2 | `tier_1_review_first` | 177 | priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 2_suggested_replacements |
| 3 | `benqa_8th-Math_0167` | benqa | test | 3 | `tier_1_review_first` | 173 | priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 5_suggested_replacements |
| 4 | `benqa_12th-Physics-II_0046` | benqa | test | 4 | `tier_1_review_first` | 171 | priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 2_suggested_replacements; ksh_heavy |
| 5 | `banglamath_0526` | banglamath | test | 5 | `tier_1_review_first` | 170 | priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 4_suggested_replacements; ksh_heavy |
| 6 | `benqa_10th-Physics_0021` | benqa | test | 6 | `tier_1_review_first` | 170 | priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements |
| 7 | `benqa_8th-Science_0202` | benqa | test | 7 | `tier_1_review_first` | 170 | priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements |
| 8 | `banglamath_0230` | banglamath | test | 17 | `tier_1_review_first` | 155 | priority=both_wrong_single_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements |
| 9 | `banglamath_0231` | banglamath | test | 19 | `tier_1_review_first` | 152 | priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 2_suggested_replacements |
| 10 | `banglamath_0552` | banglamath | test | 22 | `tier_1_review_first` | 148 | priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 4_suggested_replacements; ksh_heavy |
