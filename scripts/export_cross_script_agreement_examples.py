#!/usr/bin/env python3
"""Export qualitative examples for cross-script answer agreement analysis."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                out[str(row["id"])] = row
    return out


def truthy(value: str) -> bool:
    return value.strip().lower() == "true"


def clip(text: Any, limit: int = 420) -> str:
    value = " ".join(str(text or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def model_label(model: str) -> str:
    labels = {
        "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
        "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
        "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
    }
    return labels.get(model, model)


def write_example(
    lines: list[str],
    row: dict[str, str],
    item: dict[str, Any],
    idx: int,
) -> None:
    lines.append(f"### Example {idx}: {model_label(row['model'])} / {row['id']}")
    lines.append("")
    lines.append(f"- Dataset: `{row['dataset']}`")
    lines.append(f"- Gold: `{row['gold']}`")
    lines.append(f"- Agreement bucket: `{row['agreement_bucket']}`")
    lines.append(f"- Bangla parsed: `{row['bangla_parsed']}`; correct: `{row['bangla_correct']}`")
    lines.append(
        f"- Banglish parsed: `{row['banglish_parsed']}`; correct: `{row['banglish_correct']}`"
    )
    lines.append(f"- English parsed: `{row['english_parsed']}`; correct: `{row['english_correct']}`")
    lines.append("")
    lines.append("Banglish prompt snippet:")
    lines.append("")
    lines.append("```text")
    lines.append(clip(item.get("banglish_clean", "")))
    lines.append("```")
    lines.append("")
    lines.append("English prompt snippet:")
    lines.append("")
    lines.append("```text")
    lines.append(clip(item.get("english", "")))
    lines.append("```")
    lines.append("")


def select_examples(rows: list[dict[str, str]], model: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    model_rows = [row for row in rows if row["model"] == model]
    agreement_gains = [
        row
        for row in model_rows
        if row["agreement_bucket"] == "bangla_english_agree_banglish_differs"
        and not truthy(row["banglish_correct"])
        and truthy(row["bangla_english_route_correct"])
    ]
    hard_recoverable = [
        row
        for row in model_rows
        if row["agreement_bucket"] == "all_three_different"
        and not truthy(row["banglish_correct"])
        and truthy(row["oracle_correct"])
    ]
    return agreement_gains[:2], hard_recoverable[:1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--items",
        type=Path,
        default=ROOT / "data/slices/validation_200_v5.jsonl",
    )
    parser.add_argument(
        "--agreement-items",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_cross_script_answer_agreement_items.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/cross_script_answer_agreement_examples.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_items(args.items)
    rows = load_csv(args.agreement_items)
    models = [
        "Qwen/Qwen2.5-3B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen3-4B-Instruct-2507",
    ]

    lines = [
        "# Cross-Script Answer Agreement Examples",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "These examples support `reports/cross_script_diagnostics_validation200_v5.md`.",
        "Prompt snippets and Banglish outputs use frozen reviewed validation-200 v5.",
        "Bangla and English outputs are reused because those fields did not change.",
        "",
    ]
    idx = 1
    for model in models:
        agreement_gains, hard_recoverable = select_examples(rows, model)
        lines.append(f"## {model_label(model)}")
        lines.append("")
        lines.append("### Bangla+English Agreement Recovers Banglish Failure")
        lines.append("")
        for row in agreement_gains:
            write_example(lines, row, items.get(row["id"], {}), idx)
            idx += 1
        lines.append("### Recoverable But All Three Answers Differ")
        lines.append("")
        for row in hard_recoverable:
            write_example(lines, row, items.get(row["id"], {}), idx)
            idx += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
