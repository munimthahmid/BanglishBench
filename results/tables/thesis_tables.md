# Generated Thesis Tables

Generated from authoritative CSV artifacts. Re-run:

```bash
python3 scripts/build_thesis_tables.py
```

## Frozen V5 Main Script Gap

| Model | Slice | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | validation_200_v5 | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] | Point deficit remains; all-200 CI reaches zero. Historical v3 and strict-197 checks remain negative. |
| Qwen2.5-7B 8-bit | validation_200_v5 | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] | Reviewed gap remains reliable at the stronger Qwen2.5 scaling point. |
| Qwen3-4B | validation_200_v5 | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] | Strongest reviewed open-model gap. |

## Main Script Gap

| Model | Family | Slice | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | Qwen2.5 | validation_200_v3 | 54/200 | 38/200 | 71/200 | -8.0 pts, CI [-14.0, -2.0] | -16.5 pts, CI [-24.0, -9.0] | Main Qwen2.5 evidence for clean Banglish below native Bangla. |
| Qwen2.5-7B 8-bit | Qwen2.5 | validation_200_v4 | 65/200 | 48/200 | 94/200 | -8.5 pts, CI [-15.5, -1.5] | -23.0 pts, CI [-30.5, -15.5] | Strong Qwen2.5 scaling point; Banglish-below-Bangla persists at 7B. |
| Qwen3-4B | Qwen3 | validation_200_v3 | 80/200 | 46/200 | 88/200 | -17.0 pts, CI [-23.5, -10.5] | -21.0 pts, CI [-28.5, -13.5] | Strongest open-model evidence; robust Banglish-below-Bangla and Banglish-below-English gaps. |

## Model Family And Scaling

| Model | Family | Slice | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-0.5B | Qwen2.5 | validation_200_v3 | 40/200 | 44/200 | 40/200 | +2.0 pts, CI [-2.5, +7.0] | +2.0 pts, CI [-3.0, +7.5] | Too weak/noisy; not useful as a main script-gap anchor. |
| Qwen2.5-1.5B | Qwen2.5 | validation_200_v3 | 46/200 | 38/200 | 72/200 | -4.0 pts, CI [-10.0, +2.0] | -17.0 pts, CI [-24.5, -9.5] | English-vs-Banglish gap appears before Banglish-vs-Bangla is clearly separated. |
| Qwen2.5-3B | Qwen2.5 | validation_200_v3 | 54/200 | 38/200 | 71/200 | -8.0 pts, CI [-14.0, -2.0] | -16.5 pts, CI [-24.0, -9.0] | Main Qwen2.5 evidence for clean Banglish below native Bangla. |
| Qwen2.5-7B 8-bit | Qwen2.5 | validation_200_v4 | 65/200 | 48/200 | 94/200 | -8.5 pts, CI [-15.5, -1.5] | -23.0 pts, CI [-30.5, -15.5] | Strong Qwen2.5 scaling point; Banglish-below-Bangla persists at 7B. |
| Qwen3-1.7B no-thinking | Qwen3 | validation_200_v4 | 34/200 | 36/200 | 61/200 | +1.0 pts, CI [-6.0, +7.5] | -12.5 pts, CI [-20.0, -5.0] | Useful Qwen3 low-capacity point; English gap but no Banglish-below-Bangla gap. |
| Qwen3-4B | Qwen3 | validation_200_v3 | 80/200 | 46/200 | 88/200 | -17.0 pts, CI [-23.5, -10.5] | -21.0 pts, CI [-28.5, -13.5] | Strongest open-model evidence; robust Banglish-below-Bangla and Banglish-below-English gaps. |
| Phi-3.5-mini | Phi | validation_200_v4 | 38/200 | 40/200 | 80/200 | +1.0 pts, CI [-4.0, +6.0] | -20.0 pts, CI [-28.0, -11.5] | Non-Qwen contrast; large English gap but no Banglish-below-Bangla ordering. |

## Self-Normalization

| Model | Slice | Baseline | Self-normalized | Delta | 95% CI | Direction p |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | validation_200_v3 | 38/200 | 51/200 | +6.5 pts | [+0.5, +13.0] | 0.0236 |
| Qwen2.5-7B 8-bit | validation_200_v4 | 48/200 | 47/200 | -0.5 pts | [-7.0, +6.5] | 0.4699 |
| Qwen3-4B | validation_200_v3 | 46/200 | 21/200 | -12.5 pts | [-19.5, -5.5] | 0.0001 |

