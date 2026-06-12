# Thesis Results Dashboard

Updated: 2026-06-05

This dashboard consolidates the current thesis-facing evidence for the Script
Matters project. Use it as the first stop before reading the narrower reports.

## Current Bottom Line

The strongest current claim is not merely that models are weak at Bangla. It is
that the same underlying Bangla content becomes substantially harder when it is
written in clean Latin-script Banglish. The effect is visible on validation-200
for competent Qwen2.5/Qwen3 models, survives conservative romanizer cleanup, is
not explained by token count alone, and is not fixed by simple prompting. The
frozen validation-200 v5 review confirms that cleanup does not erase the gap.

The strongest mitigation finding is negative but useful: same-model
self-normalization is model-dependent. It helps Qwen2.5-3B on validation-200 but
does not scale cleanly to Qwen2.5-7B 8-bit and hurts Qwen3-4B on
validation-200 and MGSM. This should be framed as evidence that Banglish
robustness needs reliable normalization, routing, or adaptation, not just a
prompt wrapper.

The latest generated-view diagnostics reinforce the same caution. Reviewed-v5
protected-v2 deterministic generated-Bengali views were answered by Qwen3 and
Qwen2.5, but the tightened formula-expression gate rejects 16/36 rows and
gate-eligible gains are only 0 to +1 item. Protected FMS-byte MBART fails 15/36
formula-expression gates and leaves Latin residue on 7/36 rows. A generated-
English self-translation route gives only a +1 dev gain and should not go to
test150. The new formulaish-token protected-v3 deterministic wrapper clears the
preservation gate, but dev answer gains remain small and uncertain.

The frontier/API panel now has five completed validation-200 v5 rows: Gemini
3.5 Flash, GPT-5.5 low, Claude Sonnet 4.6, DeepSeek V4 Flash non-thinking, and
Groq-hosted Llama 3.3 70B. The panel shows the mixed-task boundary clearly:
GPT-5.5 nearly collapses the validation-200 reviewed-Banglish population gap
under secondary scoring, while Gemini reduces it, Claude remains strong but
format-verbose with a clear deficit, and DeepSeek/Groq show much larger
deficits under the same frozen prompts and parser.

The dataset-size weakness now has a human-reviewed scale answer. A BEnQA-only
extension selected 1,000 rows from 4,939 eligible source rows after excluding
the frozen validation core; human review accepts or edits 974 rows for the
gold/pass evaluation set and rejects 26. The completed 974-row panel now covers
Qwen2.5-3B, Groq Llama 3.3 70B, Gemini 3.5 Flash, GPT-5.5 none, Claude Sonnet
4.6, and DeepSeek V4 Flash. Every row keeps reviewed Banglish below Bangla on
paired items. The most important update is GPT-5.5 none: 820/974 Bangla,
699/974 reviewed Banglish, and 825/974 English, with paired gaps of -12.42
points against Bangla and -12.94 points against English. This turns the earlier
validation-200 GPT boundary into a stronger scale claim: even a very strong
OpenAI row does not erase the human-gold BEnQA reviewed-Banglish deficit.

## Frozen-V5 Core Validation-200 Result

Dataset: `data/slices/validation_200_v5.jsonl`, 200 English-matched items
(144 BEnQA, 56 BanglaMATH). Bangla and English are unchanged from the
historical controlled slice; Banglish uses the completed reviewed-v5 reruns.

| Model | Bangla | Reviewed Banglish | English | Banglish - Bangla | Banglish - English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] |
| Qwen3-4B | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] |

Qwen2.5-7B and Qwen3-4B retain negative all-200 paired intervals. Qwen2.5-3B
retains a -6.5-point deficit, but its reviewed-v5 all-200 interval reaches
zero; its historical v3 and strict-197 checks remain negative.

Historical v3 dataset split for provenance:

Dataset split:

