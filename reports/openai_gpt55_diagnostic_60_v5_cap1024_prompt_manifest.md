# API Audit Prompt Manifest

Updated: 2026-06-04

## Purpose

This provider-neutral manifest freezes the exact paid-audit prompts without
calling any external API. Gold answers are intentionally excluded from the
request records.

## Artifacts

- Input slice: `data/slices/openai_gpt55_diagnostic_60_v5.jsonl`
- Request JSONL: `data/api_audit/openai_gpt55_diagnostic_60_v5_cap1024_requests.jsonl`
- Requests: 180
- Approximate prompt tokens: 9469

## Variant Counts

| Variant | Requests |
| --- | ---: |
| `bangla` | 60 |
| `banglish_clean` | 60 |
| `english` | 60 |

## Response Import Contract

Each provider response JSONL row must include `request_id` and `raw_output`.
Optional fields are `provider_response_id`, `usage_input_tokens`,
`usage_output_tokens`, and `seconds`. Import responses with
`scripts/import_api_audit_responses.py`.
