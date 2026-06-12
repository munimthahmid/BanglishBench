# Continuous Research Checkpoint: 2026-05-31

## Current State

The reviewed validation-200 v5 benchmark remains frozen and the release-facing
Qwen table is unchanged. The 2026-05-31 work focused on reducing restart-log
size, adding no-spend consensus/label-balance evidence, auditing
source-variant structural parity and review edit-distance sensitivity, and
advancing the non-paid deployable-routing path plus BEnQA option-switching
and switch-confound diagnostics.

## Log Compaction

`research_log.md` is a guarded restart ledger at 235 lines / 12.8 KB while
preserving:

- The frozen-v5 thesis claim and caveats.
- The three-model reviewed-v5 main result.
- The strict-197 sensitivity result.
- Tokenization and cross-script diagnostic evidence.
- Compute policy, QA state, and immediate queue.

Detailed run provenance remains in `results/experiment_log.md`.

## Frozen-V5 Source-Variant Structural Parity

A no-spend source audit now checks all frozen-v5 Bangla, reviewed Banglish, and
English prompt variants for MCQ option labels, digit sequences, formula-like
tokens, and answer instructions.

Artifacts:

- `scripts/analyze_v5_source_variant_structural_parity.py`
- `reports/v5_source_variant_structural_parity.md`
- `results/analysis/v5_source_variant_structural_parity_items.csv`
- `results/analysis/v5_source_variant_structural_parity_summary.csv`

Key result:

- Bangla vs reviewed Banglish has 0/200 structural mismatches and 0 primary
  hard-fail rows.
- Bangla vs English and reviewed Banglish vs English each have 39/200
  diagnostic warnings, mostly digit/formula differences from upstream English
  translations.

Interpretation: the primary paired Bangla-vs-reviewed-Banglish claim is not
driven by source-variant option/digit/formula/instruction mismatches. English
remains useful privileged diagnostic evidence, but these warnings should be
cited as source-translation caveats.

## English-Warning Sensitivity

The source-parity result raises a narrower diagnostic question: whether the
English-backed oracle/recoverability evidence depends on the 39 items with
English-side structural warnings. A new no-spend sensitivity audit separates
those warning rows from the 161 English-structurally-clean rows.

Artifacts:

- `scripts/analyze_v5_english_warning_sensitivity.py`
- `reports/v5_english_warning_sensitivity.md`
- `results/analysis/v5_english_warning_sensitivity_items.csv`
- `results/analysis/v5_english_warning_sensitivity_summary.csv`

Key result:

- On the 161 clean-English items, reviewed Banglish remains below both Bangla
  and English for Qwen2.5-3B (31/161 vs 45/161 Bangla and 60/161 English),
  Qwen2.5-7B (38/161 vs 55/161 and 80/161), and Qwen3 (36/161 vs 64/161 and
  73/161).
- Recoverable Banglish misses persist on that clean-English subset: 50, 58,
  and 51 for Qwen2.5-3B, Qwen2.5-7B, and Qwen3 respectively.

Interpretation: English source warnings should remain explicit caveats, but
the English-backed diagnostic story is not carried only by those warning rows.

## Review Edit-Distance Sensitivity

The review-label check now has a finer no-spend companion audit that asks
whether the final reviewed-v5 gap is introduced only by rows that required
substantial Banglish edits.

Artifacts:

- `scripts/analyze_v5_review_edit_distance_sensitivity.py`
- `reports/v5_review_edit_distance_sensitivity.md`
- `results/analysis/v5_review_edit_distance_sensitivity_items.csv`
- `results/analysis/v5_review_edit_distance_sensitivity_summary.csv`

Key result:

- Applied-edit buckets contain 63 no-applied-change rows, 73 tiny edits, 45
  small edits, and 19 larger edits.
- The 63 no-applied-change rows already keep reviewed Banglish below Bangla
  and English for all three thesis-facing Qwen rows.
- Larger-edit rows are too few to support a standalone effect-size claim, but
  they are now visible as a dataset-quality caveat.

Interpretation: the reviewed-v5 deficit is not introduced only by heavier
manual Banglish edits, strengthening the cleanup-sensitivity story while
keeping small edit strata descriptive.

## Reviewed-V5 Generated-BN Dev Assets

The protected-v2 deterministic generated-Bengali route was rebuilt against
reviewed v5 Banglish, using the old v4 dev50 ids only as the split filter.
Nineteen of the 36 dev BEnQA MCQ rows changed from v4 to v5, so this v5-aligned
slice is the correct dev input for the next answer audit.

Artifacts:

- Prompt set:
  `data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl`
