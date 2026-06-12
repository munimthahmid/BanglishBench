# Deployable Consistency Mitigation Plan

Updated: 2026-05-31

## Purpose

The cross-script answer-agreement result is strong but privileged: it uses the
benchmark's gold Bangla and English views. This plan turns that diagnostic into
a deployable mitigation protocol that can be tested later without gold alternate
views.

## Diagnostic Starting Point

Gold-view Bangla+English agreement improves frozen-v5 reviewed Banglish point
accuracy:

| Model | Banglish only | Gold Bangla+English agreement route | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5,+8.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5,+17.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0,+19.0] |

This says agreement is a useful signal. It does not say a real system can use
gold Bangla and English prompts. The Qwen2.5-3B interval crosses zero, so keep
that model-specific uncertainty explicit.

Reviewed-v5 diagnostic artifact:
`reports/cross_script_diagnostics_validation200_v5.md`.

## Deployable Protocol

Input:

- One Banglish evaluation item.
- No gold Bangla or English view.
- No access to the answer key.

Step 1: generate alternate views.

- `generated_bn`: rewrite the Banglish item into Bengali script.
- `generated_en`: translate the Banglish item into English.
- The generator prompt must explicitly preserve numbers, formulas, options, and
  line breaks, and must prohibit solving.

Step 2: answer all three views with the same evaluator model.

- `answer_banglish`: answer original Banglish.
- `answer_bn`: answer `generated_bn`.
- `answer_en`: answer `generated_en`.

Step 3: parse answers with the locked evaluator parser.

- MCQ answers normalize to `A`, `B`, `C`, or `D`.
- Short answers use the existing compact answer normalization.
- Empty parses are treated as no agreement.

Step 4: route conservatively.

- If `answer_bn` and `answer_en` are both non-empty and agree, and
  `answer_banglish` is different, return the agreed answer.
- Otherwise return `answer_banglish`.

This mirrors the diagnostic route while replacing gold alternate views with
generated views.

## Development Discipline

Use validation-200 v4 dev50 only for selecting:

- generator model or transliterator,
- generator prompt,
- whether to include short-answer items or MCQ-only routing,
- exact agreement normalization,
- fallback behavior when one generated view fails preservation checks.

Evaluate the selected rule unchanged on test150.

Do not tune on test150. Do not report any generated-view result as final unless
the generation method and routing rule were fixed before test150.

## Preservation Checks Before Answering

Reject a generated alternate view and fall back to Banglish if:

- MCQ option labels are missing or duplicated.
- A choice option line changes its option letter.
- Any Arabic or Bengali numeral count changes unexpectedly.
- Obvious formulas, standalone scientific tokens, nested LaTeX identifiers, or
  annotated units disappear or change.
- The generator outputs an answer instead of a rewritten/translated item.

For MCQ, preservation checks should be strict. For short-answer math, start with
stricter checks or exclude short-answer items from the first deployable route.

## Candidate Generators

| Generator | Role | Status | Risk |
| --- | --- | --- | --- |
| `sk-community/romanized-bengali-transliterator-60M` | Banglish to Bengali script | Already tested as external normalizer on validation-100; weak but cheap. | Domain mismatch and digit/formula corruption. |
| `phonetic-bangla==1.0.0` | Deterministic Banglish to Bengali script | Raw smoke failed 36/36 hard gates. Historical protected-v1 answer-audit input still fails 9/36 tightened gates. Reviewed-v5 protected-v2 fails the formula-expression gate on 16/36 rows. Formulaish-token protected-v3 passes 0/36 hard gates; answer audits are Qwen3 14/36 vs Banglish 15/36 and Qwen2.5 10/36 vs 9/36. | Preservation repaired, but generated-BN answer evidence is too weak for test150. |
| `bnbphoneticparser==0.1.5` | Deterministic Banglish to Bengali script | Raw smoke failed 36/36 hard gates. Historical protected-v1 answer-audit input still fails 10/36 tightened gates. Reviewed-v5 protected-v2 fails the formula-expression gate on 16/36 rows. Formulaish-token protected-v3 passes 0/36 hard gates; answer audits are Qwen3 17/36 vs Banglish 15/36 and Qwen2.5 9/36 vs 9/36. | Weak Qwen3 dev lead only; guarded generated-English routing is still only +1 item for Qwen3. |
| `fms-byte/banglish_to_bangla` | MBART Banglish to Bengali script | Locked 36-item expanded-protection Kaggle dry run fails the tightened formula-expression gate on 15/36 rows, leaves genuine Latin residue on 7/36 rows, and has worse native-reference mean CER (0.1855) than deterministic protected phonetic (0.0906). | Do not escalate unless the FMS protection wrapper is repaired and re-audited. |
| Same evaluator model | Banglish to Bengali/English | Tested via self-normalization and English-pivot; brittle. | Can solve, corrupt options, or hurt Qwen3. |
| Strong paid API model | Banglish to Bengali/English | Defer until final benchmark state. | Cost and possible leakage if prompt is not strict. |
| Human-reviewed v5 source | Dataset quality, not deployment | High priority for final benchmark quality. | Not a deployable generator. |