## Answer-Signal Routing

| Model | Rule | Baseline | Always selfnorm | Routed | Routed-Baseline | Routed-Selfnorm | BEnQA routed gain | BanglaMATH routed gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | selfnorm if parsed answer non-empty | 31/150 | 41/150 | 43/150 | +8.0 pts, CI [+0.7, +15.3] | +1.3 pts, CI [0.0, +3.3] | +8 | +4 |
| Qwen3-4B | selfnorm if parsed answer non-empty | 32/150 | 16/150 | 40/150 | +5.3 pts, CI [+1.3, +10.0] | +16.0 pts, CI [+10.0, +22.0] | +6 | +2 |

## Cross-Script Answer Agreement

| Model | Banglish | Agreement route | Route-Banglish | Oracle | Oracle-Banglish |
| --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5, +8.5] | 99/200 | +29.0 pts, CI [+23.0, +35.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5, +17.5] | 115/200 | +34.0 pts, CI [+27.5, +40.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0, +19.0] | 108/200 | +29.5 pts, CI [+23.5, +36.0] |

## Generated-View Preservation Gates

| Model | Dataset | n | Options changed | Digit sequence changed | Formulas changed | Line count changed | Extra answer markers | Gate implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-7B 8-bit | banglamath | 56 | 0 | 6 | 0 | 56 | 0 | Reject generated view on option/digit/formula/answer-marker failures. |
| Qwen2.5-7B 8-bit | benqa | 144 | 10 | 25 | 5 | 64 | 21 | Reject generated view on option/digit/formula/answer-marker failures. |
| Qwen3-4B | banglamath | 56 | 0 | 1 | 0 | 56 | 0 | Reject generated view on option/digit/formula/answer-marker failures. |
| Qwen3-4B | benqa | 144 | 3 | 14 | 1 | 108 | 5 | Reject generated view on option/digit/formula/answer-marker failures. |

## Deterministic Generated-View Smokes

| Generator | Protection | Dataset | Target view | n | Hard fails | Option failures | Digit failures | Formula failures | Extra answer markers | Latin fragment warnings | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phonetic-bangla 1.0.0 | raw | benqa | generated_bn | 36 | 36 | 36 | 0 | 23 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | raw | benqa | generated_bn | 36 | 36 | 36 | 0 | 23 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | legacy protected v1; historical answer-audit input | benqa | generated_bn | 36 | 20 | 0 | 0 | 20 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | legacy protected v1; historical answer-audit input | benqa | generated_bn | 36 | 22 | 0 | 0 | 22 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | reviewed-v5 expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | reviewed-v5 expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | reviewed-v5 formulaish protected v3 | benqa | generated_bn | 36 | 0 | 0 | 0 | 0 | 0 | 0 | Gate-passing; answer audit complete |
| bnbphoneticparser 0.1.5 | reviewed-v5 formulaish protected v3 | benqa | generated_bn | 36 | 0 | 0 | 0 | 0 | 0 | 0 | Gate-passing; answer audit complete |

## Generated-BN Candidate Preservation

| Generator | Protection | Dataset | Target view | n | Hard fails | Option failures | Digit failures | Formula failures | Extra answer markers | Latin fragment warnings | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phonetic-bangla 1.0.0 | raw | benqa | generated_bn | 36 | 36 | 36 | 0 | 23 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | raw | benqa | generated_bn | 36 | 36 | 36 | 0 | 23 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | legacy protected v1; historical answer-audit input | benqa | generated_bn | 36 | 20 | 0 | 0 | 20 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | legacy protected v1; historical answer-audit input | benqa | generated_bn | 36 | 22 | 0 | 0 | 22 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | reviewed-v5 expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| bnbphoneticparser 0.1.5 | reviewed-v5 expanded protected v2 | benqa | generated_bn | 36 | 16 | 0 | 0 | 16 | 0 | 0 | Reject for routing |
| phonetic-bangla 1.0.0 | reviewed-v5 formulaish protected v3 | benqa | generated_bn | 36 | 0 | 0 | 0 | 0 | 0 | 0 | Gate-passing; answer audit complete |
| bnbphoneticparser 0.1.5 | reviewed-v5 formulaish protected v3 | benqa | generated_bn | 36 | 0 | 0 | 0 | 0 | 0 | 0 | Gate-passing; answer audit complete |
| fms-byte/banglish_to_bangla MBART | expanded protected line segments | benqa | generated_bn | 36 | 15 | 0 | 0 | 15 | 0 | 7 | Reject for routing |

