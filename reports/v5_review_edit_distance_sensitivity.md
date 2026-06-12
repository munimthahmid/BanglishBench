# V5 Review Edit-Distance Sensitivity Audit

Updated: 2026-06-11

## Inputs

- Review audit: `results/analysis/validation200_v5_banglish_review_audit.csv`
- Recoverability items: `results/analysis/v5_recoverability_source_items.csv`
- Main dataset intervals for all-item rows: `results/analysis/v5_dataset_gap_intervals.csv`
- Item sensitivity CSV: `results/analysis/v5_review_edit_distance_sensitivity_items.csv`
- Summary CSV: `results/analysis/v5_review_edit_distance_sensitivity_summary.csv`

## Headline

- Applied-edit buckets: No applied Banglish change=63, Tiny edit <=0.5%=73, Small edit >0.5% to <=2%=45, Larger edit >2%=19
- The no-applied-change subset already shows reviewed Banglish below Bangla and English for all three thesis-facing Qwen rows.
- Larger-edit rows are few (19 items), so they are a quality-control caveat, not a standalone statistical source of the main result.

## All Items And Edit Buckets

| Model | Bucket | n | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Recoverable misses |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | All frozen-v5 items | 200 | 54/200 (27.0%) | 41/200 (20.5%) | 71/200 (35.5%) | -6.5 pts [-12.5, 0.0] | -15.0 pts [-22.0, -7.5] | 58 |
| Qwen2.5-3B | No applied Banglish change | 63 | 17/63 (27.0%) | 15/63 (23.8%) | 24/63 (38.1%) | -3.2 pts [-14.3, +7.9] | -14.3 pts [-28.6, 0.0] | 21 |
| Qwen2.5-3B | Tiny edit <=0.5% | 73 | 26/73 (35.6%) | 20/73 (27.4%) | 30/73 (41.1%) | -8.2 pts [-19.2, +2.7] | -13.7 pts [-26.0, -1.4] | 22 |
| Qwen2.5-3B | Small edit >0.5% to <=2% | 45 | 8/45 (17.8%) | 5/45 (11.1%) | 13/45 (28.9%) | -6.7 pts [-20.0, +6.7] | -17.8 pts [-33.3, -4.4] | 12 |
| Qwen2.5-3B | Larger edit >2% | 19 | 3/19 (15.8%) | 1/19 (5.3%) | 4/19 (21.1%) | -10.5 pts [-26.3, 0.0] | -15.8 pts [-31.6, 0.0] | 3 |
| Qwen2.5-7B 8-bit | All frozen-v5 items | 200 | 65/200 (32.5%) | 47/200 (23.5%) | 94/200 (47.0%) | -9.0 pts [-16.5, -2.0] | -23.5 pts [-31.0, -16.0] | 68 |
| Qwen2.5-7B 8-bit | No applied Banglish change | 63 | 24/63 (38.1%) | 15/63 (23.8%) | 35/63 (55.6%) | -14.3 pts [-28.6, 0.0] | -31.8 pts [-44.4, -19.1] | 28 |
| Qwen2.5-7B 8-bit | Tiny edit <=0.5% | 73 | 24/73 (32.9%) | 23/73 (31.5%) | 35/73 (47.9%) | -1.4 pts [-13.7, +12.3] | -16.4 pts [-31.5, -1.4] | 22 |
| Qwen2.5-7B 8-bit | Small edit >0.5% to <=2% | 45 | 15/45 (33.3%) | 8/45 (17.8%) | 20/45 (44.4%) | -15.6 pts [-28.9, -2.2] | -26.7 pts [-40.0, -13.3] | 15 |
| Qwen2.5-7B 8-bit | Larger edit >2% | 19 | 2/19 (10.5%) | 1/19 (5.3%) | 4/19 (21.1%) | -5.3 pts [-15.8, 0.0] | -15.8 pts [-31.6, 0.0] | 3 |
| Qwen3-4B | All frozen-v5 items | 200 | 80/200 (40.0%) | 49/200 (24.5%) | 88/200 (44.0%) | -15.5 pts [-22.0, -9.0] | -19.5 pts [-27.0, -12.0] | 59 |
| Qwen3-4B | No applied Banglish change | 63 | 28/63 (44.4%) | 15/63 (23.8%) | 34/63 (54.0%) | -20.6 pts [-33.3, -9.5] | -30.2 pts [-42.9, -17.5] | 25 |
| Qwen3-4B | Tiny edit <=0.5% | 73 | 36/73 (49.3%) | 25/73 (34.2%) | 31/73 (42.5%) | -15.1 pts [-26.0, -4.1] | -8.2 pts [-23.3, +5.5] | 20 |
| Qwen3-4B | Small edit >0.5% to <=2% | 45 | 16/45 (35.6%) | 9/45 (20.0%) | 20/45 (44.4%) | -15.6 pts [-28.9, -2.2] | -24.4 pts [-37.8, -13.3] | 11 |
| Qwen3-4B | Larger edit >2% | 19 | 0/19 (0.0%) | 0/19 (0.0%) | 3/19 (15.8%) | 0.0 pts [0.0, 0.0] | -15.8 pts [-31.6, 0.0] | 3 |

## Interpretation

This audit separates the magnitude of applied v5 Banglish edits from
model behavior. It shows that the deficit is not introduced only by
rows that required heavier review edits: the no-applied-change subset
already contains the same directional pattern. The larger-edit bucket
is useful for dataset transparency but is too small to support a
standalone effect-size claim.
