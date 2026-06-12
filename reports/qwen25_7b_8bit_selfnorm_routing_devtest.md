# Qwen2.5-7B 8-bit Self-Normalization Routing Dev/Test

Updated: 2026-05-28

## Purpose

After the plain Qwen2.5-7B self-normalization run came out flat overall, this
analysis checks whether existing baseline and self-normalized outputs contain a
useful routing signal.

## Inputs

- Compare file:
  `results/analysis/qwen25_7b_8bit_validation200_v4_full200_baseline_vs_selfnorm_items_reparsed.csv`
- Dev split: `data/slices/validation_200_v4_dev50.jsonl`
- Test split: `data/slices/validation_200_v4_test150.jsonl`

## Routing Scan

Top dev rules:

| Rule | Dev | Test | Test used selfnorm |
| --- | ---: | ---: | ---: |
| Always baseline | 13/50 | 35/150 | 0 |
| Always selfnorm | 18/50 | 29/150 | 150 |
| Selfnorm if parsed answers disagree | 18/50 | 29/150 | 103 |
| Selfnorm if BanglaMATH | 15/50 | 38/150 | 42 |

The dev-best answer-signal rules collapse to nearly the same result as always
self-normalize and fail on test. A conservative task-aware route, self-normalize
only BanglaMATH, is lower on dev but slightly better on test.

## Bootstrap Checks

| Rule | Split | Baseline | Routed | Delta | 95% CI |
| --- | --- | ---: | ---: | ---: | --- |
| Parsed-disagree | Dev | 13/50 | 18/50 | +10 pts | [-2, +22] |
| Parsed-disagree | Test | 35/150 | 29/150 | -4 pts | [-12, +4] |
| BanglaMATH-only | Dev | 13/50 | 15/50 | +4 pts | [0, +10] |
| BanglaMATH-only | Test | 35/150 | 38/150 | +2 pts | [0, +4.67] |

## Interpretation

For Qwen2.5-7B, answer-side routing is not solved:

- Dev-selected answer-signal routing overfits the small dev split.
- The only held-out positive rule is task-aware and modest: it protects BEnQA
  from self-normalization losses while taking the BanglaMATH gains.
- This supports the broader mitigation story: routing needs stronger signals
  than parsed-answer shape alone, and dev/test reporting is necessary.

Decision: keep the BanglaMATH-only result as exploratory evidence, but do not
promote it to a main mitigation claim. It is useful for designing future locked
routing rules.

## Artifacts

- Routing scan:
  `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_selfnorm_answer_signal_routing.csv`
- Parsed-disagree routed items:
  `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_selfnorm_answer_signal_parsed_disagree_items.csv`
- Parsed-disagree bootstrap:
  `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_selfnorm_answer_signal_parsed_disagree_bootstrap.csv`
- BanglaMATH-only routed items:
  `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_selfnorm_banglamath_route_items.csv`
- BanglaMATH-only bootstrap:
  `results/analysis/qwen25_7b_8bit_validation200_v4_devtest_selfnorm_banglamath_route_bootstrap.csv`