- Prompt report:
  `reports/generated_view_prompt_set_v5_dev50_benqa_mcq.md`
- Phonetic protected-v2 generated BN:
  `results/generated_views/phonetic_bangla_protected_v2_v5_dev50_benqa_mcq_generated_bn.jsonl`
- BNB protected-v2 generated BN:
  `results/generated_views/bnbphoneticparser_protected_v2_v5_dev50_benqa_mcq_generated_bn.jsonl`
- Answer-audit slice:
  `data/generated_views/validation200_v5_dev50_benqa_mcq_protected_v2_generated_bn_answer_audit.jsonl`
- Answer-audit slice report:
  `reports/generated_bn_answer_audit_slice_v5_dev50_benqa_mcq.md`

Preservation gates:

- Phonetic protected-v2 v5: 36 rows, 16 tightened formula-expression hard
  failures.
- BNB protected-v2 v5: 36 rows, 16 tightened formula-expression hard failures.

The first structural gate pass was too weak: item-level answer-audit inspection
showed formula/operator corruption, so the auditor now treats formula-like
expressions as preservation-critical.

## Formulaish Protected-V3 Repair

The deterministic protection wrapper was extended to mask the same formula-like
ASCII/operator tokens that the auditor now checks. Reviewed-v5 protected-v3
outputs were generated for both deterministic generators.

Artifacts:

- Phonetic protected-v3 generated BN:
  `results/generated_views/phonetic_bangla_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`
- BNB protected-v3 generated BN:
  `results/generated_views/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`
- Phonetic protected-v3 audit:
  `reports/phonetic_bangla_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- BNB protected-v3 audit:
  `reports/bnbphoneticparser_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- Protected-v3 answer-audit slice:
  `data/generated_views/validation200_v5_dev50_benqa_mcq_protected_v3_generated_bn_answer_audit.jsonl`

Preservation gates:

- Phonetic protected-v3 v5: 36 rows, 0 hard failures.
- BNB protected-v3 v5: 36 rows, 0 hard failures.

Kaggle dev answer-audit kernels completed:

- Qwen3-4B:
  `munimthahmid/qwen3-4b-generated-bn-v5-protected-v3-dev50`
  - `results/runs/qwen3_4b_generated_bn_v5_pv3_dev50/`
  - `reports/qwen3_4b_generated_bn_v5_pv3_dev50.md`
- Qwen2.5-3B:
  `munimthahmid3/qwen2-5-3b-generated-bn-v5-protected-v3-dev50`
  - `results/runs/qwen25_3b_generated_bn_v5_pv3_dev50/`
  - `reports/qwen25_3b_generated_bn_v5_pv3_dev50.md`

Protected-v3 answer audit:

- Qwen3-4B: Banglish 15/36, phonetic-v3 14/36, BNB-v3 17/36. BNB
  delta is +5.6 pts with CI [-8.3,+19.4].
- Qwen2.5-3B: Banglish 9/36, phonetic-v3 10/36, BNB-v3 9/36. Phonetic
  delta is +2.8 pts with CI [-13.9,+19.4].

Interpretation: protected-v3 repairs generated-BN preservation, but
generated-BN alone is not strong enough for test150.

## Guarded Generated-English Repair

The raw Qwen3 generated-English self-translation remained weak under the
tightened auditor: 16/36 hard failures and 18/36 warnings, mostly from
digit/formula and line-count changes. A conservative deterministic repair now
keeps only preservation-safe generated stems and restores the source
option/answer lines; when preservation still fails it falls back to the source
Banglish row.

Artifacts:

- Guarded generated-English output:
  `results/generated_views/qwen3_4b_selftranslate_guarded_v5_dev50_benqa_mcq_generated_en.jsonl`
- Guarded preservation report:
  `reports/qwen3_4b_selftranslate_guarded_v5_generated_en_dev50_benqa_mcq_audit.md`
- Guarded answer-audit slice:
  `data/generated_views/validation200_v5_dev50_benqa_mcq_guarded_generated_en_answer_audit.jsonl`
- Qwen3 answer audit:
  `reports/qwen3_4b_guarded_generated_en_v5_dev50.md`
- Qwen2.5 answer audit:
  `reports/qwen25_3b_guarded_generated_en_v5_dev50.md`
- Guarded repair provenance:
  `reports/guarded_generated_en_repair_provenance.md`
- Route bottleneck analysis:
  `reports/generated_view_route_bottleneck_analysis.md`
- Routing-candidate scan:
  `reports/generated_view_routing_candidate_scan.md`

Guarded preservation and answer audit:

