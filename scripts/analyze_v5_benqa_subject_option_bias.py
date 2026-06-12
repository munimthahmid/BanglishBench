#!/usr/bin/env python3
"""Audit whether BEnQA option-label bias is broad across subjects."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_answer_format_audit_items.csv"
DEFAULT_VALIDATION = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_subject_option_bias_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_subject_option_bias_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_subject_option_bias.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
VARIANTS = ("bangla", "banglish_clean", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}
OPTIONS = ("A", "B", "C", "D")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_validation_metadata(path: Path) -> dict[str, dict[str, str]]:
    metadata: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            item_meta = row.get("metadata", {})
            metadata[str(row["id"])] = {
                "dataset": str(row.get("dataset", "")),
                "domain": str(row.get("domain", "")),
                "subject": str(item_meta.get("subject") or row.get("domain", "")),
                "grade": str(item_meta.get("grade", "")),
            }
    return metadata


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


def valid_option(value: Any) -> str:
    parsed = str(value).strip().upper()
    return parsed if parsed in OPTIONS else ""


def entropy(counts: Counter[str]) -> float:
    total = sum(counts[option] for option in OPTIONS)
    if total == 0:
        return 0.0
    value = 0.0
    for option in OPTIONS:
        count = counts[option]
        if count:
            p = count / total
            value -= p * math.log(p)
    return value / math.log(len(OPTIONS))


def total_variation(pred: Counter[str], gold: Counter[str], n: int) -> float:
    if n == 0:
        return 0.0
    return 0.5 * sum(abs(pred[option] / n - gold[option] / n) for option in OPTIONS)


def load_benqa_rows(path: Path, validation: Path) -> list[dict[str, Any]]:
    metadata = read_validation_metadata(validation)
    rows: list[dict[str, Any]] = []
    for row in read_csv(path):
        if row.get("dataset") != "benqa" or row.get("answer_type") != "choice":
            continue
        item_id = str(row["id"])
        meta = metadata[item_id]
        parsed = valid_option(row.get("parsed", ""))
        rows.append(
            {
                "model": row["model"],
                "variant": row["variant"],
                "variant_label": VARIANT_LABELS.get(row["variant"], row["variant"]),
                "id": item_id,
                "subject": meta["subject"],
                "domain": meta["domain"],
                "grade": meta["grade"],
                "gold": valid_option(row.get("gold", "")),
                "parsed_option": parsed or "invalid",
                "valid_option": bool(parsed),
                "correct": truthy(row.get("correct", "")),
                "format_failure": truthy(row.get("format_failure", "")),
            }
        )
    expected = len(MODELS) * len(VARIANTS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} BEnQA rows, got {len(rows)}")
    return sorted(rows, key=lambda row: (row["model"], row["variant"], row["subject"], row["id"]))


def summarize_subject(rows: list[dict[str, Any]], model: str, variant: str, subject: str) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["model"] == model and row["variant"] == variant and row["subject"] == subject
    ]
    if not selected:
        raise SystemExit(f"No rows for {model} {variant} {subject}")
    n = len(selected)
    pred_counts = Counter(row["parsed_option"] for row in selected)
    gold_counts = Counter(row["gold"] for row in selected)
    valid_n = sum(1 for row in selected if row["valid_option"])
    majority_option, majority_count = max(
        ((option, pred_counts[option]) for option in OPTIONS),
        key=lambda item: item[1],
    )
    return {
        "section": "subject_variant",
        "model": model,
        "variant": variant,
        "variant_label": VARIANT_LABELS.get(variant, variant),
        "subject": subject,
        "n": n,
        "correct": sum(1 for row in selected if row["correct"]),
        "invalid": pred_counts["invalid"],
        "valid_n": valid_n,
        "pred_A": pred_counts["A"],
        "pred_B": pred_counts["B"],
        "pred_C": pred_counts["C"],
        "pred_D": pred_counts["D"],
        "gold_A": gold_counts["A"],
        "gold_B": gold_counts["B"],
        "gold_C": gold_counts["C"],
        "gold_D": gold_counts["D"],
        "majority_option": majority_option,
        "majority_share": round(majority_count / n, 4),
        "d_share": round(pred_counts["D"] / n, 4),
        "gold_d_share": round(gold_counts["D"] / n, 4),
        "option_entropy": round(entropy(pred_counts), 4),
        "tvd_pred_vs_gold": round(total_variation(pred_counts, gold_counts, n), 4),
        "majority_d": majority_option == "D" and pred_counts["D"] > n / 2,
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    subjects = sorted({row["subject"] for row in rows})
    summary: list[dict[str, Any]] = []
    for model in MODELS:
        for variant in VARIANTS:
            for subject in subjects:
                summary.append(summarize_subject(rows, model, variant, subject))
    return summary


def subject_summary(rows: list[dict[str, Any]], model: str, variant: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["model"] == model and row["variant"] == variant]


def add_subject_table(lines: list[str], rows: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            "| Subject | N | Correct | Pred A | Pred B | Pred C | Pred D | Gold D | Majority | Entropy | TVD |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            "| {subject} | {n} | {correct}/{n} | {pred_A} | {pred_B} | {pred_C} | "
            "{pred_D} | {gold_D} | {majority_option} ({majority_share:.1%}) | "
            "{option_entropy:.2f} | {tvd_pred_vs_gold:.2f} |".format(**row)
        )


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    qwen3_banglish = subject_summary(summary_rows, "Qwen3-4B", "banglish_clean")
    qwen25_3b_banglish = subject_summary(summary_rows, "Qwen2.5-3B", "banglish_clean")
    qwen25_7b_banglish = subject_summary(summary_rows, "Qwen2.5-7B 8-bit", "banglish_clean")
    qwen3_bangla = subject_summary(summary_rows, "Qwen3-4B", "bangla")
    qwen3_english = subject_summary(summary_rows, "Qwen3-4B", "english")

    def majority_d_count(rows: list[dict[str, Any]]) -> int:
        return sum(1 for row in rows if row["majority_d"])

    qwen3_d_subjects = majority_d_count(qwen3_banglish)
    q25_3b_d_subjects = majority_d_count(qwen25_3b_banglish)
    q25_7b_d_subjects = majority_d_count(qwen25_7b_banglish)
    qwen3_bangla_d_subjects = majority_d_count(qwen3_bangla)
    qwen3_english_d_subjects = majority_d_count(qwen3_english)
    max_gold_d = max(row["gold_d_share"] for row in qwen3_banglish)

    lines = [
        "# Frozen-V5 BEnQA Subject Option-Bias Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the Qwen3 reviewed-Banglish BEnQA",
        "D-attractor is broad across subjects or concentrated in one subject",
        "cluster. It joins the frozen-v5 answer-format rows with BEnQA subject",
        "metadata from the validation slice.",
        "",
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Subject summary: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            f"- Qwen3-4B reviewed Banglish has majority-D predictions in {qwen3_d_subjects}/13 "
            "BEnQA subjects."
        ),
        (
            "- The same check gives "
            f"{q25_3b_d_subjects}/13 for Qwen2.5-3B and {q25_7b_d_subjects}/13 "
            "for Qwen2.5-7B 8-bit reviewed Banglish."
        ),
        (
            "- Qwen3-4B Bangla and English have majority-D predictions in "
            f"{qwen3_bangla_d_subjects}/13 and {qwen3_english_d_subjects}/13 subjects, "
            "so the reviewed-Banglish collapse is much broader than its native-script rows."
        ),
        (
            "- No subject has gold-D share above "
            f"{max_gold_d:.1%}; the subject-level D-attractor is not a single gold-label "
            "distribution artifact."
        ),
        "",
        "## Qwen3 Reviewed-Banglish By Subject",
        "",
    ]
    add_subject_table(lines, qwen3_banglish)
    lines.extend(
        [
            "",
            "## Qwen2.5 Reviewed-Banglish Subject Check",
            "",
            "| Model | Majority-D subjects | Highest subject D share | Mean subject entropy |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for label, rows in (
        ("Qwen2.5-3B", qwen25_3b_banglish),
        ("Qwen2.5-7B 8-bit", qwen25_7b_banglish),
        ("Qwen3-4B", qwen3_banglish),
    ):
        lines.append(
            "| {label} | {majority}/13 | {max_d:.1%} | {entropy:.2f} |".format(
                label=label,
                majority=majority_d_count(rows),
                max_d=max(row["d_share"] for row in rows),
                entropy=sum(row["option_entropy"] for row in rows) / len(rows),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Qwen3's reviewed-Banglish D-attractor is broad across BEnQA subjects, not",
            "  just a single-subject artifact.",
            "- Qwen2.5 rows remain useful contrast cases: they still lose accuracy under",
            "  reviewed Banglish, but their subject-level option distributions do not",
            "  collapse to D.",
            "- This is behavioral evidence about answer selection, not a mechanism claim.",
            "  It should be cited beside the choice-bias, distractor-transition, and",
            "  label-balance audits.",
            "",
            "## Reproducibility",
            "",
            f"- Builder: `scripts/analyze_v5_benqa_subject_option_bias.py`",
            f"- Item rows: {len(item_rows)}",
            f"- Subject summary rows: {len(summary_rows)}",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = load_benqa_rows(args.input, args.validation)
    summary_rows = build_summary(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    qwen3_banglish = subject_summary(summary_rows, "Qwen3-4B", "banglish_clean")
    majority_d = sum(1 for row in qwen3_banglish if row["majority_d"])
    print(
        "items={items} | summary_rows={summary_rows} | "
        "qwen3_banglish_majority_d_subjects={majority}/13 | report={report}".format(
            items=len(item_rows),
            summary_rows=len(summary_rows),
            majority=majority_d,
            report=repo_path(args.report_output),
        )
    )


if __name__ == "__main__":
    main()
