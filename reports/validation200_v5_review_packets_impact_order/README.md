# Validation-200 v5 Review Packets

Updated: 2026-05-28

## Purpose

These Markdown packets make the source-aware v5 review queue easier to
read in batches. They are read-only reviewer aids; the authoritative
worksheet remains the CSV queue.

This packet set includes impact-rank metadata from the v5 review
impact ranking CSV.

## Inputs

- Queue: `data/slices/validation_200_v5_review_queue.csv`
- Batch size: 20

## Progress

- Rows: 140
- Packets: 7

| Status | Rows |
| --- | ---: |
| `pending` | 140 |

| Priority bucket | Rows |
| --- | ---: |
| `both_wrong_single_edit` | 55 |
| `both_wrong_multi_edit` | 40 |
| `lower_priority` | 39 |
| `qwen25_wrong_multi_edit` | 4 |
| `qwen3_wrong_multi_edit` | 2 |

| Impact tier | Rows |
| --- | ---: |
| `tier_2_high` | 52 |
| `tier_1_review_first` | 43 |
| `tier_4_low` | 39 |
| `tier_3_medium` | 6 |

| Dataset | Rows |
| --- | ---: |
| `benqa` | 93 |
| `banglamath` | 47 |

## Packet Files

- `reports/validation200_v5_review_packets_impact_order/batch_01.md`
- `reports/validation200_v5_review_packets_impact_order/batch_02.md`
- `reports/validation200_v5_review_packets_impact_order/batch_03.md`
- `reports/validation200_v5_review_packets_impact_order/batch_04.md`
- `reports/validation200_v5_review_packets_impact_order/batch_05.md`
- `reports/validation200_v5_review_packets_impact_order/batch_06.md`
- `reports/validation200_v5_review_packets_impact_order/batch_07.md`

## Validation

After editing the CSV queue, run:

```bash
python3 scripts/validate_banglish_review_queue.py
```

Before freezing v5, run:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```
