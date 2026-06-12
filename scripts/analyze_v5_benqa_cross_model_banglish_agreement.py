#!/usr/bin/env python3
"""Audit Qwen3 BEnQA behavior when Qwen2.5 models agree on Banglish."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_cross_model_banglish_agreement_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_cross_model_banglish_agreement_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_cross_model_banglish_agreement.md"

Q25_3B = "Qwen2.5-3B"
Q25_7B = "Qwen2.5-7B 8-bit"
Q3 = "Qwen3-4B"
MODELS = (Q25_3B, Q25_7B, Q3)
OPTIONS = ("A", "B", "C", "D")
SCOPES = (
    ("all", "All BEnQA rows"),
    ("q25_both_valid", "Both Qwen2.5 Banglish predictions are valid"),
    ("q25_agree", "Qwen2.5 models agree on Banglish"),
    ("q25_agree_non_d", "Qwen2.5 models agree on non-D Banglish"),
    ("q25_agree_d", "Qwen2.5 models agree on D Banglish"),
    ("q25_correct_agree", "Qwen2.5 models are correct and agree"),
    ("q25_correct_agree_non_d", "Qwen2.5 models are correct and agree on non-D"),
    ("q25_correct_agree_d", "Qwen2.5 models are correct and agree on D"),
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


def model_slug(model: str) -> str:
    return {
        Q25_3B: "qwen25_3b",
        Q25_7B: "qwen25_7b_8bit",
        Q3: "qwen3_4b",
    }[model]


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    if len(rows) != len(MODELS) * 144:
        raise SystemExit(f"Expected {len(MODELS) * 144} choice-bias item rows, got {len(rows)}")

    index = {(row["model"], row["id"]): row for row in rows}
    ids = sorted({row["id"] for row in rows})
    out: list[dict[str, Any]] = []
    for item_id in ids:
        missing = [model for model in MODELS if (model, item_id) not in index]
        if missing:
            raise SystemExit(f"Missing rows for {item_id}: {missing}")

        first = index[(Q25_3B, item_id)]
        row: dict[str, Any] = {
            "id": item_id,
            "gold": valid_option(first["gold"]) or "invalid",
        }
        for model in MODELS:
            source = index[(model, item_id)]
            slug = model_slug(model)
            option = valid_option(source["banglish_clean_parsed_option"])
            row[f"{slug}_banglish_option"] = option or "invalid"
            row[f"{slug}_banglish_valid"] = bool(option)
            row[f"{slug}_banglish_correct"] = truthy(source["banglish_clean_correct"])

        q25_3 = str(row["qwen25_3b_banglish_option"])
        q25_7 = str(row["qwen25_7b_8bit_banglish_option"])
        q3 = str(row["qwen3_4b_banglish_option"])
        q25_3_valid = bool(row["qwen25_3b_banglish_valid"])
        q25_7_valid = bool(row["qwen25_7b_8bit_banglish_valid"])
        q3_valid = bool(row["qwen3_4b_banglish_valid"])
        q25_3_correct = bool(row["qwen25_3b_banglish_correct"])
        q25_7_correct = bool(row["qwen25_7b_8bit_banglish_correct"])
        q3_correct = bool(row["qwen3_4b_banglish_correct"])

        q25_both_valid = q25_3_valid and q25_7_valid
        q25_agree = q25_both_valid and q25_3 == q25_7
        q25_agreement_option = q25_3 if q25_agree else ""
        q25_both_correct = q25_3_correct and q25_7_correct
        q25_correct_agree = q25_agree and q25_both_correct
        q3_same = q25_agree and q3_valid and q3 == q25_agreement_option

        row.update(
            {
                "q25_both_valid": q25_both_valid,
                "q25_agree": q25_agree,
                "q25_agreement_option": q25_agreement_option or "none",
                "q25_agree_non_d": q25_agree and q25_agreement_option != "D",
                "q25_agree_d": q25_agree and q25_agreement_option == "D",
                "q25_both_correct": q25_both_correct,
                "q25_correct_agree": q25_correct_agree,
                "q25_correct_agree_non_d": q25_correct_agree and q25_agreement_option != "D",
                "q25_correct_agree_d": q25_correct_agree and q25_agreement_option == "D",
                "qwen3_same_as_q25_agreement": q3_same,
                "qwen3_switches_from_q25_agreement": q25_agree and q3_valid and not q3_same,
                "qwen3_D": q3 == "D",
                "qwen3_wrong_D": q3 == "D" and not q3_correct,
                "qwen3_invalid": not q3_valid,
            }
        )
        out.append(row)
    return out


def in_scope(row: dict[str, Any], scope: str) -> bool:
    if scope == "all":
        return True
    return bool(row[scope])


def summarize_scope(rows: list[dict[str, Any]], scope: str, label: str) -> dict[str, Any]:
    selected = [row for row in rows if in_scope(row, scope)]
    n = len(selected)
    return {
        "section": "scope_summary",
        "scope": scope,
        "scope_label": label,
        "n": n,
        "qwen3_correct": sum(bool(row["qwen3_4b_banglish_correct"]) for row in selected),
        "qwen3_D": sum(bool(row["qwen3_D"]) for row in selected),
        "qwen3_wrong_D": sum(bool(row["qwen3_wrong_D"]) for row in selected),
        "qwen3_same_as_q25_agreement": sum(bool(row["qwen3_same_as_q25_agreement"]) for row in selected),
        "qwen3_switches_from_q25_agreement": sum(bool(row["qwen3_switches_from_q25_agreement"]) for row in selected),
        "qwen3_invalid": sum(bool(row["qwen3_invalid"]) for row in selected),
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [summarize_scope(item_rows, scope, label) for scope, label in SCOPES]


def row_for(rows: list[dict[str, Any]], scope: str) -> dict[str, Any]:
    matches = [row for row in rows if row["scope"] == scope]
    if len(matches) != 1:
        raise SystemExit(f"Expected one summary row for {scope}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    agree = row_for(summary_rows, "q25_agree")
    agree_non_d = row_for(summary_rows, "q25_agree_non_d")
    correct_non_d = row_for(summary_rows, "q25_correct_agree_non_d")
    correct_d = row_for(summary_rows, "q25_correct_agree_d")

    lines = [
        "# Frozen-V5 BEnQA Cross-Model Banglish-Agreement Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit asks how Qwen3-4B behaves on reviewed Banglish",
        "BEnQA items where the two Qwen2.5 thesis rows agree on the same",
        "reviewed-Banglish option. Unlike the cross-script agreement audit,",
        "this holds the script fixed and varies only the model row.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- The two Qwen2.5 rows agree on a reviewed-Banglish option in "
            f"{agree['n']}/144 BEnQA items; {agree_non_d['n']} of those agreements are non-D."
        ),
        (
            "- When the Qwen2.5 rows agree on a non-D reviewed-Banglish option, "
            f"Qwen3-4B predicts D on {agree_non_d['qwen3_D']}/{agree_non_d['n']} rows "
            f"({percent(int(agree_non_d['qwen3_D']), int(agree_non_d['n']))}) and wrong D on "
            f"{agree_non_d['qwen3_wrong_D']}/{agree_non_d['n']} rows."
        ),
        (
            "- In the stricter slice where both Qwen2.5 rows are correct and agree "
            f"on the same non-D option, Qwen3-4B is wrong-D on "
            f"{correct_non_d['qwen3_wrong_D']}/{correct_non_d['n']} rows and matches the "
            f"Qwen2.5 agreement on {correct_non_d['qwen3_same_as_q25_agreement']}/"
            f"{correct_non_d['n']} rows."
        ),
        (
            "- When both Qwen2.5 rows are correct and agree on D, Qwen3-4B also "
            f"predicts D on {correct_d['qwen3_D']}/{correct_d['n']} rows."
        ),
        "",
        "## Summary",
        "",
        "| Scope | N | Qwen3 correct | Qwen3 D | Qwen3 wrong D | Same as Qwen2.5 agreement | Switches from agreement | Qwen3 invalid |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for scope, _label in SCOPES:
        row = row_for(summary_rows, scope)
        lines.append(
            f"| {row['scope_label']} | {row['n']} | {row['qwen3_correct']} | "
            f"{row['qwen3_D']} | {row['qwen3_wrong_D']} | "
            f"{row['qwen3_same_as_q25_agreement']} | "
            f"{row['qwen3_switches_from_q25_agreement']} | {row['qwen3_invalid']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The result isolates a model-specific reviewed-Banglish failure mode:",
            "  the same Banglish items can support non-D agreement for both Qwen2.5",
            "  rows while Qwen3 still falls into D.",
            "- The strict correct-non-D slice is small, so use it as corroborating",
            "  evidence beside the larger cross-script option-agreement and",
            "  option-switching audits.",
            "- This remains behavioral evidence over fixed outputs; it does not claim",
            "  an internal mechanism or a deployable mitigation.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_cross_model_banglish_agreement.py`",
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
    item_rows = build_item_rows(read_csv(args.input))
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    print(
        f"wrote {len(item_rows)} item rows and {len(summary_rows)} summary rows to "
        f"{args.items_output} / {args.summary_output}"
    )


if __name__ == "__main__":
    main()
