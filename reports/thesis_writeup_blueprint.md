# Thesis Write-Up Blueprint

Updated: 2026-06-03

## Working Thesis

Script choice is a real robustness variable for Bangla LLM use. For competent
Qwen models, the same Bangla content becomes substantially harder when written
as clean Latin-script Banglish than when written in native Bengali script.
Across several compact open models, Banglish is also much harder than English
despite using Latin characters. Mitigation is model-dependent: simple prompts
do not solve the gap, and same-model self-normalization helps Qwen2.5-3B,
fails to scale cleanly to Qwen2.5-7B, and hurts Qwen3. Cross-script answer
agreement is a strong diagnostic mitigation signal, but the deployable version
must use generated alternate-script views with preservation checks.

## Chapter 1: Introduction

Purpose:

- Motivate Banglish as a real user script, not a niche artifact.
- State the practical risk: systems evaluated only on native Bangla or English
  can fail on common Latin-script Bangla input.
- Present the thesis as benchmark plus analysis plus mitigation.

Core claims to introduce:

- Controlled script changes can change accuracy substantially.
- Token count alone does not explain the gap.
- Mitigation requires explicit reliability checks.

Current draft:

- `reports/chapter_1_introduction_draft.md`

## Chapter 2: Related Work

Sections:

- Bangla and multilingual QA/math benchmarks: BEnQA, BanglaMATH, MGSM, BnMMLU,
  BLUCK.
- Romanization and transliteration robustness: Bangla transliteration
  perturbation work, BanglaTLit, RomanLens.
- English-centric and script-sensitive multilingual processing.
- Mitigation approaches: prompting, normalization, translation, routing,
  adaptation.

Main differentiation:

- Prior work studies partial transliteration perturbations or latent
  romanization. This thesis studies full native Bangla vs full clean Banglish
  vs noisy Banglish vs English controls on downstream QA/reasoning, with
  mitigation and item-level failure analysis.

Current draft:

- `reports/chapter_2_related_work_draft.md`

## Chapter 3: Benchmark Construction

Tables:

- Dataset composition: BEnQA, BanglaMATH, MGSM.
- Script variants: Bangla, clean Banglish, noisy Banglish, English.
- Validation slices: validation-100 v3, validation-200 v3, validation-200 v4,
  dev50/test150.

Key artifacts:

- `results/tables/thesis_tables.md`
- `reports/thesis_figures_and_tables_plan.md`
- `reports/reproducibility_release_checklist.md`
- `reports/reproducibility_artifact_manifest.md`
- `data/slices/validation_200_v3.jsonl`
- `data/slices/validation_200_v4.jsonl`
- `data/slices/validation_200_v4_dev50.jsonl`
- `data/slices/validation_200_v4_test150.jsonl`
- `data/slices/validation_200_v5.jsonl`
- `data/slices/validation_200_v5.manifest.json`
- `reports/banglish_quality_v4_plan.md`
- `reports/banglish_human_review_packet_v2.md`
- `reports/validation200_v5_review_queue.md`
- `data/slices/validation_200_v5_review_queue.csv`
- `reports/v5_analysis_preregistration.md`
- `reports/real_banglish_distribution_comparison.md`
- `reports/v5_benqa_option_lexical_coverage.md`
- `reports/v5_banglatlit_model_coverage_sensitivity.md`
- `reports/v5_review_edit_distance_sensitivity.md`

Must state clearly:

- v4 Banglish is the rule-based predecessor used for historical sensitivity.
- Frozen v5 is the reviewed controlled benchmark: 140/140 queued rows reviewed,
  126 `minor_edit`, 11 `major_edit`, 3 `bad`, and 0 pending.
- The all-200 policy keeps flagged bad rows in the main denominator.
- Reviewed v5 still does not make the benchmark a sample of natural user
  conversations.
- BnSentMix external validation should be used as a separate natural
  code-mixed sentiment task: Qwen2.5-3B 89/200, Qwen2.5-7B 8-bit 98/200,
  Qwen3-4B 99/200, and 600/600 valid labels. Do not merge this with the paired
  script-gap estimate. The complementarity audit adds that the best single row
  is 99/200 but the any-model diagnostic oracle is 154/200, showing diverse
  natural-task errors. The routing dev-test audit is the deployability caveat:
  majority + Qwen2.5-7B fallback reaches 106/200 under hash5 CV, but block40 CV
  drops to 84/200, so it is not a locked mitigation.
