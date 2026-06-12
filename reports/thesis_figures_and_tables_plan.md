# Thesis Figures And Tables Plan

Updated: 2026-05-31

## Purpose

This plan maps the current evidence into thesis-ready tables and figures. It
should prevent the write-up from becoming a pile of exploratory reports.

## Main Tables

| Table | Role | Source artifact | Status |
| --- | --- | --- | --- |
| T1: Validation-200 composition | Dataset sources, item counts, script variants, dev/test split | `reports/dataset_card_validation200.md`, `data/slices/*.manifest.json` | Frozen v5 state reflected in dataset card. |
| T2: Main script gap | Primary frozen-v5 Qwen2.5/Qwen3 Bangla/reviewed-Banglish/English result with paired CIs | `results/tables/main_script_gap_validation200_v5.csv` | Ready; reviewed v5 promoted. Historical table retained separately. |
| T3: Model-family breadth | Qwen scaling, Phi, diagnostic models | `results/tables/model_family_scaling_validation200.csv` | Ready as nuance/breadth table. |
| T4: Robustness checks | v4 cleanup, auto-suggested cleanup, noisy Banglish, reviewed-v5 cleanup, strict-197 policy | `reports/v4_banglish_sensitivity_validation200.md`, `reports/validation200_v4_auto_suggested_sensitivity.md`, `reports/noisy_banglish_validation200.md`, `reports/v5_bad_row_policy_sensitivity.md` | Ready. |
| T5: Tokenization by script | Bangla/Banglish/English token cost by dataset | `reports/tokenization_validation200.md` | Ready; keep descriptive. |
| T6: Cross-script oracle and agreement | Reviewed-v5 recoverability and privileged agreement routing | `results/tables/cross_script_answer_agreement.csv`, `reports/cross_script_diagnostics_validation200_v5.md` | Ready; label diagnostic. |
| T7: Mitigation summary | Self-normalization and answer-signal routing | `results/tables/selfnorm_validation200.csv`, `results/tables/answer_signal_routing_test150.csv` | Ready; separate exploratory routing from primary. |
| T8: Generated-view diagnostics | Preservation gates, dev answer audits, and agreement routes | `results/tables/generated_view_preservation_v2.csv`, `results/tables/generated_bn_answer_audit_dev50.csv`, `results/tables/generated_view_agreement_route_dev.csv` | Ready; dev-only diagnostic. |
| T9: Real Banglish comparison | BanglaTLit vs validation-200 clean Banglish | `results/tables/real_banglish_distribution.csv` | Ready for limitations. |
| T10: v5 review/release status | Review tiers, substitutions, metadata, bad-row policy | `reports/validation200_v5_review_impact_ranking.md`, `reports/validation200_v5_review_metadata_summary.md` | Ready; review complete. |

## Main Figures

| Figure | Message | Data source | Recommended form |
| --- | --- | --- | --- |
| F1: Paired script-gap bars | Reviewed Banglish drops below Bangla/English for competent Qwen models | `results/tables/main_script_gap_validation200_v5.csv` | Grouped bar chart; surrounding table carries CI labels and 3B nuance. |
| F2: Scaling trajectory | Script gap becomes meaningful once models have task competence | `results/tables/model_family_scaling_validation200.csv` | Line or slope plot by model size/family. |
| F3: Token cost vs accuracy | Banglish is token-cheaper than Bangla but less accurate | `reports/tokenization_validation200.md` + main result table | Scatter or paired arrow plot. |
| F4: Failure taxonomy | Many reviewed-Banglish misses are correct under Bangla or English | `reports/cross_script_diagnostics_validation200_v5.md` | Stacked bar by failure category. |
| F5: Oracle/agreement recovery | Reviewed-v5 cross-script agreement recovers signal but is privileged | `results/tables/cross_script_answer_agreement.csv` | Bar chart: Banglish, agreement route, oracle. |
| F6: Mitigation brittleness | Self-normalization helps Qwen2.5-3B, not Qwen2.5-7B, hurts Qwen3 | `results/tables/selfnorm_validation200.csv` | Delta bar chart with CIs. |
| F7: v5 review impact map | Human review focuses on test rows and repeated substitutions | `reports/validation200_v5_review_impact_ranking.md`, `reports/validation200_v5_review_impact_substitutions.md` | Small stacked bars or table-figure. |
| F8: Generated-view funnel | Raw generators fail gates; guarded/protected views pass gates but answer/routing gains are unstable | `results/tables/deterministic_generated_view_smokes.csv`, `results/tables/generated_bn_answer_audit_dev50.csv`, `results/tables/generated_view_agreement_route_dev.csv` | Funnel diagram or grouped table. |

## Tables To Avoid In Main Body

- Full Kaggle run logs.
- Every pilot20 result.
- Every generated-view item-level audit.
- Full v5 review queue.
- Full bootstrap resample outputs.

Move these to appendix or artifact references.

## Appendix Tables

| Appendix table | Source |
| --- | --- |
| Full model-family result matrix | `reports/model_family_scaling_synthesis_validation200.md` |
| Subject breakdown | `reports/subject_breakdown_validation200_v5.md` |
| v4/v5 item-flip table after reruns | future `results/analysis/*v5_vs_v4*_items.csv` |
| Generated-view preservation failures | `reports/generated_view_preservation_audit_v2.md` |
| Real-Banglish distribution details | `reports/real_banglish_distribution_comparison.md` |
| Artifact manifest | `reports/reproducibility_artifact_manifest.md` |

## Figure Build Notes

- Draft SVG figures are available in `reports/figures/` and can be regenerated
  with `python3 scripts/build_thesis_figures.py`.
- Use accuracy as percent points in figures, but keep numerator/denominator in
  table labels.
- Always label whether a result is full200, dev50, or test150.
- Use paired bootstrap intervals for script-gap and mitigation deltas.
- Mark generated-view and answer-signal routing figures as diagnostic or
  exploratory unless v5/post-v5 preregistration promotes them.
- Do not combine v3, v4, and v5 rows in one primary figure without a footnote.

## Post-v5 Updates

Completed on 2026-05-30:

1. Promoted reviewed v5 into T2 and F1.
2. Added v5-v4 and strict-197 sensitivity artifacts to T4.
3. Added final reviewed-row and bad-row counts to T10.
4. Retained `results/tables/main_script_gap_validation200.csv` as the
   historical provenance table for earlier analyses.
5. Regenerated figures and updated captions.
6. Refreshed the subject/grade breakdown against frozen-v5 reviewed Banglish.
