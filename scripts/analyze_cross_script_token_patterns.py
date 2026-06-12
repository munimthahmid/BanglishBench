#!/usr/bin/env python3
"""Join cross-script failure taxonomy with tokenization metrics."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


VARIANTS = ["bangla", "banglish_clean", "english"]


def read_csv(path: Path) -> list[dict[str, str]]:
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


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def fnum(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def build_token_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    out: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        tokenizer = row.get("tokenizer", "")
        if tokenizer == "unicode_baseline":
            continue
        out[(tokenizer, row["id"], row["variant"])] = row
    return out


def mean(rows: list[dict[str, Any]], key: str) -> float:
    values = [float(row[key]) for row in rows if row.get(key) not in {"", None}]
    return round(sum(values) / len(values), 4) if values else 0.0


def join_rows(
    taxonomy_rows: list[dict[str, str]],
    token_rows: dict[tuple[str, str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in taxonomy_rows:
        model = row["model"]
        item_id = row["id"]
        tokens = {
            variant: token_rows.get((model, item_id, variant), {})
            for variant in VARIANTS
        }
        if any(not tokens[variant] for variant in VARIANTS):
            continue
        bangla_tokens = fnum(tokens["bangla"]["hf_tokens"])
        banglish_tokens = fnum(tokens["banglish_clean"]["hf_tokens"])
        english_tokens = fnum(tokens["english"]["hf_tokens"])
        out.append(
            {
                "model": model,
                "dataset": row["dataset"],
                "task_type": row["task_type"],
                "id": item_id,
                "pattern": row["pattern"],
                "banglish_wrong_other_correct": truthy(
                    row.get("banglish_wrong_other_correct", "")
                ),
                "bangla_correct": truthy(row.get("bangla_correct", "")),
                "banglish_clean_correct": truthy(row.get("banglish_clean_correct", "")),
                "english_correct": truthy(row.get("english_correct", "")),
                "bangla_tokens": bangla_tokens,
                "banglish_tokens": banglish_tokens,
                "english_tokens": english_tokens,
                "banglish_minus_bangla_tokens": banglish_tokens - bangla_tokens,
                "banglish_minus_english_tokens": banglish_tokens - english_tokens,
                "banglish_over_bangla_tokens": round(
                    banglish_tokens / bangla_tokens, 4
                )
                if bangla_tokens
                else 0.0,
                "banglish_over_english_tokens": round(
                    banglish_tokens / english_tokens, 4
                )
                if english_tokens
                else 0.0,
                "bangla_tokens_per_word": fnum(tokens["bangla"]["hf_tokens_per_word"]),
                "banglish_tokens_per_word": fnum(
                    tokens["banglish_clean"]["hf_tokens_per_word"]
                ),
                "english_tokens_per_word": fnum(tokens["english"]["hf_tokens_per_word"]),
            }
        )
    return out


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    group_specs = [
        ("by_model_dataset_pattern", ["model", "dataset", "pattern"]),
        (
            "by_model_dataset_banglish_wrong_other_correct",
            ["model", "dataset", "banglish_wrong_other_correct"],
        ),
        ("by_model_pattern", ["model", "pattern"]),
        ("by_model_banglish_wrong_other_correct", ["model", "banglish_wrong_other_correct"]),
    ]
    out: list[dict[str, Any]] = []
    for group_name, cols in group_specs:
        buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            buckets[tuple(row[col] for col in cols)].append(row)
        for key, items in sorted(buckets.items()):
            record: dict[str, Any] = {
                "group": group_name,
                "n": len(items),
                "mean_bangla_tokens": mean(items, "bangla_tokens"),
                "mean_banglish_tokens": mean(items, "banglish_tokens"),
                "mean_english_tokens": mean(items, "english_tokens"),
                "mean_banglish_minus_bangla_tokens": mean(
                    items, "banglish_minus_bangla_tokens"
                ),
                "mean_banglish_over_bangla_tokens": mean(
                    items, "banglish_over_bangla_tokens"
                ),
                "mean_bangla_tokens_per_word": mean(items, "bangla_tokens_per_word"),
                "mean_banglish_tokens_per_word": mean(
                    items, "banglish_tokens_per_word"
                ),
                "mean_english_tokens_per_word": mean(
                    items, "english_tokens_per_word"
                ),
            }
            for col, value in zip(cols, key):
                record[col] = value
            out.append(record)
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--taxonomy", type=Path, required=True)
    parser.add_argument("--tokenization-audit", type=Path, required=True)
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token_rows = build_token_index(read_csv(args.tokenization_audit))
    joined = join_rows(read_csv(args.taxonomy), token_rows)
    write_csv(args.items_output, joined)
    write_csv(args.summary_output, summarize(joined))
    print(f"joined={len(joined)}")
    print(f"wrote={args.items_output}")
    print(f"wrote={args.summary_output}")


if __name__ == "__main__":
    main()
