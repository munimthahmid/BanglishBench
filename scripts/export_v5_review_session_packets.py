#!/usr/bin/env python3
"""Export read-only Markdown packets for generated v5 review sessions."""

from __future__ import annotations

import argparse
import csv
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fenced(text: str) -> list[str]:
    return ["```text", text.rstrip(), "```"]


def write_session_packet(
    path: Path,
    session: dict[str, str],
    queue_by_id: dict[str, dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
) -> None:
    row_ids = [row_id for row_id in session["row_ids"].split(";") if row_id]
    lines = [
        f"# Validation-200 v5 Review Session {int(session['session']):02d}",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This is a read-only review packet. Fill the authoritative CSV with",
        "`scripts/review_validation200_v5_queue.py`, not this Markdown file.",
        "",
        f"Review command: `{session['command']}`",
        f"Preview command: `{session['preview_command']}`",
        f"Substitution group: `{session['substitution']}`",
        f"Planned rows: `{session['planned_new_rows']}`",
        "",
    ]
    for index, row_id in enumerate(row_ids, start=1):
        row = queue_by_id[row_id]
        rank = rank_by_id.get(row_id, {})
        lines.extend(
            [
                f"## {index}. `{row_id}`",
                "",
                (
                    f"Dataset: `{row.get('dataset', '')}`; "
                    f"task: `{row.get('task_type', '')}`; "
                    f"answer type: `{row.get('answer_type', '')}`."
                ),
                (
                    f"Impact rank: `{rank.get('impact_rank', '')}`; "
                    f"tier: `{rank.get('impact_tier', '')}`; "
                    f"split: `{rank.get('split', '')}`; "
                    f"score: `{rank.get('impact_score', '')}`."
                ),
                f"Priority: `{row.get('priority_bucket', '')}`; replacements: `{row.get('replacement_count', '')}`.",
                f"Reasons: {rank.get('impact_reasons', '')}",
                f"Suggestions: {row.get('suggestion_notes', '')}",
                "",
                "### Bangla",
                "",
                *fenced(row.get("bangla", "")),
                "",
                "### English",
                "",
                *fenced(row.get("english", "")),
                "",
                "### Current Banglish",
                "",
                *fenced(row.get("current_banglish_clean", "")),
                "",
                "### Auto-Suggested Banglish",
                "",
                *fenced(row.get("auto_suggested_banglish_clean", "")),
                "",
                "### Review Fields",
                "",
                "- `quality_label`: pending",
                "- `reviewed_banglish`: pending",
                "- `review_notes`: pending",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readme(path: Path, sessions: list[dict[str, str]]) -> None:
    lines = [
        "# Validation-200 v5 Review Session Packets",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "These packets mirror `reports/validation200_v5_review_session_plan.md`.",
        "They are read-only context files. The source of truth is",
        "`data/slices/validation_200_v5_review_queue.csv`.",
        "",
        "| Session | Packet | Substitution | Rows | Preview command | Review command |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    for session in sessions:
        number = int(session["session"])
        packet = f"session_{number:02d}.md"
        lines.append(
            "| "
            f"{number} | `{packet}` | `{session['substitution']}` | "
            f"{session['planned_new_rows']} | `{session['preview_command']}` | "
            f"`{session['command']}` |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queue",
        type=Path,
        default=ROOT / "data/slices/validation_200_v5_review_queue.csv",
    )
    parser.add_argument(
        "--ranking",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv",
    )
    parser.add_argument(
        "--session-plan",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_session_plan.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "reports/validation200_v5_review_session_packets",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queue_rows = read_csv(args.queue)
    rank_rows = read_csv(args.ranking)
    sessions = read_csv(args.session_plan)
    queue_by_id = {row["id"]: row for row in queue_rows}
    rank_by_id = {row["id"]: row for row in rank_rows}

    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_readme(args.output_dir / "README.md", sessions)
    for session in sessions:
        write_session_packet(
            args.output_dir / f"session_{int(session['session']):02d}.md",
            session,
            queue_by_id,
            rank_by_id,
        )
    print(f"wrote={args.output_dir} sessions={len(sessions)}")


if __name__ == "__main__":
    main()
