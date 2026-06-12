#!/usr/bin/env python3
"""Rank validation-200 v5 review rows by likely thesis impact."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_DEV = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_TEST = ROOT / "data/slices/validation_200_v4_test150.jsonl"
DEFAULT_AGREEMENT = ROOT / "results/analysis/validation200_cross_script_answer_agreement_items.csv"
DEFAULT_OUTPUT = ROOT / "results/analysis/validation200_v5_review_impact_ranking.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_review_impact_ranking.md"
DEFAULT_IMPACT_PACKETS = ROOT / "reports/validation200_v5_review_packets_impact_order/README.md"

MODEL_KEYS = {
    "Qwen/Qwen2.5-3B-Instruct": "qwen25",
    "Qwen/Qwen3-4B-Instruct-2507": "qwen3",
}

PRIORITY_WEIGHT = {
    "both_wrong_multi_edit": 90,
    "both_wrong_single_edit": 85,
    "qwen25_wrong_multi_edit": 70,
    "qwen3_wrong_multi_edit": 70,
    "lower_priority": 25,
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_split_ids(path: Path, split: str) -> dict[str, str]:
    ids: dict[str, str] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            ids[str(row["id"])] = split
    return ids


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def read_agreement(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    out: dict[tuple[str, str], dict[str, str]] = {}
    if not path.exists():
        return out
    for row in load_csv(path):
        model_key = MODEL_KEYS.get(row.get("model", ""))
        if not model_key:
            continue
        out[(row["id"], model_key)] = row
    return out


def tier(score: int) -> str:
    if score >= 135:
        return "tier_1_review_first"
    if score >= 115:
        return "tier_2_high"
    if score >= 85:
        return "tier_3_medium"
    return "tier_4_low"


def model_impact(
    row: dict[str, str],
    agreement: dict[tuple[str, str], dict[str, str]],
    model_key: str,
) -> dict[str, bool]:
    v4_correct_key = "qwen25_v4_correct" if model_key == "qwen25" else "qwen3_v4_correct"
    agreement_row = agreement.get((row["id"], model_key), {})
    banglish_correct = parse_bool(agreement_row.get("banglish_correct", ""))
    route_correct = parse_bool(agreement_row.get("bangla_english_route_correct", ""))
    return {
        "v4_wrong": not parse_bool(row.get(v4_correct_key, "")),
        "cross_script_recoverable": parse_bool(
            agreement_row.get("banglish_wrong_other_correct", "")
        ),
        "agreement_route_gain": (not banglish_correct) and route_correct,
    }


def score_row(
    row: dict[str, str],
    split: str,
    agreement: dict[tuple[str, str], dict[str, str]],
) -> tuple[int, dict[str, Any], list[str]]:
    qwen25 = model_impact(row, agreement, "qwen25")
    qwen3 = model_impact(row, agreement, "qwen3")
    replacement_count = int(row.get("replacement_count", "0") or 0)
    priority = row.get("priority_bucket", "")

    score = PRIORITY_WEIGHT.get(priority, 0)
    reasons = [f"priority={priority}"]

    if split == "test":
        score += 18
        reasons.append("heldout_test150")
    elif split == "dev":
        score += 10
        reasons.append("dev50_tuning_slice")

    if row.get("dataset") == "benqa":
        score += 5
        reasons.append("main_benqa_gap_slice")

    for model_key, impact in [("qwen25", qwen25), ("qwen3", qwen3)]:
        if impact["v4_wrong"]:
            score += 8
            reasons.append(f"{model_key}_v4_wrong")
        if impact["cross_script_recoverable"]:
            score += 12
            reasons.append(f"{model_key}_recoverable_by_other_script")
        if impact["agreement_route_gain"]:
            score += 10
            reasons.append(f"{model_key}_agreement_route_gain")

    if replacement_count:
        edit_points = min(replacement_count, 8) * 2
        score += edit_points
        reasons.append(f"{replacement_count}_suggested_replacements")

    if "ksh_heavy" in row.get("artifact_patterns", ""):
        score += 4
        reasons.append("ksh_heavy")

    details: dict[str, Any] = {
        "qwen25_v4_wrong": qwen25["v4_wrong"],
        "qwen3_v4_wrong": qwen3["v4_wrong"],
        "qwen25_cross_script_recoverable": qwen25["cross_script_recoverable"],
        "qwen3_cross_script_recoverable": qwen3["cross_script_recoverable"],
        "qwen25_agreement_route_gain": qwen25["agreement_route_gain"],
        "qwen3_agreement_route_gain": qwen3["agreement_route_gain"],
    }
    return score, details, reasons


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit("No ranked rows to write.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def short_text(value: str, limit: int = 80) -> str:
    clean = " ".join(value.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def write_report(
    path: Path,
    queue_path: Path,
    output_path: Path,
    rows: list[dict[str, Any]],
) -> None:
    tier_counts = Counter(row["impact_tier"] for row in rows)
    split_counts = Counter(row["split"] for row in rows)
    priority_counts = Counter(row["priority_bucket"] for row in rows)

    lines = [
        "# Validation-200 v5 Review Impact Ranking",
        "",
        "Updated: 2026-05-28",
        "",
        "## Inputs",
        "",
        f"- Review queue: `{queue_path.relative_to(ROOT)}`",
        f"- Ranked CSV: `{output_path.relative_to(ROOT)}`",
        f"- Impact-ordered packets: `{DEFAULT_IMPACT_PACKETS.relative_to(ROOT)}`",
        f"- Rows ranked: {len(rows)}",
        "",
        "This ranking is for review triage only. It does not mark any row as",
        "correct, and it must not be used to auto-accept suggested Banglish edits.",
        "",
        "## Tier Counts",
        "",
        "| Tier | Rows |",
        "| --- | ---: |",
    ]
    for key, value in sorted(tier_counts.items()):
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Split Counts", "", "| Split | Rows |", "| --- | ---: |"])
    for key, value in split_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Priority Counts", "", "| Priority bucket | Rows |", "| --- | ---: |"])
    for key, value in priority_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(
        [
            "",
            "## Top 25 Rows",
            "",
            "| Rank | Score | Tier | Split | ID | Dataset | Priority | Repl | Model signals | Suggested edit sample |",
            "| ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in rows[:25]:
        model_signals = ", ".join(
            key
            for key in [
                "qwen25_v4_wrong",
                "qwen3_v4_wrong",
                "qwen25_cross_script_recoverable",
                "qwen3_cross_script_recoverable",
                "qwen25_agreement_route_gain",
                "qwen3_agreement_route_gain",
            ]
            if parse_bool(row[key])
        )
        lines.append(
            "| {rank} | {score} | `{tier}` | {split} | `{id}` | {dataset} | `{priority}` | {repl} | {signals} | {sample} |".format(
                rank=row["impact_rank"],
                score=row["impact_score"],
                tier=row["impact_tier"],
                split=row["split"],
                id=row["id"],
                dataset=row["dataset"],
                priority=row["priority_bucket"],
                repl=row["replacement_count"],
                signals=model_signals or "none",
                sample=short_text(str(row["suggestion_notes"])),
            )
        )

    lines.extend(
        [
            "",
            "## Suggested Review Order",
            "",
            "1. Review the impact-ordered packets first, especially held-out test150 rows in `tier_1_review_first`.",
            "2. Then review `tier_2_high` rows with repeated substitutions, checking Bangla and English source text side by side.",
            "3. Leave `tier_4_low` rows until the high-impact rows are resolved unless they share an obvious pattern already being reviewed.",
            "",
            "After editing the queue, run:",
            "",
            "```bash",
            "python3 scripts/validate_banglish_review_queue.py --require-complete",
            "```",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--dev", type=Path, default=DEFAULT_DEV)
    parser.add_argument("--test", type=Path, default=DEFAULT_TEST)
    parser.add_argument("--agreement", type=Path, default=DEFAULT_AGREEMENT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    split_by_id = {}
    split_by_id.update(load_split_ids(args.dev, "dev"))
    split_by_id.update(load_split_ids(args.test, "test"))
    agreement = read_agreement(args.agreement)

    ranked_rows: list[dict[str, Any]] = []
    for row in load_csv(args.queue):
        split = split_by_id.get(row["id"], "unknown")
        score, details, reasons = score_row(row, split, agreement)
        out_row: dict[str, Any] = {
            "impact_rank": 0,
            "impact_score": score,
            "impact_tier": tier(score),
            "split": split,
            "id": row["id"],
            "dataset": row["dataset"],
            "task_type": row["task_type"],
            "answer_type": row["answer_type"],
            "priority_bucket": row["priority_bucket"],
            "replacement_count": row["replacement_count"],
            **details,
            "impact_reasons": "; ".join(reasons),
            "artifact_patterns": row["artifact_patterns"],
            "suggestion_notes": row["suggestion_notes"],
            "current_banglish_clean": row["current_banglish_clean"],
            "auto_suggested_banglish_clean": row["auto_suggested_banglish_clean"],
            "quality_label": row.get("quality_label", ""),
            "review_notes": row.get("review_notes", ""),
        }
        ranked_rows.append(out_row)

    ranked_rows.sort(
        key=lambda row: (
            -int(row["impact_score"]),
            row["split"] != "test",
            row["dataset"],
            row["id"],
        )
    )
    for index, row in enumerate(ranked_rows, start=1):
        row["impact_rank"] = index

    write_csv(args.output, ranked_rows)
    write_report(args.report, args.queue, args.output, ranked_rows)
    print(f"ranked_rows={len(ranked_rows)}")
    print(f"report={args.report}")
    print(f"csv={args.output}")


if __name__ == "__main__":
    main()
