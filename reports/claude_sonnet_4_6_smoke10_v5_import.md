# API Audit Response Import

Updated: 2026-06-05

- Provider: `anthropic`
- Model: `claude-sonnet-4-6`
- Requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Raw responses: `results/api_audit/claude_sonnet_4_6_smoke10_v5_raw.jsonl`
- Imported results: `results/analysis/claude_sonnet_4_6_smoke10_v5_imported.jsonl`

## Validation

- Expected requests: 30
- Imported responses: 30
- Parsed-empty responses: 1
- Correct responses: 22
- Reported input tokens: 3314
- Reported output tokens: 1027

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
