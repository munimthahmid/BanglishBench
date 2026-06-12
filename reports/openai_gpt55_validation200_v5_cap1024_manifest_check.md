# API Audit Manifest Integrity Check

Updated: 2026-06-04

This no-spend check validates the provider-neutral API smoke request
manifest before any paid call is made.

Machine-readable checks: `results/analysis/openai_gpt55_validation200_v5_cap1024_manifest_check.csv`.

## Summary

- Checks: 18
- Issues: 0

No API audit manifest integrity issues found.

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| `exists:data/slices/validation_200_v5.jsonl` | `ok` | present |
| `exists:data/api_audit/openai_gpt55_validation200_v5_cap1024_requests.jsonl` | `ok` | present |
| `exists:results/analysis/openai_gpt55_validation200_v5_cap1024_prompt_budget_summary.csv` | `ok` | present |
| `item_count` | `ok` | items=200 expected=200 |
| `request_count` | `ok` | requests=600 expected=600 |
| `request_id_unique` | `ok` | duplicates=0 |
| `request_id_format` | `ok` | all id::variant::prompt_mode |
| `request_item_ids` | `ok` | all in input slice |
| `variants_per_item` | `ok` | all items have bangla,banglish_clean,english |
| `variant_counts` | `ok` | bangla=200,banglish_clean=200,english=200 |
| `required_fields` | `ok` | all present |
| `gold_excluded` | `ok` | no answer/gold/source fields in request rows |
| `prompt_contract` | `ok` | all prompts include evaluation prefix and answer instruction |
| `max_output_tokens` | `ok` | 0 < max_output_tokens <= 1024 |
| `prompt_chars_total` | `ok` | chars=144960 |
| `approx_prompt_tokens_total` | `ok` | approx_tokens=36471 |
| `budget_call_count` | `ok` | budget_calls=600 requests=600 |
| `budget_token_sum` | `ok` | budget_tokens=36471 request_tokens=36471 |