| Model | Dataset | Bangla | Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | BEnQA | 49/144 | 38/144 | 66/144 |
| Qwen2.5-3B | BanglaMATH | 5/56 | 0/56 | 5/56 |
| Qwen3-4B | BEnQA | 76/144 | 45/144 | 82/144 |
| Qwen3-4B | BanglaMATH | 4/56 | 1/56 | 6/56 |

Main artifacts:

- `reports/script_matters_paper_draft.md`
- `reports/main_results_validation200_v5.md`
- `results/tables/main_script_gap_validation200_v5.csv`
- `reports/gemini_3_5_flash_validation200_v5_results.md`
- `reports/openai_gpt55_low_validation200_v5_cap1024_results.md`
- `reports/openai_gpt55_low_diagnostic_60_v5_cap1024_results.md`
- `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md`
- `reports/deepseek_v4_flash_validation200_v5_results.md`
- `reports/groq_llama33_70b_validation200_v5_results.md`
- `reports/frontier_api_panel_validation200_v5.md`
- `reports/benqa_extension_publication_strategy.md`
- `reports/benqa_extended_1000_v1_ai_review.md`
- `reports/qwen25_3b_benqa_ext_smoke26.md`
- `reports/qwen25_3b_benqa_ext_smoke26_paired_gap_analysis.md`
- `reports/benqa_extension_kaggle_pilot130_launch.md`
- `reports/qwen25_3b_benqa_ext_pilot130.md`
- `reports/qwen25_3b_benqa_ext_pilot130_paired_gap_analysis.md`
- `reports/qwen25_3b_benqa_ext_pilot130_recoverable_examples.md`
- `reports/benqa_extension_kaggle_full851_launch.md`
- `reports/qwen25_3b_benqa_ext_full851.md`
- `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- `reports/qwen25_3b_benqa_ext_full851_recoverable_examples.md`
- `reports/deepseek_v4_flash_benqa_ext_full851.md`
- `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`
- `reports/deepseek_v4_flash_benqa_ext_full851_recoverable_examples.md`
- `reports/benqa_gold_core_extension_alignment.md`
- `reports/main_results_validation200.md`
- `results/runs/validation200_v3_128_model_comparison_by_variant_reparsed_rescored.csv`
- `results/analysis/qwen25_validation200_v3_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen3_validation200_v3_banglish_minus_bangla_bootstrap.csv`

## Frontier/API Audit

The main cross-family frontier table is
`reports/frontier_api_panel_validation200_v5.md`. All rows use the same frozen
validation-200 v5 prompt manifest and the same strict parser, with secondary
parser/unit sensitivity reported separately.

| Model | Score | Bangla | Reviewed Banglish | English | Banglish - Bangla | Banglish - English |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | Strict | 163/200 | 136/200 | 144/200 | -13.5 pts | -4.0 pts |
| Gemini 3.5 Flash | Secondary | 170/200 | 161/200 | 165/200 | -4.5 pts | -2.0 pts |
| GPT-5.5 low | Strict | 172/200 | 169/200 | 154/200 | -1.5 pts | +7.5 pts |
| GPT-5.5 low | Secondary | 173/200 | 174/200 | 168/200 | +0.5 pts | +3.0 pts |
| Claude Sonnet 4.6 | Strict | 162/200 | 130/200 | 153/200 | -16.0 pts | -11.5 pts |
| Claude Sonnet 4.6 | Secondary | 167/200 | 133/200 | 166/200 | -17.0 pts | -16.5 pts |
| DeepSeek V4 Flash | Strict | 143/200 | 82/200 | 132/200 | -30.5 pts | -25.0 pts |
| DeepSeek V4 Flash | Secondary | 152/200 | 96/200 | 148/200 | -28.0 pts | -26.0 pts |
| Groq Llama 3.3 70B | Strict | 90/200 | 48/200 | 102/200 | -21.0 pts | -27.0 pts |
| Groq Llama 3.3 70B | Secondary | 92/200 | 56/200 | 111/200 | -18.0 pts | -27.5 pts |

Interpretation: the frontier result is not monotonic. GPT-5.5 is still the
strongest validation-200 boundary case, but the 974-row BEnQA human-gold panel
shows that the boundary does not generalize into a solved scale result. Gemini,
GPT-5.5 none, Claude, DeepSeek, Groq, and Qwen2.5-3B all retain negative
reviewed-Banglish-minus-Bangla paired gaps on the larger BEnQA set. Gemini and
Claude additionally show strict-format instability through verbose or truncated
noncanonical answers, so report their rows as strict parser results with a
format/protocol caveat.

## Robustness Checks

Noisy Banglish:

| Model | Clean Banglish | Noisy Banglish | Interpretation |
| --- | ---: | ---: | --- |
| Qwen2.5-3B | 38/200 | 41/200 | Deterministic noise is not causing the gap. |
| Qwen3-4B | 46/200 | 46/200 | Noise is neutral on this slice. |

Romanizer v4 cleanup:

| Model | v3 Banglish | v4 Banglish | Interpretation |
| --- | ---: | ---: | --- |
| Qwen2.5-3B | 38/200 | 39/200 | Dataset cleanup does not remove the gap. |
| Qwen3-4B | 46/200 | 47/200 | Same conclusion. |

Broader auto-suggested cleanup:

| Model | v4 Banglish | Auto-suggested | Interpretation |
| --- | ---: | ---: | --- |
| Qwen2.5-3B | 39/200 | 40/200 | +1 item; not material. |
| Qwen3-4B | 47/200 | 48/200 | +1 item; not material. |

Frozen v5 reviewed Banglish:

| Model | v4 Banglish | v5 reviewed | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 39/200 | 41/200 | +1.0 pts, CI [-1.0, +3.0] |
| Qwen3-4B | 47/200 | 49/200 | +1.0 pts, CI [0.0, +2.5] |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-3.5, +2.5] |

The reviewed shifts are small. Cleanup does not materially alter the script-gap
interpretation.

Flagged-bad denominator policy:

| Model | Strict policy | Reviewed Banglish - Bangla | 95% CI |
| --- | --- | ---: | --- |
| Qwen2.5-3B | 197 rows | -7.1 pts | [-13.2, -1.0] |
| Qwen3-4B | 197 rows | -15.7 pts | [-22.3, -9.6] |
| Qwen2.5-7B 8-bit | 197 rows | -9.6 pts | [-16.8, -2.5] |

The strict view is secondary; the frozen all-200 denominator remains primary.

Tokenization:

| Dataset | Bangla tokens/word | Reviewed Banglish tokens/word | English tokens/word |
| --- | ---: | ---: | ---: |
| BEnQA | 4.0242 | 2.4942 | 1.9545 |
| BanglaMATH | 4.6285 | 2.1114 | 1.4080 |

For the three thesis-facing Qwen tokenizers, reviewed Banglish is much cheaper
than native Bangla, yet accuracy is lower. The frozen-v5 token/failure join
also shows recoverable BEnQA Banglish misses are shorter than other rows for
Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B. Token count alone is therefore not a
sufficient explanation.

Main artifacts:

- `reports/noisy_banglish_validation200.md`
- `reports/v4_banglish_sensitivity_validation200.md`
- `reports/validation200_v4_auto_suggested_sensitivity.md`
- `results/tables/v5_reviewed_banglish_sensitivity.csv`
- `reports/v5_bad_row_policy_sensitivity.md`
- `reports/tokenization_validation200.md`
- `reports/tokenization_cross_script_failure_patterns.md`
- `reports/banglish_human_review_workflow_v5.md`

## Mitigation Results

The validation-200 mitigation rows below intentionally retain historical v3/v4
outputs. They diagnose mitigation behavior; they are not frozen-v5 main-result
reruns.

Validation-200 self-normalization:

| Model | Baseline Banglish | Self-normalized | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +6.5 pts, CI [+0.5, +13] |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-7, +6.5] |
| Qwen3-4B | 46/200 | 21/200 | -12.5 pts, CI [-19.5, -5.5] |

Qwen2.5-7B self-normalization is a dev/test caution: dev50 improved 13/50 ->
18/50, but held-out test150 dropped 35/150 -> 29/150.
The follow-up routing scan is also cautious: dev-best answer-signal routing
failed on test, while a BanglaMATH-only route modestly improved held-out
test150 from 35/150 to 38/150.

MGSM transfer:

| Model | Baseline Banglish | Self-normalized | English pivot |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 0/50 | 0/50 | not run |
| Qwen3-4B | 5/50 | 0/50 | 2/50 |

Self-normalization routing:

| Model | Always baseline | Always selfnorm | Best simple routing tried | Oracle union |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | 51/200 | 65/200 |
| Qwen3-4B | 46/200 | 21/200 | 49/200 | 59/200 |

Interpretation: there is recoverable signal, but the simple routing heuristics
are not enough. Qwen3's only simple improvement came from a task-aware rule
using self-normalization only on BanglaMATH.

Dev/test routing check:

| Model | Selected on dev | Dev selected | Test baseline | Test selected |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | selfnorm if options preserved | 10/50 | 31/150 | 41/150 |
| Qwen3-4B | selfnorm if BanglaMATH | 15/50 | 32/150 | 34/150 |

Main artifacts:

- `reports/selfnorm_validation200.md`
- `reports/qwen25_7b_8bit_selfnorm_validation200_v4.md`
- `reports/qwen25_7b_8bit_selfnorm_routing_devtest.md`
- `reports/selfnorm_oracle_routing_validation200.md`
- `reports/selfnorm_routing_heuristics_validation200.md`
- `reports/selfnorm_routing_devtest_validation200_v4.md`
- `reports/mgsm_selfnorm_answer_signal_routing_transfer.md`
- `reports/mitigation_summary.md`

## Model Scaling

This historical cross-model matrix intentionally retains each model's
available v3/v4 output. Use the frozen-v5 core table above for final
three-model release numbers.

| Model | Bangla | Banglish | English | Thesis use |
| --- | ---: | ---: | ---: | --- |
| Qwen2.5-0.5B | 40/200 | 44/200 | 40/200 | Too weak/noisy for the main claim. |
| Qwen2.5-1.5B | 46/200 | 38/200 | 72/200 | Clear English gap, weaker Bangla gap. |
| Qwen2.5-3B | 54/200 | 38/200 | 71/200 | Main Qwen2.5 result. |
| Qwen2.5-7B 8-bit | 65/200 | 48/200 | 94/200 | Stronger Qwen2.5 scaling point; gap persists. |
| Qwen3-1.7B no-thinking | 34/200 | 36/200 | 61/200 | English gap, no Banglish-below-Bangla gap. |
| Qwen3-4B | 80/200 | 46/200 | 88/200 | Strongest open-model result. |

Interpretation: the script gap becomes most meaningful once the model has enough
task competence. The 0.5B model is not a good evidence anchor.

Qwen3-8B 8-bit was attempted as the next stronger Qwen3 scaling point, but is
blocked on Kaggle P100 by bitsandbytes backend compatibility. Do not treat its
absence as a research choice; it is a compute/runtime constraint.

Mistral-7B-Instruct-v0.3 is feasible in 8-bit on P100 but the pilot20 was weak
and slow: Bangla 3/20, Banglish 4/20, English 4/20. Keep it diagnostic unless a
specific non-Qwen 7B comparison becomes necessary.

Indic-Gemma-2B Navarasa is feasible and parseable with an Alpaca wrapper, but
pilot20 was also weak: Bangla 4/20, Banglish 3/20, English 5/20. Do not scale
it to dev50 under the current protocol.

Main artifact:

- `reports/qwen_scaling_validation200.md`
- `reports/qwen25_7b_8bit_dev50_probe.md`
- `reports/qwen25_7b_8bit_validation200_v4.md`
- `reports/qwen3_1_7b_nothink_validation200_v4.md`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/qwen3_8b_8bit_pilot20_failure.md`
- `reports/mistral7b_8bit_pilot20_validation200_v4.md`
- `reports/indic_gemma2b_pilot20_validation200_v4.md`

