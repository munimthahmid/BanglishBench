# API Audit Response Import

Updated: 2026-06-07

- Provider: `Anthropic`
- Model: `claude-sonnet-4-6`
- Requests: `data/api_audit/benqa_human_gold_974_requests.jsonl`
- Raw responses: `results/api_audit/claude_sonnet_4_6_benqa_human_gold_974_raw.jsonl`
- Imported results: `results/analysis/claude_sonnet_4_6_benqa_human_gold_974_imported.jsonl`

## Validation

- Expected requests: 2922
- Imported responses: 2922
- Parsed-empty responses: 300
- Correct responses: 2059
- Reported input tokens: 370873
- Reported output tokens: 87633

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
