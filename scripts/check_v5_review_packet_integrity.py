#!/usr/bin/env python3
"""Validate generated validation-200 v5 review session packets."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_ROW_RE = re.compile(r"^## \d+\. `([^`]+)`", re.MULTILINE)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def is_reviewed(row: dict[str, str]) -> bool:
    return bool(row.get("quality_label", "").strip())


def split_row_ids(raw: str) -> list[str]:
    return [item for item in raw.split(";") if item]


def add_check(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate(
    queue_rows: list[dict[str, str]],
    session_rows: list[dict[str, str]],
    resume_rows: list[dict[str, str]],
    packet_dir: Path,
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    queue_by_id = {row["id"]: row for row in queue_rows}
    pending_ids = [row["id"] for row in queue_rows if not is_reviewed(row)]
    session_numbers = [int(row["session"]) for row in session_rows]

    expected_sessions = list(range(1, len(session_rows) + 1))
    add_check(
        checks,
        "session_numbers_consecutive",
        "ok" if session_numbers == expected_sessions else "error",
        f"found={session_numbers} expected={expected_sessions}",
    )

    planned_ids: list[str] = []
    planned_by_session: dict[int, list[str]] = {}
    for row in session_rows:
        session = int(row["session"])
        row_ids = split_row_ids(row.get("row_ids", ""))
        planned_by_session[session] = row_ids
        planned_ids.extend(row_ids)
        planned_count = int(row.get("planned_new_rows", "0") or 0)
        add_check(
            checks,
            f"session_{session:02d}_planned_count",
            "ok" if planned_count == len(row_ids) else "error",
            f"planned_new_rows={planned_count} row_ids={len(row_ids)}",
        )
        unknown = sorted(set(row_ids) - set(queue_by_id))
        add_check(
            checks,
            f"session_{session:02d}_row_ids_exist",
            "ok" if not unknown else "error",
            "all row ids exist" if not unknown else ", ".join(unknown),
        )

    duplicates = duplicate_values(planned_ids)
    add_check(
        checks,
        "planned_row_ids_unique",
        "ok" if not duplicates else "error",
        "no duplicates" if not duplicates else ", ".join(duplicates),
    )
    missing_pending = sorted(set(pending_ids) - set(planned_ids))
    unexpected_planned = sorted(set(planned_ids) - set(pending_ids))
    add_check(
        checks,
        "planned_ids_cover_pending_queue",
        "ok" if not missing_pending and not unexpected_planned else "error",
        (
            f"pending={len(pending_ids)} planned_unique={len(set(planned_ids))}"
            if not missing_pending and not unexpected_planned
            else f"missing_pending={missing_pending} unexpected_planned={unexpected_planned}"
        ),
    )

    readme_path = packet_dir / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.exists() else ""
    add_check(
        checks,
        "packet_readme_exists",
        "ok" if readme_path.exists() else "error",
        str(readme_path.relative_to(ROOT)),
    )

    expected_packet_names = {f"session_{session:02d}.md" for session in session_numbers}
    actual_packet_names = {path.name for path in packet_dir.glob("session_*.md")} if packet_dir.exists() else set()
    missing_packets = sorted(expected_packet_names - actual_packet_names)
    extra_packets = sorted(actual_packet_names - expected_packet_names)
    add_check(
        checks,
        "packet_file_set",
        "ok" if not missing_packets and not extra_packets else "error",
        (
            f"packets={len(actual_packet_names)}"
            if not missing_packets and not extra_packets
            else f"missing={missing_packets} extra={extra_packets}"
        ),
    )

    for row in session_rows:
        session = int(row["session"])
        packet_name = f"session_{session:02d}.md"
        packet_path = packet_dir / packet_name
        if not packet_path.exists():
            continue
        packet_text = packet_path.read_text(encoding="utf-8", errors="replace")
        packet_ids = PACKET_ROW_RE.findall(packet_text)
        expected_ids = planned_by_session[session]
        add_check(
            checks,
            f"session_{session:02d}_packet_ids",
            "ok" if packet_ids == expected_ids else "error",
            f"packet_ids={len(packet_ids)} expected_ids={len(expected_ids)}",
        )
        required_strings = [
            f"Review command: `{row['command']}`",
            f"Preview command: `{row['preview_command']}`",
            f"Substitution group: `{row['substitution']}`",
            f"Planned rows: `{row['planned_new_rows']}`",
        ]
        missing_strings = [text for text in required_strings if text not in packet_text]
        add_check(
            checks,
            f"session_{session:02d}_packet_metadata",
            "ok" if not missing_strings else "error",
            "metadata present" if not missing_strings else "; ".join(missing_strings),
        )
        add_check(
            checks,
            f"session_{session:02d}_readme_link",
            "ok" if f"`{packet_name}`" in readme_text else "error",
            packet_name,
        )

    resume_by_session = {int(row["session"]): row for row in resume_rows if row.get("session", "").isdigit()}
    add_check(
        checks,
        "resume_session_set",
        "ok" if set(resume_by_session) == set(session_numbers) else "error",
        f"resume_sessions={sorted(resume_by_session)} plan_sessions={session_numbers}",
    )
    for row in session_rows:
        session = int(row["session"])
        resume = resume_by_session.get(session)
        if not resume:
            continue
        row_ids = planned_by_session[session]
        reviewed = sum(1 for row_id in row_ids if is_reviewed(queue_by_id[row_id]))
        pending = len(row_ids) - reviewed
        expected_values = {
            "substitution": row["substitution"],
            "total_rows": str(len(row_ids)),
            "reviewed_rows": str(reviewed),
            "pending_rows": str(pending),
            "preview_command": row["preview_command"],
            "review_command": row["command"],
        }
        mismatches = [
            f"{key}: expected={expected} found={resume.get(key, '')}"
            for key, expected in expected_values.items()
            if resume.get(key, "") != expected
        ]
        add_check(
            checks,
            f"session_{session:02d}_resume_counts",
            "ok" if not mismatches else "error",
            "resume matches plan and queue" if not mismatches else "; ".join(mismatches),
        )

    return checks


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, str]], output: Path, csv_path: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    issues = [row for row in rows if row["status"] != "ok"]
    lines = [
        "# Validation-200 v5 Review Packet Integrity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report validates that generated review session packets, the session",
        "plan, and the resume card still match the authoritative v5 review queue.",
        "",
        f"Machine-readable check: `{csv_path.relative_to(ROOT)}`.",
        "",
        "## Summary",
        "",
        f"- Checks: {len(rows)}",
        f"- Passing checks: {len(rows) - len(issues)}",
        f"- Issues: {len(issues)}",
        "",
    ]
    if issues:
        lines.extend(["## Issues", ""])
        for row in issues:
            lines.append(f"- `{row['check']}`: {row['detail']}")
        lines.append("")
    else:
        lines.extend(["No review packet integrity issues found.", ""])
    lines.extend(
        [
            "## Checks",
            "",
            "| Check | Status | Detail |",
            "| --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(f"| `{row['check']}` | `{row['status']}` | {row['detail']} |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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
        "--resume-csv",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_resume_card.csv",
    )
    parser.add_argument(
        "--packet-dir",
        type=Path,
        default=ROOT / "reports/validation200_v5_review_session_packets",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_packet_integrity.csv",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=ROOT / "reports/validation200_v5_review_packet_integrity.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = validate(
        read_csv(args.queue),
        read_csv(args.session_plan),
        read_csv(args.resume_csv),
        args.packet_dir,
    )
    write_csv(rows, args.output_csv)
    write_report(rows, args.output_md, args.output_csv)
    issues = [row for row in rows if row["status"] != "ok"]
    print(
        f"checks={len(rows)} issues={len(issues)} "
        f"report={args.output_md}"
    )
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
