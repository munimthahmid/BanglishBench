#!/usr/bin/env python3
"""Summarize v5 review queue coverage by validation metadata."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v4.jsonl"
DEFAULT_DEV = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_TEST = ROOT / "data/slices/validation_200_v4_test150.jsonl"
DEFAULT_RANKING = ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv"
DEFAULT_OUTPUT = ROOT / "results/analysis/validation200_v5_review_metadata_summary.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_review_metadata_summary.md"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_jsonl_by_id(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                out[str(row["id"])] = row
    return out


def load_split_map(dev_path: Path, test_path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for split, path in [("dev", dev_path), ("test", test_path)]:
        for item_id in load_jsonl_by_id(path):
            out[item_id] = split
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows for {path}")
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


def build_enriched_rows(
    queue_rows: list[dict[str, str]],
    item_by_id: dict[str, dict[str, Any]],
    split_by_id: dict[str, str],
    rank_by_id: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in queue_rows:
        item = item_by_id.get(row["id"], {})
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata", {}), dict) else {}
        rank = rank_by_id.get(row["id"], {})
        out.append(
            {
                "id": row["id"],
                "dataset": row["dataset"],
                "split": split_by_id.get(row["id"], "unknown"),
                "domain": item.get("domain", ""),
                "subject": metadata.get("subject", ""),
                "grade": metadata.get("grade", ""),
                "task_type": row["task_type"],
                "answer_type": row["answer_type"],
                "priority_bucket": row["priority_bucket"],
                "impact_tier": rank.get("impact_tier", ""),
                "impact_score": int(rank.get("impact_score", "0") or 0),
                "replacement_count": int(row.get("replacement_count", "0") or 0),
            }
        )
    return out


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("dataset", ["dataset"]),
        ("split", ["split"]),
        ("dataset_split", ["dataset", "split"]),
        ("priority_bucket", ["priority_bucket"]),
        ("impact_tier", ["impact_tier"]),
        ("dataset_priority", ["dataset", "priority_bucket"]),
        ("domain", ["domain"]),
        ("subject", ["subject"]),
        ("grade", ["grade"]),
        ("dataset_domain", ["dataset", "domain"]),
    ]
    out: list[dict[str, Any]] = []
    for group_name, keys in specs:
        grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[tuple(str(row.get(key, "")) or "blank" for key in keys)].append(row)
        for values, items in grouped.items():
            tier_counts = Counter(str(item.get("impact_tier", "")) for item in items)
            split_counts = Counter(str(item.get("split", "")) for item in items)
            out.append(
                {
                    "group": group_name,
                    "key": " | ".join(values),
                    "rows": len(items),
                    "tier1_rows": tier_counts["tier_1_review_first"],
                    "tier2_rows": tier_counts["tier_2_high"],
                    "test_rows": split_counts["test"],
                    "dev_rows": split_counts["dev"],
                    "mean_impact_score": round(
                        sum(int(item["impact_score"]) for item in items) / len(items), 1
                    ),
                    "mean_replacement_count": round(
                        sum(int(item["replacement_count"]) for item in items)
                        / len(items),
                        2,
                    ),
                }
            )
    out.sort(key=lambda row: (row["group"], -int(row["rows"]), row["key"]))
    return out


def write_report(path: Path, output_path: Path, summary_rows: list[dict[str, Any]]) -> None:
    def rows_for(group: str) -> list[dict[str, Any]]:
        return [row for row in summary_rows if row["group"] == group]

    lines = [
        "# Validation-200 v5 Review Metadata Summary",
        "",
        "Updated: 2026-05-28",
        "",
        "## Inputs",
        "",
        f"- Summary CSV: `{output_path.relative_to(ROOT)}`",
        "",
    ]
    for title, group in [
        ("Dataset And Split", "dataset_split"),
        ("Impact Tier", "impact_tier"),
        ("Priority Bucket", "priority_bucket"),
        ("Top Domains", "domain"),
        ("Top Subjects", "subject"),
        ("Grades", "grade"),
    ]:
        lines.extend(
            [
                f"## {title}",
                "",
                "| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in rows_for(group)[:20]:
            lines.append(
                f"| `{row['key']}` | {row['rows']} | {row['tier1_rows']} | {row['test_rows']} | {row['mean_impact_score']} | {row['mean_replacement_count']} |"
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--dev", type=Path, default=DEFAULT_DEV)
    parser.add_argument("--test", type=Path, default=DEFAULT_TEST)
    parser.add_argument("--ranking", type=Path, default=DEFAULT_RANKING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queue_rows = load_csv(args.queue)
    item_by_id = load_jsonl_by_id(args.items)
    split_by_id = load_split_map(args.dev, args.test)
    rank_by_id = {row["id"]: row for row in load_csv(args.ranking)}
    enriched = build_enriched_rows(queue_rows, item_by_id, split_by_id, rank_by_id)
    summary_rows = summarize(enriched)
    write_csv(args.output, summary_rows)
    write_report(args.report, args.output, summary_rows)
    print(f"queue_rows={len(queue_rows)}")
    print(f"summary_rows={len(summary_rows)}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
