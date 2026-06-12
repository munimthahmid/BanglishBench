#!/usr/bin/env python3
"""Build generated-Bengali dev answer-audit slices."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_OUTPUT = (
    ROOT
    / "data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl"
)
DEFAULT_REPORT = ROOT / "reports/generated_bn_answer_audit_slice_dev50_benqa_mcq.md"
GENERATOR_SPECS = [
    (
        "generated_bn_phonetic_protected",
        ROOT / "results/generated_views/phonetic_bangla_protected_dev50_benqa_mcq_generated_bn.jsonl",
    ),
    (
        "generated_bn_bnb_protected",
        ROOT / "results/generated_views/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn.jsonl",
    ),
]
DEFAULT_STATUS = "historical_protected_v1_deterministic_generated_bn_dev_audit"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def load_generated(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in load_jsonl(path):
        out[str(row["id"])] = str(row.get("generated_text", ""))
    return out


def parse_generator_specs(raw_specs: list[str] | None) -> list[tuple[str, Path]]:
    if not raw_specs:
        return GENERATOR_SPECS

    specs: list[tuple[str, Path]] = []
    for raw in raw_specs:
        if "=" not in raw:
            raise SystemExit("--generator-spec must use FIELD=PATH")
        field, path_text = raw.split("=", 1)
        field = field.strip()
        if not field:
            raise SystemExit("--generator-spec FIELD cannot be empty")
        path = Path(path_text.strip())
        if not path.is_absolute():
            path = ROOT / path
        specs.append((field, path))
    return specs


def build_rows(
    items: list[dict[str, Any]],
    generator_specs: list[tuple[str, Path]],
    status: str,
) -> list[dict[str, Any]]:
    generated_by_field = {
        field: load_generated(path) for field, path in generator_specs
    }
    item_ids = set.intersection(
        *(set(generated.keys()) for generated in generated_by_field.values())
    )

    rows: list[dict[str, Any]] = []
    for item in items:
        item_id = str(item.get("id", ""))
        if item_id not in item_ids:
            continue
        if item.get("dataset") != "benqa" or item.get("answer_type") != "choice":
            continue
        row = dict(item)
        row["generated_view_status"] = status
        for field, generated in generated_by_field.items():
            row[field] = generated[item_id]
        rows.append(row)
    return rows


def write_report(
    path: Path,
    items_path: Path,
    output_path: Path,
    rows: list[dict[str, Any]],
    generator_specs: list[tuple[str, Path]],
    status: str,
) -> None:
    dataset_counts = Counter(row.get("dataset", "") for row in rows)
    subject_counts = Counter(row.get("subject", "") for row in rows)
    lines = [
        "# Generated-BN Answer Audit Slice: Dev50 BEnQA MCQ",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This slice joins a locked dev50 BEnQA MCQ item subset with generated",
        "Bengali candidate views so the standard evaluator can answer Banglish",
        "and generated views under the same parser.",
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
    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Rows: {len(rows)}",
        ]
    )
    for key, value in dataset_counts.most_common():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "| Subject | Rows |", "| --- | ---: |"])
    for key, value in subject_counts.most_common():
        lines.append(f"| `{key or 'unknown'}` | {value} |")
    lines.extend(
        [
            "",
            "## Suggested Dev-Only Variants",
            "",
            "- `banglish_clean`",
        ]
    )
    for field, _ in generator_specs:
        lines.append(f"- `{field}`")
    lines.extend(
        [
            "",
            "Do not run test150 from this slice. If a generated-BN variant helps on",
            "dev, first inspect item-level outputs and decide whether a generated",
            "English view is needed for the full agreement-routing protocol.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--generator-spec",
        action="append",
        help="Generated view mapping as FIELD=PATH. Repeat for multiple generators.",
    )
    parser.add_argument("--status", default=DEFAULT_STATUS)
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
    )
    print(f"rows={len(rows)}")
    print(f"output={args.output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
