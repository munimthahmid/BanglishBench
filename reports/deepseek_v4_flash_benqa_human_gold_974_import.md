# API Audit Response Import

Updated: 2026-06-07

- Provider: `deepseek`
- Model: `deepseek-v4-flash`
- Requests: `data/api_audit/benqa_human_gold_974_requests.jsonl`
- Raw responses: `results/api_audit/deepseek_v4_flash_benqa_human_gold_974_raw.jsonl`
- Imported results: `results/analysis/deepseek_v4_flash_benqa_human_gold_974_imported.jsonl`

## Validation

- Expected requests: 2922
- Imported responses: 2922
- Parsed-empty responses: 0
- Correct responses: 1985
- Reported input tokens: 302113
- Reported output tokens: 2995

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
