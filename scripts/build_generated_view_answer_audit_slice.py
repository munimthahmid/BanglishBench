#!/usr/bin/env python3
"""Build dev answer-audit slices with arbitrary generated-view fields."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from build_generated_bn_answer_audit_slice import (
    ROOT,
    build_rows,
    parse_generator_specs,
    repo_path,
    load_jsonl,
    write_jsonl,
)


DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_OUTPUT = (
    ROOT
    / "data/generated_views/validation200_v5_dev50_benqa_mcq_guarded_generated_en_answer_audit.jsonl"
)
DEFAULT_REPORT = (
    ROOT / "reports/generated_view_answer_audit_slice_v5_dev50_benqa_mcq_guarded_en.md"
)
DEFAULT_STATUS = "reviewed_v5_guarded_generated_en_dev_audit"


def write_report(
    path: Path,
    items_path: Path,
    output_path: Path,
    rows: list[dict[str, Any]],
    generator_specs: list[tuple[str, Path]],
    status: str,
    title: str,
) -> None:
    dataset_counts = Counter(row.get("dataset", "") for row in rows)
    subject_counts = Counter(row.get("subject", "") for row in rows)
    lines = [
        f"# {title}",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This slice joins a locked dev item subset with generated alternate views",
        "so the standard evaluator can answer Banglish and generated views under",
        "the same parser.",
        "",
        f"Status label: `{status}`",
        "",
        "## Artifacts",
        "",
        f"- Source items: `{repo_path(items_path)}`",
        f"- Output JSONL: `{repo_path(output_path)}`",
    ]
    for field, generated_path in generator_specs:
        lines.append(f"- `{field}` source: `{repo_path(generated_path)}`")
    lines.extend(["", "## Counts", "", f"- Rows: {len(rows)}"])
    for key, value in dataset_counts.most_common():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "| Subject | Rows |", "| --- | ---: |"])
    for key, value in subject_counts.most_common():
        lines.append(f"| `{key or 'unknown'}` | {value} |")
    lines.extend(["", "## Suggested Dev-Only Variants", "", "- `banglish_clean`"])
    for field, _ in generator_specs:
        lines.append(f"- `{field}`")
    lines.extend(
        [
            "",
            "Do not run test150 from this slice. If a generated-view variant",
            "helps on dev, first inspect item-level outputs and preservation-gate",
            "status, then decide whether a full agreement-routing protocol is",
            "ready.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--generator-spec", action="append", required=True)
    parser.add_argument("--status", default=DEFAULT_STATUS)
    parser.add_argument("--title", default="Generated-View Answer Audit Slice")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_jsonl(args.items)
    generator_specs = parse_generator_specs(args.generator_spec)
    rows = build_rows(items, generator_specs, args.status)
    write_jsonl(args.output, rows)
    write_report(
        args.report_output,
        args.items,
        args.output,
        rows,
        generator_specs,
        args.status,
        args.title,
    )
    print(f"rows={len(rows)}")
    print(f"output={args.output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
