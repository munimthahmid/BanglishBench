# API Audit Response Import

Updated: 2026-06-04

- Provider: `gemini`
- Model: `gemini-3.5-flash`
- Requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Raw responses: `results/api_audit/gemini_3_5_flash_smoke10_v5_raw.jsonl`
- Imported results: `results/analysis/gemini_3_5_flash_smoke10_v5_imported.jsonl`

## Validation

- Expected requests: 30
- Imported responses: 30
- Parsed-empty responses: 1
- Correct responses: 26
- Reported input tokens: 2432
- Reported output tokens: 188

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
