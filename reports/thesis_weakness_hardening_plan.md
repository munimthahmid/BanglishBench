# Thesis Weakness Hardening Plan

Updated: 2026-06-07

## Goal

The goal is not to pretend the thesis has no limitations. A strong thesis makes
the remaining limitations explicit, then shows that the main claim survives the
important objections. The current work is already past the benchmark-only stage;
the next hardening step is to convert the strongest possible examiner criticisms
into either completed analyses, bounded claims, or targeted follow-up runs.

## Current Strong Position

The strongest current result is a model-capability curve:

- Open Qwen baselines show a substantial reviewed-Banglish accuracy deficit
  under a controlled paired Bangla/Banglish/English design.
- Gemini 3.5 Flash is much stronger but preserves a reviewed-Banglish gap on
  both validation-200 and the 974-row human-reviewed BEnQA scale panel.
- GPT-5.5 low on the full validation-200 v5 triad nearly collapses the
  reviewed-Banglish population gap, but GPT-5.5 none on the 974-row BEnQA scale
  panel keeps a clear paired reviewed-Banglish deficit.
- Claude Sonnet 4.6 remains strong but gap-positive, and DeepSeek V4 Flash
  plus Groq-hosted Llama 3.3 70B retain large reviewed-Banglish deficits.

This should be framed as a script-robustness framework: accuracy, strict-format
robustness, recoverability, and reasoning/output cost.

## Weakness Matrix

| Weak point | Why an examiner may press it | Current defense | Hardening action |
| --- | --- | --- | --- |
| "It is just a benchmark." | Dataset papers can sound incremental if no larger finding is extracted. | Controlled paired design, v5 review, five-model frontier panel, broad diagnostics, and BEnQA scale replication. | Build a frontier script robustness and cost curve plus an error-transition map. |
| Dataset is only 200 items. | Small datasets can overfit or miss broad behavior. | Paired design plus a 974-row human-reviewed BEnQA gold/pass extension; six completed model rows keep negative paired reviewed-Banglish gaps. | Integrate the mixed-task validation core plus human-gold BEnQA scale framing into the thesis; no more broad scale model runs by default. |
| Controlled Banglish is not natural Banglish. | Natural Banglish varies by spelling, slang, and code-mixing. | v5 human review, BanglaTLit distribution/coverage audits, BnSentMix natural code-mixed layer. | Add a one-page "controlled vs natural Banglish" scope note linking the paired benchmark and BnSentMix ecological layer. |
| Mitigation is not solved. | A thesis can look incomplete if it only diagnoses a problem. | Prompting and self-normalization were tested and shown brittle; generated-view routing has preservation gates and negative/weak results. | Reframe mitigation as a negative contribution plus run one targeted format-control intervention only if it answers semantic-vs-protocol uncertainty. |
| Mechanism is behavioral, not causal. | Tokenization/failure analysis does not prove internal model mechanisms. | Thesis already avoids internal causal claims and has option-permutation behavioral evidence. | Add a "mechanism boundary" defense slide: ruled out simple causes, did not claim representation causality. |
| Model coverage could be challenged. | Qwen-family baselines may not represent all models. | Phi/Mistral/Indic/Bangla pilots plus Gemini, GPT-5.5, Claude, DeepSeek, and Groq validation-200 API rows. | Stop adding models by default; use the frontier panel as bounded coverage. |
| Strict parser may be unfair. | Strong models may answer correctly in a noncanonical form. | Secondary parser/unit sensitivity is already reported separately. | Make strict-vs-secondary a core thesis metric: strict accuracy measures deployable answer compliance; secondary measures semantic recoverability. |

## Completed Hardening Since This Plan

The dataset-size weakness now has a concrete human-reviewed extension layer:

- `reports/benqa_extension_publication_strategy.md`
- `reports/benqa_extended_1000_v1.md`
- `reports/benqa_extended_1000_v1_ai_review.md`
- `reports/benqa_extended_1000_v1_human_review_freeze.md`
- `reports/benqa_human_gold_974_scale_summary.md`
- `reports/qwen25_3b_benqa_ext_full851.md`
- `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- `reports/gemini_3_5_flash_benqa_human_gold_974.md`
- `reports/openai_gpt55_none_benqa_human_gold_974.md`
- `reports/claude_sonnet_4_6_benqa_human_gold_974.md`
- `reports/deepseek_v4_flash_benqa_ext_full851.md`
- `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`
- `data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl`
- `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- `data/slices/benqa_extended_1000_v1_human_gold.jsonl`

