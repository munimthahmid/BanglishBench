#!/usr/bin/env python3
"""Summarize v5 review suggested substitutions by impact-ranked rows."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RANKING = ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv"
DEFAULT_OUTPUT = ROOT / "results/analysis/validation200_v5_review_impact_substitutions.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_review_impact_substitutions.md"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_suggestions(notes: str) -> list[tuple[str, str, int]]:
    out: list[tuple[str, str, int]] = []
    for part in notes.split(";"):
        part = part.strip()
        if not part or "->" not in part:
            continue
        src, rest = part.split("->", 1)
        dst = rest
        count = 1
        if "(" in rest and rest.endswith(")"):
            dst, raw_count = rest.rsplit("(", 1)
            raw_count = raw_count.rstrip(")").strip()
            try:
                count = int(raw_count)
            except ValueError:
                count = 1
        out.append((src.strip(), dst.strip(), count))
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit("No substitution rows to write.")
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


def summarize(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    occurrence_counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        score = int(row["impact_score"])
        for src, dst, count in parse_suggestions(row.get("suggestion_notes", "")):
            key = (src, dst)
            occurrence_counts[key] += count
            grouped[key].append(
                {
                    "id": row["id"],
                    "score": score,
                    "tier": row["impact_tier"],
                    "split": row["split"],
                    "priority": row["priority_bucket"],
                    "count": count,
                }
            )

    out_rows: list[dict[str, Any]] = []
    for (src, dst), items in grouped.items():
        scores = [int(item["score"]) for item in items]
        tier_counts = Counter(item["tier"] for item in items)
        split_counts = Counter(item["split"] for item in items)
        priority_counts = Counter(item["priority"] for item in items)
        examples = sorted(items, key=lambda item: (-int(item["score"]), item["id"]))[:5]
        out_rows.append(
            {
                "source": src,
                "target": dst,
                "rows": len(items),
                "occurrences": occurrence_counts[(src, dst)],
                "max_impact_score": max(scores),
                "mean_impact_score": round(mean(scores), 1),
                "tier1_rows": tier_counts["tier_1_review_first"],
                "tier2_rows": tier_counts["tier_2_high"],
                "test_rows": split_counts["test"],
                "dev_rows": split_counts["dev"],
                "top_priority_bucket": priority_counts.most_common(1)[0][0],
                "example_ids": "; ".join(item["id"] for item in examples),
            }
        )
    out_rows.sort(
        key=lambda row: (
            -int(row["tier1_rows"]),
            -int(row["test_rows"]),
            -int(row["occurrences"]),
            -int(row["max_impact_score"]),
            row["source"],
            row["target"],
        )
    )
    return out_rows


def write_report(
    path: Path,
    ranking_path: Path,
    output_path: Path,
    rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# Validation-200 v5 Review Impact Substitutions",
        "",
        "Updated: 2026-05-28",
        "",
        "## Inputs",
        "",
        f"- Impact ranking: `{ranking_path.relative_to(ROOT)}`",
        f"- Substitution CSV: `{output_path.relative_to(ROOT)}`",
        "",
        "This report helps batch review repeated suggested substitutions. It is",
        "not an auto-accept list; every row still needs source-context review.",
        "",
        "## Top Substitutions By Impact",
        "",
        "| Substitution | Rows | Occurrences | Tier-1 rows | Test rows | Max score | Mean score | Example IDs |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows[:30]:
        lines.append(
            "| `{src}` -> `{dst}` | {rows} | {occ} | {tier1} | {test} | {max_score} | {mean_score} | {examples} |".format(
                src=row["source"],
                dst=row["target"],
                rows=row["rows"],
                occ=row["occurrences"],
                tier1=row["tier1_rows"],
                test=row["test_rows"],
                max_score=row["max_impact_score"],
                mean_score=row["mean_impact_score"],
                examples=row["example_ids"],
            )
        )

    lines.extend(
        [
            "",
            "## Review Use",
            "",
            "Start with high tier-1/test-row substitutions, but verify each item",
            "against Bangla and English because the same spelling edit can be correct",
            "in one context and too aggressive in another.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ranking", type=Path, default=DEFAULT_RANKING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = summarize(load_csv(args.ranking))
    write_csv(args.output, rows)
    write_report(args.report, args.ranking, args.output, rows)
    print(f"substitutions={len(rows)}")
    print(f"csv={args.output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
