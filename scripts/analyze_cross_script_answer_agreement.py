#!/usr/bin/env python3
"""Analyze parsed-answer agreement across Bangla, Banglish, and English runs."""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from run_eval_kaggle import compact_answer, is_correct, parse_answer


VARIANTS = ["bangla", "banglish_clean", "english"]


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
    for path in jsonl_paths(paths):
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"id", "model", "variant", "correct"}.issubset(row):
                    continue
                if row.get("variant") not in VARIANTS:
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


def norm_answer(parsed: Any, answer_type: str) -> str:
    value = str(parsed or "").strip()
    if not value:
        return ""
    if answer_type == "choice":
        return value.upper()
    return compact_answer(value)


def agreement_bucket(norms: dict[str, str]) -> str:
    bangla = norms["bangla"]
    banglish = norms["banglish_clean"]
    english = norms["english"]
    if not bangla or not banglish or not english:
        return "has_empty"
    if bangla == banglish == english:
        return "all_three_same"
    if bangla == banglish and banglish != english:
        return "banglish_matches_bangla"
    if english == banglish and banglish != bangla:
        return "banglish_matches_english"
    if bangla == english and banglish != bangla:
        return "bangla_english_agree_banglish_differs"
    return "all_three_different"


def majority_answer(norms: dict[str, str]) -> tuple[str, str]:
    counts = Counter(value for value in norms.values() if value)
    if not counts:
        return "", "all_empty"
    answer, count = counts.most_common(1)[0]
    if count >= 2:
        return answer, "pair_or_three_agreement"
    return norms["banglish_clean"], "fallback_banglish"


def bangla_english_route(norms: dict[str, str]) -> tuple[str, str]:
    bangla = norms["bangla"]
    english = norms["english"]
    if bangla and bangla == english:
        return bangla, "bangla_english_agree"
    return norms["banglish_clean"], "fallback_banglish"


def correctness_for_norm(answer: str, gold: str, answer_type: str) -> bool:
    if answer_type == "choice":
        return answer.upper() == str(gold).strip().upper()
    return is_correct(answer, gold, answer_type)


def build_item_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        key = (str(row["model"]), str(row["prompt_mode"]), str(row["id"]))
        grouped[key][str(row["variant"])] = row

    out: list[dict[str, Any]] = []
    for (model, prompt_mode, item_id), by_variant in sorted(grouped.items()):
        if not all(variant in by_variant for variant in VARIANTS):
            continue
        sample = by_variant["banglish_clean"]
        answer_type = str(sample.get("answer_type", ""))
        gold = str(sample.get("gold", ""))
        parsed = {variant: str(by_variant[variant].get("parsed", "")) for variant in VARIANTS}
        norms = {variant: norm_answer(parsed[variant], answer_type) for variant in VARIANTS}
        correct = {variant: bool(by_variant[variant].get("correct")) for variant in VARIANTS}

        majority_norm, majority_source = majority_answer(norms)
        be_norm, be_source = bangla_english_route(norms)
        majority_correct = correctness_for_norm(majority_norm, gold, answer_type)
        be_correct = correctness_for_norm(be_norm, gold, answer_type)
        oracle_correct = any(correct.values())
        bucket = agreement_bucket(norms)

        out.append(
            {
                "model": model,
                "prompt_mode": prompt_mode,
                "id": item_id,
                "dataset": sample.get("dataset", ""),
                "task_type": sample.get("task_type", ""),
                "answer_type": answer_type,
                "gold": gold,
                "agreement_bucket": bucket,
                "bangla_correct": correct["bangla"],
                "banglish_correct": correct["banglish_clean"],
                "english_correct": correct["english"],
                "bangla_parsed": parsed["bangla"],
                "banglish_parsed": parsed["banglish_clean"],
                "english_parsed": parsed["english"],
                "bangla_norm": norms["bangla"],
                "banglish_norm": norms["banglish_clean"],
                "english_norm": norms["english"],
                "majority_source": majority_source,
                "majority_correct": majority_correct,
                "bangla_english_route_source": be_source,
                "bangla_english_route_correct": be_correct,
                "oracle_correct": oracle_correct,
                "banglish_wrong_other_correct": (
                    (not correct["banglish_clean"]) and (correct["bangla"] or correct["english"])
                ),
            }
        )
    return out


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    pos = (len(values) - 1) * q
    low = int(pos)
    high = min(low + 1, len(values) - 1)
    frac = pos - low
    return values[low] * (1 - frac) + values[high] * frac