## Model-Family Breadth

Phi-3.5-mini gives a useful non-Qwen contrast:

| Model | Bangla | Banglish | English | Banglish - Bangla | Banglish - English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Phi-3.5-mini | 38/200 | 40/200 | 80/200 | +1 pt, CI [-4, +6] | -20 pts, CI [-28, -11.5] |

Interpretation: Phi does not replicate the Qwen Banglish-below-Bangla ordering,
but it does show a large English-vs-Banglish gap. Use it as breadth and nuance:
script/language choice strongly changes behavior, while the specific
Banglish-below-Bangla deficit is strongest in the Qwen models tested so far.

Main artifact:

- `reports/phi35_mini_validation200_v4.md`
- `reports/model_family_scaling_synthesis_validation200.md`

## Natural Code-Mixed External Layer

The BnSentMix layer adds a task-labeled natural Bengali-English code-mixed
sentiment check. It is not paired by script, so it broadens ecological validity
without replacing the controlled validation-200 script-gap estimate.

| Model | Rows | Valid outputs | Correct | Accuracy | Macro-F1 | Main weakness |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Qwen2.5-3B | 200 | 200/200 | 89/200 | 44.5% | 0.431 | Neutral recall is 20%; mixed recall is 42%. |
| Qwen2.5-7B 8-bit | 200 | 200/200 | 98/200 | 49.0% | 0.479 | Neutral overprediction: predicts neutral on 92/200 rows. |
| Qwen3-4B | 200 | 200/200 | 99/200 | 49.5% | 0.486 | Strong positive-label bias: predicts positive on 106/200 rows. |