## First Testable Version

The first deployable experiment should be intentionally narrow:

- Model: Qwen3-4B or Qwen2.5-7B 8-bit.
- Slice: validation-200 v4 dev50.
- Items: BEnQA/MCQ only at first.
- Generated English: one locked generator prompt.
- Generated Bengali: one locked generator or external normalizer.
- Route: generated Bangla+English agreement only.

Scale to test150 only if dev50 improves over Banglish baseline after passing
the preservation gate and after a generated-English view is locked.

Prepared prompt set:

- `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- `data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl`
- `reports/generated_view_prompt_set_dev50_benqa_mcq.md`
- `reports/generated_view_prompt_set_v5_dev50_benqa_mcq.md`
- 36 dev50 BEnQA MCQ items, with Bengali-rewrite and English-translation prompts
  from Banglish-only input.

## Thesis Framing

Safe claim today:

- Gold-view agreement shows that cross-script consistency is a strong mitigation
  signal and motivates deployable generated-view routing.

Claim to avoid until this protocol is run:

- Do not claim we have a deployable mitigation that recovers 71/200 or 76/200.
  Those numbers use gold alternate-script views.

## Preservation Audit Status

Implemented:

- `reports/generated_view_preservation_audit_v2.md`
- `scripts/analyze_rewrite_outputs.py`
- `scripts/audit_generated_view_outputs.py`

Before launching a generated-view route, apply the v2 preservation gates to the
candidate generated Bengali and English views. Reject alternate views with
option-label changes, digit-sequence changes, formula changes, or extra answer
markers.

## Dev Generated-View Route Check

Completed historical dev-only check:

- Generated-BN: historical protected-v1 `bnbphoneticparser`.
- Generated-EN: Qwen3 self-translation.
- Evaluator/router: Qwen3-4B.
- Slice: 36 validation-200 v4 dev50 BEnQA MCQ items.

Result:

- Banglish baseline: 15/36.
- Protected BNB generated-BN: 17/36.
- Generated English self-translate: 7/36.
- Agreement route after generated-EN hard gates: 16/36.
- Tightened generated-EN preservation gate: 16/36 hard failures; the route
  fires on 1/36 item and that item is correct.
- Qwen2.5-3B generated-BN sanity check on the same slice shows the opposite
  generator preference: Banglish 8/36, historical protected-v1
  phonetic-bangla 14/36, historical protected-v1 BNB 7/36.

Completed reviewed-v5 guarded check:

- Guarded generated-EN preservation: 0/36 hard failures, but 15/36 rows are
  source fallbacks.
- Qwen3 guarded EN answer audit: 15/36 vs Banglish 15/36.
- Qwen2.5 guarded EN answer audit: 11/36 vs Banglish 9/36.
- Qwen3 protected-v3 BNB + guarded EN route: 16/36 vs Banglish 15/36.
- Qwen2.5 protected-v3 phonetic + guarded EN route: 8/36 vs Banglish 9/36.

Decision:

- Do not launch test150 for these routes. Raw generated-English is
  gate-blocked; guarded generated-English repairs hard preservation but relies
  on source fallback. Routed gain is only +1 for Qwen3 and -1 for Qwen2.5 on
  dev, and generated-BN gains remain model/generator-specific.