- Preservation: 0/36 hard failures, 0 warnings.
- Repair provenance: 21/36 translated-stem rows, 15/36 source fallbacks.
- Qwen3-4B: Banglish 15/36, guarded EN 15/36, delta 0.0 pts with CI
  [-11.1,+11.1].
- Qwen2.5-3B: Banglish 9/36, guarded EN 11/36, delta +5.6 pts with CI
  [-8.3,+19.4].
- Provenance split: the 21 translated-stem rows account for the Qwen2.5 +2
  guarded-EN answer delta; the 15 source-fallback rows have zero answer delta
  for both Qwen3 and Qwen2.5.

Agreement routes:

- Qwen3 protected-v3 BNB + guarded EN: 16/36 routed vs 15/36 Banglish,
  one routed item, +1 item.
- Qwen2.5 protected-v3 phonetic + guarded EN: 8/36 routed vs 9/36 Banglish,
  one routed item, -1 item.
- Bottleneck analysis: Qwen3 has 5 baseline-wrong rows recoverable by at
  least one generated view but only 1 recovered by strict agreement; Qwen2.5
  has 10 such rows and 0 recovered by strict agreement.
- Simple deployable routing-candidate scan: Qwen3 best guarded simple rules
  reach 17/36 (+2); Qwen2.5's best reaches 13/36 (+4) but with 5 losses and no
  matching Qwen3 gain. Generated-BN-only is weakly positive on both current
  guarded routes (+2 Qwen3, +1 Qwen2.5) but is still too small/uncertain.

Interpretation: guarded EN repairs hard preservation, but source fallback means
it is not a pure English translation. The resulting routes remain dev-only
diagnostics and should not be launched on test150; the strict agreement rule is
also too sparse to exploit most generated-view recoveries, and simple
answer-level routing alternatives are too volatile on dev.

## Reviewed-V5 Fragility Feature Analysis

A no-spend failure-analysis pass now joins the frozen-v5 cross-script failure
rows with item metadata and prompt features.

Artifacts:

- `scripts/analyze_v5_banglish_fragility_features.py`
- `reports/v5_banglish_fragility_feature_analysis.md`
- `results/analysis/v5_banglish_fragility_items.csv`
- `results/analysis/v5_banglish_fragility_feature_summary.csv`
- `reports/research_log_compactness_check.md`

Key results:

- Banglish-fragile model-item slots: 185/600. Here, reviewed Banglish is wrong
  while Bangla or English is correct.
- Strict Bangla+English-correct/Banglish-wrong slots: 76/600.
- Items with at least one fragile thesis-facing model: 108/200.
- Items fragile for all three thesis-facing models: 21/200.
- Model-overlap refresh: 52 any-fragile items affect exactly one model, 35
  affect exactly two, and 21 affect all three. Shared fragility affects
  56/108 any-fragile items.
- Recoverable fragility is concentrated in BEnQA MCQ science domains; BanglaMATH
  has fewer recoverable fragility events but much higher all-script-wrong
  difficulty.

This strengthens Chapter 6 as descriptive failure analysis, not as a causal
feature attribution or routing rule.

Additional overlap artifacts:

- `scripts/analyze_v5_fragility_model_overlap.py`
- `reports/v5_banglish_fragility_model_overlap.md`
- `results/analysis/v5_banglish_fragility_model_overlap_items.csv`
- `results/analysis/v5_banglish_fragility_model_overlap_summary.csv`

Item-consensus artifacts:

- `scripts/analyze_v5_item_consensus.py`
- `reports/v5_item_consensus.md`
- `results/analysis/v5_item_consensus_items.csv`
- `results/analysis/v5_item_consensus_summary.csv`
- `scripts/analyze_v5_recoverability_sources.py`
- `reports/v5_recoverability_source_decomposition.md`
- `results/analysis/v5_recoverability_source_items.csv`
- `results/analysis/v5_recoverability_source_summary.csv`
- `scripts/analyze_v5_consensus_stability.py`
- `reports/v5_consensus_stability.md`
- `results/analysis/v5_consensus_stability_items.csv`
- `results/analysis/v5_consensus_stability_summary.csv`
- `scripts/analyze_v5_composition_sensitivity.py`
- `reports/v5_composition_sensitivity.md`
- `results/analysis/v5_composition_sensitivity_items.csv`
- `results/analysis/v5_composition_sensitivity_summary.csv`
- `scripts/analyze_v5_benqa_choice_bias.py`
- `reports/v5_benqa_choice_bias.md`
- `results/analysis/v5_benqa_choice_bias_items.csv`
- `results/analysis/v5_benqa_choice_bias_summary.csv`

Item-consensus result:

