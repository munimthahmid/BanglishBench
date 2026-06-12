# Thesis Defense Q&A Prep

Updated: 2026-06-03

## Purpose

This note turns the current evidence into direct answers for likely thesis
defense questions. It is not a replacement for the full reports; it is the
short, defensible version to rehearse.

## Core Defense Position

The thesis is not that Bangla LLM evaluation is absent, or that every model
always finds Banglish harder than Bangla. The thesis is narrower and stronger:
when the same Bangla educational content is held fixed across native Bangla
script, Latin-script Banglish, and English, script choice itself changes model
behavior. For competent Qwen baselines, clean Banglish is substantially worse
than native Bangla and English, and this cannot be dismissed as a token-length
artifact, noisy romanization artifact, or impossible-item artifact.

## Likely Questions

| Question | Short answer | Evidence to cite |
| --- | --- | --- |
| Why is this novel if Bengali benchmarks already exist? | Recent Bengali benchmarks cover many tasks, but they usually do not isolate orthography while holding item, answer, and task fixed across Bangla, Banglish, and English. | `literature/notes/benchmark_gap_matrix.md`, `literature/notes/script_matters_literature_synthesis.md` |
| Why not claim this is a natural Banglish benchmark? | Because the main validation-200 slice is controlled for paired script comparison. The BnSentMix layer now adds a natural code-mixed sentiment task, but it is unpaired and should be treated as ecological-validity evidence, not as the main script-gap estimate. | `reports/threats_to_validity.md`, `reports/dataset_card_validation200.md`, `reports/real_banglish_distribution_comparison.md`, `reports/bnsentmix_external_validation_results.md` |
| Does the result survive better Banglish spelling? | Yes. After the 140-row v5 review, Qwen2.5-3B changes 39/200 -> 41/200, Qwen3-4B changes 47/200 -> 49/200, and Qwen2.5-7B changes 48/200 -> 47/200. Cleanup improves quality without erasing the gap. | `results/tables/v5_reviewed_banglish_sensitivity.csv` |
| Do the three flagged bad rows drive the result? | No. The preregistered main policy keeps all 200 rows, but a separately reported strict-197 exclusion still gives negative reviewed-Banglish-vs-Bangla CIs for Qwen2.5-3B, Qwen3-4B, and Qwen2.5-7B. | `reports/v5_bad_row_policy_sensitivity.md`, `results/tables/v5_bad_row_policy_sensitivity.csv` |
| Why use Qwen as the main evidence? | Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B are the strongest feasible open baselines we successfully ran at validation-200 scale. They show task competence and clear paired script gaps. | `reports/qwen_scaling_validation200.md`, `reports/model_family_scaling_synthesis_validation200.md` |
| Does every model show Banglish below Bangla? | No. Phi-3.5-mini and Qwen3-1.7B no-thinking do not show a reliable Banglish-below-Bangla gap, though both show a Banglish-vs-English deficit. This is why the thesis avoids universal claims. | `reports/phi35_mini_validation200_v4.md`, `reports/qwen3_1_7b_nothink_validation200_v4.md` |
| Could tokenization explain the whole effect? | Tokenization matters, but token count alone does not explain the result. In frozen-v5, reviewed Banglish is token-cheaper than Bangla for all three thesis-facing Qwen tokenizers, yet the main Qwen models answer less accurately in Banglish; recoverable BEnQA misses are also not the long Banglish prompts. | `reports/tokenization_validation200.md`, `reports/tokenization_cross_script_failure_patterns.md` |
| Is Qwen3's BEnQA D-attractor just the original D answer content? | The controlled dev-only option-permutation probe argues against that narrow explanation. On Qwen3 identity wrong-D items, 35/45 rotated rows remain literal label D while only 6/45 follow original-D content. Qwen2.5-3B trends the other way at 5/21 versus 12/21. This is behavioral failure-mode evidence, not proof of an internal causal mechanism. | `reports/v5_benqa_option_permutation_probe_results.md` |
| Are Banglish items just harder items? | The item ids and gold answers are paired across scripts. Frozen-v5 oracle and transfer analyses show many reviewed-Banglish misses are answered correctly by the same model under Bangla or English. A difficulty-conditioned audit also shows the deficit grows in high-headroom buckets: when all three Qwen rows answer English correctly, reviewed Banglish has 50/147 correct slots versus 92/147 for Bangla. | `reports/cross_script_diagnostics_validation200_v5.md`, `reports/v5_difficulty_conditioned_gap.md` |
| Why does BanglaMATH matter if accuracy is low? | BanglaMATH is a stress test and should not carry the fine-grained script-gap interpretation. The strongest clean script-gap evidence is BEnQA-heavy, especially for Qwen3, where reviewed Banglish is below Bangla in 12/13 BEnQA subject strata. | `reports/main_results_validation200_v5.md`, `reports/subject_breakdown_validation200_v5.md` |
| Did prompting solve it? | No. Simple Banglish-aware and few-shot prompts were neutral or worse in early validation runs. | `reports/mitigation_summary.md`, `results/runs/validation100_v2_banglish_prompt_mitigation_summary_reparsed.csv` |
| Did self-normalization solve it? | Not generally. It helps Qwen2.5-3B, is flat for Qwen2.5-7B after held-out testing, and hurts Qwen3-4B. | `reports/selfnorm_validation200.md`, `reports/qwen25_7b_8bit_selfnorm_validation200_v4.md` |
| What is the strongest mitigation lead? | Frozen-v5 cross-script agreement is the strongest diagnostic signal, but it is privileged because it uses benchmark Bangla and English views. Deployable generated-view routing still needs a better generated-English source and a stronger locked routing signal; strict generated-view agreement misses most recoveries and looser rules are volatile. | `reports/cross_script_diagnostics_validation200_v5.md`, `reports/generated_view_diagnostics_summary.md`, `reports/generated_view_route_bottleneck_analysis.md` |
| Why not run frontier APIs immediately? | Paid APIs are reserved for a budgeted final external-validity audit. The open-model table is now locked enough to justify a 10-item smoke, but exploratory full runs would still waste budget. | `reports/final_api_audit_cost_plan.md`, `reports/api_audit_smoke_subset_v5.md` |
| What remains before a thesis-grade benchmark release? | Decide whether the paid API smoke adds enough external-validity value and run the final release checks. The 140-row v5 review, freeze, three sensitivity reruns, and prose refresh are complete. | `reports/current_research_status_dashboard.md`, `reports/post_v5_thesis_revision_todo.md` |

