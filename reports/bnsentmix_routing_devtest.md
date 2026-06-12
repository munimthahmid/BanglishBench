# BnSentMix Routing Dev-Test Audit

Updated: 2026-06-11

## Scope

This no-spend audit tests whether the BnSentMix three-model
complementarity signal can be converted into a simple deployable route.
It deliberately separates post-hoc oracle evidence from rules selected
without seeing the evaluation fold labels.

- Source complementarity items: `results/analysis/bnsentmix_model_complementarity_items.csv`
- Candidate table: `results/analysis/bnsentmix_routing_devtest_candidates.csv`
- Routing summary: `results/analysis/bnsentmix_routing_devtest_summary.csv`

## Headline

| Selection protocol | Selected result | Baseline context | Interpretation |
| --- | ---: | --- | --- |
| Pilot40 -> holdout160 | 72/160 | Qwen3 and Qwen2.5-7B each reach 87/160 as the best single held-out rows; post-hoc best route reaches 95/160. | The 40-row ordered pilot is too small/misleading for route selection. |
| Hash5 cross-validation | 106/200 | Qwen3 99/200; Qwen2.5-7B 98/200. | All hash folds select majority vote with Qwen2.5-7B fallback; this is a weak deployable candidate, not a locked mitigation. |
| Block40 cross-validation | 84/200 | Qwen3 99/200; Qwen2.5-7B 98/200. | Ordered blocks expose route-selection instability. |

## What This Means

- The complementarity result remains meaningful: the same natural
  code-mixed items are not failed by all models in the same way.
- A simple majority route with Qwen2.5-7B fallback is the only practical
  candidate that survives hash-fold selection, reaching 106/200.
- The candidate is not strong enough to claim a deployed solution because
  block folds and the pilot-prefix split underperform single-model baselines.

## Fold Details

| Split | Fold | Selected rule | Train | Eval | Qwen3 eval | Qwen2.5-7B eval |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| hash5 | 0 | majority_fallback\|Qwen2.5-7B 8-bit | 82/156 | 24/44 | 18/44 | 24/44 |
| hash5 | 1 | majority_fallback\|Qwen2.5-7B 8-bit | 77/149 | 29/51 | 27/51 | 27/51 |
| hash5 | 2 | majority_fallback\|Qwen2.5-7B 8-bit | 87/161 | 19/39 | 22/39 | 18/39 |
| hash5 | 3 | majority_fallback\|Qwen2.5-7B 8-bit | 82/156 | 24/44 | 23/44 | 21/44 |
| hash5 | 4 | majority_fallback\|Qwen2.5-7B 8-bit | 96/178 | 10/22 | 9/22 | 8/22 |
| block40 | 0 | majority_fallback\|Qwen2.5-7B 8-bit | 95/160 | 11/40 | 12/40 | 11/40 |
| block40 | 1 | majority_fallback\|Qwen3-4B | 85/160 | 17/40 | 18/40 | 29/40 |
| block40 | 2 | single\|Qwen3-4B | 87/160 | 12/40 | 12/40 | 26/40 |
| block40 | 3 | majority_fallback\|Qwen2.5-7B 8-bit | 85/160 | 21/40 | 23/40 | 15/40 |
| block40 | 4 | majority_fallback\|Qwen2.5-7B 8-bit | 83/160 | 23/40 | 34/40 | 17/40 |

## Claim Boundary

- Report this as a deployability stress test for the complementarity
  finding, not as a final routing method.
- The thesis-safe result is: large natural-task complementarity exists,
  but simple label-only routing needs a larger preregistered external
  development set before it can be claimed as mitigation.
