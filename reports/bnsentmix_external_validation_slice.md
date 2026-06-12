# BnSentMix External-Validation Slice

Updated: 2026-06-11

## Purpose

This layer evaluates zero-shot sentiment classification on naturally
occurring Bengali-English code-mixed text. It broadens the thesis beyond
controlled romanized benchmark variants. It is an ecological-validity
layer, not a paired causal estimate of script effects.

## Upstream Source

- Dataset card: https://huggingface.co/datasets/aplycaebous/BnSentMix
- Paper: https://aclanthology.org/2025.loreslm-1.4/
- Local pinned CSV: `literature/data/bnsentmix/dataset.csv`
- Source SHA-256: `148f23eb3dc40c1012a973efec920eaccc39700a74e5bcfb56806b0bf389029d`
- The paper and card describe 20,000 samples. The current pinned CSV
  contains 20,015 rows; exact duplicate text
  rows removed before sampling: 209.
- License metadata needs reconciliation before public redistribution:
  the paper states CC BY 4.0 while the current Hugging Face card states MIT.

## Slice Design

- Output: `data/slices/bnsentmix_balanced200_v1.jsonl`
- Sampling seed: `20260603`
- Balanced external slice: 200 rows (50 per label).
- Pilot prefix: 40 rows (10 per label).
- Prompt output is a sentiment word, not an A/B/C/D option, so the
  external layer does not reuse the core MCQ label-position behavior.

| Label | Unique source rows | Slice rows | Pilot rows |
| --- | ---: | ---: | ---: |
| positive | 5343 | 50 | 10 |
| negative | 6090 | 50 | 10 |
| neutral | 6609 | 50 | 10 |
| mixed | 1764 | 50 | 10 |

## Interpretation Contract

- Report accuracy, macro-F1, per-label recall, and invalid output rate.
- Compare models within this independently sampled external layer.
- Do not compare its absolute accuracy directly with the paired
  knowledge benchmark as if the tasks had equal difficulty.
- Treat data contamination as an open threat because the public
  dataset predates the evaluated instruction checkpoints.
