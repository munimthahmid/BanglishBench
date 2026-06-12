# Statistical Method Notes

Updated: 2026-05-27

## Why Paired Tests

Most Script Matters comparisons reuse the same underlying item across two
conditions:

- Bangla vs Banglish.
- English vs Banglish.
- Baseline Banglish vs mitigated Banglish.

Because the item is the same, raw aggregate accuracy differences should be
treated as paired differences rather than as two independent samples. A paired
analysis is more appropriate because it asks whether the same questions flip
from correct to wrong or wrong to correct under a script or mitigation change.

## Current Implementation

Script:

- `scripts/bootstrap_accuracy_delta.py`

Input:

- One or more JSONL model-output files.
- A left condition filter, e.g. `variant=bangla`.
- A right condition filter, e.g. `variant=banglish_clean`.
- A shared key, currently `id`.

Procedure:

1. Load all rows and optionally rescore with the current parser.
2. Filter rows into the left and right conditions.
3. Pair rows by item id.
4. Compute observed delta:
   `accuracy(right) - accuracy(left)`.
5. Bootstrap paired items with replacement for 10,000 samples.
6. Report the 2.5th and 97.5th percentile interval.

## Interpretation Rules

Use raw deltas and confidence intervals together:

- If the interval stays below zero, the right condition is reliably worse.
- If the interval crosses zero, phrase the result cautiously.
- If the interval stays above zero, the right condition is reliably better.

For example:

- Qwen3 validation v2 Banglish-vs-Bangla: -16 points, CI approx. [-25, -7].
  This is strong evidence of a Banglish drop.
- Qwen2.5 validation v2 Banglish-vs-Bangla: -5 points, CI approx. [-14, +4].
  This should be described as a weaker or inconclusive native-script drop,
  even though absolute Banglish accuracy is still low.
- Qwen3 MGSM Banglish-vs-English: -36 points, CI approx. [-52, -20].
  This is strong evidence of an English-vs-Banglish gap.

## Current Limitation

The bootstrap intervals are descriptive and useful for thesis reporting, but
they are still based on small slices:

- 100 validation items.
- 50 MGSM items.

Final claims should avoid overgeneralizing beyond these tasks until the benchmark
is expanded or a human-reviewed subset is completed.

