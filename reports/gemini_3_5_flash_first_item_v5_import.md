# API Audit Response Import

Updated: 2026-06-04

- Provider: `gemini`
- Model: `gemini-3.5-flash`
- Requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Raw responses: `results/api_audit/gemini_3_5_flash_first_item_v5_raw.jsonl`
- Imported results: `results/analysis/gemini_3_5_flash_first_item_v5_imported.jsonl`

## Validation

- Expected requests: 30
- Imported responses: 3
- Parsed-empty responses: 0
- Correct responses: 3
- Reported input tokens: 226
- Reported output tokens: 3

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
