#!/usr/bin/env python3
"""Create human-review suggestions for common rule-based Banglish artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


REPLACEMENTS: dict[str, str] = {
    "achhe": "ache",
    "ayotakar": "ayotokar",
    "choora": "chowra",
    "doirghy": "doirgho",
    "ekoti": "ekti",
    "konoti": "konti",
    "korote": "korte",
    "kot": "koto",
    "kshetre": "khetre",
    "kshetrofol": "khetrofol",
    "penyaj": "peyaj",
    "prosth": "prostho",
    "sborn": "shorno",
    "thakole": "thakle",
    "uchchota": "ucchota",
}


def replace_word(text: str, old: str, new: str) -> tuple[str, int]:
    pattern = re.compile(rf"\b{re.escape(old)}\b")
    return pattern.subn(new, text)


def suggest(text: str) -> tuple[str, list[str]]:
    suggested = text
    notes: list[str] = []
    for old, new in REPLACEMENTS.items():
        suggested, count = replace_word(suggested, old, new)
        if count:
            notes.append(f"{old}->{new} ({count})")
    return suggested, notes


def read_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit("No rows to write")
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


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Banglish Review Suggestions v3\n\n")
        f.write(
            "These are heuristic suggestions for human review. They are not "
            "human-reviewed labels and should not be applied blindly.\n\n"
        )
        changed = [row for row in rows if row["suggestion_notes"]]
        f.write(f"Items with suggestions: {len(changed)} / {len(rows)}\n\n")
        for index, row in enumerate(changed, start=1):
            f.write(f"## {index}. {row['id']}\n\n")
            f.write(f"- Dataset: `{row['dataset']}`\n")
            f.write(f"- Patterns: `{row['patterns']}`\n")
            f.write(f"- Suggested edits: {row['suggestion_notes']}\n\n")
            f.write("Current Banglish:\n\n```text\n")
            f.write(str(row["banglish_clean"]).rstrip() + "\n")
            f.write("```\n\nSuggested Banglish:\n\n```text\n")
            f.write(str(row["suggested_banglish"]).rstrip() + "\n")
            f.write("```\n\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--csv-output", type=Path, required=True)
    parser.add_argument("--md-output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_rows(args.review)
    out_rows: list[dict[str, Any]] = []
    for row in rows:
        suggested, notes = suggest(str(row.get("banglish_clean", "")))
        new_row = dict(row)
        new_row["suggested_banglish"] = suggested if notes else ""
        new_row["suggestion_notes"] = "; ".join(notes)
        out_rows.append(new_row)
    write_csv(args.csv_output, out_rows)
    write_markdown(args.md_output, out_rows)
    print(f"rows={len(out_rows)}")
    print(f"suggested={sum(1 for row in out_rows if row['suggestion_notes'])}")
    print(f"wrote={args.csv_output}")
    print(f"wrote={args.md_output}")


if __name__ == "__main__":
    main()