- BanglaTLit comparison should be used to show how controlled clean Banglish
  differs from naturally written Romanized Bangla.
- BEnQA option lexical coverage should be used to state that answer options
  are especially low-coverage versus BanglaTLit, while high-coverage option
  buckets still have negative point gaps.
- BanglaTLit model-coverage sensitivity should be used to state that every
  all-200 coverage quartile keeps reviewed Banglish below Bangla/English for
  each thesis-facing Qwen row.
- BanglaTLit spelling-variation sensitivity should be used to state that the
  highest all-200 repeated-variant-exposure quartile keeps reviewed Banglish
  below Bangla/English for each Qwen row, while the lowest bucket has a
  Qwen2.5-3B tie.
- Source-variant parity should be used to state that the primary
  Bangla-vs-reviewed-Banglish pair has 0/200 structural mismatches, while
  English comparisons retain 39/200 diagnostic source-translation warnings.
- English-warning sensitivity should be used to state that the 161 clean-English
  subset still keeps reviewed Banglish below Bangla/English for all three Qwen
  rows, with 50/58/51 recoverable Banglish misses.
- Review edit-distance sensitivity should be used to state that the 63
  no-applied-change rows already keep reviewed Banglish below Bangla/English
  for all three Qwen rows; larger-edit rows are only 19 items.
- The reproducibility manifest excludes secret credentials and should be
  regenerated after any thesis-table update.

Current draft:

- `reports/chapter_3_benchmark_construction_draft.md`

## Chapter 4: Main Script-Gap Results

Primary table:

| Model | Bangla | Reviewed Banglish | English | Banglish - Bangla | Banglish - English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] |
| Qwen3-4B | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] |

The Qwen2.5-3B reviewed all-200 Banglish-Bangla interval reaches zero. Keep its
historical v3 estimate and strict-197 sensitivity as supporting evidence rather
than claiming every reviewed all-200 interval is negative.

Supporting tables:

- Reviewed-v5 dataset split BEnQA vs BanglaMATH.
- Dataset-level paired intervals: BEnQA is the clearest source of the
  reviewed-v5 gap, while BanglaMATH remains a low-accuracy stress test.
- BEnQA leave-one-subject stability: every one-subject drop keeps the
  reviewed-Banglish-minus-Bangla delta negative for each thesis-facing Qwen row.
- BEnQA subject-macro balance: equal-weighting the 13 subjects keeps Qwen3 and
  Qwen2.5-7B below zero with subject-bootstrap intervals below zero, while
  Qwen2.5-3B remains the qualified row.
- Answer-format audit: parser-empty and MCQ-format failures do not drive the
  release-facing Banglish deficit.
- Reviewed-v5 subject spread for BEnQA.
- Paired bootstrap uncertainty.

Key artifacts:

