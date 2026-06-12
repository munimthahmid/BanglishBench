#!/usr/bin/env python3
"""Build a small calibration packet before full validation-200 v5 review."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def first_sentence(text: str, limit: int = 220) -> str:
    clean = " ".join((text or "").split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def add_selected(
    selected: list[tuple[str, str]],
    seen: set[str],
    rows: list[dict[str, str]],
    reason: str,
    limit: int,
) -> None:
    for row in rows:
        item_id = row["id"]
        if item_id in seen:
            continue
        selected.append((item_id, reason))
        seen.add(item_id)
        if sum(1 for _, r in selected if r == reason) >= limit:
            return


def build_selection(
    queue_rows: list[dict[str, str]],
    ranking_rows: list[dict[str, str]],
    substitution_rows: list[dict[str, str]],
    max_rows: int,
) -> list[tuple[str, str]]:
    selected: list[tuple[str, str]] = []
    seen: set[str] = set()

    tier1 = [r for r in ranking_rows if r.get("impact_tier") == "tier_1_review_first"]
    add_selected(selected, seen, tier1, "top impact tier-1 row", 6)

    by_id = {row["id"]: row for row in ranking_rows}
    for sub in substitution_rows[:5]:
        examples = [item.strip() for item in sub.get("example_ids", "").split(";") if item.strip()]
        rows = [by_id[item] for item in examples if item in by_id]
        reason = f"calibrate `{sub['source']} -> {sub['target']}`"
        add_selected(selected, seen, rows, reason, 2)
        if len(selected) >= max_rows:
            break

    if len(selected) < max_rows:
        dev_rows = [r for r in ranking_rows if r.get("split") == "dev"]
        add_selected(selected, seen, dev_rows, "include dev split example", 2)

    if len(selected) < max_rows:
        math_rows = [
            r
            for r in ranking_rows
            if r.get("dataset") == "banglamath" and int(r.get("replacement_count") or 0) >= 5
        ]
        add_selected(selected, seen, math_rows, "high-edit BanglaMATH wording", 3)

    if len(selected) < max_rows:
        add_selected(selected, seen, ranking_rows, "fill from impact ranking", max_rows - len(selected))

    queue_ids = {row["id"] for row in queue_rows}
    return [(item_id, reason) for item_id, reason in selected[:max_rows] if item_id in queue_ids]


def write_markdown(
    selected: list[tuple[str, str]],
    queue_rows: list[dict[str, str]],
    ranking_rows: list[dict[str, str]],
    output: Path,
) -> None:
    queue_by_id = {row["id"]: row for row in queue_rows}
    rank_by_id = {row["id"]: row for row in ranking_rows}
    queue_line_by_id = {row["id"]: idx + 2 for idx, row in enumerate(queue_rows)}

    lines: list[str] = [
        "# Validation-200 v5 Review Calibration Set",
        "",
        "Updated: 2026-05-28",
        "",
        "Use this packet before reviewing the full 140-row v5 queue. The goal is",
        "to establish a consistent editing style for repeated Banglish patterns,",
        "not to auto-accept the suggested edits.",
        "",
        "Authoritative worksheet:",
        "`data/slices/validation_200_v5_review_queue.csv`.",
        "",
        "## Calibration Procedure",
        "",
        "1. Read each item's Bangla, English, current Banglish, and auto-suggested",
        "   Banglish.",
        "2. Decide whether the current Banglish is acceptable.",
        "3. If editing, write the full replacement prompt, not only the changed word.",
        "4. After the calibration set, apply the same style to the impact-ordered",
        "   packets.",
        "",
        "## Selected Items",
        "",
    ]

    for item_id, reason in selected:
        queue = queue_by_id[item_id]
        rank = rank_by_id.get(item_id, {})
        lines.extend(
            [
                f"### {item_id}",
                "",
                f"- Calibration reason: {reason}",
                f"- CSV line: {queue_line_by_id[item_id]}",
                f"- Impact rank/tier: {rank.get('impact_rank', 'n/a')} / {rank.get('impact_tier', 'n/a')}",
                f"- Split: {rank.get('split', 'n/a')}",
                f"- Dataset/task: {queue.get('dataset', '')} / {queue.get('task_type', '')}",
                f"- Answer: {queue.get('answer', '')}",
                f"- Priority: {queue.get('priority_bucket', '')}",
                f"- Suggestions: {queue.get('suggestion_notes', '') or 'none'}",
                "",
                "**Bangla**",
                "",
                first_sentence(queue.get("bangla", "")),
                "",
                "**English**",
                "",
                first_sentence(queue.get("english", "")),
                "",
                "**Current Banglish**",
                "",
                first_sentence(queue.get("current_banglish_clean", "")),
                "",
                "**Auto-Suggested Banglish**",
                "",
                first_sentence(queue.get("auto_suggested_banglish_clean", "")),
                "",
                "Review fields to fill in the CSV:",
                "",
                "- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`",
                "- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits",
                "- `review_notes`: short reason when useful",
                "",
            ]
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default="data/slices/validation_200_v5_review_queue.csv")
    parser.add_argument(
        "--ranking",
        default="results/analysis/validation200_v5_review_impact_ranking.csv",
    )
    parser.add_argument(
        "--substitutions",
        default="results/analysis/validation200_v5_review_impact_substitutions.csv",
    )
    parser.add_argument(
        "--output",
        default="reports/validation200_v5_review_calibration_set.md",
    )
    parser.add_argument("--max-rows", type=int, default=16)
    args = parser.parse_args()

    queue_rows = read_csv(Path(args.queue))
    ranking_rows = read_csv(Path(args.ranking))
    substitution_rows = read_csv(Path(args.substitutions))
    selected = build_selection(queue_rows, ranking_rows, substitution_rows, args.max_rows)
    write_markdown(selected, queue_rows, ranking_rows, Path(args.output))
    print(f"wrote {len(selected)} calibration rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