- Across 600 paired model-item slots, reviewed Banglish is correct 137 times,
  versus 199 for Bangla and 253 for English.
- Item-cluster bootstrap deltas stay negative: -10.3 pts vs Bangla with CI
  [-14.7,-6.3], and -19.3 pts vs English with CI [-25.0,-13.7].
- BEnQA has 61/144 items with at least two-model support in Bangla or English
  while reviewed Banglish has at most one correct model; BanglaMATH remains a
  hard stress-test slice with 42/56 all-script-hard items.
- Recoverability source decomposition: 185/463 reviewed-Banglish misses are
  recoverable by Bangla or English, while 278/463 are all-script hard. Native
  Bangla participates in 104/185 recoverable misses, English in 157/185, and
  both alternates recover 76/185.
- Cross-script transfer retention: when the same model is correct in Bangla or
  English, reviewed Banglish retains correctness only 34/92, 39/107, and
  44/103 times for Qwen2.5-3B, Qwen2.5-7B, and Qwen3 respectively.
- Difficulty-conditioned consensus: on all-200 items where all three Qwen rows
  answer the English view correctly, reviewed Banglish has 50/147 correct
  model-item slots versus 92/147 for Bangla; the paired item-bootstrap delta is
  -28.6 pts, CI [-38.8,-18.4].
- Leave-one-model-out consensus stability: all three two-model Qwen subsets
  keep reviewed Banglish below both Bangla and English on all-200 and BEnQA;
  all-200 Banglish-minus-Bangla pair deltas range from -7.8 to -12.2 pts.
- Composition sensitivity: no-digit, no-formula/operator, and BEnQA
  no-digit/no-formula subsets keep reviewed Banglish below Bangla and English
  for all three thesis-facing Qwen rows.
- BanglaTLit lexical coverage: exact token overlap is low, averaging 36.8%
  across frozen-v5 content Banglish, but the highest-coverage all-200 quartile
  still has reviewed Banglish 28/150 correct slots versus Bangla 40/150.
- BEnQA option lexical coverage: all-option exact BanglaTLit coverage averages
  18.5% and gold-option coverage 17.3%; the highest all-option coverage
  quartile remains directionally negative at 40/108 reviewed-Banglish slots
  versus 50/108 Bangla slots.
- BanglaTLit model-coverage sensitivity: every all-200 lexical-coverage
  quartile keeps reviewed Banglish below Bangla and English for each
  thesis-facing Qwen row; in the highest-coverage quartile, Qwen2.5-3B is
  8/50 vs 10/50 Bangla and 16/50 English, Qwen2.5-7B is 8/50 vs 15/50 and
  21/50, and Qwen3 is 12/50 vs 15/50 and 21/50.
- BanglaTLit spelling-variation sensitivity: the highest all-200
  repeated-variant-exposure quartile keeps reviewed Banglish below Bangla and
  English for all three Qwen rows; the lowest exposure bucket is mixed for
  Qwen2.5-3B, so use it as descriptive robustness/limitation evidence.
- BEnQA choice-bias audit: Qwen2.5 reviewed-Banglish rows do not collapse to
  one option label, while Qwen3 reviewed Banglish over-selects D on 111/144
  rows against a gold D count of 39/144.
- BEnQA distractor-transition audit: 162/164 recoverable reviewed-Banglish
  BEnQA misses are valid distractor choices; 27/50 items with at least two
  valid recoverable Banglish misses share the same wrong option across models.
- BEnQA label-balance sensitivity: gold-label balancing keeps reviewed
  Banglish below Bangla and English for all three thesis-facing Qwen rows;
  Qwen3 is -21.7 pts vs Bangla on the balanced metric and -29.5 pts on the
  non-D slice.

## Frozen-V5 Shared-Fragility Examples

The qualitative example source is now reproducible from the frozen-v5 overlap
and failure-pattern tables. The packet exports 17 shared-strict rows, including
5 all-three strict cases where every thesis-facing Qwen row answers Bangla and
English correctly but reviewed Banglish incorrectly.

Recommended main-body examples:

- `banglamath_0229`
- `banglamath_0230`
- `benqa_10th-Physics_0021`

Artifacts:

- `scripts/export_v5_shared_fragility_examples.py`
- `reports/v5_shared_fragility_examples.md`
- `results/analysis/v5_shared_fragility_examples.csv`

## Frozen-V5 Review-Label Sensitivity

The dataset-quality sensitivity now joins v5 review labels with the frozen-v5
failure taxonomy. It checks whether the final gap is only coming from rows that
needed manual Banglish edits.

Artifacts:

