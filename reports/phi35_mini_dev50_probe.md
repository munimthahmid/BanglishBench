# Phi-3.5-mini Dev50 Probe

Updated: 2026-05-28 11:56 +0600

This is the first non-Qwen dev/test protocol probe after the Phi-4-mini Kaggle
stack failure.

## Run

- Model: `microsoft/Phi-3.5-mini-instruct`
- Slice: `data/slices/validation_200_v4_dev50.jsonl`
- Variants: Bangla, clean Banglish, English
- Prompt mode: baseline
- Max new tokens: 128
- Kaggle kernel: `munimthahmid/phi35-mini-validation200-v4-dev50`
- Local outputs: `results/runs/phi35_mini_validation200_v4_dev50/`
- Package stack: `transformers==4.43.4`, `accelerate==0.33.0`

## Results

Overall:

| Variant | Correct | Accuracy |
| --- | ---: | ---: |
| Bangla | 5/50 | 0.10 |
| Clean Banglish | 7/50 | 0.14 |
| English | 19/50 | 0.38 |

By dataset:

| Dataset | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 5/36 | 7/36 | 17/36 |
| BanglaMATH | 0/14 | 0/14 | 2/14 |

For comparison on the same dev50 split:

| Model | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 11/50 | 7/50 | 18/50 |
| Qwen3-4B | 19/50 | 14/50 | 21/50 |
| Phi-3.5-mini | 5/50 | 7/50 | 19/50 |

## Interpretation

- Phi-3.5-mini is competent enough in English on dev50 to be informative.
- It is much weaker than Qwen3 on Bangla and Banglish.
- Unlike the Qwen-family main result, Phi-3.5-mini does not show a dev-set
  Banglish-below-Bangla gap; Banglish is slightly higher than native Bangla.
- This is useful nuance: the thesis should avoid claiming every model has the
  same Bangla-vs-Banglish ordering. The stronger claim is that script choice
  changes model behavior, and in Qwen models with better Bangla competence it
  produces a robust Banglish deficit.

## Decision

Run the unchanged test150 baseline for Phi-3.5-mini because the dev result is
not degenerate:

- English is 19/50.
- Bangla and Banglish are non-zero on BEnQA.
- The non-Qwen script ordering is different enough to matter for the thesis.

## Artifacts

- `results/runs/phi35_mini_validation200_v4_dev50/results/runs/phi35_mini_validation200_v4_dev50.jsonl`
- `results/runs/phi35_mini_validation200_v4_dev50/summary_by_variant_reparsed_rescored.csv`
- `results/runs/phi35_mini_validation200_v4_dev50/summary_by_dataset_variant_reparsed_rescored.csv`
