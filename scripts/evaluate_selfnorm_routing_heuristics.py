#!/usr/bin/env python3
"""Evaluate simple baseline-vs-selfnorm routing heuristics."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any, Callable


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def float_value(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0


def index_quality(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["id"]: row for row in rows}


def route_rows(
    compare_rows: list[dict[str, str]],
    quality_rows: dict[str, dict[str, str]],
    name: str,
    predicate: Callable[[dict[str, str], dict[str, str]], bool],
) -> dict[str, Any]:
    n = 0
    correct = 0
    used_after = 0
    for row in compare_rows:
        quality = quality_rows.get(row["id"], {})
        use_after = predicate(row, quality)
        used_after += int(use_after)
        correct += int(truthy(row["after_correct"] if use_after else row["before_correct"]))
        n += 1
    return {
        "heuristic": name,
        "n": n,
        "correct": correct,
        "accuracy": round(correct / n, 4) if n else 0.0,
        "used_selfnorm": used_after,
        "used_selfnorm_rate": round(used_after / n, 4) if n else 0.0,
    }


def heuristics() -> list[tuple[str, Callable[[dict[str, str], dict[str, str]], bool]]]:
    return [
        ("always_baseline", lambda row, q: False),
        ("always_selfnorm", lambda row, q: True),
        (
            "selfnorm_if_options_preserved",
            lambda row, q: truthy(q.get("options_preserved", "true")),
        ),
        (
            "selfnorm_if_digits_formulas_preserved",
            lambda row, q: truthy(q.get("digit_count_preserved", "false"))
            and truthy(q.get("formulas_preserved", "false")),
        ),
        (
            "selfnorm_if_all_structure_preserved",
            lambda row, q: truthy(q.get("options_preserved", "false"))
            and truthy(q.get("digit_count_preserved", "false"))
            and truthy(q.get("formulas_preserved", "false")),
        ),
        (
            "selfnorm_if_bengali_ratio_ge_0_5",
            lambda row, q: float_value(q.get("bengali_ratio", "0")) >= 0.5,
        ),
        (
            "selfnorm_if_structure_and_bengali_ratio_ge_0_3",
            lambda row, q: truthy(q.get("options_preserved", "false"))
            and truthy(q.get("digit_count_preserved", "false"))
            and truthy(q.get("formulas_preserved", "false"))
            and float_value(q.get("bengali_ratio", "0")) >= 0.3,
        ),
        (
            "selfnorm_if_banglamath",
            lambda row, q: row.get("dataset", "") == "banglamath",
        ),
        (
            "selfnorm_if_benqa",
            lambda row, q: row.get("dataset", "") == "benqa",
        ),
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path, required=True)
    parser.add_argument("--quality", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compare_rows = load_csv(args.compare)
    quality_rows = index_quality(load_csv(args.quality))
    rows = [
        route_rows(compare_rows, quality_rows, name, predicate)
        for name, predicate in heuristics()
    ]
    write_csv(args.output, rows)
    for row in rows:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
