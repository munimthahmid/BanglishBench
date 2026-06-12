# Reproducibility And Release Checklist

Updated: 2026-06-05

## Purpose

This checklist defines what must be true before the project is treated as a
thesis-grade artifact rather than an exploratory research workspace.

## Current Status

| Area | Status | Evidence |
| --- | --- | --- |
| Validation-200 open-model results | Ready for thesis draft | `reports/thesis_results_dashboard.md` |
| v5 human-reviewed Banglish | Complete: 140/140 reviewed and frozen | `data/slices/validation_200_v5.jsonl` |
| Reproducibility manifest | Generated | `reports/reproducibility_artifact_manifest.md` |
| Local artifact reference check | Clean except expected future refs | `reports/local_artifact_reference_check.md` |
| Secret hygiene check | Clean | `reports/secret_hygiene_check.md` |
| Research log compactness | Clean | `reports/research_log_compactness_check.md` |
| Citation readiness check | Clean | `reports/citation_readiness_check.md` |
| Dataset card draft | Drafted | `reports/dataset_card_validation200.md` |
| Threats to validity | Drafted | `reports/threats_to_validity.md` |
| v5 analysis preregistration | Locked before v5 outputs | `reports/v5_analysis_preregistration.md` |
| Post-v5 rerun protocol | Locked | `reports/post_v5_rerun_protocol.md` |
| Frozen-v5 main Qwen table | Generated | `results/tables/main_script_gap_validation200_v5.csv`, `reports/main_results_validation200_v5.md` |
| Frozen-v5 review-label sensitivity | Generated | `reports/v5_review_label_sensitivity.md`, `results/analysis/v5_review_label_sensitivity_summary.csv` |
| Frozen-v5 dataset-level paired intervals | Generated | `reports/v5_dataset_gap_intervals.md`, `results/analysis/v5_dataset_gap_intervals.csv` |
| Frozen-v5 paired sign tests | Generated | `reports/v5_paired_sign_tests.md`, `results/analysis/v5_paired_sign_tests.csv` |
| Frozen-v5 clustered gap robustness | Generated | `reports/v5_clustered_gap_robustness.md`, `results/analysis/v5_clustered_gap_summary.csv` |
| Frozen-v5 BEnQA subject stability | Generated | `reports/v5_benqa_subject_stability.md`, `results/analysis/v5_benqa_subject_stability.csv` |
| Frozen-v5 BEnQA subject-macro balance | Generated | `reports/v5_benqa_subject_balance.md`, `results/analysis/v5_benqa_subject_balance_summary.csv` |
| Frozen-v5 Qwen scaling-transfer audit | Generated | `reports/v5_qwen_scaling_transfer.md`, `results/analysis/v5_qwen_scaling_transfer_summary.csv` |
| Frozen-v5 answer-format audit | Generated | `reports/v5_answer_format_audit.md`, `results/analysis/v5_answer_format_audit_summary.csv` |
| Frozen-v5 response-style drift audit | Generated | `reports/v5_response_style_drift.md`, `results/analysis/v5_response_style_drift_summary.csv` |
| Frozen-v5 BanglaMATH numeric sensitivity | Generated | `reports/v5_banglamath_numeric_sensitivity.md`, `results/analysis/v5_banglamath_numeric_sensitivity_summary.csv` |
| Frozen-v5 BanglaMATH numeric transfer | Generated | `reports/v5_banglamath_numeric_transfer.md`, `results/analysis/v5_banglamath_numeric_transfer_summary.csv` |
| Frozen-v5 BEnQA choice-bias audit | Generated | `reports/v5_benqa_choice_bias.md`, `results/analysis/v5_benqa_choice_bias_summary.csv` |
| Frozen-v5 BEnQA subject option-bias audit | Generated | `reports/v5_benqa_subject_option_bias.md`, `results/analysis/v5_benqa_subject_option_bias_summary.csv` |
| Frozen-v5 BEnQA prediction-diversity audit | Generated | `reports/v5_benqa_prediction_diversity.md`, `results/analysis/v5_benqa_prediction_diversity_summary.csv` |
| Frozen-v5 BEnQA option position/content audit | Generated | `reports/v5_benqa_option_position_content.md`, `results/analysis/v5_benqa_option_position_content_summary.csv` |
| Frozen-v5 BEnQA option-switching audit | Generated | `reports/v5_benqa_option_switching.md`, `results/analysis/v5_benqa_option_switching_summary.csv` |
| Frozen-v5 BEnQA cross-script option-agreement audit | Generated | `reports/v5_benqa_cross_script_option_agreement.md`, `results/analysis/v5_benqa_cross_script_option_agreement_summary.csv` |
| Frozen-v5 BEnQA cross-model Banglish-agreement audit | Generated | `reports/v5_benqa_cross_model_banglish_agreement.md`, `results/analysis/v5_benqa_cross_model_banglish_agreement_summary.csv` |
| Frozen-v5 BEnQA order-confound audit | Generated | `reports/v5_benqa_order_confound.md`, `results/analysis/v5_benqa_order_confound_summary.csv` |
| Frozen-v5 BEnQA review-label option-bias audit | Generated | `reports/v5_benqa_review_label_option_bias.md`, `results/analysis/v5_benqa_review_label_option_bias_summary.csv` |
| Frozen-v5 BEnQA length/token confound audit | Generated | `reports/v5_benqa_length_token_confound.md`, `results/analysis/v5_benqa_length_token_confound_summary.csv` |
| Frozen-v5 BEnQA option-coverage confound audit | Generated | `reports/v5_benqa_option_coverage_confound.md`, `results/analysis/v5_benqa_option_coverage_confound_summary.csv` |
| Frozen-v5 BEnQA option-switch confound audit | Generated | `reports/v5_benqa_option_switch_confound.md`, `results/analysis/v5_benqa_option_switch_confound_summary.csv` |
| Frozen-v5 BEnQA option semantic-cue audit | Generated | `reports/v5_benqa_option_semantic_cues.md`, `results/analysis/v5_benqa_option_semantic_cues_summary.csv` |
| Frozen-v5 BEnQA multi-confound residual audit | Generated | `reports/v5_benqa_multiconfound_residual.md`, `results/analysis/v5_benqa_multiconfound_residual_summary.csv` |
| Frozen-v5 BEnQA distractor-transition audit | Generated | `reports/v5_benqa_distractor_transition.md`, `results/analysis/v5_benqa_distractor_transition_summary.csv` |
| Frozen-v5 BEnQA label-balance sensitivity | Generated | `reports/v5_benqa_label_balance.md`, `results/analysis/v5_benqa_label_balance_summary.csv` |
| Frozen-v5 real-Banglish distribution comparison | Generated | `reports/real_banglish_distribution_comparison.md`, `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv` |
| Frozen-v5 BanglaTLit lexical coverage audit | Generated | `reports/v5_banglatlit_lexical_coverage.md`, `results/analysis/v5_banglatlit_lexical_coverage_summary.csv` |
| Frozen-v5 BEnQA option lexical coverage audit | Generated | `reports/v5_benqa_option_lexical_coverage.md`, `results/analysis/v5_benqa_option_lexical_coverage_summary.csv` |
| Frozen-v5 BanglaTLit model-coverage sensitivity audit | Generated | `reports/v5_banglatlit_model_coverage_sensitivity.md`, `results/analysis/v5_banglatlit_model_coverage_sensitivity_summary.csv` |
| Frozen-v5 BanglaTLit spelling-variation sensitivity audit | Generated | `reports/v5_banglatlit_spelling_variation_sensitivity.md`, `results/analysis/v5_banglatlit_spelling_variation_sensitivity_summary.csv` |
| Frozen-v5 source-variant structural parity audit | Generated | `reports/v5_source_variant_structural_parity.md`, `results/analysis/v5_source_variant_structural_parity_summary.csv` |
| Frozen-v5 English-warning sensitivity audit | Generated | `reports/v5_english_warning_sensitivity.md`, `results/analysis/v5_english_warning_sensitivity_summary.csv` |
| Frozen-v5 review edit-distance sensitivity audit | Generated | `reports/v5_review_edit_distance_sensitivity.md`, `results/analysis/v5_review_edit_distance_sensitivity_summary.csv` |
| Frozen-v5 cross-script diagnostics | Generated | `reports/cross_script_diagnostics_validation200_v5.md` |
| Frozen-v5 recoverability source decomposition | Generated | `reports/v5_recoverability_source_decomposition.md`, `results/analysis/v5_recoverability_source_summary.csv` |
| Frozen-v5 cross-script transfer retention | Generated | `reports/v5_cross_script_transfer.md`, `results/analysis/v5_cross_script_transfer_summary.csv` |
| Frozen-v5 tokenization/failure mechanism check | Generated | `reports/tokenization_cross_script_failure_patterns.md`, `results/analysis/validation200_v5_cross_script_token_patterns_summary.csv` |
| Frozen-v5 fragility feature analysis | Generated | `reports/v5_banglish_fragility_feature_analysis.md`, `results/analysis/v5_banglish_fragility_items.csv` |
| Frozen-v5 fragility model-overlap analysis | Generated | `reports/v5_banglish_fragility_model_overlap.md`, `results/analysis/v5_banglish_fragility_model_overlap_summary.csv` |
| Frozen-v5 item-consensus audit | Generated | `reports/v5_item_consensus.md`, `results/analysis/v5_item_consensus_summary.csv` |
| Frozen-v5 difficulty-conditioned gap audit | Generated | `reports/v5_difficulty_conditioned_gap.md`, `results/analysis/v5_difficulty_conditioned_gap_summary.csv` |
| Frozen-v5 consensus stability audit | Generated | `reports/v5_consensus_stability.md`, `results/analysis/v5_consensus_stability_summary.csv` |
| Frozen-v5 composition sensitivity audit | Generated | `reports/v5_composition_sensitivity.md`, `results/analysis/v5_composition_sensitivity_summary.csv` |
| Frozen-v5 shared-fragility examples | Generated | `reports/v5_shared_fragility_examples.md`, `results/analysis/v5_shared_fragility_examples.csv` |
| Paper manuscript draft | Generated | `reports/script_matters_paper_draft.md` |
| BEnQA 1000-row extension | Generated, AI-assisted reviewed, human-review freeze complete with 974 gold/pass rows; six-model 974-row scale panel complete | `reports/benqa_extension_publication_strategy.md`, `reports/benqa_extended_1000_v1.md`, `reports/benqa_extended_1000_v1_ai_review.md`, `reports/benqa_extended_1000_v1_human_review_freeze.md`, `reports/benqa_human_gold_974_scale_summary.md`, `reports/qwen25_3b_benqa_human_gold_974.md`, `reports/groq_llama33_70b_benqa_human_gold_974.md`, `reports/gemini_3_5_flash_benqa_human_gold_974.md`, `reports/openai_gpt55_none_benqa_human_gold_974.md`, `reports/claude_sonnet_4_6_benqa_human_gold_974.md`, `reports/deepseek_v4_flash_benqa_human_gold_974.md`, `results/analysis/benqa_human_gold_974_scale_summary.csv`, `data/slices/benqa_extended_1000_v1_human_gold.jsonl` |
| Paid API audit | Gemini 3.5 Flash, GPT-5.5 low, Claude Sonnet 4.6, DeepSeek V4 Flash, and Groq Llama 3.3 70B validation-200 v5 audits complete; Gemini/GPT-5.5 none/Claude 974-row human-gold BEnQA audits complete | `reports/frontier_api_panel_validation200_v5.md`, `results/analysis/frontier_api_panel_validation200_v5.csv`, `reports/gemini_3_5_flash_validation200_v5_results.md`, `reports/openai_gpt55_low_validation200_v5_cap1024_results.md`, `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md`, `reports/deepseek_v4_flash_validation200_v5_results.md`, `reports/groq_llama33_70b_validation200_v5_results.md`, `reports/gemini_3_5_flash_benqa_human_gold_974.md`, `reports/openai_gpt55_none_benqa_human_gold_974.md`, `reports/claude_sonnet_4_6_benqa_human_gold_974.md`, `reports/api_audit_manifest_integrity_check.md`, `reports/api_audit_import_roundtrip_check.md`, `reports/paid_api_audit_execution_runbook.md`, `reports/validation200_v5_api_audit_prompt_manifest.md`, `reports/benqa_human_gold_974_prompt_manifest.md`, `data/api_audit/validation200_v5_requests.jsonl`, `data/api_audit/benqa_human_gold_974_requests.jsonl`, `scripts/run_anthropic_api_audit.py`, `scripts/run_openai_api_audit.py`, `scripts/run_gemini_api_audit.py` |

