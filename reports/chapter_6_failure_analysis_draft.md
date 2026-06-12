# Chapter 6 Failure Analysis Draft

Updated: 2026-06-03

## 6.1 Chapter Goal

The main script-gap result shows that competent Qwen models answer fewer items
correctly in Banglish. This chapter asks whether those Banglish failures are
actually script-specific, or whether they are simply hard items that the model
would fail in any form.

The evidence comes from cross-script oracle analysis, failure taxonomy,
cross-script transfer retention, recoverability-source decomposition,
item-consensus analysis, difficulty-conditioned consensus buckets, qualitative
examples, and tokenization/failure joins.

These diagnostic analyses use frozen-v5 reviewed Banglish outputs. Bangla and
English outputs are reused because those fields did not change. The historical
v3/v4 reports remain available as audit trails.

## 6.2 Cross-Script Oracle

The any-script oracle asks whether the model answers an item correctly in at
least one script view. This is not deployable accuracy because it uses
benchmark-provided Bangla, Banglish, and English views. It is a diagnostic for
recoverability.

| Model | Banglish only | Any-script oracle | BEnQA oracle |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 99/200 | 92/144 |
| Qwen2.5-7B 8-bit | 47/200 | 115/200 | 105/144 |
| Qwen3-4B | 49/200 | 108/200 | 102/144 |

The oracle is much higher than Banglish-only accuracy. This means many
Banglish failures are not impossible questions for the model. The same model
often has enough task knowledge to answer the item when it is shown in Bangla
or English.

The transfer-retention view conditions on that same-model competence. Among
items where the same model is correct in Bangla or English, reviewed Banglish
retains correctness only 34/92 times for Qwen2.5-3B, 39/107 for Qwen2.5-7B
8-bit, and 44/103 for Qwen3-4B. This is a stricter way to say that Banglish
failures are not merely low overall task competence.

Artifact:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/v5_cross_script_transfer.md`

## 6.3 Failure Taxonomy

The failure taxonomy classifies each item by which script views are correct.
Two categories are especially important:

- Bangla and English correct, Banglish wrong.
- Bangla or English correct, Banglish wrong.

For Qwen3-4B, 32/200 items are correct in both Bangla and English but wrong in
reviewed Banglish. Recoverable misses remain substantial: 58/200 for
Qwen2.5-3B, 68/200 for Qwen2.5-7B 8-bit, and 59/200 for Qwen3-4B.

These categories support the core interpretation: Banglish can block access to
answers the model can otherwise produce.

The source decomposition sharpens this point. Across the 600 model-item slots,
reviewed Banglish is wrong in 463 slots. Of these misses, 185/463 are
recoverable by native Bangla or English and 278/463 are all-script hard. The
recoverable portion is not just an English-only effect: native Bangla
participates in 104/185 recoverable misses, English participates in 157/185,
and both alternate scripts recover 76/185. This keeps the analysis aligned
with the thesis claim: script form matters even when the task is available in
the language family, while English remains a stronger alternate view overall.

Artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/v5_cross_script_transfer.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_shared_fragility_examples.md`

## 6.4 Feature Concentration

The reviewed-v5 fragility analysis joins the cross-script failure taxonomy with
dataset metadata and prompt features. It counts a fragility event when a model
gets reviewed Banglish wrong while getting Bangla or English right on the same
item.

Across the three thesis-facing Qwen rows, 185/600 model-item slots are
Banglish-fragile by this definition. The stricter category where both Bangla
and English are correct but Banglish is wrong appears in 76/600 slots. At the
item level, 108/200 items have at least one fragile model, and 21/200 are
fragile for all three thesis-facing models.

The model-overlap refresh separates shared failure from one-model quirks.
Among the 108 any-fragile items, 52 affect exactly one model, 35 affect exactly
two models, and 21 affect all three models. In other words, 56/108 any-fragile
items affect at least two thesis-facing Qwen rows. This supports a family-level
fragility interpretation while preserving the model-specific caveat.

The concentration is not uniform. BEnQA MCQ rows account for most recoverable
Banglish-specific fragility: 164/432 model-item slots, compared with 21/168 in
BanglaMATH. BanglaMATH is still difficult, but much of its difficulty appears
as all-script-wrong behavior rather than recoverable Banglish-only failure. The
highest fragility rates are in science-heavy BEnQA domains such as Biology-I,
Biology-II, Chemistry-II, Biology, Chemistry-I, and general Science. This makes
the failure analysis more precise: the Banglish gap is broad, but recoverable
script-specific misses are especially visible where technical vocabulary and
curriculum terminology must be read through Latin-script Bangla.
The model-overlap report ranks shared fragility by dataset and domain, so
BEnQA math and BanglaMATH math are interpreted separately rather than merged
under one `math` label.

