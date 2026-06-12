# API Audit Prompt Manifest

Updated: 2026-06-05

## Purpose

This provider-neutral manifest freezes the exact paid-audit prompts without
calling any external API. Gold answers are intentionally excluded from the
request records.

## Artifacts

- Input slice: `data/slices/validation_200_v5.jsonl`
- Request JSONL: `data/api_audit/validation200_v5_requests.jsonl`
- Requests: 600
- Approximate prompt tokens: 36471

## Variant Counts

| Variant | Requests |
| --- | ---: |
| `bangla` | 200 |
| `banglish_clean` | 200 |
| `english` | 200 |

## Response Import Contract

Each provider response JSONL row must include `request_id` and `raw_output`.
Optional fields are `provider_response_id`, `usage_input_tokens`,
`usage_output_tokens`, and `seconds`. Import responses with
`scripts/import_api_audit_responses.py`.
