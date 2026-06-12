# Guarded Generated-English Repair

Updated: 2026-06-11

## Purpose

This deterministic repair creates a conservative generated-English view
from Qwen3 self-translation outputs. It restores source option and
answer-format lines, keeps a translated stem only if the hard
preservation gate still passes, and otherwise falls back to the original
Banglish item. This is a dev diagnostic, not a claim that the fallback
rows are translated English.

## Artifacts

- Prompt set: `data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl`
- Input generated-English outputs: `results/generated_views/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq.jsonl`
- Repaired output JSONL: `results/generated_views/qwen3_4b_selftranslate_guarded_v5_dev50_benqa_mcq_generated_en.jsonl`

## Counts

- Rows: 36
- `source_fallback_after_failed_repair`: 15
- `translated_stem_source_tail`: 21

## Decision Rule

Run `scripts/audit_generated_view_outputs.py` on this file before any
answer audit. Even if the gate passes, use the results only as a
conservative generated-English diagnostic because fallback rows are
the original Banglish view.