The item-consensus audit gives a second, model-family view of the same pattern.
Across 600 paired model-item slots, reviewed Banglish is correct 137 times,
versus 199 for Bangla and 253 for English. The item-cluster bootstrap deltas
remain negative against both Bangla and English. On BEnQA, 61/144 items have at
least two-model support in Bangla or English while reviewed Banglish has at
most one correct model; only 12/144 BEnQA items are all-script hard. This
supports the claim that many Banglish misses are recoverable script-specific
failures rather than uniformly impossible items.

The difficulty-conditioned consensus audit makes the item-difficulty argument
more direct. It buckets items by how many thesis-facing Qwen rows answer the
English, Bangla, or best alternate-script view correctly. In the all-200 bucket
where all three Qwen rows answer English correctly, reviewed Banglish has
50/147 correct model-item slots versus 92/147 for Bangla, a paired
item-bootstrap delta of -28.6 points with CI [-38.8,-18.4]. In the
English-consensus=2 bucket, reviewed Banglish is 36/108 versus 49/108 for
Bangla. These high-headroom buckets are the important ones: they show that the
Banglish deficit grows on items the Qwen family can answer in another script,
rather than appearing only in all-script-hard rows.

A leave-one-model-out stability audit checks that this consensus pattern is
not driven by any one Qwen row. Every two-model subset remains negative against
both Bangla and English on all-200 and BEnQA. This narrows the residual risk:
the result is still Qwen-family evidence, but it is not a single-model artifact
inside that family.

The composition-sensitivity audit addresses a related alternative explanation:
that the recoverable failures are mostly caused by numeric or formula-heavy
rows. In no-digit rows, no-formula/operator rows, and the stricter BEnQA
no-digit/no-formula subset, all three thesis-facing Qwen rows still answer
reviewed Banglish less accurately than Bangla and English. This does not erase
the benchmark-naturalness limitation, but it weakens a simple
numeric-composition explanation.

The BEnQA choice-bias audit adds a more specific MCQ failure mode. For Qwen2.5,
reviewed Banglish does not collapse to a single answer label, so the Qwen2.5
gap is not just a label-prior artifact. For Qwen3, reviewed Banglish strongly
over-selects option D: 111/144 predictions are D, while gold D appears on
39/144 rows. This is useful failure evidence because it shows script choice can
change not only correctness but also the model's answer-selection prior.

The prediction-diversity audit makes that collapse easier to quantify. Gold
BEnQA labels have 0.994 normalized entropy and 3.97 effective options. Qwen3
reviewed Banglish falls to 0.502 normalized entropy and 2.01 effective options,
while the same model has 3.52 effective options in Bangla and 3.69 in English.
The two Qwen2.5 reviewed-Banglish rows retain 3.75 and 3.77 effective options.

The distractor-transition audit shows that recoverable BEnQA Banglish misses
are usually real wrong-option choices rather than invalid MCQ outputs:
162/164 are valid distractors. Cross-model convergence is also visible: among
50 items where at least two models make valid recoverable Banglish misses, 27
share the same wrong option across at least two models. This is behavioral
evidence of script-conditioned distractor attraction, not an internal mechanism
claim.

The gold-label balance sensitivity check verifies that this is not merely a
gold-label distribution artifact. Label-balanced BEnQA accuracy keeps reviewed
Banglish below Bangla and English for every thesis-facing Qwen row; for Qwen3,
the reviewed-Banglish gap is -21.7 points versus Bangla under balancing and
-29.5 points after removing gold-D items. The non-D slice turns Qwen3's
D-heavy behavior into direct failure evidence rather than a confound.

The subject option-bias audit checks whether Qwen3's D-attractor is localized
to one subject. It is not: Qwen3-4B reviewed Banglish has majority-D
predictions in 12/13 BEnQA subjects, compared with 1/13 for Qwen2.5-3B and
0/13 for Qwen2.5-7B 8-bit. No subject has gold-D share above 45.5%, so this
extends the label-balance result to subject-level behavior.

The option position/content audit checks whether this is only because D is
often the longest option. D is tied for longest on 98/144 BEnQA items, but
Qwen3 still predicts D on 30/46 items where D is not longest, compared with
9/46 and 5/46 for the two Qwen2.5 rows. Length/content therefore contributes
to the behavior but does not reduce it to a length heuristic.