## Generated-BN Reference Similarity Dev50

| Rank | Generator | n | Mean CER | Median CER | Mean sequence similarity | Mean Bengali ratio | Exact matches | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | protected_phonetic_bangla | 36 | 0.0906 | 0.0665 | 0.8915 | 0.4036 | 0 | Closest native-reference match among audited candidates |
| 2 | protected_bnbphoneticparser | 36 | 0.1235 | 0.1032 | 0.8598 | 0.3925 | 1 | Privileged dev-only lexical diagnostic |
| 3 | protected_fms_byte_mbart | 36 | 0.1855 | 0.1928 | 0.8103 | 0.3839 | 1 | Privileged dev-only lexical diagnostic |

## Generated-BN Answer Audit Dev50

| Model | Variant | n | Correct | Accuracy | Delta vs Banglish | Delta 95% CI (pts) | Direction p | Parsed empty | Gate hard fails | Eligible n | Eligible baseline | Eligible generated | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-4B | Banglish baseline | 36 | 15 | 0.417 | 0 |  |  | 2 |  |  |  |  | Baseline |
| Qwen3-4B | Historical protected-v1 bnbphoneticparser generated-BN | 36 | 17 | 0.472 | 2 | [-8.3, +19.4] | 0.2603 | 0 |  |  |  |  | Model-specific dev lead |
| Qwen3-4B | Historical protected-v1 phonetic-bangla generated-BN | 36 | 11 | 0.306 | -4 | [-25.0, +2.8] | 0.1 | 0 |  |  |  |  | Drop for this model |
| Qwen2.5-3B | Banglish baseline | 36 | 8 | 0.222 | 0 |  |  | 0 |  |  |  |  | Baseline |
| Qwen2.5-3B | Historical protected-v1 bnbphoneticparser generated-BN | 36 | 7 | 0.194 | -1 | [-16.7, +11.1] | 0.4249 | 0 |  |  |  |  | Drop for this model |
| Qwen2.5-3B | Historical protected-v1 phonetic-bangla generated-BN | 36 | 14 | 0.389 | 6 | [0.0, +33.3] | 0.0303 | 0 |  |  |  |  | Model-specific dev lead |
| Qwen3-4B | Banglish baseline | 36 | 15 | 0.417 | 0 |  |  | 2 |  |  |  |  | Baseline |
| Qwen3-4B | Reviewed-v5 protected-v2 bnbphoneticparser generated-BN | 36 | 16 | 0.444 | 1 |  |  | 1 | 16 | 20 | 10 | 11 | Gate-blocked diagnostic |
| Qwen3-4B | Reviewed-v5 protected-v2 phonetic-bangla generated-BN | 36 | 13 | 0.361 | -2 |  |  | 0 | 16 | 20 | 10 | 9 | Gate-blocked diagnostic |
| Qwen2.5-3B | Banglish baseline | 36 | 9 | 0.250 | 0 |  |  | 0 |  |  |  |  | Baseline |
| Qwen2.5-3B | Reviewed-v5 protected-v2 bnbphoneticparser generated-BN | 36 | 8 | 0.222 | -1 |  |  | 0 | 16 | 20 | 5 | 6 | Gate-blocked diagnostic |
| Qwen2.5-3B | Reviewed-v5 protected-v2 phonetic-bangla generated-BN | 36 | 10 | 0.278 | 1 |  |  | 0 | 16 | 20 | 5 | 5 | Gate-blocked diagnostic |
| Qwen3-4B | Banglish baseline | 36 | 15 | 0.417 | 0 |  |  | 2 |  |  |  |  | Baseline |
| Qwen3-4B | Reviewed-v5 protected-v3 bnbphoneticparser generated-BN | 36 | 17 | 0.472 | 2 | [-8.3, +19.4] | 0.2704 | 1 | 0 | 36 | 15 | 17 | Gate-passing dev lead; needs generated-English before test150 |
| Qwen3-4B | Reviewed-v5 protected-v3 phonetic-bangla generated-BN | 36 | 14 | 0.389 | -1 | [-16.7, +11.1] | 0.4284 | 1 | 0 | 36 | 15 | 14 | Gate-passing but no lead |
| Qwen2.5-3B | Banglish baseline | 36 | 9 | 0.250 | 0 |  |  | 0 |  |  |  |  | Baseline |
| Qwen2.5-3B | Reviewed-v5 protected-v3 bnbphoneticparser generated-BN | 36 | 9 | 0.250 | 0 | [-19.4, +19.4] | 0.5553 | 0 | 0 | 36 | 9 | 9 | Gate-passing but no lead |
| Qwen2.5-3B | Reviewed-v5 protected-v3 phonetic-bangla generated-BN | 36 | 10 | 0.278 | 1 | [-13.9, +19.4] | 0.435 | 0 | 0 | 36 | 9 | 10 | Gate-passing dev lead; needs generated-English before test150 |

