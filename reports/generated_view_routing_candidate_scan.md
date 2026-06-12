# Generated-View Routing Candidate Scan

Updated: 2026-06-11

This dev-only scan evaluates simple deployable answer-routing rules over
the existing Banglish, generated-BN, and generated-EN parsed answers. It
does not authorize held-out testing; it identifies whether a rule family
is promising enough to preregister later.

## Artifacts

- Item CSV: `results/analysis/generated_view_routing_candidate_items.csv`
- Summary CSV: `results/analysis/generated_view_routing_candidate_summary.csv`

## Best Rule Per Route

| Route | Rule | Baseline | Routed | Delta | Gains | Losses | Routed nonbaseline |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_en_priority_nonbaseline | 9/36 | 13/36 | 4 | 9 | 5 | 24 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | all_disagree_bn_tiebreak | 15/36 | 17/36 | 2 | 2 | 0 | 3 |
| Qwen3 protected-v3 BNB + guarded EN | all_disagree_bn_tiebreak | 15/36 | 17/36 | 2 | 2 | 0 | 3 |

## Full Summary

| Route | Rule | Baseline | Routed | Delta | Gains | Losses | Routed nonbaseline |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5 protected-v3 phonetic + guarded EN | all_disagree_bn_tiebreak | 9/36 | 8/36 | -1 | 1 | 2 | 5 |
| Qwen2.5 protected-v3 phonetic + guarded EN | all_disagree_en_tiebreak | 9/36 | 9/36 | 0 | 2 | 2 | 5 |
| Qwen2.5 protected-v3 phonetic + guarded EN | baseline | 9/36 | 9/36 | 0 | 0 | 0 | 0 |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_bn_if_baseline_empty | 9/36 | 9/36 | 0 | 0 | 0 | 0 |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_bn_only | 9/36 | 10/36 | 1 | 6 | 5 | 19 |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_bn_priority_nonbaseline | 9/36 | 12/36 | 3 | 8 | 5 | 24 |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_en_if_baseline_empty | 9/36 | 9/36 | 0 | 0 | 0 | 0 |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_en_only | 9/36 | 11/36 | 2 | 4 | 2 | 10 |
| Qwen2.5 protected-v3 phonetic + guarded EN | generated_en_priority_nonbaseline | 9/36 | 13/36 | 4 | 9 | 5 | 24 |
| Qwen2.5 protected-v3 phonetic + guarded EN | strict_generated_agreement | 9/36 | 8/36 | -1 | 0 | 1 | 1 |
| Qwen2.5 protected-v3 phonetic + guarded EN | three_view_majority | 9/36 | 8/36 | -1 | 0 | 1 | 1 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | all_disagree_bn_tiebreak | 15/36 | 17/36 | 2 | 2 | 0 | 3 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | all_disagree_en_tiebreak | 15/36 | 16/36 | 1 | 1 | 0 | 3 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | baseline | 15/36 | 15/36 | 0 | 0 | 0 | 0 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | generated_bn_if_baseline_empty | 15/36 | 16/36 | 1 | 1 | 0 | 2 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | generated_bn_only | 15/36 | 17/36 | 2 | 4 | 2 | 10 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | generated_bn_priority_nonbaseline | 15/36 | 13/36 | -2 | 5 | 7 | 16 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | generated_en_if_baseline_empty | 15/36 | 15/36 | 0 | 0 | 0 | 0 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | generated_en_only | 15/36 | 12/36 | -3 | 2 | 5 | 9 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | generated_en_priority_nonbaseline | 15/36 | 12/36 | -3 | 4 | 7 | 16 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | strict_generated_agreement | 15/36 | 16/36 | 1 | 1 | 0 | 2 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | three_view_majority | 15/36 | 16/36 | 1 | 1 | 0 | 2 |
| Qwen3 protected-v3 BNB + guarded EN | all_disagree_bn_tiebreak | 15/36 | 17/36 | 2 | 2 | 0 | 3 |
| Qwen3 protected-v3 BNB + guarded EN | all_disagree_en_tiebreak | 15/36 | 17/36 | 2 | 2 | 0 | 3 |
| Qwen3 protected-v3 BNB + guarded EN | baseline | 15/36 | 15/36 | 0 | 0 | 0 | 0 |
| Qwen3 protected-v3 BNB + guarded EN | generated_bn_if_baseline_empty | 15/36 | 15/36 | 0 | 0 | 0 | 1 |
| Qwen3 protected-v3 BNB + guarded EN | generated_bn_only | 15/36 | 17/36 | 2 | 4 | 2 | 10 |
| Qwen3 protected-v3 BNB + guarded EN | generated_bn_priority_nonbaseline | 15/36 | 15/36 | 0 | 4 | 4 | 12 |
| Qwen3 protected-v3 BNB + guarded EN | generated_en_if_baseline_empty | 15/36 | 15/36 | 0 | 0 | 0 | 0 |
| Qwen3 protected-v3 BNB + guarded EN | generated_en_only | 15/36 | 15/36 | 0 | 2 | 2 | 5 |
| Qwen3 protected-v3 BNB + guarded EN | generated_en_priority_nonbaseline | 15/36 | 15/36 | 0 | 4 | 4 | 12 |
| Qwen3 protected-v3 BNB + guarded EN | strict_generated_agreement | 15/36 | 16/36 | 1 | 1 | 0 | 1 |
| Qwen3 protected-v3 BNB + guarded EN | three_view_majority | 15/36 | 16/36 | 1 | 1 | 0 | 1 |

## Decision

No candidate is strong enough to justify generated-view test150.
Rules that route more often can expose generated-view oracle signal, but
they also add losses and are selected on the same small 36-item dev set.
Keep the current generated-view branch as diagnostic evidence unless a
better generated-English source and a pre-registered routing rule are
available.
