#!/usr/bin/env python3
"""Compute oracle union accuracy across multiple variants in one eval JSONL."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_rows(inputs: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in jsonl_paths(inputs):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"id", "model", "variant", "correct"}.issubset(row):
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
                rows.append(row)
    return rows


def summarize(rows: list[dict[str, Any]], variants: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row["variant"] not in variants:
            continue
        key = (row["model"], row["prompt_mode"], row["id"])
        grouped[key][row["variant"]] = row

    by_group: dict[tuple[str, str, str], list[dict[str, dict[str, Any]]]] = defaultdict(list)
    for (model, prompt_mode, _item_id), variant_rows in grouped.items():
        if not all(variant in variant_rows for variant in variants):
            continue
        sample = next(iter(variant_rows.values()))
        key = (model, prompt_mode, str(sample.get("dataset", "")))
        by_group[key].append(variant_rows)

    out: list[dict[str, Any]] = []
    for key, items in sorted(by_group.items()):
        row: dict[str, Any] = {
            "model": key[0],
            "prompt_mode": key[1],
            "dataset": key[2],
            "n": len(items),
        }
        for variant in variants:
            row[f"{variant}_correct"] = sum(
                int(bool(item[variant].get("correct"))) for item in items
            )
            row[f"{variant}_accuracy"] = round(row[f"{variant}_correct"] / len(items), 4)
        oracle = sum(
            int(any(bool(item[variant].get("correct")) for variant in variants))
            for item in items
        )
        all_correct = sum(
            int(all(bool(item[variant].get("correct")) for variant in variants))
            for item in items
        )
        row["oracle_correct"] = oracle
        row["oracle_accuracy"] = round(oracle / len(items), 4)
        row["all_variants_correct"] = all_correct
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
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--variants", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.inputs, args.rescore)
    summary = summarize(rows, args.variants)
    write_csv(args.output, summary)
    for row in summary:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