## Before Freezing v5

Completed on 2026-05-29. The commands below are retained as the audit trail.

Run:

```bash
python3 scripts/validate_banglish_review_queue.py
```

Final result:

- `errors=0`
- `warnings=0`
- `pending=0`

Then complete review:

```bash
python3 scripts/review_validation200_v5_queue.py --session 1
```

Preview a batch without writing:

```bash
python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run
python3 scripts/review_validation200_v5_queue.py --session 1 --list-ids
```

Track progress:

```bash
python3 scripts/plan_v5_review_sessions.py
python3 scripts/summarize_v5_review_progress.py
```

Review order:

1. `tier_1_review_first`
2. `tier_2_high`
3. `tier_3_medium`
4. `tier_4_low`

Use these artifacts while reviewing:

- `reports/validation200_v5_review_packets_impact_order/README.md`
- `reports/validation200_v5_review_calibration_set.md`
- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_impact_substitutions.md`
- `reports/validation200_v5_substitution_review_playbook.md`
- `reports/validation200_v5_review_metadata_summary.md`
- `reports/validation200_v5_review_progress.md`
- `reports/validation200_v5_review_session_plan.md`
- `reports/validation200_v5_review_resume_card.md`
- `reports/validation200_v5_review_session_log.md`
- `results/analysis/validation200_v5_review_progress_summary.csv`
- `results/analysis/validation200_v5_review_session_plan.csv`
- `results/analysis/validation200_v5_review_resume_card.csv`
- `results/analysis/validation200_v5_review_session_01_preview.csv`
- `data/slices/banglish_review_guidelines.md`

## Freeze Gate

Fast local check bundle:

```bash
python3 scripts/run_research_checks.py
```

The bundle also regenerates tightened generated-view audits, the combined
candidate-preservation table, and the privileged dev-only native-reference
similarity table.

Post-v5 rerun preflight:

```bash
python3 scripts/check_post_v5_rerun_readiness.py
python3 scripts/build_post_v5_kaggle_job_plan.py
```

Post-v5 Kaggle packaging plan:

- `reports/post_v5_kaggle_job_plan.md`
- `results/analysis/post_v5_kaggle_job_plan.csv`
- `reports/post_v5_compute_budget.md`
- `results/analysis/post_v5_compute_budget.csv`

Do not freeze v5 until this command passes:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```

