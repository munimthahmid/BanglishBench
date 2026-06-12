#!/usr/bin/env python3
"""Plan manageable validation-200 v5 human-review sessions."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUB_RE = re.compile(r"([A-Za-z0-9_.+-]+)->([A-Za-z0-9_.+-]+)")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def status(row: dict[str, str]) -> str:
    label = row.get("quality_label", "").strip()
    return label if label else "pending"


def row_substitutions(row: dict[str, str]) -> set[str]:
    return {
        f"{source}->{target}"
        for source, target in SUB_RE.findall(row.get("suggestion_notes", ""))
    }


def impact_rank(row_id: str, rank_by_id: dict[str, dict[str, str]]) -> int:
    raw = rank_by_id.get(row_id, {}).get("impact_rank", "")
    return int(raw) if raw.isdigit() else 999999


def split_substitution(substitution: str) -> tuple[str, str]:
    source, target = substitution.split("->", 1)
    return source, target


def helper_arg(substitution: str) -> str:
    source, target = split_substitution(substitution)
    return f"{source}:{target}"


def session_command(session_order: int) -> str:
    return f"python3 scripts/review_validation200_v5_queue.py --session {session_order}"


def chunked(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def build_sessions(
    queue_rows: list[dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
    session_size: int,
) -> list[dict[str, str]]:
    pending_rows = [row for row in queue_rows if status(row) == "pending"]
    row_by_id = {row["id"]: row for row in pending_rows}
    uncovered = set(row_by_id)
    rows_by_substitution: dict[str, set[str]] = defaultdict(set)

    for row in pending_rows:
        for substitution in row_substitutions(row):
            rows_by_substitution[substitution].add(row["id"])

    sessions: list[dict[str, str]] = []
    session_order = 0

    while uncovered:
        candidates: list[tuple[int, int, int, int, str, set[str]]] = []
        for substitution, row_ids in rows_by_substitution.items():
            new_ids = row_ids & uncovered
            if not new_ids:
                continue
            tier1 = sum(
                1
                for row_id in new_ids
                if rank_by_id.get(row_id, {}).get("impact_tier", "")
                == "tier_1_review_first"
            )
            test = sum(1 for row_id in new_ids if rank_by_id.get(row_id, {}).get("split", "") == "test")
            candidates.append((len(new_ids), tier1, test, len(row_ids), substitution, new_ids))

        if not candidates:
            ordered_fallback = sorted(uncovered, key=lambda row_id: (impact_rank(row_id, rank_by_id), row_id))
            for row_ids in chunked(ordered_fallback, session_size):
                session_order += 1
                command = session_command(session_order)
                sessions.append(
                    {
                        "session": str(session_order),
                        "substitution": "",
                        "helper_arg": "",
                        "planned_new_rows": str(len(row_ids)),
                        "tier1_rows": str(
                            sum(
                                1
                                for row_id in row_ids
                                if rank_by_id.get(row_id, {}).get("impact_tier", "")
                                == "tier_1_review_first"
                            )
                        ),
                        "test_rows": str(
                            sum(
                                1
                                for row_id in row_ids
                                if rank_by_id.get(row_id, {}).get("split", "") == "test"
                            )
                        ),
                        "command": command,
                        "preview_command": f"{command} --dry-run",
                        "row_ids": ";".join(row_ids),
                    }
                )
            break

        candidates.sort(key=lambda item: (-item[0], -item[1], -item[2], -item[3], item[4]))
        new_count, tier1_count, test_count, _total_count, substitution, new_ids = candidates[0]
        ordered_ids = sorted(new_ids, key=lambda row_id: (impact_rank(row_id, rank_by_id), row_id))
        for row_ids in chunked(ordered_ids, session_size):
            session_order += 1
            command = session_command(session_order)
            sessions.append(
                {
                    "session": str(session_order),
                    "substitution": substitution,
                    "helper_arg": helper_arg(substitution),
                    "planned_new_rows": str(len(row_ids)),
                    "tier1_rows": str(
                        sum(
                            1
                            for row_id in row_ids
                            if rank_by_id.get(row_id, {}).get("impact_tier", "")
                            == "tier_1_review_first"
                        )
                    ),
                    "test_rows": str(
                        sum(
                            1
                            for row_id in row_ids
                            if rank_by_id.get(row_id, {}).get("split", "") == "test"
                        )
                    ),
                    "command": command,
                    "preview_command": f"{command} --dry-run",
                    "row_ids": ";".join(row_ids),
                }
            )
        uncovered -= new_ids

    return sessions


def write_sessions_csv(path: Path, sessions: list[dict[str, str]]) -> None:
    fieldnames = [
        "session",
        "substitution",
        "helper_arg",
        "planned_new_rows",
        "tier1_rows",
        "test_rows",
        "command",
        "preview_command",
        "row_ids",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sessions)


def build_report(
    sessions: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    session_size: int,
) -> str:
    pending = sum(1 for row in queue_rows if status(row) == "pending")
    planned = sum(int(row["planned_new_rows"]) for row in sessions)
    planned_ids = [
        row_id
        for session in sessions
        for row_id in session["row_ids"].split(";")
        if row_id
    ]
    unique_planned = len(set(planned_ids))
    duplicate_planned = len(planned_ids) - unique_planned
    lines = [
        "# Validation-200 v5 Review Session Plan",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        f"Pending rows at planning time: `{pending}`.",
        f"Session size target: `{session_size}` rows.",
        f"Planned row slots: `{planned}`.",
        f"Unique row ids in plan: `{unique_planned}`.",
        f"Duplicate planned row ids: `{duplicate_planned}`.",
        "",
        "This plan is generated from the current pending queue and impact ranking.",
        "Each command uses the terminal helper's default behavior of skipping",
        "already reviewed rows, so repeated substitution sessions can be rerun",
        "after prior sessions are saved.",
        "",
        "## Session Commands",
        "",
        "| Session | Substitution | Planned new rows | Tier-1 rows | Test rows | Preview command | Review command |",
        "| ---: | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in sessions:
        substitution = f"`{row['substitution']}`" if row["substitution"] else "`fallback-impact-order`"
        lines.append(
            "| "
            f"{row['session']} | {substitution} | {row['planned_new_rows']} | "
            f"{row['tier1_rows']} | {row['test_rows']} | "
            f"`{row['preview_command']}` | `{row['command']}` |"
        )

    lines.extend(
        [
            "",
            "## Exact Row Ids",
            "",
        ]
    )
    for row in sessions:
        row_ids = ", ".join(f"`{row_id}`" for row_id in row["row_ids"].split(";") if row_id)
        lines.append(f"### Session {row['session']}")
        lines.append("")
        lines.append(f"- Substitution: `{row['substitution'] or 'fallback-impact-order'}`")
        lines.append(f"- Planned new rows: `{row['planned_new_rows']}`")
        lines.append(f"- Row ids: {row_ids}")
        lines.append("")

    lines.extend(
        [
            "## After Each Session",
            "",
            "1. Update `reports/validation200_v5_review_session_log.md`.",
            "2. Run `python3 scripts/summarize_v5_review_progress.py`.",
            "3. Run `python3 scripts/validate_banglish_review_queue.py`.",
            "4. Run `python3 scripts/check_post_v5_rerun_readiness.py`.",
            "",
        ]
    )
    return "\n".join(lines)


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
    parser.add_argument("--session-size", type=int, default=20)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/validation200_v5_review_session_plan.md",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_session_plan.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queue_rows = read_csv(args.queue)
    rank_rows = read_csv(args.ranking)
    rank_by_id = {row["id"]: row for row in rank_rows}
    sessions = build_sessions(queue_rows, rank_by_id, args.session_size)
    pending_ids = {row["id"] for row in queue_rows if status(row) == "pending"}
    planned_ids = {
        row_id
        for session in sessions
        for row_id in session["row_ids"].split(";")
        if row_id
    }
    if planned_ids != pending_ids:
        missing = sorted(pending_ids - planned_ids)
        unexpected = sorted(planned_ids - pending_ids)
        raise SystemExit(
            "session plan coverage mismatch: "
            f"missing={len(missing)} unexpected={len(unexpected)}"
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(sessions, queue_rows, args.session_size), encoding="utf-8")
    write_sessions_csv(args.csv_output, sessions)
    print(f"wrote={args.output}")
    print(f"wrote={args.csv_output}")
    print(f"sessions={len(sessions)} planned_rows={sum(int(row['planned_new_rows']) for row in sessions)}")


if __name__ == "__main__":
    main()
