# API Audit Response Import

Updated: 2026-06-07

- Provider: `OpenAI`
- Model: `gpt-5.5-none`
- Requests: `data/api_audit/benqa_human_gold_974_requests.jsonl`
- Raw responses: `results/api_audit/openai_gpt55_none_benqa_human_gold_974_raw.jsonl`
- Imported results: `results/analysis/openai_gpt55_none_benqa_human_gold_974_imported.jsonl`

## Validation

- Expected requests: 2922
- Imported responses: 2922
- Parsed-empty responses: 0
- Correct responses: 2344
- Reported input tokens: 316948
- Reported output tokens: 14610

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
