# API Audit Response Import

Updated: 2026-06-05

- Provider: `deepseek`
- Model: `deepseek-v4-flash`
- Requests: `data/api_audit/validation200_v5_requests.jsonl`
- Raw responses: `results/api_audit/deepseek_v4_flash_validation200_v5_raw.jsonl`
- Imported results: `results/analysis/deepseek_v4_flash_validation200_v5_imported.jsonl`

## Validation

- Expected requests: 600
- Imported responses: 600
- Parsed-empty responses: 0
- Correct responses: 357
- Reported input tokens: 57285
- Reported output tokens: 3169

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
