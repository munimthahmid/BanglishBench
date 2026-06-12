#!/usr/bin/env python3
"""Summarize evaluation outputs after joining item metadata."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_GROUP_BY = ["model", "dataset", "stratum", "variant"]


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            item_id = str(row.get("id", "")).strip()
            if not item_id:
                raise ValueError(f"{path}:{line_no} has no id")
            items[item_id] = row
    return items


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_eval_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if "correct" not in row or "model" not in row or "variant" not in row:
                    continue
                row["_source"] = str(path)
                row["_line"] = line_no
                rows.append(row)
    return rows


def attach_metadata(
    rows: list[dict[str, Any]],
    items: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = items.get(str(row.get("id", "")), {})
        metadata = item.get("metadata") or {}
        dataset = row.get("dataset") or item.get("dataset", "")
        if dataset == "benqa":
            stratum = metadata.get("subject") or item.get("domain") or "unknown"
        elif dataset == "banglamath":
            stratum = metadata.get("grade") or "unknown"
        else:
            stratum = item.get("domain") or "unknown"

        joined = dict(row)
        joined["domain"] = item.get("domain", "")
        joined["subject"] = metadata.get("subject", "")
        joined["grade"] = metadata.get("grade", "")
        joined["stratum"] = str(stratum)
        out.append(joined)
    return out


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
        groups[tuple(row.get(column, "") for column in group_by)].append(row)

    out_rows: list[dict[str, Any]] = []
    for key, items in sorted(groups.items(), key=lambda item: item[0]):
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
            }
        )
        out_rows.append(out)
    return out_rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--group-by", nargs="+", default=DEFAULT_GROUP_BY)
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = attach_metadata(load_eval_rows(jsonl_paths(args.inputs)), load_items(args.items))
    if not rows:
        raise SystemExit("No evaluation rows found.")
    if args.rescore:
        rescore_rows(rows)
    summary_rows = summarize(rows, args.group_by)
    fieldnames = args.group_by + ["n", "unique_items", "correct", "accuracy", "parsed_empty"]
    write_csv(args.output, summary_rows, fieldnames)
    print(f"rows={len(rows)}")
    print(f"summary_rows={len(summary_rows)}")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
