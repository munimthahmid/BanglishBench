#!/usr/bin/env python3
"""Heuristic artifact audit for rule-based Banglish fields."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_PATTERNS = {
    "tb_virama_b": r"tb",
    "boij_scientific": r"boij",
    "oja_loanword": r"oja",
    "khady_sanskritized": r"khady",
    "ksh_heavy": r"ksh",
    "db_cluster": r"\bdb",
    "jn_cluster": r"jn",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def snippet(text: str, pattern: str, width: int = 80) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return text[:width].replace("\n", " ")
    start = max(0, match.start() - width // 2)
    end = min(len(text), match.end() + width // 2)
    return text[start:end].replace("\n", " ")


def audit(
    rows: list[dict[str, Any]],
    fields: list[str],
    patterns: dict[str, str],
    max_examples: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summary: list[dict[str, Any]] = []
    examples: list[dict[str, Any]] = []
    for field in fields:
        texts = [(row.get("id", ""), str(row.get(field, ""))) for row in rows if row.get(field)]
        for name, pattern in patterns.items():
            matched = []
            occurrence_count = 0
            for item_id, text in texts:
                matches = re.findall(pattern, text, flags=re.IGNORECASE)
                if not matches:
                    continue
                occurrence_count += len(matches)
                matched.append((item_id, text))
            summary.append(
                {
                    "field": field,
                    "pattern_name": name,
                    "regex": pattern,
                    "items": len(matched),
                    "occurrences": occurrence_count,
                }
            )
            for item_id, text in matched[:max_examples]:
                examples.append(
                    {
                        "field": field,
                        "pattern_name": name,
                        "id": item_id,
                        "snippet": snippet(text, pattern),
                    }
                )
    return summary, examples


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--fields", nargs="+", default=["banglish_clean"])
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--examples-output", type=Path, required=True)
    parser.add_argument("--max-examples", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    summary, examples = audit(rows, args.fields, DEFAULT_PATTERNS, args.max_examples)
    write_csv(args.summary_output, summary)
    write_csv(args.examples_output, examples)
    for row in summary:
        print(
            f"{row['field']} {row['pattern_name']}: "
            f"{row['items']} items, {row['occurrences']} occurrences"
        )
    print(f"Wrote {args.summary_output}")
    print(f"Wrote {args.examples_output}")


if __name__ == "__main__":
    main()
