# MGSM Self-Normalization Answer-Signal Routing Transfer

Updated: 2026-05-28

## Purpose

This report tests whether the validation-200 exploratory routing rule,
`selfnorm if parsed answer non-empty`, transfers to MGSM Bengali arithmetic using
already completed baseline-vs-self-normalization compare files. No new GPU was
used.

## Artifacts

- Qwen2.5 routing scan:
  `results/analysis/qwen25_mgsm_bn50_selfnorm_answer_signal_routing.csv`
- Qwen2.5 routed items:
  `results/analysis/qwen25_mgsm_bn50_selfnorm_answer_signal_routed_items.csv`
- Qwen2.5 bootstrap:
  `results/analysis/qwen25_mgsm_bn50_selfnorm_answer_signal_bootstrap.csv`
- Qwen3 routing scan:
  `results/analysis/qwen3_mgsm_bn50_selfnorm_answer_signal_routing.csv`
- Qwen3 routed items:
  `results/analysis/qwen3_mgsm_bn50_selfnorm_answer_signal_routed_items.csv`
- Qwen3 bootstrap:
  `results/analysis/qwen3_mgsm_bn50_selfnorm_answer_signal_bootstrap.csv`

## Result

| Model | Baseline | Always selfnorm | Routed rule | Routed-baseline delta |
| --- | ---: | ---: | ---: | --- |
| Qwen2.5-3B | 0/50 | 0/50 | 0/50 | 0 pts, CI [0, 0] |
| Qwen3-4B | 5/50 | 0/50 | 0/50 | -10 pts, CI [-20, -2] |

The selected validation rule uses self-normalization whenever the
self-normalized parsed answer is non-empty. On MGSM, that condition fires for
all 50 items for both models, so it degenerates to always self-normalize.

## Interpretation

- The validation answer-signal routing rule does not transfer to MGSM.
- For Qwen3, it reproduces the known MGSM self-normalization failure: 5/50 -> 0/50.
- For Qwen2.5, MGSM clean Banglish is already 0/50, so routing cannot show a
  useful improvement under the existing outputs.
- This strengthens the thesis caveat: answer-side routing is a promising
  validation-slice mitigation lead, not a general arithmetic solution.

## Thesis Use

Use this as a limitation/boundary condition in the mitigation chapter. The safe
claim is that answer-signal routing improves validation-200 v4 test150 in an
exploratory setup, while MGSM arithmetic still requires a different mitigation
strategy or a stronger normalizer.
