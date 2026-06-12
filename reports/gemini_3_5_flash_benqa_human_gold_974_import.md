# API Audit Response Import

Updated: 2026-06-07

- Provider: `Google`
- Model: `gemini-3.5-flash`
- Requests: `data/api_audit/benqa_human_gold_974_requests.jsonl`
- Raw responses: `results/api_audit/gemini_3_5_flash_benqa_human_gold_974_raw.jsonl`
- Imported results: `results/analysis/gemini_3_5_flash_benqa_human_gold_974_imported.jsonl`

## Validation

- Expected requests: 2922
- Imported responses: 2922
- Parsed-empty responses: 650
- Correct responses: 2056
- Reported input tokens: 292959
- Reported output tokens: 89953

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
