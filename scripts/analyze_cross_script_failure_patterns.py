#!/usr/bin/env python3
"""Classify item-level correctness patterns across script variants."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


DEFAULT_VARIANTS = ["bangla", "banglish_clean", "english"]


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            items[str(row["id"])] = row
    return items


def load_eval_rows(paths: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in jsonl_paths(paths):
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
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
                row["_source"] = str(path)
                row["_line"] = line_no
                rows.append(row)
    return rows


def pattern_name(correct: dict[str, bool]) -> str:
    bangla = correct.get("bangla", False)
    banglish = correct.get("banglish_clean", False)
    english = correct.get("english", False)

    if bangla and banglish and english:
        return "all_correct"
    if not bangla and not banglish and not english:
        return "all_wrong"
    if bangla and english and not banglish:
        return "bangla_english_correct_banglish_wrong"
    if bangla and banglish and not english:
        return "bangla_banglish_correct_english_wrong"
    if banglish and english and not bangla:
        return "banglish_english_correct_bangla_wrong"
    if bangla:
        return "bangla_only_correct"
    if banglish:
        return "banglish_only_correct"
    if english:
        return "english_only_correct"
    return "other"


def build_item_rows(
    eval_rows: list[dict[str, Any]],
    items: dict[str, dict[str, Any]],
    variants: list[str],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = {}
    for row in eval_rows:
        variant = str(row.get("variant", ""))
        if variant not in variants:
            continue
        key = (str(row.get("model", "")), str(row.get("prompt_mode", "")), str(row.get("id", "")))
        grouped.setdefault(key, {})[variant] = row

    out: list[dict[str, Any]] = []
    for (model, prompt_mode, item_id), by_variant in sorted(grouped.items()):
        if not all(variant in by_variant for variant in variants):
            continue
        sample = by_variant[variants[0]]
        item = items.get(item_id, {})
        metadata = item.get("metadata") or {}
        correct = {variant: bool(by_variant[variant].get("correct")) for variant in variants}
        row: dict[str, Any] = {
            "model": model,
            "prompt_mode": prompt_mode,
            "dataset": sample.get("dataset", item.get("dataset", "")),
            "task_type": sample.get("task_type", item.get("task_type", "")),
            "answer_type": sample.get("answer_type", item.get("answer_type", "")),
            "id": item_id,
            "domain": item.get("domain", ""),
            "subject": metadata.get("subject", ""),
            "grade": metadata.get("grade", ""),
            "gold": sample.get("gold", item.get("answer", "")),
            "pattern": pattern_name(correct),
            "banglish_wrong_other_correct": (
                (not correct.get("banglish_clean", False))
                and (correct.get("bangla", False) or correct.get("english", False))
            ),
            "any_correct": any(correct.values()),
            "all_correct": all(correct.values()),
        }
        for variant in variants:
            source = by_variant[variant]
            row[f"{variant}_correct"] = correct[variant]
            row[f"{variant}_parsed"] = source.get("parsed", "")
        out.append(row)
    return out


def summarize(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: Counter[tuple[str, str, str]] = Counter()
    counts: Counter[tuple[str, str, str, str]] = Counter()
    recoverable: Counter[tuple[str, str, str]] = Counter()

    for row in item_rows:
        base_keys = [
            (
                str(row["model"]),
                str(row["prompt_mode"]),
                str(row["dataset"]),
            ),
            (
                str(row["model"]),
                str(row["prompt_mode"]),
                "all",
            ),
        ]
        for base_key in base_keys:
            totals[base_key] += 1
            counts[base_key + (str(row["pattern"]),)] += 1
            if row["banglish_wrong_other_correct"]:
                recoverable[base_key] += 1

    summary_rows: list[dict[str, Any]] = []
    for key, n in sorted(counts.items()):
        base_key = key[:3]
        total = totals[base_key]
        summary_rows.append(
            {
                "model": key[0],
                "prompt_mode": key[1],
                "dataset": key[2],
                "pattern": key[3],
                "n": n,
                "total": total,
                "share": round(n / total, 4) if total else 0.0,
                "banglish_wrong_other_correct_total": recoverable[base_key],
                "banglish_wrong_other_correct_share": round(recoverable[base_key] / total, 4)
                if total
                else 0.0,
            }
        )
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
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--variants", nargs="+", default=DEFAULT_VARIANTS)
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_items(args.items)
    eval_rows = load_eval_rows(args.inputs, args.rescore)
    item_rows = build_item_rows(eval_rows, items, args.variants)
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    print(f"Wrote {args.items_output}")
    print(f"Wrote {args.summary_output}")
    for row in summary_rows:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))


if __name__ == "__main__":
    main()
