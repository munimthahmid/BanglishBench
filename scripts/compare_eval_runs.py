#!/usr/bin/env python3
"""Compare two evaluation JSONL outputs at item level."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


DEFAULT_KEY_COLUMNS = ["model", "id", "variant", "prompt_mode"]


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_rows(paths: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"model", "id", "variant", "correct"}.issubset(row):
                    continue
                row.setdefault("prompt_mode", "baseline")
                if rescore:
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
                row["_source"] = str(path)
                row["_line"] = line_no
                rows.append(row)
    return rows


def index_rows(
    rows: list[dict[str, Any]], key_columns: list[str]
) -> dict[tuple[Any, ...], dict[str, Any]]:
    indexed: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(row.get(column, "") for column in key_columns)
        indexed[key] = row
    return indexed


def change_label(before: bool, after: bool) -> str:
    if before and after:
        return "same_correct"
    if not before and not after:
        return "same_wrong"
    if not before and after:
        return "gain"
    return "loss"


def parse_filter(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid filter {value!r}; expected column=value")
        key, raw = value.split("=", 1)
        parsed[key] = raw
    return parsed


def matches(row: dict[str, Any], filters: dict[str, str]) -> bool:
    return all(str(row.get(key, "")) == value for key, value in filters.items())


def compare(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
    key_columns: list[str],
) -> list[dict[str, Any]]:
    before = index_rows(before_rows, key_columns)
    after = index_rows(after_rows, key_columns)
    rows: list[dict[str, Any]] = []
    for key in sorted(set(before) & set(after)):
        left = before[key]
        right = after[key]
        left_correct = bool(left.get("correct"))
        right_correct = bool(right.get("correct"))
        out = {column: value for column, value in zip(key_columns, key)}
        out.update(
            {
                "dataset": right.get("dataset", left.get("dataset", "")),
                "task_type": right.get("task_type", left.get("task_type", "")),
                "answer_type": right.get("answer_type", left.get("answer_type", "")),
                "gold": right.get("gold", left.get("gold", "")),
                "before_correct": left_correct,
                "after_correct": right_correct,
                "change": change_label(left_correct, right_correct),
                "before_parsed": left.get("parsed", ""),
                "after_parsed": right.get("parsed", ""),
                "before_seconds": left.get("seconds", ""),
                "after_seconds": right.get("seconds", ""),
                "before_source": left.get("_source", ""),
                "after_source": right.get("_source", ""),
            }
        )
        if right.get("rewrite_output"):
            out["after_rewrite_output"] = right.get("rewrite_output", "")
        rows.append(out)
    return rows


def summarize(rows: list[dict[str, Any]], group_by: list[str]) -> list[dict[str, Any]]:
    counts: Counter[tuple[Any, ...]] = Counter()
    for row in rows:
        key = tuple(row.get(column, "") for column in group_by + ["change"])
        counts[key] += 1

    summary_rows: list[dict[str, Any]] = []
    for key, n in sorted(counts.items()):
        values = dict(zip(group_by + ["change"], key))
        values["n"] = n
        summary_rows.append(values)
    return summary_rows


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
    parser.add_argument("--before", type=Path, nargs="+", required=True)
    parser.add_argument("--after", type=Path, nargs="+", required=True)
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--key-columns", nargs="+", default=DEFAULT_KEY_COLUMNS)
    parser.add_argument("--before-filter", nargs="*", default=[])
    parser.add_argument("--after-filter", nargs="*", default=[])
    parser.add_argument(
        "--summary-group-by",
        nargs="+",
        default=["model", "dataset", "variant", "prompt_mode"],
    )
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    before_rows = load_rows(jsonl_paths(args.before), args.rescore)
    after_rows = load_rows(jsonl_paths(args.after), args.rescore)
    before_filter = parse_filter(args.before_filter)
    after_filter = parse_filter(args.after_filter)
    if before_filter:
        before_rows = [row for row in before_rows if matches(row, before_filter)]
    if after_filter:
        after_rows = [row for row in after_rows if matches(row, after_filter)]
    rows = compare(before_rows, after_rows, args.key_columns)
    if not rows:
        raise SystemExit("No overlapping rows found.")
    summary_rows = summarize(rows, args.summary_group_by)
    write_csv(args.items_output, rows)
    write_csv(args.summary_output, summary_rows)
    print(f"Wrote {args.items_output}")
    print(f"Wrote {args.summary_output}")
    for row in summary_rows:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))


if __name__ == "__main__":
    main()