Then freeze with the default all-rows policy:

```bash
python3 scripts/apply_banglish_review.py \
  --input data/slices/validation_200_v4.jsonl \
  --review data/slices/validation_200_v5_review_queue.csv \
  --output data/slices/validation_200_v5.jsonl \
  --audit-output results/analysis/validation200_v5_banglish_review_audit.csv \
  --quality-status human_reviewed_banglish_v5
```

Only use `--drop-bad` if the thesis explicitly switches to a strict-subset
policy. Do not mix all-200 and strict-subset tables silently.

Before launching post-v5 model jobs, confirm that
`reports/v5_analysis_preregistration.md` still reflects the intended primary
models, comparisons, denominator policy, and statistics.

## Post-Freeze Validation

Run:

```bash
python3 scripts/audit_banglish_artifacts.py \
  data/slices/validation_200_v5.jsonl \
  --summary-output results/analysis/validation200_v5_banglish_artifact_summary.csv \
  --examples-output results/analysis/validation200_v5_banglish_artifact_examples.csv

python3 scripts/build_artifact_manifest.py
python3 scripts/check_local_artifact_refs.py
python3 scripts/check_citation_readiness.py
python3 scripts/check_v5_review_packet_integrity.py
python3 scripts/build_v5_next_session_brief.py
python3 scripts/build_v5_cross_script_diagnostics.py
python3 scripts/analyze_v5_recoverability_sources.py
python3 scripts/export_cross_script_agreement_examples.py
python3 scripts/analyze_v5_banglish_fragility_features.py
python3 scripts/analyze_v5_fragility_model_overlap.py
python3 scripts/analyze_v5_item_consensus.py
python3 scripts/analyze_v5_difficulty_conditioned_gap.py
python3 scripts/analyze_v5_consensus_stability.py
python3 scripts/analyze_v5_composition_sensitivity.py
python3 scripts/export_v5_shared_fragility_examples.py
python3 scripts/analyze_v5_cross_script_transfer.py
python3 scripts/analyze_v5_dataset_gap_intervals.py
python3 scripts/analyze_v5_paired_sign_tests.py
python3 scripts/analyze_v5_clustered_gap_robustness.py
python3 scripts/analyze_v5_benqa_subject_stability.py
python3 scripts/analyze_v5_benqa_subject_balance.py
python3 scripts/analyze_v5_qwen_scaling_transfer.py
python3 scripts/analyze_v5_answer_format_audit.py
python3 scripts/analyze_v5_response_style_drift.py
python3 scripts/analyze_v5_banglamath_numeric_sensitivity.py
python3 scripts/analyze_v5_banglamath_numeric_transfer.py
python3 scripts/analyze_v5_benqa_choice_bias.py
python3 scripts/analyze_v5_benqa_subject_option_bias.py
python3 scripts/analyze_v5_benqa_option_position_content.py
python3 scripts/analyze_v5_benqa_length_token_confound.py
python3 scripts/analyze_v5_benqa_option_coverage_confound.py
python3 scripts/analyze_v5_benqa_multiconfound_residual.py
python3 scripts/analyze_v5_benqa_distractor_transition.py
python3 scripts/analyze_v5_benqa_label_balance.py
python3 scripts/compare_banglish_distributions.py \
  --validation data/slices/validation_200_v5.jsonl \
  --validation-variant banglish_clean \
  --banglatlit literature/code/BanglaTLit/data/BanglaTLiT_val.csv literature/code/BanglaTLit/data/BanglaTLiT_test.csv \
  --items-output results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_items.csv \
  --summary-output results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv \
  --top-words-output results/analysis/banglatlit_vs_validation200_v5_banglish_top_words.csv
python3 scripts/analyze_v5_banglatlit_lexical_coverage.py
python3 scripts/analyze_v5_benqa_option_lexical_coverage.py
python3 scripts/analyze_v5_banglatlit_model_coverage_sensitivity.py
python3 scripts/analyze_v5_banglatlit_spelling_variation_sensitivity.py
python3 scripts/analyze_v5_source_variant_structural_parity.py
python3 scripts/analyze_v5_english_warning_sensitivity.py
python3 scripts/analyze_v5_review_edit_distance_sensitivity.py
python3 scripts/check_secret_hygiene.py
python3 scripts/check_research_log_compactness.py
python3 scripts/compile_thesis_draft.py
python3 scripts/build_current_research_status_dashboard.py
python3 scripts/check_thesis_tables.py
python3 scripts/check_thesis_figures.py
python3 scripts/check_api_audit_manifest.py
python3 scripts/check_api_audit_import_roundtrip.py
```

