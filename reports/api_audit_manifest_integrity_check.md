# API Audit Manifest Integrity Check

Updated: 2026-06-11

This no-spend check validates the provider-neutral API smoke request
manifest before any paid call is made.

Machine-readable checks: `results/analysis/api_audit_manifest_integrity_check.csv`.

## Summary

- Checks: 18
- Issues: 0

No API audit manifest integrity issues found.

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| `exists:data/slices/api_audit_smoke_10_v5.jsonl` | `ok` | present |
| `exists:data/api_audit/api_audit_smoke_10_v5_requests.jsonl` | `ok` | present |
| `exists:results/analysis/api_audit_smoke_10_v5_prompt_budget_summary.csv` | `ok` | present |
| `item_count` | `ok` | items=10 expected=10 |
| `request_count` | `ok` | requests=30 expected=30 |
| `request_id_unique` | `ok` | duplicates=0 |
| `request_id_format` | `ok` | all id::variant::prompt_mode |
| `request_item_ids` | `ok` | all in input slice |
| `variants_per_item` | `ok` | all items have bangla,banglish_clean,english |
| `variant_counts` | `ok` | bangla=10,banglish_clean=10,english=10 |
| `required_fields` | `ok` | all present |
| `gold_excluded` | `ok` | no answer/gold/source fields in request rows |
| `prompt_contract` | `ok` | all prompts include evaluation prefix and answer instruction |
| `max_output_tokens` | `ok` | 0 < max_output_tokens <= 128 |
| `prompt_chars_total` | `ok` | chars=6904 |
| `approx_prompt_tokens_total` | `ok` | approx_tokens=1736 |
| `budget_call_count` | `ok` | budget_calls=30 requests=30 |
| `budget_token_sum` | `ok` | budget_tokens=1736 request_tokens=1736 |
