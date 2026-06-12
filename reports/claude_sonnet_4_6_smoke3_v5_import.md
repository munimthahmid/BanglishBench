# API Audit Response Import

Updated: 2026-06-05

- Provider: `anthropic`
- Model: `claude-sonnet-4-6`
- Requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Raw responses: `results/api_audit/claude_sonnet_4_6_smoke3_v5_raw.jsonl`
- Imported results: `results/analysis/claude_sonnet_4_6_smoke3_v5_imported.jsonl`

## Validation

- Expected requests: 30
- Imported responses: 3
- Parsed-empty responses: 0
- Correct responses: 2
- Reported input tokens: 271
- Reported output tokens: 12

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
