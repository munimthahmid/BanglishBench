# Reproducibility Artifact Manifest

Updated: 2026-06-11

This manifest records non-secret local artifacts needed to reproduce the
current Script Matters thesis state. It intentionally excludes Kaggle API
keys, PEM files, virtual environments, raw credential files, and its own
generated manifest outputs.

Machine-readable manifest: `results/analysis/reproducibility_artifact_manifest.csv`.

## Summary

| Category | Files | Total bytes |
| --- | ---: | ---: |
| analysis_table | 573 | 26279925 |
| dataset_slice | 58 | 17018718 |
| generated_view | 6 | 462245 |
| literature_note | 5 | 51409 |
| project_log | 5 | 291664 |
| report | 345 | 3867871 |
| script | 183 | 2100137 |
| thesis_table | 22 | 33652 |

## Core Thesis Artifacts

| Path | Category | Bytes | SHA-256 prefix |
| --- | --- | ---: | --- |
| `data/slices/validation_200_v3.jsonl` | dataset_slice | 333019 | `8506113bc086` |
| `data/slices/validation_200_v3.manifest.json` | dataset_slice | 1267 | `cf4d45161074` |
| `data/slices/validation_200_v4.jsonl` | dataset_slice | 334159 | `91fc51a3d0a1` |
| `data/slices/validation_200_v4.manifest.json` | dataset_slice | 615 | `ab8a4c2a3ab7` |
| `data/slices/validation_200_v4_auto_suggested.jsonl` | dataset_slice | 410088 | `3630b54bd46a` |
| `data/slices/validation_200_v4_auto_suggested.manifest.json` | dataset_slice | 2681 | `d8b9225d61a0` |
| `data/slices/validation_200_v4_dev50.jsonl` | dataset_slice | 84731 | `6a9b2e3856c5` |
| `data/slices/validation_200_v4_dev50.manifest.json` | dataset_slice | 1422 | `d973ccb9f3eb` |
| `data/slices/validation_200_v4_test150.jsonl` | dataset_slice | 249428 | `b13f6e2897f7` |
| `data/slices/validation_200_v5.jsonl` | dataset_slice | 354346 | `3fd9908a46a8` |
| `data/slices/validation_200_v5.manifest.json` | dataset_slice | 890 | `0f283dda2e54` |
| `data/slices/validation_200_v5_review_queue.csv` | dataset_slice | 164053 | `c4ed3b08fdce` |
| `data/slices/validation_200_v5_review_queue.csv.ai_review_20260529_164442.bak` | dataset_slice | 135242 | `1b57d278ac0f` |
| `data/slices/validation_200_v5_review_queue.csv.bak` | dataset_slice | 135135 | `7427aa2e23eb` |
| `project_index.md` | project_log | 34003 | `f04343694322` |
| `requirements-kaggle.txt` | project_log | 59 | `a4a1408e8d8d` |
| `research_log.md` | project_log | 17459 | `09c0527f6d61` |
| `results/experiment_log.md` | project_log | 175344 | `6271bc09dc6f` |
| `thesis_plan.md` | project_log | 64799 | `d99d0f4316f5` |
| `reports/current_research_state.md` | report | 54967 | `3411342a1d0b` |
| `reports/dataset_card_validation200.md` | report | 5261 | `3943dc8dfc69` |
| `reports/evidence_matrix.md` | report | 42354 | `a7888bfe12dd` |
| `reports/final_api_audit_cost_plan.md` | report | 7063 | `135986470ad8` |
| `reports/post_v5_compute_budget.md` | report | 1822 | `fd857de7f644` |
| `reports/post_v5_kaggle_job_plan.md` | report | 3166 | `fe4d24c98fcd` |
| `reports/post_v5_rerun_protocol.md` | report | 5987 | `02d7593f9e2a` |
| `reports/post_v5_rerun_readiness.md` | report | 1661 | `f38f0bc182cf` |
| `reports/post_v5_thesis_revision_todo.md` | report | 5068 | `3e7c28c51d1e` |
| `reports/thesis_abstract_and_contributions_draft.md` | report | 7002 | `b33e026d06ca` |
| `reports/thesis_appendix_plan.md` | report | 5217 | `70d312202469` |
| `reports/thesis_defense_qna.md` | report | 9000 | `551d4a324ef7` |
| `reports/thesis_defense_slide_outline.md` | report | 7850 | `058fafcbff2e` |
| `reports/thesis_draft_compiled.md` | report | 108838 | `6beb21567665` |
| `reports/thesis_figure_captions.md` | report | 3639 | `41d280cf5390` |
| `reports/thesis_figure_integrity_check.md` | report | 2614 | `ae040978d282` |
| `reports/thesis_figures_and_tables_plan.md` | report | 6226 | `2306b8ca891a` |
| `reports/thesis_qualitative_examples.md` | report | 2293 | `030d7033ff0d` |
| `reports/thesis_results_dashboard.md` | report | 28854 | `2e7a83c89977` |
| `reports/thesis_table_integrity_check.md` | report | 10592 | `bed384097ac0` |
| `reports/thesis_weakness_hardening_plan.md` | report | 9630 | `f3df62f73b29` |
| `reports/thesis_writeup_blueprint.md` | report | 30774 | `d626d466d132` |
| `scripts/apply_banglish_review.py` | script | 7761 | `f9a2acba1dfa` |
| `scripts/run_eval_kaggle.py` | script | 24940 | `a0cd7c9a1485` |
| `scripts/validate_banglish_review_queue.py` | script | 14403 | `5a4a63780d8e` |
| `results/tables/answer_signal_routing_test150.csv` | thesis_table | 381 | `5ef2b10c3e54` |
| `results/tables/auto_suggested_banglish_sensitivity.csv` | thesis_table | 194 | `4b4c8fed5bf4` |
| `results/tables/bnsentmix_external_validation.csv` | thesis_table | 521 | `60cd9df9d21d` |
| `results/tables/bnsentmix_model_complementarity.csv` | thesis_table | 686 | `1fea804af198` |
| `results/tables/bnsentmix_routing_devtest.csv` | thesis_table | 601 | `68f334e9a5c5` |
| `results/tables/cross_script_answer_agreement.csv` | thesis_table | 356 | `e44ba3c9bbf4` |
| `results/tables/deterministic_generated_view_smokes.csv` | thesis_table | 1273 | `e22aea33d029` |
| `results/tables/diagnostic_model_pilots.csv` | thesis_table | 341 | `c59f6f0fa3f4` |
| `results/tables/generated_bn_answer_audit_dev50.csv` | thesis_table | 2157 | `2d0889116c90` |
| `results/tables/generated_bn_candidate_preservation.csv` | thesis_table | 1396 | `218dd11dea98` |
| `results/tables/generated_bn_reference_similarity_dev50.csv` | thesis_table | 426 | `582580fc1bee` |
| `results/tables/generated_view_agreement_route_dev.csv` | thesis_table | 514 | `249771b62884` |
| `results/tables/generated_view_preservation_v2.csv` | thesis_table | 563 | `ee8244157ee1` |
| `results/tables/main_script_gap_validation200.csv` | thesis_table | 675 | `f482aaff87f3` |
| `results/tables/main_script_gap_validation200_v5.csv` | thesis_table | 635 | `3493a30dff77` |
| `results/tables/model_family_scaling_validation200.csv` | thesis_table | 1446 | `b86f1a2096df` |
| `results/tables/real_banglish_distribution.csv` | thesis_table | 319 | `2073221c949e` |
| `results/tables/selfnorm_validation200.csv` | thesis_table | 295 | `7b481dc13749` |
| `results/tables/thesis_tables.md` | thesis_table | 19010 | `77722836aa2f` |
| `results/tables/v5_bad_row_policy_sensitivity.csv` | thesis_table | 917 | `8002a6a6c457` |
| `results/tables/v5_benqa_option_permutation_dev50.csv` | thesis_table | 413 | `1dd4181f9ad8` |
| `results/tables/v5_reviewed_banglish_sensitivity.csv` | thesis_table | 533 | `5709b76d130e` |

## Notes

- Rebuild this manifest after freezing v5 or regenerating thesis tables.
- Treat changes in dataset slices, parser/evaluator scripts, or thesis
  tables as versioned thesis events and log them in `research_log.md`.
- The full CSV contains every included artifact and complete SHA-256 hash.
