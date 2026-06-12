# Validation-200 v5 Review Packets

Updated: 2026-05-28

## Purpose

These Markdown packets make the source-aware v5 review queue easier to
read in batches. They are read-only reviewer aids; the authoritative
worksheet remains the CSV queue.

## Inputs

- Queue: `data/slices/validation_200_v5_review_queue.csv`
- Batch size: 25

## Progress

- Rows: 140
- Packets: 6

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

| Dataset | Rows |
| --- | ---: |
| `benqa` | 93 |
| `banglamath` | 47 |

## Packet Files

- `reports/validation200_v5_review_packets/batch_01.md`
- `reports/validation200_v5_review_packets/batch_02.md`
- `reports/validation200_v5_review_packets/batch_03.md`
- `reports/validation200_v5_review_packets/batch_04.md`
- `reports/validation200_v5_review_packets/batch_05.md`
- `reports/validation200_v5_review_packets/batch_06.md`

## Validation

After editing the CSV queue, run:

```bash
python3 scripts/validate_banglish_review_queue.py
```

Before freezing v5, run:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```