Summary: 1,000 BEnQA extension rows were selected from 4,939 eligible source
rows after excluding the frozen validation core. Human review accepts or edits
974 rows for the gold/pass evaluation set and rejects 26 rows. Six completed
model rows on this 974-row set keep reviewed Banglish below Bangla: Qwen2.5-3B
(-3.90 pts), Groq Llama 3.3 70B (-21.97 pts), Gemini 3.5 Flash (-11.29 pts),
GPT-5.5 none (-12.42 pts), Claude Sonnet 4.6 (-24.64 pts), and DeepSeek V4
Flash (-32.65 pts). This gives the thesis a defensible mixed-task validation
core plus human-gold BEnQA scale structure.

## Highest-Value No-Spend Work

### 1. Frontier Script Robustness And Cost Curve

Create one report and figure that combines:

- Qwen2.5-3B, Qwen2.5-7B, Qwen3-4B, Gemini 3.5 Flash, GPT-5.5 low, Claude
  Sonnet 4.6, DeepSeek V4 Flash, and Groq Llama 3.3 70B.
- Bangla, reviewed Banglish, and English strict accuracy.
- Secondary accuracy where available for the API rows.
- Banglish-minus-Bangla gap.
- Output/reasoning token cost where available.

Expected thesis value: this changes the story from "we evaluated models on a
Banglish benchmark" to "we measured how script robustness changes with model
capability and protocol strictness."

### 2. Cross-Model Error Transition Map

Classify each validation-200 item into transitions such as:

- Open-model Banglish failure fixed by Gemini.
- Gemini Banglish failure fixed by GPT-5.5.
- Strict-only failure recovered by secondary scoring.
- Still hard for GPT-5.5.
- Correct but high-cost/high-output Banglish case.

Expected thesis value: this gives a deeper result than aggregate accuracy and
shows what stronger models are actually fixing.

### 3. Dataset Size And Claim-Scope Memo

Add a short memo explaining:

- Why paired 200-item evaluation is stronger than an unpaired 200-item table.
- Which claims are statistically supported by exact paired tests and bootstrap
  intervals.
- Which claims remain descriptive because strata are small.
- Why BEnQA carries the cleanest open-model script-gap claim and BanglaMATH is
  a stress/protocol test.

Expected thesis value: turns "only 200 items" into "carefully paired,
reviewed, repeatedly audited 200 items with explicit claim boundaries."

### 4. Defense Q&A Refresh

Update the defense answers with the five-model frontier panel and DeepSeek
full851 result. The old defense note still describes frontier API work as
optional/future, so it should be refreshed.

Expected thesis value: prevents stale answers during defense preparation.

## Targeted Paid/GPU Work Only If Needed

### A. Format-Control Micro-Audit

Run only if the no-spend reports show that the remaining frontier uncertainty
is format/protocol rather than model capability.

Recommended scope:

- 40 to 60 items, selected from Gemini strict failures, GPT strict-only
  recoveries, and BanglaMATH unit/numeric cases.
- Same model, same item, two prompt protocols: current free-form answer-only
  versus strict structured answer field.
- Primary question: does stricter output control reduce Banglish strict failure
  without changing semantic accuracy?

This is stronger than adding another full model because it tests the specific
remaining weakness.

### B. Controlled Cross-Family Frontier Panel

Complete. The panel answers:

"Does the GPT-5.5 near-collapse generalize to non-OpenAI frontier families
under the finalized cap and parser protocol?"

Current answer: no. Gemini reduces the gap, Claude remains strong but
gap-positive, and DeepSeek/Groq keep large deficits. The 974-row human-gold
BEnQA scale panel strengthens the answer: Gemini, GPT-5.5 none, Claude,
DeepSeek, Groq, and Qwen2.5-3B all retain negative reviewed-Banglish-minus-
Bangla paired gaps. Do not run more broad scale models by default.

## Claim Framing To Use

Strong version:

"Script choice is a measurable robustness variable. In controlled Bangla
educational QA/math, reviewed Latin-script Banglish degrades competent open
models. Frontier models reduce the mixed-task validation gap, and GPT-5.5
nearly closes it there, but the 974-row human-reviewed BEnQA scale panel shows
that the reviewed-Banglish deficit persists even for strong hosted models."

Avoid:

- "Banglish is universally harder for all models."
- "The benchmark fully represents natural user Banglish."
- "We solved Banglish mitigation."
- "Tokenization causally explains the effect."

## Recommended Next Sprint

1. Write the dataset-size and claim-scope memo around validation-200 plus the
   974-row human-gold BEnQA scale panel.
2. Refresh the defense Q&A with the five-model validation panel and six-model
   human-gold BEnQA scale panel.
3. Build the cross-model error transition map if the paper needs more
   qualitative mechanism evidence.
4. Consider a small format-control micro-audit only if the write-up still needs
   sharper protocol-vs-semantic evidence.

This sequence hardens the thesis without turning it into an unfocused model
leaderboard.
