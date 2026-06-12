# Research Log Compactness Check

Updated: 2026-06-11

This check keeps `research_log.md` as a compact restart ledger while
guarding against accidental removal of thesis-critical results.

- Log: `research_log.md`
- Machine-readable checks: `results/analysis/research_log_compactness_check.csv`

## Summary

- Checks: 72
- Issues: 0

No research-log compactness issues found.

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| `exists` | `ok` | research_log.md |
| `line_count` | `ok` | lines=299 max=300 |
| `byte_count` | `ok` | bytes=17459 max=20000 |
| `heading:Fast Restart` | `ok` | present |
| `heading:Thesis Claim` | `ok` | present |
| `heading:Frozen Dataset` | `ok` | present |
| `heading:Main Results` | `ok` | present |
| `heading:Supporting Evidence` | `ok` | present |
| `heading:Model Breadth` | `ok` | present |
| `heading:Compute And QA` | `ok` | present |
| `heading:Immediate Queue` | `ok` | present |
| `reference:reports/current_research_status_dashboard.md` | `ok` | present |
| `reference:reports/next_experiment_decision_queue.md` | `ok` | present |
| `reference:results/tables/main_script_gap_validation200_v5.csv` | `ok` | present |
| `reference:reports/v5_recoverability_source_decomposition.md` | `ok` | present |
| `reference:reports/v5_dataset_gap_intervals.md` | `ok` | present |
| `reference:reports/v5_paired_sign_tests.md` | `ok` | present |
| `reference:reports/v5_clustered_gap_robustness.md` | `ok` | present |
| `reference:reports/v5_benqa_subject_stability.md` | `ok` | present |
| `reference:reports/v5_benqa_subject_balance.md` | `ok` | present |
| `reference:reports/cross_script_diagnostics_validation200_v5.md` | `ok` | present |
| `reference:reports/v5_cross_script_transfer.md` | `ok` | present |
| `reference:reports/v5_review_label_sensitivity.md` | `ok` | present |
| `reference:reports/v5_banglish_fragility_feature_analysis.md` | `ok` | present |
| `reference:reports/v5_qwen_scaling_transfer.md` | `ok` | present |
| `reference:reports/v5_item_consensus.md` | `ok` | present |
| `reference:reports/v5_difficulty_conditioned_gap.md` | `ok` | present |
| `reference:reports/v5_consensus_stability.md` | `ok` | present |
| `reference:reports/v5_composition_sensitivity.md` | `ok` | present |
| `reference:reports/v5_answer_format_audit.md` | `ok` | present |
| `reference:reports/v5_response_style_drift.md` | `ok` | present |
| `reference:reports/v5_banglamath_numeric_sensitivity.md` | `ok` | present |
| `reference:reports/v5_banglamath_numeric_transfer.md` | `ok` | present |
| `reference:reports/v5_benqa_choice_bias.md` | `ok` | present |
| `reference:reports/v5_benqa_subject_option_bias.md` | `ok` | present |
| `reference:reports/v5_benqa_prediction_diversity.md` | `ok` | present |
| `reference:reports/v5_benqa_option_position_content.md` | `ok` | present |
| `reference:reports/v5_benqa_option_switching.md` | `ok` | present |
| `reference:reports/v5_benqa_cross_script_option_agreement.md` | `ok` | present |
| `reference:reports/v5_benqa_cross_model_banglish_agreement.md` | `ok` | present |
| `reference:reports/v5_benqa_order_confound.md` | `ok` | present |
| `reference:reports/v5_benqa_review_label_option_bias.md` | `ok` | present |
| `reference:reports/v5_benqa_length_token_confound.md` | `ok` | present |
| `reference:reports/v5_benqa_option_coverage_confound.md` | `ok` | present |
| `reference:reports/v5_benqa_option_switch_confound.md` | `ok` | present |
| `reference:reports/v5_benqa_option_semantic_cues.md` | `ok` | present |
| `reference:reports/v5_benqa_multiconfound_residual.md` | `ok` | present |
| `reference:reports/v5_benqa_distractor_transition.md` | `ok` | present |
| `reference:reports/v5_benqa_label_balance.md` | `ok` | present |
| `reference:reports/v5_benqa_option_permutation_probe_results.md` | `ok` | present |
| `reference:reports/bnsentmix_external_validation_results.md` | `ok` | present |
| `reference:reports/bnsentmix_model_complementarity.md` | `ok` | present |
| `reference:reports/bnsentmix_routing_devtest.md` | `ok` | present |
| `reference:reports/generated_view_diagnostics_summary.md` | `ok` | present |
| `reference:reports/real_banglish_distribution_comparison.md` | `ok` | present |
| `reference:reports/v5_banglatlit_lexical_coverage.md` | `ok` | present |
| `reference:reports/v5_benqa_option_lexical_coverage.md` | `ok` | present |
| `reference:reports/v5_banglatlit_model_coverage_sensitivity.md` | `ok` | present |
| `reference:reports/v5_banglatlit_spelling_variation_sensitivity.md` | `ok` | present |
| `reference:reports/v5_source_variant_structural_parity.md` | `ok` | present |
| `reference:reports/v5_english_warning_sensitivity.md` | `ok` | present |
| `reference:reports/v5_review_edit_distance_sensitivity.md` | `ok` | present |
| `reference:reports/final_api_audit_cost_plan.md` | `ok` | present |
| `pattern:main_qwen25_3b` | `ok` | present |
| `pattern:main_qwen25_7b` | `ok` | present |
| `pattern:main_qwen3_4b` | `ok` | present |
| `pattern:fragility_events` | `ok` | present |
| `pattern:api_manifest_check` | `ok` | present |
| `pattern:api_import_roundtrip` | `ok` | present |
| `pattern:bnsentmix_external` | `ok` | present |
| `pattern:bnsentmix_complementarity` | `ok` | present |
| `pattern:bnsentmix_routing` | `ok` | present |
