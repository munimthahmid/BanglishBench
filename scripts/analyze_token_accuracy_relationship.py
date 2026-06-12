#!/usr/bin/env python3
"""Join tokenization metrics with evaluation correctness and summarize links."""

from __future__ import annotations

import argparse
import csv
import json
import math
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


def load_eval_rows(inputs: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in jsonl_paths(inputs):
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


def load_token_rows(path: Path, tokenizer: str) -> dict[tuple[str, str], dict[str, str]]:
    rows: dict[tuple[str, str], dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("tokenizer") != tokenizer:
                continue
            rows[(row["id"], row["variant"])] = row
    return rows


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (
            row["model"],
            row["prompt_mode"],
            row["dataset"],
            row["variant"],
            row["tokenizer"],
        )
        groups[key].append(row)

    out: list[dict[str, Any]] = []
    for key, items in sorted(groups.items()):
        correct = [row for row in items if row["correct"]]
        wrong = [row for row in items if not row["correct"]]
        token_values = [float(row["hf_tokens"]) for row in items]
        token_per_word_values = [float(row["hf_tokens_per_word"]) for row in items]
        correctness = [1.0 if row["correct"] else 0.0 for row in items]
        out.append(
            {
                "model": key[0],
                "prompt_mode": key[1],
                "dataset": key[2],
                "variant": key[3],
                "tokenizer": key[4],
                "n": len(items),
                "correct": len(correct),
                "accuracy": round(len(correct) / len(items), 4) if items else 0.0,
                "mean_hf_tokens_correct": round(
                    sum(float(row["hf_tokens"]) for row in correct) / len(correct), 4
                )
                if correct
                else "",
                "mean_hf_tokens_wrong": round(
                    sum(float(row["hf_tokens"]) for row in wrong) / len(wrong), 4
                )
                if wrong
                else "",
                "corr_correct_vs_hf_tokens": round(
                    pearson(correctness, token_values), 4
                ),
                "corr_correct_vs_tokens_per_word": round(
                    pearson(correctness, token_per_word_values), 4
                ),
            }
        )
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
    parser.add_argument("--tokenization-audit", type=Path, required=True)
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--eval", type=Path, nargs="+", required=True)
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token_rows = load_token_rows(args.tokenization_audit, args.tokenizer)
    eval_rows = load_eval_rows(args.eval, args.rescore)

    joined: list[dict[str, Any]] = []
    for row in eval_rows:
        token_row = token_rows.get((str(row["id"]), str(row["variant"])))
        if not token_row:
            continue
        joined.append(
            {
                "model": row["model"],
                "prompt_mode": row["prompt_mode"],
                "dataset": row.get("dataset", ""),
                "task_type": row.get("task_type", ""),
                "variant": row["variant"],
                "id": row["id"],
                "correct": bool(row["correct"]),
                "tokenizer": token_row["tokenizer"],
                "words": token_row["words"],
                "hf_tokens": token_row["hf_tokens"],
                "hf_tokens_per_word": token_row["hf_tokens_per_word"],
                "chars": token_row["chars"],
                "utf8_bytes": token_row["utf8_bytes"],
            }
        )

    write_csv(args.items_output, joined)
    summary = summarize(joined)
    write_csv(args.summary_output, summary)
    for row in summary:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print(f"Wrote {args.items_output}")
    print(f"Wrote {args.summary_output}")


if __name__ == "__main__":
    main()