## Generated-View Agreement Route Dev

| Route | n | Banglish | Generated-BN | Generated-EN | Routed | Routed-Banglish | Routed items | EN gate fallbacks | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Historical protected-v1 BNB generated-BN + Qwen3 generated-EN agreement | 36 | 15 | 17 | 7 | 16 | 1 | 1 | 16 | Do not test150; generated-EN bottleneck. |
| Qwen3 protected-v3 BNB generated-BN + guarded generated-EN agreement | 36 | 15 | 17 | 15 | 16 | 1 | 1 | 0 | Weak dev-only +1 item; no held-out launch. |
| Qwen2.5 protected-v3 phonetic generated-BN + guarded generated-EN agreement | 36 | 9 | 10 | 11 | 8 | -1 | 1 | 0 | Negative dev route; drop for this model. |

## V5 BEnQA Option Permutation Dev50

| Model | Source items | Identity pred D | Identity wrong D | Rotated identity-D rows | Remain label D | Follow original D content | Semantic match vs identity | Exact semantic-equivariant items | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | 36 | 11/36 | 7 | 33 | 10/33 | 15/33 | 39/108 | 4/36 | Semantic D-content tracking dominates label-position attraction |
| Qwen3-4B | 36 | 26/36 | 15 | 78 | 60/78 | 9/78 | 19/108 | 2/36 | Label-position attraction dominates semantic D-content tracking |

## BnSentMix External Validation

| Model | Rows | Valid outputs | Correct | Accuracy | Macro-F1 | Positive recall | Negative recall | Neutral recall | Mixed recall | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | 200 | 200/200 | 89/200 | 44.5% | 0.431 | 60.0% | 56.0% | 20.0% | 42.0% | Zero-shot natural code-mixed sentiment external-validity layer |
| Qwen2.5-7B 8-bit | 200 | 200/200 | 98/200 | 49.0% | 0.479 | 40.0% | 44.0% | 78.0% | 34.0% | Zero-shot natural code-mixed sentiment external-validity layer |
| Qwen3-4B | 200 | 200/200 | 99/200 | 49.5% | 0.486 | 86.0% | 36.0% | 40.0% | 36.0% | Zero-shot natural code-mixed sentiment external-validity layer |

## BnSentMix Model Complementarity

| Result | Count | Delta | Interpretation |
| --- | --- | --- | --- |
| Best single model | 99/200 |  | Qwen3-4B is the strongest single BnSentMix row. |
| Any-model diagnostic oracle | 154/200 | +27.5 pts, CI [+21.5, +34.0] | Upper bound showing cross-model error complementarity, not deployable accuracy. |
| Exactly one model correct | 66/200 |  | Rows where the answer is recoverable by only one of the three models. |
| All models wrong | 46/200 |  | Residual hard natural code-mixed sentiment rows for this model set. |
| Best pair oracle | 133/200 |  | Qwen2.5-7B 8-bit vs Qwen3-4B has the largest pairwise oracle coverage. |
| Majority + 7B fallback | 106/200 | +4.0 pts, CI [0.0, +8.0] | Simple behavioral route; promising but not a locked deployment claim. |

## BnSentMix Routing Dev-Test

| Protocol | Selected result | Baseline context | Post-hoc context | Interpretation |
| --- | --- | --- | --- | --- |
| Pilot40-selected rule | 72/160 | best single heldout 87/160 | best heldout route 95/160 | Ordered 40-row pilot underperforms; not a reliable route selector. |
| Hash5 cross-validation | 106/200 | Qwen3 99/200; Qwen2.5-7B 98/200 | majority + Qwen2.5-7B fallback=5 | Majority + Qwen2.5-7B fallback is a weak deployable candidate. |
| Block40 cross-validation | 84/200 | Qwen3 99/200; Qwen2.5-7B 98/200 | majority + Qwen2.5-7B fallback=3;majority + Qwen3 fallback=1;single Qwen3=1 | Ordered blocks expose split sensitivity; do not claim deployed mitigation. |

