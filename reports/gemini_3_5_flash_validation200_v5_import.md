# API Audit Response Import

Updated: 2026-06-04

- Provider: `gemini`
- Model: `gemini-3.5-flash`
- Requests: `data/api_audit/gemini_3_5_flash_validation200_v5_requests.jsonl`
- Raw responses: `results/api_audit/gemini_3_5_flash_validation200_v5_raw.jsonl`
- Imported results: `results/analysis/gemini_3_5_flash_validation200_v5_imported.jsonl`

## Validation

- Expected requests: 600
- Imported responses: 600
- Parsed-empty responses: 6
- Correct responses: 443
- Reported input tokens: 54648
- Reported output tokens: 37191

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
