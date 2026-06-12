# API Audit Response Import

Updated: 2026-06-05

- Provider: `deepseek`
- Model: `deepseek-v4-flash`
- Requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Raw responses: `results/api_audit/deepseek_v4_flash_smoke10_v5_raw.jsonl`
- Imported results: `results/analysis/deepseek_v4_flash_smoke10_v5_imported.jsonl`

## Validation

- Expected requests: 30
- Imported responses: 30
- Parsed-empty responses: 0
- Correct responses: 26
- Reported input tokens: 2585
- Reported output tokens: 60

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
