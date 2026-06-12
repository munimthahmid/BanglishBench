# API Audit Response Import

Updated: 2026-06-04

- Provider: `openai`
- Model: `gpt-5.5-low`
- Requests: `data/api_audit/openai_gpt55_diagnostic_60_v5_requests.jsonl`
- Raw responses: `results/api_audit/openai_gpt55_low_diagnostic_smoke3_v5_raw.jsonl`
- Imported results: `results/analysis/openai_gpt55_low_diagnostic_smoke3_v5_imported.jsonl`

## Validation

- Expected requests: 180
- Imported responses: 3
- Parsed-empty responses: 0
- Correct responses: 3
- Reported input tokens: 190
- Reported output tokens: 124

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
