# BEnQA 1,000 Human Review Freeze

Updated: 2026-06-07

## Files

- Source: `data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl`
- Human decisions: `results/analysis/benqa_extended_1000_v1_human_review_decisions.jsonl`
- Full reviewed audit slice: `data/slices/benqa_extended_1000_v1_human_reviewed.jsonl`
- Gold/pass slice: `data/slices/benqa_extended_1000_v1_human_gold.jsonl`

## Counts

- Source rows: 1000
- Full reviewed rows: 1000
- Gold/pass rows accepted for evaluation: 974

| Decision | Count |
| --- | ---: |
| accept | 618 |
| edited | 356 |
| reject | 26 |

## Freeze Status

Freeze is complete. Every source row has a valid human decision.

Rows marked `accept` or `edited` are included in the gold/pass output.
Rows marked `reject` or `unsure` remain in the audit slice but are excluded from the gold/pass output.
