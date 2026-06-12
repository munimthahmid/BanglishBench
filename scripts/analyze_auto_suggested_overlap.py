#!/usr/bin/env python3
"""Analyze how auto-suggested Banglish edits overlap existing model outcomes."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
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


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def changed_field_set(row: dict[str, Any]) -> set[str]:
    meta = row.get("banglish_auto_suggestion") or {}
    return set(meta.get("changed_fields") or [])


def summarize_model(
    model_name: str,
    rows: list[dict[str, str]],
    changed_ids: set[str],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    buckets = {
        "auto_changed": [row for row in rows if row["id"] in changed_ids],
        "auto_unchanged": [row for row in rows if row["id"] not in changed_ids],
        "all": rows,
    }
    for bucket, items in buckets.items():
        changes = Counter(row["change"] for row in items)
        before_correct = sum(truthy(row["before_correct"]) for row in items)
        after_correct = sum(truthy(row["after_correct"]) for row in items)
        out.append(
            {
                "model": model_name,
                "bucket": bucket,
                "n": len(items),
                "v3_correct": before_correct,
                "v4_correct": after_correct,
                "v4_minus_v3_correct": after_correct - before_correct,
                "same_correct": changes["same_correct"],
                "same_wrong": changes["same_wrong"],
                "gain": changes["gain"],
                "loss": changes["loss"],
                "v4_wrong_items": len(items) - after_correct,
            }
        )
    return out


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    changed_ids: set[str],
    clean_changed_ids: set[str],
    noisy_changed_ids: set[str],
    qwen25_compare: Path,
    qwen3_compare: Path,
    summary_output: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_model = {(row["model"], row["bucket"]): row for row in summary_rows}
    with path.open("w", encoding="utf-8") as f:
        f.write("# Auto-Suggested Banglish Candidate: Prior Outcome Overlap\n\n")
        f.write("Updated: 2026-05-28\n\n")
        f.write("## Purpose\n\n")
        f.write(
            "This analysis checks where the automatic Banglish spelling suggestions "
            "fall relative to the already completed validation-200 v3-to-v4 "
            "Banglish sensitivity results. It helps interpret the currently "
            "running auto-suggested GPU sensitivity jobs.\n\n"
        )
        f.write("## Inputs\n\n")
        f.write(f"- Qwen2.5 v3-v4 compare: `{repo_path(qwen25_compare)}`\n")
        f.write(f"- Qwen3 v3-v4 compare: `{repo_path(qwen3_compare)}`\n")
        f.write(f"- Summary CSV: `{repo_path(summary_output)}`\n\n")

        f.write("## Candidate Coverage\n\n")
        f.write(f"- Items with any auto-suggested text change: {len(changed_ids)}/200\n")
        f.write(f"- Items with clean-field change: {len(clean_changed_ids)}/200\n")
        f.write(f"- Items with noisy-field change: {len(noisy_changed_ids)}/200\n\n")

        f.write("## Existing v4 Outcomes by Candidate Bucket\n\n")
        f.write("| Model | Bucket | n | v3 correct | v4 correct | v4-v3 | v4 wrong |\n")
        f.write("| --- | --- | ---: | ---: | ---: | ---: | ---: |\n")
        for row in summary_rows:
            f.write(
                f"| {row['model']} | {row['bucket']} | {row['n']} | "
                f"{row['v3_correct']} | {row['v4_correct']} | "
                f"{row['v4_minus_v3_correct']} | {row['v4_wrong_items']} |\n"
            )
        f.write("\n")

        f.write("## Interpretation Before New GPU Results\n\n")
        for model in ["Qwen2.5-3B", "Qwen3-4B"]:
            changed = by_model[(model, "auto_changed")]
            unchanged = by_model[(model, "auto_unchanged")]
            f.write(
                f"- {model}: among the 140 auto-changed items, v4 already gets "
                f"{changed['v4_correct']}/{changed['n']} correct and leaves "
                f"{changed['v4_wrong_items']} wrong; among the 60 unchanged items, "
                f"v4 gets {unchanged['v4_correct']}/{unchanged['n']} correct.\n"
            )
        f.write(
            "- The auto-suggested run therefore has room to improve many currently "
            "wrong changed items, but it can also create losses. The paired result "
            "after the Kaggle runs finish is the decisive check.\n"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=ROOT / "data/slices/validation_200_v4_auto_suggested.jsonl",
    )
    parser.add_argument(
        "--qwen25-compare",
        type=Path,
        default=ROOT / "results/analysis/qwen25_validation200_v3_vs_v4_banglish_items_reparsed.csv",
    )
    parser.add_argument(
        "--qwen3-compare",
        type=Path,
        default=ROOT / "results/analysis/qwen3_validation200_v3_vs_v4_banglish_items_reparsed.csv",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT / "results/analysis/validation200_v4_auto_suggested_prior_overlap_summary.csv",
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=ROOT / "reports/validation200_v4_auto_suggested_prior_overlap.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidate_rows = load_jsonl(args.candidate)
    changed_ids = {row["id"] for row in candidate_rows if changed_field_set(row)}
    clean_changed_ids = {
        row["id"] for row in candidate_rows if "banglish_clean" in changed_field_set(row)
    }
    noisy_changed_ids = {
        row["id"] for row in candidate_rows if "banglish_noisy" in changed_field_set(row)
    }

    summary_rows: list[dict[str, Any]] = []
    summary_rows.extend(
        summarize_model("Qwen2.5-3B", load_csv(args.qwen25_compare), changed_ids)
    )
    summary_rows.extend(
        summarize_model("Qwen3-4B", load_csv(args.qwen3_compare), changed_ids)
    )

    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        summary_rows,
        changed_ids,
        clean_changed_ids,
        noisy_changed_ids,
        args.qwen25_compare,
        args.qwen3_compare,
        args.summary_output,
    )
    print(f"changed_ids={len(changed_ids)}")
    print(f"wrote={args.summary_output}")
    print(f"wrote={args.report_output}")


if __name__ == "__main__":
    main()
