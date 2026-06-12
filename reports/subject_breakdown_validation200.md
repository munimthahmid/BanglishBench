# Validation-200 Subject Breakdown

Updated: 2026-05-28 11:56 +0600

This report checks whether the main Banglish gap is concentrated in one subject
area or spread across the validation-200 slice.

## Method

Joined baseline evaluation outputs with item metadata from:

- `data/slices/validation_200_v3.jsonl`

Generated summary:

- `results/analysis/validation200_v3_baseline_by_metadata_stratum_reparsed_rescored.csv`

For BEnQA, `stratum` is the source subject. For BanglaMATH, `stratum` is grade.

## BEnQA Subject Breakdown

Qwen2.5-3B:

| Subject | n | Bangla | Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Biology | 12 | 5 | 0 | 3 | -5 |
| Biology-I | 11 | 3 | 2 | 7 | -1 |
| Biology-II | 11 | 3 | 3 | 6 | 0 |
| Chemistry | 11 | 3 | 3 | 7 | 0 |
| Chemistry-I | 11 | 4 | 2 | 5 | -2 |
| Chemistry-II | 11 | 2 | 4 | 6 | +2 |
| Math | 11 | 5 | 3 | 8 | -2 |
| Math-I | 11 | 3 | 3 | 2 | 0 |
| Math-II | 11 | 6 | 5 | 3 | -1 |
| Physics | 11 | 5 | 5 | 7 | 0 |
| Physics-I | 11 | 4 | 4 | 5 | 0 |
| Physics-II | 11 | 2 | 3 | 3 | +1 |
| Science | 11 | 4 | 1 | 4 | -3 |

Qwen3-4B:

| Subject | n | Bangla | Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Biology | 12 | 5 | 3 | 4 | -2 |
| Biology-I | 11 | 6 | 2 | 6 | -4 |
| Biology-II | 11 | 6 | 2 | 4 | -4 |
| Chemistry | 11 | 7 | 4 | 8 | -3 |
| Chemistry-I | 11 | 7 | 5 | 9 | -2 |
| Chemistry-II | 11 | 7 | 2 | 8 | -5 |
| Math | 11 | 5 | 2 | 6 | -3 |
| Math-I | 11 | 5 | 4 | 5 | -1 |
| Math-II | 11 | 6 | 7 | 5 | +1 |
| Physics | 11 | 8 | 5 | 9 | -3 |
| Physics-I | 11 | 6 | 4 | 6 | -2 |
| Physics-II | 11 | 3 | 2 | 4 | -1 |
| Science | 11 | 5 | 3 | 8 | -2 |

## BanglaMATH Grade Breakdown

Qwen2.5-3B:

| Grade | n | Bangla | Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eight | 16 | 0 | 0 | 0 | 0 |
| seven | 20 | 2 | 0 | 1 | -2 |
| six | 20 | 3 | 0 | 4 | -3 |

Qwen3-4B:

| Grade | n | Bangla | Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eight | 16 | 2 | 1 | 2 | -1 |
| seven | 20 | 0 | 0 | 1 | 0 |
| six | 20 | 2 | 0 | 3 | -2 |

## Interpretation

- Qwen3's BEnQA Banglish deficit is broad: Banglish is below Bangla in 12 of 13
  BEnQA strata, with only Math-II slightly positive.
- Qwen2.5's BEnQA gap is weaker and more mixed by subject, matching the smaller
  overall Banglish-vs-Bangla gap.
- BanglaMATH is too low-accuracy for fine-grained subject claims. It is useful as
  a stress test but not the cleanest place to explain the script gap.
- The strongest subject-level thesis evidence should come from Qwen3 BEnQA,
  because the deficit is both larger and more consistently distributed.

## Generated Artifact

- `scripts/summarize_outputs_by_metadata.py`
