# Generated-View Route Bottleneck Analysis

Updated: 2026-06-11

This dev-only analysis asks why protected generated-BN plus generated-EN
agreement routing is weak. It compares the current conservative agreement
route with two upper bounds: generated-view oracle and triad oracle.

## Artifacts

- Item CSV: `results/analysis/generated_view_route_bottleneck_items.csv`
- Summary CSV: `results/analysis/generated_view_route_bottleneck_summary.csv`

## Route Summary

| Route | Group | Banglish | Generated-view oracle | Triad oracle | Generated agreement | Recoverable by generated views | Recovered by agreement | Missed by agreement | Disagree+one-correct | Current route | Route delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5 protected-v3 phonetic + guarded EN | all | 9/36 | 17/36 | 19/36 | 4/13 | 10 | 0 | 10 | 13 | 8/36 | -1 |
| Qwen3 historical protected-v1 BNB + raw self-translate EN | all | 15/36 | 20/36 | 20/36 | 4/12 | 5 | 1 | 4 | 9 | 16/36 | 1 |
| Qwen3 protected-v3 BNB + guarded EN | all | 15/36 | 20/36 | 20/36 | 12/24 | 5 | 1 | 4 | 8 | 16/36 | 1 |

## Reading The Columns

- Generated-view oracle counts rows where either generated-BN or generated-EN is correct.
- Triad oracle counts rows where Banglish, generated-BN, or generated-EN is correct.
- Recoverable by generated views counts baseline-wrong rows where at least one generated view is correct.
- Recovered by agreement is the subset where generated-BN and generated-EN agree on the correct answer.
- Disagree+one-correct shows recoverable rows missed by a strict agreement rule.

## Interpretation

- Qwen2.5 protected-v3 phonetic + guarded EN: generated views contain 10 baseline-wrong recoveries, but agreement recovers only 0 and misses 10.
- Qwen3 historical protected-v1 BNB + raw self-translate EN: generated views contain 5 baseline-wrong recoveries, but agreement recovers only 1 and misses 4.
- Qwen3 protected-v3 BNB + guarded EN: generated views contain 5 baseline-wrong recoveries, but agreement recovers only 1 and misses 4.
- The bottleneck is not only preservation. The generated views often do not
  agree when one of them is correct, so the conservative route is sparse.
- This supports the current decision not to launch generated-view test150
  until a better generated-English source or a pre-registered stronger
  routing signal is available.