- `results/tables/main_script_gap_validation200_v5.csv`
- `reports/main_results_validation200_v5.md`
- `results/tables/main_script_gap_validation200.csv`
- `reports/main_results_validation200.md`
- `reports/v5_dataset_gap_intervals.md`
- `reports/v5_benqa_subject_stability.md`
- `reports/v5_benqa_subject_balance.md`
- `reports/v5_answer_format_audit.md`
- `reports/subject_breakdown_validation200_v5.md`
- `results/tables/subject_breakdown_validation200_v5.csv`
- `results/analysis/qwen25_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen3_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `reports/chapter_4_main_results_draft.md`

## Chapter 5: Robustness and Model Breadth

Sections:

- Noisy Banglish: current deterministic noise does not explain the main gap.
- v4 cleanup: targeted romanizer cleanup does not remove the gap.
- Frozen v5 review: reviewed cleanup does not materially alter the gap.
- Review-label sensitivity: unreviewed and reviewed non-bad v5 buckets both
  retain the Banglish-below-Bangla deficit for the main Qwen rows.
- Review edit-distance sensitivity: no-applied-change rows already retain the
  Banglish-below-Bangla/Banglish-below-English direction for the main Qwen rows.
- Flagged-bad policy: a separate strict-197 view preserves negative
  reviewed-Banglish-vs-Bangla confidence intervals for all three main Qwen rows.
- Model scaling: weak models do not always show Banglish below Bangla.
- Scaling-transfer audit: Qwen2.5 3B->7B gains 11 Bangla and 23 English items,
  but only 6 reviewed-Banglish items; Qwen2.5-3B->Qwen3-4B gains 26 Bangla,
  17 English, and 8 reviewed-Banglish items.
- Model-family breadth: Phi-3.5-mini shows large Banglish-vs-English gap but
  no Banglish-below-Bangla gap.
- Bangla/Indic-specialized models: BanglaLLM and TituLM are prompt/runtime
  diagnostics, not valid baselines; Indic-Gemma-2B follows the Alpaca-wrapped
  protocol but is around chance on pilot20.
- Larger-model feasibility: Qwen3-8B is blocked on P100; Mistral-7B 8-bit is
  feasible but weak and slow on pilot20.

Main interpretation:

- Banglish-vs-English gap is broad across compact open models.
- Banglish-below-Bangla should be anchored in competent Qwen models, not claimed
  as universal.

Key artifacts:

- `results/tables/model_family_scaling_validation200.csv`
- `reports/noisy_banglish_validation200.md`
- `reports/v4_banglish_sensitivity_validation200.md`
- `reports/v5_bad_row_policy_sensitivity.md`
- `reports/v5_review_label_sensitivity.md`
- `reports/v5_review_edit_distance_sensitivity.md`
- `reports/v5_qwen_scaling_transfer.md`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/phi35_mini_validation200_v4.md`
- `reports/qwen3_1_7b_nothink_validation200_v4.md`
- `reports/bangla_specialized_model_pilots.md`
- `reports/qwen3_8b_8bit_pilot20_failure.md`
- `reports/mistral7b_8bit_pilot20_validation200_v4.md`
- `reports/indic_gemma2b_pilot20_validation200_v4.md`
- `reports/kaggle_gpu_feasibility_notes.md`
- `reports/chapter_5_robustness_and_model_breadth_draft.md`

New stronger Qwen2.5 point:

- Qwen2.5-7B 8-bit:
  `reports/qwen25_7b_8bit_validation200_v4.md`.
- Full200: Bangla 65/200, Banglish 48/200, English 94/200.
- Banglish minus Bangla: -8.5 points, CI [-15.5, -1.5].

## Chapter 6: Why The Gap Is Not Just Item Difficulty

Provenance note:

- Oracle, taxonomy, and agreement analyses use frozen-v5 reviewed Banglish.
  Bangla and English outputs are reused because those fields did not change.

Sections:

- Cross-script oracle.
- Failure taxonomy.
- Cross-script transfer retention.
- Difficulty-conditioned consensus buckets.
- Paired sign-test robustness.
- Clustered gap robustness.
- Recoverability source decomposition.
- Feature concentration by domain and prompt attributes.
- Example packet.

Core evidence:

| Model | Any-script oracle | Banglish only | Banglish misses correct under Bangla/English |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 99/200 | 41/200 | 58/200 |
| Qwen2.5-7B 8-bit | 115/200 | 47/200 | 68/200 |
| Qwen3-4B | 108/200 | 49/200 | 59/200 |

Strongest item-level pattern:

- Qwen3-4B has 32/200 items where Bangla and English are correct but reviewed
  Banglish is wrong.
- 30/144 of those are BEnQA.
- Paired sign tests: all-200 Banglish-vs-Bangla discordant pairs are
  asymmetric for Qwen2.5-7B (19 gains, 37 losses, p=0.0222) and Qwen3-4B
  (8 gains, 39 losses, p<0.0001); Qwen2.5-3B remains the qualified weaker row
  at 15 gains versus 28 losses, p=0.0660.
