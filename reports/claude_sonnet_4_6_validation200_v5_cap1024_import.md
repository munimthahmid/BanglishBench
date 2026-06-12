# API Audit Response Import

Updated: 2026-06-05

- Provider: `anthropic`
- Model: `claude-sonnet-4-6`
- Requests: `data/api_audit/validation200_v5_requests.jsonl`
- Raw responses: `results/api_audit/claude_sonnet_4_6_validation200_v5_cap1024_raw.jsonl`
- Imported results: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_imported.jsonl`

## Validation

- Expected requests: 600
- Imported responses: 600
- Parsed-empty responses: 3
- Correct responses: 445
- Reported input tokens: 70903
- Reported output tokens: 51324

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
