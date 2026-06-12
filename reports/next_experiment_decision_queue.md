# Next Experiment Decision Queue

Updated: 2026-06-07

## Purpose

This note converts the current evidence into a launch queue. The goal is to
avoid spending GPU on runs that do not change the thesis claim.

## Latest Resolved Job

| Priority | Run | Status | Decision Needed |
| ---: | --- | --- | --- |
| 0 | Gemini 3.5 Flash validation-200 v5 API audit | complete: `reports/gemini_3_5_flash_validation200_v5_results.md` | Use as a bounded frontier-model row: strict 163/200 Bangla, 136/200 reviewed Banglish, 144/200 English; secondary parser/unit sensitivity 170/200, 161/200, 165/200. Next API spend should replicate on one different frontier family or test stricter answer-format control, not add a full prestige triad blindly. |
| 0 | GPT-5.5 low validation-200 v5 full API audit | complete: `reports/openai_gpt55_low_validation200_v5_cap1024_results.md` | Use as the strongest frontier boundary: strict 172/200 Bangla, 169/200 reviewed Banglish, 154/200 English; secondary 173/200, 174/200, 168/200. Top-tier reasoning nearly collapses the population Banglish gap, but reviewed Banglish has the highest output/hidden-token cost. |
| 0 | DeepSeek V4 Flash validation-200 v5 API audit | complete: `reports/deepseek_v4_flash_validation200_v5_results.md` | Use as a cheap non-OpenAI/non-Google frontier-family row: strict 143/200 Bangla, 82/200 reviewed Banglish, and 132/200 English; secondary 152/200, 96/200, and 148/200. The reviewed-Banglish deficit is large: -30.5 strict pts vs Bangla and -25.0 strict pts vs English. |
| 0 | Groq Llama 3.3 70B validation-200 v5 API audit | complete: `reports/groq_llama33_70b_validation200_v5_results.md` | Use as hosted-open Llama evidence, not as a closed frontier peer: strict 90/200 Bangla, 48/200 reviewed Banglish, and 102/200 English; secondary 92/200, 56/200, and 111/200. It shows a large reviewed-Banglish deficit but weak absolute performance. |
| 0 | Claude Sonnet 4.6 validation-200 v5 API audit | complete: `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md` | Use as a high-accuracy but still gap-positive frontier row: strict 162/200 Bangla, 130/200 reviewed Banglish, and 153/200 English; secondary 167/200, 133/200, and 166/200. It has 2 MAX_TOKENS rows and visible answer-only format drift, so do not run Claude full851 by default. |
| 0 | Frontier API panel synthesis | complete: `reports/frontier_api_panel_validation200_v5.md` | Use as the thesis-facing cross-family table. The panel shows non-monotonic frontier behavior: GPT-5.5 nearly collapses the gap, Gemini reduces it, Claude remains strong but gap-positive, and DeepSeek/Groq retain large reviewed-Banglish deficits. |
| 0 | BEnQA extended 1000 v1 review freeze | complete: `reports/benqa_extended_1000_v1_human_review_freeze.md`, `reports/benqa_human_gold_974_prompt_manifest.md` | Use as dataset-size hardening: 1,000 BEnQA candidates were reviewed into a 974-row human-reviewed gold/pass scale panel. The older AI-triaged pass subset remains historical support only. |
| 0 | Qwen2.5-3B BEnQA extension smoke26 | complete: `reports/qwen25_3b_benqa_ext_smoke26.md` | The smoke collected 78/78 rows with 0 parsed-empty rows and no runtime/parser failure pattern. Accuracy on 26 rows is 8/26 Bangla, 11/26 reviewed Banglish, and 20/26 English. The 130-row pilot is now justified and has been launched. |
| 0 | Qwen2.5-3B BEnQA extension pilot130 | complete: `reports/qwen25_3b_benqa_ext_pilot130.md`, `reports/benqa_gold_core_extension_alignment.md` | The pilot collected 390/390 rows with 0 parsed-empty rows. Accuracy is 53/130 Bangla, 42/130 reviewed Banglish, and 71/130 English; paired gaps are -8.46 pts Banglish-Bangla and -22.31 pts Banglish-English. It matches the gold-core BEnQA ordering English > Bangla > Banglish with similar gap magnitudes and is superseded by the completed scale panel. |
| 0 | Qwen2.5-3B BEnQA historical scale run | complete: `reports/qwen25_3b_benqa_ext_full851.md` | Collected 2,553/2,553 rows with 0 parsed-empty rows. Accuracy is 291/851 Bangla, 248/851 reviewed Banglish, and 437/851 English; paired gaps are -5.05 pts Banglish-Bangla, -22.21 pts Banglish-English, and +17.16 pts English-Bangla. Use as historical support behind the human-reviewed 974-row panel. |
| 0 | DeepSeek V4 Flash BEnQA historical scale run | complete: `reports/deepseek_v4_flash_benqa_ext_full851.md` | Collected 2,553/2,553 rows with STOP=2,553 and 0 parsed-empty rows. Accuracy is 665/851 Bangla, 376/851 reviewed Banglish, and 697/851 English; paired gaps are -33.96 pts Banglish-Bangla, -37.72 pts Banglish-English, and +3.76 pts English-Bangla. Use as historical API support behind the human-reviewed 974-row panel. |
| 0 | BEnQA human-gold 974 six-row scale panel | complete: `reports/benqa_human_gold_974_scale_summary.md` | Use as the thesis-facing BEnQA scale result. Gemini 3.5 Flash, GPT-5.5 none, Claude Sonnet 4.6, DeepSeek V4 Flash, Groq Llama 3.3 70B, and Qwen2.5-3B all keep reviewed Banglish below Bangla. |
| 0 | Gemini/GPT/Claude BEnQA human-gold 974 API audits | complete: `reports/gemini_3_5_flash_benqa_human_gold_974.md`, `reports/openai_gpt55_none_benqa_human_gold_974.md`, `reports/claude_sonnet_4_6_benqa_human_gold_974.md` | Use as the completed paid-provider scale add-on. GPT-5.5 none is the largest story update: it nearly closes the mixed-task validation gap, but remains -12.42 points behind Bangla on the BEnQA scale layer. |
| 0 | GPT-5.5 low diagnostic 60-item hard slice | complete: `reports/openai_gpt55_low_diagnostic_60_v5_cap1024_results.md` | Use as targeted frontier evidence, not a population estimate: on the same selected Banglish requests GPT-5.5 improves over Gemini by +60.0 strict points and +28.3 secondary points, while cap-256 produced 4 no-answer failures in 70 partial calls. |
| 0 | `munimthahmid/qwen3-4b-generated-bn-dev50` | complete: `reports/qwen3_4b_generated_bn_answer_audit_dev50.md` | Keep BNB protected as a weak dev-only lead; do not launch test150 or claim mitigation without generated-English routing. |
| 0 | `munimthahmid/qwen3-4b-generated-en-dev50` | complete: `reports/qwen3_4b_generated_view_agreement_route_dev.md` | Do not launch test150; generated-English self-translation is weak and agreement routing gives only +1 on dev. |
| 0 | `munimthahmid/qwen25-3b-generated-bn-dev50` | complete: `reports/qwen25_3b_generated_bn_answer_audit_dev50.md` | Do not launch test150; generated-BN gains are model/generator-specific. |
| 0 | `munimthahmid/fms-byte-generated-bn-dev50` | complete: `reports/fms_byte_protected_generated_bn_dev50_benqa_mcq_audit.md` | Do not escalate; tightened formula-expression gate fails 15/36 rows and 7/36 rows retain Latin residue. |
| 0 | reviewed-v5 protected-v2 generated-BN answer audits | complete: `reports/qwen3_4b_generated_bn_v5_pv2_dev50.md`, `reports/qwen25_3b_generated_bn_v5_pv2_dev50.md` | Do not launch test150; tightened formula gate fails 16/36 rows and gate-eligible gains are only 0 to +1 item depending on model/generator. |
| 0 | reviewed-v5 protected-v3 generated-BN answer audits | complete: `reports/qwen3_4b_generated_bn_v5_pv3_dev50.md`, `reports/qwen25_3b_generated_bn_v5_pv3_dev50.md` | Do not launch test150 from generated-BN alone; preservation is repaired, but answer gains are small. |
| 0 | guarded generated-English + protected-v3 route audits | complete: `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`, `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`, `reports/generated_view_route_bottleneck_analysis.md`, `reports/generated_view_routing_candidate_scan.md` | Do not launch test150; guarded EN passes hard preservation but 15/36 rows are source fallbacks, Qwen3 routing is only +1 item, and Qwen2.5 routing is -1 item. Bottleneck and candidate-rule scans show strict agreement is too sparse while looser rules are volatile. |
| 0 | reviewed-v5 BEnQA option-permutation dev probe | complete: `reports/v5_benqa_option_permutation_probe_results.md` | Keep dev-only as behavioral evidence: on Qwen3 identity wrong-D items, 35/45 rotations stay literal label D while only 6/45 follow original-D content; Qwen2.5-3B trends the other way at 5/21 versus 12/21. Do not claim an internal causal mechanism or launch an adjacent Qwen-only probe without a distinct question. |
| 0 | BnSentMix natural code-mixed sentiment external validation | complete: `reports/bnsentmix_external_validation_results.md` | Use as bounded ecological-validity evidence: Qwen2.5-3B scores 89/200, Qwen2.5-7B 8-bit scores 98/200, Qwen3-4B scores 99/200, and all three have 200/200 valid labels. Do not frame it as a paired script-gap estimate. |
| 0 | BnSentMix model complementarity audit | complete: `reports/bnsentmix_model_complementarity.md` | Use as natural-task error-overlap evidence: best single model is 99/200, any-model diagnostic oracle is 154/200, and 66 items are correct for exactly one model. Do not present the oracle as deployable accuracy. |
| 0 | BnSentMix routing dev-test audit | complete: `reports/bnsentmix_routing_devtest.md` | Use as the deployment boundary for the complementarity result: majority + Qwen2.5-7B fallback reaches 106/200 under hash5 CV, but pilot40 holdout is 72/160 and block40 CV is 84/200. Do not call it a solved ensemble. |
| 1 | `Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0` pilot20 | complete: `reports/indic_gemma2b_pilot20_validation200_v4.md` | Do not scale; accuracy was around chance despite clean parsing. |