- Clustered gap robustness: resampling BEnQA subjects and BanglaMATH grades
  keeps Qwen2.5-7B 8-bit and Qwen3-4B all-200 Banglish-minus-Bangla intervals
  below zero; Qwen2.5-3B remains the qualified row whose interval reaches zero.
- Across the three thesis-facing Qwen rows, 185/600 model-item slots are
  Banglish-fragile: reviewed Banglish is wrong while Bangla or English is
  correct. BEnQA MCQ rows account for 164/432 of these events, versus 21/168
  for BanglaMATH short-answer rows.
- Source decomposition: 185/463 reviewed-Banglish misses are recoverable by
  Bangla or English, while 278/463 are all-script hard. Native Bangla
  participates in 104/185 recoverable misses, English in 157/185, and both
  alternate scripts recover 76/185.
- Transfer retention: conditioning on same-model correctness in Bangla or
  English, reviewed Banglish stays correct only 34/92, 39/107, and 44/103
  times for Qwen2.5-3B, Qwen2.5-7B, and Qwen3 respectively.
- Model-overlap analysis separates shared Qwen-family fragility from
  one-model quirks: 56/108 any-fragile items affect at least two thesis-facing
  Qwen rows, while 52 affect exactly one.
- Item-consensus audit: reviewed Banglish has 137/600 correct model-item slots,
  compared with 199/600 for Bangla and 253/600 for English. BEnQA has 61/144
  items with at least two-model support in Bangla or English and at most one
  correct reviewed-Banglish model.
- Difficulty-conditioned gap: in all-200 items where all three Qwen rows
  answer English correctly, reviewed Banglish has 50/147 correct slots versus
  Bangla's 92/147; in the English-consensus=2 bucket it is 36/108 versus 49/108.
- Leave-one-model-out consensus stability: every two-model Qwen subset keeps
  reviewed Banglish below both Bangla and English on all-200 and BEnQA.
- Composition sensitivity: no-digit and no-formula/operator subsets keep
  reviewed Banglish below Bangla and English for all three Qwen rows.
- BEnQA choice-bias audit: Qwen2.5 Banglish outputs do not collapse to one
  option label; Qwen3 Banglish over-selects D on 111/144 rows.
- BEnQA prediction diversity: Qwen3 reviewed Banglish drops to 0.502
  normalized entropy and 2.01 effective options; Qwen2.5 reviewed Banglish
  stays at 3.75/3.77 effective options.
- BEnQA distractor-transition audit: 162/164 recoverable Banglish BEnQA misses
  are valid distractor choices, and 27/50 two-plus recoverable items share a
  wrong option across models.
- BEnQA label-balance sensitivity: gold-label-balanced and non-D slices keep
  reviewed Banglish below Bangla/English; Qwen3 is -21.7 pts vs Bangla
  balanced and -29.5 pts on non-D.
- BEnQA subject option-bias: Qwen3 reviewed Banglish has majority-D
  predictions in 12/13 subjects; Qwen2.5 rows have 1/13 and 0/13.
- BEnQA option position/content: D is longest on 98/144 items, but Qwen3 still
  predicts D on 30/46 rows where D is not longest.
- BEnQA option-switching: Qwen3 converts valid non-D Bangla/English choices to
  D in reviewed Banglish on 47/73 and 55/78 rows.
- BEnQA cross-script option agreement: when Qwen3 Bangla and English both
  correctly agree on the same non-D option, reviewed Banglish still switches
  to wrong D on 23/36 rows.
- BEnQA cross-model Banglish agreement: when both Qwen2.5 rows agree on non-D
  reviewed Banglish, Qwen3 predicts D on 26/42 rows and wrong D on 18/42; in
  the both-correct non-D slice Qwen3 is wrong-D on 8/15.
- BEnQA order-confound audit: Qwen3 predicts D by reviewed-Banglish output-line
  quartile on 26/36, 31/36, 28/36, and 26/36 rows; the first and last quartiles
  are both high, so this is not a simple late-run artifact.
- BEnQA review-label option bias: Qwen3 predicts D on 39/51 unreviewed rows and
  69/90 reviewed nonbad rows; Qwen2.5 rows are much lower in both buckets.
