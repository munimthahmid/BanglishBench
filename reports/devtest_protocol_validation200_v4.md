# Validation-200 v4 Dev/Test Protocol

Updated: 2026-05-28 11:56 +0600

This report turns the v4 dev/test split into an operational protocol. The goal
is to keep future prompt, routing, and normalization choices from being tuned on
the same 200 items used for thesis-facing claims.

## Split Definition

Source slice:

- `data/slices/validation_200_v4.jsonl`

Split artifacts:

- `data/slices/validation_200_v4_dev50.jsonl`
- `data/slices/validation_200_v4_test150.jsonl`
- `data/slices/validation_200_v4_dev50.manifest.json`

Counts:

| Split | Items | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| Dev | 50 | 36 | 14 |
| Test | 150 | 108 | 42 |

The split is deterministic with seed `20260528` and is stratified by BEnQA
subject and BanglaMATH grade.

## Protocol

1. Use dev for prompt wording, routing heuristics, rewrite filters, and
   preliminary ablations.
2. Use test only after a choice has been made on dev.
3. Report both dev and test for transparency, but treat test as the thesis-facing
   estimate.
4. Keep full validation-200 numbers as the historical evidence base, but do not
   tune new decisions on full validation-200.
5. Any future paid-model or stronger-open-model run should first be specified on
   dev, then run unchanged on test.

## Existing Runs Re-Summarized By Split

The following tables reuse existing outputs; no new GPU run was launched.

Baseline v3, all scripts:

| Split | Model | Bangla | Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Dev | Qwen2.5-3B | 11/50 | 7/50 | 18/50 |
| Dev | Qwen3-4B | 19/50 | 14/50 | 21/50 |
| Test | Qwen2.5-3B | 43/150 | 31/150 | 53/150 |
| Test | Qwen3-4B | 61/150 | 32/150 | 67/150 |

Dataset-level baseline:

| Split | Model | Dataset | Bangla | Banglish | English |
| --- | --- | --- | ---: | ---: | ---: |
| Dev | Qwen2.5-3B | BEnQA | 11/36 | 7/36 | 18/36 |
| Dev | Qwen2.5-3B | BanglaMATH | 0/14 | 0/14 | 0/14 |
| Dev | Qwen3-4B | BEnQA | 19/36 | 14/36 | 21/36 |
| Dev | Qwen3-4B | BanglaMATH | 0/14 | 0/14 | 0/14 |
| Test | Qwen2.5-3B | BEnQA | 38/108 | 31/108 | 48/108 |
| Test | Qwen2.5-3B | BanglaMATH | 5/42 | 0/42 | 5/42 |
| Test | Qwen3-4B | BEnQA | 57/108 | 31/108 | 61/108 |
| Test | Qwen3-4B | BanglaMATH | 4/42 | 1/42 | 6/42 |

v4 Banglish sensitivity:

| Split | Model | v3 Banglish | v4 Banglish |
| --- | --- | ---: | ---: |
| Dev | Qwen2.5-3B | 7/50 | 8/50 |
| Dev | Qwen3-4B | 14/50 | 15/50 |
| Test | Qwen2.5-3B | 31/150 | 31/150 |
| Test | Qwen3-4B | 32/150 | 32/150 |

Noisy Banglish:

| Split | Model | Clean Banglish | Noisy Banglish |
| --- | --- | ---: | ---: |
| Dev | Qwen2.5-3B | 7/50 | 7/50 |
| Dev | Qwen3-4B | 14/50 | 15/50 |
| Test | Qwen2.5-3B | 31/150 | 34/150 |
| Test | Qwen3-4B | 32/150 | 31/150 |

Self-normalization:

| Split | Model | Baseline Banglish | Self-normalized |
| --- | --- | ---: | ---: |
| Dev | Qwen2.5-3B | 7/50 | 10/50 |
| Dev | Qwen3-4B | 14/50 | 5/50 |
| Test | Qwen2.5-3B | 31/150 | 41/150 |
| Test | Qwen3-4B | 32/150 | 16/150 |

## Interpretation

- The clean Banglish gap appears on both dev and test for both main models.
- The test split preserves the main full-validation conclusion: Banglish remains
  below Bangla and English.
- v4 cleanup does not materially change test accuracy.
- Current deterministic noisy Banglish still does not explain the gap.
- Self-normalization directions agree between dev and test: positive for
  Qwen2.5-3B and negative for Qwen3-4B.
- Dev BanglaMATH is too small and currently has zero baseline correct across
  scripts, so routing decisions should not rely on dev math accuracy alone.

## Generated Artifacts

- `scripts/summarize_outputs_by_slice.py`
- `results/analysis/validation200_v4_devtest_baseline_v3_by_split_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_baseline_v3_by_split_dataset_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_v4_banglish_by_split_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_v4_banglish_by_split_dataset_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_noisy_v3_by_split_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_noisy_v3_by_split_dataset_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_selfnorm_v3_by_split_variant_reparsed_rescored.csv`
- `results/analysis/validation200_v4_devtest_selfnorm_v3_by_split_dataset_variant_reparsed_rescored.csv`

## Next Use

The next routing or prompt experiment should be selected using dev only. The
most defensible immediate candidate is a routing method that decides between
baseline and self-normalization without looking at test labels, because the
oracle results show recoverable signal but current preservation heuristics are
too weak.

Follow-up completed:

- `reports/selfnorm_routing_devtest_validation200_v4.md` applies this protocol
  to self-normalization routing.
