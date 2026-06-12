#!/usr/bin/env python3
"""Summarize JSONL model evaluation outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_GROUP_BY = ["model", "dataset", "task_type", "variant", "answer_type"]


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if "correct" not in row or "variant" not in row or "model" not in row:
                    continue
                row["_source"] = str(path)
                row["_line"] = line_no
                rows.append(row)
    return rows


def rescore_rows(rows: list[dict[str, Any]]) -> None:
    from run_eval_kaggle import is_correct, parse_answer

    for row in rows:
        if row.get("raw_output"):
            row["parsed"] = parse_answer(
                str(row.get("raw_output", "")),
                str(row.get("answer_type", "")),
            )
        row["correct"] = is_correct(
            str(row.get("parsed", "")),
            str(row.get("gold", "")),
            str(row.get("answer_type", "")),
        )


def summarize(rows: list[dict[str, Any]], group_by: list[str]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(column, "") for column in group_by)
        groups[key].append(row)

    summary_rows: list[dict[str, Any]] = []
    for key, items in sorted(groups.items(), key=lambda item: item[0]):
        seconds = [float(row.get("seconds", 0.0) or 0.0) for row in items]
        correct = sum(1 for row in items if bool(row.get("correct")))
        parsed_empty = sum(1 for row in items if not str(row.get("parsed", "")).strip())
        out = {column: value for column, value in zip(group_by, key)}
        out.update(
            {
                "n": len(items),
                "unique_items": len({row.get("id") for row in items}),
                "correct": correct,
                "accuracy": round(correct / len(items), 4) if items else 0.0,
                "parsed_empty": parsed_empty,
                "mean_seconds": round(sum(seconds) / len(seconds), 4) if seconds else 0.0,
                "total_seconds": round(sum(seconds), 4),
            }
        )
        summary_rows.append(out)
    return summary_rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows: list[dict[str, Any]], group_by: list[str]) -> None:
    fields = group_by + ["n", "correct", "accuracy", "mean_seconds"]
    widths = {
        field: max(len(field), *(len(str(row.get(field, ""))) for row in rows))
        for field in fields
    }
    print(" | ".join(field.ljust(widths[field]) for field in fields))
    print("-+-".join("-" * widths[field] for field in fields))
    for row in rows:
        print(" | ".join(str(row.get(field, "")).ljust(widths[field]) for field in fields))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--group-by", nargs="+", default=DEFAULT_GROUP_BY)
    parser.add_argument(
        "--rescore",
        action="store_true",
        help="Recompute correctness with the current answer-normalization code.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(jsonl_paths(args.inputs))
    if not rows:
        raise SystemExit("No evaluation rows found.")
    if args.rescore:
        rescore_rows(rows)

    summary_rows = summarize(rows, args.group_by)
    fieldnames = args.group_by + [
        "n",
        "unique_items",
        "correct",
        "accuracy",
        "parsed_empty",
        "mean_seconds",
        "total_seconds",
    ]
    write_csv(args.output, summary_rows, fieldnames)
    print_table(summary_rows, args.group_by)
    print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()
