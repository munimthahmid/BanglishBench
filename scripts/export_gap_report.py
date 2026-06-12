#!/usr/bin/env python3
"""Export a Markdown report for selected script-gap examples."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                items[row["id"]] = row
    return items


def load_gap_rows(
    path: Path,
    pattern: str,
    limit: int,
    filters: dict[str, str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("pattern") == pattern:
                if any(row.get(key, "") != value for key, value in filters.items()):
                    continue
                rows.append(row)
    return rows[:limit]


def block(label: str, text: str) -> str:
    return f"**{label}**\n\n```text\n{text.strip()}\n```\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--gaps", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pattern", default="banglish_drop_vs_bangla_english")
    parser.add_argument(
        "--filter",
        action="append",
        default=[],
        help="Optional CSV row filter as column=value. Can be repeated.",
    )
    parser.add_argument("--limit", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_items(args.items)
    filters: dict[str, str] = {}
    for value in args.filter:
        if "=" not in value:
            raise SystemExit(f"Invalid --filter {value!r}; expected column=value")
        key, raw = value.split("=", 1)
        filters[key] = raw
    rows = load_gap_rows(args.gaps, args.pattern, args.limit, filters)

    lines = [
        f"# Script-Gap Examples: `{args.pattern}`",
        "",
        f"Source gaps: `{args.gaps}`",
        f"Items: `{args.items}`",
        f"Filters: `{filters}`",
        f"Examples exported: {len(rows)}",
        "",
    ]

    for idx, row in enumerate(rows, start=1):
        item = items[row["id"]]
        lines.extend(
            [
                f"## {idx}. {row['id']} ({row['dataset']}, {row['task_type']})",
                "",
                f"Model: `{row.get('model', '')}`",
                "",
                f"Gold: `{row['gold']}`",
                "",
                block("Bangla Prompt", item.get("bangla", "")),
                f"Bangla parsed: `{row.get('bangla_parsed', '')}`; correct: `{row.get('bangla_correct', '')}`",
                "",
                block("Banglish Prompt", item.get("banglish_clean", "")),
                f"Banglish parsed: `{row.get('banglish_clean_parsed', '')}`; correct: `{row.get('banglish_clean_correct', '')}`",
                "",
                block("English Prompt", item.get("english", "")),
                f"English parsed: `{row.get('english_parsed', '')}`; correct: `{row.get('english_correct', '')}`",
                "",
            ]
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