def bootstrap_delta(
    pairs: list[tuple[bool, bool]], samples: int, seed: int
) -> tuple[float, float, float, float]:
    rng = random.Random(seed)
    n = len(pairs)
    deltas: list[float] = []
    for _ in range(samples):
        left = right = 0
        for _ in range(n):
            before, after = pairs[rng.randrange(n)]
            left += int(before)
            right += int(after)
        deltas.append((right / n) - (left / n))
    observed = (sum(int(after) for _, after in pairs) / n) - (
        sum(int(before) for before, _ in pairs) / n
    )
    if observed >= 0:
        p_opposite = sum(1 for value in deltas if value <= 0) / samples
    else:
        p_opposite = sum(1 for value in deltas if value >= 0) / samples
    return observed, percentile(deltas, 0.025), percentile(deltas, 0.975), p_opposite


def summarize(
    item_rows: list[dict[str, Any]], samples: int, seed: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    overall: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in item_rows:
        groups[
            (
                str(row["model"]),
                str(row["prompt_mode"]),
                str(row["dataset"]),
                str(row["agreement_bucket"]),
            )
        ].append(row)
        groups[
            (
                str(row["model"]),
                str(row["prompt_mode"]),
                "all",
                str(row["agreement_bucket"]),
            )
        ].append(row)
        overall[(str(row["model"]), str(row["prompt_mode"]), str(row["dataset"]))].append(row)
        overall[(str(row["model"]), str(row["prompt_mode"]), "all")].append(row)

    bucket_rows: list[dict[str, Any]] = []
    for (model, prompt_mode, dataset, bucket), rows in sorted(groups.items()):
        n = len(rows)
        bucket_rows.append(
            {
                "model": model,
                "prompt_mode": prompt_mode,
                "dataset": dataset,
                "agreement_bucket": bucket,
                "n": n,
                "banglish_correct": sum(row["banglish_correct"] for row in rows),
                "banglish_accuracy": round(sum(row["banglish_correct"] for row in rows) / n, 4),
                "majority_correct": sum(row["majority_correct"] for row in rows),
                "majority_accuracy": round(sum(row["majority_correct"] for row in rows) / n, 4),
                "bangla_english_route_correct": sum(
                    row["bangla_english_route_correct"] for row in rows
                ),
                "bangla_english_route_accuracy": round(
                    sum(row["bangla_english_route_correct"] for row in rows) / n, 4
                ),
                "oracle_correct": sum(row["oracle_correct"] for row in rows),
                "oracle_accuracy": round(sum(row["oracle_correct"] for row in rows) / n, 4),
                "banglish_wrong_other_correct": sum(
                    row["banglish_wrong_other_correct"] for row in rows
                ),
            }
        )

    route_rows: list[dict[str, Any]] = []
    for (model, prompt_mode, dataset), rows in sorted(overall.items()):
        n = len(rows)
        comparisons = [
            ("majority_vote", "majority_correct"),
            ("bangla_english_agreement_route", "bangla_english_route_correct"),
            ("oracle", "oracle_correct"),
        ]
        for label, key in comparisons:
            observed, low, high, p_opposite = bootstrap_delta(
                [(bool(row["banglish_correct"]), bool(row[key])) for row in rows],
                samples=samples,
                seed=seed,
            )
            route_rows.append(
                {
                    "model": model,
                    "prompt_mode": prompt_mode,
                    "dataset": dataset,
                    "route": label,
                    "n": n,
                    "banglish_correct": sum(row["banglish_correct"] for row in rows),
                    "route_correct": sum(row[key] for row in rows),
                    "delta_route_minus_banglish": observed,
                    "ci95_low": low,
                    "ci95_high": high,
                    "bootstrap_p_opposite_direction": p_opposite,
                }
            )
    return bucket_rows, route_rows


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
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--bucket-output", type=Path, required=True)
    parser.add_argument("--route-output", type=Path, required=True)
    parser.add_argument("--rescore", action="store_true")
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.inputs, rescore=args.rescore)
    item_rows = build_item_rows(rows)
    bucket_rows, route_rows = summarize(item_rows, args.bootstrap_samples, args.seed)
    write_csv(args.items_output, item_rows)
    write_csv(args.bucket_output, bucket_rows)
    write_csv(args.route_output, route_rows)
    print(f"Wrote {args.items_output}")
    print(f"Wrote {args.bucket_output}")
    print(f"Wrote {args.route_output}")
    for row in route_rows:
        if row["dataset"] == "all":
            print(
                f"{row['model']} | {row['route']} | "
                f"{row['banglish_correct']}/{row['n']} -> {row['route_correct']}/{row['n']} "
                f"delta={row['delta_route_minus_banglish']:.4f}"
            )


if __name__ == "__main__":
    main()
