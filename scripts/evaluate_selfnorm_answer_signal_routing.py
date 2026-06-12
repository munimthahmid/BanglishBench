#!/usr/bin/env python3
"""Evaluate answer-signal routing candidates for self-normalization outputs."""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
from pathlib import Path
from typing import Any, Callable


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows for {path}")
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


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    pos = (len(values) - 1) * q
    low = int(pos)
    high = min(low + 1, len(values) - 1)
    frac = pos - low
    return values[low] * (1 - frac) + values[high] * frac


def parse_slice_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Slice must use NAME=PATH format.")
    name, raw_path = value.split("=", 1)
    if not name:
        raise argparse.ArgumentTypeError("Slice name cannot be empty.")
    return name, Path(raw_path)


def load_slice_ids(slices: list[tuple[str, Path]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for name, path in slices:
        ids: set[str] = set()
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    ids.add(str(json.loads(line)["id"]))
        out[name] = ids
    return out


def attach_splits(
    rows: list[dict[str, str]], split_ids: dict[str, set[str]]
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


def parsed(row: dict[str, str], side: str) -> str:
    return row.get(f"{side}_parsed", "").strip()


def has_digits(text: str) -> bool:
    return bool(re.search(r"[0-9\u09e6-\u09ef]", text))


def before_meta(row: dict[str, str]) -> bool:
    return bool(
        re.search(
            r"appears|cannot|unclear|not clear|fragment|translates|evaluation",
            parsed(row, "before"),
            flags=re.IGNORECASE,
        )
    )


def heuristics() -> list[tuple[str, Callable[[dict[str, str]], bool], str]]:
    return [
        ("always_baseline", lambda row: False, "control"),
        ("always_selfnorm", lambda row: True, "control"),
        (
            "selfnorm_if_after_nonempty",
            lambda row: bool(parsed(row, "after")),
            "answer_signal",
        ),
        (
            "selfnorm_if_before_empty_after_nonempty",
            lambda row: not parsed(row, "before") and bool(parsed(row, "after")),
            "answer_signal",
        ),
        (
            "selfnorm_if_after_short_le10",
            lambda row: 0 < len(parsed(row, "after")) <= 10,
            "answer_signal",
        ),
        (
            "selfnorm_if_after_short_le20",
            lambda row: 0 < len(parsed(row, "after")) <= 20,
            "answer_signal",
        ),
        (
            "selfnorm_if_parsed_disagree",
            lambda row: parsed(row, "before") != parsed(row, "after"),
            "answer_signal",
        ),
        (
            "selfnorm_if_before_long_gt40",
            lambda row: len(parsed(row, "before")) > 40,
            "answer_signal",
        ),
        (
            "selfnorm_if_before_meta",
            before_meta,
            "answer_signal",
        ),
        (
            "selfnorm_if_banglamath",
            lambda row: row.get("dataset") == "banglamath",
            "task",
        ),
        (
            "selfnorm_if_math_after_nonempty",
            lambda row: row.get("dataset") == "banglamath" and bool(parsed(row, "after")),
            "answer_signal_task",
        ),
        (
            "selfnorm_if_choice_after_nonempty",
            lambda row: row.get("answer_type") == "choice" and bool(parsed(row, "after")),
            "answer_signal_task",
        ),
        (
            "selfnorm_if_short_answer_after_has_digit",
            lambda row: row.get("answer_type") == "short_answer"
            and has_digits(parsed(row, "after")),
            "answer_signal_task",
        ),
    ]


def heuristic_map() -> dict[str, tuple[Callable[[dict[str, str]], bool], str]]:
    return {name: (predicate, family) for name, predicate, family in heuristics()}


def route(
    rows: list[dict[str, str]],
    split: str,
    name: str,
    family: str,
    predicate: Callable[[dict[str, str]], bool],
) -> dict[str, Any]:
    n = 0
    correct = 0
    used = 0
    model = rows[0].get("model", "") if rows else ""
    for row in rows:
        use_after = predicate(row)
        used += int(use_after)
        correct += int(truthy(row["after_correct"] if use_after else row["before_correct"]))
        n += 1
    return {
        "split": split,
        "model": model,
        "heuristic": name,
        "family": family,
        "n": n,
        "correct": correct,
        "accuracy": round(correct / n, 4) if n else 0.0,
        "used_selfnorm": used,
        "used_selfnorm_rate": round(used / n, 4) if n else 0.0,
    }


def routed_item_rows(
    rows: list[dict[str, str]],
    selected_heuristic: str,
    predicate: Callable[[dict[str, str]], bool],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        use_after = predicate(row)
        before_correct = truthy(row.get("before_correct", ""))
        after_correct = truthy(row.get("after_correct", ""))
        routed_correct = after_correct if use_after else before_correct
        if not before_correct and routed_correct:
            change = "gain"
        elif before_correct and not routed_correct:
            change = "loss"
        elif routed_correct:
            change = "same_correct"
        else:
            change = "same_wrong"
        out.append(
            {
                "split": row.get("split", ""),
                "model": row.get("model", ""),
                "id": row.get("id", ""),
                "dataset": row.get("dataset", ""),
                "task_type": row.get("task_type", ""),
                "answer_type": row.get("answer_type", ""),
                "gold": row.get("gold", ""),
                "heuristic": selected_heuristic,
                "used_selfnorm": use_after,
                "before_correct": before_correct,
                "after_correct": after_correct,
                "routed_correct": routed_correct,
                "change_vs_baseline": change,
                "before_parsed": row.get("before_parsed", ""),
                "after_parsed": row.get("after_parsed", ""),
                "routed_parsed": row.get("after_parsed" if use_after else "before_parsed", ""),
            }
        )
    return out


def bootstrap_pairs(
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
        p_opposite = sum(1 for delta in deltas if delta <= 0) / len(deltas)
    else:
        p_opposite = sum(1 for delta in deltas if delta >= 0) / len(deltas)
    return observed, lower, upper, p_opposite


def bootstrap_rows(
    items: list[dict[str, Any]],
    selected_heuristic: str,
    samples: int,
    seed: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    comparisons = [
        ("baseline_vs_routed", "before_correct", "routed_correct"),
        ("selfnorm_vs_routed", "after_correct", "routed_correct"),
    ]
    for split in sorted({str(row["split"]) for row in items}):
        split_rows = [row for row in items if row["split"] == split]
        for comparison, left_col, right_col in comparisons:
            pairs = [
                (bool(row[left_col]), bool(row[right_col]))
                for row in split_rows
            ]
            observed, lower, upper, p_opposite = bootstrap_pairs(
                pairs, samples=samples, seed=seed
            )
            left_correct = sum(int(left) for left, _ in pairs)
            right_correct = sum(int(right) for _, right in pairs)
            out.append(
                {
                    "split": split,
                    "comparison": comparison,
                    "heuristic": selected_heuristic,
                    "n": len(pairs),
                    "left_correct": left_correct,
                    "right_correct": right_correct,
                    "left_accuracy": round(left_correct / len(pairs), 4),
                    "right_accuracy": round(right_correct / len(pairs), 4),
                    "delta_right_minus_left": round(observed, 4),
                    "ci95_low": round(lower, 4),
                    "ci95_high": round(upper, 4),
                    "bootstrap_p_opposite_direction": round(p_opposite, 4),
                    "samples": samples,
                    "seed": seed,
                }
            )
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path, required=True)
    parser.add_argument("--slice", dest="slices", action="append", type=parse_slice_arg, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selected-heuristic", default="")
    parser.add_argument("--items-output", type=Path)
    parser.add_argument("--bootstrap-output", type=Path)
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--bootstrap-seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    split_ids = load_slice_ids(args.slices)
    rows = attach_splits(load_csv(args.compare), split_ids)
    if not rows:
        raise SystemExit("No rows matched the requested slices.")

    out: list[dict[str, Any]] = []
    for split in split_ids:
        split_rows = [row for row in rows if row["split"] == split]
        for name, predicate, family in heuristics():
            out.append(route(split_rows, split, name, family, predicate))
    write_csv(args.output, out)
    print(f"wrote={args.output}")
    if args.items_output or args.bootstrap_output:
        if not args.selected_heuristic:
            raise SystemExit("--selected-heuristic is required for item/bootstrap outputs.")
        heuristics_by_name = heuristic_map()
        if args.selected_heuristic not in heuristics_by_name:
            raise SystemExit(f"Unknown heuristic: {args.selected_heuristic}")
        predicate, _family = heuristics_by_name[args.selected_heuristic]
        items = routed_item_rows(rows, args.selected_heuristic, predicate)
        if args.items_output:
            write_csv(args.items_output, items)
            print(f"wrote={args.items_output}")
        if args.bootstrap_output:
            boot_rows = bootstrap_rows(
                items,
                args.selected_heuristic,
                samples=args.bootstrap_samples,
                seed=args.bootstrap_seed,
            )
            write_csv(args.bootstrap_output, boot_rows)
            print(f"wrote={args.bootstrap_output}")


if __name__ == "__main__":
    main()
