# BEnQA 1,000 Human Review Fastpack

Updated: 2026-06-06

## Purpose

This fastpack is for converting the BEnQA 1,000-row extension from
AI-assisted triage into a human-reviewed extension. It is designed for
fast row-by-row review without hiding quality checks.

## Files

- Dashboard: `reports/benqa_ext_human_review_fast/index.html`
- Source rows: `data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl`
- Review queue CSV: `results/analysis/benqa_extended_1000_v1_human_review_queue.csv`
- Spreadsheet template: `results/analysis/benqa_extended_1000_v1_human_review_template.csv`

## Counts

- Total rows: 1000
- AI-warning rows shown first: 149
- AI-pass rows after warnings: 851

## Blitz Protocol

1. Open `index.html` in a browser.
2. Start with the default `Todo first` filter; rows with AI warnings are already first.
3. For each row, compare Bangla source against Banglish.
4. Accept if question, options, digits/formulas, answer label, and answer instruction are preserved.
5. Edit only the Banglish field when the fix is obvious.
6. Reject if option mapping, formula/digit content, or meaning is uncertain.
7. Export JSONL when done or at every break.

Keyboard shortcuts: `A` accept, `E` edited, `R` reject, `U` unsure, `N` next, `P` previous.

## After Export

Save the exported JSONL as:

`results/analysis/benqa_extended_1000_v1_human_review_decisions.jsonl`

Then freeze the reviewed extension with:

```bash
python3 scripts/freeze_benqa_human_reviewed_extension.py
```

The freeze script writes:

- `data/slices/benqa_extended_1000_v1_human_reviewed.jsonl`
- `data/slices/benqa_extended_1000_v1_human_gold.jsonl`
- `reports/benqa_extended_1000_v1_human_review_freeze.md`

## Freeze Rule

The extension should only be called human-reviewed after every row has a
human decision and the exported JSONL is used to build a frozen reviewed
slice. Rows marked `reject` or `unsure` should not enter the gold extension.
