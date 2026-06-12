# Thesis Qualitative Examples

Updated: 2026-05-31

## Purpose

This file is the short thesis-facing pointer to the frozen-v5 qualitative
packet. Use `reports/v5_shared_fragility_examples.md` as the authoritative
example source because it is regenerated from the model-overlap and
failure-pattern tables.

Use examples to make the aggregate script-gap result concrete. Do not use them
as standalone proof of a causal mechanism.

## Main-Body Shortlist

These three examples are recommended for Chapter 6 prose or a compact table:

| Slot | Example | Task | Pattern | Why It Belongs |
| --- | --- | --- | --- | --- |
| A | `banglamath_0229` | BanglaMATH short answer | All three thesis-facing Qwen rows are correct in Bangla and English but wrong in reviewed Banglish. | Very short arithmetic item; the Banglish error is easy to see. |
| B | `banglamath_0230` | BanglaMATH short answer | All three thesis-facing Qwen rows are strict Bangla+English-correct/Banglish-wrong. | Shows reviewed-v5 wording still leaves a clean script-conditioned numeric miss. |
| C | `benqa_10th-Physics_0021` | BEnQA MCQ | All three thesis-facing Qwen rows choose gold `C` in Bangla and English, but choose non-gold options in Banglish. | Adds a non-arithmetic curriculum MCQ example with simple option parsing. |

## Frozen-V5 Counts

- Shared Banglish fragility: 56/200 items affect at least two Qwen rows.
- All-three fragility: 21/200 items affect all three Qwen rows.
- Shared strict fragility: 17/200 items affect at least two Qwen rows under
  the Bangla+English-correct/Banglish-wrong pattern.
- All-three strict qualitative cases: 5/200 items.

## Artifacts

- Main packet: `reports/v5_shared_fragility_examples.md`
- Machine-readable examples: `results/analysis/v5_shared_fragility_examples.csv`
- Builder: `scripts/export_v5_shared_fragility_examples.py`
- Overlap source: `reports/v5_banglish_fragility_model_overlap.md`
- Failure taxonomy source: `reports/cross_script_diagnostics_validation200_v5.md`

## Boundary

The examples should be described as qualitative illustrations of the
frozen-v5 aggregate evidence. The claim should cite the aggregate diagnostics:
185/600 fragile model-item slots, 108/200 any-fragile items, and 56/108
any-fragile items shared by at least two thesis-facing Qwen rows.