- BEnQA length/token confound: Qwen3 predicts D by reviewed-Banglish HF-token
  quartile on 32/36, 26/36, 27/36, and 26/36 rows, so the collapse is not a
  longest-token-burden artifact.
- BEnQA option-coverage confound: when all four options have tied exact
  BanglaTLit lexical coverage, Qwen3 still predicts D on 76/101 rows while
  Qwen2.5 rows predict D on 14/101 and 8/101.
- BEnQA option-switch confound: when D is not longest, Qwen3 still turns
  correct non-D Bangla/English choices into wrong D on 11/19 and 12/21 rows.
- BEnQA option semantic cues: Qwen3 still predicts D on 38/47 rows where D has
  no composite/numeric/formula cue; Qwen2.5 rows are 9/47 and 4/47.
- BEnQA multi-confound residual: after combining gold-not-D, D-not-longest,
  no-simple-D-cue, and tied-coverage controls, Qwen3 remains wrong-D on 16/20
  rows while Qwen2.5 rows are 4/20 and 1/20.
- BEnQA option-permutation dev probe: rotating semantic option content through
  A/B/C/D keeps Qwen3 identity wrong-D rows attached to literal label D on
  35/45 rotations, while only 6/45 follow original-D content. Qwen2.5-3B
  trends the other way at 5/21 versus 12/21. Use as dev-only behavioral
  evidence for a Qwen3 label-position D-attractor, not as internal causal proof.
- Response-style drift: Qwen3 BanglaMATH reviewed Banglish has 15/56
  meta/uncertainty outputs versus 0 Bangla and 1 English; frame as
  model-specific short-answer behavior drift.
- BanglaMATH numeric sensitivity: generous raw numeric-signature credit still
  leaves reviewed Banglish below Bangla/English for all three Qwen rows; Qwen3
  is 10/56 vs 19/56 Bangla and 24/56 English.
- BanglaMATH numeric transfer: Qwen3 has alternate-script raw numeric signatures
  on 24/56 items; reviewed Banglish retains 8/24 and is correct on 2/24, with
  9/24 meta outputs in that slice.

