#!/usr/bin/env python3
"""Evaluate self-normalization routing heuristics by named item-id slices."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Callable


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_slice_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Slices must use NAME=PATH format.")
    name, path = value.split("=", 1)
    name = name.strip()
    if not name:
        raise argparse.ArgumentTypeError("Slice name cannot be empty.")
    return name, Path(path)


def load_slice_ids(slices: list[tuple[str, Path]]) -> dict[str, set[str]]:
    split_ids: dict[str, set[str]] = {}
    for split, path in slices:
        ids: set[str] = set()
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                item_id = str(row.get("id", "")).strip()
                if not item_id:
                    raise ValueError(f"{path}:{line_no} has no id")
                ids.add(item_id)
        split_ids[split] = ids
    return split_ids


def attach_splits(
    rows: list[dict[str, str]],
    split_ids: dict[str, set[str]],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        item_id = row.get("id", "")
        for split, ids in split_ids.items():
            if item_id in ids:
                tagged = dict(row)
                tagged["split"] = split
                out.append(tagged)
    return out


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def float_value(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0


def index_quality(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["id"]: row for row in rows}


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


def route_rows(
    rows: list[dict[str, str]],
    quality_rows: dict[str, dict[str, str]],
    split: str,
    name: str,
    predicate: Callable[[dict[str, str], dict[str, str]], bool],
) -> dict[str, Any]:
    n = 0
    correct = 0
    used_after = 0
    model = rows[0].get("model", "") if rows else ""
    for row in rows:
        quality = quality_rows.get(row["id"], {})
        use_after = predicate(row, quality)
        used_after += int(use_after)
        correct += int(truthy(row["after_correct"] if use_after else row["before_correct"]))
        n += 1
    return {
        "split": split,
        "model": model,
        "heuristic": name,
        "n": n,
        "correct": correct,
        "accuracy": round(correct / n, 4) if n else 0.0,
        "used_selfnorm": used_after,
        "used_selfnorm_rate": round(used_after / n, 4) if n else 0.0,
    }


def choose_dev_heuristic(
    rows: list[dict[str, Any]],
    selection_split: str,
    evaluation_split: str,
) -> list[dict[str, Any]]:
    dev_rows = [row for row in rows if row["split"] == selection_split]
    if not dev_rows:
        raise ValueError(f"No rows for selection split {selection_split!r}")
    chosen = max(
        dev_rows,
        key=lambda row: (
            int(row["correct"]),
            float(row["accuracy"]),
            -float(row["used_selfnorm_rate"]),
            row["heuristic"],
        ),
    )
    heuristic = chosen["heuristic"]
    eval_rows = [row for row in rows if row["split"] == evaluation_split and row["heuristic"] == heuristic]
    if not eval_rows:
        raise ValueError(f"No evaluation row for heuristic {heuristic!r} on {evaluation_split!r}")
    eval_row = eval_rows[0]
    return [
        {
            "model": chosen["model"],
            "selected_on": selection_split,
            "evaluated_on": evaluation_split,
            "selected_heuristic": heuristic,
            "dev_correct": chosen["correct"],
            "dev_n": chosen["n"],
            "dev_accuracy": chosen["accuracy"],
            "test_correct": eval_row["correct"],
            "test_n": eval_row["n"],
            "test_accuracy": eval_row["accuracy"],
            "test_used_selfnorm": eval_row["used_selfnorm"],
            "test_used_selfnorm_rate": eval_row["used_selfnorm_rate"],
        }
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path, required=True)
    parser.add_argument("--quality", type=Path, required=True)
    parser.add_argument("--slice", dest="slices", action="append", type=parse_slice_arg, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selection-output", type=Path)
    parser.add_argument("--selection-split", default="dev")
    parser.add_argument("--evaluation-split", default="test")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    split_ids = load_slice_ids(args.slices)
    compare_rows = attach_splits(load_csv(args.compare), split_ids)
    if not compare_rows:
        raise SystemExit("No compare rows matched the requested slices.")
    quality_rows = index_quality(load_csv(args.quality))

    rows: list[dict[str, Any]] = []
    for split in split_ids:
        split_rows = [row for row in compare_rows if row["split"] == split]
        for name, predicate in heuristics():
            rows.append(route_rows(split_rows, quality_rows, split, name, predicate))

    write_csv(args.output, rows)
    print(f"wrote={args.output}")
    if args.selection_output:
        selection_rows = choose_dev_heuristic(rows, args.selection_split, args.evaluation_split)
        write_csv(args.selection_output, selection_rows)
        print(f"wrote={args.selection_output}")


if __name__ == "__main__":
    main()