Pilot20 decision rule:

- Actual result: Bangla 4/20, Banglish 3/20, English 5/20, parsed-empty 0.
- Decision: keep as a diagnostic Indic-family probe and do not spend dev50 or
  test150 on this checkpoint now.

## Launch Next Only If

| Candidate | Launch Condition | Why It Matters | Current Bias |
| --- | --- | --- | --- |
| Human-reviewed v5 slice | Completed: `data/slices/validation_200_v5.jsonl` is frozen after 140/140 reviewed queue rows. | Reduces the largest residual risk: rule-based Banglish naturalness. | Complete; retain the review audit as release evidence. |
| Post-v5 clean-Banglish reruns | Completed for required Qwen2.5-3B and Qwen3-4B rows plus the optional pinned-stack Qwen2.5-7B 8-bit row. | Measures human-reviewed Banglish without rerunning stable Bangla/English baselines. | Complete; use `results/tables/v5_reviewed_banglish_sensitivity.csv`. |
| Frozen-v5 cross-script diagnostic refresh | Completed locally from reviewed Banglish plus unchanged Bangla/English outputs. | Aligns oracle, failure taxonomy, and privileged agreement routing with the final reviewed slice without new inference. | Complete; use `reports/cross_script_diagnostics_validation200_v5.md`. |
| Task-labeled real-Banglish/code-mixed layer | Completed with BnSentMix balanced200 on Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B, plus complementarity and routing dev-test audits. | Adds a natural, human-annotated sentiment task so the thesis is not only controlled curriculum QA/math; complementarity shows model errors are diverse, while route selection shows the deployment boundary. | Complete; use as ecological-validity/error-overlap evidence only. |
| BEnQA human-gold scale evaluation | Smoke, pilot, historical scale runs, and the six-row 974 panel all passed operational gates; every completed scale row has a negative paired Banglish-vs-Bangla gap. | Tests whether the gold-core BEnQA script-gap direction scales beyond 144 reviewed BEnQA rows to a much larger human-reviewed BEnQA-only layer. | Complete. Write it up as the thesis-facing BEnQA scale answer. |
| Deployable consistency route | Only after generated-view prompts, preservation gates, and routing are fixed on dev50. | Turns the privileged answer-agreement diagnostic into a practical mitigation. | Protected-v3 repairs generated-BN preservation and guarded EN repairs hard preservation, but agreement is too sparse and simple looser routing rules are volatile on dev. |
| Controlled frontier API panel | Completed for Gemini, GPT-5.5, Claude Sonnet 4.6, DeepSeek V4 Flash, and Groq Llama 3.3 70B. | Adds cross-family frontier/hosted evidence beyond local Qwen without turning the thesis into an unfocused leaderboard. | Complete for thesis writing; no more validation-200 API rows by default. |
| Additional frontier BEnQA scale add-ons | The six-row 974 human-gold scale panel is complete. | More broad paid rows would mainly create leaderboard breadth, not sharper thesis evidence. | Complete; do not launch additional full-scale paid rows unless a named reviewer-risk question requires it. |
| `fms-byte/banglish_to_bangla` generated-Bengali dry run | Completed as `munimthahmid/fms-byte-generated-bn-dev50` after the v5/review priority work completed. | Public Apache-2.0 MBART transliterator trained on paired Bengali/Romanized text. | Do not escalate: 15/36 formula-expression hard failures, 7/36 lexical-residue warnings, and worse native-reference CER than deterministic protected phonetic. |
| `nahidstaq/bangla-transliteration` generated-Bengali dry run | Only if Hugging Face gated access is available. | Small 6M character transliterator; CPU-feasible. | Candidate after access; no GPU until it passes preservation audit. |
| Better generated-English source for consistency route | Only if generated-view mitigation becomes the focused next question. | Raw Qwen3 self-translation was weak: 7/36 answer accuracy and 16/36 hard preservation failures. Guarded EN fixes preservation but uses 15/36 source fallbacks and does not improve routing enough. | Defer; no test150. |
| GanitLLM math-specialized pilot | Only if math-specialized script behavior becomes a focused question. | Tests Bengali math tuning effects on Bangla/Banglish arithmetic. | Defer; contamination/scope check needed. |