Key artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/v5_cross_script_transfer.md`
- `reports/v5_paired_sign_tests.md`
- `reports/v5_clustered_gap_robustness.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_banglish_fragility_feature_analysis.md`
- `reports/v5_banglish_fragility_model_overlap.md`
- `reports/v5_item_consensus.md`
- `reports/v5_difficulty_conditioned_gap.md`
- `reports/v5_consensus_stability.md`
- `reports/v5_composition_sensitivity.md`
- `reports/v5_response_style_drift.md`
- `reports/v5_banglamath_numeric_sensitivity.md`
- `reports/v5_banglamath_numeric_transfer.md`
- `reports/v5_benqa_choice_bias.md`
- `reports/v5_benqa_prediction_diversity.md`
- `reports/v5_benqa_subject_option_bias.md`
- `reports/v5_benqa_option_position_content.md`
- `reports/v5_benqa_option_switching.md`
- `reports/v5_benqa_cross_script_option_agreement.md`
- `reports/v5_benqa_cross_model_banglish_agreement.md`
- `reports/v5_benqa_order_confound.md`
- `reports/v5_benqa_review_label_option_bias.md`
- `reports/v5_benqa_length_token_confound.md`
- `reports/v5_benqa_option_coverage_confound.md`
- `reports/v5_benqa_option_switch_confound.md`
- `reports/v5_benqa_option_semantic_cues.md`
- `reports/v5_benqa_multiconfound_residual.md`
- `reports/v5_benqa_option_permutation_probe_results.md`
- `reports/v5_benqa_label_balance.md`
- `reports/v5_shared_fragility_examples.md`
- `reports/thesis_qualitative_examples.md`
- `reports/chapter_6_failure_analysis_draft.md`

## Chapter 7: Tokenization and Mechanism

Current evidence:

- Frozen-v5 Qwen tokenization audits encode reviewed Banglish more cheaply than
  native Bangla.
- Despite lower token cost, Banglish accuracy is lower than Bangla for the main
  Qwen runs.
- Cross-script Banglish failures that are recoverable under Bangla or English
  are not the long Banglish prompts; in BEnQA, they are shorter on average than
  non-recoverable/other items for Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B.

Thesis-safe conclusion:

- Token count alone is not sufficient as an explanation.

Optional extension:

- Add representation similarity or logit-lens analysis on a smaller selected
  subset after the benchmark story is stable.

Key artifact:

- `reports/tokenization_validation200.md`
- `reports/tokenization_cross_script_failure_patterns.md`
- `reports/chapter_7_tokenization_mechanism_draft.md`

## Defense Prep

Use `reports/thesis_defense_qna.md` as the rehearsal file. It gives concise
answers for expected questions about novelty, dataset naturalness, Qwen scope,
tokenization, mitigation, frontier API timing, and frozen-v5 evidence.

## Chapter 8: Mitigation

Provenance note:

- Validation-200 mitigation rows intentionally retain historical v3/v4
  baseline outputs. They diagnose mitigation behavior rather than report
  reviewed-v5 main-result reruns.

Main table:

| Model | Baseline Banglish | Self-normalized | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +6.5 pts, CI [+0.5, +13] |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-7, +6.5] |
| Qwen3-4B | 46/200 | 21/200 | -12.5 pts, CI [-19.5, -5.5] |

Routing result:

| Model | Dev-selected rule | Test baseline | Test selected |
| --- | --- | ---: | ---: |
| Qwen2.5-3B | selfnorm if options preserved | 31/150 | 41/150 |
| Qwen3-4B | selfnorm if BanglaMATH | 32/150 | 34/150 |

Exploratory answer-signal routing:

| Model | Candidate rule | Test baseline | Test routed |
| --- | --- | ---: | ---: |
| Qwen2.5-3B | selfnorm if parsed answer non-empty | 31/150 | 43/150, CI delta [+0.7, +15.3] |
| Qwen3-4B | selfnorm if parsed answer non-empty | 32/150 | 40/150, CI delta [+1.3, +10.0] |

Dataset note:

- The routed gain appears in both BEnQA and BanglaMATH on test150:
  Qwen2.5 gains +8 BEnQA and +4 BanglaMATH; Qwen3 gains +6 BEnQA and +2
  BanglaMATH.

Interpretation:

- Same-model normalization is not a general solution.
- Qwen2.5-7B is the cautionary result: dev50 improved but held-out test150
  reversed, so mitigation claims cannot rely on dev-only prompt gains.
- There is recoverable signal, but the router must be stronger than simple
  preservation heuristics.
- Answer-side signals are promising, but the final rule must be locked before
  any new held-out evaluation.

Cross-script consistency:

| Model | Banglish | Gold Bangla+English agreement route | Oracle |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | 99/200 |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | 115/200 |
| Qwen3-4B | 49/200 | 76/200 | 108/200 |

This is diagnostic only because it uses gold alternate-script views. The
deployable plan is to generate Bengali and English views, reject corrupted
generations using preservation gates, and use agreement only when generated
Bengali and generated English answers match.

Generated-view dev diagnostics:

Historical protected-v1 answer rows are diagnostics only. Reviewed-v5
protected-v2 deterministic files received Qwen answer audits, but the tightened
formula-expression gate rejects 16/36 rows for both deterministic generators.
The formulaish-token protected-v3 wrapper now passes 0/36 hard gates; its
answer audits show only small dev changes.

| Model / route | Banglish | Generated view | Routed | Decision |
| --- | ---: | ---: | ---: | --- |
| Qwen3 protected BNB generated-BN | 15/36 | 17/36, +5.6 pts CI [-8.3,+19.4] | n/a | Weak dev-only lead. |
| Qwen3 protected phonetic generated-BN | 15/36 | 11/36, -11.1 pts CI [-25.0,+2.8] | n/a | Drop for Qwen3. |
| Qwen2.5 protected phonetic generated-BN | 8/36 | 14/36, +16.7 pts CI [0.0,+33.3] | n/a | Model-specific dev lead. |
| Qwen2.5 protected BNB generated-BN | 8/36 | 7/36, -2.8 pts CI [-16.7,+11.1] | n/a | Drop for Qwen2.5. |
| Qwen3 generated-BN + generated-EN agreement | 15/36 | BN 17/36, EN 7/36 | 16/36 | Do not test150. |

Reviewed-v5 protected-v2 generated-BN answer audits:

| Model / route | Banglish | Generated view | Gate-eligible view | Decision |
| --- | ---: | ---: | ---: | --- |
| Qwen3 protected-v2 phonetic generated-BN | 15/36 | 13/36 | 9/20 vs Banglish 10/20 | Gate-blocked; no dev lead. |
| Qwen3 protected-v2 BNB generated-BN | 15/36 | 16/36 | 11/20 vs Banglish 10/20 | Gate-blocked; +1 eligible item only. |
| Qwen2.5 protected-v2 phonetic generated-BN | 9/36 | 10/36 | 5/20 vs Banglish 5/20 | Gate-blocked; flat eligible result. |
| Qwen2.5 protected-v2 BNB generated-BN | 9/36 | 8/36 | 6/20 vs Banglish 5/20 | Gate-blocked; +1 eligible item only. |

Reviewed-v5 protected-v3 generated-BN answer audits:

| Model / route | Banglish | Generated view | Bootstrap | Decision |
| --- | ---: | ---: | ---: | --- |
| Qwen3 protected-v3 phonetic generated-BN | 15/36 | 14/36 | -2.8 pts CI [-16.7,+11.1] | Drop for Qwen3. |
| Qwen3 protected-v3 BNB generated-BN | 15/36 | 17/36 | +5.6 pts CI [-8.3,+19.4] | Weak dev lead only. |
| Qwen2.5 protected-v3 phonetic generated-BN | 9/36 | 10/36 | +2.8 pts CI [-13.9,+19.4] | Weak/flat dev result. |
| Qwen2.5 protected-v3 BNB generated-BN | 9/36 | 9/36 | +0.0 pts CI [-19.4,+19.4] | Flat. |

Formal-gate-only generated-BN candidates:

| Generator | Hard failures | Latin residue warnings | Native-reference mean CER | Decision |
| --- | ---: | ---: | ---: | --- |
| Reviewed-v5 protected-v2 phonetic | 16/36 | 0/36 | n/a | Formula-expression gate blocks route. |
| Reviewed-v5 protected-v2 BNB | 16/36 | 0/36 | n/a | Formula-expression gate blocks route. |
| Reviewed-v5 protected-v3 phonetic | 0/36 | 0/36 | n/a | Gate-passing; answer gains small. |
| Reviewed-v5 protected-v3 BNB | 0/36 | 0/36 | n/a | Gate-passing; Qwen3 weak lead only. |
| Protected FMS-byte MBART | 15/36 | 7/36 | 0.1855 | Do not escalate. |

Interpretation:

- Structural preservation gates are necessary but not sufficient.
- Historical-v1 generated-BN answer effects differ across Qwen2.5 and Qwen3.
- Protected-v2 answer effects are too small after the tightened gate, so the
  protection wrapper itself had to be repaired before any further route claim.
- Protected-v3 fixes deterministic preservation, and guarded generated-English
  fixes hard preservation, but the guarded route remains weak: +1 item for
  Qwen3 and -1 item for Qwen2.5 on dev.
- Route-bottleneck analysis shows strict generated-view agreement recovers only
  1/5 Qwen3 baseline-wrong generated-view recoveries and 0/10 Qwen2.5
  recoveries.
- Simple looser answer-routing rules are not stable enough for held-out launch:
  Qwen3 best guarded rules are +2, while Qwen2.5's best is +4 with 5 losses.
- FMS-byte fails the tightened formula-expression gate and still has lexical
  residue.
- Raw Qwen3 self-translated English is too weak, while guarded generated-English
  uses 15/36 source fallbacks and still does not produce a route-ready
  agreement signal.

Key artifacts:

- `results/tables/selfnorm_validation200.csv`
- `results/tables/answer_signal_routing_test150.csv`
- `reports/selfnorm_validation200.md`
- `reports/mitigation_summary.md`
- `reports/selfnorm_routing_devtest_validation200_v4.md`
- `reports/selfnorm_answer_signal_routing_validation200.md`
- `reports/qwen25_selfnorm_answer_signal_routing_examples.md`
- `reports/qwen3_selfnorm_answer_signal_routing_examples.md`
- `reports/qwen25_7b_8bit_selfnorm_validation200_v4.md`
- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/deployable_consistency_mitigation_plan.md`
- `reports/generated_view_preservation_audit_v2.md`
- `reports/qwen3_4b_generated_bn_answer_audit_dev50.md`
- `reports/qwen25_3b_generated_bn_answer_audit_dev50.md`
- `reports/qwen3_4b_generated_view_agreement_route_dev.md`
- `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/generated_view_route_bottleneck_analysis.md`
- `reports/generated_view_routing_candidate_scan.md`
- `results/tables/generated_bn_candidate_preservation.csv`
- `results/tables/generated_bn_reference_similarity_dev50.csv`
- `reports/chapter_8_mitigation_draft.md`

