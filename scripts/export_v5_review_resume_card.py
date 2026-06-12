#!/usr/bin/env python3
"""Export a compact resume card for validation-200 v5 manual review."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SessionStatus:
    session: int
    substitution: str
    total_rows: int
    reviewed_rows: int
    pending_rows: int
    preview_command: str
    review_command: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def is_reviewed(row: dict[str, str]) -> bool:
    return bool(row.get("quality_label", "").strip())


def label_status(row: dict[str, str]) -> str:
    label = row.get("quality_label", "").strip()
    return label if label else "pending"


def session_statuses(
    queue_rows: list[dict[str, str]],
    session_rows: list[dict[str, str]],
) -> list[SessionStatus]:
    queue_by_id = {row["id"]: row for row in queue_rows}
    statuses: list[SessionStatus] = []
    for row in session_rows:
        row_ids = [item for item in row["row_ids"].split(";") if item]
        reviewed = sum(1 for row_id in row_ids if is_reviewed(queue_by_id[row_id]))
        total = len(row_ids)
        statuses.append(
            SessionStatus(
                session=int(row["session"]),
                substitution=row["substitution"],
                total_rows=total,
                reviewed_rows=reviewed,
                pending_rows=total - reviewed,
                preview_command=row["preview_command"],
                review_command=row["command"],
            )
        )
    return statuses


def write_csv_output(statuses: list[SessionStatus], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "session",
                "substitution",
                "total_rows",
                "reviewed_rows",
                "pending_rows",
                "preview_command",
                "review_command",
            ],
        )
        writer.writeheader()
        for status in statuses:
            writer.writerow(
                {
                    "session": status.session,
                    "substitution": status.substitution,
                    "total_rows": status.total_rows,
                    "reviewed_rows": status.reviewed_rows,
                    "pending_rows": status.pending_rows,
                    "preview_command": status.preview_command,
                    "review_command": status.review_command,
                }
            )


def write_markdown(
    queue_rows: list[dict[str, str]],
    statuses: list[SessionStatus],
    output: Path,
    csv_path: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    label_counts = Counter(label_status(row) for row in queue_rows)
    total_rows = len(queue_rows)
    reviewed_rows = total_rows - label_counts.get("pending", 0)
    next_session = next((status for status in statuses if status.pending_rows), None)

    lines = [
        "# Validation-200 v5 Review Resume Card",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This card is generated from the authoritative review queue and session",
        "plan. It is meant to be the quickest restart point after an interruption.",
        "",
        f"Machine-readable session status: `{csv_path}`.",
        "",
        "## Overall",
        "",
        "| Metric | Rows |",
        "| --- | ---: |",
        f"| Total review rows | {total_rows} |",
        f"| Reviewed rows | {reviewed_rows} |",
        f"| Pending rows | {label_counts.get('pending', 0)} |",
        "",
        "## Label Counts",
        "",
        "| Label | Rows |",
        "| --- | ---: |",
    ]
    for label in ["pending", "ok", "minor_edit", "major_edit", "bad"]:
        lines.append(f"| `{label}` | {label_counts.get(label, 0)} |")
    lines.append("")

    if next_session:
        packet = f"reports/validation200_v5_review_session_packets/session_{next_session.session:02d}.md"
        lines.extend(
            [
                "## Next Session",
                "",
                f"- Session: `{next_session.session}`",
                f"- Substitution batch: `{next_session.substitution}`",
                f"- Pending in session: `{next_session.pending_rows}` of `{next_session.total_rows}`",
                f"- Read-only packet: `{packet}`",
                "",
                "Preview first:",
                "",
                "```bash",
                next_session.preview_command,
                "```",
                "",
                "Then review:",
                "",
                "```bash",
                next_session.review_command,
                "```",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Next Session",
                "",
                "All planned sessions are reviewed. Move to the completion gate:",
                "",
                "```bash",
                "python3 scripts/validate_banglish_review_queue.py --require-complete",
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## After Each Session",
            "",
            "```bash",
            "python3 scripts/plan_v5_review_sessions.py",
            "python3 scripts/export_v5_review_session_packets.py",
            "python3 scripts/summarize_v5_review_progress.py",
            "python3 scripts/export_v5_review_resume_card.py",
            "python3 scripts/validate_banglish_review_queue.py",
            "python3 scripts/check_post_v5_rerun_readiness.py",
            "```",
            "",
            "Record the session outcome in",
            "`reports/validation200_v5_review_session_log.md` before freezing v5.",
            "",
            "## Session Status",
            "",
            "| Session | Substitution | Total | Reviewed | Pending |",
            "| ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for status in statuses:
        lines.append(
            f"| {status.session} | `{status.substitution}` | {status.total_rows} | "
            f"{status.reviewed_rows} | {status.pending_rows} |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queue",
        type=Path,
        default=ROOT / "data/slices/validation_200_v5_review_queue.csv",
    )
    parser.add_argument(
        "--session-plan",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_session_plan.csv",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_resume_card.csv",
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=ROOT / "reports/validation200_v5_review_resume_card.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queue_rows = read_csv(args.queue)
    plan_rows = read_csv(args.session_plan)
    statuses = session_statuses(queue_rows, plan_rows)
    write_csv_output(statuses, args.csv_output)
    write_markdown(
        queue_rows,
        statuses,
        args.md_output,
        args.csv_output.relative_to(ROOT),
    )
    pending_sessions = sum(1 for status in statuses if status.pending_rows)
    next_session = next((status.session for status in statuses if status.pending_rows), "none")
    print(
        f"sessions={len(statuses)} pending_sessions={pending_sessions} "
        f"next_session={next_session} report={args.md_output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
