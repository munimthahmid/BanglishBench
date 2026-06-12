#!/usr/bin/env python3
"""Build a source-aware human review queue for validation-200 v5 Banglish."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLICE = ROOT / "data/slices/validation_200_v4.jsonl"
DEFAULT_AUTO_QUEUE = ROOT / "data/slices/banglish_auto_suggested_review_priority_v1.csv"
DEFAULT_ARTIFACT_QUEUE = ROOT / "data/slices/banglish_human_review_priority_v3_suggestions.csv"
DEFAULT_OUTPUT = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_review_queue.md"


PRIORITY_ORDER = {
    "both_wrong_multi_edit": 0,
    "both_wrong_single_edit": 1,
    "qwen25_wrong_multi_edit": 2,
    "qwen3_wrong_multi_edit": 3,
    "lower_priority": 4,
}


def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                rows[row["id"]] = row
    return rows


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def artifact_lookup(path: Path) -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    if not path.exists():
        return lookup
    for row in load_csv(path):
        if row.get("source_file") == "data/slices/validation_200_v4.jsonl":
            lookup[row["id"]] = row
    return lookup


def sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    return (
        PRIORITY_ORDER.get(row["priority_bucket"], 99),
        -int(row["replacement_count"] or 0),
        row["id"],
    )


def build_rows(
    items: dict[str, dict[str, Any]],
    auto_rows: list[dict[str, str]],
    artifacts: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for auto in sorted(auto_rows, key=sort_key):
        item = items[auto["id"]]
        artifact = artifacts.get(auto["id"], {})
        out.append(
            {
                "id": auto["id"],
                "dataset": auto["dataset"],
                "task_type": str(item.get("task_type", "")),
                "answer_type": str(item.get("answer_type", "")),
                "answer": str(item.get("answer", "")),
                "priority_bucket": auto["priority_bucket"],
                "replacement_count": auto["replacement_count"],
                "artifact_patterns": artifact.get("patterns", ""),
                "suggestion_notes": auto["suggestion_notes"],
                "qwen25_v4_correct": auto["qwen25_v4_correct"],
                "qwen3_v4_correct": auto["qwen3_v4_correct"],
                "qwen25_v3_to_v4_change": auto["qwen25_v3_to_v4_change"],
                "qwen3_v3_to_v4_change": auto["qwen3_v3_to_v4_change"],
                "bangla": str(item.get("bangla", "")),
                "english": str(item.get("english", "")),
                "current_banglish_clean": auto["current_banglish_clean"],
                "auto_suggested_banglish_clean": auto["auto_suggested_banglish_clean"],
                "reviewed_banglish": "",
                "quality_label": "",
                "review_notes": "",
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No review rows to write")
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fenced(text: str) -> str:
    return "```text\n" + text.rstrip() + "\n```"


def write_report(
    path: Path,
    csv_path: Path,
    rows: list[dict[str, str]],
    top_n: int,
) -> None:
    dataset_counts = Counter(row["dataset"] for row in rows)
    bucket_counts = Counter(row["priority_bucket"] for row in rows)
    artifact_counts = Counter(
        row["artifact_patterns"] or "not_in_artifact_queue" for row in rows
    )

    lines = [
        "# Validation-200 v5 Review Queue",
        "",
        "Updated: 2026-05-28",
        "",
        "## Purpose",
        "",
        "This queue merges the broad auto-suggested Banglish edits with the",
        "Bangla and English source text needed for human review. It is not a",
        "reviewed dataset; the blank review columns are for manual decisions.",
        "",
        "## Artifacts",
        "",
        f"- CSV: `{csv_path.relative_to(ROOT)}`",
        "- Source slice: `data/slices/validation_200_v4.jsonl`",
        "- Auto-suggestion queue: `data/slices/banglish_auto_suggested_review_priority_v1.csv`",
        "- Artifact-priority queue: `data/slices/banglish_human_review_priority_v3_suggestions.csv`",
        "",
        "## Counts",
        "",
        f"- Rows: {len(rows)}",
    ]
    for key, value in dataset_counts.most_common():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "| Priority bucket | Items |", "| --- | ---: |"])
    for key, value in bucket_counts.most_common():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "| Artifact pattern | Items |", "| --- | ---: |"])
    for key, value in artifact_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(
        [
            "",
            "## Review Instructions",
            "",
            "- Compare `current_banglish_clean` and `auto_suggested_banglish_clean`",
            "  against both `bangla` and `english`.",
            "- Fill `reviewed_banglish` only when the reviewed text should replace",
            "  the current Banglish.",
            "- Use `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`.",
            "- Do not treat `auto_suggested_banglish_clean` as gold; it is only a",
            "  candidate.",
            "",
            f"## Top {top_n} Review Items",
            "",
        ]
    )

    for idx, row in enumerate(rows[:top_n], start=1):
        lines.extend(
            [
                f"### {idx}. {row['id']}",
                "",
                f"- Dataset: `{row['dataset']}`",
                f"- Priority: `{row['priority_bucket']}`",
                f"- Replacement count: {row['replacement_count']}",
                f"- Artifact patterns: `{row['artifact_patterns'] or 'none'}`",
                f"- Suggestions: {row['suggestion_notes']}",
                f"- v4 correctness: Qwen2.5={row['qwen25_v4_correct']}, Qwen3={row['qwen3_v4_correct']}",
                "",
                "Bangla:",
                "",
                fenced(row["bangla"]),
                "",
                "English:",
                "",
                fenced(row["english"]),
                "",
                "Current Banglish:",
                "",
                fenced(row["current_banglish_clean"]),
                "",
                "Auto-suggested Banglish:",
                "",
                fenced(row["auto_suggested_banglish_clean"]),
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slice", type=Path, default=DEFAULT_SLICE)
    parser.add_argument("--auto-queue", type=Path, default=DEFAULT_AUTO_QUEUE)
    parser.add_argument("--artifact-queue", type=Path, default=DEFAULT_ARTIFACT_QUEUE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--top-n", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_jsonl(args.slice)
    auto_rows = load_csv(args.auto_queue)
    artifacts = artifact_lookup(args.artifact_queue)
    rows = build_rows(items, auto_rows, artifacts)
    write_csv(args.output, rows)
    write_report(args.report_output, args.output, rows, args.top_n)
    print(f"Wrote {len(rows)} review rows to {args.output}")
    print(f"Wrote report to {args.report_output}")


if __name__ == "__main__":
    main()