## Chapter 9: Limitations

Must include:

- Rule-based Banglish is not the same as natural human Banglish.
- BnSentMix adds a bounded natural code-mixed task layer, but it is not paired
  by script and has public-dataset contamination/license-metadata caveats.
  Its simple routing candidate is also split-sensitive, so the thesis should
  claim natural-task complementarity rather than a deployable ensemble.
- BanglaTLit distribution analysis shows real Banglish is shorter, less
  number-heavy, sometimes script-mixed, and spelling-variable; frozen
  validation-200 v5 is therefore a controlled script-equivalence benchmark
  rather than a naturalness benchmark.
- BanglaTLit lexical coverage is limited: exact token coverage averages 36.8%
  overall, but the highest-coverage all-200 quartile still keeps reviewed
  Banglish below Bangla, 28/150 slots versus 40/150.
- BEnQA option exact-token coverage is lower than stem coverage: all options
  average 18.5% and gold options 17.3%; high option/gold-option coverage
  quartiles still have negative reviewed-Banglish-minus-Bangla point gaps, with
  intervals crossing zero.
- Per-model coverage sensitivity keeps reviewed Banglish below Bangla and
  English for each main Qwen row in every all-200 coverage quartile.
- Spelling-variation sensitivity keeps reviewed Banglish below Bangla and
  English for each main Qwen row in the highest all-200 repeated-variant
  exposure quartile, but the lowest exposure bucket is mixed for Qwen2.5-3B.
