#!/usr/bin/env python3
"""Analyze item-level script-gap patterns from model-output JSONL files."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


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
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"model", "id", "variant", "correct"}.issubset(row):
                    continue
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


def pattern_for(values: dict[str, bool | None]) -> str:
    bn = values.get("bangla")
    bg = values.get("banglish_clean")
    en = values.get("english")
    present = {key for key, value in values.items() if value is not None}

    if present == {"bangla", "banglish_clean"}:
        if bn and bg:
            return "bangla_banglish_both_correct_no_english"
        if bn and not bg:
            return "bangla_correct_banglish_wrong_no_english"
        if bg and not bn:
            return "banglish_correct_bangla_wrong_no_english"
        return "bangla_banglish_both_wrong_no_english"

    if bn and bg and en:
        return "all_correct"
    if not bn and not bg and not en:
        return "all_wrong"
    if en and bn and not bg:
        return "banglish_drop_vs_bangla_english"
    if en and not bn and bg:
        return "bangla_drop_vs_banglish_english"
    if bn and not bg and not en:
        return "bangla_only_correct"
    if bg and not bn and not en:
        return "banglish_only_correct"
    if en and not bn and not bg:
        return "english_only_correct"
    if bn and bg and not en:
        return "english_wrong_only"
    return "mixed_other"


def truncate(text: Any, limit: int) -> str:
    value = str(text or "").replace("\r", " ").replace("\n", " ")
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def analyze(rows: list[dict[str, Any]], raw_limit: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        grouped[(row["model"], row["id"])][row["variant"]] = row

    out: list[dict[str, Any]] = []
    for (model, item_id), by_variant in sorted(grouped.items()):
        values = {
            variant: bool(by_variant[variant]["correct"]) if variant in by_variant else None
            for variant in VARIANTS
        }
        first = next(iter(by_variant.values()))
        row = {
            "model": model,
            "id": item_id,
            "dataset": first.get("dataset", ""),
            "task_type": first.get("task_type", ""),
            "answer_type": first.get("answer_type", ""),
            "gold": first.get("gold", ""),
            "pattern": pattern_for(values),
        }
        for variant in VARIANTS:
            item = by_variant.get(variant)
            row[f"{variant}_present"] = bool(item)
            row[f"{variant}_correct"] = values[variant]
            row[f"{variant}_parsed"] = item.get("parsed", "") if item else ""
            row[f"{variant}_raw"] = truncate(item.get("raw_output", ""), raw_limit) if item else ""
            row[f"{variant}_seconds"] = item.get("seconds", "") if item else ""
        out.append(row)
    return out


def summarize(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counter: Counter[tuple[str, str, str, str]] = Counter()
    for row in item_rows:
        counter[(row["model"], row["dataset"], row["task_type"], row["pattern"])] += 1
    return [
        {
            "model": model,
            "dataset": dataset,
            "task_type": task_type,
            "pattern": pattern,
            "n": n,
        }
        for (model, dataset, task_type, pattern), n in sorted(counter.items())
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--rescore", action="store_true")
    parser.add_argument("--raw-limit", type=int, default=220)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(jsonl_paths(args.inputs), args.rescore)
    if not rows:
        raise SystemExit("No evaluation rows found.")
    item_rows = analyze(rows, args.raw_limit)
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    print(f"Wrote {args.items_output}")
    print(f"Wrote {args.summary_output}")
    for row in summary_rows:
        print(f"{row['model']} | {row['dataset']} | {row['pattern']} | {row['n']}")


if __name__ == "__main__":
    main()
