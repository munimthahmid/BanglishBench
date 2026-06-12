# Chapter 5 Robustness And Model Breadth Draft

Updated: 2026-05-31

## 5.1 Chapter Goal

Chapter 4 establishes the main validation-200 script gap. This chapter asks how
stable that result is under dataset cleanup, spelling stress tests, model size,
and model family. The goal is not to claim that every model behaves the same
way. The goal is to show which parts of the finding are robust and which parts
need careful qualification.

## 5.2 Cleanup Sensitivity

The first robustness concern is that the Banglish gap might be an artifact of a
bad romanizer. The project therefore created validation-200 v4, keeping the
same 200 item ids while applying conservative Banglish cleanup.

The v4 reruns show that targeted cleanup does not remove the main result.
Qwen2.5-3B changes from 38/200 on v3 Banglish to 39/200 on v4 Banglish.
Qwen3-4B changes from 46/200 to 47/200. Both shifts are only one item.

A broader automatic spelling-suggestion candidate also has little effect.
Qwen2.5-3B moves from 39/200 on v4 to 40/200 on the auto-suggested candidate.
Qwen3-4B moves from 47/200 to 48/200. This candidate is not human-reviewed and
should not be used as the final benchmark, but it is useful sensitivity
evidence.

Interpretation:

- The main Qwen script-gap result is not driven by the known v3 artifact classes
  targeted by v4.
- Automatic spelling cleanup does not materially change accuracy.
- The frozen v5 human review also produces small changes relative to v4:
  Qwen2.5-3B moves 39/200 -> 41/200, Qwen3-4B moves 47/200 -> 49/200, and
  Qwen2.5-7B 8-bit moves 48/200 -> 47/200.
- Review-label sensitivity shows the final deficit is not confined to rows
  that required edits. In unreviewed rows, reviewed Banglish is below Bangla
  for Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B; the same is true for the
  reviewed non-bad bucket.
- Review edit-distance sensitivity sharpens that check: the 63 rows with no
  applied Banglish change already keep reviewed Banglish below Bangla and
  English for all three thesis-facing Qwen rows, while larger-edit rows are
  only 19 items.
- Source-variant structural parity shows the primary Bangla-vs-reviewed
  Banglish pair has 0/200 option-label, digit-sequence, formula-token, or
  answer-instruction mismatches. English comparisons have 39/200 diagnostic
  warnings and should remain privileged support rather than the main paired
  denominator.
- English-warning sensitivity shows those 39 warning rows do not carry the
  diagnostic story: on the 161 clean-English items, reviewed Banglish remains
  below both Bangla and English for all three thesis-facing Qwen rows.
- Human review strengthens benchmark quality without turning controlled
  educational Banglish into a fully natural user corpus.
- The BEnQA option-lexical audit makes that limitation concrete: all-option
  exact BanglaTLit coverage is only 18.5%, but the highest option-coverage
  quartile still has a negative reviewed-Banglish-minus-Bangla point gap.

Artifacts:

- `reports/v4_banglish_sensitivity_validation200.md`
- `reports/validation200_v4_auto_suggested_sensitivity.md`
- `reports/validation200_v5_review_queue.md`
- `reports/v5_review_label_sensitivity.md`
- `reports/v5_review_edit_distance_sensitivity.md`
- `reports/v5_source_variant_structural_parity.md`
- `reports/v5_english_warning_sensitivity.md`
- `reports/v5_benqa_option_lexical_coverage.md`
- `results/tables/v5_reviewed_banglish_sensitivity.csv`

## 5.3 Noisy Banglish Sensitivity

The current noisy-Banglish variant tests whether deterministic spelling noise
itself explains the gap. This historical v3 stress test predates reviewed v5
and remains a robustness diagnostic rather than the release-facing main table.
It does not explain the gap. Qwen2.5-3B scores 38/200 on clean
Banglish and 41/200 on noisy Banglish. Qwen3-4B scores 46/200 on both.

This result should be framed narrowly. The noisy generator is a deterministic
stress test, not a model of real social-media Banglish. Natural Banglish has
more diverse spelling variation, code-mixing, abbreviations, and pragmatic
context. The result only shows that this synthetic noise variant is not what
caused the clean Banglish deficit.

Artifact:

- `reports/noisy_banglish_validation200.md`

## 5.4 Qwen Scaling

The Qwen scaling results show that task competence matters. This historical
cross-model matrix intentionally retains the version-specific v3/v4 outputs
available for each model; use the frozen-v5 table in Chapter 4 for final
three-model release numbers.

