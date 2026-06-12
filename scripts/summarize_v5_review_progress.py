#!/usr/bin/env python3
"""Summarize validation-200 v5 manual-review progress."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
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


def is_reviewed(row: dict[str, str]) -> bool:
    return bool(row.get("quality_label", "").strip())


def next_session_status(
    queue_rows: list[dict[str, str]],
    session_rows: list[dict[str, str]],
) -> tuple[dict[str, str], int, int] | None:
    queue_by_id = {row["id"]: row for row in queue_rows}
    for session in sorted(session_rows, key=lambda row: int(row["session"])):
        row_ids = [item for item in session.get("row_ids", "").split(";") if item]
        pending = [
            row_id
            for row_id in row_ids
            if row_id in queue_by_id and not is_reviewed(queue_by_id[row_id])
        ]
        if pending:
            return session, len(pending), len(row_ids)
    return None


def write_counter_table(lines: list[str], title: str, counter: Counter[str]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| Value | Rows |")
    lines.append("| --- | ---: |")
    for key, value in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")


def write_group_status_table(
    lines: list[str],
    title: str,
    groups: dict[str, Counter[str]],
) -> None:
    labels = ["pending", "ok", "minor_edit", "major_edit", "bad"]
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| Group | Total | Pending | ok | minor_edit | major_edit | bad |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for group, counter in sorted(
        groups.items(), key=lambda item: (-sum(item[1].values()), item[0])
    ):
        total = sum(counter.values())
        values = [counter.get(label, 0) for label in labels]
        lines.append(
            f"| `{group}` | {total} | {values[0]} | {values[1]} | "
            f"{values[2]} | {values[3]} | {values[4]} |"
        )
    lines.append("")


def substitution_counts(rows: list[dict[str, str]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        if status(row) != "pending":
            continue
        for substitution in row_substitutions(row):
            counter[substitution] += 1
    return counter


def row_substitutions(row: dict[str, str]) -> set[str]:
    return {
        f"{source}->{target}"
        for source, target in SUB_RE.findall(row.get("suggestion_notes", ""))
    }


def status_groups(
    queue_rows: list[dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
) -> tuple[Counter[str], dict[str, Counter[str]], dict[str, Counter[str]], dict[str, Counter[str]]]:
    status_counts = Counter(status(row) for row in queue_rows)
    by_tier: dict[str, Counter[str]] = defaultdict(Counter)
    by_split: dict[str, Counter[str]] = defaultdict(Counter)
    by_priority: dict[str, Counter[str]] = defaultdict(Counter)

    for row in queue_rows:
        row_status = status(row)
        rank = rank_by_id.get(row["id"], {})
        by_tier[rank.get("impact_tier", "unranked")][row_status] += 1
        by_split[rank.get("split", "unknown")][row_status] += 1
        by_priority[row.get("priority_bucket", "unknown")][row_status] += 1

    return status_counts, by_tier, by_split, by_priority


def pending_substitution_coverage(
    queue_rows: list[dict[str, str]],
    substitutions: list[str],
) -> list[tuple[str, int, int, int]]:
    pending_rows = [row for row in queue_rows if status(row) == "pending"]
    covered: set[str] = set()
    rows_by_substitution: dict[str, set[str]] = defaultdict(set)
    for row in pending_rows:
        for substitution in row_substitutions(row):
            rows_by_substitution[substitution].add(row["id"])

    coverage: list[tuple[str, int, int, int]] = []
    for substitution in substitutions:
        matching = rows_by_substitution.get(substitution, set())
        new_ids = matching - covered
        covered.update(matching)
        coverage.append((substitution, len(matching), len(new_ids), len(covered)))
    return coverage


def progress_table_rows(
    status_counts: Counter[str],
    by_tier: dict[str, Counter[str]],
    by_split: dict[str, Counter[str]],
    by_priority: dict[str, Counter[str]],
) -> list[dict[str, str]]:
    labels = ["pending", "ok", "minor_edit", "major_edit", "bad"]
    rows: list[dict[str, str]] = []

    def add(dimension: str, group: str, counter: Counter[str]) -> None:
        total = sum(counter.values())
        out = {"dimension": dimension, "group": group, "total": str(total)}
        out.update({label: str(counter.get(label, 0)) for label in labels})
        rows.append(out)

    add("overall", "all", status_counts)
    for group, counter in sorted(by_tier.items()):
        add("impact_tier", group, counter)
    for group, counter in sorted(by_split.items()):
        add("split", group, counter)
    for group, counter in sorted(by_priority.items()):
        add("priority_bucket", group, counter)
    return rows


def write_progress_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["dimension", "group", "total", "pending", "ok", "minor_edit", "major_edit", "bad"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_report(
    queue_rows: list[dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
    session_rows: list[dict[str, str]],
) -> str:
    status_counts, by_tier, by_split, by_priority = status_groups(queue_rows, rank_by_id)
    pending_substitutions = substitution_counts(queue_rows)
    top_substitutions = [substitution for substitution, _count in pending_substitutions.most_common(12)]
    coverage = pending_substitution_coverage(queue_rows, top_substitutions)
    lines = [
        "# Validation-200 v5 Review Progress",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report summarizes manual-review progress for",
        "`data/slices/validation_200_v5_review_queue.csv`.",
        "",
    ]
    write_counter_table(lines, "Overall Status", status_counts)
    write_group_status_table(lines, "By Impact Tier", by_tier)
    write_group_status_table(lines, "By Split", by_split)
    write_group_status_table(lines, "By Priority Bucket", by_priority)
    lines.append("## Top Pending Substitutions")
    lines.append("")
    lines.append("| Substitution | Pending rows | Helper command |")
    lines.append("| --- | ---: | --- |")
    for substitution, count in pending_substitutions.most_common(12):
        helper_arg = substitution.replace("->", ":")
        lines.append(
            "| "
            f"`{substitution}` | {count} | "
            f"`python3 scripts/review_validation200_v5_queue.py --substitution {helper_arg}` |"
        )
    lines.append("")
    lines.append("## Top Substitution Batch Coverage")
    lines.append("")
    lines.append(
        "Rows overlap across substitutions. This table estimates unique pending-row"
    )
    lines.append("coverage if the top substitutions are reviewed in the listed order.")
    lines.append("")
    lines.append("| Order | Substitution | Matching rows | New rows | Cumulative rows |")
    lines.append("| ---: | --- | ---: | ---: | ---: |")
    for order, (substitution, matching, new_rows, cumulative) in enumerate(coverage, start=1):
        lines.append(
            f"| {order} | `{substitution}` | {matching} | {new_rows} | {cumulative} |"
        )
    lines.append("")
    lines.append("## Next Command")
    lines.append("")
    if status_counts.get("pending", 0):
        next_session = next_session_status(queue_rows, session_rows)
        lines.append("```bash")
        if next_session:
            session, _pending, _total = next_session
            lines.append(session["preview_command"])
            lines.append(session["command"])
        else:
            lines.append("python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run")
            lines.append("python3 scripts/review_validation200_v5_queue.py --session 1")
        lines.append("```")
        lines.append("")
        if next_session:
            session, pending, total = next_session
            lines.append(
                f"Next incomplete session: `{session['session']}` "
                f"(`{session['substitution']}`), {pending}/{total} rows pending."
            )
            lines.append("")
        lines.append("Regenerate exact sessions with:")
        lines.append("")
        lines.append("```bash")
        lines.append("python3 scripts/plan_v5_review_sessions.py")
        lines.append("python3 scripts/export_v5_review_resume_card.py")
        lines.append("```")
    else:
        lines.append("```bash")
        lines.append("python3 scripts/validate_banglish_review_queue.py --require-complete")
        lines.append("```")
    lines.append("")
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
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/validation200_v5_review_progress.md",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_progress_summary.csv",
    )
    parser.add_argument(
        "--session-plan",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_session_plan.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queue_rows = read_csv(args.queue)
    rank_rows = read_csv(args.ranking)
    session_rows = read_csv(args.session_plan) if args.session_plan.exists() else []
    rank_by_id = {row["id"]: row for row in rank_rows}
    report = build_report(queue_rows, rank_by_id, session_rows)
    status_counts, by_tier, by_split, by_priority = status_groups(queue_rows, rank_by_id)
    progress_rows = progress_table_rows(status_counts, by_tier, by_split, by_priority)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    write_progress_csv(args.csv_output, progress_rows)
    print(f"wrote={args.output}")
    print(f"wrote={args.csv_output}")


if __name__ == "__main__":
    main()