Required outputs:

- `data/slices/validation_200_v5.jsonl`
- `results/analysis/validation200_v5_banglish_review_audit.csv`
- `results/analysis/validation200_v5_banglish_artifact_summary.csv`
- `results/analysis/validation200_v5_banglish_artifact_examples.csv`
- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/v5_review_label_sensitivity.md`
- `reports/v5_dataset_gap_intervals.md`
- `results/analysis/v5_dataset_gap_intervals.csv`
- `reports/v5_benqa_subject_stability.md`
- `results/analysis/v5_benqa_subject_stability.csv`
- `reports/v5_benqa_subject_balance.md`
- `results/analysis/v5_benqa_subject_balance_summary.csv`
- `results/analysis/v5_benqa_subject_balance_subjects.csv`
- `reports/v5_answer_format_audit.md`
- `results/analysis/v5_answer_format_audit_summary.csv`
- `results/analysis/v5_answer_format_audit_items.csv`
- `reports/v5_response_style_drift.md`
- `results/analysis/v5_response_style_drift_summary.csv`
- `results/analysis/v5_response_style_drift_items.csv`
- `reports/v5_banglamath_numeric_sensitivity.md`
- `results/analysis/v5_banglamath_numeric_sensitivity_summary.csv`
- `results/analysis/v5_banglamath_numeric_sensitivity_items.csv`
- `reports/v5_banglamath_numeric_transfer.md`
- `results/analysis/v5_banglamath_numeric_transfer_summary.csv`
- `results/analysis/v5_banglamath_numeric_transfer_items.csv`
- `reports/v5_benqa_choice_bias.md`
- `results/analysis/v5_benqa_choice_bias_summary.csv`
- `results/analysis/v5_benqa_choice_bias_items.csv`
- `reports/v5_benqa_subject_option_bias.md`
- `results/analysis/v5_benqa_subject_option_bias_summary.csv`
- `results/analysis/v5_benqa_subject_option_bias_items.csv`
- `reports/v5_benqa_option_position_content.md`
- `results/analysis/v5_benqa_option_position_content_summary.csv`
- `results/analysis/v5_benqa_option_position_content_items.csv`
- `reports/v5_benqa_length_token_confound.md`
- `results/analysis/v5_benqa_length_token_confound_summary.csv`
- `results/analysis/v5_benqa_length_token_confound_items.csv`
- `reports/v5_benqa_option_coverage_confound.md`
- `results/analysis/v5_benqa_option_coverage_confound_summary.csv`
- `results/analysis/v5_benqa_option_coverage_confound_items.csv`
- `reports/v5_benqa_multiconfound_residual.md`
- `results/analysis/v5_benqa_multiconfound_residual_summary.csv`
- `results/analysis/v5_benqa_multiconfound_residual_items.csv`
- `reports/v5_benqa_label_balance.md`
- `results/analysis/v5_benqa_label_balance_summary.csv`
- `results/analysis/v5_benqa_label_balance_by_label.csv`
- `reports/v5_paired_sign_tests.md`
- `results/analysis/v5_paired_sign_tests.csv`
- `reports/v5_clustered_gap_robustness.md`
- `results/analysis/v5_clustered_gap_summary.csv`
- `results/analysis/v5_clustered_gap_clusters.csv`
- `reports/v5_banglish_fragility_feature_analysis.md`
- `reports/v5_recoverability_source_decomposition.md`
- `results/analysis/v5_recoverability_source_summary.csv`
- `results/analysis/v5_recoverability_source_items.csv`
- `reports/v5_cross_script_transfer.md`
- `results/analysis/v5_cross_script_transfer_summary.csv`
- `results/analysis/v5_cross_script_transfer_items.csv`
- `results/analysis/v5_banglish_fragility_items.csv`
- `results/analysis/v5_banglish_fragility_feature_summary.csv`
- `reports/v5_banglish_fragility_model_overlap.md`
- `results/analysis/v5_banglish_fragility_model_overlap_summary.csv`
- `reports/v5_item_consensus.md`
- `results/analysis/v5_item_consensus_summary.csv`
- `results/analysis/v5_item_consensus_items.csv`
- `reports/v5_difficulty_conditioned_gap.md`
- `results/analysis/v5_difficulty_conditioned_gap_summary.csv`
- `results/analysis/v5_difficulty_conditioned_gap_items.csv`
- `reports/v5_consensus_stability.md`
- `results/analysis/v5_consensus_stability_summary.csv`
- `results/analysis/v5_consensus_stability_items.csv`
- `reports/v5_composition_sensitivity.md`
- `results/analysis/v5_composition_sensitivity_summary.csv`
- `results/analysis/v5_composition_sensitivity_items.csv`
- `reports/real_banglish_distribution_comparison.md`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_items.csv`
- `reports/v5_banglatlit_lexical_coverage.md`
- `results/analysis/v5_banglatlit_lexical_coverage_summary.csv`
- `results/analysis/v5_banglatlit_lexical_coverage_items.csv`
- `reports/v5_benqa_option_lexical_coverage.md`
- `results/analysis/v5_benqa_option_lexical_coverage_summary.csv`
- `results/analysis/v5_benqa_option_lexical_coverage_items.csv`
- `reports/v5_banglatlit_model_coverage_sensitivity.md`
- `results/analysis/v5_banglatlit_model_coverage_sensitivity_summary.csv`
- `results/analysis/v5_banglatlit_model_coverage_sensitivity_items.csv`
- `reports/v5_source_variant_structural_parity.md`
- `results/analysis/v5_source_variant_structural_parity_summary.csv`
- `results/analysis/v5_source_variant_structural_parity_items.csv`
- `reports/v5_english_warning_sensitivity.md`
- `results/analysis/v5_english_warning_sensitivity_summary.csv`
- `results/analysis/v5_english_warning_sensitivity_items.csv`
- `reports/v5_review_edit_distance_sensitivity.md`
- `results/analysis/v5_review_edit_distance_sensitivity_summary.csv`
- `results/analysis/v5_review_edit_distance_sensitivity_items.csv`
- `results/analysis/validation200_v5_cross_script_diagnostics_summary.csv`
- `reports/reproducibility_artifact_manifest.md`
- `results/analysis/reproducibility_artifact_manifest.csv`
- `reports/local_artifact_reference_check.md`
- `reports/secret_hygiene_check.md`
- `reports/research_log_compactness_check.md`
- `reports/api_audit_manifest_integrity_check.md`
- `reports/api_audit_import_roundtrip_check.md`
- `reports/v5_shared_fragility_examples.md`
- `results/analysis/v5_shared_fragility_examples.csv`
- `results/analysis/secret_hygiene_check.csv`

