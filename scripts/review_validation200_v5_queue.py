#!/usr/bin/env python3
"""Interactive helper for manually reviewing validation-200 v5 Banglish rows."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_RANKING = ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv"
DEFAULT_SESSION_PLAN = ROOT / "results/analysis/validation200_v5_review_session_plan.csv"
VALID_LABELS = {"ok", "minor_edit", "major_edit", "bad"}
SUB_RE = re.compile(r"([A-Za-z0-9_.+-]+)->([A-Za-z0-9_.+-]+)")


def load_csv_with_fields(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def load_rank(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def load_session_ids(path: Path, session: int) -> list[str]:
    if not path.exists():
        raise SystemExit(f"Session plan not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("session") == str(session):
                return [row_id for row_id in row.get("row_ids", "").split(";") if row_id]
    raise SystemExit(f"Session {session} not found in {path}")


def write_queue(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in fieldnames} for row in rows)


def normalize_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def matches_substitution(row: dict[str, str], substitution: str) -> bool:
    if ":" in substitution:
        source, target = substitution.split(":", 1)
        needle = f"{source.strip()}->{target.strip()}"
    else:
        needle = substitution.strip()
    return bool(needle) and needle in row.get("suggestion_notes", "")


def row_substitutions(row: dict[str, str]) -> list[str]:
    return [
        f"{source}->{target}"
        for source, target in SUB_RE.findall(row.get("suggestion_notes", ""))
    ]


def section(title: str, text: str) -> str:
    return f"\n{title}\n{'-' * len(title)}\n{text.rstrip()}\n"


def display_row(row: dict[str, str], rank: dict[str, str], position: int, total: int) -> None:
    print("\n" + "=" * 88)
    print(f"{position}/{total}  {row['id']}")
    print("=" * 88)
    print(f"Dataset: {row['dataset']} | Task: {row['task_type']} | Answer type: {row['answer_type']}")
    print(f"Priority: {row['priority_bucket']} | Replacement count: {row['replacement_count']}")
    print(f"Qwen2.5 v4 correct: {row['qwen25_v4_correct']} | Qwen3 v4 correct: {row['qwen3_v4_correct']}")
    if rank:
        print(
            "Impact: rank {rank}, tier {tier}, score {score}, split {split}".format(
                rank=rank.get("impact_rank", ""),
                tier=rank.get("impact_tier", ""),
                score=rank.get("impact_score", ""),
                split=rank.get("split", ""),
            )
        )
        print(f"Reasons: {rank.get('impact_reasons', '')}")
    print(f"Suggestions: {row['suggestion_notes']}")
    print(section("Bangla", row["bangla"]))
    print(section("English", row["english"]))
    print(section("Current Banglish", row["current_banglish_clean"]))
    print(section("Auto-suggested Banglish", row["auto_suggested_banglish_clean"]))
    if row.get("reviewed_banglish") or row.get("quality_label") or row.get("review_notes"):
        print(section("Existing Review", f"label={row.get('quality_label', '')}\nreviewed={row.get('reviewed_banglish', '')}\nnotes={row.get('review_notes', '')}"))


def print_match_summary(
    rows: list[dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
) -> None:
    print(
        "order,id,impact_rank,impact_tier,split,dataset,task_type,"
        "priority_bucket,replacement_count,quality_label,substitutions"
    )
    for position, row in enumerate(rows, start=1):
        rank = rank_by_id.get(row["id"], {})
        substitutions = ";".join(row_substitutions(row))
        print(
            ",".join(
                [
                    str(position),
                    row["id"],
                    rank.get("impact_rank", ""),
                    rank.get("impact_tier", ""),
                    rank.get("split", ""),
                    row.get("dataset", ""),
                    row.get("task_type", ""),
                    row.get("priority_bucket", ""),
                    row.get("replacement_count", ""),
                    row.get("quality_label", ""),
                    substitutions,
                ]
            )
        )


def export_matches(
    path: Path,
    rows: list[dict[str, str]],
    rank_by_id: dict[str, dict[str, str]],
) -> None:
    fieldnames = [
        "match_order",
        "id",
        "impact_rank",
        "impact_tier",
        "split",
        "impact_score",
        "impact_reasons",
        "dataset",
        "task_type",
        "answer_type",
        "priority_bucket",
        "replacement_count",
        "quality_label",
        "reviewed_banglish",
        "review_notes",
        "substitutions",
        "suggestion_notes",
        "bangla",
        "english",
        "current_banglish_clean",
        "auto_suggested_banglish_clean",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for position, row in enumerate(rows, start=1):
            rank = rank_by_id.get(row["id"], {})
            writer.writerow(
                {
                    "match_order": position,
                    "id": row["id"],
                    "impact_rank": rank.get("impact_rank", ""),
                    "impact_tier": rank.get("impact_tier", ""),
                    "split": rank.get("split", ""),
                    "impact_score": rank.get("impact_score", ""),
                    "impact_reasons": rank.get("impact_reasons", ""),
                    "dataset": row.get("dataset", ""),
                    "task_type": row.get("task_type", ""),
                    "answer_type": row.get("answer_type", ""),
                    "priority_bucket": row.get("priority_bucket", ""),
                    "replacement_count": row.get("replacement_count", ""),
                    "quality_label": row.get("quality_label", ""),
                    "reviewed_banglish": row.get("reviewed_banglish", ""),
                    "review_notes": row.get("review_notes", ""),
                    "substitutions": ";".join(row_substitutions(row)),
                    "suggestion_notes": row.get("suggestion_notes", ""),
                    "bangla": row.get("bangla", ""),
                    "english": row.get("english", ""),
                    "current_banglish_clean": row.get("current_banglish_clean", ""),
                    "auto_suggested_banglish_clean": row.get(
                        "auto_suggested_banglish_clean", ""
                    ),
                }
            )


def prompt_label() -> str:
    while True:
        raw = input("Label [ok/minor_edit/major_edit/bad, Enter=skip, q=quit]: ").strip()
        if raw in {"", "q", "quit"}:
            return raw
        if raw in VALID_LABELS:
            return raw
        print("Invalid label.")


def prompt_replacement(label: str, suggestion: str) -> str:
    if label in {"ok", "bad"}:
        return ""
    while True:
        print("Replacement is required for minor_edit/major_edit.")
        print("Press Enter to use the auto-suggested Banglish shown above.")
        replacement = input("Reviewed Banglish: ")
        replacement = suggestion if not replacement.strip() else replacement
        if replacement.strip():
            return replacement
        print("Replacement cannot be blank for this label.")


def prompt_notes(label: str) -> str:
    while True:
        notes = input("Review notes [optional]: ").strip()
        if label != "bad" or notes:
            return notes
        print("A short note is required for bad rows.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--ranking", type=Path, default=DEFAULT_RANKING)
    parser.add_argument("--session-plan", type=Path, default=DEFAULT_SESSION_PLAN)
    parser.add_argument(
        "--session",
        type=int,
        help="Review one exact session from the generated v5 review session plan.",
    )
    parser.add_argument("--tier", help="Optional impact tier filter.")
    parser.add_argument("--id", help="Review one specific item id.")
    parser.add_argument(
        "--substitution",
        help="Filter rows by suggested substitution, e.g. konoti:konti or konoti->konti.",
    )
    parser.add_argument(
        "--suggestion-contains",
        help="Filter rows whose suggestion_notes contain this exact text.",
    )
    parser.add_argument("--limit", type=int, help="Maximum rows to show.")
    parser.add_argument("--all", action="store_true", help="Include already reviewed rows.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a .bak file before the first write.")
    parser.add_argument(
        "--list-ids",
        action="store_true",
        help="Print matching row ids and exit without prompting or writing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print a compact CSV-style summary of matching rows and exit without writing.",
    )
    parser.add_argument(
        "--export-matches",
        type=Path,
        help="Write matching rows plus impact metadata to a CSV and exit without editing the queue.",
    )
    args = parser.parse_args()
    if args.session is not None and any(
        [args.id, args.tier, args.substitution, args.suggestion_contains]
    ):
        parser.error("--session cannot be combined with --id, --tier, --substitution, or --suggestion-contains")

    queue_path = normalize_path(args.queue)
    ranking_path = normalize_path(args.ranking)
    session_plan_path = normalize_path(args.session_plan)
    rows, fieldnames = load_csv_with_fields(queue_path)
    rank_by_id = load_rank(ranking_path)

    if args.session is not None:
        row_by_id = {row["id"]: row for row in rows}
        ordered = [
            row_by_id[row_id]
            for row_id in load_session_ids(session_plan_path, args.session)
            if row_id in row_by_id
        ]
    else:
        ordered = list(rows)
        ordered.sort(
            key=lambda row: int(rank_by_id.get(row["id"], {}).get("impact_rank", "999999"))
        )
    if args.id:
        ordered = [row for row in ordered if row["id"] == args.id]
    if args.tier:
        ordered = [
            row
            for row in ordered
            if rank_by_id.get(row["id"], {}).get("impact_tier", "") == args.tier
        ]
    if args.substitution:
        ordered = [row for row in ordered if matches_substitution(row, args.substitution)]
    if args.suggestion_contains:
        ordered = [
            row for row in ordered if args.suggestion_contains in row.get("suggestion_notes", "")
        ]
    if not args.all:
        ordered = [row for row in ordered if not row.get("quality_label", "").strip()]
    if args.limit is not None:
        ordered = ordered[: args.limit]

    if not ordered:
        print("No rows matched.")
        return

    if args.list_ids:
        for row in ordered:
            print(row["id"])
        return

    if args.dry_run:
        print_match_summary(ordered, rank_by_id)
        return

    if args.export_matches:
        export_path = normalize_path(args.export_matches)
        export_matches(export_path, ordered, rank_by_id)
        print(f"wrote={export_path} rows={len(ordered)}")
        return

    backup_written = False
    for position, row in enumerate(ordered, start=1):
        rank = rank_by_id.get(row["id"], {})
        display_row(row, rank, position, len(ordered))
        label = prompt_label()
        if label in {"q", "quit"}:
            break
        if not label:
            continue
        replacement = prompt_replacement(label, row["auto_suggested_banglish_clean"])
        notes = prompt_notes(label)
        confirm = input(f"Save label={label!r} for {row['id']}? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Skipped save.")
            continue

        row["quality_label"] = label
        row["reviewed_banglish"] = replacement
        row["review_notes"] = notes
        if not backup_written and not args.no_backup:
            backup_path = queue_path.with_suffix(queue_path.suffix + ".bak")
            shutil.copy2(queue_path, backup_path)
            print(f"Backup written: {backup_path}")
            backup_written = True
        write_queue(queue_path, rows, fieldnames)
        print("Saved. Run validate_banglish_review_queue.py after the review session.")


if __name__ == "__main__":
    main()