- `scripts/analyze_v5_review_label_sensitivity.py`
- `reports/v5_review_label_sensitivity.md`
- `results/analysis/v5_review_label_sensitivity_summary.csv`

Key result:

- Unreviewed rows and reviewed non-bad rows both show reviewed Banglish below
  native Bangla for Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B.
- The three bad rows remain a denominator-sensitivity issue, not a stable
  review-label stratum.

## Frozen-V5 Dataset-Gap Intervals

The dataset-level interval pass adds paired bootstrap intervals to the
Chapter 4 BEnQA/BanglaMATH split without launching new model jobs.

Artifacts:

- `scripts/analyze_v5_dataset_gap_intervals.py`
- `reports/v5_dataset_gap_intervals.md`
- `results/analysis/v5_dataset_gap_intervals.csv`
- `scripts/analyze_v5_paired_sign_tests.py`
- `reports/v5_paired_sign_tests.md`
- `results/analysis/v5_paired_sign_tests.csv`
- `scripts/analyze_v5_clustered_gap_robustness.py`
- `reports/v5_clustered_gap_robustness.md`
- `results/analysis/v5_clustered_gap_clusters.csv`
- `results/analysis/v5_clustered_gap_summary.csv`

Key result:

- BEnQA is the clearest dataset-level source of the reviewed-v5 gap. Qwen3-4B
  BEnQA reviewed-Banglish-minus-Bangla is -20.1 points, CI [-28.5, -11.8].
- Qwen2.5-3B and Qwen2.5-7B 8-bit are directionally negative on BEnQA but
  their dataset-only intervals reach zero.
- BanglaMATH remains a low-accuracy stress test rather than the best source
  for fine-grained dataset-level script-gap claims.
- Exact paired sign tests show all-200 Banglish-vs-Bangla discordant pairs are
  asymmetric for Qwen2.5-7B 8-bit (19 gains, 37 losses, p=0.0222) and
  Qwen3-4B (8 gains, 39 losses, p<0.0001). Qwen2.5-3B remains weaker at
  15 gains versus 28 losses, p=0.0660.
- Clustered robustness resampling BEnQA subjects and BanglaMATH grades keeps
  Qwen2.5-7B 8-bit and Qwen3-4B all-200 Banglish-minus-Bangla intervals below
  zero. Qwen2.5-3B remains directionally negative but reaches zero, matching
  the existing all-200 qualification.
- Subject-macro BEnQA balancing equal-weights the 13 BEnQA subjects and keeps
  reviewed Banglish below Bangla for all three Qwen rows. Qwen3 is -20.2 pts
  with CI [-28.6,-11.2], Qwen2.5-7B is -9.2 pts [-16.8,-1.6], and
  Qwen2.5-3B remains the qualified row at -5.3 pts [-15.2,+4.2].

## Frozen-V5 BEnQA Subject Stability

The BEnQA stability pass checks whether the dataset-level gap is driven by a
single subject stratum. It recomputes the reviewed-Banglish-minus-Bangla count
after dropping each BEnQA subject in turn.

Artifacts:

- `scripts/analyze_v5_benqa_subject_stability.py`
- `reports/v5_benqa_subject_stability.md`
- `results/analysis/v5_benqa_subject_stability.csv`

Key result:

- All 13 leave-one-subject drops remain negative for Qwen2.5-3B,
  Qwen2.5-7B 8-bit, and Qwen3-4B.
- Qwen3-4B has the strongest stability range: -23.3 to -18.0 points.
- This supports the BEnQA interpretation without turning the small subject
  strata into standalone inferential claims.

## Frozen-V5 Subject/Grade Breakdown

The stale subject-spread report was refreshed against the frozen-v5 reviewed
Banglish outputs used in the release-facing main table, with Bangla and English
outputs reused because those fields did not change.

Artifacts:

- `scripts/build_v5_subject_breakdown.py`
- `reports/subject_breakdown_validation200_v5.md`
- `results/analysis/validation200_v5_subject_breakdown.csv`
- `results/tables/subject_breakdown_validation200_v5.csv`

Key results:

- The builder validates 1,800 model-item-variant rows and 48 summary strata.
- Qwen3-4B reviewed Banglish is below Bangla in 12/13 BEnQA subject strata.
- Qwen2.5-7B 8-bit is below Bangla in 8/13 BEnQA strata.
- Qwen2.5-3B is more mixed at 7/13 BEnQA strata.
- BanglaMATH grade strata remain low-accuracy and should stay stress-test
  evidence rather than fine-grained grade claims.

## Frozen-V5 Answer-Format Audit

The answer-format pass checks whether parser-empty outputs or invalid MCQ
formatting could explain the release-facing script gap.

