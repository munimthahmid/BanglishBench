# BEnQA Extended 1000 V1

Updated: 2026-06-05

## Purpose

This artifact adds a publication-scale BEnQA-only extension layer while
keeping `validation_200_v5` as the frozen reviewed gold core. The extension
is intended for scale and robustness checks, not as a replacement for the
deeply audited 200-item paired benchmark.

## Files

- Extended slice: `data/slices/benqa_extended_1000_v1.jsonl`
- Manifest: `data/slices/benqa_extended_1000_v1.manifest.json`

## Construction

- Upstream BEnQA source rows seen: 5087.
- Frozen-core BEnQA rows excluded: 144.
- Candidate pool after required-field filtering: 4939.
- Selected rows: 1000.
- Seed: 20260605.
- Sampling: deterministic round-robin by BEnQA subject file.
- Banglish generation: local rule-based bootstrap romanizer v4.

## Selected Composition

| Group | Count |
| --- | ---: |
| Biology | 77 |
| Biology-I | 77 |
| Biology-II | 77 |
| Chemistry | 77 |
| Chemistry-I | 77 |
| Chemistry-II | 77 |
| Math | 77 |
| Math-I | 77 |
| Math-II | 77 |
| Physics | 77 |
| Physics-I | 77 |
| Physics-II | 77 |
| Science | 76 |

## Review Status

This slice is not human-reviewed. It should be paired with the
AI-assisted review/triage output before any thesis or paper claim uses
it as quality-controlled evidence. Any future human review must be
logged separately from AI-assisted review.
