#!/usr/bin/env python3
"""Export a CSV sheet for reviewing or correcting Banglish variants."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def flatten(text: str) -> str:
    return (text or "").replace("\r", " ").replace("\n", " \\n ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "dataset",
        "task_type",
        "domain",
        "answer",
        "bangla",
        "current_banglish",
        "noisy_banglish",
        "english",
        "reviewed_banglish",
        "quality_label",
        "review_notes",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "id": row["id"],
                    "dataset": row["dataset"],
                    "task_type": row["task_type"],
                    "domain": row.get("domain", ""),
                    "answer": row.get("answer", ""),
                    "bangla": flatten(row.get("bangla", "")),
                    "current_banglish": flatten(row.get("banglish_clean", "")),
                    "noisy_banglish": flatten(row.get("banglish_noisy", "")),
                    "english": flatten(row.get("english", "")),
                    "reviewed_banglish": "",
                    "quality_label": "",
                    "review_notes": "",
                }
            )
    print(f"Wrote {len(rows)} review rows to {args.output}")


if __name__ == "__main__":
    main()
