# Chapter 8 Mitigation Draft

Updated: 2026-05-30

## 8.1 Chapter Goal

This chapter evaluates low-cost ways to recover Banglish accuracy. The goal is
not only to find a positive result. Negative mitigation results are important
because they show that Banglish robustness is not fixed by a simple prompt
wrapper or by blindly rewriting Banglish into another script.

The safest current mitigation conclusion is that recovery is possible, but
reliable recovery requires routing, preservation checks, and held-out
evaluation.

The self-normalization tables intentionally retain historical v3/v4 baseline
outputs. The privileged cross-script agreement route is refreshed against
reviewed-v5 Banglish because that update is locally computable without new
model inference.

## 8.2 Prompting Baselines

Simple Banglish-aware instructions and few-shot Banglish prompting were tested
early on validation-100. They did not close the gap. Qwen3-4B was essentially
unchanged, and Qwen2.5-3B showed at most small prompt-specific gains that did
not solve the underlying issue.

Interpretation:

- The models are not merely missing an instruction that the input is Banglish.
- Few-shot prompting can add noise or distract from answer-only format.
- Prompting alone should not be presented as a strong mitigation.

Artifacts:

- `reports/mitigation_summary.md`
- `results/runs/validation100_v2_banglish_prompt_mitigation_summary_reparsed.csv`

## 8.3 Same-Model Self-Normalization

Self-normalization asks the same model to rewrite Banglish into a more standard
form before answering. This is attractive because it does not require an
external model. The results are strongly model-dependent.

| Model | Baseline Banglish | Self-normalized | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +6.5 pts, CI [+0.5, +13.0] |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-7.0, +6.5] |
| Qwen3-4B | 46/200 | 21/200 | -12.5 pts, CI [-19.5, -5.5] |

Qwen2.5-3B improves, but Qwen3-4B degrades sharply. Qwen2.5-7B is especially
important because it prevents a misleading scaling story: dev50 improved from
13/50 to 18/50, but held-out test150 dropped from 35/150 to 29/150. Full200 was
flat overall.

Interpretation:

- Self-normalization can recover signal for one model.
- It is not a general solution.
- Dev-only mitigation gains can reverse on held-out test.

Artifacts:

- `reports/selfnorm_validation200.md`
- `reports/qwen25_7b_8bit_selfnorm_validation200_v4.md`
- `reports/figures/selfnorm_delta.svg`

## 8.4 Answer-Signal Routing

Routing tries to choose between baseline Banglish and self-normalized answers.
The strongest exploratory answer-side rule is:

```text
use self-normalization if the self-normalized answer parses non-empty
```

On test150, this improves Qwen2.5-3B from 31/150 to 43/150 and Qwen3-4B from
32/150 to 40/150. These gains are promising, but they are exploratory because
the candidate rule came from scanning answer-side signals.

| Model | Baseline | Always selfnorm | Routed | Routed - Baseline |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 31/150 | 41/150 | 43/150 | +8.0 pts, CI [+0.7, +15.3] |
| Qwen3-4B | 32/150 | 16/150 | 40/150 | +5.3 pts, CI [+1.3, +10.0] |

The same rule does not transfer to MGSM arithmetic. For MGSM, it routes every
item to self-normalization; Qwen2.5 remains 0/50 and Qwen3 drops from 5/50 to
0/50. This limits the generality of the routing result.

Artifacts:

- `reports/selfnorm_answer_signal_routing_validation200.md`
- `reports/mgsm_selfnorm_answer_signal_routing_transfer.md`
- `results/tables/answer_signal_routing_test150.csv`

## 8.5 Cross-Script Agreement As A Diagnostic Mitigation

Reviewed-v5 cross-script answer agreement is the strongest recovery signal. If
Bangla and English views agree on an answer, replacing the Banglish answer with
that agreement improves point accuracy for all main Qwen baselines.

| Model | Banglish | Agreement route | Route delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5, +8.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5, +17.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0, +19.0] |

This is not deployable as stated because it uses benchmark-provided Bangla and
English views. It should be framed as a diagnostic upper-bound signal and a
design target: if a system can generate or retrieve faithful alternate-script
views, agreement may be useful.

The reviewed-v5 interval remains clearly positive for Qwen2.5-7B 8-bit and
Qwen3-4B. Qwen2.5-3B retains a positive point estimate, but its interval
crosses zero.

Artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/deployable_consistency_mitigation_plan.md`
- `reports/figures/cross_script_recovery.svg`

## 8.6 Generated-View Preservation

Generated-view routing only works if generated views preserve the task. The
audits show this is not automatic.

Raw deterministic Banglish-to-Bangla packages failed preservation on all 36
dev50 BEnQA MCQ generated-Bengali rows because option labels were corrupted.
The historical protected-v1 files used by the first answer audits still fail
the tightened scientific-token gate on 9/36 and 10/36 rows. Reviewed-v5
protected-v2 structural masking was then answered by Qwen3 and Qwen2.5, but the
tightened formula-expression gate rejects 16/36 rows for both deterministic
generators. Formulaish-token protected-v3 now passes 0/36 hard gates, but its
dev-only answer gains remain weak: Qwen3-4B BNB improves 15/36 to 17/36 with a
wide CI crossing zero, while Qwen2.5-3B is flat to +1 item.

Historical protected-v1 generated-BN answer audits were model/generator-specific:

- Qwen3-4B: Banglish 15/36, protected BNB 17/36, protected phonetic 11/36.
- Qwen2.5-3B: Banglish 8/36, protected phonetic 14/36, protected BNB 7/36.

The raw Qwen3 generated-English route was weak: generated-English accuracy was
7/36 and the tightened preservation audit found 16/36 hard failures. A guarded
generated-English repair passes 0/36 hard gates by restoring source
option/answer lines and falling back to the source Banglish row when needed,
but 15/36 rows are source fallbacks. With protected-v3 generated-BN, guarded
agreement routing is still not route-ready: Qwen3 improves only from 15/36 to
16/36 on dev, while Qwen2.5 drops from 9/36 to 8/36.
The bottleneck analysis shows that strict answer agreement is also too sparse:
Qwen3 has 5 baseline-wrong rows recoverable by at least one generated view but
only 1 recovered by generated-BN/generated-EN agreement, and Qwen2.5 has 10
such rows with 0 recovered by agreement.
A simple deployable rule scan does not solve this. Qwen3's best guarded
answer-level rules reach 17/36, only +2 over Banglish; Qwen2.5's best reaches
13/36, but with 5 losses and no matching Qwen3 improvement. The only weakly
positive rule on both current guarded routes is generated-BN-only, which is
already too uncertain as a generated-BN-only effect.

A protected `fms-byte/banglish_to_bangla` MBART Kaggle dry run adds a useful
negative result. Under the tightened formula-expression gate it fails 15/36
rows, leaves genuine Latin residue on 7/36 rows, and has worse privileged
native-reference mean CER than deterministic protected phonetic generation
(0.1855 vs 0.0906). Formal preservation is therefore necessary but not
sufficient for lexical quality, and the gate itself must include formula-like
operators rather than only chemistry-style tokens.

Interpretation:

- Generated views need preservation gates before answer evaluation.
- Generator choice interacts with model choice.
- Gate-passing structure alone is not enough: the protected-v2 answer effects
  were at most +1 gate-eligible item on reviewed-v5 dev.
- Protected-v3 repairs formula preservation, and guarded generated-English
  repairs hard preservation, but the resulting agreement route is only
  +1 item for Qwen3 and -1 item for Qwen2.5.
- Strict generated-view agreement misses most generated-view oracle recoveries,
  so future work needs either better agreement or a stronger pre-registered
  routing signal.
- Looser answer-level rules can recover more dev items but add losses and are
  too model-specific for a held-out launch.
- Current cheap generated-view routes are diagnostics, not held-out
  mitigations.

Artifacts:

- `reports/generated_view_diagnostics_summary.md`
- `reports/generated_view_preservation_audit_v2.md`
- `reports/qwen3_4b_generated_bn_answer_audit_dev50.md`
- `reports/qwen25_3b_generated_bn_answer_audit_dev50.md`
- `reports/qwen3_4b_generated_view_agreement_route_dev.md`
- `reports/qwen3_4b_selftranslate_guarded_v5_generated_en_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_guarded_generated_en_v5_dev50.md`
- `reports/qwen25_3b_guarded_generated_en_v5_dev50.md`
- `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/generated_view_route_bottleneck_analysis.md`
- `reports/generated_view_routing_candidate_scan.md`
- `reports/qwen3_4b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen3_4b_generated_bn_v5_pv3_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv3_dev50.md`
- `reports/phonetic_bangla_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `results/tables/generated_bn_answer_audit_dev50.csv`
- `results/tables/generated_bn_candidate_preservation.csv`
- `results/tables/generated_bn_reference_similarity_dev50.csv`

## 8.7 External Normalization And English Pivot

External normalization and English-pivot self-translation were also tested in
smaller validation/MGSM probes. Under the current setup, they were weak or
harmful. Some outputs changed digits or otherwise altered key task content.

These results should not be interpreted as proof that external normalization is
bad. They show that normalization quality, domain fit, and preservation checks
are central. A stronger transliterator or translation model may still be a good
future mitigation, but it must pass the same preservation and dev/test gates.

Artifacts:

- `reports/mitigation_summary.md`
- `reports/mgsm_bn50_v1_to_v2_banglish_diff.md`
- `reports/qwen3_4b_mgsm_bn50_selftranslate_examples_reparsed.md`

## 8.8 Chapter Conclusion

The mitigation story is deliberately cautious. Simple prompts do not close the
Banglish gap. Self-normalization can help one model and hurt another. Routing
can recover signal, but exploratory rules must be locked before held-out claims.
Cross-script agreement is a strong diagnostic target, but deployable generated
views need strict preservation gates. The practical conclusion is that Banglish
robustness needs explicit script-aware evaluation and reliability checks, not
just bigger models or generic prompt wrappers.