Artifacts:

- `scripts/analyze_v5_answer_format_audit.py`
- `reports/v5_answer_format_audit.md`
- `results/analysis/v5_answer_format_audit_summary.csv`
- `results/analysis/v5_answer_format_audit_items.csv`

Key result:

- The audit covers 1,800 thesis-facing outputs and 27 summary rows.
- Qwen2.5-3B has 0 format failures; Qwen2.5-7B 8-bit has 2 reviewed-Banglish
  BEnQA format failures, but crediting both still leaves a -8.0 point all-200
  Banglish-Bangla gap.
- Qwen3-4B has more BEnQA format failures in English and Bangla than in
  reviewed Banglish, so its gap is not a Banglish-specific parser artifact.

## Frozen-V5 BEnQA Subject Option-Bias Audit

The subject option-bias pass checks whether Qwen3's BEnQA D-attractor is
localized to one subject cluster.

Artifacts:

- `scripts/analyze_v5_benqa_subject_option_bias.py`
- `reports/v5_benqa_subject_option_bias.md`
- `results/analysis/v5_benqa_subject_option_bias_summary.csv`
- `results/analysis/v5_benqa_subject_option_bias_items.csv`

Key result:

- Qwen3-4B reviewed Banglish has majority-D predictions in 12/13 BEnQA
  subjects.
- The same check is 1/13 for Qwen2.5-3B and 0/13 for Qwen2.5-7B 8-bit.
- No subject has gold-D share above 45.5%, so the broad D-attractor is not a
  single-subject gold-label artifact.

## Frozen-V5 BEnQA Option Position/Content Audit

The option position/content pass checks whether Qwen3's D-attractor is only
because D is often the longest reviewed-Banglish option.

Artifacts:

- `scripts/analyze_v5_benqa_option_position_content.py`
- `reports/v5_benqa_option_position_content.md`
- `results/analysis/v5_benqa_option_position_content_summary.csv`
- `results/analysis/v5_benqa_option_position_content_items.csv`

Key result:

- D is tied for longest on 98/144 BEnQA items, so length is a real confound.
- Qwen3-4B still predicts D on 30/46 rows where D is not longest, compared
  with 9/46 and 5/46 for the two Qwen2.5 rows.

## Frozen-V5 BEnQA Option-Switching Audit

The option-switching pass checks whether reviewed-Banglish BEnQA predictions
preserve the model's Bangla/English option choices or instead move toward D.

Artifacts:

- `scripts/analyze_v5_benqa_option_switching.py`
- `reports/v5_benqa_option_switching.md`
- `results/analysis/v5_benqa_option_switching_summary.csv`
- `results/analysis/v5_benqa_option_switching_items.csv`

Key result:

- Qwen3-4B converts valid non-D Bangla predictions to D in reviewed Banglish on
  47/73 rows, and converts valid non-D English predictions to D on 55/78 rows.
- Among correct non-D alternate-script predictions, those become wrong-D
  reviewed-Banglish choices on 30/44 Bangla rows and 37/54 English rows.
- The Qwen2.5 Bangla-side non-D-to-D rates are much smaller: 14/99 for
  Qwen2.5-3B and 17/126 for Qwen2.5-7B 8-bit.

Interpretation: Qwen3's reviewed-Banglish D-attractor is not only an aggregate
label-frequency artifact. It is a directional option-switching failure relative
to the same model's Bangla and English choices.

## Frozen-V5 BEnQA Option-Switch Confound Audit

The switch-confound pass joins option switching with option position/content
features to check whether the directional Qwen3 switch survives stricter
controls for D being the longest option and gold-D rows.

Artifacts:

- `scripts/analyze_v5_benqa_option_switch_confound.py`
- `reports/v5_benqa_option_switch_confound.md`
- `results/analysis/v5_benqa_option_switch_confound_summary.csv`
- `results/analysis/v5_benqa_option_switch_confound_items.csv`

Key result:

- When the alternate-script prediction is correct, non-D, and D is not longest,
  Qwen3 still switches to wrong reviewed-Banglish D on 11/19 Bangla rows and
  12/21 English rows.
- In the broader non-D, gold-not-D, D-not-longest scope, Qwen3 switches to D on
  13/25 Bangla rows and 15/26 English rows.
- The corresponding correct-non-D and D-not-longest Bangla-side counts for
  Qwen2.5 rows are only 1/13 and 2/22.

Interpretation: D length and gold-D distribution are real confounds, but they
do not explain away the Qwen3 reviewed-Banglish D-attractor.

## Frozen-V5 Response-Style Drift Audit

The response-style pass checks whether script choice changes raw answer
behavior, not only parsed correctness.

