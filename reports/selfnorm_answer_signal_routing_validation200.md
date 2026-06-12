# Self-Normalization Answer-Signal Routing

Updated: 2026-05-28

## Purpose

The earlier routing report used rewrite-preservation and task metadata. This
report adds deployable answer-side signals from the existing baseline vs
self-normalization outputs, such as whether the self-normalized answer parses to
a non-empty answer.

This is an exploratory candidate scan. It should guide the next pre-registered
routing rule, not be presented as a fully locked final mitigation unless the
selection policy is stated carefully.

## Main Candidate

Rule:

> Use self-normalization only if the self-normalized answer parses as non-empty;
> otherwise keep the baseline Banglish answer.

Results:

| Model | Split | Baseline | Always selfnorm | Answer-signal route | Uses selfnorm |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Dev50 | 7/50 | 10/50 | 11/50 | 47/50 |
| Qwen2.5-3B | Test150 | 31/150 | 41/150 | 43/150 | 142/150 |
| Qwen3-4B | Dev50 | 14/50 | 5/50 | 15/50 | 27/50 |
| Qwen3-4B | Test150 | 32/150 | 16/150 | 40/150 | 82/150 |

Paired bootstrap uncertainty for test150:

| Model | Comparison | Delta | 95% CI | Direction p |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | routed - baseline | +8.0 pts | [+0.7, +15.3] | 0.0159 |
| Qwen2.5-3B | routed - always selfnorm | +1.3 pts | [0.0, +3.3] | 0.1358 |
| Qwen3-4B | routed - baseline | +5.3 pts | [+1.3, +10.0] | 0.0104 |
| Qwen3-4B | routed - always selfnorm | +16.0 pts | [+10.0, +22.0] | 0.0000 |

Item-level test150 changes vs baseline:

| Model | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 21 | 9 | 22 | 98 |
| Qwen3-4B | 10 | 2 | 30 | 108 |

Dataset breakdown on test150:

| Model | Dataset | Baseline | Always selfnorm | Routed | Routed - baseline | Gains | Losses |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | BEnQA | 31/108 | 37/108 | 39/108 | +8 | 17 | 9 |
| Qwen2.5-3B | BanglaMATH | 0/42 | 4/42 | 4/42 | +4 | 4 | 0 |
| Qwen3-4B | BEnQA | 31/108 | 13/108 | 37/108 | +6 | 8 | 2 |
| Qwen3-4B | BanglaMATH | 1/42 | 3/42 | 3/42 | +2 | 2 | 0 |

Interpretation:

- Qwen2.5-3B: the answer-signal rule is the best dev rule in this candidate
  set and improves test from 31/150 baseline to 43/150.
- Qwen3-4B: the same rule ties for best dev accuracy and improves test from
  32/150 baseline to 40/150, far better than always self-normalizing.
- For Qwen3, several dev rules tie at 15/50, so the exact selection policy is
  still a research choice. The result is promising but should be reported as
  candidate discovery unless the answer-signal rule is fixed before another
  held-out evaluation.

## Other Notable Qwen3 Candidates

| Rule | Dev | Test | Uses selfnorm on test |
| --- | ---: | ---: | ---: |
| selfnorm if after parsed length <= 20 | 15/50 | 40/150 | 55/150 |
| selfnorm if after parsed length <= 10 | 14/50 | 39/150 | 46/150 |
| selfnorm if choice and after non-empty | 14/50 | 38/150 | 40/150 |
| selfnorm if BanglaMATH | 15/50 | 34/150 | 42/150 |

The answer-length variants use less self-normalization than the non-empty rule
while preserving most of the test gain. These are worth considering if latency
or rewrite risk matters.

## Example Packets

The generated example packets show representative gains and losses:

- `reports/qwen25_selfnorm_answer_signal_routing_examples.md`
- `reports/qwen3_selfnorm_answer_signal_routing_examples.md`

Observed pattern:

- Gains often occur when baseline Banglish parsing or reasoning latches onto a
  wrong answer, while the self-normalized path produces a clean MCQ letter or
  a recognizable numeric/unit answer.
- Losses are mostly BEnQA cases where baseline was already correct but the
  self-normalized path changes the answer. This is why routing remains necessary
  even when the aggregate self-normalization signal is positive.

## Thesis-Safe Claim

Use:

> Answer-side routing signals are a promising mitigation direction. A simple
> rule that only trusts self-normalization when it yields a parseable answer
> improves both Qwen2.5-3B and Qwen3-4B on the validation-200 v4 test split in
> this exploratory scan.

Avoid:

- Claiming this fully solves Banglish robustness.
- Claiming the Qwen3 rule is final without acknowledging the dev tie.
- Selecting among many exploratory heuristics using test accuracy.

## Artifacts

- `scripts/evaluate_selfnorm_answer_signal_routing.py`
- `results/analysis/qwen25_validation200_v4_devtest_selfnorm_answer_signal_routing.csv`
- `results/analysis/qwen25_validation200_v4_devtest_selfnorm_answer_signal_routed_items.csv`
- `results/analysis/qwen25_validation200_v4_devtest_selfnorm_answer_signal_routed_breakdown.csv`
- `results/analysis/qwen25_validation200_v4_devtest_selfnorm_answer_signal_bootstrap.csv`
- `results/analysis/qwen3_validation200_v4_devtest_selfnorm_answer_signal_routing.csv`
- `results/analysis/qwen3_validation200_v4_devtest_selfnorm_answer_signal_routed_items.csv`
- `results/analysis/qwen3_validation200_v4_devtest_selfnorm_answer_signal_routed_breakdown.csv`
- `results/analysis/qwen3_validation200_v4_devtest_selfnorm_answer_signal_bootstrap.csv`
- `reports/qwen25_selfnorm_answer_signal_routing_examples.md`
- `reports/qwen3_selfnorm_answer_signal_routing_examples.md`
- Previous routing report:
  `reports/selfnorm_routing_devtest_validation200_v4.md`
