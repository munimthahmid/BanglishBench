#!/usr/bin/env python3
"""Audit BEnQA option bias by frozen-v5 Banglish review label."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_review_label_option_bias_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_review_label_option_bias_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_review_label_option_bias.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
OPTIONS = ("A", "B", "C", "D")
BUCKETS = (
    ("all", "All BEnQA rows"),
    ("unreviewed", "Rows not selected for v5 Banglish review"),
    ("minor_edit", "Rows with minor Banglish edit"),
    ("major_edit", "Rows with major Banglish edit"),
    ("bad", "Rows flagged bad under the default all-200 policy"),
    ("reviewed_nonbad", "Minor/major edited rows"),
    ("reviewed_all", "All rows selected for v5 review"),
    ("strict_nonbad", "All rows except bad"),
)


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
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def valid_option(value: Any) -> str:
    option = str(value).strip().upper()
    return option if option in OPTIONS else "invalid"


def load_benqa_review_metadata(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            if item.get("dataset") != "benqa":
                continue
            review = item.get("banglish_review", {}) or {}
            metadata = item.get("metadata", {}) or {}
            review_label = str(review.get("label") or "unreviewed")
            out[str(item["id"])] = {
                "review_label": review_label,
                "quality_status": str(item.get("quality_status", "")),
                "subject": str(metadata.get("subject", "")),
                "grade": str(metadata.get("grade", "")),
                "domain": str(item.get("domain", "")),
            }
    if len(out) != 144:
        raise SystemExit(f"Expected 144 BEnQA metadata rows, got {len(out)}")
    return out


def build_item_rows(items_path: Path, choice_items_path: Path) -> list[dict[str, Any]]:
    metadata = load_benqa_review_metadata(items_path)
    choice_rows = read_csv(choice_items_path)
    if len(choice_rows) != len(MODELS) * 144:
        raise SystemExit(f"Expected {len(MODELS) * 144} choice-bias item rows, got {len(choice_rows)}")

    rows: list[dict[str, Any]] = []
    for row in choice_rows:
        item_id = row["id"]
        if item_id not in metadata:
            raise SystemExit(f"Missing BEnQA review metadata for {item_id}")
        meta = metadata[item_id]
        gold = valid_option(row["gold"])
        option = valid_option(row["banglish_clean_parsed_option"])
        correct = truthy(row["banglish_clean_correct"])
        rows.append(
            {
                "model": row["model"],
                "id": item_id,
                "review_label": meta["review_label"],
                "quality_status": meta["quality_status"],
                "subject": meta["subject"],
                "grade": meta["grade"],
                "domain": meta["domain"],
                "gold": gold,
                "banglish_option": option,
                "banglish_correct": correct,
                "gold_D": gold == "D",
                "banglish_D": option == "D",
                "banglish_wrong_D": option == "D" and not correct,
                "banglish_invalid": option == "invalid",
            }
        )
    return rows


def in_bucket(row: dict[str, Any], bucket: str) -> bool:
    label = str(row["review_label"])
    if bucket == "all":
        return True
    if bucket == "reviewed_nonbad":
        return label in {"minor_edit", "major_edit"}
    if bucket == "reviewed_all":
        return label in {"minor_edit", "major_edit", "bad"}
    if bucket == "strict_nonbad":
        return label != "bad"
    return label == bucket


def summarize_bucket(rows: list[dict[str, Any]], model: str, bucket: str, label: str) -> dict[str, Any]:
    selected = [row for row in rows if row["model"] == model and in_bucket(row, bucket)]
    n = len(selected)
    pred_counts = Counter(str(row["banglish_option"]) for row in selected)
    gold_counts = Counter(str(row["gold"]) for row in selected)
    d_count = pred_counts["D"]
    gold_d = gold_counts["D"]
    return {
        "section": "review_bucket",
        "model": model,
        "bucket": bucket,
        "bucket_label": label,
        "n": n,
        "banglish_correct": sum(bool(row["banglish_correct"]) for row in selected),
        "gold_D": gold_d,
        "banglish_D": d_count,
        "banglish_wrong_D": sum(bool(row["banglish_wrong_D"]) for row in selected),
        "banglish_invalid": sum(bool(row["banglish_invalid"]) for row in selected),
        "pred_A": pred_counts["A"],
        "pred_B": pred_counts["B"],
        "pred_C": pred_counts["C"],
        "pred_D": pred_counts["D"],
        "gold_A": gold_counts["A"],
        "gold_B": gold_counts["B"],
        "gold_C": gold_counts["C"],
        "gold_D_count": gold_d,
        "d_over_gold_d": d_count - gold_d,
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        for bucket, label in BUCKETS:
            rows.append(summarize_bucket(item_rows, model, bucket, label))
    return rows


def row_for(rows: list[dict[str, Any]], model: str, bucket: str) -> dict[str, Any]:
    matches = [row for row in rows if row["model"] == model and row["bucket"] == bucket]
    if len(matches) != 1:
        raise SystemExit(f"Expected one row for {model} {bucket}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_all = row_for(summary_rows, "Qwen3-4B", "all")
    q3_unreviewed = row_for(summary_rows, "Qwen3-4B", "unreviewed")
    q3_minor = row_for(summary_rows, "Qwen3-4B", "minor_edit")
    q3_reviewed_nonbad = row_for(summary_rows, "Qwen3-4B", "reviewed_nonbad")
    q25_3_unreviewed = row_for(summary_rows, "Qwen2.5-3B", "unreviewed")
    q25_7_unreviewed = row_for(summary_rows, "Qwen2.5-7B 8-bit", "unreviewed")
    q25_3_reviewed_nonbad = row_for(summary_rows, "Qwen2.5-3B", "reviewed_nonbad")
    q25_7_reviewed_nonbad = row_for(summary_rows, "Qwen2.5-7B 8-bit", "reviewed_nonbad")

    lines = [
        "# Frozen-V5 BEnQA Review-Label Option-Bias Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether Qwen3-4B's reviewed-Banglish BEnQA",
        "D-attractor can be reduced to rows that were selected for v5 Banglish",
        "review or manual edits. It joins frozen-v5 review labels with the BEnQA",
        "choice-bias item table.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- Overall, Qwen3-4B predicts D on "
            f"{q3_all['banglish_D']}/{q3_all['n']} BEnQA rows while gold D appears on "
            f"{q3_all['gold_D']}/{q3_all['n']} rows."
        ),
        (
            "- On unreviewed BEnQA rows, Qwen3-4B still predicts D on "
            f"{q3_unreviewed['banglish_D']}/{q3_unreviewed['n']} rows "
            f"({percent(int(q3_unreviewed['banglish_D']), int(q3_unreviewed['n']))}) "
            f"with wrong D on {q3_unreviewed['banglish_wrong_D']}/{q3_unreviewed['n']}; "
            f"gold D is only {q3_unreviewed['gold_D']}/{q3_unreviewed['n']}."
        ),
        (
            "- On minor-edit rows, Qwen3-4B predicts D on "
            f"{q3_minor['banglish_D']}/{q3_minor['n']} rows and wrong D on "
            f"{q3_minor['banglish_wrong_D']}/{q3_minor['n']}."
        ),
        (
            "- On reviewed nonbad rows, Qwen3-4B predicts D on "
            f"{q3_reviewed_nonbad['banglish_D']}/{q3_reviewed_nonbad['n']} rows; "
            f"the corresponding Qwen2.5 D counts are "
            f"{q25_3_reviewed_nonbad['banglish_D']}/{q25_3_reviewed_nonbad['n']} and "
            f"{q25_7_reviewed_nonbad['banglish_D']}/{q25_7_reviewed_nonbad['n']}."
        ),
        (
            "- Even in the unreviewed bucket, Qwen2.5 rows remain much lower at "
            f"{q25_3_unreviewed['banglish_D']}/{q25_3_unreviewed['n']} and "
            f"{q25_7_unreviewed['banglish_D']}/{q25_7_unreviewed['n']} D predictions."
        ),
        "",
        "## Summary",
        "",
        "| Model | Bucket | N | Correct | Gold D | Pred D | Wrong D | D over gold-D |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        for bucket, _label in BUCKETS:
            row = row_for(summary_rows, model, bucket)
            lines.append(
                f"| {model} | {row['bucket_label']} | {row['n']} | "
                f"{row['banglish_correct']} | {row['gold_D']} | {row['banglish_D']} | "
                f"{row['banglish_wrong_D']} | {row['d_over_gold_d']} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Qwen3's D-attractor is present in both unreviewed and edited BEnQA rows,",
            "  so it is not a simple artifact of human-reviewed edits.",
            "- Gold-D counts are modest in the unreviewed and minor-edit buckets, so",
            "  the high Qwen3 D count is not explained by review-label-specific gold",
            "  label balance.",
            "- The major-edit and bad buckets are too small for standalone claims;",
            "  use them only as completeness checks.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_review_label_option_bias.py`",
            f"- Item table: `{repo_path(items_output)}`",
            f"- Summary table: `{repo_path(summary_output)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.items, args.choice_items)
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    q3_unreviewed = row_for(summary_rows, "Qwen3-4B", "unreviewed")
    q3_reviewed_nonbad = row_for(summary_rows, "Qwen3-4B", "reviewed_nonbad")
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"qwen3_unreviewed_D={q3_unreviewed['banglish_D']}/{q3_unreviewed['n']} "
        f"qwen3_reviewed_nonbad_D={q3_reviewed_nonbad['banglish_D']}/"
        f"{q3_reviewed_nonbad['n']} report={args.report_output}"
    )


if __name__ == "__main__":
    main()
