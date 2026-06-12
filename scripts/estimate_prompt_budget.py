#!/usr/bin/env python3
"""Estimate prompt sizes for evaluation slices without calling a model API."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import load_jsonl, make_prompt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_OUTPUT = ROOT / "results/analysis/validation200_v5_prompt_budget_summary.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_prompt_budget.md"


def approx_tokens(text: str) -> int:
    # Common API-budget rule of thumb. Real tokenizers differ by provider.
    return math.ceil(len(text) / 4)


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


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(path)


def summarize(prompts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    grouped["overall"] = prompts
    for row in prompts:
        grouped[f"variant={row['variant']}"].append(row)
        grouped[f"dataset={row['dataset']}"].append(row)
        grouped[f"dataset={row['dataset']};variant={row['variant']}"].append(row)

    rows: list[dict[str, Any]] = []
    for group, items in grouped.items():
        chars = [int(item["chars"]) for item in items]
        toks = [int(item["approx_tokens"]) for item in items]
        rows.append(
            {
                "group": group,
                "calls": len(items),
                "total_chars": sum(chars),
                "mean_chars": round(sum(chars) / len(chars), 1),
                "max_chars": max(chars),
                "total_approx_tokens": sum(toks),
                "mean_approx_tokens": round(sum(toks) / len(toks), 1),
                "max_approx_tokens": max(toks),
            }
        )
    rows.sort(key=lambda row: (row["group"] != "overall", row["group"]))
    return rows


def write_report(path: Path, input_path: Path, output_path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Prompt Budget Estimate",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Input slice: `{repo_path(input_path)}`",
        f"- Summary CSV: `{repo_path(output_path)}`",
        "",
        "Approximate tokens use `ceil(characters / 4)`. This is a budget heuristic,",
        "not provider-specific tokenization.",
        "",
        "## Summary",
        "",
        "| Group | Calls | Total approx tokens | Mean | Max |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['group']}` | {row['calls']} | {row['total_approx_tokens']} | {row['mean_approx_tokens']} | {row['max_approx_tokens']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--variants", nargs="+", default=["bangla", "banglish_clean", "english"]
    )
    parser.add_argument("--prompt-mode", default="baseline")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_jsonl(args.input)
    if args.limit:
        items = items[: args.limit]
    prompts: list[dict[str, Any]] = []
    for item in items:
        for variant in args.variants:
            prompt = make_prompt(item, variant, args.prompt_mode)
            prompts.append(
                {
                    "id": item["id"],
                    "dataset": item.get("dataset", ""),
                    "variant": variant,
                    "chars": len(prompt),
                    "approx_tokens": approx_tokens(prompt),
                }
            )
    rows = summarize(prompts)
    write_csv(args.output, rows)
    write_report(args.report, args.input, args.output, rows)
    overall = rows[0]
    print(f"calls={overall['calls']}")
    print(f"total_approx_tokens={overall['total_approx_tokens']}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
