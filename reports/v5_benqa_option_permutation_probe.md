# Frozen-V5 BEnQA Option-Permutation Probe

Updated: 2026-06-11

## Purpose

This controlled dev-only probe rotates each reviewed-Banglish BEnQA MCQ
option content through labels A/B/C/D while remapping the gold label.
It distinguishes semantic-option tracking from fixed-label attraction.
The probe is diagnostic and does not launch held-out test150.

## Inputs

- Frozen validation: `data/slices/validation_200_v5.jsonl`
- Dev-id source: `data/slices/validation_200_v4_dev50.jsonl`
- Probe JSONL: `data/slices/validation200_v5_dev50_benqa_option_permutations.jsonl`

## Counts

- Source dev BEnQA MCQs: 36
- Counterfactual rows: 144
- Rotations per item: 4
- Rows per rotation: 0=36, 1=36, 2=36, 3=36
- Remapped gold labels: A=36, B=36, C=36, D=36

## Interpretation Contract

- If a prediction follows the option content after rotation, it supports
  semantic-option tracking.
- If a prediction remains attached to label D after the original content
  moves away from D, it supports a positional D-attractor.
- Treat all results as dev-only behavioral evidence, not an internal
  causal-mechanism proof.
