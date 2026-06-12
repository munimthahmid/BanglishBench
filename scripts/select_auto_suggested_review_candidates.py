#!/usr/bin/env python3
"""Prioritize auto-suggested Banglish edits for human review."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


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


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def replacement_count(notes: str) -> int:
    counts = [int(match) for match in re.findall(r"\((\d+)\)", notes)]
    return sum(counts) if counts else int(bool(notes.strip()))


def index_compare(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["id"]: row for row in rows}


def priority_bucket(qwen25_correct: bool, qwen3_correct: bool, count: int) -> str:
    if not qwen25_correct and not qwen3_correct and count >= 2:
        return "both_wrong_multi_edit"
    if not qwen25_correct and not qwen3_correct:
        return "both_wrong_single_edit"
    if not qwen3_correct and count >= 2:
        return "qwen3_wrong_multi_edit"
    if not qwen25_correct and count >= 2:
        return "qwen25_wrong_multi_edit"
    if count >= 3:
        return "high_edit_count"
    return "lower_priority"


def build_candidates(
    audit_rows: list[dict[str, str]],
    qwen25_rows: dict[str, dict[str, str]],
    qwen3_rows: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in audit_rows:
        if row.get("field") != "banglish_clean" or row.get("changed") != "True":
            continue
        item_id = row["id"]
        q25 = qwen25_rows.get(item_id, {})
        q3 = qwen3_rows.get(item_id, {})
        q25_v4_correct = truthy(q25.get("after_correct", ""))
        q3_v4_correct = truthy(q3.get("after_correct", ""))
        count = replacement_count(row.get("suggestion_notes", ""))
        bucket = priority_bucket(q25_v4_correct, q3_v4_correct, count)
        out.append(
            {
                "id": item_id,
                "dataset": row.get("dataset", ""),
                "priority_bucket": bucket,
                "replacement_count": count,
                "suggestion_notes": row.get("suggestion_notes", ""),
                "qwen25_v4_correct": q25_v4_correct,
                "qwen3_v4_correct": q3_v4_correct,
                "qwen25_v3_to_v4_change": q25.get("change", ""),
                "qwen3_v3_to_v4_change": q3.get("change", ""),
                "current_banglish_clean": row.get("old_text", ""),
                "auto_suggested_banglish_clean": row.get("new_text", ""),
                "reviewed_banglish": "",
                "quality_label": "",
                "review_notes": "",
            }
        )

    rank = {
        "both_wrong_multi_edit": 0,
        "both_wrong_single_edit": 1,
        "qwen3_wrong_multi_edit": 2,
        "qwen25_wrong_multi_edit": 3,
        "high_edit_count": 4,
        "lower_priority": 5,
    }
    out.sort(
        key=lambda row: (
            rank[row["priority_bucket"]],
            -int(row["replacement_count"]),
            row["dataset"],
            row["id"],
        )
    )
    return out


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    csv_output: Path,
    max_examples: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bucket_counts = Counter(row["priority_bucket"] for row in rows)
    dataset_counts = Counter(row["dataset"] for row in rows)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Auto-Suggested Banglish Human-Review Priority v1\n\n")
        f.write("Updated: 2026-05-28\n\n")
        f.write("## Purpose\n\n")
        f.write(
            "This queue prioritizes automatic Banglish spelling suggestions for "
            "manual review. It is not a reviewed dataset; blank review fields are "
            "included so accepted edits can later be copied into the v5 workflow.\n\n"
        )
        f.write("## Artifacts\n\n")
        f.write(f"- Review CSV: `{repo_path(csv_output)}`\n\n")
        f.write("## Counts\n\n")
        f.write(f"- Candidate rows: {len(rows)}\n")
        for dataset, count in sorted(dataset_counts.items()):
            f.write(f"- `{dataset}`: {count}\n")
        f.write("\n")
        f.write("| Priority bucket | Items |\n")
        f.write("| --- | ---: |\n")
        for bucket, count in bucket_counts.most_common():
            f.write(f"| `{bucket}` | {count} |\n")
        f.write("\n")
        f.write("## Review Guidance\n\n")
        f.write(
            "- Review `current_banglish_clean` against the Bangla/English source "
            "before accepting `auto_suggested_banglish_clean`.\n"
        )
        f.write(
            "- Fill `reviewed_banglish` only when the reviewed text should replace "
            "the current clean Banglish.\n"
        )
        f.write(
            "- Use `quality_label` values from the v5 workflow: `ok`, `minor_edit`, "
            "`major_edit`, or `bad`.\n\n"
        )
        f.write("## Top Examples\n\n")
        for index, row in enumerate(rows[:max_examples], start=1):
            f.write(f"### {index}. {row['id']}\n\n")
            f.write(f"- Dataset: `{row['dataset']}`\n")
            f.write(f"- Priority: `{row['priority_bucket']}`\n")
            f.write(f"- Suggestions: {row['suggestion_notes']}\n")
            f.write(
                f"- v4 correctness: Qwen2.5={row['qwen25_v4_correct']}, "
                f"Qwen3={row['qwen3_v4_correct']}\n\n"
            )
            f.write("Current:\n\n```text\n")
            f.write(str(row["current_banglish_clean"]).rstrip() + "\n")
            f.write("```\n\nAuto-suggested:\n\n```text\n")
            f.write(str(row["auto_suggested_banglish_clean"]).rstrip() + "\n")
            f.write("```\n\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audit",
        type=Path,
        default=ROOT / "results/analysis/validation200_v4_auto_suggested_audit.csv",
    )
    parser.add_argument(
        "--qwen25-compare",
        type=Path,
        default=ROOT / "results/analysis/qwen25_validation200_v3_vs_v4_banglish_items_reparsed.csv",
    )
    parser.add_argument(
        "--qwen3-compare",
        type=Path,
        default=ROOT / "results/analysis/qwen3_validation200_v3_vs_v4_banglish_items_reparsed.csv",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "data/slices/banglish_auto_suggested_review_priority_v1.csv",
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=ROOT / "reports/banglish_auto_suggested_review_priority_v1.md",
    )
    parser.add_argument("--max-report-examples", type=int, default=15)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_candidates(
        load_csv(args.audit),
        index_compare(load_csv(args.qwen25_compare)),
        index_compare(load_csv(args.qwen3_compare)),
    )
    write_csv(args.csv_output, rows)
    write_report(args.report_output, rows, args.csv_output, args.max_report_examples)
    print(f"rows={len(rows)}")
    print(f"wrote={args.csv_output}")
    print(f"wrote={args.report_output}")


if __name__ == "__main__":
    main()
