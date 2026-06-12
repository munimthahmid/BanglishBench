#!/usr/bin/env python3
"""Audit BEnQA MCQ option-label behavior for frozen-v5 thesis rows."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_answer_format_audit_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_choice_bias_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_choice_bias.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
VARIANTS = ("bangla", "banglish_clean", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}
OPTIONS = ("A", "B", "C", "D")
PAIRS = (
    ("bangla", "banglish_clean"),
    ("english", "banglish_clean"),
    ("bangla", "english"),
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


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def valid_option(value: Any) -> str:
    value = str(value).strip().upper()
    return value if value in OPTIONS else ""


def percent(numerator: int | float, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


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
    return 0.5 * sum(abs(pred[option] / n - gold[option] / n) for option in OPTIONS)


def marginal_expected_correct(pred: Counter[str], gold: Counter[str], n: int) -> float:
    return sum(pred[option] * gold[option] / n for option in OPTIONS)


def load_benqa_choice_rows(path: Path) -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(path)
        if row.get("dataset") == "benqa" and row.get("answer_type") == "choice"
    ]
    expected = len(MODELS) * len(VARIANTS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} BEnQA choice rows, got {len(rows)}")
    return rows


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    index = {(row["model"], row["id"], row["variant"]): row for row in rows}
    ids = sorted({row["id"] for row in rows})
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for item_id in ids:
            first = index[(model, item_id, "bangla")]
            item_row: dict[str, Any] = {
                "model": model,
                "id": item_id,
                "gold": valid_option(first["gold"]),
            }
            for variant in VARIANTS:
                row = index[(model, item_id, variant)]
                parsed = valid_option(row.get("parsed", ""))
                item_row[f"{variant}_parsed_option"] = parsed or "invalid"
                item_row[f"{variant}_valid_option"] = bool(parsed)
                item_row[f"{variant}_correct"] = truthy(row.get("correct", ""))
                item_row[f"{variant}_format_failure"] = truthy(row.get("format_failure", ""))
            item_row["banglish_same_as_bangla"] = (
                item_row["banglish_clean_valid_option"]
                and item_row["bangla_valid_option"]
                and item_row["banglish_clean_parsed_option"] == item_row["bangla_parsed_option"]
            )
            item_row["banglish_same_as_english"] = (
                item_row["banglish_clean_valid_option"]
                and item_row["english_valid_option"]
                and item_row["banglish_clean_parsed_option"] == item_row["english_parsed_option"]
            )
            item_row["banglish_wrong_bangla_correct"] = (
                not item_row["banglish_clean_correct"] and item_row["bangla_correct"]
            )
            item_row["banglish_wrong_english_correct"] = (
                not item_row["banglish_clean_correct"] and item_row["english_correct"]
            )
            out.append(item_row)
    return out


def build_variant_summary(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    gold_counts = Counter(valid_option(row["gold"]) for row in rows if row["variant"] == "bangla")
    # The gold counts repeat once per model in raw rows; normalize to one item set.
    gold_counts = Counter({option: gold_counts[option] // len(MODELS) for option in OPTIONS})
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for variant in VARIANTS:
            selected = [
                row for row in rows if row["model"] == model and row["variant"] == variant
            ]
            n = len(selected)
            pred_counts = Counter(valid_option(row.get("parsed", "")) or "invalid" for row in selected)
            correct = sum(truthy(row["correct"]) for row in selected)
            invalid = pred_counts["invalid"]
            majority_option, majority_count = max(
                ((option, pred_counts[option]) for option in OPTIONS),
                key=lambda item: item[1],
            )
            expected = marginal_expected_correct(pred_counts, gold_counts, n)
            out.append(
                {
                    "section": "variant_distribution",
                    "model": model,
                    "variant": variant,
                    "variant_label": VARIANT_LABELS[variant],
                    "n": n,
                    "correct": correct,
                    "invalid": invalid,
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
                    "option_entropy": round(entropy(pred_counts), 4),
                    "tvd_pred_vs_gold": round(total_variation(pred_counts, gold_counts, n), 4),
                    "marginal_expected_correct": round(expected, 2),
                    "actual_minus_marginal_expected": round(correct - expected, 2),
                }
            )
    return out


def build_pair_summary(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        rows = [row for row in item_rows if row["model"] == model]
        for left, right in PAIRS:
            both_valid = [
                row
                for row in rows
                if row[f"{left}_valid_option"] and row[f"{right}_valid_option"]
            ]
            same = [
                row
                for row in both_valid
                if row[f"{left}_parsed_option"] == row[f"{right}_parsed_option"]
            ]
            different = len(both_valid) - len(same)
            left_correct_right_wrong = sum(
                row[f"{left}_correct"] and not row[f"{right}_correct"] for row in both_valid
            )
            right_correct_left_wrong = sum(
                row[f"{right}_correct"] and not row[f"{left}_correct"] for row in both_valid
            )
            same_wrong = sum(
                (row in same)
                and not row[f"{left}_correct"]
                and not row[f"{right}_correct"]
                for row in both_valid
            )
            out.append(
                {
                    "section": "pair_agreement",
                    "model": model,
                    "variant": f"{left}_vs_{right}",
                    "variant_label": f"{VARIANT_LABELS[left]} vs {VARIANT_LABELS[right]}",
                    "n": len(rows),
                    "correct": "",
                    "invalid": len(rows) - len(both_valid),
                    "pred_A": "",
                    "pred_B": "",
                    "pred_C": "",
                    "pred_D": "",
                    "gold_A": "",
                    "gold_B": "",
                    "gold_C": "",
                    "gold_D": "",
                    "majority_option": "",
                    "majority_share": "",
                    "option_entropy": "",
                    "tvd_pred_vs_gold": "",
                    "marginal_expected_correct": "",
                    "actual_minus_marginal_expected": "",
                    "both_valid": len(both_valid),
                    "same_option": len(same),
                    "different_option": different,
                    "same_wrong": same_wrong,
                    "left_correct_right_wrong": left_correct_right_wrong,
                    "right_correct_left_wrong": right_correct_left_wrong,
                }
            )
    return out


def row_for(rows: list[dict[str, Any]], model: str, variant: str) -> dict[str, Any]:
    return next(row for row in rows if row["model"] == model and row["variant"] == variant)


def write_report(
    path: Path,
    variant_summary: list[dict[str, Any]],
    pair_summary: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    lines = [
        "# Frozen-V5 BEnQA Choice-Bias Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether BEnQA MCQ losses are caused by",
        "malformed option outputs or by a script-conditioned option-label bias.",
        "It uses the frozen-v5 answer-format audit rows for the 144 BEnQA MCQs",
        "and the three thesis-facing Qwen models.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "The gold BEnQA option distribution is not collapsed: A=29, B=35, C=41,",
        "and D=39.",
        "",
        "## Option Distribution",
        "",
        "| Model | Variant | Correct | Invalid | Pred A | Pred B | Pred C | Pred D | Majority | Entropy | TVD vs gold |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        for variant in VARIANTS:
            row = row_for(variant_summary, model, variant)
            lines.append(
                f"| {model} | {row['variant_label']} | {row['correct']}/{row['n']} | "
                f"{row['invalid']} | {row['pred_A']} | {row['pred_B']} | "
                f"{row['pred_C']} | {row['pred_D']} | "
                f"{row['majority_option']} ({percent(float(row['majority_share']) * int(row['n']), int(row['n']))}) | "
                f"{row['option_entropy']:.2f} | {row['tvd_pred_vs_gold']:.2f} |"
            )

    lines.extend(
        [
            "",
            "## Banglish Agreement With Other Scripts",
            "",
            "| Model | Pair | Both valid | Same option | Different option | Left correct/right wrong | Right correct/left wrong |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        for left, right in PAIRS:
            if right != "banglish_clean" and left != "banglish_clean":
                continue
            row = row_for(pair_summary, model, f"{left}_vs_{right}")
            lines.append(
                f"| {model} | {row['variant_label']} | {row['both_valid']} | "
                f"{row['same_option']} | {row['different_option']} | "
                f"{row['left_correct_right_wrong']} | {row['right_correct_left_wrong']} |"
            )

    qwen3_banglish = row_for(variant_summary, "Qwen3-4B", "banglish_clean")
    qwen25_3b_banglish = row_for(variant_summary, "Qwen2.5-3B", "banglish_clean")
    qwen25_7b_banglish = row_for(variant_summary, "Qwen2.5-7B 8-bit", "banglish_clean")
    qwen3_always_d = 39
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- MCQ format failure is not the main explanation: Qwen2.5-3B has no",
            "  invalid BEnQA choices, Qwen2.5-7B has two invalid reviewed-Banglish",
            "  choices, and Qwen3 has three invalid reviewed-Banglish choices.",
            "- Qwen2.5 rows do not collapse to one Banglish option label. Their",
            f"  reviewed-Banglish majority shares are {percent(float(qwen25_3b_banglish['majority_share']) * 144, 144)}",
            f"  for Qwen2.5-3B and {percent(float(qwen25_7b_banglish['majority_share']) * 144, 144)}",
            "  for Qwen2.5-7B.",
            "- Qwen3-4B does show a real script-conditioned choice bias: reviewed",
            f"  Banglish predicts D on {qwen3_banglish['pred_D']}/144 rows "
            f"({percent(int(qwen3_banglish['pred_D']), 144)}), while gold D appears on",
            f"  {qwen3_always_d}/144 rows.",
            "- The Qwen3 Banglish row scores 47/144, only 8 items above an always-D",
            "  baseline, while Qwen3 Bangla and English score 76/144 and 82/144.",
            "- Treat option-label bias as a discovered failure mode for Qwen3",
            "  Banglish, not as a reason to dismiss the gap: Qwen2.5 gaps remain",
            "  without one-label collapse, and Qwen3's collapse is itself",
            "  script-conditioned behavior.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_choice_bias.py`",
            f"- Item table: `{repo_path(items_output)}`",
            f"- Summary table: `{repo_path(summary_output)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_benqa_choice_rows(args.input)
    item_rows = build_item_rows(rows)
    variant_summary = build_variant_summary(rows)
    pair_summary = build_pair_summary(item_rows)
    summary_rows = variant_summary + pair_summary
    item_fields = list(item_rows[0])
    summary_fields: list[str] = []
    for row in summary_rows:
        for key in row:
            if key not in summary_fields:
                summary_fields.append(key)
    write_csv(args.items_output, item_rows, item_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(args.report_output, variant_summary, pair_summary, args.items_output, args.summary_output)
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
