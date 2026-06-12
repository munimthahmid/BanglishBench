# Continuous Research Checkpoint: 2026-06-03

## Current State

The frozen validation-200 v5 benchmark remains locked. This continuation made
two no-spend research advances:

- a controlled reviewed-v5 BEnQA option-permutation dev probe that
  distinguishes literal label-position attraction from semantic distractor
  tracking;
- a BnSentMix natural Bengali-English code-mixed sentiment external-validation
  layer that broadens ecological validity beyond controlled QA/math, now with a
  Qwen2.5-7B 8-bit scaling row.

All Kaggle P100 runs completed successfully. No paid API call was made.

## Controlled Option-Permutation Probe

Artifacts:

- `scripts/build_v5_benqa_option_permutation_probe.py`
- `scripts/analyze_v5_benqa_option_permutation_probe.py`
- `data/slices/validation200_v5_dev50_benqa_option_permutations.jsonl`
- `reports/v5_benqa_option_permutation_probe.md`
- `reports/v5_benqa_option_permutation_probe_results.md`
- `results/analysis/v5_benqa_option_permutation_probe_items.csv`
- `results/analysis/v5_benqa_option_permutation_probe_summary.csv`
- `results/tables/v5_benqa_option_permutation_dev50.csv`

Design:

- Select the 36 reviewed-v5 BEnQA MCQs in the existing v4 dev50 id set.
- Emit four cyclic option rotations per item, producing 144 inference rows.
- Rotate semantic option content through A/B/C/D and remap gold labels.
- Keep the resulting gold grid balanced: 36 rows for each answer label.
- Run reviewed Banglish only with Qwen3-4B and Qwen2.5-3B.

## Result

| Model | Identity D predictions | Identity wrong-D items | Rotated identity-wrong-D rows | Remain literal label D | Follow original-D content |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen3-4B | 26/36 | 15 | 45 | 35/45 | 6/45 |
| Qwen2.5-3B | 11/36 | 7 | 21 | 5/21 | 12/21 |

The Qwen3 contrast is strong: after semantic content moves, most identity
wrong-D rows remain attached to literal position D rather than following the
original D distractor. Qwen2.5-3B trends in the opposite direction. This
supports a Qwen3-specific label-position D-attractor interpretation under
reviewed Banglish.

Claim boundary: this is a 36-item controlled dev-only behavioral intervention.
It does not prove an internal causal mechanism, does not explain every Qwen2.5
error, and is not a held-out mitigation result.

## BnSentMix External-Validation Layer

Artifacts:

- `scripts/fetch_bnsentmix.py`
- `scripts/build_bnsentmix_external_validation_slice.py`
- `scripts/analyze_bnsentmix_external_validation.py`
- `scripts/analyze_bnsentmix_model_complementarity.py`
- `scripts/analyze_bnsentmix_routing_devtest.py`
- `data/slices/bnsentmix_balanced200_v1.jsonl`
- `reports/bnsentmix_external_validation_slice.md`
- `reports/bnsentmix_external_validation_results.md`
- `reports/bnsentmix_model_complementarity.md`
- `reports/bnsentmix_routing_devtest.md`
- `results/analysis/bnsentmix_external_validation_items.csv`
- `results/analysis/bnsentmix_external_validation_summary.csv`
- `results/analysis/bnsentmix_model_complementarity_items.csv`
- `results/analysis/bnsentmix_model_complementarity_summary.csv`
- `results/analysis/bnsentmix_routing_devtest_candidates.csv`
- `results/analysis/bnsentmix_routing_devtest_summary.csv`
- `results/tables/bnsentmix_external_validation.csv`
- `results/tables/bnsentmix_model_complementarity.csv`
- `results/tables/bnsentmix_routing_devtest.csv`

Design:

- Pin the Hugging Face BnSentMix CSV by SHA-256.
- Remove exact duplicate text before sampling.
- Build a deterministic 200-row balanced slice: 50 positive, 50 negative,
  50 neutral, and 50 mixed.
- Use the first 40 rows as a balanced pilot prefix.
- Evaluate sentiment as word labels rather than A/B/C/D choices.

Result:

| Model | Rows | Valid outputs | Correct | Macro-F1 | Main weakness |
| --- | ---: | ---: | ---: | ---: | --- |
| Qwen2.5-3B | 200 | 200/200 | 89/200 | 0.431 | Neutral recall is 20%; mixed recall is 42%. |
| Qwen2.5-7B 8-bit | 200 | 200/200 | 98/200 | 0.479 | Neutral overprediction: predicts neutral on 92/200 rows. |
| Qwen3-4B | 200 | 200/200 | 99/200 | 0.486 | Strong positive-label bias: predicts positive on 106/200 rows. |

Complementarity result: the best single row is Qwen3-4B at 99/200, but the
any-model diagnostic oracle reaches 154/200, +27.5 points over best single
with CI [+21.5,+34.0]. Exactly one model is correct on 66/200 items.

Routing stress test: majority vote with Qwen2.5-7B fallback is the only simple
candidate that survives hash5 selection, reaching 106/200, but pilot40
selection reaches only 72/160 on holdout and block40 CV reaches 84/200.

Claim boundary: this is ecological-validity evidence for natural code-mixed
text. It is not a paired script-effect estimate because BnSentMix has no
matched Bangla-script or English view per item. Public-dataset contamination
and upstream license metadata mismatch remain threats to validity. The
any-model oracle is diagnostic error-overlap evidence, and the route stress
test is not strong enough to claim deployable accuracy.

## Integration

The probe is now included in:

- `reports/chapter_6_failure_analysis_draft.md`
- `reports/thesis_writeup_blueprint.md`
- `reports/thesis_results_dashboard.md`
- `reports/evidence_matrix.md`
- `reports/current_research_state.md`
- `reports/threats_to_validity.md`
- `reports/thesis_defense_slide_outline.md`
- `reports/thesis_defense_qna.md`
- `reports/next_experiment_decision_queue.md`
- `reports/bnsentmix_external_validation_results.md`
- `reports/bnsentmix_model_complementarity.md`
- `reports/bnsentmix_routing_devtest.md`
- `research_log.md`
- `project_index.md`
- `results/experiment_log.md`

The restart ledger remains below its compactness budget while preserving all
required references.

## QA Snapshot

`python3 scripts/run_research_checks.py` passed end to end after the new
analysis was integrated:

- Thesis tables: 86/86 checks.
- Thesis figures: 25/25 checks.
- v5 review packets: 6/6 checks.
- Research-log compactness: 72/72 checks.
- Literature corpus and citation readiness: 33/33 complete.
- Secret hygiene: 930 files checked, 0 suspicious findings.
- Local artifact references: 4,212 checked, 0 unexpected missing.
- Reproducibility manifest: 928 non-secret artifacts after adding this
  checkpoint.

## Queue

1. Use the completed BnSentMix external layer and routing stress test in
   ecological-validity/complementarity prose, without merging it into the
   paired validation-200 script-gap estimate or claiming solved deployment.
2. Keep the frozen-v5 paid API smoke optional and approval-gated under
   `reports/final_api_audit_cost_plan.md`.
3. Pause generated-view routing unless a better generated-English source avoids
   source fallbacks and produces a stronger locked dev agreement rule.
4. Do not launch adjacent Qwen-only BEnQA D-attractor probes unless they answer
   a distinct mechanism or mitigation question.
