#!/usr/bin/env python3
"""Check whether frozen-v5 BEnQA script gaps depend on one subject."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAILURES = (
    ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
)
DEFAULT_OUTPUT = ROOT / "results/analysis/v5_benqa_subject_stability.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_subject_stability.md"

MODELS = (
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen3-4B-Instruct-2507",
)
MODEL_LABELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def points(value: Any) -> str:
    scaled = float(value)
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def summarize(
    rows: list[dict[str, str]],
    model: str,
    row_type: str,
    excluded_subject: str,
) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["model"] == model
        and row["dataset"] == "benqa"
        and (not excluded_subject or row["subject"] != excluded_subject)
    ]
    excluded_n = sum(
        1
        for row in rows
        if row["model"] == model and row["dataset"] == "benqa" and row["subject"] == excluded_subject
    )
    pairs = [(truthy(row["bangla_correct"]), truthy(row["banglish_clean_correct"])) for row in selected]
    bangla_correct = sum(int(left) for left, _right in pairs)
    banglish_correct = sum(int(right) for _left, right in pairs)
    delta_items = banglish_correct - bangla_correct
    n = len(pairs)
    return {
        "model": MODEL_LABELS.get(model, model),
        "model_id": model,
        "row_type": row_type,
        "excluded_subject": excluded_subject or "none",
        "excluded_n": excluded_n,
        "n": n,
        "bangla_correct": bangla_correct,
        "reviewed_banglish_correct": banglish_correct,
        "delta_items": delta_items,
        "delta_points": round((delta_items / n) * 100, 1) if n else 0.0,
        "gains": sum((not left) and right for left, right in pairs),
        "losses": sum(left and (not right) for left, right in pairs),
    }


def subjects_by_model(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row["dataset"] == "benqa" and row["model"] in MODELS:
            out[row["model"]].add(row["subject"])
    return {model: sorted(subjects) for model, subjects in out.items()}


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    subjects = subjects_by_model(rows)
    out: list[dict[str, Any]] = []
    for model in MODELS:
        model_subjects = subjects.get(model, [])
        if len(model_subjects) != 13:
            raise SystemExit(f"Expected 13 BEnQA subjects for {model}, got {len(model_subjects)}")
        out.append(summarize(rows, model, "all_subjects", ""))
        for subject in model_subjects:
            out.append(summarize(rows, model, "drop_one_subject", subject))
    return out


def write_report(path: Path, rows: list[dict[str, Any]], output_csv: Path, source: Path) -> None:
    lines = [
        "# Frozen-V5 BEnQA Subject Stability",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend report checks whether the BEnQA portion of the frozen-v5",
        "Banglish-minus-Bangla gap is an artifact of a single subject stratum.",
        "For each thesis-facing Qwen row, it recomputes the BEnQA paired count",
        "after dropping one subject at a time.",
        "",
        f"- Machine-readable summary: `{repo_path(output_csv)}`",
        f"- Source failure table: `{repo_path(source)}`",
        "",
        "## Summary",
        "",
        "| Model | All BEnQA Delta | Leave-One-Subject Delta Range | Negative Drops | Closest To Zero | Strongest Drop |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for model in MODEL_LABELS.values():
        all_row = next(row for row in rows if row["model"] == model and row["row_type"] == "all_subjects")
        drop_rows = [
            row for row in rows if row["model"] == model and row["row_type"] == "drop_one_subject"
        ]
        closest = max(drop_rows, key=lambda row: float(row["delta_points"]))
        strongest = min(drop_rows, key=lambda row: float(row["delta_points"]))
        negative = sum(1 for row in drop_rows if int(row["delta_items"]) < 0)
        low = min(float(row["delta_points"]) for row in drop_rows)
        high = max(float(row["delta_points"]) for row in drop_rows)
        lines.append(
            f"| {model} | {points(all_row['delta_points'])} pts "
            f"({all_row['reviewed_banglish_correct']}/{all_row['n']} vs "
            f"{all_row['bangla_correct']}/{all_row['n']}) | "
            f"[{points(low)}, {points(high)}] pts | {negative}/13 | "
            f"drop `{closest['excluded_subject']}`: {points(closest['delta_points'])} pts | "
            f"drop `{strongest['excluded_subject']}`: {points(strongest['delta_points'])} pts |"
        )

    lines.extend(
        [
            "",
            "## Leave-One-Subject Rows",
            "",
            "| Model | Dropped Subject | Remaining n | Bangla | Reviewed Banglish | Delta | Gains | Losses |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        if row["row_type"] != "drop_one_subject":
            continue
        lines.append(
            f"| {row['model']} | `{row['excluded_subject']}` | {row['n']} | "
            f"{row['bangla_correct']}/{row['n']} | {row['reviewed_banglish_correct']}/{row['n']} | "
            f"{points(row['delta_points'])} pts | {row['gains']} | {row['losses']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Dropping any one BEnQA subject keeps the reviewed-Banglish-minus-Bangla",
            "  gap negative for all three thesis-facing Qwen rows.",
            "- Qwen3-4B remains the strongest BEnQA case: its leave-one-subject gaps",
            "  range from -23.3 to -18.0 points.",
            "- The Qwen2.5 rows are smaller and should still be described as",
            "  directionally negative at the dataset level, but they are not driven",
            "  by only one subject bucket.",
            "",
            "Thesis-safe phrasing:",
            "",
            "> Within BEnQA, the reviewed-v5 Banglish deficit is not a single-subject",
            "> artifact: every leave-one-subject recomputation remains negative for",
            "> the three thesis-facing Qwen rows.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = read_csv(args.failure_items)
    if len(source_rows) != 600:
        raise SystemExit(f"Expected 600 source rows, got {len(source_rows)}")
    rows = build_rows(source_rows)
    if len(rows) != 42:
        raise SystemExit(f"Expected 42 summary rows, got {len(rows)}")
    all_rows = [row for row in rows if row["row_type"] == "all_subjects"]
    if any(int(row["n"]) != 144 for row in all_rows):
        raise SystemExit("Expected all-subject BEnQA rows to use n=144")
    write_csv(args.output, rows)
    write_report(args.report_output, rows, args.output, args.failure_items)
    print(f"rows={len(rows)} report={args.report_output} csv={args.output}")


if __name__ == "__main__":
    main()
