# API Audit Response Import

Updated: 2026-06-05

- Provider: `groq`
- Model: `llama-3.3-70b-versatile`
- Requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Raw responses: `results/api_audit/groq_llama33_70b_smoke10_v5_raw.jsonl`
- Imported results: `results/analysis/groq_llama33_70b_smoke10_v5_imported.jsonl`

## Validation

- Expected requests: 30
- Imported responses: 30
- Parsed-empty responses: 0
- Correct responses: 15
- Reported input tokens: 4100
- Reported output tokens: 86

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
