# API Audit Response Import

Updated: 2026-06-04

- Provider: `openai`
- Model: `gpt-5.5-low-cap1024`
- Requests: `data/api_audit/openai_gpt55_validation200_v5_cap1024_requests.jsonl`
- Raw responses: `results/api_audit/openai_gpt55_low_validation200_v5_cap1024_raw.jsonl`
- Imported results: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_imported.jsonl`

## Validation

- Expected requests: 600
- Imported responses: 600
- Parsed-empty responses: 0
- Correct responses: 495
- Reported input tokens: 59852
- Reported output tokens: 59270

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