The option-switching audit compares reviewed-Banglish BEnQA predictions with
the same model's Bangla and English option choices. For Qwen3-4B, valid non-D
Bangla predictions become D in reviewed Banglish on 47/73 rows, and valid
non-D English predictions become D on 55/78 rows. Among correct non-D
alternate-script predictions, those switches become wrong-D reviewed-Banglish
answers on 30/44 Bangla rows and 37/54 English rows. The Qwen2.5 rows have
much smaller Bangla-side non-D-to-D rates, 14/99 and 17/126. This makes the
D-attractor a directional script-conditioned transition, not only an aggregate
label-frequency shift.

The cross-script option-agreement audit applies a stricter agreement filter.
When Qwen3 Bangla and English are both correct and agree on the same non-D
option, reviewed Banglish still switches to wrong D on 23/36 rows. The
corresponding Qwen2.5 rates are 2/23 and 7/44. In the broader Qwen3
Bangla-English non-D agreement slice, reviewed Banglish predicts D on 30/47
rows. This shows the D-attractor survives even when both alternate-script
views give the same non-D answer.

The cross-model Banglish-agreement audit holds the reviewed-Banglish input
fixed and asks what happens when both Qwen2.5 rows agree. The two Qwen2.5 rows
agree on a non-D reviewed-Banglish option in 42 BEnQA rows; Qwen3-4B predicts
D on 26 of those rows and wrong D on 18. In the stricter slice where both
Qwen2.5 rows are correct and agree on the same non-D answer, Qwen3 is wrong-D
on 8/15 rows and matches the Qwen2.5 agreement on 4/15. This makes the failure
mode model-specific under the same script, but the strict slice is small and
should be treated as corroborating evidence.

The order-confound audit checks whether the D-attractor is a simple execution
artifact. By reviewed-Banglish output-line quartile, Qwen3 predicts D on
26/36, 31/36, 28/36, and 26/36 rows; wrong-D counts are 20/36, 19/36, 19/36,
and 19/36. Qwen3 has 23 separate D-runs and a longest contiguous D-run of 13,
whereas the Qwen2.5 rows have lower D totals and longest D-runs of 3 and 2.
This rules out a simple late-run or single terminal-corruption explanation.

The review-label option-bias audit checks whether the D-attractor was created
by the v5 Banglish review edits. On unreviewed BEnQA rows, Qwen3 still predicts
D on 39/51 rows and wrong D on 28/51, while gold D appears on 13/51. On
reviewed nonbad rows, Qwen3 predicts D on 69/90 rows; the corresponding Qwen2.5
D counts are 28/90 and 17/90. This rules out a simple review-edit-only
explanation while preserving the caveat that major-edit and bad buckets are
too small for standalone claims.

The length/token confound audit checks whether the same Qwen3 collapse is just
prompt burden. It is not. By reviewed-Banglish HF-token quartile, Qwen3
predicts D on 32/36, 26/36, 27/36, and 26/36 rows, with wrong-D counts of
26/36, 17/36, 15/36, and 19/36. Character-length quartiles tell the same story:
Qwen3 predicts D on 31/36 shortest rows and 29/36 longest rows. The two Qwen2.5
rows stay far lower in the shortest and longest HF-token quartiles. This makes
the D-attractor a script/model behavior rather than a simple long-prompt
failure.

The option-coverage confound audit checks whether Qwen3 is simply choosing the
option with the most familiar BanglaTLit lexical overlap. On 101 BEnQA items,
all four answer options have identical exact coverage under the same tokenizer
used by the option-lexical audit. Qwen3 still predicts D on 76/101 of those
rows and wrong D on 52/101, while the two Qwen2.5 rows predict D on only
14/101 and 8/101. When at least one option has higher coverage than D, Qwen3
still predicts D on 31/35 rows. Exact option familiarity is therefore not a
sufficient explanation for the D-attractor.

The switch-confound audit joins the transition rows with option length/content
features. When the alternate-script prediction is correct, non-D, and D is not
the longest option, Qwen3 still switches to a wrong reviewed-Banglish D on
11/19 Bangla rows and 12/21 English rows. In the broader non-D, gold-not-D,
D-not-longest scope, Qwen3 switches to D on 13/25 Bangla rows and 15/26
English rows. The corresponding correct-non-D and D-not-longest Bangla-side
counts for Qwen2.5 rows are only 1/13 and 2/22. This keeps the failure mode
visible after removing the two most direct confounds: longest-option D and
gold-D rows.

