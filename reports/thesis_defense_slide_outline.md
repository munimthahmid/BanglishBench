# Thesis Defense Slide Outline

Updated: 2026-06-03

## Purpose

This is a draft defense structure based on the current thesis evidence. It
includes the completed v5 review and required reruns. Add a paid API slide only
if that optional audit is run.

## 1. Title

Message:

- Script choice matters for Bangla LLM access.

Content:

- Working title: Script Matters.
- Subtitle: Bangla, Banglish, and English robustness in educational QA/math.
- One-line thesis: models that answer Bangla and English can still fail when
  the same content is written as user-facing Banglish.

## 2. Motivation

Message:

- Banglish is a real user interface, not a typo condition.

Content:

- Bangla users often type Bangla content in Latin characters.
- Education and QA assistants must handle this input style.
- Existing Bangla benchmarks rarely isolate script choice while holding item
  and gold answer fixed.

Evidence:

- `literature/notes/script_matters_literature_synthesis.md`
- `literature/notes/benchmark_gap_matrix.md`

## 3. Research Questions

Message:

- The thesis asks measurement, mechanism, and mitigation questions.

Content:

1. Does Banglish reduce answer accuracy when item meaning is held fixed?
2. Is the gap just tokenization cost or item difficulty?
3. Can prompt or routing mitigations recover the loss?
4. What release process makes the benchmark trustworthy?

## 4. Benchmark Design

Message:

- Same item, same answer, different script views.

Content:

- Sources: BEnQA and BanglaMATH, with MGSM as external breadth.
- Variants: Bangla, clean Banglish, noisy Banglish, English.
- validation-200: 144 BEnQA, 56 BanglaMATH.
- v5 manual review reduces pipeline-artifact risk.

Evidence:

- `reports/dataset_card_validation200.md`
- `reports/chapter_3_benchmark_construction_draft.md`

## 5. Main Result

Message:

- Competent Qwen models show a clear Banglish gap.

Content:

- Frozen-v5 reviewed Banglish is the main release view.
- Qwen2.5-3B: Bangla 54/200, Banglish 41/200, English 71/200.
- Qwen2.5-7B 8-bit: Bangla 65/200, Banglish 47/200, English 94/200.
- Qwen3-4B: Bangla 80/200, Banglish 49/200, English 88/200.
- Qwen2.5-3B all-200 CI reaches zero; Qwen2.5-7B and Qwen3-4B remain clearly
  negative, and strict-197 keeps all three negative.
- Dataset intervals place the clearest split-level source in BEnQA: Qwen3-4B
  BEnQA reviewed-Banglish-minus-Bangla is -20.1 pts, CI [-28.5, -11.8];
  BanglaMATH remains a low-accuracy stress test.
- BEnQA leave-one-subject stability keeps the gap negative under every subject
  drop for all three thesis-facing Qwen rows.

Visual:

- `reports/figures/main_script_gap.svg`

Evidence:

- `reports/main_results_validation200_v5.md`
- `reports/v5_dataset_gap_intervals.md`
- `reports/v5_benqa_subject_stability.md`

## 6. Robustness And Scope

Message:

- The result is stable under cleanup, but not universal across every small
  model.

Content:

- v4 cleanup changes Qwen2.5 and Qwen3 by only +1/200 each.
- Review-label sensitivity shows the gap is present in both unreviewed and
  reviewed non-bad v5 buckets for the main Qwen rows.
- Qwen3-1.7B and Phi-3.5 show different Bangla-vs-Banglish ordering, so the
  safest claim is script-conditioned robustness with competence/model-family
  scope.
- Qwen2.5-7B strengthens the competent-model story.

Evidence:

- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/qwen25_7b_8bit_validation200_v4.md`
- `reports/v5_review_label_sensitivity.md`

## 7. Tokenization And Mechanism

Message:

- Token count alone does not explain the Banglish drop.

Content:

- Banglish is token-cheaper than native Bangla for measured Qwen tokenizers.
- Recoverable Banglish misses are not simply the longest Banglish prompts.
- Mechanism claim remains behavioral, not causal.

Evidence:

- `reports/tokenization_validation200.md`
- `reports/tokenization_cross_script_failure_patterns.md`

## 8. Failure Analysis

Message:

- Many Banglish misses are recoverable under alternate scripts.

Content:

- Reviewed-v5 any-script oracle: Qwen2.5-3B 99/200, Qwen2.5-7B 115/200,
  Qwen3-4B 108/200.
- Qwen3 has 32 items where Bangla and English are correct but reviewed Banglish is
  wrong.
- Difficulty-conditioned consensus: among items all three Qwen rows answer
  correctly in English, reviewed Banglish is 50/147 correct slots versus
  92/147 for Bangla.
- Controlled option-permutation dev probe: on Qwen3 identity wrong-D items,
  35/45 rotations remain literal label D while only 6/45 follow original-D
  content. Frame as behavioral evidence for a label-position D-attractor.
- Qualitative examples now include 5 all-three strict frozen-v5 cases; main
  body can use `banglamath_0229`, `banglamath_0230`, and
  `benqa_10th-Physics_0021`.

Visual:

- `reports/figures/cross_script_recovery.svg`
- `reports/thesis_qualitative_examples.md`
- `reports/v5_difficulty_conditioned_gap.md`
- `reports/v5_shared_fragility_examples.md`
- `reports/v5_benqa_option_permutation_probe_results.md`

## 9. Mitigation Results

Message:

- Self-normalization is not a stable answer.

Content:

- Historical v3/v4 diagnostic outputs:
- Qwen2.5-3B: 38/200 -> 51/200.
- Qwen2.5-7B 8-bit: 48/200 -> 47/200.
- Qwen3-4B: 46/200 -> 21/200.

Visual:

- `reports/figures/selfnorm_delta.svg`

## 10. Stronger Mitigation Signal

Message:

- Cross-script agreement is promising but privileged.

Content:

- Bangla+English agreement route:
  Qwen2.5-3B 41 -> 49,
  Qwen2.5-7B 47 -> 71,
  Qwen3-4B 49 -> 76.
- Reviewed-v5 intervals remain clearly positive for Qwen2.5-7B and Qwen3;
  Qwen2.5-3B crosses zero.
- This is diagnostic because it uses benchmark-provided alternate views.
- Generated-view experiments show preservation gates are mandatory.

Evidence:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/generated_view_diagnostics_summary.md`

## 11. Dataset Quality And v5

Message:

- The completed v5 review strengthens the controlled benchmark.

Content:

- v5 queue: 140 rows reviewed, zero pending.
- Labels: 126 minor edits, 11 major edits, 3 flagged bad rows.
- Qwen2.5-3B v4 -> v5 Banglish: 39/200 -> 41/200.
- Qwen3-4B v4 -> v5 Banglish: 47/200 -> 49/200.
- Qwen2.5-7B 8-bit v4 -> v5 Banglish: 48/200 -> 47/200.

Evidence:

- `reports/validation200_v5_review_progress.md`
- `reports/validation200_v5_substitution_review_playbook.md`

## 12. Contributions

Message:

- The thesis contribution is benchmark plus analysis plus release discipline.

Content:

1. Controlled Bangla/Banglish/English QA/math benchmark.
2. Open-model evidence of a Banglish script robustness gap.
3. Tokenization and failure analyses that narrow explanations.
4. Mitigation evidence showing prompt normalization is brittle.
5. Cross-script agreement diagnostic and generated-view caution.
6. Human-review and reproducibility workflow for thesis-grade release.

## 13. Limitations

Message:

- The work is strong because it is precise about boundaries.

Content:

- Controlled Banglish is not full natural Banglish.
- Current models are mostly open compact/medium models.
- Mechanism evidence is behavioral.
- Generated-view mitigation is not final.
- v5 review is complete; controlled Banglish is still not a natural user corpus.

Evidence:

- `reports/threats_to_validity.md`
- `reports/chapter_9_limitations_draft.md`

## 14. Final Slide

Message:

- Treat script as an access condition.

Content:

- Banglish users should not be considered "out of distribution noise" by
  default.
- For Bangla educational QA/math, script choice can decide whether the same
  model succeeds or fails.
- Robust deployment needs script-aware evaluation and preservation-tested
  mitigation, not only English or native-script benchmarks.

## Optional Final Slide Update

Add a final API-audit slide only if the budgeted paid smoke and any promoted
full runs are completed.