Complementarity is large: the best single row is Qwen3-4B at 99/200, but the
any-model diagnostic oracle reaches 154/200, a +27.5 point bootstrap interval
over the best single row. This is an upper bound showing error diversity, not a
deployable ensemble.

Routing stress test: `reports/bnsentmix_routing_devtest.md` shows the practical
version is weaker. Hash5 cross-validation consistently selects majority vote
with Qwen2.5-7B fallback and reaches 106/200, but the ordered pilot40 ->
holdout160 split reaches only 72/160 and block40 cross-validation reaches
84/200. Use this as evidence that the complementarity is meaningful but not yet
a deployable mitigation.

Main artifacts:

- `reports/bnsentmix_external_validation_slice.md`
- `reports/bnsentmix_external_validation_results.md`
- `reports/bnsentmix_model_complementarity.md`
- `reports/bnsentmix_routing_devtest.md`
- `results/tables/bnsentmix_external_validation.csv`
- `results/tables/bnsentmix_model_complementarity.csv`
- `results/tables/bnsentmix_routing_devtest.csv`

## Cross-Script Oracle

The oracle and agreement rows below use frozen-v5 reviewed Banglish outputs.
Bangla and English outputs are reused because those fields did not change.
They remain diagnostic recoverability analyses, not deployed accuracy.

