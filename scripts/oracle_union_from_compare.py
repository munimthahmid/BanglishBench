#!/usr/bin/env python3
"""Compute oracle union accuracy from a before/after comparison CSV."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize(rows: list[dict[str, str]], group_by: list[str]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        key = tuple(row.get(column, "") for column in group_by)
        groups.setdefault(key, []).append(row)

    out: list[dict[str, Any]] = []
    for key, items in sorted(groups.items()):
        counts = Counter(row.get("change", "") for row in items)
        before_correct = counts["same_correct"] + counts["loss"]
        after_correct = counts["same_correct"] + counts["gain"]
        oracle_correct = counts["same_correct"] + counts["gain"] + counts["loss"]
        n = len(items)
        row = {column: value for column, value in zip(group_by, key)}
        row.update(
            {
                "n": n,
                "before_correct": before_correct,
                "after_correct": after_correct,
                "oracle_correct": oracle_correct,
                "before_accuracy": round(before_correct / n, 4),
                "after_accuracy": round(after_correct / n, 4),
                "oracle_accuracy": round(oracle_correct / n, 4),
                "oracle_gain_over_before": round((oracle_correct - before_correct) / n, 4),
                "gains": counts["gain"],
                "losses": counts["loss"],
                "same_correct": counts["same_correct"],
                "same_wrong": counts["same_wrong"],
            }
        )
        out.append(row)
    return out


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
    parser.add_argument("compare_csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--group-by", nargs="+", default=["model", "dataset", "variant"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.compare_csv)
    summary = summarize(rows, args.group_by)
    write_csv(args.output, summary)
    for row in summary:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