Artifacts:

- `scripts/analyze_v5_response_style_drift.py`
- `reports/v5_response_style_drift.md`
- `results/analysis/v5_response_style_drift_summary.csv`
- `results/analysis/v5_response_style_drift_items.csv`

Key result:

- Qwen3-4B BanglaMATH reviewed Banglish has 15/56 meta/uncertainty outputs
  versus 0/56 Bangla and 1/56 English.
- Qwen2.5 rows do not show the same BanglaMATH meta pattern, so this is a
  model-specific short-answer behavior drift rather than a global mechanism.

## Frozen-V5 BanglaMATH Numeric Sensitivity

The numeric-sensitivity pass checks whether conservative short-answer
normalization could explain BanglaMATH losses.

Artifacts:

- `scripts/analyze_v5_banglamath_numeric_sensitivity.py`
- `reports/v5_banglamath_numeric_sensitivity.md`
- `results/analysis/v5_banglamath_numeric_sensitivity_summary.csv`
- `results/analysis/v5_banglamath_numeric_sensitivity_items.csv`

Key result:

- Generous raw numeric-signature credit still leaves reviewed Banglish below
  Bangla and English for all three Qwen rows.
- Qwen3-4B raw numeric-signature hits are 10/56 for reviewed Banglish,
  compared with 19/56 Bangla and 24/56 English.

## Frozen-V5 Real-Banglish Distribution Refresh

The real-Banglish comparison now uses the frozen validation-200 v5 Banglish
slice rather than the older v4 fields.

Artifacts:

