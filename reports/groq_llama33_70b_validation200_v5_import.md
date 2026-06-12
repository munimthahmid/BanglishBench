# API Audit Response Import

Updated: 2026-06-05

- Provider: `groq`
- Model: `llama-3.3-70b-versatile`
- Requests: `data/api_audit/validation200_v5_requests.jsonl`
- Raw responses: `results/api_audit/groq_llama33_70b_validation200_v5_raw.jsonl`
- Imported results: `results/analysis/groq_llama33_70b_validation200_v5_imported.jsonl`

## Validation

- Expected requests: 600
- Imported responses: 600
- Parsed-empty responses: 1
- Correct responses: 240
- Reported input tokens: 88321
- Reported output tokens: 7361

Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`
fields as the open-model evaluation outputs.
