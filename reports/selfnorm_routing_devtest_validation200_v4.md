# Self-Normalization Routing Dev/Test Check

Updated: 2026-05-28 11:56 +0600

This report applies the validation-200 v4 dev/test protocol to baseline vs
self-normalization routing. Unlike the earlier full-validation heuristic report,
heuristics are selected on dev and then evaluated unchanged on test.

## Inputs

Compare files:

- `results/analysis/qwen25_validation200_v3_baseline_vs_selfnorm_items_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_baseline_vs_selfnorm_items_reparsed.csv`

Rewrite-quality files:

- `results/analysis/qwen25_validation200_v3_selfnorm_rewrite_quality_items_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_selfnorm_rewrite_quality_items_reparsed.csv`

Split files:

- `data/slices/validation_200_v4_dev50.jsonl`
- `data/slices/validation_200_v4_test150.jsonl`

## Dev-Selected Heuristics

| Model | Dev baseline | Dev selfnorm | Selected heuristic | Dev selected | Test baseline | Test selected |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| Qwen2.5-3B | 7/50 | 10/50 | selfnorm if options preserved | 10/50 | 31/150 | 41/150 |
| Qwen3-4B | 14/50 | 5/50 | selfnorm if BanglaMATH | 15/50 | 32/150 | 34/150 |

Selection rule:

- Pick the highest dev accuracy.
- If tied, prefer the heuristic using self-normalization less often.

## Heuristic Tables

Qwen2.5-3B:

| Split | Heuristic | Correct | Uses Selfnorm |
| --- | --- | ---: | ---: |
| Dev | always baseline | 7/50 | 0/50 |
| Dev | always selfnorm | 10/50 | 50/50 |
| Dev | selfnorm if options preserved | 10/50 | 46/50 |
| Dev | selfnorm if all structure preserved | 9/50 | 40/50 |
| Dev | selfnorm if BanglaMATH | 8/50 | 14/50 |
| Test | always baseline | 31/150 | 0/150 |
| Test | always selfnorm | 41/150 | 150/150 |
| Test | selfnorm if options preserved | 41/150 | 135/150 |
| Test | selfnorm if all structure preserved | 41/150 | 108/150 |
| Test | selfnorm if BanglaMATH | 35/150 | 42/150 |

Qwen3-4B:

| Split | Heuristic | Correct | Uses Selfnorm |
| --- | --- | ---: | ---: |
| Dev | always baseline | 14/50 | 0/50 |
| Dev | always selfnorm | 5/50 | 50/50 |
| Dev | selfnorm if Bengali ratio >= 0.5 | 12/50 | 28/50 |
| Dev | selfnorm if BanglaMATH | 15/50 | 14/50 |
| Dev | selfnorm if BEnQA | 4/50 | 36/50 |
| Test | always baseline | 32/150 | 0/150 |
| Test | always selfnorm | 16/150 | 150/150 |
| Test | selfnorm if Bengali ratio >= 0.5 | 28/150 | 81/150 |
| Test | selfnorm if BanglaMATH | 34/150 | 42/150 |
| Test | selfnorm if BEnQA | 14/150 | 108/150 |

## Interpretation

- Qwen2.5-3B confirms the earlier full-validation result under the split
  protocol: self-normalization is useful, and preserving option labels is enough
  to avoid some unnecessary rewrites without losing test accuracy.
- Qwen3-4B confirms that always self-normalizing is harmful. A task-aware rule
  selected on dev gives a small held-out gain on test, 32/150 -> 34/150, by
  using self-normalization only on BanglaMATH.
- The Qwen3 gain is too small to claim a solved routing method. It is useful as
  evidence that routing can recover a little signal while avoiding the large
  BEnQA damage.
- The next routing step should use an answer-disagreement or confidence signal,
  because rewrite-preservation features alone still do not identify when
  self-normalization helps.

Follow-up:

- `reports/selfnorm_answer_signal_routing_validation200.md` evaluates the first
  answer-side routing scan. The candidate rule `selfnorm if parsed answer
  non-empty` improves Qwen2.5 test150 from 31/150 to 43/150 and Qwen3 test150
  from 32/150 to 40/150, with positive paired bootstrap intervals against
  baseline.

## Generated Artifacts

- `scripts/evaluate_selfnorm_routing_by_slice.py`
- `results/analysis/qwen25_validation200_v4_devtest_selfnorm_routing_heuristics.csv`
- `results/analysis/qwen25_validation200_v4_devtest_selfnorm_routing_selection.csv`
- `results/analysis/qwen3_validation200_v4_devtest_selfnorm_routing_heuristics.csv`
- `results/analysis/qwen3_validation200_v4_devtest_selfnorm_routing_selection.csv`