The semantic-cue audit checks composite roman-marker answers, numeric/formula
strings, and all/none/both markers in option text. D has no such simple cue on
47/144 BEnQA rows; Qwen3 still predicts D on 38/47 of those rows, while the two
Qwen2.5 rows predict D on 9/47 and 4/47. Among correct non-D alternate-script
predictions where D has no cue, Qwen3 switches to wrong reviewed-Banglish D on
15/18 Bangla rows and 18/23 English rows; the Qwen2.5 Bangla-side switch counts
are only 1/11 and 3/21.

The multi-confound residual audit combines these local controls. In the primary
residual scope where gold is not D, D is not the longest option, and D has no
simple semantic cue, Qwen3 is wrong-D on 19/24 rows; Qwen2.5 rows are 4/24 and
1/24. In the stricter tied-coverage residual scope, Qwen3 is wrong-D on 16/20
rows, while Qwen2.5 rows are 4/20 and 1/20. When the same model's Bangla or
English answer is already correct and non-D in the primary residual scope,
Qwen3 still switches to wrong reviewed-Banglish D on 11/13 and 11/14 rows.

The controlled option-permutation dev probe moves beyond descriptive
confound slices. It rotates the semantic option content across A/B/C/D for 36
reviewed-v5 BEnQA dev MCQs while remapping gold labels. Among Qwen3 identity
wrong-D items, 35/45 rotated rows remain attached to literal label D and only
6/45 follow the original D content. Qwen2.5-3B shows the opposite tendency:
5/21 remain label D while 12/21 follow the original D content. This is strong
behavioral evidence for a Qwen3 label-position D-attractor under reviewed
Banglish. The probe is dev-only and does not prove an internal causal
mechanism.

The BEnQA option-lexical audit separates question stems from answer options.
Reviewed-Banglish stems average 31.3% exact BanglaTLit token coverage, while
all answer options average only 18.5% and gold options average 17.3%. This is
important limitations evidence, but it does not reduce the MCQ gap to fully
unattested option strings: in the highest all-option coverage quartile,
reviewed Banglish is 40/108 correct model-item slots versus 50/108 for Bangla.

The response-style drift audit adds a short-answer behavior check. On
BanglaMATH, Qwen3-4B reviewed Banglish produces 15/56 meta/uncertainty
outputs, compared with 0/56 for Bangla and 1/56 for English. Qwen3 is verbose
on BanglaMATH in general, so this should be framed as a model-specific
style-drift failure mode, not as a global gap explanation.

The BanglaMATH numeric-sensitivity audit adds a conservative-scoring check. It
generously credits any raw output containing the full gold numeric signature.
Even then, reviewed Banglish remains lowest for all three Qwen rows; for
Qwen3-4B the raw numeric-signature count is 10/56 for reviewed Banglish versus
19/56 for Bangla and 24/56 for English. This supports treating BanglaMATH as a
low-accuracy stress test with parser/unit caveats, not as a parser-artifact
explanation of the script gap.

The BanglaMATH numeric-transfer audit asks whether numeric evidence available in
Bangla or English carries over to reviewed Banglish. It often does not. For
Qwen3, Bangla or English contains the full raw numeric signature on 24/56 items;
reviewed Banglish retains it on 8/24 and is correct on 2/24. Qwen2.5 retention
is 1/12 and 4/24. In Qwen3's alternate-signature slice, 9/24 reviewed-Banglish
outputs contain meta/uncertainty language and 4/24 are wrong no-number outputs.
This reinforces the transfer-failure framing while keeping numeric signatures
as optimistic behavioral evidence.

Artifacts:

- `reports/v5_banglish_fragility_feature_analysis.md`
- `reports/v5_banglish_fragility_model_overlap.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_item_consensus.md`
- `reports/v5_difficulty_conditioned_gap.md`
- `reports/v5_consensus_stability.md`
- `reports/v5_composition_sensitivity.md`
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
- `reports/v5_benqa_multiconfound_residual.md`
- `reports/v5_benqa_option_permutation_probe_results.md`
- `reports/v5_benqa_option_switch_confound.md`
- `reports/v5_benqa_option_semantic_cues.md`
- `reports/v5_response_style_drift.md`
- `reports/v5_banglamath_numeric_sensitivity.md`
- `reports/v5_banglamath_numeric_transfer.md`
- `reports/v5_benqa_option_lexical_coverage.md`
- `reports/v5_benqa_label_balance.md`
- `results/analysis/v5_banglish_fragility_items.csv`
- `results/analysis/v5_banglish_fragility_feature_summary.csv`