| Model | Bangla | Banglish | English | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Qwen2.5-0.5B | 40/200 | 44/200 | 40/200 | Too weak/noisy for the main claim. |
| Qwen2.5-1.5B | 46/200 | 38/200 | 72/200 | English gap appears; Bangla gap is weaker. |
| Qwen2.5-3B | 54/200 | 38/200 | 71/200 | Main Qwen2.5 result. |
| Qwen2.5-7B 8-bit | 65/200 | 48/200 | 94/200 | Stronger Qwen2.5 scaling point. |
| Qwen3-1.7B no-thinking | 34/200 | 36/200 | 61/200 | English gap, no reliable Banglish-below-Bangla. |
| Qwen3-4B | 80/200 | 46/200 | 88/200 | Strongest open-model result. |

For Qwen2.5, the Banglish-below-Bangla gap becomes reliable at 3B and persists
at the 7B 8-bit scaling point. For Qwen3, the 1.7B no-thinking model does not
show the Banglish-below-Bangla ordering, while Qwen3-4B shows the strongest
gap. This supports a competence-threshold interpretation: once the model is
capable enough to answer many native Bangla items, Banglish failures become more
visible and meaningful.

The frozen-v5 scaling-transfer audit adds an item-level version of this point.
Under same-family Qwen2.5 3B->7B scaling, all-200 Bangla gains 11 items and
English gains 23 items, while reviewed Banglish gains only 6. Comparing
Qwen2.5-3B to Qwen3-4B, Bangla gains 26 items and English gains 17, but
reviewed Banglish gains 8. Stronger Qwen competence therefore does not
automatically transfer to Latin-script Banglish.

Artifacts:

- `reports/qwen_scaling_validation200.md`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/v5_qwen_scaling_transfer.md`
- `results/tables/model_family_scaling_validation200.csv`

## 5.5 Non-Qwen Breadth

Phi-3.5-mini is the strongest current non-Qwen validation-200 contrast. It
scores 38/200 in Bangla, 40/200 in Banglish, and 80/200 in English. The
Banglish-minus-Bangla interval crosses zero, while Banglish-minus-English is
clearly negative.

This matters because it prevents overclaiming. The thesis should not say that
Banglish is universally harder than native Bangla for every compact model. It
can say that script/language choice strongly affects model behavior, that
Banglish remains much weaker than English for Phi, and that the
Banglish-below-Bangla ordering is strongest in the competent Qwen baselines.

Mistral-7B and Indic-Gemma-2B were run only as pilot20 diagnostics. Mistral-7B
8-bit was feasible but weak and slow. Indic-Gemma-2B was parseable under an
Alpaca wrapper but around chance. These results should stay as diagnostic
breadth, not main evidence.

Artifacts:

- `reports/phi35_mini_validation200_v4.md`
- `reports/mistral7b_8bit_pilot20_validation200_v4.md`
- `reports/indic_gemma2b_pilot20_validation200_v4.md`

## 5.6 Bangla-Specialized Model Diagnostics

Bangla- or Indic-specialized labels are not enough to make a model a valid
baseline. BanglaLLM and TituLM pilots produced degenerate or unrelated outputs
under the current evaluator. Indic-Gemma-2B was parseable but low-accuracy.

This should be presented carefully. These pilots do not prove that Bangla
specialization is ineffective. They show that prompt template, answer-only
format, thinking mode, and parser compatibility must be validated before a
specialized model can become thesis evidence.

Artifact:

- `reports/bangla_specialized_model_pilots.md`

## 5.7 Compute-Limited Larger Models

Qwen3-8B was attempted but blocked on Kaggle P100. The 8-bit path failed due to
bitsandbytes backend compatibility, and older bitsandbytes was rejected by the
current Transformers stack. This is a compute/runtime constraint, not a thesis
choice.

The final API audit plan addresses external validity without turning frontier
APIs into exploratory spending. The v5 slice and required open-model reruns are
now locked, so a paid smoke audit is optional and budget-gated.

Artifacts:

- `reports/qwen3_8b_8bit_pilot20_failure.md`
- `reports/kaggle_gpu_feasibility_notes.md`
- `reports/final_api_audit_cost_plan.md`

## 5.8 Chapter Conclusion

The main Qwen script-gap result is robust to targeted Banglish cleanup,
automatic spelling suggestions, and the current deterministic noisy-Banglish
variant. It also persists across stronger competent Qwen baselines. However,
the exact Banglish-below-Bangla ordering is not universal across all compact
models tested. This is a strength rather than a weakness for the thesis: it
shows that the final claim should be precise, model-aware, and supported by
paired uncertainty estimates rather than stated as a universal law.
