# Thesis Appendix Plan

Updated: 2026-05-30

## Purpose

This plan decides what belongs outside the main thesis chapters. The main body
should argue the contribution; appendices should preserve auditability,
qualitative depth, and reproducibility without interrupting the narrative.

## Appendix A: Dataset Construction And Review

Include:

- Validation-200 source composition and split details.
- Banglish generation and v4 cleanup audit.
- v5 human-review protocol, progress summary, and final label counts.
- Bad-row policy and denominator choice.

Primary artifacts:

- `reports/dataset_card_validation200.md`
- `reports/validation200_v5_human_review_operator_checklist.md`
- `reports/validation200_v5_review_progress.md`
- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_impact_substitutions.md`
- `reports/validation200_v5_substitution_review_playbook.md`
- `reports/v5_bad_row_policy_sensitivity.md`

Do not include the full 140-row CSV in the printed appendix unless required.
Reference the artifact manifest instead.

## Appendix B: Full Result Tables

Include:

- Full model-family result matrix.
- Frozen-v5 subject and dataset breakdowns.
- Bootstrap intervals.
- v4/v5 sensitivity after reruns.

Primary artifacts:

- `results/tables/thesis_tables.md`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/subject_breakdown_validation200_v5.md`
- `reports/v4_banglish_sensitivity_validation200.md`
- `results/tables/main_script_gap_validation200_v5.csv`
- `results/tables/main_script_gap_validation200.csv`
- `results/tables/v5_reviewed_banglish_sensitivity.csv`
- `results/tables/v5_bad_row_policy_sensitivity.csv`

Main-body rule:

- Main chapters should keep only the tables needed for the thesis claim. Move
  diagnostic pilots and failed model-family probes here.

## Appendix C: Qualitative Examples

Include:

- Cross-script answer-agreement examples.
- Frozen-v5 shared-fragility examples.
- Generated-view preservation failures.
- Self-normalization examples where useful.

Primary artifacts:

- `reports/thesis_qualitative_examples.md`
- `reports/v5_shared_fragility_examples.md`
- `reports/cross_script_answer_agreement_examples.md`
- `reports/generated_view_preservation_audit_v2.md`
- `reports/qwen25_selfnorm_answer_signal_routing_examples.md`
- `reports/qwen3_selfnorm_answer_signal_routing_examples.md`

Main-body rule:

- Use at most two or three examples in Chapter 6. Put the rest here.

## Appendix D: Mitigation And Generated-View Diagnostics

Include:

- Prompt/self-normalization variants.
- Answer-signal routing scans.
- Cross-script agreement route.
- Deterministic generated-Bangla preservation and answer audits.
- Generated-English self-translation failure.
- Guarded generated-English repair and protected-v3 BN + guarded EN route.
- Generated-view route bottleneck analysis.
- Generated-view routing candidate scan.

Primary artifacts:

- `reports/selfnorm_validation200.md`
- `reports/qwen25_7b_8bit_selfnorm_validation200_v4.md`
- `reports/selfnorm_answer_signal_routing_validation200.md`
- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/generated_view_diagnostics_summary.md`
- `reports/qwen3_4b_generated_view_agreement_route_dev.md`
- `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/generated_view_route_bottleneck_analysis.md`
- `reports/generated_view_routing_candidate_scan.md`

Main-body rule:

- Keep privileged and dev-only mitigation results clearly marked. Do not let
  appendix detail weaken the main claim by making exploratory scans look final.

## Appendix E: Literature And Citation Support

Include:

- Citation key map.
- Benchmark gap matrix.
- Core paper notes.
- Model-candidate notes if needed.

Primary artifacts:

- `literature/notes/citation_key_map.md`
- `literature/references_seed.bib`
- `literature/notes/benchmark_gap_matrix.md`
- `literature/notes/core_paper_notes.md`
- `literature/notes/script_matters_literature_synthesis.md`

## Appendix F: Reproducibility

Include:

- Artifact manifest.
- Local reference checker result.
- Release checklist.
- Environment and Kaggle feasibility summary.
- Evaluation scripts and parser notes.

Primary artifacts:

- `reports/reproducibility_artifact_manifest.md`
- `reports/local_artifact_reference_check.md`
- `reports/reproducibility_release_checklist.md`
- `reports/kaggle_gpu_feasibility_notes.md`
- `scripts/run_eval_kaggle.py`
- `scripts/summarize_outputs.py`
- `scripts/build_thesis_tables.py`

## Post-v5 Update

Completed on 2026-05-30:

1. Final v5 review counts are available for Appendix A.
2. The v5-v4 sensitivity table is available for Appendix B.
3. Appendix C qualitative examples were refreshed; `banglamath_1697` was
   retired as a current failure example after its reviewed wording changed the
   Qwen3 result.
4. Figures were regenerated.
5. The artifact manifest and local-reference check were rebuilt.
6. The reviewed-v5 all-200 table was promoted to the main body; the older
   v3/v4 table remains in Appendix B for provenance.
7. The subject/grade breakdown was refreshed against frozen-v5 reviewed
   Banglish.
