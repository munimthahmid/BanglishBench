# Indic-Gemma-2B Validation-200 v4 Pilot20

Updated: 2026-05-28

## Purpose

This pilot tests whether
`Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0` is a useful small
Indic-family model-family breadth point for Script Matters.

## Setup

- Model: `Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0`
- Size/class: 2B Gemma-family instruction model
- Slice: first 20 items from `data/slices/validation_200_v4_dev50.jsonl`
- Variants: Bangla, clean Banglish, English
- Prompt mode: baseline
- Prompt wrapper: `alpaca`
- Max new tokens: 128
- Quantization: none
- Kaggle kernel: `munimthahmid3/indic-gemma2b-v4-dev50-p20`

The Alpaca wrapper was required because this checkpoint has no tokenizer chat
template and its model card specifies `### Instruction`, `### Input`,
`### Response` formatting.

## Result

| Variant | Correct | Parsed empty | Mean seconds |
| --- | ---: | ---: | ---: |
| Bangla | 4/20 | 0 | 0.7819 |
| Clean Banglish | 3/20 | 0 | 0.2484 |
| English | 5/20 | 0 | 0.2829 |

By dataset:

| Dataset | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 3/15 | 3/15 | 4/15 |
| BanglaMATH | 1/5 | 0/5 | 1/5 |

The model is operationally feasible and fast after load, with no parsed-empty
failures. However, the pilot is MCQ-heavy and the BEnQA scores are around
four-choice chance.

## Interpretation

Indic-Gemma-2B is a valid diagnostic run but not a useful thesis-facing baseline
under the current protocol:

- It follows the Alpaca-wrapped answer protocol better than the BanglaLLM and
  TituLM diagnostics.
- Accuracy is too low to justify full dev50/test150 GPU spend.
- There is no meaningful Bangla/Banglish/English ordering signal on pilot20.

Decision: do not scale this model now. Keep it as evidence that a small
Bengali-tagged Indic instruction model is easy to run but too weak for the main
benchmark.

## Artifacts

- Output directory:
  `results/runs/indic_gemma2b_validation200_v4_dev50_pilot20/`
- JSONL outputs:
  `results/runs/indic_gemma2b_validation200_v4_dev50_pilot20/results/runs/indic_gemma2b_validation200_v4_dev50_pilot20.jsonl`
- Variant summary:
  `results/runs/indic_gemma2b_validation200_v4_dev50_pilot20/summary_by_variant_reparsed_rescored.csv`
- Dataset summary:
  `results/runs/indic_gemma2b_validation200_v4_dev50_pilot20/summary_by_dataset_variant_reparsed_rescored.csv`
