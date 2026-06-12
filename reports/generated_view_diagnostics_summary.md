# Generated-View Diagnostics Summary

Updated: 2026-05-31

## Purpose

This report consolidates the generated-view mitigation diagnostics. It answers
one question: are cheap generated Bengali/English views ready for a held-out
consistency-routing experiment?

Current answer: no. Preservation gates are useful, and generated-BN can help on
some dev cases, but the effect is model/generator-specific. A tightened
formula-preservation gate also shows that the cheap generated-BN candidates
can corrupt math/science notation too often for deployable routing. The
formulaish-token protected-v3 deterministic wrapper repairs the preservation
failure locally. A guarded generated-English repair also passes the hard
preservation gate, but 15/36 rows fall back to the source Banglish text, and
the final agreement routes still do not justify held-out testing.

## Prompt Set

Prompt set:

- `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- `data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl`

Scope:

- 36 validation-200 dev50 BEnQA MCQ items. The reviewed-v5 prompt set uses
  the v4 dev50 ids as the split filter; 19/36 rows changed from v4 to v5.
- 36 `generated_bn` prompts.
- 36 `generated_en` prompts.

## Preservation Results

Raw deterministic generated-BN:

| Generator | Hard failures | Main failure |
| --- | ---: | --- |
| `phonetic-bangla==1.0.0` | 36/36 | MCQ option-label corruption on 36/36; scientific-token corruption on 17/36. |
| `bnbphoneticparser==0.1.5` | 36/36 | MCQ option-label corruption on 36/36; scientific-token corruption on 17/36. |

Protected deterministic generated-BN:

| Generator | Version | Hard failures | Latin residue warnings | Notes |
| --- | --- | ---: | ---: | --- |
| `phonetic-bangla==1.0.0` | Historical protected v1 | 9/36 | 0/36 | Existing Qwen answer-audit input; reject under tightened scientific-token gate. |
| `bnbphoneticparser==0.1.5` | Historical protected v1 | 10/36 | 0/36 | Existing Qwen answer-audit input; reject under tightened scientific-token gate. |
| `phonetic-bangla==1.0.0` | Expanded protected v2 | 16/36 | 0/36 | Initially passed structural gates, but fails the tightened formula-expression gate. |
| `bnbphoneticparser==0.1.5` | Expanded protected v2 | 16/36 | 0/36 | Initially passed structural gates, but fails the tightened formula-expression gate. |
| `phonetic-bangla==1.0.0` | Reviewed-v5 expanded protected v2 | 16/36 | 0/36 | Formula/operator corruption blocks deployable routing. |
| `bnbphoneticparser==0.1.5` | Reviewed-v5 expanded protected v2 | 16/36 | 0/36 | Formula/operator corruption blocks deployable routing. |
| `phonetic-bangla==1.0.0` | Reviewed-v5 formulaish protected v3 | 0/36 | 0/36 | Repairs formula/operator preservation; answer audit complete. |
| `bnbphoneticparser==0.1.5` | Reviewed-v5 formulaish protected v3 | 0/36 | 0/36 | Repairs formula/operator preservation; answer audit complete. |
| `fms-byte/banglish_to_bangla` MBART | Expanded protected line segments | 15/36 | 7/36 | Formula-expression failures plus Latin residue; do not escalate. |

Privileged native-reference lexical diagnostic:

| Generator | Mean CER | Mean sequence similarity | Decision |
| --- | ---: | ---: | --- |
| Expanded-v2 protected phonetic | 0.0906 | 0.8915 | Closest native-reference match among audited candidates. |
| Expanded-v2 protected BNB | 0.1235 | 0.8598 | Dev-only lexical diagnostic. |
| Protected FMS-byte MBART | 0.1855 | 0.8103 | Do not escalate to answer routing. |

Qwen3 generated-English self-translation:

| Generator | Hard failures | Warnings | Main failures |
| --- | ---: | ---: | --- |
| Qwen3 self-translate EN | 16/36 | 18/36 | Digit/formula changes, line-count changes. |
| Guarded source-tail fallback EN | 0/36 | 0/36 | Preservation repaired, but 15/36 rows fall back to the source Banglish text. |

## Answer Audits

The following answer audits are historical dev-only diagnostics. They used the
protected-v1 deterministic files before the tightened scientific-token gate;
they are not answer audits of the expanded-v2 candidates.

Generated-BN-only answer audits:

| Model | Banglish | Protected phonetic-BN | Protected BNB-BN | Bootstrap interpretation |
| --- | ---: | ---: | ---: | --- |
| Qwen3-4B | 15/36 | 11/36, -11.1 pts CI [-25.0,+2.8] | 17/36, +5.6 pts CI [-8.3,+19.4] | BNB lead is weak; both intervals cross zero. |
| Qwen2.5-3B | 8/36 | 14/36, +16.7 pts CI [0.0,+33.3] | 7/36, -2.8 pts CI [-16.7,+11.1] | Phonetic lead is suggestive but dev-only; BNB is flat/negative. |

Reviewed-v5 protected-v2 answer audits:

| Model | Banglish | Phonetic-v2 all rows | BNB-v2 all rows | Gate-eligible interpretation |
| --- | ---: | ---: | ---: | --- |
| Qwen3-4B | 15/36 | 13/36 | 16/36 | Each generator has 16/36 gate-hard-fail rows. On the 20 eligible rows, phonetic is 9/20 vs Banglish 10/20, and BNB is 11/20 vs Banglish 10/20. |
| Qwen2.5-3B | 9/36 | 10/36 | 8/36 | Each generator has 16/36 gate-hard-fail rows. On the 20 eligible rows, phonetic is 5/20 vs Banglish 5/20, and BNB is 6/20 vs Banglish 5/20. |

Reviewed-v5 protected-v3 answer audits:

| Model | Banglish | Phonetic-v3 | BNB-v3 | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Qwen3-4B | 15/36 | 14/36, -2.8 pts CI [-16.7,+11.1] | 17/36, +5.6 pts CI [-8.3,+19.4] | BNB is a weak dev lead; interval crosses zero. |
| Qwen2.5-3B | 9/36 | 10/36, +2.8 pts CI [-13.9,+19.4] | 9/36, +0.0 pts CI [-19.4,+19.4] | Flat to +1 item; interval crosses zero. |

Guarded generated-English answer audits:

| Model | Banglish | Guarded generated-EN | Bootstrap interpretation |
| --- | ---: | ---: | --- |
| Qwen3-4B | 15/36 | 15/36, +0.0 pts CI [-11.1,+11.1] | Preservation-safe but not an accuracy gain. |
| Qwen2.5-3B | 9/36 | 11/36, +5.6 pts CI [-8.3,+19.4] | Small dev-only lead; interval crosses zero. |

Guarded generated-English repair provenance:

| Repair strategy | n | Qwen3 delta | Qwen2.5 delta | Route implication |
| --- | ---: | ---: | ---: | --- |
| Translated stem + source options | 21 | +0 | +2 | All guarded-EN answer gains come from these rows, but routing fires on only one item per model. |
| Source fallback after failed repair | 15 | +0 | +0 | Preservation safety, not a generated-English intervention. |

Generated-BN + generated-EN agreement route:

| Model | Banglish | Generated-BN | Generated-EN | Routed | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Qwen3-4B historical protected-v1 + raw self-translate EN | 15/36 | 17/36 | 7/36 | 16/36 | Do not test150; generated-EN is gate-blocked. |
| Qwen3-4B protected-v3 BNB + guarded EN | 15/36 | 17/36 | 15/36 | 16/36 | Weak dev-only +1 item; no held-out launch. |
| Qwen2.5-3B protected-v3 phonetic + guarded EN | 9/36 | 10/36 | 11/36 | 8/36 | Negative route; drop for this model. |

Each guarded route fires on only 1/36 items. The Qwen3 routed item is correct;
the Qwen2.5 routed item is wrong.

Route bottleneck analysis:

| Route | Generated-view oracle | Baseline-wrong recoveries in generated views | Recovered by strict agreement | Missed by agreement |
| --- | ---: | ---: | ---: | ---: |
| Qwen3 protected-v3 BNB + guarded EN | 20/36 | 5 | 1 | 4 |
| Qwen2.5 protected-v3 phonetic + guarded EN | 17/36 | 10 | 0 | 10 |

Interpretation: the blocker is not only preservation. The generated views often
contain a correct answer without agreeing with each other, so a strict
generated-BN/generated-EN agreement route is too sparse for held-out launch.

Deployable routing-candidate scan:

| Route | Best simple dev rule | Result | Decision |
| --- | --- | --- | --- |
| Qwen3 protected-v3 BNB + guarded EN | all-disagree tiebreak | 17/36 vs 15/36 baseline, +2 | Dev-only; selected on 36 rows. |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated-EN priority if non-baseline | 13/36 vs 9/36 baseline, +4 with 9 gains and 5 losses | Too volatile; no matching Qwen3 gain. |
| Current guarded routes, shared weak rule | generated-BN-only | Qwen3 +2, Qwen2.5 +1 | Generated-BN-only effect remains too small/uncertain for test150. |

## Decision

Do not launch held-out test150 generated-view routing under the current setup.

Reasons:

- Raw deterministic transliterators corrupt evaluation structure.
- Historical protected-v1 answer gains are not stable across Qwen2.5 and Qwen3,
  and those files now fail the tightened scientific-token gate.
- Expanded-v2 deterministic candidates fail the tightened formula-expression
  gate on 16/36 reviewed-v5 dev rows.
- Formulaish protected-v3 deterministic candidates pass the tightened
  preservation gate, but answer gains are small and uncertain.
- Reviewed-v5 protected-v2 answer audits show only +0 to +1 gate-eligible
  item gains depending on model/generator, not enough to justify test150.
- Reviewed-v5 protected-v3 answer audits show Qwen3 BNB +2 items and Qwen2.5
  phonetic +1 item on 36 dev rows, with wide intervals.
- FMS-byte MBART fails the tightened formula-expression gate on 15/36 rows and
  has 7/36 lexical-residue warnings.
- Paired bootstrap intervals are wide on the 36-item dev audit and do not
  justify a held-out generated-view claim.
- Qwen3 generated-English self-translation is weak and fails the tightened
  preservation gate on 16/36 items.
- The guarded generated-English repair passes the hard gate but is not a pure
  English translation because 15/36 rows use source fallback.
- The full generated-view agreement route improves Qwen3 dev Banglish by only
  one item and is negative for Qwen2.5.
- Bottleneck analysis shows the current agreement rule misses most
  generated-view oracle recoveries, especially for Qwen2.5.
- A dev-only routing-candidate scan finds no simple deployable answer-level
  rule robust enough to preregister for test150.

## Use In Thesis

Safe claim:

- Generated-view routing is a promising design direction, but current cheap
  generated views are not reliable enough for a held-out mitigation claim.

Claim to avoid:

- Do not claim that generated-view routing solves Banglish robustness.

## Artifacts

- `reports/phonetic_bangla_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/phonetic_bangla_protected_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/phonetic_bangla_protected_v2_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_v2_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/fms_byte_protected_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/phonetic_bangla_protected_v2_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_v2_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/phonetic_bangla_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_generated_bn_answer_audit_dev50.md`
- `reports/qwen25_3b_generated_bn_answer_audit_dev50.md`
- `reports/qwen3_4b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen3_4b_generated_bn_v5_pv3_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv3_dev50.md`
- `reports/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_selftranslate_guarded_v5_generated_en_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_guarded_generated_en_v5_dev50.md`
- `reports/qwen25_3b_guarded_generated_en_v5_dev50.md`
- `reports/guarded_generated_en_repair_provenance.md`
- `reports/generated_view_route_bottleneck_analysis.md`
- `reports/generated_view_routing_candidate_scan.md`
- `reports/qwen3_4b_generated_view_agreement_route_dev.md`
- `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`
- `results/tables/deterministic_generated_view_smokes.csv`
- `results/tables/generated_bn_candidate_preservation.csv`
- `results/tables/generated_bn_reference_similarity_dev50.csv`
- `results/tables/generated_bn_answer_audit_dev50.csv`
- `results/tables/generated_view_agreement_route_dev.csv`
