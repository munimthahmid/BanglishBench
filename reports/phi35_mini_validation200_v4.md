# Phi-3.5-mini Validation-200 v4 Probe

Updated: 2026-05-28 11:56 +0600

This report summarizes the non-Qwen Phi-3.5-mini baseline on the validation-200
v4 dev/test split.

## Runs

Dev50:

- Kernel: `munimthahmid/phi35-mini-validation200-v4-dev50`
- Output: `results/runs/phi35_mini_validation200_v4_dev50/results/runs/phi35_mini_validation200_v4_dev50.jsonl`

Test150:

- Kernel: `munimthahmid3/phi35-mini-validation200-v4-test150`
- Output: `results/runs/phi35_mini_validation200_v4_test150/results/runs/phi35_mini_validation200_v4_test150.jsonl`

Model and settings:

- Model: `microsoft/Phi-3.5-mini-instruct`
- Prompt mode: baseline
- Variants: Bangla, clean Banglish, English
- Max new tokens: 128
- Pinned Kaggle package stack: `transformers==4.43.4`,
  `accelerate==0.33.0`

## Split Results

| Split | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| Dev50 | 5/50 | 7/50 | 19/50 |
| Test150 | 33/150 | 33/150 | 61/150 |
| Full200 | 38/200 | 40/200 | 80/200 |

By dataset, full200:

| Dataset | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 37/144 | 40/144 | 67/144 |
| BanglaMATH | 1/56 | 0/56 | 13/56 |

## Paired Bootstrap

| Comparison | Delta | 95% CI |
| --- | ---: | ---: |
| Banglish - Bangla | +1 point | [-4, +6] |
| Banglish - English | -20 points | [-28, -11.5] |

Artifacts:

- `results/analysis/phi35_validation200_v4_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/phi35_validation200_v4_banglish_minus_english_bootstrap.csv`

## Comparison With Qwen Results

Full validation-200:

| Model | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 38/200 | 71/200 |
| Qwen3-4B | 80/200 | 46/200 | 88/200 |
| Phi-3.5-mini | 38/200 | 40/200 | 80/200 |

Important caveat: Qwen rows are validation-200 v3 for Bangla and English, and
their Banglish v4 sensitivity changed only by +1 correct for each model. Phi is
reported on validation-200 v4. Item ids are the same.

## Interpretation

- Phi-3.5-mini is a useful non-Qwen contrast, not a replication of the Qwen
  script ordering.
- It does not show a Banglish-below-Bangla gap: Banglish is statistically tied
  with Bangla, 40/200 vs 38/200.
- It does show a large English-vs-Banglish gap, 80/200 vs 40/200, with a clearly
  negative paired interval.
- Phi's English score is competitive with the Qwen baselines, but its native
  Bangla score is much lower than Qwen3 and lower than Qwen2.5.
- This suggests the main thesis should distinguish two phenomena:
  1. English-centric model competence gaps, visible in Phi and Qwen.
  2. Banglish-below-Bangla script gaps, robust in the Qwen models but not
     universal across all compact instruction models.

## Thesis Use

Use Phi-3.5-mini as model-family breadth and nuance:

- It prevents overclaiming that every model ranks Bangla above Banglish.
- It supports the broader claim that script/language choice strongly changes
  behavior.
- The central Banglish-deficit claim should remain anchored in Qwen2.5-3B and
  Qwen3-4B, especially Qwen3 BEnQA.

## Generated Artifacts

- `results/runs/phi35_mini_validation200_v4_dev50/summary_by_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_dev50/summary_by_dataset_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_test150/summary_by_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_test150/summary_by_dataset_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_full200_by_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_full200_by_dataset_variant_reparsed_rescored.csv`
- `results/analysis/phi35_validation200_v4_devtest_by_split_variant_reparsed_rescored.csv`
- `results/analysis/phi35_validation200_v4_devtest_by_split_dataset_variant_reparsed_rescored.csv`
