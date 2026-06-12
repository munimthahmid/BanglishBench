# API Audit Import Round-Trip Check

Updated: 2026-06-11

This no-spend check synthesizes parser-friendly mock provider responses
for the frozen-v5 API smoke requests, runs the normal response importer
with `--require-complete`, and verifies that imported rows line up with
the open-model result schema.

- Source items: `data/slices/api_audit_smoke_10_v5.jsonl`
- Request manifest: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Machine-readable checks: `results/analysis/api_audit_import_roundtrip_check.csv`

Mock responses are written only inside a temporary directory; no fake paid
provider output JSONL is persisted.

## Summary

- Checks: 16
- Issues: 0

No API audit import round-trip issues found.

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| `exists:data/slices/api_audit_smoke_10_v5.jsonl` | `ok` | present |
| `exists:data/api_audit/api_audit_smoke_10_v5_requests.jsonl` | `ok` | present |
| `importer_cli` | `ok` | returncode=0 |
| `request_count` | `ok` | requests=30 expected=30 |
| `imported_count` | `ok` | imported=30 expected=30 |
| `imported_request_ids_unique` | `ok` | duplicates=0 |
| `request_id_coverage` | `ok` | complete |
| `required_imported_fields` | `ok` | all present |
| `parsed_non_empty` | `ok` | parsed_empty=0 |
| `gold_answer_correctness` | `ok` | correct=30/30 |
| `gold_join` | `ok` | all imported gold values match source items |
| `variant_counts` | `ok` | bangla=10,banglish_clean=10,english=10 |
| `provider_model_fields` | `ok` | all rows carry mock provider/model |
| `usage_input_tokens` | `ok` | imported=1766 expected=1766 |
| `usage_output_tokens` | `ok` | imported=102 expected=102 |
| `importer_report` | `ok` | temporary importer report written |
