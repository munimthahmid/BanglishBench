#!/usr/bin/env python3
"""Build a compact brief for the next pending validation-200 v5 review session."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_row_ids(raw: str) -> list[str]:
    return [item for item in raw.split(";") if item]


def next_pending_session(resume_rows: list[dict[str, str]]) -> dict[str, str] | None:
    for row in resume_rows:
        if int(row.get("pending_rows", "0") or 0) > 0:
            return row
    return None


def count_values(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row.get(field, "") or "missing" for row in rows)


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "order",
        "id",
        "impact_rank",
        "impact_tier",
        "split",
        "dataset",
        "task_type",
        "priority_bucket",
        "replacement_count",
        "quality_label",
        "substitutions",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def append_counter_table(lines: list[str], title: str, counts: Counter[str]) -> None:
    lines.extend([f"## {title}", "", "| Value | Rows |", "| --- | ---: |"])
    for value, count in counts.most_common():
        lines.append(f"| `{value}` | {count} |")
    lines.append("")


def write_no_pending_report(output_md: Path, output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["status"])
        writer.writeheader()
        writer.writerow({"status": "all_sessions_complete"})
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        "\n".join(
            [
                "# Validation-200 v5 Next Session Brief",
                "",
                f"Updated: {date.today().isoformat()}",
                "",
                "All generated review sessions are complete.",
                "",
                "Run the completion gate next:",
                "",
                "```bash",
                "python3 scripts/validate_banglish_review_queue.py --require-complete",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_report(
    session: dict[str, str],
    rows: list[dict[str, str]],
    output_md: Path,
    output_csv: Path,
) -> None:
    output_md.parent.mkdir(parents=True, exist_ok=True)
    session_number = int(session["session"])
    packet = f"reports/validation200_v5_review_session_packets/session_{session_number:02d}.md"
    multi_replacement_rows = [
        row for row in rows if int(row.get("replacement_count", "0") or 0) >= 3
    ]
    lines = [
        "# Validation-200 v5 Next Session Brief",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        f"Machine-readable brief: `{output_csv.relative_to(ROOT)}`.",
        "",
        "## Session",
        "",
        f"- Session: `{session_number}`",
        f"- Substitution batch: `{session['substitution']}`",
        f"- Rows in this session: `{len(rows)}`",
        f"- Pending rows in session: `{session['pending_rows']}`",
        f"- Read-only packet: `{packet}`",
        "",
        "Preview command:",
        "",
        "```bash",
        session["preview_command"],
        "```",
        "",
        "Review command:",
        "",
        "```bash",
        session["review_command"],
        "```",
        "",
        "## Review Focus",
        "",
        "- Keep edits limited to the authoritative CSV/helper workflow.",
        "- Prefer `ok` only when the auto-suggested Banglish preserves meaning.",
        "- Use `minor_edit` or `major_edit` when the row needs a corrected",
        "  reviewed Banglish string.",
        "- Use `bad` only when the row should be excluded and add review notes.",
        "",
    ]
    append_counter_table(lines, "By Impact Tier", count_values(rows, "impact_tier"))
    append_counter_table(lines, "By Split", count_values(rows, "split"))
    append_counter_table(lines, "By Dataset", count_values(rows, "dataset"))
    append_counter_table(lines, "By Priority Bucket", count_values(rows, "priority_bucket"))

    lines.extend(
        [
            "## Highest-Risk Rows",
            "",
            "Rows with three or more suggested replacements need extra attention.",
            "",
            "| Order | Row id | Impact rank | Replacements | Substitutions |",
            "| ---: | --- | ---: | ---: | --- |",
        ]
    )
    for row in multi_replacement_rows:
        lines.append(
            "| {order} | `{row_id}` | {rank} | {count} | {subs} |".format(
                order=row["order"],
                row_id=row["id"],
                rank=row["impact_rank"],
                count=row["replacement_count"],
                subs=row["substitutions"],
            )
        )
    lines.append("")

    lines.extend(
        [
            "## Row Order",
            "",
            "| Order | Row id | Tier | Split | Dataset | Task | Priority |",
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {order} | `{row_id}` | `{tier}` | `{split}` | `{dataset}` | `{task}` | `{priority}` |".format(
                order=row["order"],
                row_id=row["id"],
                tier=row["impact_tier"],
                split=row["split"],
                dataset=row["dataset"],
                task=row["task_type"],
                priority=row["priority_bucket"],
            )
        )
    lines.append("")
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_rows(
    session: dict[str, str],
    session_plan_rows: list[dict[str, str]],
    queue_by_id: dict[str, dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    plan = next(row for row in session_plan_rows if row["session"] == session["session"])
    rows: list[dict[str, str]] = []
    for order, row_id in enumerate(split_row_ids(plan["row_ids"]), start=1):
        queue_row = queue_by_id[row_id]
        rank_row = rank_by_id.get(row_id, {})
        rows.append(
            {
                "order": str(order),
                "id": row_id,
                "impact_rank": rank_row.get("impact_rank", ""),
                "impact_tier": rank_row.get("impact_tier", ""),
                "split": rank_row.get("split", ""),
                "dataset": queue_row.get("dataset", ""),
                "task_type": queue_row.get("task_type", ""),
                "priority_bucket": queue_row.get("priority_bucket", ""),
                "replacement_count": queue_row.get("replacement_count", ""),
                "quality_label": queue_row.get("quality_label", ""),
                "substitutions": queue_row.get("suggestion_notes", ""),
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=ROOT / "data/slices/validation_200_v5_review_queue.csv")
    parser.add_argument("--ranking", type=Path, default=ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv")
    parser.add_argument("--session-plan", type=Path, default=ROOT / "results/analysis/validation200_v5_review_session_plan.csv")
    parser.add_argument("--resume-csv", type=Path, default=ROOT / "results/analysis/validation200_v5_review_resume_card.csv")
    parser.add_argument("--output-csv", type=Path, default=ROOT / "results/analysis/validation200_v5_next_session_brief.csv")
    parser.add_argument("--output-md", type=Path, default=ROOT / "reports/validation200_v5_next_session_brief.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queue_rows = read_csv(args.queue)
    rank_rows = read_csv(args.ranking)
    session_plan_rows = read_csv(args.session_plan)
    resume_rows = read_csv(args.resume_csv)
    session = next_pending_session(resume_rows)
    if session is None:
        write_no_pending_report(args.output_md, args.output_csv)
        print(f"next_session=none rows=0 report={args.output_md}")
        return
    queue_by_id = {row["id"]: row for row in queue_rows}
    rank_by_id = {row["id"]: row for row in rank_rows}
    rows = build_rows(session, session_plan_rows, queue_by_id, rank_by_id)
    write_csv(rows, args.output_csv)
    write_report(session, rows, args.output_md, args.output_csv)
    print(
        f"next_session={session['session']} rows={len(rows)} "
        f"report={args.output_md}"
    )


if __name__ == "__main__":
    main()
