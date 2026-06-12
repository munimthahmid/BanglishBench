#!/usr/bin/env python3
"""Paired bootstrap confidence intervals for two evaluation conditions."""

from __future__ import annotations

import argparse
import csv
import json
import random
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


def load_rows(paths: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"id", "variant", "model", "correct"}.issubset(row):
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


def index_rows(
    rows: list[dict[str, Any]],
    filters: dict[str, str],
    key_columns: list[str],
) -> dict[tuple[Any, ...], dict[str, Any]]:
    indexed: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        if not matches(row, filters):
            continue
        key = tuple(row.get(column, "") for column in key_columns)
        indexed[key] = row
    return indexed


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    pos = (len(values) - 1) * q
    low = int(pos)
    high = min(low + 1, len(values) - 1)
    frac = pos - low
    return values[low] * (1 - frac) + values[high] * frac


def bootstrap_delta(
    pairs: list[tuple[bool, bool]],
    samples: int,
    seed: int,
) -> tuple[float, float, float, float]:
    rng = random.Random(seed)
    n = len(pairs)
    deltas: list[float] = []
    for _ in range(samples):
        left = right = 0
        for _ in range(n):
            left_correct, right_correct = pairs[rng.randrange(n)]
            left += int(left_correct)
            right += int(right_correct)
        deltas.append((right / n) - (left / n))

    observed = (
        sum(int(right) for _, right in pairs) / n
        - sum(int(left) for left, _ in pairs) / n
    )
    lower = percentile(deltas, 0.025)
    upper = percentile(deltas, 0.975)
    if observed >= 0:
        p_direction = sum(1 for delta in deltas if delta <= 0) / len(deltas)
    else:
        p_direction = sum(1 for delta in deltas if delta >= 0) / len(deltas)
    return observed, lower, upper, p_direction


def write_csv(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument(
        "--right-inputs",
        type=Path,
        nargs="+",
        help="Optional separate inputs for the right condition. When set, positional inputs are used only for the left condition.",
    )
    parser.add_argument("--left-filter", nargs="+", required=True)
    parser.add_argument("--right-filter", nargs="+", required=True)
    parser.add_argument("--key-columns", nargs="+", default=["id"])
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    left_source_rows = load_rows(jsonl_paths(args.inputs), args.rescore)
    right_source_rows = (
        load_rows(jsonl_paths(args.right_inputs), args.rescore)
        if args.right_inputs
        else left_source_rows
    )
    left_filter = parse_filter(args.left_filter)
    right_filter = parse_filter(args.right_filter)
    left_rows = index_rows(left_source_rows, left_filter, args.key_columns)
    right_rows = index_rows(right_source_rows, right_filter, args.key_columns)
    keys = sorted(set(left_rows) & set(right_rows))
    if not keys:
        raise SystemExit("No overlapping paired rows found.")

    pairs = [
        (bool(left_rows[key].get("correct")), bool(right_rows[key].get("correct")))
        for key in keys
    ]
    observed, lower, upper, p_direction = bootstrap_delta(
        pairs, args.samples, args.seed
    )
    left_correct = sum(int(left) for left, _ in pairs)
    right_correct = sum(int(right) for _, right in pairs)
    row = {
        "label": args.label,
        "n": len(pairs),
        "left_correct": left_correct,
        "right_correct": right_correct,
        "left_accuracy": round(left_correct / len(pairs), 4),
        "right_accuracy": round(right_correct / len(pairs), 4),
        "delta_right_minus_left": round(observed, 4),
        "ci95_low": round(lower, 4),
        "ci95_high": round(upper, 4),
        "bootstrap_p_opposite_direction": round(p_direction, 4),
        "left_filter": ";".join(f"{k}={v}" for k, v in left_filter.items()),
        "right_filter": ";".join(f"{k}={v}" for k, v in right_filter.items()),
        "key_columns": ";".join(args.key_columns),
        "samples": args.samples,
        "seed": args.seed,
    }
    write_csv(args.output, row)
    for key, value in row.items():
        print(f"{key}: {value}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
