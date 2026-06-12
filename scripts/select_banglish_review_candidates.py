#!/usr/bin/env python3
"""Select high-priority Banglish rows for human review."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

from audit_banglish_artifacts import DEFAULT_PATTERNS


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def pattern_hits(text: str) -> list[str]:
    hits: list[str] = []
    for name, pattern in DEFAULT_PATTERNS.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(name)
    return hits


def build_rows(inputs: list[Path], limit: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in inputs:
        for item in load_jsonl(path):
            banglish = str(item.get("banglish_clean", ""))
            hits = pattern_hits(banglish)
            if not hits:
                continue
            out.append(
                {
                    "source_file": str(path),
                    "id": item.get("id", ""),
                    "dataset": item.get("dataset", ""),
                    "task_type": item.get("task_type", ""),
                    "hit_count": len(hits),
                    "patterns": ";".join(hits),
                    "bangla": item.get("bangla", ""),
                    "banglish_clean": banglish,
                    "english": item.get("english", ""),
                    "reviewed_banglish": "",
                    "quality_label": "",
                    "review_notes": "",
                }
            )
    out.sort(key=lambda row: (-int(row["hit_count"]), row["dataset"], row["id"]))
    return out[:limit] if limit else out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit("No review candidates found.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=60)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(args.inputs, args.limit)
    write_csv(args.output, rows)
    print(f"Wrote {args.output} with {len(rows)} candidates")


if __name__ == "__main__":
    main()
