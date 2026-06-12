#!/usr/bin/env python3
"""Apply conservative heuristic Banglish suggestions to a JSONL candidate slice."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from suggest_banglish_review_edits import REPLACEMENTS, suggest


ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def note_pairs(notes: list[str]) -> list[str]:
    return [note.split(" ", 1)[0] for note in notes]


def apply_suggestions(
    rows: list[dict[str, Any]],
    fields: list[str],
    quality_status: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    output: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    for row in rows:
        item = dict(row)
        item_id = str(item.get("id", ""))
        old_status = str(item.get("quality_status", ""))
        changed_fields: list[str] = []
        item_notes: dict[str, list[str]] = {}

        for field in fields:
            old_text = str(item.get(field, ""))
            if not old_text:
                continue
            new_text, notes = suggest(old_text)
            changed = new_text != old_text
            if changed:
                item[field] = new_text
                changed_fields.append(field)
                item_notes[field] = notes
                counts[f"changed_field:{field}"] += 1
                for pair in note_pairs(notes):
                    counts[f"replacement:{field}:{pair}"] += 1

            audit_rows.append(
                {
                    "id": item_id,
                    "dataset": item.get("dataset", ""),
                    "field": field,
                    "changed": changed,
                    "suggestion_notes": "; ".join(notes),
                    "old_text": old_text,
                    "new_text": new_text,
                }
            )

        item["quality_status"] = quality_status
        item["banglish_auto_suggestion"] = {
            "human_reviewed": False,
            "previous_quality_status": old_status,
            "source_script": "scripts/apply_banglish_auto_suggestions.py",
            "replacement_source": "scripts/suggest_banglish_review_edits.py",
            "changed_fields": changed_fields,
            "suggestion_notes": {
                field: "; ".join(notes) for field, notes in item_notes.items()
            },
        }
        if changed_fields:
            counts["items_with_any_change"] += 1
            counts[f"dataset:{item.get('dataset', '')}:changed"] += 1
        else:
            counts["items_without_text_change"] += 1
        output.append(item)

    counts["items"] = len(rows)
    counts["audit_rows"] = len(audit_rows)
    return output, audit_rows, counts


def write_markdown_report(
    path: Path,
    input_path: Path,
    output_path: Path,
    audit_path: Path,
    manifest_path: Path,
    counts: Counter[str],
    audit_rows: list[dict[str, Any]],
    fields: list[str],
    quality_status: str,
    max_examples: int,
) -> None:
    changed_rows = [row for row in audit_rows if row["changed"]]
    replacement_counts = {
        key.removeprefix("replacement:"): value
        for key, value in sorted(counts.items())
        if key.startswith("replacement:")
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Validation-200 v4 Auto-Suggested Banglish Candidate\n\n")
        f.write(f"Updated: {datetime.now(timezone.utc).date().isoformat()}\n\n")
        f.write("## Purpose\n\n")
        f.write(
            "This file documents a heuristic, unreviewed candidate slice created "
            "by applying the conservative Banglish replacement map already used "
            "for the human-review suggestion packet. It is intended for data QA "
            "and reviewer triage, not as a thesis-grade frozen v5 benchmark.\n\n"
        )
        f.write("## Artifacts\n\n")
        f.write(f"- Input: `{repo_path(input_path)}`\n")
        f.write(f"- Output: `{repo_path(output_path)}`\n")
        f.write(f"- Audit CSV: `{repo_path(audit_path)}`\n")
        f.write(f"- Manifest: `{repo_path(manifest_path)}`\n")
        f.write(f"- Fields edited: `{', '.join(fields)}`\n")
        f.write(f"- Output quality status: `{quality_status}`\n\n")

        f.write("## Counts\n\n")
        f.write(f"- Items: {counts['items']}\n")
        f.write(f"- Items with any text change: {counts['items_with_any_change']}\n")
        f.write(f"- Items without text change: {counts['items_without_text_change']}\n")
        for field in fields:
            f.write(
                f"- Changed `{field}` rows: {counts[f'changed_field:{field}']}\n"
            )
        f.write("\n")

        if replacement_counts:
            f.write("## Replacement Counts\n\n")
            f.write("| Field / replacement | Rows affected |\n")
            f.write("| --- | ---: |\n")
            for key, value in replacement_counts.items():
                f.write(f"| `{key}` | {value} |\n")
            f.write("\n")

        f.write("## Caveats\n\n")
        f.write("- These edits are automatic spelling-normalization suggestions.\n")
        f.write("- They are not human-reviewed labels or final Banglish gold text.\n")
        f.write(
            "- The candidate may be useful for a sensitivity rerun, but any v5 "
            "benchmark claim still needs the human-review workflow.\n"
        )
        f.write(
            "- The replacement map is intentionally narrow; it does not solve "
            "broader naturalness, dialect, or spelling-variation coverage.\n\n"
        )

        f.write("## Changed Examples\n\n")
        for index, row in enumerate(changed_rows[:max_examples], start=1):
            f.write(f"### {index}. {row['id']} / `{row['field']}`\n\n")
            f.write(f"- Dataset: `{row['dataset']}`\n")
            f.write(f"- Suggestions: {row['suggestion_notes']}\n\n")
            f.write("Before:\n\n```text\n")
            f.write(str(row["old_text"]).rstrip() + "\n")
            f.write("```\n\nAfter:\n\n```text\n")
            f.write(str(row["new_text"]).rstrip() + "\n")
            f.write("```\n\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    parser.add_argument("--report-output", type=Path, required=True)
    parser.add_argument(
        "--fields",
        nargs="+",
        default=["banglish_clean", "banglish_noisy"],
        help="Text fields to transform with the conservative suggestion map.",
    )
    parser.add_argument(
        "--quality-status",
        default="auto_suggested_unreviewed_v4_1",
        help="quality_status value written to every output row.",
    )
    parser.add_argument("--max-report-examples", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    output, audit_rows, counts = apply_suggestions(
        rows,
        args.fields,
        args.quality_status,
    )
    write_jsonl(args.output, output)
    write_csv(args.audit_output, audit_rows)

    manifest_path = args.output.with_suffix(".manifest.json")
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(args.input),
        "output": repo_path(args.output),
        "audit_output": repo_path(args.audit_output),
        "report_output": repo_path(args.report_output),
        "same_item_order": [row.get("id") for row in rows]
        == [row.get("id") for row in output],
        "fields": args.fields,
        "quality_status": args.quality_status,
        "human_reviewed": False,
        "replacement_map": REPLACEMENTS,
        "counts": dict(sorted(counts.items())),
        "notes": [
            "This is an auto-suggested candidate, not validation-200 v5.",
            "Use the human-review workflow before making final benchmark claims.",
            "Item ids, answers, Bangla prompts, English prompts, and source metadata are preserved.",
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown_report(
        args.report_output,
        args.input,
        args.output,
        args.audit_output,
        manifest_path,
        counts,
        audit_rows,
        args.fields,
        args.quality_status,
        args.max_report_examples,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