- Source-variant parity is clean for Bangla vs reviewed Banglish, but English
  comparisons have 39/200 diagnostic warnings; English is privileged support,
  not the primary paired source claim.
- The English-warning sensitivity audit shows this caveat does not erase the
  diagnostic pattern on the clean-English subset.
- Current noisy Banglish is deterministic and incomplete.
- BanglaMATH is too hard at current model scale for fine-grained math claims.
- Model coverage is still compact-open-model heavy.
- Cross-script oracle is an analysis upper bound, not deployable accuracy.
- Cross-script answer agreement is also privileged until generated alternate
  views are tested.
- Generated-view routing is not solved: raw generated-English quality is weak,
  guarded generated-English uses source fallback, and generated-BN gains are
  model/generator-specific.
- Mechanistic evidence is currently behavioral plus tokenization, not causal
  internal proof.

Current draft:

- `reports/chapter_9_limitations_draft.md`

## Chapter 10: Conclusion

Main final sentence:

> Banglish robustness is not solved by treating Latin-script Bangla as ordinary
> English-like text or by wrapping the same model in a simple normalization
> prompt. Script choice changes model behavior, and robust Bangla systems need
> explicit evaluation and mitigation for Latin-script Banglish.

Current draft:

- `reports/chapter_10_conclusion_draft.md`

## Remaining Before Submission Polish

1. Decide whether the frozen-v5 paid API smoke adds enough external-validity
   value to run.
2. Add one bounded mechanism section beyond tokenization only if it can be done
   cleanly.
3. Optionally run a deployable generated-view consistency route only after
   generator prompts and preservation gates are locked on dev50.
5. Keep chapter drafts and generated tables synchronized through
   `python3 scripts/run_research_checks.py`.
