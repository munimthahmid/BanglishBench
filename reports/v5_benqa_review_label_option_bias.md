# Frozen-V5 BEnQA Review-Label Option-Bias Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether Qwen3-4B's reviewed-Banglish BEnQA
D-attractor can be reduced to rows that were selected for v5 Banglish
review or manual edits. It joins frozen-v5 review labels with the BEnQA
choice-bias item table.

- Item table: `results/analysis/v5_benqa_review_label_option_bias_items.csv`
- Summary table: `results/analysis/v5_benqa_review_label_option_bias_summary.csv`

## Headline

- Overall, Qwen3-4B predicts D on 111/144 BEnQA rows while gold D appears on 39/144 rows.
- On unreviewed BEnQA rows, Qwen3-4B still predicts D on 39/51 rows (76.5%) with wrong D on 28/51; gold D is only 13/51.
- On minor-edit rows, Qwen3-4B predicts D on 67/88 rows and wrong D on 45/88.
- On reviewed nonbad rows, Qwen3-4B predicts D on 69/90 rows; the corresponding Qwen2.5 D counts are 28/90 and 17/90.
- Even in the unreviewed bucket, Qwen2.5 rows remain much lower at 10/51 and 7/51 D predictions.

## Summary

| Model | Bucket | N | Correct | Gold D | Pred D | Wrong D | D over gold-D |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | All BEnQA rows | 144 | 41 | 39 | 39 | 25 | 0 |
| Qwen2.5-3B | Rows not selected for v5 Banglish review | 51 | 13 | 13 | 10 | 7 | -3 |
| Qwen2.5-3B | Rows with minor Banglish edit | 88 | 25 | 25 | 28 | 18 | 3 |
| Qwen2.5-3B | Rows with major Banglish edit | 2 | 1 | 0 | 0 | 0 | 0 |
| Qwen2.5-3B | Rows flagged bad under the default all-200 policy | 3 | 2 | 1 | 1 | 0 | 0 |
| Qwen2.5-3B | Minor/major edited rows | 90 | 26 | 25 | 28 | 18 | 3 |
| Qwen2.5-3B | All rows selected for v5 review | 93 | 28 | 26 | 29 | 18 | 3 |
| Qwen2.5-3B | All rows except bad | 141 | 39 | 38 | 38 | 25 | 0 |
| Qwen2.5-7B 8-bit | All BEnQA rows | 144 | 47 | 39 | 25 | 17 | -14 |
| Qwen2.5-7B 8-bit | Rows not selected for v5 Banglish review | 51 | 14 | 13 | 7 | 6 | -6 |
| Qwen2.5-7B 8-bit | Rows with minor Banglish edit | 88 | 31 | 25 | 17 | 11 | -8 |
| Qwen2.5-7B 8-bit | Rows with major Banglish edit | 2 | 1 | 0 | 0 | 0 | 0 |
| Qwen2.5-7B 8-bit | Rows flagged bad under the default all-200 policy | 3 | 1 | 1 | 1 | 0 | 0 |
| Qwen2.5-7B 8-bit | Minor/major edited rows | 90 | 32 | 25 | 17 | 11 | -8 |
| Qwen2.5-7B 8-bit | All rows selected for v5 review | 93 | 33 | 26 | 18 | 11 | -8 |
| Qwen2.5-7B 8-bit | All rows except bad | 141 | 46 | 38 | 24 | 17 | -14 |
| Qwen3-4B | All BEnQA rows | 144 | 47 | 39 | 111 | 77 | 72 |
| Qwen3-4B | Rows not selected for v5 Banglish review | 51 | 14 | 13 | 39 | 28 | 26 |
| Qwen3-4B | Rows with minor Banglish edit | 88 | 32 | 25 | 67 | 45 | 42 |
| Qwen3-4B | Rows with major Banglish edit | 2 | 0 | 0 | 2 | 2 | 2 |
| Qwen3-4B | Rows flagged bad under the default all-200 policy | 3 | 1 | 1 | 3 | 2 | 2 |
| Qwen3-4B | Minor/major edited rows | 90 | 32 | 25 | 69 | 47 | 44 |
| Qwen3-4B | All rows selected for v5 review | 93 | 33 | 26 | 72 | 49 | 46 |
| Qwen3-4B | All rows except bad | 141 | 46 | 38 | 108 | 75 | 70 |

## Interpretation

- Qwen3's D-attractor is present in both unreviewed and edited BEnQA rows,
  so it is not a simple artifact of human-reviewed edits.
- Gold-D counts are modest in the unreviewed and minor-edit buckets, so
  the high Qwen3 D count is not explained by review-label-specific gold
  label balance.
- The major-edit and bad buckets are too small for standalone claims;
  use them only as completeness checks.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_review_label_option_bias.py`
- Item table: `results/analysis/v5_benqa_review_label_option_bias_items.csv`
- Summary table: `results/analysis/v5_benqa_review_label_option_bias_summary.csv`
