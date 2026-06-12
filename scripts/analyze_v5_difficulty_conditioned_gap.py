#!/usr/bin/env python3
"""Difficulty-conditioned frozen-v5 consensus gaps."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_item_consensus_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_difficulty_conditioned_gap_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_difficulty_conditioned_gap_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_difficulty_conditioned_gap.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
DATASETS = ("all", "benqa", "banglamath")
BUCKETS = (0, 1, 2, 3)
AXES = (
    ("english_consensus", "english_model_correct_count", "English-consensus bucket"),
    ("bangla_consensus", "bangla_model_correct_count", "Bangla-consensus bucket"),
    (
        "alternate_best_consensus",
        "alternate_best_correct_count",
        "Best alternate-script consensus bucket",
    ),
)
BOOTSTRAP_ITERATIONS = 5000
BOOTSTRAP_SEED = 20260531


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def to_int(row: dict[str, Any], key: str) -> int:
    return int(str(row.get(key, "0")).strip() or 0)


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def percent(count: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * count / denominator:.1f}%"


def points(value: float) -> str:
    pct = value * 100
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.1f}"


def stable_seed(label: str) -> int:
    return BOOTSTRAP_SEED + sum((index + 1) * ord(char) for index, char in enumerate(label))


def bootstrap_delta(
    rows: list[dict[str, Any]],
    candidate_key: str,
    baseline_key: str,
    denominator: int,
    seed_label: str,
) -> tuple[float, float, float]:
    if not rows or denominator == 0:
        return 0.0, 0.0, 0.0
    observed = sum(to_int(row, candidate_key) - to_int(row, baseline_key) for row in rows) / denominator
    rng = random.Random(stable_seed(seed_label))
    draws: list[float] = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        total = 0
        for _i in range(len(rows)):
            row = rng.choice(rows)
            total += to_int(row, candidate_key) - to_int(row, baseline_key)
        draws.append(total / denominator)
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    return observed, low, high


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    item_rows: list[dict[str, Any]] = []
    for row in rows:
        item_rows.append(
            {
                "id": row["id"],
                "dataset": row["dataset"],
                "domain": row.get("domain", ""),
                "subject": row.get("subject", ""),
                "grade": row.get("grade", ""),
                "task_type": row.get("task_type", ""),
                "review_label": row.get("review_label", ""),
                "english_consensus_bucket": to_int(row, "english_model_correct_count"),
                "bangla_consensus_bucket": to_int(row, "bangla_model_correct_count"),
                "alternate_best_consensus_bucket": to_int(
                    row, "alternate_best_correct_count"
                ),
                "bangla_model_correct_count": to_int(row, "bangla_model_correct_count"),
                "banglish_model_correct_count": to_int(row, "banglish_model_correct_count"),
                "english_model_correct_count": to_int(row, "english_model_correct_count"),
                "alternate_best_correct_count": to_int(row, "alternate_best_correct_count"),
                "banglish_minus_bangla_model_count": to_int(
                    row, "banglish_minus_bangla_model_count"
                ),
                "banglish_minus_english_model_count": to_int(
                    row, "banglish_minus_english_model_count"
                ),
                "strong_alternate_low_banglish": truthy(
                    row.get("strong_alternate_low_banglish", "")
                ),
                "zero_banglish_any_alternate": truthy(
                    row.get("zero_banglish_any_alternate", "")
                ),
                "banglish_preview": row.get("banglish_preview", ""),
            }
        )
    return item_rows


def rows_for_dataset(rows: list[dict[str, Any]], dataset: str) -> list[dict[str, Any]]:
    if dataset == "all":
        return rows
    return [row for row in rows if row["dataset"] == dataset]


def summarize_bucket(
    rows: list[dict[str, Any]],
    axis: str,
    axis_label: str,
    dataset: str,
    bucket: int,
) -> dict[str, Any]:
    denominator = len(rows) * len(MODELS)
    bangla = sum(to_int(row, "bangla_model_correct_count") for row in rows)
    banglish = sum(to_int(row, "banglish_model_correct_count") for row in rows)
    english = sum(to_int(row, "english_model_correct_count") for row in rows)
    delta_bangla = bootstrap_delta(
        rows,
        "banglish_model_correct_count",
        "bangla_model_correct_count",
        denominator,
        f"{axis}:{dataset}:{bucket}:bangla",
    )
    delta_english = bootstrap_delta(
        rows,
        "banglish_model_correct_count",
        "english_model_correct_count",
        denominator,
        f"{axis}:{dataset}:{bucket}:english",
    )
    return {
        "axis": axis,
        "axis_label": axis_label,
        "dataset": dataset,
        "bucket": bucket,
        "n_items": len(rows),
        "model_item_slots": denominator,
        "bangla_correct": bangla,
        "banglish_correct": banglish,
        "english_correct": english,
        "bangla_accuracy": rate(bangla, denominator),
        "banglish_accuracy": rate(banglish, denominator),
        "english_accuracy": rate(english, denominator),
        "banglish_minus_bangla": round(delta_bangla[0], 4),
        "banglish_minus_bangla_ci95_low": round(delta_bangla[1], 4),
        "banglish_minus_bangla_ci95_high": round(delta_bangla[2], 4),
        "banglish_minus_english": round(delta_english[0], 4),
        "banglish_minus_english_ci95_low": round(delta_english[1], 4),
        "banglish_minus_english_ci95_high": round(delta_english[2], 4),
        "strong_alternate_low_banglish_items": sum(
            truthy(row["strong_alternate_low_banglish"]) for row in rows
        ),
        "zero_banglish_any_alternate_items": sum(
            truthy(row["zero_banglish_any_alternate"]) for row in rows
        ),
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for axis, source_column, axis_label in AXES:
        bucket_column = f"{axis}_bucket"
        if axis == "alternate_best_consensus":
            bucket_column = "alternate_best_consensus_bucket"
        for dataset in DATASETS:
            dataset_rows = rows_for_dataset(item_rows, dataset)
            for bucket in BUCKETS:
                rows = [row for row in dataset_rows if to_int(row, source_column) == bucket]
                if not rows:
                    rows = [row for row in dataset_rows if to_int(row, bucket_column) == bucket]
                summary.append(summarize_bucket(rows, axis, axis_label, dataset, bucket))
    return summary


def summary_row(
    summary_rows: list[dict[str, Any]],
    axis: str,
    dataset: str,
    bucket: int,
) -> dict[str, Any]:
    return next(
        row
        for row in summary_rows
        if row["axis"] == axis and row["dataset"] == dataset and row["bucket"] == bucket
    )


def delta_cell(row: dict[str, Any], key: str) -> str:
    low = row[f"{key}_ci95_low"]
    high = row[f"{key}_ci95_high"]
    return f"{points(float(row[key]))} pts, CI [{points(float(low))},{points(float(high))}]"


def success_cell(row: dict[str, Any], key: str) -> str:
    return f"{row[key]}/{row['model_item_slots']} ({percent(int(row[key]), int(row['model_item_slots']))})"


def add_axis_table(
    lines: list[str],
    summary_rows: list[dict[str, Any]],
    axis: str,
    dataset: str,
    title: str,
) -> None:
    lines.extend(
        [
            f"### {title}",
            "",
            "| Bucket | Items | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for bucket in BUCKETS:
        row = summary_row(summary_rows, axis, dataset, bucket)
        lines.append(
            "| "
            f"{bucket} | {row['n_items']} | {success_cell(row, 'bangla_correct')} | "
            f"{success_cell(row, 'banglish_correct')} | {success_cell(row, 'english_correct')} | "
            f"{delta_cell(row, 'banglish_minus_bangla')} |"
        )
    lines.append("")


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
    source_input: Path,
) -> None:
    english_high = summary_row(summary_rows, "english_consensus", "all", 3)
    english_high_benqa = summary_row(summary_rows, "english_consensus", "benqa", 3)
    english_mid = summary_row(summary_rows, "english_consensus", "all", 2)
    alternate_high = summary_row(summary_rows, "alternate_best_consensus", "all", 3)

    lines = [
        "# V5 Difficulty-Conditioned Script Gap",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This no-spend audit asks whether the reviewed-Banglish deficit is",
        "concentrated only in globally hard items. It reuses the frozen-v5",
        "three-model item-consensus table and buckets each item by how many Qwen",
        "rows answer the same item correctly in English, native Bangla, or the",
        "best non-Banglish alternate script.",
        "",
        "## Inputs And Outputs",
        "",
        f"- Input item consensus: `{repo_path(source_input)}`",
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        "- The Banglish deficit grows, rather than disappears, on items with",
        "  stronger alternate-script consensus.",
        f"- In the all-200 English-consensus=3 bucket, reviewed Banglish has "
        f"{english_high['banglish_correct']}/{english_high['model_item_slots']} "
        f"correct model-item slots versus Bangla "
        f"{english_high['bangla_correct']}/{english_high['model_item_slots']} "
        f"({delta_cell(english_high, 'banglish_minus_bangla')}).",
        f"- In the all-200 English-consensus=2 bucket, reviewed Banglish has "
        f"{english_mid['banglish_correct']}/{english_mid['model_item_slots']} "
        f"versus Bangla {english_mid['bangla_correct']}/{english_mid['model_item_slots']} "
        f"({delta_cell(english_mid, 'banglish_minus_bangla')}).",
        f"- On BEnQA items with English consensus=3, reviewed Banglish has "
        f"{english_high_benqa['banglish_correct']}/{english_high_benqa['model_item_slots']} "
        f"versus Bangla {english_high_benqa['bangla_correct']}/"
        f"{english_high_benqa['model_item_slots']} "
        f"({delta_cell(english_high_benqa, 'banglish_minus_bangla')}).",
        f"- In the all-200 best-alternate-consensus=3 bucket, reviewed Banglish has "
        f"{alternate_high['banglish_correct']}/{alternate_high['model_item_slots']} "
        f"versus Bangla {alternate_high['bangla_correct']}/"
        f"{alternate_high['model_item_slots']} "
        f"({delta_cell(alternate_high, 'banglish_minus_bangla')}).",
        "",
        "## English-Consensus Buckets",
        "",
        "The bucket value is the number of thesis-facing Qwen rows that answer the",
        "English version correctly. This avoids using Banglish itself to define",
        "the difficulty bucket.",
        "",
    ]
    add_axis_table(lines, summary_rows, "english_consensus", "all", "All 200 Items")
    add_axis_table(lines, summary_rows, "english_consensus", "benqa", "BEnQA Only")

    lines.extend(
        [
            "## Best Alternate-Script Buckets",
            "",
            "Here the bucket is the larger of the native-Bangla and English model",
            "correct counts. This is a headroom view: it asks how Banglish behaves",
            "when at least one trusted non-Banglish script shows that the item is",
            "answerable for the same Qwen family.",
            "",
        ]
    )
    add_axis_table(lines, summary_rows, "alternate_best_consensus", "all", "All 200 Items")

    lines.extend(
        [
            "## Interpretation",
            "",
            "- The near-zero low-consensus buckets are not good evidence for or against",
            "  a script gap because they contain many all-script-hard rows.",
            "- The stronger diagnostic rows are the high-consensus buckets. There, the",
            "  same item is answerable by multiple Qwen rows in English or native",
            "  Bangla, yet reviewed Banglish loses many of those model-item successes.",
            "- This supports the thesis wording that the Banglish weakness is not just",
            "  ordinary item difficulty or a different mix of easy and hard questions.",
            "- This remains Qwen-family behavioral evidence. It is not an independent",
            "  model-family replication and does not prove an internal mechanism.",
            "",
            "## Reproducibility",
            "",
            f"- Builder: `scripts/analyze_v5_difficulty_conditioned_gap.py`",
            f"- Input rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "- Bootstrap: item-cluster resampling within each bucket, 5,000 samples.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = read_csv(args.input)
    item_rows = build_item_rows(source_rows)
    summary_rows = build_summary_rows(item_rows)

    item_fields = [
        "id",
        "dataset",
        "domain",
        "subject",
        "grade",
        "task_type",
        "review_label",
        "english_consensus_bucket",
        "bangla_consensus_bucket",
        "alternate_best_consensus_bucket",
        "bangla_model_correct_count",
        "banglish_model_correct_count",
        "english_model_correct_count",
        "alternate_best_correct_count",
        "banglish_minus_bangla_model_count",
        "banglish_minus_english_model_count",
        "strong_alternate_low_banglish",
        "zero_banglish_any_alternate",
        "banglish_preview",
    ]
    summary_fields = [
        "axis",
        "axis_label",
        "dataset",
        "bucket",
        "n_items",
        "model_item_slots",
        "bangla_correct",
        "banglish_correct",
        "english_correct",
        "bangla_accuracy",
        "banglish_accuracy",
        "english_accuracy",
        "banglish_minus_bangla",
        "banglish_minus_bangla_ci95_low",
        "banglish_minus_bangla_ci95_high",
        "banglish_minus_english",
        "banglish_minus_english_ci95_low",
        "banglish_minus_english_ci95_high",
        "strong_alternate_low_banglish_items",
        "zero_banglish_any_alternate_items",
    ]
    write_csv(args.items_output, item_rows, item_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(
        args.report_output,
        item_rows,
        summary_rows,
        args.items_output,
        args.summary_output,
        args.input,
    )
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