## 6.5 Qualitative Failure Examples

Qualitative examples are useful because aggregate accuracy alone does not show
what changes across scripts. The frozen-v5 shared-fragility packet now exports
these examples directly from the model-overlap and failure-pattern tables. The
most thesis-relevant examples are items where:

1. Bangla and English answers agree with the gold answer.
2. Banglish produces a wrong but parseable answer.
3. The prompt content is visibly equivalent across scripts.

The cleanest current packet has five all-three strict cases: every
thesis-facing Qwen row answers Bangla and English correctly while answering
reviewed Banglish incorrectly. The recommended main-body shortlist is
`banglamath_0229`, `banglamath_0230`, and `benqa_10th-Physics_0021`, giving
two compact arithmetic examples and one non-arithmetic MCQ example.

These examples make the result concrete. They show that a failure can be
triggered by orthography rather than by a different question or a malformed
answer format.

The examples should be used sparingly in the thesis. Two or three well-chosen
examples are enough for the main body; the full packet can go in the appendix
or artifact list.

Artifacts:

- `reports/v5_shared_fragility_examples.md`
- `results/analysis/v5_shared_fragility_examples.csv`
- `reports/thesis_qualitative_examples.md`
- `reports/cross_script_answer_agreement_examples.md`

## 6.6 Cross-Script Answer Agreement

The reviewed-v5 cross-script agreement route is a stronger diagnostic. It uses
Bangla and English answer agreement as a signal for when to override Banglish.
This improves Banglish point accuracy for all main Qwen baselines:

| Model | Banglish | Bangla+English agreement route | Route delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5, +8.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5, +17.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0, +19.0] |

This is not a final mitigation, because a deployed system usually does not have
gold Bangla and English views. But it shows that answer consistency across
scripts is informative. It motivates generated-view routing, retrieval, or
multi-view prompting as future mitigation directions.

The model-aware uncertainty matters: the reviewed-v5 interval remains clearly
positive for Qwen2.5-7B 8-bit and Qwen3-4B, while the Qwen2.5-3B interval
crosses zero.

Artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/figures/cross_script_recovery.svg`

## 6.7 Tokenization-Failure Join

A simple explanation would be that Banglish prompts are longer or more
fragmented than Bangla prompts. The tokenization audit does not support this as
a sufficient explanation. For Qwen tokenizers, Banglish is token-cheaper than
native Bangla, yet the main Qwen models are less accurate on Banglish.

Joining tokenization with failure categories gives another check. Under the
frozen-v5 token/failure join, recoverable Banglish misses are not merely the
longest Banglish prompts. In BEnQA, they are shorter on average than
non-recoverable or other items for Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B. The
strict `bangla_english_correct_banglish_wrong` pattern is also token-cheaper in
reviewed Banglish than native Bangla.

This does not mean tokenization is irrelevant. It means token count alone cannot
explain the Banglish deficit. The mechanism may involve spelling distribution,
subword identity, training frequency, representation alignment, or prompt
grounding.

Artifacts:

- `reports/tokenization_validation200.md`
- `reports/tokenization_cross_script_failure_patterns.md`
- `reports/v5_benqa_length_token_confound.md`

## 6.8 Limits Of The Failure Analysis

The oracle and agreement analyses use privileged benchmark views. They are not
deployable accuracy estimates. They should be presented as diagnostic evidence
that many Banglish misses are recoverable in principle.

The tokenization analysis is also descriptive. It rules out a simple
token-length explanation but does not identify the internal causal mechanism.
Representation-level or intervention experiments would be needed for a
mechanistic claim.

## 6.9 Chapter Conclusion

The Banglish gap is not just a hard-item effect. Many Banglish misses are
answered correctly by the same model under Bangla or English, and privileged
cross-script answer agreement recovers substantial accuracy. At the same time,
Banglish is token-cheaper than native Bangla for the Qwen tokenizers, so the
deficit cannot be reduced to longer token sequences. The feature-level
fragility analysis further shows that recoverable Banglish-specific failures
concentrate in BEnQA science domains, while BanglaMATH is more often hard
across all scripts. The safest conclusion is behavioral: Latin-script Banglish
changes access to task knowledge in ways that standard Bangla-vs-English
evaluation misses.