## Diagnostic Model Pilots

| Model | Mode | Bangla | Banglish | English | Decision |
| --- | --- | --- | --- | --- | --- |
| Qwen3-8B | 8-bit | blocked | blocked | blocked | Do not retry on P100; bitsandbytes backend blocked. |
| Mistral-7B-Instruct-v0.3 | 8-bit pilot20 | 3/20 | 4/20 | 4/20 | Diagnostic only; weak and slow. |
| Indic-Gemma-2B Navarasa | fp16 pilot20, Alpaca wrapper | 4/20 | 3/20 | 5/20 | Diagnostic only; parseable but around chance. |

## Real Banglish Distribution

| Source | Rows | Mean chars | Mean words | Mean Latin ratio | Digit row share | Mixed-script share |
| --- | --- | --- | --- | --- | --- | --- |
| BanglaTLit test | 2500 | 56.9 | 10.7 | 0.927 | 0.183 | 0.025 |
| BanglaTLit val | 1500 | 56.4 | 10.6 | 0.927 | 0.179 | 0.024 |
| Validation-200 v5 content Banglish | 200 | 86.2 | 14.2 | 0.902 | 0.545 | 0.000 |
| Validation-200 v5 raw Banglish | 200 | 159.5 | 31.5 | 0.834 | 0.695 | 0.000 |

## Auto-Suggested Banglish Sensitivity

| Model | v3 Banglish | v4 Banglish | Auto-suggested | Auto-v4 | Gains | Losses |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | 38/200 | 39/200 | 40/200 | +0.5 pts, CI [-1.5, +2.5] | 3 | 2 |
| Qwen3-4B | 46/200 | 47/200 | 48/200 | +0.5 pts, CI [0.0, +1.5] | 1 | 0 |

## V5 Reviewed Banglish Sensitivity

| Model | v4 Banglish | v5 reviewed | v5-v4 | Test split v5-v4 | Gains | Losses | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | 39/200 | 41/200 | +1.0 pts, CI [-1.0, +3.0] | +0.7 pts, CI [-1.3, +3.3] | 3 | 1 | Use v5 for final Banglish reruns; cleanup does not erase the gap. |
| Qwen3-4B | 47/200 | 49/200 | +1.0 pts, CI [0.0, +2.5] | +1.3 pts, CI [0.0, +3.3] | 2 | 0 | Use v5 for final Banglish reruns; cleanup does not erase the gap. |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-3.5, +2.5] | 0.0 pts, CI [-4.0, +3.3] | 4 | 5 | Use v5 for final Banglish reruns; cleanup does not erase the gap. |

## V5 Flagged-Bad Policy Sensitivity

| Model | Comparison | Policy | Left | Right | Delta | Gains | Losses |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | v5_minus_v4_banglish | strict197 | 37/197 | 39/197 | +1.0 pts, CI [-1.0, +3.0] | 3 | 1 |
| Qwen2.5-3B | v5_banglish_minus_bangla | strict197 | 53/197 | 39/197 | -7.1 pts, CI [-13.2, -1.0] | 14 | 28 |
| Qwen2.5-3B | v5_banglish_minus_english | strict197 | 71/197 | 39/197 | -16.2 pts, CI [-23.4, -9.1] | 13 | 45 |
| Qwen3-4B | v5_minus_v4_banglish | strict197 | 46/197 | 48/197 | +1.0 pts, CI [0.0, +2.5] | 2 | 0 |
| Qwen3-4B | v5_banglish_minus_bangla | strict197 | 79/197 | 48/197 | -15.7 pts, CI [-22.3, -9.6] | 8 | 39 |
| Qwen3-4B | v5_banglish_minus_english | strict197 | 87/197 | 48/197 | -19.8 pts, CI [-27.4, -12.2] | 13 | 52 |
| Qwen2.5-7B 8-bit | v5_minus_v4_banglish | strict197 | 47/197 | 46/197 | -0.5 pts, CI [-3.5, +2.5] | 4 | 5 |
| Qwen2.5-7B 8-bit | v5_banglish_minus_bangla | strict197 | 65/197 | 46/197 | -9.6 pts, CI [-16.8, -2.5] | 18 | 37 |
| Qwen2.5-7B 8-bit | v5_banglish_minus_english | strict197 | 93/197 | 46/197 | -23.9 pts, CI [-31.5, -15.7] | 13 | 60 |
