#!/usr/bin/env python3
"""Build a targeted frontier-model diagnostic slice from Gemini audit outcomes."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import load_jsonl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_GEMINI_ITEMS = ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_items.csv"
DEFAULT_OUTPUT = ROOT / "data/slices/openai_gpt55_diagnostic_60_v5.jsonl"
DEFAULT_REPORT = ROOT / "reports/openai_gpt55_diagnostic_60_v5_slice.md"
VARIANTS = ("bangla", "banglish_clean", "english")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def add_ids(
    selected: list[str],
    selected_set: set[str],
    candidates: list[str],
    limit: int | None = None,
) -> None:
    added = 0
    for item_id in candidates:
        if item_id in selected_set:
            continue
        selected.append(item_id)
        selected_set.add(item_id)
        added += 1
        if limit is not None and added >= limit:
            return


def build_selection(
    gemini_rows: list[dict[str, str]],
    max_items: int,
    control_items: int,
) -> tuple[list[str], dict[str, str]]:
    by_id: dict[str, dict[str, dict[str, str]]] = {}
    for row in gemini_rows:
        by_id.setdefault(row["id"], {})[row["variant"]] = row

    buckets: dict[str, list[str]] = {
        "bangla_correct_banglish_wrong": [],
        "banglish_recoverable": [],
        "banglish_unrecovered_wrong": [],
        "benqa_banglish_wrong": [],
        "all_strict_correct_control": [],
    }
    for item_id in sorted(by_id):
        variants = by_id[item_id]
        if not all(variant in variants for variant in VARIANTS):
            continue
        bangla = variants["bangla"]
        banglish = variants["banglish_clean"]
        english = variants["english"]
        if truthy(bangla["strict_correct"]) and not truthy(banglish["strict_correct"]):
            buckets["bangla_correct_banglish_wrong"].append(item_id)
        if not truthy(banglish["strict_correct"]) and truthy(banglish["secondary_correct"]):
            buckets["banglish_recoverable"].append(item_id)
        if not truthy(banglish["strict_correct"]) and not truthy(banglish["secondary_correct"]):
            buckets["banglish_unrecovered_wrong"].append(item_id)
        if banglish["dataset"] == "benqa" and not truthy(banglish["strict_correct"]):
            buckets["benqa_banglish_wrong"].append(item_id)
        if all(truthy(variants[variant]["strict_correct"]) for variant in VARIANTS):
            buckets["all_strict_correct_control"].append(item_id)

    selected: list[str] = []
    selected_set: set[str] = set()
    bucket_for_id: dict[str, str] = {}

    hard_cap = max(0, max_items - control_items)
    schedule = [
        ("bangla_correct_banglish_wrong", None),
        ("banglish_recoverable", None),
        ("benqa_banglish_wrong", None),
        ("banglish_unrecovered_wrong", None),
    ]
    for bucket, limit in schedule:
        before = set(selected_set)
        add_ids(selected, selected_set, buckets[bucket], limit)
        for item_id in selected_set - before:
            bucket_for_id[item_id] = bucket
        if len(selected) >= hard_cap:
            break

    selected = selected[:hard_cap]
    selected_set = set(selected)
    before = set(selected_set)
    add_ids(selected, selected_set, buckets["all_strict_correct_control"], control_items)
    for item_id in selected_set - before:
        bucket_for_id[item_id] = "all_strict_correct_control"
    selected = selected[:max_items]
    bucket_for_id = {item_id: bucket_for_id[item_id] for item_id in selected}
    return selected, bucket_for_id


def build_rows(
    source_items: list[dict[str, Any]],
    selected_ids: list[str],
    bucket_for_id: dict[str, str],
) -> list[dict[str, Any]]:
    source_by_id = {str(item["id"]): item for item in source_items}
    missing = [item_id for item_id in selected_ids if item_id not in source_by_id]
    if missing:
        raise SystemExit(f"Selected ids missing from source slice: {', '.join(missing[:5])}")

    rows: list[dict[str, Any]] = []
    for rank, item_id in enumerate(selected_ids, start=1):
        row = dict(source_by_id[item_id])
        row["diagnostic_rank"] = rank
        row["diagnostic_bucket"] = bucket_for_id[item_id]
        rows.append(row)
    return rows


def write_report(
    path: Path,
    source_items: Path,
    gemini_items: Path,
    output: Path,
    rows: list[dict[str, Any]],
) -> None:
    dataset_counts = Counter(str(row.get("dataset", "")) for row in rows)
    bucket_counts = Counter(str(row.get("diagnostic_bucket", "")) for row in rows)
    lines = [
        "# GPT-5.5 Diagnostic Slice",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This slice targets the frontier-model question raised by the Gemini audit:",
        "whether reviewed Banglish failures persist because of semantic understanding",
        "or because the code-mixed setting destabilizes answer format and unit",
        "normalization. It is not the final full SOTA run.",
        "",
        "## Artifacts",
        "",
        f"- Source items: `{repo_path(source_items)}`",
        f"- Gemini item audit: `{repo_path(gemini_items)}`",
        f"- Diagnostic slice: `{repo_path(output)}`",
        f"- Items: {len(rows)}",
        f"- Planned API calls with 3 variants: {len(rows) * 3}",
        "",
        "## Dataset Counts",
        "",
        "| Dataset | Items |",
        "| --- | ---: |",
    ]
    for dataset, count in sorted(dataset_counts.items()):
        lines.append(f"| `{dataset}` | {count} |")
    lines.extend(["", "## Selection Buckets", "", "| Bucket | Items |", "| --- | ---: |"])
    for bucket, count in sorted(bucket_counts.items()):
        lines.append(f"| `{bucket}` | {count} |")
    lines.extend(
        [
            "",
            "## Item IDs",
            "",
            ", ".join(str(row["id"]) for row in rows),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--gemini-items", type=Path, default=DEFAULT_GEMINI_ITEMS)
    parser.add_argument("--max-items", type=int, default=60)
    parser.add_argument("--control-items", type=int, default=6)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected_ids, bucket_for_id = build_selection(
        read_csv(args.gemini_items),
        args.max_items,
        args.control_items,
    )
    rows = build_rows(load_jsonl(args.source_items), selected_ids, bucket_for_id)
    write_jsonl(args.output, rows)
    write_report(args.report, args.source_items, args.gemini_items, args.output, rows)
    print(f"items={len(rows)}")
    print(f"calls={len(rows) * 3}")
    print(f"output={args.output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
