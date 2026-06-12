#!/usr/bin/env python3
"""Audit BEnQA option-label switches from Bangla/English into reviewed Banglish."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_option_switching_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_option_switching_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_switching.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
BASELINES = ("bangla", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "english": "English",
    "banglish_clean": "Reviewed Banglish",
}
OPTIONS = ("A", "B", "C", "D")
OPTION_OR_INVALID = ("A", "B", "C", "D", "invalid")


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


def valid_option(value: Any) -> str:
    parsed = str(value).strip().upper()
    return parsed if parsed in OPTIONS else ""


def option_or_invalid(value: Any) -> str:
    return valid_option(value) or "invalid"


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def build_item_rows(choice_items: Path) -> list[dict[str, Any]]:
    source_rows = read_csv(choice_items)
    out: list[dict[str, Any]] = []
    for source in source_rows:
        model = source["model"]
        if model not in MODELS:
            continue
        banglish_option = option_or_invalid(source["banglish_clean_parsed_option"])
        banglish_valid = banglish_option in OPTIONS
        banglish_correct = truthy(source["banglish_clean_correct"])
        for baseline in BASELINES:
            baseline_option = option_or_invalid(source[f"{baseline}_parsed_option"])
            baseline_valid = baseline_option in OPTIONS
            baseline_correct = truthy(source[f"{baseline}_correct"])
            both_valid = baseline_valid and banglish_valid
            baseline_non_d = baseline_option in {"A", "B", "C"}
            baseline_d = baseline_option == "D"
            switched_non_d_to_d = baseline_non_d and banglish_option == "D"
            switched_d_to_non_d = baseline_d and banglish_option in {"A", "B", "C"}
            out.append(
                {
                    "model": model,
                    "baseline_variant": baseline,
                    "baseline_label": VARIANT_LABELS[baseline],
                    "id": source["id"],
                    "gold": valid_option(source["gold"]),
                    "baseline_option": baseline_option,
                    "banglish_option": banglish_option,
                    "baseline_correct": baseline_correct,
                    "banglish_correct": banglish_correct,
                    "both_valid": both_valid,
                    "same_option": both_valid and baseline_option == banglish_option,
                    "switched_valid_option": both_valid and baseline_option != banglish_option,
                    "baseline_non_d": baseline_non_d,
                    "baseline_d": baseline_d,
                    "switched_non_d_to_d": switched_non_d_to_d,
                    "switched_d_to_non_d": switched_d_to_non_d,
                    "baseline_correct_non_d": baseline_non_d and baseline_correct,
                    "baseline_correct_non_d_to_d_wrong": (
                        switched_non_d_to_d and baseline_correct and not banglish_correct
                    ),
                    "baseline_correct_to_banglish_wrong": baseline_correct and not banglish_correct,
                    "banglish_wrong_d": banglish_option == "D" and not banglish_correct,
                }
            )
    expected = len(MODELS) * len(BASELINES) * 144
    if len(out) != expected:
        raise SystemExit(f"Expected {expected} option-switch rows, got {len(out)}")
    return sorted(out, key=lambda row: (row["model"], row["baseline_variant"], row["id"]))


def headline_summary(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        for baseline in BASELINES:
            selected = [
                row
                for row in item_rows
                if row["model"] == model and row["baseline_variant"] == baseline
            ]
            non_d = [row for row in selected if row["baseline_non_d"]]
            baseline_correct_non_d = [row for row in selected if row["baseline_correct_non_d"]]
            non_d_to_d = [row for row in selected if row["switched_non_d_to_d"]]
            d_to_non_d = [row for row in selected if row["switched_d_to_non_d"]]
            rows.append(
                {
                    "section": "headline",
                    "model": model,
                    "baseline_variant": baseline,
                    "baseline_label": VARIANT_LABELS[baseline],
                    "n": len(selected),
                    "both_valid": sum(row["both_valid"] for row in selected),
                    "same_option": sum(row["same_option"] for row in selected),
                    "switched_valid_option": sum(row["switched_valid_option"] for row in selected),
                    "baseline_non_d_n": len(non_d),
                    "non_d_to_D": len(non_d_to_d),
                    "baseline_D_n": sum(row["baseline_d"] for row in selected),
                    "D_to_non_D": len(d_to_non_d),
                    "net_valid_D_shift": len(non_d_to_d) - len(d_to_non_d),
                    "baseline_correct_non_d_n": len(baseline_correct_non_d),
                    "baseline_correct_non_d_to_D_wrong": sum(
                        row["baseline_correct_non_d_to_d_wrong"] for row in selected
                    ),
                    "baseline_correct_to_banglish_wrong": sum(
                        row["baseline_correct_to_banglish_wrong"] for row in selected
                    ),
                    "banglish_wrong_D": sum(row["banglish_wrong_d"] for row in selected),
                }
            )
    return rows


def matrix_summary(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        for baseline in BASELINES:
            selected = [
                row
                for row in item_rows
                if row["model"] == model and row["baseline_variant"] == baseline
            ]
            matrix = Counter(
                (row["baseline_option"], row["banglish_option"])
                for row in selected
            )
            for baseline_option in OPTION_OR_INVALID:
                row_out: dict[str, Any] = {
                    "section": "transition_matrix",
                    "model": model,
                    "baseline_variant": baseline,
                    "baseline_label": VARIANT_LABELS[baseline],
                    "baseline_option": baseline_option,
                    "n": sum(matrix[(baseline_option, option)] for option in OPTION_OR_INVALID),
                }
                for option in OPTION_OR_INVALID:
                    row_out[f"to_{option}"] = matrix[(baseline_option, option)]
                rows.append(row_out)
    return rows


def build_summary(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return headline_summary(item_rows) + matrix_summary(item_rows)


def find_headline(rows: list[dict[str, Any]], model: str, baseline: str) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == "headline"
        and row["model"] == model
        and row["baseline_variant"] == baseline
    )


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    headline_rows = [row for row in summary_rows if row["section"] == "headline"]
    qwen3_bangla = find_headline(summary_rows, "Qwen3-4B", "bangla")
    qwen3_english = find_headline(summary_rows, "Qwen3-4B", "english")
    qwen25_3b_bangla = find_headline(summary_rows, "Qwen2.5-3B", "bangla")
    qwen25_7b_bangla = find_headline(summary_rows, "Qwen2.5-7B 8-bit", "bangla")

    lines = [
        "# Frozen-V5 BEnQA Option-Switching Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit asks whether reviewed-Banglish BEnQA choices are",
        "a stable reuse of the model's Bangla/English option labels or a",
        "script-conditioned switch pattern. It uses the frozen-v5 BEnQA",
        "choice-bias item table for the three thesis-facing Qwen rows.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- Qwen3-4B switches valid non-D Bangla predictions to D in reviewed "
            f"Banglish on {qwen3_bangla['non_d_to_D']}/"
            f"{qwen3_bangla['baseline_non_d_n']} rows "
            f"({percent(int(qwen3_bangla['non_d_to_D']), int(qwen3_bangla['baseline_non_d_n']))})."
        ),
        (
            "- The same Qwen3 non-D-to-D switch from English is "
            f"{qwen3_english['non_d_to_D']}/"
            f"{qwen3_english['baseline_non_d_n']} rows "
            f"({percent(int(qwen3_english['non_d_to_D']), int(qwen3_english['baseline_non_d_n']))})."
        ),
        (
            "- Qwen2.5 rows are far less D-attracted from Bangla: "
            f"{qwen25_3b_bangla['non_d_to_D']}/"
            f"{qwen25_3b_bangla['baseline_non_d_n']} for Qwen2.5-3B and "
            f"{qwen25_7b_bangla['non_d_to_D']}/"
            f"{qwen25_7b_bangla['baseline_non_d_n']} for Qwen2.5-7B 8-bit."
        ),
        (
            "- Among correct non-D alternate-script predictions, Qwen3 changes to a "
            f"wrong D on {qwen3_bangla['baseline_correct_non_d_to_D_wrong']}/"
            f"{qwen3_bangla['baseline_correct_non_d_n']} Bangla rows and "
            f"{qwen3_english['baseline_correct_non_d_to_D_wrong']}/"
            f"{qwen3_english['baseline_correct_non_d_n']} English rows."
        ),
        "",
        "## Summary",
        "",
        "| Model | Baseline | Same valid option | Valid switches | Non-D->D | D->non-D | Net D shift | Correct non-D->wrong D |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in headline_rows:
        lines.append(
            "| {model} | {baseline_label} | {same_option}/{both_valid} | "
            "{switched_valid_option}/{both_valid} | {non_d_to_D}/{baseline_non_d_n} | "
            "{D_to_non_D}/{baseline_D_n} | {net_valid_D_shift:+d} | "
            "{baseline_correct_non_d_to_D_wrong}/{baseline_correct_non_d_n} |".format(
                **{
                    **row,
                    "net_valid_D_shift": int(row["net_valid_D_shift"]),
                }
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Qwen3 reviewed Banglish does not merely preserve its alternate-script",
            "  choice labels. It sharply converts many non-D Bangla/English choices",
            "  into D while rarely moving D back to another option.",
            "- The Qwen2.5 rows switch options too, but their non-D-to-D rates and",
            "  net D shifts are much smaller. This supports treating the Qwen3",
            "  D-attractor as a script-conditioned failure mode rather than a",
            "  generic BEnQA transition pattern.",
            "- Use this audit beside the choice-bias, option-position/content,",
            "  distractor-transition, and label-balance checks.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_benqa_option_switching.py`",
            f"- Item rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.choice_items)
    summary_rows = build_summary(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    qwen3_bangla = find_headline(summary_rows, "Qwen3-4B", "bangla")
    qwen3_english = find_headline(summary_rows, "Qwen3-4B", "english")
    print(
        "items={items} | summary_rows={summary} | "
        "qwen3_nonD_to_D=bangla:{bangla}/{bangla_n},english:{english}/{english_n} | "
        "report={report}".format(
            items=len(item_rows),
            summary=len(summary_rows),
            bangla=qwen3_bangla["non_d_to_D"],
            bangla_n=qwen3_bangla["baseline_non_d_n"],
            english=qwen3_english["non_d_to_D"],
            english_n=qwen3_english["baseline_non_d_n"],
            report=args.report_output,
        )
    )


if __name__ == "__main__":
    main()
