# Frozen-V5 Review-Label Sensitivity

Updated: 2026-06-11

## Scope

This no-spend check asks whether the final Banglish deficit is confined
to rows that needed v5 Banglish edits. It joins the frozen-v5 item review
labels with the frozen-v5 cross-script failure taxonomy.

- Machine-readable summary: `results/analysis/v5_review_label_sensitivity_summary.csv`
- Item source: `data/slices/validation_200_v5.jsonl`
- Failure-pattern source: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`

## Review-Label Counts

| Review label | Items |
| --- | ---: |
| `unreviewed` | 60 |
| `minor_edit` | 126 |
| `major_edit` | 11 |
| `bad` | 3 |

By dataset:

| Dataset | Unreviewed | Minor edit | Major edit | Bad |
| --- | ---: | ---: | ---: | ---: |
| `banglamath` | 9 | 38 | 9 | 0 |
| `benqa` | 51 | 88 | 2 | 3 |

## Main Buckets

| Model | Bucket | n | Bangla | Reviewed Banglish | English | Banglish - Bangla | Recoverable misses | Strict misses |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | `all` | 200 | 54 | 41 | 71 | -6.5 pts | 58 | 15 |
| Qwen2.5-3B | `unreviewed` | 60 | 16 | 13 | 24 | -5.0 pts | 21 | 3 |
| Qwen2.5-3B | `reviewed_nonbad` | 137 | 37 | 26 | 47 | -8.0 pts | 37 | 12 |
| Qwen2.5-3B | `reviewed_all` | 140 | 38 | 28 | 47 | -7.1 pts | 37 | 12 |
| Qwen2.5-3B | `strict197_nonbad` | 197 | 53 | 39 | 71 | -7.1 pts | 58 | 15 |
| Qwen2.5-7B 8-bit | `all` | 200 | 65 | 47 | 94 | -9.0 pts | 68 | 29 |
| Qwen2.5-7B 8-bit | `unreviewed` | 60 | 24 | 14 | 34 | -16.7 pts | 28 | 9 |
| Qwen2.5-7B 8-bit | `reviewed_nonbad` | 137 | 41 | 32 | 59 | -6.6 pts | 40 | 20 |
| Qwen2.5-7B 8-bit | `reviewed_all` | 140 | 41 | 33 | 60 | -5.7 pts | 40 | 20 |
| Qwen2.5-7B 8-bit | `strict197_nonbad` | 197 | 65 | 46 | 93 | -9.6 pts | 68 | 29 |
| Qwen3-4B | `all` | 200 | 80 | 49 | 88 | -15.5 pts | 59 | 32 |
| Qwen3-4B | `unreviewed` | 60 | 27 | 14 | 33 | -21.7 pts | 25 | 11 |
| Qwen3-4B | `reviewed_nonbad` | 137 | 52 | 34 | 54 | -13.1 pts | 34 | 21 |
| Qwen3-4B | `reviewed_all` | 140 | 53 | 35 | 55 | -12.9 pts | 34 | 21 |
| Qwen3-4B | `strict197_nonbad` | 197 | 79 | 48 | 87 | -15.7 pts | 59 | 32 |

## Fine Review Labels

| Model | Review label | n | Bangla | Reviewed Banglish | English | Banglish - Bangla | Recoverable misses | Strict misses |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | `unreviewed` | 60 | 16 | 13 | 24 | -5.0 pts | 21 | 3 |
| Qwen2.5-3B | `minor_edit` | 126 | 35 | 25 | 45 | -7.9 pts | 36 | 11 |
| Qwen2.5-3B | `major_edit` | 11 | 2 | 1 | 2 | -9.1 pts | 1 | 1 |
| Qwen2.5-3B | `bad` | 3 | 1 | 2 | 0 | +33.3 pts | 0 | 0 |
| Qwen2.5-7B 8-bit | `unreviewed` | 60 | 24 | 14 | 34 | -16.7 pts | 28 | 9 |
| Qwen2.5-7B 8-bit | `minor_edit` | 126 | 40 | 31 | 57 | -7.1 pts | 39 | 20 |
| Qwen2.5-7B 8-bit | `major_edit` | 11 | 1 | 1 | 2 | 0.0 pts | 1 | 0 |
| Qwen2.5-7B 8-bit | `bad` | 3 | 0 | 1 | 1 | +33.3 pts | 0 | 0 |
| Qwen3-4B | `unreviewed` | 60 | 27 | 14 | 33 | -21.7 pts | 25 | 11 |
| Qwen3-4B | `minor_edit` | 126 | 52 | 34 | 53 | -14.3 pts | 33 | 21 |
| Qwen3-4B | `major_edit` | 11 | 0 | 0 | 1 | 0.0 pts | 1 | 0 |
| Qwen3-4B | `bad` | 3 | 1 | 1 | 1 | 0.0 pts | 0 | 0 |

## Interpretation

- The reviewed-v5 Banglish deficit is not confined to edited rows.
  Unreviewed rows and reviewed non-bad rows both show Banglish below
  native Bangla for all three thesis-facing Qwen rows.
- The three `bad` rows are too few to interpret and are not driving the
  release-facing result; the separate strict-197 sensitivity remains the
  denominator check for excluding them.
- `major_edit` rows are only 11 items, so their per-label accuracies are
  descriptive audit evidence rather than a stable performance stratum.

Thesis-safe phrasing:

> The human-review process improves benchmark quality, but the measured
> Banglish deficit is visible in both unreviewed and reviewed non-bad
> v5 buckets. The gap is therefore not solely an artifact of the rows
> that required manual Banglish edits.
