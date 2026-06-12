#!/usr/bin/env python3
"""Summarize routed mitigation item files and export example packets."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


GROUPS = [
    ("overall", []),
    ("by_split", ["split"]),
    ("by_split_dataset", ["split", "dataset"]),
    ("by_split_answer_type", ["split", "answer_type"]),
    ("by_split_used_selfnorm", ["split", "used_selfnorm"]),
    ("by_split_dataset_used_selfnorm", ["split", "dataset", "used_selfnorm"]),
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            items[str(row["id"])] = row
    return items


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def summarize(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for group_name, cols in GROUPS:
        buckets: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            key = tuple(row.get(col, "") for col in cols)
            buckets[key].append(row)
        for key, bucket in sorted(buckets.items()):
            changes = Counter(row.get("change_vs_baseline", "") for row in bucket)
            baseline_correct = sum(truthy(row.get("before_correct", "")) for row in bucket)
            selfnorm_correct = sum(truthy(row.get("after_correct", "")) for row in bucket)
            routed_correct = sum(truthy(row.get("routed_correct", "")) for row in bucket)
            used_selfnorm = sum(truthy(row.get("used_selfnorm", "")) for row in bucket)
            n = len(bucket)
            record: dict[str, Any] = {
                "group": group_name,
                "n": n,
                "baseline_correct": baseline_correct,
                "selfnorm_correct": selfnorm_correct,
                "routed_correct": routed_correct,
                "routed_minus_baseline": routed_correct - baseline_correct,
                "routed_minus_selfnorm": routed_correct - selfnorm_correct,
                "used_selfnorm": used_selfnorm,
                "used_selfnorm_rate": round(used_selfnorm / n, 4) if n else 0.0,
                "gains": changes["gain"],
                "losses": changes["loss"],
                "same_correct": changes["same_correct"],
                "same_wrong": changes["same_wrong"],
            }
            for col, value in zip(cols, key):
                record[col] = value
            out.append(record)
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


def clip(text: str, limit: int = 900) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def write_examples(
    path: Path,
    rows: list[dict[str, str]],
    items: dict[str, dict[str, Any]],
    split: str,
    limit_per_change: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wanted_changes = ["gain", "loss"]
    with path.open("w", encoding="utf-8") as f:
        model = rows[0].get("model", "") if rows else ""
        heuristic = rows[0].get("heuristic", "") if rows else ""
        f.write("# Routed Self-Normalization Examples\n\n")
        f.write(f"- Model: `{model}`\n")
        f.write(f"- Heuristic: `{heuristic}`\n")
        f.write(f"- Split: `{split}`\n\n")
        for change in wanted_changes:
            subset = [
                row
                for row in rows
                if row.get("split") == split and row.get("change_vs_baseline") == change
            ][:limit_per_change]
            heading = {"gain": "Gains", "loss": "Losses"}[change]
            f.write(f"## {heading}\n\n")
            if not subset:
                f.write("No examples.\n\n")
                continue
            for index, row in enumerate(subset, start=1):
                item = items.get(row["id"], {})
                f.write(f"### {index}. {row['id']}\n\n")
                f.write(f"- Dataset: `{row.get('dataset', '')}`\n")
                f.write(f"- Answer type: `{row.get('answer_type', '')}`\n")
                f.write(f"- Gold: `{row.get('gold', '')}`\n")
                f.write(f"- Used selfnorm: `{row.get('used_selfnorm', '')}`\n")
                f.write(f"- Baseline correct: `{row.get('before_correct', '')}`\n")
                f.write(f"- Selfnorm correct: `{row.get('after_correct', '')}`\n")
                f.write(f"- Routed correct: `{row.get('routed_correct', '')}`\n\n")
                f.write("Banglish item:\n\n```text\n")
                f.write(clip(str(item.get("banglish_clean", ""))) + "\n")
                f.write("```\n\n")
                f.write("Baseline parsed:\n\n```text\n")
                f.write(clip(row.get("before_parsed", ""), 500) + "\n")
                f.write("```\n\nSelf-normalized parsed:\n\n```text\n")
                f.write(clip(row.get("after_parsed", ""), 500) + "\n")
                f.write("```\n\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--routed-items", type=Path, required=True)
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--examples-output", type=Path, required=True)
    parser.add_argument("--examples-split", default="test")
    parser.add_argument("--limit-per-change", type=int, default=6)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_csv(args.routed_items)
    items = load_items(args.items)
    write_csv(args.summary_output, summarize(rows))
    write_examples(
        args.examples_output,
        rows,
        items,
        args.examples_split,
        args.limit_per_change,
    )
    print(f"wrote={args.summary_output}")
    print(f"wrote={args.examples_output}")


if __name__ == "__main__":
    main()
