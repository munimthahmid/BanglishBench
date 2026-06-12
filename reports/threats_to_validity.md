# Threats To Validity

Updated: 2026-06-03

## Purpose

This note collects the main risks to the thesis claims and the controls already
in place. It should feed the limitations chapter.

## Dataset Construction Risks

| Risk | Why it matters | Current control | Remaining action |
| --- | --- | --- | --- |
| Controlled Banglish may not match natural human Banglish. | The main benchmark could underrepresent organic spelling variation, code-mixing, and pragmatic context. | v4 cleanup, real-Banglish distribution comparison, frozen 140-row v5 review queue, impact-ordered packets, reviewed-v5 sensitivity reruns, and the BnSentMix natural code-mixed sentiment external layer. | Keep the naturalness limitation explicit; use BnSentMix as ecological-validity evidence rather than as a paired script-gap estimate. |
| Source datasets contain noisy English translations or formulas. | Cross-script comparisons can inherit source noise. | Paired item ids, source-aware review packets, preservation checks for options/digits/formulas, explicit bad-row flags. | Do not silently repair non-Banglish fields. |
| BanglaMATH is very hard for current open models. | Low accuracy can hide script effects. | Report BEnQA and BanglaMATH separately; treat BanglaMATH as a stress test. | Keep main script-gap interpretation anchored in competent BEnQA-heavy evidence. |
| Reviewed v5 contains flagged bad rows. | Accuracy tables become incomparable if bad rows are dropped silently. | The frozen main policy keeps all 200 rows and flags 3 bad rows. A separate strict-197 sensitivity report excludes them and preserves the main conclusion. | Keep all-200 and strict-subset results clearly separated. |

## Evaluation Risks

| Risk | Why it matters | Current control | Remaining action |
| --- | --- | --- | --- |
| Answer parsing errors can distort accuracy. | Short-answer and MCQ extraction are brittle. | Reparsed/rescored result files, parser smoke checks, item-level changed-output reports. | Reuse same parser for post-v5 and paid API audit. |
| Qwen3 thinking mode can break answer-only evaluation. | Truncated reasoning traces caused degenerate early outputs. | Disable-thinking controls recorded for Qwen3-family no-thinking probes; Qwen3-4B Instruct runs use stable answer-only setup. | Continue recording thinking mode in every Qwen3-family run. |
| Dev exploration can overfit test150. | Mitigation claims can be inflated by trying many rules. | validation-200 v4 dev50/test150 split, next-experiment queue, post-v5 rerun protocol. | Do not launch test150 generated-view routing without a locked dev rule. |
| Kaggle GPU environment constrains model choice. | P100/quantization limits can make model coverage look narrower than desired. | Feasibility notes, blocked Qwen3-8B record, pilot20-first policy, pinned-stack Qwen2.5-7B rerun. | Decide whether the locked-table paid API smoke adds enough external-validity value. |

## Mechanism Risks

| Risk | Why it matters | Current control | Remaining action |
| --- | --- | --- | --- |
| Tokenization evidence is descriptive, not causal. | Token counts cannot prove internal representation mechanisms. | Tokenization/failure-pattern analysis is framed as ruling out a simple length explanation only. | Avoid causal mechanism claims unless representation probes are added. |
| The option-permutation probe is controlled and dev-only. | A strong positional effect on 36 BEnQA dev MCQs can be mistaken for an internal causal mechanism or a held-out generalization result. | Rotate semantic option content through every label, remap gold labels, compare Qwen3 against Qwen2.5-3B, and report label-D versus original-D-content persistence separately. | Use as behavioral failure-mode evidence only; do not promote it as internal causal proof or a mitigation result. |
| Cross-script oracle uses privileged benchmark views. | It can overstate deployable mitigation. | Reports label it as diagnostic; the reviewed-v5 oracle/taxonomy/agreement refresh is in `reports/cross_script_diagnostics_validation200_v5.md`, and the generated-view route is separately audited. | Keep oracle and deployable mitigation claims separate. |
| Generated-view diagnostics are small and dev-only. | Cheap generated-BN/EN results may not generalize, and formal preservation can miss lexical quality problems. | Tightened preservation gates, lexical-residue warnings, privileged native-reference similarity, historical-v1 provenance labels, bootstrap intervals, no test150 escalation. | Revisit only after a stronger generator is selected and separately answer-audited. |

## Scope Risks

| Risk | Why it matters | Current control | Remaining action |
| --- | --- | --- | --- |
| Main evidence is strongest for Qwen-family compact models. | The result may not hold identically for all LLM families. | Phi, Mistral, Indic-Gemma, Bangla-specialized diagnostic pilots; final API audit plan. | Use paid APIs as external validity, not exploration. |
| Banglish social-media distributions differ from curriculum QA/math. | Real user Banglish includes spelling variation, code-mixing, slang, and shorter utterances. | BanglaTLit/BanglishRev/BAN-TH/BnSentMix/MixSarc literature, distribution comparison, and BnSentMix task-layer evaluation. | State that the benchmark is controlled educational Banglish, while BnSentMix supplies a separate natural code-mixed task rather than a causal script-control. |
| Results may change with stronger future models. | Frontier models evolve quickly. | Date-stamped model IDs and current pricing/model audit plan. | Record exact model IDs, dates, and costs for any final API run. |

## Thesis-Safe Claim Boundary

Safe:

- Controlled Latin-script Banglish exposes a robust orthographic weakness in
  current competent open Qwen baselines on Bangla educational QA/math.
- The weakness is not explained by token count alone.
- Mitigation is possible but brittle; agreement/routing signals need strict
  preservation and dev/test discipline.

Avoid:

- Claiming Banglish is universally harder than Bangla for every model.
- Claiming frozen reviewed Banglish fully represents natural Banglish.
- Claiming BnSentMix sentiment accuracy is directly comparable to paired
  validation-200 QA/math script-gap accuracy.
- Claiming generated-view routing is solved.
- Claiming internal causal mechanisms beyond the evidence collected.
