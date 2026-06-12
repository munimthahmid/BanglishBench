#!/usr/bin/env python3
"""Export a batch-review playbook for repeated v5 Banglish substitutions."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def clip(text: str, limit: int = 260) -> str:
    value = " ".join((text or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def md_code_cell(text: str) -> str:
    return clip(text).replace("|", r"\|").replace("`", "'")


def yes_no(value: str) -> str:
    return "yes" if value.strip().lower() == "true" else "no"


def index_by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["id"]: row for row in rows}


def contains_substitution(row: dict[str, str], source: str, target: str) -> bool:
    needle = f"{source}->{target}"
    return needle in row.get("suggestion_notes", "")


def row_matches_substitution(row: dict[str, str], source: str, target: str) -> bool:
    return contains_substitution(row, source, target)


def batch_coverage(
    summary_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    top_substitutions: int,
) -> list[tuple[int, str, int, int, int]]:
    covered: set[str] = set()
    rows_by_substitution: dict[str, set[str]] = {}
    for row in summary_rows[:top_substitutions]:
        source = row["source"]
        target = row["target"]
        substitution = f"{source}->{target}"
        rows_by_substitution[substitution] = {
            queue_row["id"]
            for queue_row in queue_rows
            if row_matches_substitution(queue_row, source, target)
        }

    out: list[tuple[int, str, int, int, int]] = []
    for order, row in enumerate(summary_rows[:top_substitutions], start=1):
        substitution = f"{row['source']}->{row['target']}"
        matching = rows_by_substitution[substitution]
        new_rows = matching - covered
        covered.update(matching)
        out.append((order, substitution, len(matching), len(new_rows), len(covered)))
    return out


def sort_by_pending_coverage(
    summary_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    def pending_count(row: dict[str, str]) -> int:
        source = row["source"]
        target = row["target"]
        return sum(
            1 for queue_row in queue_rows if row_matches_substitution(queue_row, source, target)
        )

    return sorted(
        summary_rows,
        key=lambda row: (
            -pending_count(row),
            -int(row.get("tier1_rows", "0") or 0),
            -int(row.get("test_rows", "0") or 0),
            row["source"],
            row["target"],
        ),
    )


def write_example(
    lines: list[str],
    rank_row: dict[str, str],
    queue_row: dict[str, str],
    index: int,
) -> None:
    lines.append(f"#### Example {index}: `{rank_row['id']}`")
    lines.append("")
    lines.append(
        "- "
        f"Split: `{rank_row['split']}`; tier: `{rank_row['impact_tier']}`; "
        f"impact score: `{rank_row['impact_score']}`; "
        f"priority: `{rank_row['priority_bucket']}`"
    )
    lines.append(
        "- "
        f"Qwen2.5 wrong: `{yes_no(rank_row['qwen25_v4_wrong'])}`; "
        f"Qwen3 wrong: `{yes_no(rank_row['qwen3_v4_wrong'])}`; "
        f"Qwen2.5 recoverable: `{yes_no(rank_row['qwen25_cross_script_recoverable'])}`; "
        f"Qwen3 recoverable: `{yes_no(rank_row['qwen3_cross_script_recoverable'])}`"
    )
    lines.append(f"- Suggested edits: `{queue_row.get('suggestion_notes', '')}`")
    lines.append("")
    lines.append("| Field | Text |")
    lines.append("| --- | --- |")
    lines.append(f"| Current Banglish | `{md_code_cell(queue_row.get('current_banglish_clean', ''))}` |")
    lines.append(
        f"| Suggested Banglish | `{md_code_cell(queue_row.get('auto_suggested_banglish_clean', ''))}` |"
    )
    lines.append(f"| Bangla source | `{md_code_cell(queue_row.get('bangla', ''))}` |")
    lines.append(f"| English source | `{md_code_cell(queue_row.get('english', ''))}` |")
    lines.append("")
    lines.append("Review decision:")
    lines.append("")
    lines.append("- Accept only if the suggested wording preserves the Bangla/English meaning.")
    lines.append("- Edit manually if the repeated substitution is correct but another word is still awkward.")
    lines.append("- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.")
    lines.append("")


def build_playbook(
    summary_rows: list[dict[str, str]],
    ranking_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
    top_substitutions: int,
    examples_per_substitution: int,
) -> str:
    queue_by_id = index_by_id(queue_rows)
    coverage = batch_coverage(summary_rows, queue_rows, top_substitutions)
    lines = [
        "# Validation-200 v5 Substitution Review Playbook",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This playbook turns the repeated substitution summary into a practical",
        "human-review sequence. It is not an auto-accept list; every row must still",
        "be checked against the Bangla and English source views.",
        "",
        "## Inputs",
        "",
        "- `data/slices/validation_200_v5_review_queue.csv`",
        "- `results/analysis/validation200_v5_review_impact_ranking.csv`",
        "- `results/analysis/validation200_v5_review_impact_substitutions.csv`",
        "",
        "## Batch Review Order",
        "",
        "The order prioritizes current pending-row coverage, then tier-1 and",
        "held-out test coverage. Impact scores are still shown so high-value rows",
        "remain visible during review.",
        "",
        "| Order | Substitution | Rows | Tier-1 rows | Test rows | Mean score | First examples |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for order, row in enumerate(summary_rows[:top_substitutions], start=1):
        lines.append(
            "| "
            f"{order} | `{row['source']}` -> `{row['target']}` | "
            f"{row['rows']} | {row['tier1_rows']} | {row['test_rows']} | "
            f"{row['mean_impact_score']} | {row['example_ids']} |"
        )

    lines.extend(
        [
            "",
            "## Review Rules",
            "",
            "- Work substitution groups in the order above, but write decisions row by row.",
            "- Repeated edit patterns are evidence for review efficiency, not authority.",
            "- Prefer the shortest natural Banglish spelling that preserves the source meaning.",
            "- Keep MCQ option labels and answer-only instructions unchanged.",
            "- Do not normalize domain terms so aggressively that a real Banglish reader would",
            "  see a different word.",
            "",
            "## Batch Coverage",
            "",
            "Rows overlap across substitutions. The cumulative column estimates how many",
            "unique queue rows are reached if groups are reviewed in this order.",
            "",
            "| Order | Substitution | Matching rows | New rows | Cumulative rows |",
            "| ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for order, substitution, matching, new_rows, cumulative in coverage:
        lines.append(
            f"| {order} | `{substitution}` | {matching} | {new_rows} | {cumulative} |"
        )

    lines.extend(
        [
            "",
            "## Terminal Helper Shortcuts",
            "",
            "Review one repeated substitution group interactively:",
            "",
            "```bash",
            "python3 scripts/review_validation200_v5_queue.py --substitution konoti:konti",
            "```",
            "",
            "Combine it with the impact tier filter:",
            "",
            "```bash",
            "python3 scripts/review_validation200_v5_queue.py --tier tier_1_review_first --substitution kot:koto",
            "```",
            "",
            "## Substitution Packets",
            "",
        ]
    )

    for row in summary_rows[:top_substitutions]:
        source = row["source"]
        target = row["target"]
        matching = [
            rank_row
            for rank_row in ranking_rows
            if contains_substitution(rank_row, source, target)
        ]
        matching.sort(
            key=lambda item: (
                0 if item["impact_tier"] == "tier_1_review_first" else 1,
                0 if item["split"] == "test" else 1,
                -int(item["impact_score"]),
                item["id"],
            )
        )

        lines.append(f"### `{source}` -> `{target}`")
        lines.append("")
        lines.append(
            f"Rows: `{row['rows']}`; occurrences: `{row['occurrences']}`; "
            f"tier-1 rows: `{row['tier1_rows']}`; test rows: `{row['test_rows']}`."
        )
        lines.append("")
        if not matching:
            lines.append("No matching rows found in the impact ranking.")
            lines.append("")
            continue
        for index, rank_row in enumerate(matching[:examples_per_substitution], start=1):
            queue_row = queue_by_id.get(rank_row["id"], {})
            write_example(lines, rank_row, queue_row, index)

    lines.extend(
        [
            "## Completion Check",
            "",
            "After a review session:",
            "",
            "1. Save the edited CSV.",
            "2. Run `python3 scripts/validate_banglish_review_queue.py --require-complete`",
            "   only when all rows are filled.",
            "3. Run `python3 scripts/validate_banglish_review_queue.py` during partial",
            "   sessions to catch formatting errors without failing on pending rows.",
            "4. Record accepted/rejected/bad counts in",
            "   `reports/validation200_v5_review_session_log.md`.",
            "5. Record final accepted/rejected/bad counts in the research log before",
            "   freezing v5.",
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
    parser.add_argument(
        "--substitutions",
        type=Path,
        default=ROOT / "results/analysis/validation200_v5_review_impact_substitutions.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/validation200_v5_substitution_review_playbook.md",
    )
    parser.add_argument("--top-substitutions", type=int, default=10)
    parser.add_argument("--examples-per-substitution", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_rows = read_csv(args.substitutions)
    ranking_rows = read_csv(args.ranking)
    queue_rows = read_csv(args.queue)
    summary_rows = sort_by_pending_coverage(summary_rows, queue_rows)
    markdown = build_playbook(
        summary_rows,
        ranking_rows,
        queue_rows,
        args.top_substitutions,
        args.examples_per_substitution,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
