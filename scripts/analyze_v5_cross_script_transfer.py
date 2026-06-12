#!/usr/bin/env python3
"""Conditional cross-script transfer rates for frozen-v5 Qwen rows."""

from __future__ import annotations

import argparse
import csv
import math
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAILURES = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_cross_script_transfer_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_cross_script_transfer_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_cross_script_transfer.md"

MODELS = (
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen3-4B-Instruct-2507",
)
MODEL_LABELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}
DATASETS = ("all", "benqa", "banglamath")
CONDITIONS = (
    ("bangla_correct", "Bangla correct", lambda row: row["bangla_correct"]),
    ("english_correct", "English correct", lambda row: row["english_correct"]),
    (
        "bangla_or_english_correct",
        "Bangla or English correct",
        lambda row: row["bangla_correct"] or row["english_correct"],
    ),
    (
        "bangla_and_english_correct",
        "Bangla and English correct",
        lambda row: row["bangla_correct"] and row["english_correct"],
    ),
)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def points(value: float) -> str:
    return f"{100 * value:.1f}"


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    spread = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - spread), min(1.0, center + spread)


def normalize_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        bangla = truthy(row["bangla_correct"])
        banglish = truthy(row["banglish_clean_correct"])
        english = truthy(row["english_correct"])
        out.append(
            {
                "model": MODEL_LABELS[row["model"]],
                "model_id": row["model"],
                "dataset": row["dataset"],
                "task_type": row["task_type"],
                "answer_type": row["answer_type"],
                "id": row["id"],
                "domain": row["domain"],
                "subject": row["subject"],
                "grade": row["grade"],
                "gold": row["gold"],
                "pattern": row["pattern"],
                "bangla_correct": bangla,
                "reviewed_banglish_correct": banglish,
                "english_correct": english,
                "bangla_correct_banglish_wrong": bangla and not banglish,
                "english_correct_banglish_wrong": english and not banglish,
                "alternate_correct_banglish_wrong": (bangla or english) and not banglish,
                "both_alternates_correct_banglish_wrong": bangla and english and not banglish,
                "all_three_correct": bangla and banglish and english,
                "all_three_wrong": (not bangla) and (not banglish) and (not english),
            }
        )
    return out


def build_summary_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODEL_LABELS.values():
        model_items = [row for row in items if row["model"] == model]
        for dataset in DATASETS:
            selected = [
                row for row in model_items if dataset == "all" or row["dataset"] == dataset
            ]
            for condition, condition_label, selector in CONDITIONS:
                anchor_rows = [row for row in selected if selector(row)]
                n = len(anchor_rows)
                retained = sum(row["reviewed_banglish_correct"] for row in anchor_rows)
                lost = n - retained
                low, high = wilson_interval(retained, n)
                out.append(
                    {
                        "model": model,
                        "dataset": dataset,
                        "condition": condition,
                        "condition_label": condition_label,
                        "n": len(selected),
                        "anchor_correct": n,
                        "reviewed_banglish_retained": retained,
                        "reviewed_banglish_lost": lost,
                        "retention_rate": round(retained / n, 4) if n else 0.0,
                        "retention_ci95_low": round(low, 4),
                        "retention_ci95_high": round(high, 4),
                    }
                )
    return out


def find_row(rows: list[dict[str, Any]], model: str, dataset: str, condition: str) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["model"] == model and row["dataset"] == dataset and row["condition"] == condition
    )


def cell(row: dict[str, Any]) -> str:
    return (
        f"{row['reviewed_banglish_retained']}/{row['anchor_correct']} "
        f"({pct(row['retention_rate'])}, "
        f"CI [{pct(row['retention_ci95_low'])}, {pct(row['retention_ci95_high'])}])"
    )


