# API Audit Prompt Manifest

Updated: 2026-06-05

## Purpose

This provider-neutral manifest freezes the exact paid-audit prompts without
calling any external API. Gold answers are intentionally excluded from the
request records.

## Artifacts

- Input slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Request JSONL: `data/api_audit/deepseek_v4_flash_benqa_ext_full851_requests.jsonl`
- Requests: 2553
- Approximate prompt tokens: 159178

## Variant Counts

| Variant | Requests |
| --- | ---: |
| `bangla` | 851 |
| `banglish_clean` | 851 |
| `english` | 851 |

## Response Import Contract

Each provider response JSONL row must include `request_id` and `raw_output`.
Optional fields are `provider_response_id`, `usage_input_tokens`,
`usage_output_tokens`, and `seconds`. Import responses with
`scripts/import_api_audit_responses.py`.