## Do Not Launch Now

| Run | Reason |
| --- | --- |
| Qwen3-8B on Kaggle P100 | 8-bit is blocked by bitsandbytes backend errors; 4-bit is not usable on P100. |
| Full Mistral-7B dev/test | Pilot20 was weak and slow: 3/20 Bangla, 4/20 Banglish, 4/20 English. |
| More plain same-model self-normalization | Qwen2.5-7B dev/test showed dev-only gains can reverse on held-out test. |
| BanglaLLM test150 under current prompt | No-thinking dev50 remained degenerate with high parsed-empty rates. |
| TituLM larger run | Pilot20 produced unrelated prose and zero-score behavior. |
| Indic-Gemma-2B dev50/test150 | Pilot20 was parseable but around chance: Bangla 4/20, Banglish 3/20, English 5/20. |
| MGSM external-normalizer jobs | Validation external-normalization was weak and changed many digit counts. |
| GanitLLM without a focused math-scope decision | Interesting but math-specialized; should not distract from final-scope work. |
| `Tamim18/banglish_to_bangla` on P100 | Llama-3.1 8B 4-bit path is a poor fit for current P100/bitsandbytes limits. |
| `phonetic-bangla` answer routing | Local generated-Bengali smoke failed preservation gates on 36/36 dev50 BEnQA MCQ items, corrupting all option labels. |
| Raw `bnbphoneticparser` answer routing | Local generated-Bengali smoke also failed preservation gates on 36/36 dev50 BEnQA MCQ items, corrupting all option labels. |
| Protected `phonetic-bangla` answer routing | Qwen3 dev-only audit dropped Banglish 15/36 to 11/36. |
| Protected `fms-byte` answer routing | Tightened formula-expression gate now fails 15/36 rows, with 7/36 Latin-residue warnings and worse native-reference CER than deterministic candidates. |
| Reviewed-v5 protected-v2 deterministic generated-BN routing | Formula-expression preservation fails on 16/36 rows for both deterministic generators; answer audits show only 0 to +1 gate-eligible item gains. |
| Reviewed-v5 protected-v3 deterministic generated-BN test150 | Dev answer audits show only Qwen3 BNB +2/36 and Qwen2.5 phonetic +1/36 with wide CIs; guarded generated-English agreement routing is only +1 for Qwen3 and -1 for Qwen2.5. |
| More paid API full triads by default | Gemini, GPT-5.5, Claude, DeepSeek, and Groq validation-200 rows are complete, and the 974-row human-gold BEnQA scale panel now covers Gemini, GPT-5.5 none, Claude, DeepSeek, Groq, and Qwen2.5-3B. More rows would add leaderboard noise rather than thesis clarity. |
| More full-scale frontier rows without a named question | The six-model 974-row human-gold BEnQA panel already answers the scale question: all completed rows keep reviewed Banglish below Bangla. New paid work should be a targeted format-control or mechanism test, not another broad leaderboard row. |
| More Qwen-only BEnQA D-attractor probes without a distinct question | The controlled option-permutation dev audit already separates literal label-D persistence from original-D-content tracking. New GPU work must answer a different mechanism or mitigation question. |

## Thesis Priority Order

1. Integrate the completed five-model validation-200 frontier API panel and
   six-model 974-row human-gold BEnQA scale panel as the core boundary story.
2. Use the frontier result with a clear boundary: GPT-5.5 nearly collapses the
   mixed-task validation gap, but GPT-5.5 none still has a -12.42 point paired
   reviewed-Banglish deficit on the 974-row BEnQA scale layer.
3. Frame the 974-row BEnQA extension as human-reviewed scale evidence, not as
   the older AI-pass-only silver layer.
4. Integrate the completed BnSentMix external layer and routing dev-test audit
   into the write-up as ecological-validity/complementarity evidence, not as
   the main paired script-gap result or a solved deployment method.
5. Do not add paid models or full-scale API sweeps unless they answer a named
   reviewer-risk question.
6. Pause generated-view routing unless a better generated-English source can
   avoid source fallbacks and produce a stronger dev agreement route.
7. Keep any new open/local model-family work behind the pilot20-first policy.

## Current Compute Policy

- Pilot20 first for any new model family.
- Dev50 is allowed only after pilot20 proves parsing/runtime.
- Test150 is allowed only after a pre-set dev50 rule is met.
- 7B/8B runs on P100 require a known-good stack before launch.