## Minimal Reruns

Follow `reports/post_v5_rerun_protocol.md`.

Run first:

1. Qwen2.5-3B `banglish_clean` on validation-200 v5 full200.
2. Qwen3-4B `banglish_clean` on validation-200 v5 full200.

The optional Qwen2.5-7B 8-bit pinned retry also completed:

- v4 Banglish: 48/200
- v5 reviewed Banglish: 47/200
- Delta: -0.5 points, CI [-3.5, +2.5]

The earlier latest-stack failure is retained in
`reports/qwen25_7b_8bit_validation200_v5_failure.md`.

Flagged-bad denominator sensitivity:

- Main policy: keep all 200 frozen rows and flag 3 bad rows.
- Secondary strict policy: exclude the 3 flagged rows and report 197 rows.
- Report: `reports/v5_bad_row_policy_sensitivity.md`.

Release-facing main table:

- Use `results/tables/main_script_gap_validation200_v5.csv`.
- Keep `results/tables/main_script_gap_validation200.csv` as the historical
  provenance table for earlier analyses.

Do not rerun Bangla/English unless non-Banglish fields changed.

## Table Regeneration

After post-v5 reruns:

```bash
python3 scripts/analyze_banglish_variant_sensitivity.py \
  --baseline-results path/to/v4_banglish.jsonl \
  --candidate-results path/to/v5_banglish.jsonl \
  --model Qwen/Qwen2.5-3B-Instruct \
  --model-label Qwen2.5-3B \
  --baseline-name v4 \
  --candidate-name v5 \
  --output-prefix results/analysis/qwen25_validation200_v5_vs_v4_banglish

python3 scripts/build_v5_cross_script_diagnostics.py
python3 scripts/export_cross_script_agreement_examples.py
python3 scripts/build_thesis_tables.py
python3 scripts/build_artifact_manifest.py
```

