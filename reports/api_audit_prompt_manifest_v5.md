# API Audit Prompt Manifest

Updated: 2026-06-11

## Purpose

This provider-neutral manifest freezes the exact paid-audit prompts without
calling any external API. Gold answers are intentionally excluded from the
request records.

## Artifacts

- Input slice: `data/slices/api_audit_smoke_10_v5.jsonl`
- Request JSONL: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Requests: 30
- Approximate prompt tokens: 1736

## Variant Counts

| Variant | Requests |
| --- | ---: |
| `bangla` | 10 |
| `banglish_clean` | 10 |
| `english` | 10 |

## Response Import Contract

Each provider response JSONL row must include `request_id` and `raw_output`.
Optional fields are `provider_response_id`, `usage_input_tokens`,
`usage_output_tokens`, and `seconds`. Import responses with
`scripts/import_api_audit_responses.py`.
