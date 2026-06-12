#!/usr/bin/env python3
"""Build a small high-impact smoke subset for final paid API audits."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_RANKING = ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv"
DEFAULT_OUTPUT = ROOT / "data/slices/api_audit_smoke_10_v5.jsonl"
DEFAULT_REPORT = ROOT / "reports/api_audit_smoke_subset_v5.md"


def load_jsonl_by_id(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                out[str(row["id"])] = row
    return out


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def select_rows(
    ranking: list[dict[str, str]],
    item_by_id: dict[str, dict[str, Any]],
    total: int,
    benqa_target: int,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    seen: set[str] = set()
    banglamath_target = total - benqa_target
    targets = {"benqa": benqa_target, "banglamath": banglamath_target}
    counts = {"benqa": 0, "banglamath": 0}
    for row in sorted(ranking, key=lambda r: int(r["impact_rank"])):
        item_id = row["id"]
        item = item_by_id.get(item_id)
        if not item or item_id in seen:
            continue
        dataset = str(item.get("dataset", ""))
        if dataset not in counts or counts[dataset] >= targets[dataset]:
            continue
        selected.append(row)
        seen.add(item_id)
        counts[dataset] += 1
        if len(selected) == total:
            break
    if len(selected) < total:
        raise SystemExit(f"Only selected {len(selected)} rows; wanted {total}")
    return selected


def write_report(
    path: Path,
    items_path: Path,
    ranking_path: Path,
    output_path: Path,
    selected: list[dict[str, str]],
) -> None:
    lines = [
        "# API Audit Smoke Subset",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Items: `{items_path.relative_to(ROOT)}`",
        f"- Impact ranking: `{ranking_path.relative_to(ROOT)}`",
        f"- Output JSONL: `{output_path.relative_to(ROOT)}`",
        "",
        "This subset is for paid-API prompt/token/cost smoke testing only. It is",
        "not a replacement for full validation-200 reporting.",
        "",
        "## Selected Items",
        "",
        "| # | ID | Dataset | Split | Impact rank | Tier | Score | Reasons |",
        "| ---: | --- | --- | --- | ---: | --- | ---: | --- |",
    ]
    for idx, row in enumerate(selected, start=1):
        lines.append(
            f"| {idx} | `{row['id']}` | {row['dataset']} | {row['split']} | {row['impact_rank']} | `{row['impact_tier']}` | {row['impact_score']} | {row['impact_reasons']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--ranking", type=Path, default=DEFAULT_RANKING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--total", type=int, default=10)
    parser.add_argument("--benqa-target", type=int, default=6)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_by_id = load_jsonl_by_id(args.items)
    ranking = load_csv(args.ranking)
    selected_rank_rows = select_rows(
        ranking, item_by_id, total=args.total, benqa_target=args.benqa_target
    )
    selected_items = [item_by_id[row["id"]] for row in selected_rank_rows]
    write_jsonl(args.output, selected_items)
    write_report(args.report, args.items, args.ranking, args.output, selected_rank_rows)
    print(f"selected={len(selected_items)}")
    print(f"output={args.output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