## Hard Questions And Safe Answers

### Is this a causal mechanism thesis?

No. The thesis gives controlled behavioral evidence and rules out several
simple explanations. It does not claim to prove an internal causal mechanism.
Tokenization and failure-pattern analyses support the interpretation, but a
representation or intervention study would be future work unless added later.

### Is Banglish really a script, language, or transliteration?

For this thesis, Banglish means Bengali-language content written in Latin
script. The important experimental variable is orthography/script encoding,
while the underlying task, meaning, and answer are held fixed.

### Why include English?

English is a control and upper-reference view. It shows whether a model knows
the underlying task content when written in a high-resource Latin-script
language, and it helps separate "Latin characters are easy" from "Bengali
language in Latin script is robust."

### Why not fine-tune a model?

Fine-tuning could be a strong future mitigation, but the current thesis first
establishes and measures the benchmark gap under controlled conditions. Without
that measurement, adaptation gains would be hard to interpret. Given compute
constraints, the thesis prioritizes benchmark quality, paired evaluation, and
low-cost mitigation diagnostics.

### What would make the thesis claim fail?

The narrow main claim would weaken if final frontier API audits showed that
modern strong models are completely robust under the same paired protocol. The
frozen v5 review did not erase the open-model gap: Qwen2.5-3B and Qwen3-4B each
improved by only +1.0 percentage point relative to v4.

## One-Minute Defense Summary

We built a controlled benchmark where Bangla educational QA/math items are held
fixed across native Bangla, Latin-script Banglish, and English. On 200 paired
items, competent open Qwen models lose substantial accuracy on Banglish compared
with Bangla and English. The effect survives romanizer cleanup, is not explained
by token count alone, and many misses are recoverable when the same item is
shown in another script. Simple prompting and self-normalization are not robust
solutions, while cross-script agreement is a strong diagnostic lead that still
needs deployable generated views. The frozen v5 review and required reruns
strengthen the benchmark-quality argument without changing the core result.