| Model | Banglish only | Any-script oracle | BEnQA oracle |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 99/200 | 92/144 |
| Qwen2.5-7B 8-bit | 47/200 | 115/200 | 105/144 |
| Qwen3-4B | 49/200 | 108/200 | 102/144 |

Many Banglish failures are not impossible items. The same model often answers
the item under another script, which supports the thesis that script changes
access to task knowledge rather than merely selecting harder questions.

Cross-script answer agreement:

| Model | Banglish only | Bangla+English agreement route | Route delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5, +8.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5, +17.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0, +19.0] |

This is a privileged diagnostic because it uses the benchmark's parallel Bangla
and English views. Use it to motivate future consistency/routing methods, not
as deployed accuracy.

The reviewed-v5 route interval remains clearly positive for Qwen2.5-7B 8-bit
and Qwen3-4B. The Qwen2.5-3B point gain remains positive, but its interval
crosses zero.

Main artifact:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/deployable_consistency_mitigation_plan.md`
- `reports/generated_view_preservation_audit_v2.md`

Generated-view dev diagnostics:

The first answer rows below are historical protected-v1 diagnostics. They
predate the tightened formula gate and should not be treated as route-ready
results. Reviewed-v5 protected-v2 answer audits are listed separately because
their outputs now fail the formula-expression gate on 16/36 rows.

| Model/route | Banglish | Generated-BN / Generated-EN | Routed | Decision |
| --- | ---: | ---: | ---: | --- |
| Qwen3 protected BNB generated-BN | 15/36 | 17/36, +5.6 pts CI [-8.3,+19.4] | n/a | Weak dev-only lead. |
| Qwen3 protected phonetic generated-BN | 15/36 | 11/36, -11.1 pts CI [-25.0,+2.8] | n/a | Drop for Qwen3. |
| Qwen2.5 protected phonetic generated-BN | 8/36 | 14/36, +16.7 pts CI [0.0,+33.3] | n/a | Model-specific dev lead. |
| Qwen2.5 protected BNB generated-BN | 8/36 | 7/36, -2.8 pts CI [-16.7,+11.1] | n/a | Drop for Qwen2.5. |
| Qwen3 BNB generated-BN + Qwen3 generated-EN agreement | 15/36 | BN 17/36, EN 7/36 | 16/36 | Do not launch test150. |

Reviewed-v5 protected-v2 answer audits:

| Model/route | Banglish | Generated-BN | Gate-eligible result | Decision |
| --- | ---: | ---: | ---: | --- |
| Qwen3 protected-v2 phonetic | 15/36 | 13/36 | 9/20 vs Banglish 10/20 | Gate-blocked; no lead. |
| Qwen3 protected-v2 BNB | 15/36 | 16/36 | 11/20 vs Banglish 10/20 | Gate-blocked; +1 eligible item only. |
| Qwen2.5 protected-v2 phonetic | 9/36 | 10/36 | 5/20 vs Banglish 5/20 | Gate-blocked; flat eligible result. |
| Qwen2.5 protected-v2 BNB | 9/36 | 8/36 | 6/20 vs Banglish 5/20 | Gate-blocked; +1 eligible item only. |

Reviewed-v5 protected-v3 answer audits:

| Model/route | Banglish | Generated-BN | Bootstrap | Decision |
| --- | ---: | ---: | ---: | --- |
| Qwen3 protected-v3 phonetic | 15/36 | 14/36 | -2.8 pts CI [-16.7,+11.1] | Drop for Qwen3. |
| Qwen3 protected-v3 BNB | 15/36 | 17/36 | +5.6 pts CI [-8.3,+19.4] | Weak dev-only lead. |
| Qwen2.5 protected-v3 phonetic | 9/36 | 10/36 | +2.8 pts CI [-13.9,+19.4] | Weak/flat dev result. |
| Qwen2.5 protected-v3 BNB | 9/36 | 9/36 | +0.0 pts CI [-19.4,+19.4] | Flat. |

New formal-gate-only candidates:

| Generator | Hard failures | Latin residue warnings | Native-reference mean CER | Decision |
| --- | ---: | ---: | ---: | --- |
| Reviewed-v5 protected-v2 phonetic | 16/36 | 0/36 | n/a | Formula-expression gate blocks route. |
| Reviewed-v5 protected-v2 BNB | 16/36 | 0/36 | n/a | Formula-expression gate blocks route. |
| Reviewed-v5 protected-v3 phonetic | 0/36 | 0/36 | n/a | Gate-passing; answer gains small. |
| Reviewed-v5 protected-v3 BNB | 0/36 | 0/36 | n/a | Gate-passing; Qwen3 weak lead only. |
| Protected FMS-byte MBART | 15/36 | 7/36 | 0.1855 | Do not escalate. |

Generated-view artifacts:

- `reports/qwen3_4b_generated_bn_answer_audit_dev50.md`
- `reports/qwen25_3b_generated_bn_answer_audit_dev50.md`
- `reports/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_selftranslate_guarded_v5_generated_en_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_guarded_generated_en_v5_dev50.md`
- `reports/qwen25_3b_guarded_generated_en_v5_dev50.md`
- `reports/qwen3_4b_generated_view_agreement_route_dev.md`
- `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`
- `results/tables/generated_bn_candidate_preservation.csv`
- `results/tables/generated_bn_reference_similarity_dev50.csv`
- `reports/qwen3_4b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen3_4b_generated_bn_v5_pv3_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv3_dev50.md`
- `reports/phonetic_bangla_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`

## Subject Spread

Qwen3's frozen-v5 BEnQA Banglish gap is not concentrated in a single subject:
reviewed Banglish is below Bangla in 12 of 13 BEnQA subject strata, with only
Math-II slightly positive. Qwen2.5-7B 8-bit is below Bangla in 8 of 13 strata,
and Qwen2.5-3B is more mixed at 7 of 13, matching its smaller overall
Banglish-vs-Bangla gap. BanglaMATH remains too low-accuracy for fine-grained
grade-level conclusions.

Main artifact:

- `reports/subject_breakdown_validation200_v5.md`

## Thesis Claims That Are Safe Today

1. Reviewed Banglish point accuracy is below native Bangla for Qwen2.5-3B,
   Qwen2.5-7B, and Qwen3-4B on the validation-200 slice. The all-200 paired
   interval remains negative for Qwen2.5-7B and Qwen3-4B; Qwen2.5-3B reaches
   zero but remains negative under strict-197.
2. The gap is not removed by conservative romanizer cleanup, broader automatic
   spelling suggestions, the frozen reviewed-v5 cleanup, or the current noisy
   Banglish generator.
3. Token count alone does not explain the gap because Qwen tokenizers encode
   Banglish more cheaply than Bangla.
4. Same-model mitigation is brittle: self-normalization helps Qwen2.5-3B on
   validation-200, is flat for Qwen2.5-7B 8-bit after held-out testing, and
   hurts Qwen3 on validation-200 and MGSM.
   Exploratory answer-side routing recovers some of the lost Qwen3 signal:
   `selfnorm if parsed answer non-empty` gives 40/150 on test vs 32/150
   baseline, CI delta [+1.3, +10.0]. The same rule does not transfer to MGSM.
5. Cross-script oracle results show that many Banglish misses are recoverable
   in principle.
6. Cross-script answer agreement shows a non-oracle consistency signal:
   Bangla+English agreement against reviewed Banglish recovers 49/200 for
   Qwen2.5-3B, 71/200 for Qwen2.5-7B, and 76/200 for Qwen3-4B, but only as a privileged
   diagnostic.
7. Reviewed-v5 item-level failure taxonomy shows recoverable Banglish misses:
   58/200 for Qwen2.5-3B, 68/200 for Qwen2.5-7B, and 59/200 for Qwen3-4B.
8. Reviewed-v5 fragility feature analysis shows 185/600 thesis-facing Qwen
   model-item slots where reviewed Banglish is wrong while Bangla or English is
   correct; these recoverable events concentrate in BEnQA MCQ science domains.
   Model-overlap analysis shows 56/108 any-fragile items affect at least two
   Qwen rows, while 52 affect exactly one model.
9. A controlled dev-only BEnQA option-permutation probe strengthens the Qwen3
   failure-mode interpretation: on identity wrong-D items, 35/45 rotated rows
   remain attached to literal label D while only 6/45 follow original-D
   content. Qwen2.5-3B trends the other way at 5/21 versus 12/21. This is
   behavioral evidence for a label-position D-attractor, not internal causal
   proof: `reports/v5_benqa_option_permutation_probe_results.md`.
10. The frontier/API panel now has five completed validation-200 v5 rows:
    Gemini 3.5 Flash, GPT-5.5 low, Claude Sonnet 4.6, DeepSeek V4 Flash, and
    Groq-hosted Llama 3.3 70B. GPT-5.5 nearly collapses the mixed-task
    validation gap, but the new 974-row BEnQA human-gold panel shows the scale
    deficit persists across Gemini, GPT-5.5 none, Claude, DeepSeek, Groq, and
    Qwen2.5-3B.
11. The GPT-5.5 full all-200 audit remains the strongest validation boundary:
    reviewed Banglish is only -1.5 strict points behind Bangla and is +0.5
    points ahead under secondary parser/unit scoring. The 974-row GPT-5.5 none
    BEnQA run now supplies the complementary scale result: reviewed Banglish is
    -12.42 points behind Bangla and -12.94 points behind English.
12. The BEnQA extension now addresses the dataset-size objection with a
    two-tier design: validation-200 v5 remains the mixed-task human-reviewed
    gold core, while the 974-row human-reviewed BEnQA gold/pass panel is the
    thesis-facing scale layer. All six scale rows preserve a negative
    reviewed-Banglish-vs-Bangla paired gap; GPT-5.5 none is -12.42 points,
    Gemini 3.5 Flash is -11.29 points, Claude Sonnet 4.6 is -24.64 points,
    DeepSeek V4 Flash is -33.96 points, Groq Llama 3.3 70B is -38.81 points,
    and Qwen2.5-3B is -5.05 points.

## Claims To Avoid For Now

1. Do not claim the frozen reviewed dataset fully represents natural human
   Banglish. It is a controlled educational benchmark, not a user-conversation
   sample.
2. Do not claim noisy Banglish is solved. The current noise generator is a
   deterministic stress test, not a realistic user corpus.
3. Do not claim tokenization is irrelevant. The current evidence says token
   count alone is insufficient, not that tokenization has no role.
4. Do not claim self-normalization is a general solution. It is strongly
   model-dependent and task-sensitive.
5. Do not claim generated-view routing is solved. Raw generated-English
   quality is weak; guarded generated-English uses source fallback on 15/36
   rows; and generated-BN gains are model/generator-specific.
6. Do not let the older AI-triaged extension replace the newer 974-row
   human-reviewed BEnQA panel. The older Qwen2.5-3B and DeepSeek scale runs
   remain historical support; the six-row 974 panel is the current scale
   evidence.

## Next High-Value Work

1. Integrate the completed five-model validation-200 frontier panel and the
   six-model 974-row human-reviewed BEnQA scale panel into the thesis chapters.
2. Preserve the completed dev/test protocol for any future routing or prompt
   choices: `reports/devtest_protocol_validation200_v4.md`.
3. Avoid more Qwen-only scaling unless it answers a specific mechanism or
   mitigation question. Qwen2.5-7B is already folded into the current scaling
   narrative.
4. Pause generated-view routing unless a better generated-English source is
   chosen. Current guarded generated-view dev artifacts show only +1 routed
   gain for Qwen3 and -1 for Qwen2.5; bottleneck analysis also shows strict
   agreement misses most generated-view oracle recoveries, so they should not
   be promoted to test150:
   `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`.
5. Use the completed BanglaTLit comparison as limitations/motivation evidence,
   not as a replacement benchmark.
   Current report: `reports/real_banglish_distribution_comparison.md`.
6. Do not spend held-out test150 GPU on the current BanglaLLM checkpoint. The
   no-thinking dev50 retry remained degenerate, so Bangla-specialized models
   need a prompt/template fix before they can become thesis evidence.
   Current diagnostic note: `reports/bangla_specialized_model_pilots.md`.
