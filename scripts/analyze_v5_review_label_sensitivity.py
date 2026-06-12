#!/usr/bin/env python3
"""Summarize frozen-v5 script gaps by Banglish review label."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_FAILURES = (
    ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
)
DEFAULT_SUMMARY = ROOT / "results/analysis/v5_review_label_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_review_label_sensitivity.md"

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
LABEL_ORDER = ("unreviewed", "minor_edit", "major_edit", "bad")
BUCKETS: tuple[tuple[str, Callable[[str], bool], str], ...] = (
    ("all", lambda label: True, "all 200 frozen-v5 items"),
    ("unreviewed", lambda label: label == "unreviewed", "not selected for v5 review"),
    (
        "reviewed_nonbad",
        lambda label: label in {"minor_edit", "major_edit"},
        "reviewed rows excluding the three bad rows",
    ),
    (
        "reviewed_all",
        lambda label: label in {"minor_edit", "major_edit", "bad"},
        "all rows selected for v5 review",
    ),
    ("strict197_nonbad", lambda label: label != "bad", "all rows except bad"),
)
STRICT_PATTERN = "bangla_english_correct_banglish_wrong"


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


def percent_points(delta_correct: int, n: int) -> float:
    return round(100 * delta_correct / n, 1) if n else 0.0


def points(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def load_item_labels(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            review = item.get("banglish_review", {}) or {}
            label = str(review.get("label") or "unreviewed")
            out[str(item["id"])] = {
                "review_label": label,
                "dataset": str(item.get("dataset", "")),
                "quality_status": str(item.get("quality_status", "")),
            }
    return out


def add_counts_row(
    rows: list[dict[str, Any]],
    section: str,
    key: str,
    n: int,
    detail: str = "",
    model: str = "",
    dataset: str = "",
) -> None:
    rows.append(
        {
            "section": section,
            "key": key,
            "model": model,
            "dataset": dataset,
            "n": n,
            "bangla_correct": "",
            "banglish_correct": "",
            "english_correct": "",
            "banglish_minus_bangla_correct": "",
            "banglish_minus_bangla_points": "",
            "banglish_wrong_other_correct": "",
            "strict_bangla_english_correct_banglish_wrong": "",
            "all_wrong": "",
            "all_correct": "",
            "detail": detail,
        }
    )


def summarize_rows(
    rows: list[dict[str, str]],
    labels: dict[str, dict[str, str]],
    section: str,
    key: str,
    model: str,
    predicate: Callable[[str], bool],
    detail: str = "",
) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["model"] == model and predicate(labels[row["id"]]["review_label"])
    ]
    n = len(selected)
    bangla = sum(truthy(row["bangla_correct"]) for row in selected)
    banglish = sum(truthy(row["banglish_clean_correct"]) for row in selected)
    english = sum(truthy(row["english_correct"]) for row in selected)
    delta = banglish - bangla
    return {
        "section": section,
        "key": key,
        "model": MODEL_LABELS.get(model, model),
        "dataset": "",
        "n": n,
        "bangla_correct": bangla,
        "banglish_correct": banglish,
        "english_correct": english,
        "banglish_minus_bangla_correct": delta,
        "banglish_minus_bangla_points": percent_points(delta, n),
        "banglish_wrong_other_correct": sum(
            truthy(row["banglish_wrong_other_correct"]) for row in selected
        ),
        "strict_bangla_english_correct_banglish_wrong": sum(
            row["pattern"] == STRICT_PATTERN for row in selected
        ),
        "all_wrong": sum(row["pattern"] == "all_wrong" for row in selected),
        "all_correct": sum(row["pattern"] == "all_correct" for row in selected),
        "detail": detail,
    }


def build_summary(
    failure_rows: list[dict[str, str]], labels: dict[str, dict[str, str]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    label_counts = Counter(value["review_label"] for value in labels.values())
    for label in LABEL_ORDER:
        add_counts_row(rows, "item_review_label_count", label, label_counts[label])

    dataset_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for value in labels.values():
        dataset_counts[value["dataset"]][value["review_label"]] += 1
    for dataset in sorted(dataset_counts):
        for label in LABEL_ORDER:
            add_counts_row(
                rows,
                "dataset_review_label_count",
                label,
                dataset_counts[dataset][label],
                dataset=dataset,
            )

    for model in MODELS:
        for bucket, predicate, detail in BUCKETS:
            rows.append(summarize_rows(failure_rows, labels, "analysis_bucket", bucket, model, predicate, detail))
        for label in LABEL_ORDER:
            rows.append(
                summarize_rows(
                    failure_rows,
                    labels,
                    "review_label",
                    label,
                    model,
                    lambda value, label=label: value == label,
                    f"review_label={label}",
                )
            )
    return rows


def by_section(rows: list[dict[str, Any]], section: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["section"] == section]


def write_report(path: Path, rows: list[dict[str, Any]], summary_path: Path, items: Path, failures: Path) -> None:
    label_counts = by_section(rows, "item_review_label_count")
    dataset_counts = by_section(rows, "dataset_review_label_count")
    buckets = by_section(rows, "analysis_bucket")
    fine_labels = by_section(rows, "review_label")
    lines = [
        "# Frozen-V5 Review-Label Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend check asks whether the final Banglish deficit is confined",
        "to rows that needed v5 Banglish edits. It joins the frozen-v5 item review",
        "labels with the frozen-v5 cross-script failure taxonomy.",
        "",
        f"- Machine-readable summary: `{repo_path(summary_path)}`",
        f"- Item source: `{repo_path(items)}`",
        f"- Failure-pattern source: `{repo_path(failures)}`",
        "",
        "## Review-Label Counts",
        "",
        "| Review label | Items |",
        "| --- | ---: |",
    ]
    for label in LABEL_ORDER:
        row = next(row for row in label_counts if row["key"] == label)
        lines.append(f"| `{label}` | {row['n']} |")

    lines.extend(
        [
            "",
            "By dataset:",
            "",
            "| Dataset | Unreviewed | Minor edit | Major edit | Bad |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    by_dataset: dict[str, dict[str, int]] = defaultdict(dict)
    for row in dataset_counts:
        by_dataset[row["dataset"]][row["key"]] = int(row["n"])
    for dataset, counts in sorted(by_dataset.items()):
        lines.append(
            f"| `{dataset}` | {counts.get('unreviewed', 0)} | "
            f"{counts.get('minor_edit', 0)} | {counts.get('major_edit', 0)} | "
            f"{counts.get('bad', 0)} |"
        )

    lines.extend(
        [
            "",
            "## Main Buckets",
            "",
            "| Model | Bucket | n | Bangla | Reviewed Banglish | English | Banglish - Bangla | Recoverable misses | Strict misses |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in (MODEL_LABELS[value] for value in MODELS):
        for bucket, _predicate, _detail in BUCKETS:
            row = next(row for row in buckets if row["model"] == model and row["key"] == bucket)
            lines.append(
                f"| {model} | `{bucket}` | {row['n']} | {row['bangla_correct']} | "
                f"{row['banglish_correct']} | {row['english_correct']} | "
                f"{points(float(row['banglish_minus_bangla_points']))} pts | "
                f"{row['banglish_wrong_other_correct']} | "
                f"{row['strict_bangla_english_correct_banglish_wrong']} |"
            )

    lines.extend(
        [
            "",
            "## Fine Review Labels",
            "",
            "| Model | Review label | n | Bangla | Reviewed Banglish | English | Banglish - Bangla | Recoverable misses | Strict misses |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in (MODEL_LABELS[value] for value in MODELS):
        for label in LABEL_ORDER:
            row = next(row for row in fine_labels if row["model"] == model and row["key"] == label)
            lines.append(
                f"| {model} | `{label}` | {row['n']} | {row['bangla_correct']} | "
                f"{row['banglish_correct']} | {row['english_correct']} | "
                f"{points(float(row['banglish_minus_bangla_points']))} pts | "
                f"{row['banglish_wrong_other_correct']} | "
                f"{row['strict_bangla_english_correct_banglish_wrong']} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The reviewed-v5 Banglish deficit is not confined to edited rows.",
            "  Unreviewed rows and reviewed non-bad rows both show Banglish below",
            "  native Bangla for all three thesis-facing Qwen rows.",
            "- The three `bad` rows are too few to interpret and are not driving the",
            "  release-facing result; the separate strict-197 sensitivity remains the",
            "  denominator check for excluding them.",
            "- `major_edit` rows are only 11 items, so their per-label accuracies are",
            "  descriptive audit evidence rather than a stable performance stratum.",
            "",
            "Thesis-safe phrasing:",
            "",
            "> The human-review process improves benchmark quality, but the measured",
            "> Banglish deficit is visible in both unreviewed and reviewed non-bad",
            "> v5 buckets. The gap is therefore not solely an artifact of the rows",
            "> that required manual Banglish edits.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    labels = load_item_labels(args.items)
    failure_rows = read_csv(args.failure_items)
    if len(labels) != 200:
        raise SystemExit(f"Expected 200 frozen-v5 items, got {len(labels)}")
    if len(failure_rows) != 600:
        raise SystemExit(f"Expected 600 model-item failure rows, got {len(failure_rows)}")
    missing = sorted({row["id"] for row in failure_rows} - set(labels))
    if missing:
        raise SystemExit(f"Failure rows reference missing item ids: {missing[:5]}")
    summary_rows = build_summary(failure_rows, labels)
    fieldnames = [
        "section",
        "key",
        "model",
        "dataset",
        "n",
        "bangla_correct",
        "banglish_correct",
        "english_correct",
        "banglish_minus_bangla_correct",
        "banglish_minus_bangla_points",
        "banglish_wrong_other_correct",
        "strict_bangla_english_correct_banglish_wrong",
        "all_wrong",
        "all_correct",
        "detail",
    ]
    write_csv(args.summary_output, summary_rows, fieldnames)
    write_report(args.report_output, summary_rows, args.summary_output, args.items, args.failure_items)

    bucket_rows = [row for row in summary_rows if row["section"] == "analysis_bucket"]
    strict197 = [row for row in bucket_rows if row["key"] == "strict197_nonbad"]
    if len(summary_rows) != 39:
        raise SystemExit(f"Expected 39 summary rows, got {len(summary_rows)}")
    print(f"summary_rows={len(summary_rows)}")
    for row in strict197:
        print(
            f"{row['model']} strict197_gap={points(float(row['banglish_minus_bangla_points']))} "
            f"bangla={row['bangla_correct']}/{row['n']} "
            f"banglish={row['banglish_correct']}/{row['n']}"
        )
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
