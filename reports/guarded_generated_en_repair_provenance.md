# Guarded Generated-English Repair Provenance

Updated: 2026-06-11

This report separates the guarded generated-English answer effects by
repair strategy. The guarded view is preservation-safe, but not all rows
are actual translated-English stems.

## Artifacts

- Item CSV: `results/analysis/guarded_generated_en_repair_provenance_items.csv`
- Summary CSV: `results/analysis/guarded_generated_en_repair_provenance_summary.csv`

## Summary

| repair_strategy | n | raw_hard_fail | raw_warning | raw_digit_fail | raw_formula_fail | raw_line_count_warn | qwen3_banglish_correct | qwen3_guarded_en_correct | qwen3_delta | qwen3_gains | qwen3_losses | qwen3_agreement_routed_items | qwen3_agreement_routed_correct | qwen3_route_total_correct | qwen25_banglish_correct | qwen25_guarded_en_correct | qwen25_delta | qwen25_gains | qwen25_losses | qwen25_agreement_routed_items | qwen25_agreement_routed_correct | qwen25_route_total_correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 36 | 16 | 18 | 5 | 16 | 18 | 15 | 15 | 0 | 2 | 2 | 1 | 1 | 16 | 9 | 11 | 2 | 4 | 2 | 1 | 0 | 8 |
| source_fallback_after_failed_repair | 15 | 15 | 8 | 5 | 15 | 8 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 7 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| translated_stem_source_tail | 21 | 1 | 10 | 0 | 1 | 10 | 8 | 8 | 0 | 2 | 2 | 1 | 1 | 9 | 5 | 7 | 2 | 4 | 2 | 1 | 0 | 4 |

## Interpretation

- Overall, guarded EN is Qwen3 15/36 vs Banglish 15/36, and Qwen2.5 11/36 vs Banglish 9/36.
- Translated-stem rows: n=21, Qwen3 delta 0, Qwen2.5 delta 2.
- Source-fallback rows: n=15, Qwen3 delta 0, Qwen2.5 delta 0.
- Agreement routing fires on 1 Qwen3 item and 1 Qwen2.5 item.
- The guarded route should remain dev-only because source fallback dilutes
  the generated-English intervention and the agreement route is too sparse.
