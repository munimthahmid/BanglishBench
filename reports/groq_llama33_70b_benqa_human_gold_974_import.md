# API Audit Response Import

Updated: 2026-06-07

- Provider: `groq`
- Model: `llama-3.3-70b-versatile`
- Requests: `data/api_audit/benqa_human_gold_974_requests.jsonl`
- Raw responses: `results/api_audit/groq_llama33_70b_benqa_human_gold_974_raw.jsonl`
- Imported results: `results/analysis/groq_llama33_70b_benqa_human_gold_974_imported.jsonl`

## Validation

- Expected requests: 2922
- Imported responses: 2922
- Parsed-empty responses: 9
- Correct responses: 1502
- Reported input tokens: 449388
- Reported output tokens: 6611

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
