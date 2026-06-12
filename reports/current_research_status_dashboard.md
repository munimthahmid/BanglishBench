# Current Research Status Dashboard

Updated: 2026-06-11

This dashboard is generated from the current local reports and CSVs. It
is intended as the fastest one-file resume point before running local checks
or deciding whether the next API step is replication or format-control testing.

Machine-readable dashboard: `results/analysis/current_research_status_dashboard.csv`.

## Stoplight

| Area | Status | Summary |
| --- | --- | --- |
| v5 manual review | `pass` | all review sessions complete |
| post-v5 reruns | `pass` | Qwen2.5-3B 39/200->41/200 (+1.0 pts, CI [-1.0, +3.0]); Qwen3-4B 47/200->49/200 (+1.0 pts, CI [0.0, +2.5]) |
| QA/literature gates | `pass` | generated checks are green if status is `pass` |

## Immediate Next Action

Required and optional post-v5 Banglish reruns are complete.
Use the frozen-v5 three-model main table in the thesis update,
then integrate the completed frontier panel and DeepSeek
full851 API replication before any broader API spend.

- Main table: `results/tables/main_script_gap_validation200_v5.csv`
- Main report: `reports/main_results_validation200_v5.md`
- v5 sensitivity table: `results/tables/v5_reviewed_banglish_sensitivity.csv`
- v5 recoverability source decomposition: `reports/v5_recoverability_source_decomposition.md`
- v5 cross-script transfer retention: `reports/v5_cross_script_transfer.md`
- v5 review-label sensitivity: `reports/v5_review_label_sensitivity.md`
- v5 dataset gap intervals: `reports/v5_dataset_gap_intervals.md`
- v5 paired sign tests: `reports/v5_paired_sign_tests.md`
- v5 clustered gap robustness: `reports/v5_clustered_gap_robustness.md`
- v5 BEnQA subject stability: `reports/v5_benqa_subject_stability.md`
- v5 BEnQA subject-macro balance: `reports/v5_benqa_subject_balance.md`
- v5 fragility feature analysis: `reports/v5_banglish_fragility_feature_analysis.md`
- v5 Qwen scaling-transfer audit: `reports/v5_qwen_scaling_transfer.md`
- v5 fragility model-overlap analysis: `reports/v5_banglish_fragility_model_overlap.md`
- v5 item consensus audit: `reports/v5_item_consensus.md`
- v5 difficulty-conditioned gap audit: `reports/v5_difficulty_conditioned_gap.md`
- v5 consensus stability audit: `reports/v5_consensus_stability.md`
- v5 composition sensitivity audit: `reports/v5_composition_sensitivity.md`
- v5 shared-fragility examples: `reports/v5_shared_fragility_examples.md`
- v5 tokenization/failure join: `reports/tokenization_cross_script_failure_patterns.md`
- v5 subject/grade breakdown: `reports/subject_breakdown_validation200_v5.md`
- v5 answer-format audit: `reports/v5_answer_format_audit.md`
- v5 response-style drift audit: `reports/v5_response_style_drift.md`
- v5 BanglaMATH numeric sensitivity: `reports/v5_banglamath_numeric_sensitivity.md`
- v5 BanglaMATH numeric transfer audit: `reports/v5_banglamath_numeric_transfer.md`
- v5 BEnQA choice-bias audit: `reports/v5_benqa_choice_bias.md`
- v5 BEnQA subject option-bias audit: `reports/v5_benqa_subject_option_bias.md`
- v5 BEnQA prediction-diversity audit: `reports/v5_benqa_prediction_diversity.md`
- v5 BEnQA option position/content audit: `reports/v5_benqa_option_position_content.md`
- v5 BEnQA option-switching audit: `reports/v5_benqa_option_switching.md`
- v5 BEnQA cross-script option-agreement audit: `reports/v5_benqa_cross_script_option_agreement.md`
- v5 BEnQA cross-model Banglish-agreement audit: `reports/v5_benqa_cross_model_banglish_agreement.md`
- v5 BEnQA order-confound audit: `reports/v5_benqa_order_confound.md`
- v5 BEnQA review-label option-bias audit: `reports/v5_benqa_review_label_option_bias.md`
- v5 BEnQA length/token confound audit: `reports/v5_benqa_length_token_confound.md`
- v5 BEnQA option-coverage confound audit: `reports/v5_benqa_option_coverage_confound.md`
- v5 BEnQA option-switch confound audit: `reports/v5_benqa_option_switch_confound.md`
- v5 BEnQA option semantic-cue audit: `reports/v5_benqa_option_semantic_cues.md`
- v5 BEnQA multi-confound residual audit: `reports/v5_benqa_multiconfound_residual.md`
- v5 BEnQA distractor-transition audit: `reports/v5_benqa_distractor_transition.md`
- v5 BEnQA label-balance sensitivity: `reports/v5_benqa_label_balance.md`
- v5 BEnQA option-permutation dev probe: `reports/v5_benqa_option_permutation_probe_results.md`
- real-Banglish v5 distribution: `reports/real_banglish_distribution_comparison.md`
- v5 BanglaTLit lexical coverage audit: `reports/v5_banglatlit_lexical_coverage.md`
- v5 BEnQA option lexical coverage audit: `reports/v5_benqa_option_lexical_coverage.md`
- v5 BanglaTLit model-coverage sensitivity: `reports/v5_banglatlit_model_coverage_sensitivity.md`
- v5 BanglaTLit spelling-variation sensitivity: `reports/v5_banglatlit_spelling_variation_sensitivity.md`
- v5 source-variant structural parity audit: `reports/v5_source_variant_structural_parity.md`
- v5 English-warning sensitivity audit: `reports/v5_english_warning_sensitivity.md`
- v5 review edit-distance sensitivity audit: `reports/v5_review_edit_distance_sensitivity.md`
- BEnQA extension strategy: `reports/benqa_extension_publication_strategy.md`
- BEnQA extension AI-assisted review: `reports/benqa_extended_1000_v1_ai_review.md`
- BEnQA extension eval subsets: `reports/benqa_extension_eval_subsets.md`
- BEnQA extension Kaggle smoke: `reports/benqa_extension_kaggle_smoke_launch.md`
- BEnQA extension full Qwen2.5-3B result: `reports/qwen25_3b_benqa_ext_full851.md`
- BEnQA extension full paired gaps: `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- BEnQA extension full DeepSeek result: `reports/deepseek_v4_flash_benqa_ext_full851.md`
- BEnQA extension full DeepSeek paired gaps: `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`
- BEnQA extension pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- 7B sensitivity report: `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish.md`
- Gemini API audit: `reports/gemini_3_5_flash_validation200_v5_results.md`
- Gemini API summary: `results/analysis/gemini_3_5_flash_validation200_v5_summary.csv`
- GPT-5.5 full API audit: `reports/openai_gpt55_low_validation200_v5_cap1024_results.md`
- GPT-5.5 full API summary: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_summary.csv`
- Frontier API panel: `reports/frontier_api_panel_validation200_v5.md`
- Claude API audit: `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md`
- DeepSeek API full851: `reports/deepseek_v4_flash_benqa_ext_full851.md`
- Controlled frontier runbook: `reports/paid_api_audit_execution_runbook.md`
- Claude sender: `scripts/run_anthropic_api_audit.py`
- DeepSeek/OpenAI-compatible sender: `scripts/run_openai_compatible_chat_api_audit.py`
- Full validation-200 API manifest: `data/api_audit/validation200_v5_requests.jsonl`
- Full validation-200 manifest report: `reports/validation200_v5_api_audit_prompt_manifest.md`
- API audit plan/runbook: `reports/final_api_audit_cost_plan.md`
- Paid audit manifest check: `reports/api_audit_manifest_integrity_check.md`
- Paid audit import round-trip check: `reports/api_audit_import_roundtrip_check.md`
- Generated-view status: protected-v3 repairs generated-BN preservation
  and guarded EN repairs hard preservation, but the route remains
  dev-only (+1 Qwen3, -1 Qwen2.5) and strict agreement
  misses most generated-view recoveries; looser rules are volatile:
  `reports/generated_view_diagnostics_summary.md`

