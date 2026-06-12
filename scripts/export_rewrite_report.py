#!/usr/bin/env python3
"""Export a Markdown report for self-normalization rewrite outputs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                items[row["id"]] = row
    return items


def load_eval_rows(paths: list[Path], rescore: bool) -> dict[str, dict[str, Any]]:
    from run_eval_kaggle import is_correct, parse_answer

    rows: dict[str, dict[str, Any]] = {}
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("rewrite_output"):
                    if rescore and row.get("raw_output"):
                        row["parsed"] = parse_answer(
                            str(row.get("raw_output", "")),
                            str(row.get("answer_type", "")),
                        )
                        row["correct"] = is_correct(
                            str(row.get("parsed", "")),
                            str(row.get("gold", "")),
                            str(row.get("answer_type", "")),
                        )
                    rows[row["id"]] = row
    return rows


def load_compare(path: Path | None, changes: set[str]) -> list[dict[str, str]]:
    if path is None:
        return []
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if not changes or row.get("change") in changes:
                rows.append(row)
    return rows


def block(label: str, text: str) -> str:
    return f"**{label}**\n\n```text\n{text.strip()}\n```\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--eval", type=Path, nargs="+", required=True)
    parser.add_argument("--compare", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--changes", nargs="*", default=["gain", "loss", "same_wrong"])
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_items(args.items)
    eval_rows = load_eval_rows(args.eval, args.rescore)
    compare_rows = load_compare(args.compare, set(args.changes))

    if compare_rows:
        selected_ids = [row["id"] for row in compare_rows if row["id"] in eval_rows]
    else:
        selected_ids = sorted(eval_rows)
    selected_ids = selected_ids[: args.limit]

    lines = [
        "# Self-Normalization Rewrite Report",
        "",
        f"Items: `{args.items}`",
        f"Eval rows: `{', '.join(str(path) for path in args.eval)}`",
        f"Examples exported: {len(selected_ids)}",
        "",
    ]
    if args.compare:
        lines.extend([f"Compare file: `{args.compare}`", ""])

    compare_by_id = {row["id"]: row for row in compare_rows}
    for idx, item_id in enumerate(selected_ids, start=1):
        item = items[item_id]
        row = eval_rows[item_id]
        comp = compare_by_id.get(item_id, {})
        lines.extend(
            [
                f"## {idx}. {item_id} ({row.get('dataset', '')})",
                "",
                f"Gold: `{row.get('gold', '')}`",
                f"Self-normalized parsed: `{row.get('parsed', '')}`; correct: `{row.get('correct', '')}`",
                "",
            ]
        )
        if comp:
            lines.extend(
                [
                    f"Baseline parsed: `{comp.get('before_parsed', '')}`; baseline correct: `{comp.get('before_correct', '')}`",
                    f"Change: `{comp.get('change', '')}`",
                    "",
                ]
            )
        lines.extend(
            [
                block("Banglish Input", item.get("banglish_clean", "")),
                block("Model Rewrite", row.get("rewrite_output", "")),
                block("Final Raw Output", row.get("raw_output", "")),
                "",
            ]
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
