#!/usr/bin/env python3
"""Audit BEnQA reviewed-Banglish behavior when Bangla and English agree."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_cross_script_option_agreement_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_cross_script_option_agreement_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_cross_script_option_agreement.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
OPTIONS = ("A", "B", "C", "D")
SCOPES = (
    ("all", "All BEnQA rows"),
    ("be_agree", "Bangla and English agree"),
    ("be_agree_non_d", "Bangla and English agree on non-D"),
    ("be_agree_d", "Bangla and English agree on D"),
    ("be_correct_agree", "Bangla and English are correct and agree"),
    ("be_correct_agree_non_d", "Bangla and English are correct and agree on non-D"),
    ("be_correct_agree_d", "Bangla and English are correct and agree on D"),
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


def valid_option(value: Any) -> str:
    option = str(value).strip().upper()
    return option if option in OPTIONS else ""


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    if len(rows) != len(MODELS) * 144:
        raise SystemExit(f"Expected {len(MODELS) * 144} choice-bias item rows, got {len(rows)}")
    out: list[dict[str, Any]] = []
    for row in rows:
        bangla = valid_option(row["bangla_parsed_option"])
        english = valid_option(row["english_parsed_option"])
        banglish = valid_option(row["banglish_clean_parsed_option"])
        bangla_correct = truthy(row["bangla_correct"])
        english_correct = truthy(row["english_correct"])
        banglish_correct = truthy(row["banglish_clean_correct"])
        be_both_valid = bool(bangla and english)
        all_valid = bool(bangla and english and banglish)
        be_agree = be_both_valid and bangla == english
        be_agreement_option = bangla if be_agree else ""
        be_correct_agree = be_agree and bangla_correct and english_correct
        banglish_same_as_agreement = all_valid and be_agree and banglish == be_agreement_option
        banglish_wrong_d = banglish == "D" and not banglish_correct
        out.append(
            {
                "model": row["model"],
                "id": row["id"],
                "gold": row["gold"],
                "bangla_option": bangla or "invalid",
                "english_option": english or "invalid",
                "banglish_option": banglish or "invalid",
                "bangla_correct": bangla_correct,
                "english_correct": english_correct,
                "banglish_correct": banglish_correct,
                "be_both_valid": be_both_valid,
                "all_valid": all_valid,
                "be_agree": be_agree,
                "be_agreement_option": be_agreement_option or "none",
                "be_agree_non_d": be_agree and be_agreement_option != "D",
                "be_agree_d": be_agree and be_agreement_option == "D",
                "be_correct_agree": be_correct_agree,
                "be_correct_agree_non_d": be_correct_agree and be_agreement_option != "D",
                "be_correct_agree_d": be_correct_agree and be_agreement_option == "D",
                "banglish_same_as_agreement": banglish_same_as_agreement,
                "banglish_switches_from_agreement": all_valid and be_agree and not banglish_same_as_agreement,
                "banglish_D": banglish == "D",
                "banglish_wrong_D": banglish_wrong_d,
                "banglish_correct_on_agreement": be_agree and banglish_correct,
            }
        )
    return out


def in_scope(row: dict[str, Any], scope: str) -> bool:
    if scope == "all":
        return True
    return bool(row[scope])


def summarize_scope(rows: list[dict[str, Any]], model: str, scope: str, label: str) -> dict[str, Any]:
    selected = [row for row in rows if row["model"] == model and in_scope(row, scope)]
    n = len(selected)
    same = sum(bool(row["banglish_same_as_agreement"]) for row in selected)
    switched = sum(bool(row["banglish_switches_from_agreement"]) for row in selected)
    correct = sum(bool(row["banglish_correct"]) for row in selected)
    d_count = sum(bool(row["banglish_D"]) for row in selected)
    wrong_d = sum(bool(row["banglish_wrong_D"]) for row in selected)
    invalid_banglish = sum(row["banglish_option"] == "invalid" for row in selected)
    return {
        "section": "scope_summary",
        "model": model,
        "scope": scope,
        "scope_label": label,
        "n": n,
        "banglish_correct": correct,
        "banglish_D": d_count,
        "banglish_wrong_D": wrong_d,
        "banglish_same_as_agreement": same,
        "banglish_switches_from_agreement": switched,
        "banglish_invalid": invalid_banglish,
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        for scope, label in SCOPES:
            rows.append(summarize_scope(item_rows, model, scope, label))
    return rows


def row_for(rows: list[dict[str, Any]], model: str, scope: str) -> dict[str, Any]:
    matches = [row for row in rows if row["model"] == model and row["scope"] == scope]
    if len(matches) != 1:
        raise SystemExit(f"Expected one summary row for {model} {scope}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_non_d = row_for(summary_rows, "Qwen3-4B", "be_correct_agree_non_d")
    q25_3_non_d = row_for(summary_rows, "Qwen2.5-3B", "be_correct_agree_non_d")
    q25_7_non_d = row_for(summary_rows, "Qwen2.5-7B 8-bit", "be_correct_agree_non_d")
    q3_agree_non_d = row_for(summary_rows, "Qwen3-4B", "be_agree_non_d")
    q3_agree = row_for(summary_rows, "Qwen3-4B", "be_agree")
    q3_d = row_for(summary_rows, "Qwen3-4B", "be_correct_agree_d")

    lines = [
        "# Frozen-V5 BEnQA Cross-Script Option-Agreement Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit asks what reviewed Banglish does when the same",
        "model's Bangla and English BEnQA predictions agree on an option label.",
        "The strongest slice is where Bangla and English are both correct and",
        "agree on the same non-D option. It uses only the frozen-v5 BEnQA",
        "choice-bias item table.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- When Qwen3-4B Bangla and English are both correct and agree on the "
            f"same non-D option, reviewed Banglish still switches to wrong D on "
            f"{q3_non_d['banglish_wrong_D']}/{q3_non_d['n']} rows "
            f"({percent(int(q3_non_d['banglish_wrong_D']), int(q3_non_d['n']))})."
        ),
        (
            "- The corresponding Qwen2.5 wrong-D rates are "
            f"{q25_3_non_d['banglish_wrong_D']}/{q25_3_non_d['n']} and "
            f"{q25_7_non_d['banglish_wrong_D']}/{q25_7_non_d['n']}."
        ),
        (
            "- In the broader Qwen3 Bangla-English non-D agreement slice, reviewed "
            f"Banglish predicts D on {q3_agree_non_d['banglish_D']}/{q3_agree_non_d['n']} rows."
        ),
        (
            "- Across all Qwen3 rows where Bangla and English agree, reviewed Banglish "
            f"predicts D on {q3_agree['banglish_D']}/{q3_agree['n']} rows."
        ),
        (
            "- When Bangla and English are both correct and agree on D, Qwen3 reviewed "
            f"Banglish keeps D on {q3_d['banglish_D']}/{q3_d['n']} rows."
        ),
        "",
        "## Summary",
        "",
        "| Model | Scope | N | Banglish correct | Banglish D | Wrong D | Same as agreement | Switches |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        for scope, _ in SCOPES:
            row = row_for(summary_rows, model, scope)
            lines.append(
                f"| {model} | {row['scope_label']} | {row['n']} | "
                f"{row['banglish_correct']} | {row['banglish_D']} | "
                f"{row['banglish_wrong_D']} | {row['banglish_same_as_agreement']} | "
                f"{row['banglish_switches_from_agreement']} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a stricter version of the option-switching audit: it requires",
            "  both alternate scripts to agree before inspecting the reviewed-Banglish",
            "  answer.",
            "- Qwen3's D-attractor survives this agreement filter, including the slice",
            "  where both Bangla and English are correct on the same non-D answer.",
            "- The result remains behavioral evidence and uses benchmark-provided",
            "  alternate-script views, so it is diagnostic rather than deployable.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_cross_script_option_agreement.py`",
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
    rows = read_csv(args.input)
    item_rows = build_item_rows(rows)
    summary_rows = build_summary_rows(item_rows)
    if len(summary_rows) != len(MODELS) * len(SCOPES):
        raise SystemExit(f"Unexpected summary row count: {len(summary_rows)}")
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)

    q3_non_d = row_for(summary_rows, "Qwen3-4B", "be_correct_agree_non_d")
    q25_3_non_d = row_for(summary_rows, "Qwen2.5-3B", "be_correct_agree_non_d")
    q25_7_non_d = row_for(summary_rows, "Qwen2.5-7B 8-bit", "be_correct_agree_non_d")
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"qwen3_correct_BE_agree_nonD_wrongD={q3_non_d['banglish_wrong_D']}/{q3_non_d['n']} "
        f"qwen25_wrongD={q25_3_non_d['banglish_wrong_D']}/{q25_3_non_d['n']},"
        f"{q25_7_non_d['banglish_wrong_D']}/{q25_7_non_d['n']} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