## V5 Manual Review

| Status | Metric | Value | Detail |
| --- | --- | ---: | --- |
| `pass` | `review_progress` | 140/140 | all review sessions complete |

## Post V5 Reruns

| Status | Metric | Value | Detail |
| --- | --- | ---: | --- |
| `pass` | `readiness` | ready | failing_gates=0 |
| `pass` | `kaggle_jobs` | 3 | ready_jobs=2; conditional_jobs=1; blocked_jobs=0 |
| `pass` | `conservative_gpu_hours` | 0.89/1.51 | required/required_plus_conditional under 120h Kaggle assumption |
| `pass` | `required_v5_sensitivity` | 2/2 | Qwen2.5-3B 39/200->41/200 (+1.0 pts, CI [-1.0, +3.0]); Qwen3-4B 47/200->49/200 (+1.0 pts, CI [0.0, +2.5]) |
| `pass` | `optional_7b_v5` | 200 | output rows downloaded |

## Qa Gates

| Status | Metric | Value | Detail |
| --- | --- | ---: | --- |
| `pass` | `v5_packet_integrity` | 6 | issues=0 |
| `pass` | `thesis_figure_integrity` | 25 | issues=0 |
| `pass` | `thesis_table_integrity` | 86 | issues=0 |
| `pass` | `api_audit_manifest` | 18 | issues=0 |
| `pass` | `api_audit_import_roundtrip` | 16 | issues=0 |
| `pass` | `gemini_api_audit` | 600 | Gemini 3.5 Flash all-200 strict=163/136/144; secondary=170/161/165 |
| `pass` | `openai_gpt55_full_api_audit` | 600 | GPT-5.5 low all-200 strict=172/169/154; secondary=173/174/168 |
| `pass` | `frontier_api_panel_validation200_v5` | 3000 | models=Claude Sonnet 4.6,DeepSeek V4 Flash,GPT-5.5 low,Gemini 3.5 Flash,Groq Llama 3.3 70B |
| `pass` | `benqa_extended_ai_review` | 1000 | pass=851; warn=149; fail=0 |
| `pass` | `benqa_extension_full851_qwen25_3b` | 2553 | acc=BN:291/851,BG:248/851,EN:437/851; gaps=BG-BN:-5.05pts,BG-EN:-22.21pts |
| `pass` | `benqa_extension_full851_deepseek_v4_flash` | 2553 | acc=BN:665/851,BG:376/851,EN:697/851; gaps=BG-BN:-33.96pts,BG-EN:-37.72pts |
| `pass` | `research_log_compactness` | 72 | issues=0 |
| `pass` | `v5_recoverability_sources` | 600 | summary_rows=300 |
| `pass` | `v5_cross_script_transfer` | 600 | summary_rows=36 |
| `pass` | `v5_token_failure_join` | 600 | summary_rows=78 |
| `pass` | `v5_review_label_sensitivity` | 39 | expected_rows=39 |
| `pass` | `v5_dataset_gap_intervals` | 18 | expected_rows=18 |
| `pass` | `v5_paired_sign_tests` | 18 | expected_rows=18 |
| `pass` | `v5_clustered_gap_robustness` | 192 | summary_rows=18 |
| `pass` | `v5_benqa_subject_stability` | 42 | expected_rows=42 |
| `pass` | `v5_benqa_subject_balance` | 39 | summary_rows=6 |
| `pass` | `v5_qwen_scaling_transfer` | 1800 | summary_rows=63; qwen25_net_gains=bangla:11,banglish:6,english:23; qwen3_gap_change=-18 |
| `pass` | `v5_fragility_overlap` | 200 | summary_rows=65 |
| `pass` | `v5_item_consensus` | 200 | summary_rows=80 |
| `pass` | `v5_difficulty_conditioned_gap` | 200 | summary_rows=36 |
| `pass` | `v5_consensus_stability` | 1400 | summary_rows=21 |
| `pass` | `v5_composition_sensitivity` | 200 | summary_rows=27 |
| `pass` | `v5_shared_examples` | 17 | all_three_strict=5 |
| `pass` | `v5_answer_format_audit` | 1800 | summary_rows=27 |
| `pass` | `v5_response_style_drift` | 1800 | summary_rows=27; qwen3_math_meta=bangla:0,banglish:15,english:1 |
| `pass` | `v5_banglamath_numeric_sensitivity` | 504 | summary_rows=9; qwen3_raw_signature=bangla:19,banglish:10,english:24 |
| `pass` | `v5_banglamath_numeric_transfer` | 168 | summary_rows=3; qwen3_alt_raw=24/56; qwen3_banglish_retains_alt_raw=8/24; qwen3_banglish_correct_alt_raw=2/24; qwen3_meta_alt_raw=9/24; qwen3_no_number_wrong_alt_raw=4/24; qwen25_retains_alt_raw=1/12,4/24 |
| `pass` | `v5_benqa_choice_bias` | 432 | summary_rows=18 |
| `pass` | `v5_benqa_subject_option_bias` | 1296 | summary_rows=117; majority_d_subjects=qwen3:12/13,qwen25_3b:1/13,qwen25_7b:0/13 |
| `pass` | `v5_benqa_prediction_diversity` | 25 | qwen3_effective_options=2.01; qwen3_entropy=0.5023; qwen3_D=111/144; qwen25_effective_options=3.75/3.77; qwen3_majorityD_subjects=12/13 |
| `pass` | `v5_benqa_option_position_content` | 432 | summary_rows=4; D_longest_items=98/144; qwen3_D_when_not_longest=30/46 |
| `pass` | `v5_benqa_option_switching` | 864 | summary_rows=36; qwen3_nonD_to_D=bangla:47/73,english:55/78 |
| `pass` | `v5_benqa_cross_script_option_agreement` | 432 | summary_rows=21; qwen3_correct_BE_agree_nonD_wrongD=23/36; qwen25_wrongD=2/23,7/44; qwen3_BE_agree_nonD_D=30/47; qwen3_BE_agree_D=72/92 |
| `pass` | `v5_benqa_cross_model_banglish_agreement` | 144 | summary_rows=8; q25_agree_nonD_qwen3_D=26/42; q25_agree_nonD_qwen3_wrongD=18/42; q25_correct_nonD_qwen3_wrongD=8/15; q25_correct_nonD_qwen3_same=4/15; q25_correct_D_qwen3_D=7/7 |
| `pass` | `v5_benqa_order_confound` | 432 | summary_rows=39; qwen3_run_quartile_D=26/36,31/36,28/36,26/36; qwen3_wrongD_q1_q4=20/36,19/36; qwen3_D_runs=23; qwen3_longest_D_run=13; qwen25_longest_D_run=3,2 |
| `pass` | `v5_benqa_review_label_option_bias` | 432 | summary_rows=24; qwen3_unreviewed_D=39/51; qwen3_unreviewed_wrongD=28/51; qwen3_minor_D=67/88; qwen3_reviewed_nonbad_D=69/90; qwen25_unreviewed_D=10/51,7/51; qwen25_reviewed_nonbad_D=28/90,17/90 |
| `pass` | `v5_benqa_length_token_confound` | 432 | summary_rows=48; qwen3_token_quartile_D=32/36,26/36,27/36,26/36; qwen3_token_wrongD=26/36,17/36,15/36,19/36; qwen3_char_q1_q4_D=31/36,29/36; qwen3_density_q1_q4_D=33/36,22/36; qwen25_token_q1_q4_D=5/36,14/36;1/36,9/36 |
| `pass` | `v5_benqa_option_coverage_confound` | 432 | summary_rows=21; qwen3_tied_coverage_D=76/101; qwen3_tied_coverage_wrongD=52/101; qwen25_tied_coverage_D=14/101,8/101; qwen3_D_not_highest_coverage=31/35; qwen3_wrongD_not_highest_coverage=23/35; qwen25_D_not_highest_coverage=22/35,15/35; qwen3_D_strict_highest_coverage=1/3 |
| `pass` | `v5_benqa_option_switch_confound` | 864 | summary_rows=36; qwen3_correct_nonD_D_not_longest_wrongD=bangla:11/19,english:12/21 |
| `pass` | `v5_benqa_option_semantic_cues` | 432 | summary_rows=25; D_no_cue=47/144; qwen3_D_no_cue=38/47; qwen3_correct_nonD_no_cue_wrongD=bangla:15/18,english:18/23 |
| `pass` | `v5_benqa_multiconfound_residual` | 432 | summary_rows=36; qwen3_primary_wrongD=19/24; qwen25_primary_wrongD=4/24,1/24; qwen3_tied_wrongD=16/20; qwen3_correct_nonD_residual_wrongD=bangla:11/13,english:11/14; qwen25_correct_nonD_residual_wrongD=bangla:1/7,1/14;english:1/13,0/17 |
| `pass` | `v5_benqa_option_permutation_probe` | 288 | summary_rows=10; qwen3_wrongD_rotated=labelD:35/45,semanticD:6/45; qwen25_wrongD_rotated=labelD:5/21,semanticD:12/21 |
| `pass` | `bnsentmix_external_validation` | 600 | summary_rows=75; qwen25=89/200,macro_f1=0.431; qwen25_7b=98/200,macro_f1=0.479; qwen3=99/200,macro_f1=0.486; valid_outputs=600/600 |
| `pass` | `bnsentmix_model_complementarity` | 200 | summary_rows=23; any_model_oracle=154/200; oracle_minus_best=+27.5pts; majority_7b_fallback=106/200 |
| `pass` | `bnsentmix_routing_devtest` | 15 | summary_rows=14; pilot40_holdout=72/160; hash5_cv=106/200; block40_cv=84/200 |
| `pass` | `v5_benqa_distractor_transition` | 432 | summary_rows=20; consensus_rows=144; valid_recoverable=162/164; two_plus_same_wrong=27/50 |
| `pass` | `v5_benqa_label_balance` | 24 | by_label_rows=36 |
| `pass` | `real_banglish_v5_distribution` | 4400 | summary_rows=4 |
| `pass` | `v5_banglatlit_lexical_coverage` | 200 | summary_rows=15 |
| `pass` | `v5_benqa_option_lexical_coverage` | 144 | summary_rows=15; options_parsed=144/144; options_q4=40/108 vs 50/108; gold_q4=47/108 vs 56/108 |
| `pass` | `v5_banglatlit_model_coverage_sensitivity` | 600 | summary_rows=45; all_q4_direction_ok=True; all_quartile_direction_ok=True |
| `pass` | `v5_banglatlit_spelling_variation_sensitivity` | 600 | summary_rows=45; all_q4_direction_ok=True; q2_to_q4_direction_ok=True |
| `pass` | `v5_source_variant_structural_parity` | 600 | summary_rows=15; primary_hard_fails=0 |
| `pass` | `v5_english_warning_sensitivity` | 600 | summary_rows=27; warning_items=39; clean_direction_ok=True |
| `pass` | `v5_review_edit_distance_sensitivity` | 600 | summary_rows=45; no_change_direction_ok=True |
| `pass` | `secret_hygiene` | 1199 | suspicious_findings=0 |
| `pass` | `local_artifact_refs` | 4835 | unexpected_missing=0; expected_future=18 |
| `pass` | `reproducibility_manifest` | 1197 | non-secret artifacts tracked |

## Literature

| Status | Metric | Value | Detail |
| --- | --- | ---: | --- |
| `pass` | `literature_corpus` | 33 | issues=0 |
| `pass` | `citation_readiness` | 33 | issues=0 |
