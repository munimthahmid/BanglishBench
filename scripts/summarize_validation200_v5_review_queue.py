#!/usr/bin/env python3
"""Summarize the validation-200 v5 Banglish review queue."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_SUBS_OUTPUT = ROOT / "results/analysis/validation200_v5_review_queue_substitutions.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_review_effort_summary.md"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_suggestions(notes: str) -> list[tuple[str, str, int]]:
    out: list[tuple[str, str, int]] = []
    for part in notes.split(";"):
        part = part.strip()
        if not part or "->" not in part:
            continue
        left, rest = part.split("->", 1)
        right = rest
        count = 1
        if "(" in rest and rest.endswith(")"):
            right, raw_count = rest.rsplit("(", 1)
            raw_count = raw_count.rstrip(")").strip()
            try:
                count = int(raw_count)
            except ValueError:
                count = 1
        out.append((left.strip(), right.strip(), count))
    return out


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    input_path: Path,
    substitutions_path: Path,
    rows: list[dict[str, str]],
    substitution_counts: Counter[tuple[str, str]],
) -> None:
    priority_counts = Counter(row["priority_bucket"] for row in rows)
    dataset_counts = Counter(row["dataset"] for row in rows)
    label_counts = Counter(row.get("quality_label", "").strip() or "blank" for row in rows)
    replacement_count_hist = Counter(row["replacement_count"] for row in rows)

    lines = [
        "# Validation-200 v5 Review Effort Summary",
        "",
        "Updated: 2026-05-28",
        "",
        "## Inputs",
        "",
        f"- Review queue: `{input_path.relative_to(ROOT)}`",
        f"- Substitution CSV: `{substitutions_path.relative_to(ROOT)}`",
        "",
        "## Review Progress",
        "",
        f"- Rows: {len(rows)}",
        f"- Reviewed rows: {len(rows) - label_counts['blank']}",
        f"- Pending rows: {label_counts['blank']}",
        "",
        "## Dataset Counts",
        "",
        "| Dataset | Rows |",
        "| --- | ---: |",
    ]
    for key, value in dataset_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Priority Counts", "", "| Priority bucket | Rows |", "| --- | ---: |"])
    for key, value in priority_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Replacement Count Histogram", "", "| Replacement count | Rows |", "| --- | ---: |"])
    for key, value in sorted(replacement_count_hist.items(), key=lambda item: int(item[0] or 0), reverse=True):
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Top Suggested Substitutions", "", "| Substitution | Occurrences |", "| --- | ---: |"])
    for (src, dst), count in substitution_counts.most_common(25):
        lines.append(f"| `{src}` -> `{dst}` | {count} |")

    lines.extend(
        [
            "",
            "## Review Strategy",
            "",
            "Start with the repeated math-artifact substitutions because they cover",
            "many high-priority rows. Do not bulk-accept them blindly: still compare",
            "Bangla, English, current Banglish, and auto-suggested Banglish for each",
            "row before setting `quality_label`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--substitutions-output", type=Path, default=DEFAULT_SUBS_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    substitutions: Counter[tuple[str, str]] = Counter()
    for row in rows:
        for src, dst, count in parse_suggestions(row.get("suggestion_notes", "")):
            substitutions[(src, dst)] += count
    substitution_rows = [
        {"source": src, "target": dst, "occurrences": count}
        for (src, dst), count in substitutions.most_common()
    ]
    write_csv(args.substitutions_output, substitution_rows)
    write_report(args.report_output, args.input, args.substitutions_output, rows, substitutions)
    print(f"rows={len(rows)}")
    print(f"substitutions={len(substitution_rows)}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