Then update:

- `reports/thesis_results_dashboard.md`
- `reports/evidence_matrix.md`
- `reports/current_research_state.md`
- `reports/thesis_abstract_and_contributions_draft.md`
- `reports/thesis_writeup_blueprint.md`
- `research_log.md`
- `results/experiment_log.md`

## External API Audit Gate

Only after v5 and open-model tables are stable:

1. Build a v5 API smoke subset. Complete:
   `data/slices/api_audit_smoke_10_v5.jsonl`.
2. Run 10-item triad smoke for each paid provider.
3. Inspect actual token usage and parser behavior.
4. Run full validation-200 v5 triad only if costs fit the cap.

Guardrails:

- Hard cap: $20 unless explicitly changed.
- Do not enable web, tools, search, or grounding.
- Log provider, model id, date, token usage, and cost.
- Export provider-neutral requests with
  `python3 scripts/build_api_audit_prompt_manifest.py`.
- Before paid calls, run `python3 scripts/check_api_audit_manifest.py` and
  `python3 scripts/check_api_audit_import_roundtrip.py`; both must have zero
  issues.
- Import raw responses through `scripts/import_api_audit_responses.py` so paid
  and open-model outputs use the same parser-facing schema.
- Follow `reports/paid_api_audit_execution_runbook.md`.

## Secret Hygiene

Never include these in reports, manifests, archives, or screenshots:

- `kaggle.json`
- `kaggle (1).json`
- `kaggle_api*.txt`
- `sadia.pem`
- `.env`
- shell history containing tokens

The artifact manifest builder excludes these by default.

Run the non-secret artifact scan before any archive/export:

```bash
python3 scripts/check_secret_hygiene.py
```

Current expected result:

- `suspicious=0`

It also excludes its own generated Markdown/CSV outputs so the manifest does
not record stale self-hashes.

## Release Definition

The project is release-ready when:

1. v5 review is complete and validated.
2. v5 freeze artifacts exist.
3. Qwen2.5-3B and Qwen3-4B v5 Banglish reruns are analyzed.
4. Thesis tables and dashboard are regenerated.
5. Dataset card, limitations, artifact manifest, and secret hygiene report are
   updated.
6. Paid API audit is either completed or explicitly deferred with budget reason.
7. `research_log.md` and `results/experiment_log.md` contain the final state.
