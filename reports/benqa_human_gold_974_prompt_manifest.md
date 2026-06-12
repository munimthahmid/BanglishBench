# API Audit Prompt Manifest

Updated: 2026-06-07

## Purpose

This provider-neutral manifest freezes the exact paid-audit prompts without
calling any external API. Gold answers are intentionally excluded from the
request records.

## Artifacts

- Input slice: `data/slices/benqa_extended_1000_v1_human_gold.jsonl`
- Request JSONL: `data/api_audit/benqa_human_gold_974_requests.jsonl`
- Requests: 2922
- Approximate prompt tokens: 184740

## Variant Counts

| Variant | Requests |
| --- | ---: |
| `bangla` | 974 |
| `banglish_clean` | 974 |
| `english` | 974 |

## Response Import Contract

Each provider response JSONL row must include `request_id` and `raw_output`.
Optional fields are `provider_response_id`, `usage_input_tokens`,
`usage_output_tokens`, and `seconds`. Import responses with
`scripts/import_api_audit_responses.py`.