- `scripts/compare_banglish_distributions.py`
- `reports/real_banglish_distribution_comparison.md`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_items.csv`

Key result:

- Validation-200 v5 content-only Banglish averages 86.2 characters and has
  digits in 54.5% of rows.
- BanglaTLit val/test rows average about 56-57 characters and have digits in
  about 18% of rows.
- This keeps the naturalness limitation tied to the final frozen slice:
  validation-200 v5 is controlled educational Banglish, not a natural-user
  Banglish benchmark.

## Frozen-V5 Tokenization/Failure Join

The mechanism evidence was refreshed from historical v3 diagnostics to the
frozen-v5 reviewed Banglish slice.

Artifacts:

- `scripts/build_v5_tokenization_failure_patterns.py`
- `reports/tokenization_cross_script_failure_patterns.md`
- `reports/tokenization_validation200.md`
- `results/tokenization/validation200_v5/audit.csv`
- `results/tokenization/validation200_v5/summary.csv`
- `results/analysis/validation200_v5_cross_script_token_patterns_items.csv`
- `results/analysis/validation200_v5_cross_script_token_patterns_summary.csv`

Key results:

- The join validates 600 model-item rows and 78 summary rows.
- Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B tokenizers produce identical
  item-level counts for all 600 item/variant pairs.
- Reviewed Banglish is token-cheaper than Bangla: BEnQA 2.4942 vs 4.0242
  tokens/word; BanglaMATH 2.1114 vs 4.6285.
- Recoverable BEnQA Banglish misses are shorter in Banglish token count than
  non-recoverable/other rows for all three thesis-facing Qwen models.
- The strict `bangla_english_correct_banglish_wrong` pattern remains
  token-cheaper in reviewed Banglish than native Bangla.

## Completed Kaggle Jobs

Both jobs use 36 BEnQA MCQ dev items and variants:

- `banglish_clean`
- `generated_bn_phonetic_protected_v2`
- `generated_bn_bnb_protected_v2`

Kernels and local outputs:

- Qwen3-4B:
  `munimthahmid/qwen3-4b-generated-bn-v5-protected-v2-dev50`
  - `results/runs/qwen3_4b_generated_bn_v5_pv2_dev50/`
  - `reports/qwen3_4b_generated_bn_v5_pv2_dev50.md`
- Qwen2.5-3B:
  `munimthahmid3/qwen2-5-3b-generated-bn-v5-protected-v2-dev50`
  - `results/runs/qwen25_3b_generated_bn_v5_pv2_dev50/`
  - `reports/qwen25_3b_generated_bn_v5_pv2_dev50.md`

All-row dev answer audit:

- Qwen3-4B: Banglish 15/36, phonetic-v2 13/36, BNB-v2 16/36.
- Qwen2.5-3B: Banglish 9/36, phonetic-v2 10/36, BNB-v2 8/36.

Gate-eligible rows only:

- Qwen3-4B: phonetic-v2 9/20 vs Banglish 10/20; BNB-v2 11/20 vs
  Banglish 10/20.
- Qwen2.5-3B: phonetic-v2 5/20 vs Banglish 5/20; BNB-v2 6/20 vs
  Banglish 5/20.

Decision:

- Do not launch generated-view test150 under protected-v2 or FMS-byte
  generators.
- Protected-v3 plus guarded generated-English still does not justify held-out
  routing; pause until a better generated-English source avoids source fallback
  and produces a stronger dev agreement route.

## QA

`python3 scripts/run_research_checks.py` passed after adding the reviewed-v5
generated-view gates, guarded generated-English repair, and guarded agreement
route regeneration. Later no-spend passes added API-audit importer round-trip
validation and the reviewed-v5 fragility feature analysis before any paid
calls. The latest pass also covers the v5 token/failure join, model-overlap
analysis, item-consensus, consensus-stability, and composition-sensitivity
audits, shared-fragility qualitative examples,
review-label sensitivity, dataset-gap intervals, BEnQA subject stability,
real-Banglish distribution, and subject/grade breakdown.

- Thesis table integrity: 70 checks, 0 issues.
- Thesis figure integrity: 25 checks, 0 issues.
- v5 packet integrity: 6 checks, 0 issues.
- v5 recoverability source decomposition: 600 item rows, 300 summary rows.
- v5 cross-script transfer retention: 600 item rows, 36 summary rows.
- v5 clustered gap robustness: 192 cluster rows, 18 summary rows.
- v5 Banglish fragility feature analysis: 200 items, 185/600 fragility events.
- v5 Qwen scaling-transfer audit: 1,800 transition rows, 63 summary rows.
- v5 fragility model overlap: 200 items, 56/108 any-fragile items shared by
  at least two models.
- v5 item consensus: 200 item rows, 80 summary rows.
- v5 difficulty-conditioned gap: 200 item rows, 36 summary rows.
- v5 consensus stability: 1,400 item rows, 21 summary rows.
- v5 composition sensitivity: 200 item rows, 27 summary rows.
- v5 shared-fragility examples: 17 rows, 5 all-three strict examples.
- v5 review-label sensitivity: 39 summary rows.
- v5 dataset gap intervals: 18 summary rows.
- v5 paired sign tests: 18 summary rows.
- v5 BEnQA subject stability: 42 summary rows, all 39 leave-one-subject drops
  negative.
- v5 BEnQA subject-macro balance: 39 subject rows, 6 summary rows.
- v5 answer-format audit: 1,800 item rows, 27 summary rows.
- v5 response-style drift audit: 1,800 item rows, 27 summary rows.
- v5 BanglaMATH numeric sensitivity: 504 item rows, 9 summary rows.
- v5 BEnQA subject option-bias audit: 1,296 item rows, 117 summary rows.
- v5 BEnQA option position/content audit: 432 item rows, 4 summary rows.
- v5 BEnQA option-switching audit: 864 item rows, 36 summary rows.
- v5 BEnQA option-switch confound audit: 864 item rows, 36 summary rows.
- v5 BEnQA choice-bias audit: 432 item rows, 18 summary rows.
- v5 BEnQA distractor-transition audit: 432 item rows, 144 consensus rows,
  20 summary rows.
- v5 BEnQA label-balance sensitivity: 36 by-label rows, 24 summary rows.
- v5 token/failure join: 600 joined rows, 78 summary rows.
- real-Banglish v5 distribution: 4 summary rows, 4,400 item rows.
- v5 BanglaTLit lexical coverage: 200 item rows, 15 summary rows.
- v5 BEnQA option lexical coverage: 144 item rows, 15 summary rows.
- v5 BanglaTLit model-coverage sensitivity: 600 item rows, 45 summary rows.
- v5 BanglaTLit spelling-variation sensitivity: 600 item rows, 45 summary rows.
- v5 source-variant structural parity: 600 pair rows, 15 summary rows, 0
  primary hard fails.
- v5 English-warning sensitivity: 600 item rows, 27 summary rows; clean-English
  subset direction remains negative for all three Qwen rows.
- v5 review edit-distance sensitivity: 600 item rows, 45 summary rows;
  no-applied-change subset direction remains negative for all three Qwen rows.
- Research log compactness: 55 checks, 0 issues; 235 lines and 12.8 KB.
- API audit manifest integrity: 18 checks, 0 issues.
- API audit import round-trip: 16 checks, 0 issues; 30/30 temporary mock
  responses imported and parsed correct.
- Literature corpus and citation readiness: 33/33 complete.
- Secret hygiene: 860 files checked, 0 suspicious findings.
- Local artifact references: 3,778 checked, 0 unexpected missing.
- Reproducibility manifest: 858 artifacts.
