#!/usr/bin/env python3
"""Export a markdown report of Banglish field changes between two JSONL files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            rows[str(row["id"])] = row
    return rows


def block(title: str, text: str) -> str:
    return f"**{title}**\n\n```text\n{text.strip()}\n```\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--field", default="banglish_clean")
    parser.add_argument("--limit", type=int, default=40)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    before = load_jsonl(args.before)
    after = load_jsonl(args.after)
    changed = []
    for item_id, before_row in before.items():
        after_row = after.get(item_id)
        if not after_row:
            continue
        before_text = str(before_row.get(args.field, ""))
        after_text = str(after_row.get(args.field, ""))
        if before_text != after_text:
            changed.append((item_id, before_row, after_row, before_text, after_text))

    lines = [
        f"# Banglish Diff Report: {args.field}",
        "",
        f"- Before: `{args.before}`",
        f"- After: `{args.after}`",
        f"- Changed items: {len(changed)}",
        f"- Showing: {min(args.limit, len(changed))}",
        "",
    ]
    for idx, (item_id, before_row, after_row, before_text, after_text) in enumerate(
        changed[: args.limit], start=1
    ):
        lines.extend(
            [
                f"## {idx}. {item_id}",
                "",
                f"- Dataset: `{before_row.get('dataset', '')}`",
                f"- Task type: `{before_row.get('task_type', '')}`",
                "",
                block("Bangla", str(before_row.get("bangla", ""))),
                block("Before", before_text),
                block("After", after_text),
            ]
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {args.output} with {len(changed)} changed items")


if __name__ == "__main__":
    main()
