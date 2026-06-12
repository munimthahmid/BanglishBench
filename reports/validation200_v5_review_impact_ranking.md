# Validation-200 v5 Review Impact Ranking

Updated: 2026-05-28

## Inputs

- Review queue: `data/slices/validation_200_v5_review_queue.csv`
- Ranked CSV: `results/analysis/validation200_v5_review_impact_ranking.csv`
- Impact-ordered packets: `reports/validation200_v5_review_packets_impact_order/README.md`
- Rows ranked: 140

This ranking is for review triage only. It does not mark any row as
correct, and it must not be used to auto-accept suggested Banglish edits.

## Tier Counts

| Tier | Rows |
| --- | ---: |
| `tier_1_review_first` | 43 |
| `tier_2_high` | 52 |
| `tier_3_medium` | 6 |
| `tier_4_low` | 39 |

## Split Counts

| Split | Rows |
| --- | ---: |
| `test` | 109 |
| `dev` | 31 |

## Priority Counts

| Priority bucket | Rows |
| --- | ---: |
| `both_wrong_single_edit` | 55 |
| `both_wrong_multi_edit` | 40 |
| `lower_priority` | 39 |
| `qwen25_wrong_multi_edit` | 4 |
| `qwen3_wrong_multi_edit` | 2 |

## Top 25 Rows

| Rank | Score | Tier | Split | ID | Dataset | Priority | Repl | Model signals | Suggested edit sample |
| ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | 177 | `tier_1_review_first` | test | `benqa_10th-Math_0044` | benqa | `both_wrong_multi_edit` | 2 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain, qwen3_agreement_route_gain | achhe->ache (1); ekoti->ekti (1) |
| 2 | 177 | `tier_1_review_first` | test | `benqa_12th-Chemistry-II_0228` | benqa | `both_wrong_multi_edit` | 2 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain, qwen3_agreement_route_gain | ekoti->ekti (1); konoti->konti (1) |
| 3 | 173 | `tier_1_review_first` | test | `benqa_8th-Math_0167` | benqa | `both_wrong_multi_edit` | 5 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain | ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1);... |
| 4 | 171 | `tier_1_review_first` | test | `benqa_12th-Physics-II_0046` | benqa | `both_wrong_multi_edit` | 2 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain | konoti->konti (1); kshetre->khetre (1) |
| 5 | 170 | `tier_1_review_first` | test | `banglamath_0526` | banglamath | `both_wrong_multi_edit` | 4 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain | ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1) |
| 6 | 170 | `tier_1_review_first` | test | `benqa_10th-Physics_0021` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain, qwen3_agreement_route_gain | konoti->konti (1) |
| 7 | 170 | `tier_1_review_first` | test | `benqa_8th-Science_0202` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain, qwen3_agreement_route_gain | konoti->konti (1) |
| 8 | 167 | `tier_1_review_first` | test | `benqa_12th-Biology-II_0287` | benqa | `both_wrong_multi_edit` | 2 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | konoti->konti (2) |
| 9 | 165 | `tier_1_review_first` | dev | `benqa_12th-Biology-I_0265` | benqa | `both_wrong_multi_edit` | 3 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | achhe->ache (1); ekoti->ekti (1); konoti->konti (1) |
| 10 | 164 | `tier_1_review_first` | test | `benqa_12th-Biology-I_0283` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | konoti->konti (1) |
| 11 | 164 | `tier_1_review_first` | test | `benqa_12th-Chemistry-I_0037` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | konoti->konti (1) |
| 12 | 162 | `tier_1_review_first` | dev | `benqa_8th-Science_0153` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain, qwen3_agreement_route_gain | konoti->konti (1) |
| 13 | 160 | `tier_1_review_first` | test | `benqa_10th-Biology_0128` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain | konoti->konti (1) |
| 14 | 160 | `tier_1_review_first` | test | `benqa_10th-Chemistry_0132` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | konoti->konti (1) |
| 15 | 160 | `tier_1_review_first` | test | `benqa_12th-Chemistry-II_0235` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | konoti->konti (1) |
| 16 | 160 | `tier_1_review_first` | test | `benqa_12th-Chemistry-I_0174` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | konoti->konti (1) |
| 17 | 155 | `tier_1_review_first` | test | `banglamath_0230` | banglamath | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen25_agreement_route_gain | kot->koto (1) |
| 18 | 154 | `tier_1_review_first` | test | `benqa_12th-Biology-II_0034` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable | konoti->konti (1) |
| 19 | 152 | `tier_1_review_first` | test | `banglamath_0231` | banglamath | `both_wrong_multi_edit` | 2 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable | ekoti->ekti (1); kot->koto (1) |
| 20 | 152 | `tier_1_review_first` | dev | `benqa_8th-Math_0085` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | kot->koto (1) |
| 21 | 150 | `tier_1_review_first` | test | `benqa_10th-Chemistry_0110` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen3_cross_script_recoverable | konoti->konti (1) |
| 22 | 148 | `tier_1_review_first` | test | `banglamath_0552` | banglamath | `both_wrong_multi_edit` | 4 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable | ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1) |
| 23 | 148 | `tier_1_review_first` | test | `benqa_10th-Biology_0156` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | kot->koto (1) |
| 24 | 148 | `tier_1_review_first` | test | `benqa_10th-Math_0271` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen3_cross_script_recoverable, qwen3_agreement_route_gain | kot->koto (1) |
| 25 | 148 | `tier_1_review_first` | test | `benqa_12th-Biology-I_0222` | benqa | `both_wrong_single_edit` | 1 | qwen25_v4_wrong, qwen3_v4_wrong, qwen25_cross_script_recoverable, qwen25_agreement_route_gain | konoti->konti (1) |

## Suggested Review Order

1. Review the impact-ordered packets first, especially held-out test150 rows in `tier_1_review_first`.
2. Then review `tier_2_high` rows with repeated substitutions, checking Bangla and English source text side by side.
3. Leave `tier_4_low` rows until the high-impact rows are resolved unless they share an obvious pattern already being reviewed.

After editing the queue, run:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```