def write_report(
    path: Path,
    items: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    source: Path,
    items_output: Path,
    summary_output: Path,
) -> None:
    lines = [
        "# Frozen-V5 Cross-Script Transfer Retention",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend diagnostic asks a conditional robustness question: when a",
        "model answers an item correctly in Bangla or English, how often does the",
        "same model retain correctness in reviewed Banglish? It complements the",
        "oracle/recoverability tables by reporting retention rates over items the",
        "model has already demonstrated it can solve in another script.",
        "",
        f"- Source failure table: `{repo_path(source)}`",
        f"- Item flags: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "Wilson intervals are reported for conditional proportions. These are",
        "behavioral diagnostics, not causal mechanism estimates.",
        "",
        "## All-200 Transfer Retention",
        "",
        "| Model | If Bangla Correct | If English Correct | If Bangla or English Correct | If Both Correct |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for model in MODEL_LABELS.values():
        lines.append(
            f"| {model} | "
            f"{cell(find_row(summary_rows, model, 'all', 'bangla_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'all', 'english_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'all', 'bangla_or_english_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'all', 'bangla_and_english_correct'))} |"
        )

    lines.extend(
        [
            "",
            "## BEnQA Transfer Retention",
            "",
            "| Model | If Bangla Correct | If English Correct | If Bangla or English Correct | If Both Correct |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODEL_LABELS.values():
        lines.append(
            f"| {model} | "
            f"{cell(find_row(summary_rows, model, 'benqa', 'bangla_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'benqa', 'english_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'benqa', 'bangla_or_english_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'benqa', 'bangla_and_english_correct'))} |"
        )

    lines.extend(
        [
            "",
            "## BanglaMATH Stress-Test Retention",
            "",
            "| Model | If Bangla or English Correct | If Both Correct |",
            "| --- | ---: | ---: |",
        ]
    )
    for model in MODEL_LABELS.values():
        lines.append(
            f"| {model} | "
            f"{cell(find_row(summary_rows, model, 'banglamath', 'bangla_or_english_correct'))} | "
            f"{cell(find_row(summary_rows, model, 'banglamath', 'bangla_and_english_correct'))} |"
        )

    strict_events = sum(row["both_alternates_correct_banglish_wrong"] for row in items)
    alternate_events = sum(row["alternate_correct_banglish_wrong"] for row in items)
    qwen3_both = find_row(summary_rows, "Qwen3-4B", "all", "bangla_and_english_correct")
    qwen25_7b_either = find_row(summary_rows, "Qwen2.5-7B 8-bit", "all", "bangla_or_english_correct")
    qwen25_3b_either = find_row(summary_rows, "Qwen2.5-3B", "all", "bangla_or_english_correct")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Across the 600 model-item slots, {alternate_events} have Bangla or",
            f"  English correct while reviewed Banglish is wrong; {strict_events}",
            "  are the stricter Bangla+English-correct/Banglish-wrong cases.",
            f"- Qwen3-4B retains reviewed-Banglish correctness on only",
            f"  {qwen3_both['reviewed_banglish_retained']}/{qwen3_both['anchor_correct']}",
            "  all-200 items where both Bangla and English are correct.",
            f"- Qwen2.5-7B 8-bit retains Banglish on",
            f"  {qwen25_7b_either['reviewed_banglish_retained']}/{qwen25_7b_either['anchor_correct']}",
            "  items where either Bangla or English is correct; Qwen2.5-3B retains",
            f"  {qwen25_3b_either['reviewed_banglish_retained']}/{qwen25_3b_either['anchor_correct']}.",
            "- BanglaMATH denominators are small because the models rarely solve",
            "  those items in any script; keep that dataset as a stress test.",
            "",
            "Thesis-safe phrasing:",
            "",
            "> The reviewed-Banglish deficit is not just low overall competence:",
            "> even after conditioning on same-model correctness in Bangla or",
            "> English, many items lose correctness in reviewed Banglish.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = read_csv(args.failure_items)
    if len(source_rows) != 600:
        raise SystemExit(f"Expected 600 source rows, got {len(source_rows)}")
    items = normalize_item_rows(source_rows)
    summary_rows = build_summary_rows(items)
    write_csv(args.items_output, items)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        items,
        summary_rows,
        args.failure_items,
        args.items_output,
        args.summary_output,
    )
    print(f"items={len(items)} summary_rows={len(summary_rows)} report={args.report_output}")


if __name__ == "__main__":
    main()
