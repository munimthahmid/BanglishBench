#!/usr/bin/env python3
"""Audit structural preservation across frozen-v5 source variants."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_source_variant_structural_parity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_source_variant_structural_parity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_source_variant_structural_parity.md"

VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}
COMPARISONS = (
    ("bangla_vs_banglish", "bangla", "banglish_clean", "primary"),
    ("bangla_vs_english", "bangla", "english", "diagnostic"),
    ("banglish_vs_english", "banglish_clean", "english", "diagnostic"),
)

DIGIT_SEQUENCE_RE = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
OPTION_RE = re.compile(r"^\s*([A-D])[\).]\s+", flags=re.MULTILINE)
MCQ_INSTRUCTION_RE = re.compile(
    r"Answer\s+with\s+only\s+A,\s*B,\s*C,\s*or\s*D\.", flags=re.IGNORECASE
)
FINAL_ANSWER_RE = re.compile(r"Return\s+only\s+the\s+final\s+answer\.", flags=re.IGNORECASE)
OTHER_ANSWER_RE = re.compile(r"\banswer\b|উত্তর|final\s+answer", flags=re.IGNORECASE)
DIGIT_TRANS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

LATEX_COMMAND_RE = re.compile(r"\\[A-Za-z]+")
CHEMICAL_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:[A-Z][a-z]?(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\}|\d+)*){2,}"
    r"(?![A-Za-z0-9_])"
)
ANNOTATED_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])\d+(?:\.\d+)?[A-Za-z]?"
    r"(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})+"
)
ANNOTATED_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9_])[A-Za-z]{1,4}"
    r"(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})+"
    r"(?![A-Za-z0-9_])"
)
FRACTION_RE = re.compile(r"(?<![0-9.])\d+/\d+(?![0-9.])")
ARITHMETIC_EXPR_RE = re.compile(r"(?<![0-9.])\d+(?:\.\d+)?(?:[-+*/=]\d+(?:\.\d+)?)+(?![0-9.])")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def normalize_digits(text: str) -> list[str]:
    normalized_text = text.translate(DIGIT_TRANS)
    return [match.replace(",", "") for match in DIGIT_SEQUENCE_RE.findall(normalized_text)]


def option_labels(text: str) -> list[str]:
    return OPTION_RE.findall(text)


def instruction_signature(text: str) -> str:
    signatures = []
    if MCQ_INSTRUCTION_RE.search(text):
        signatures.append("mcq_letters")
    if FINAL_ANSWER_RE.search(text):
        signatures.append("final_answer")
    if not signatures and OTHER_ANSWER_RE.search(text):
        signatures.append("other_answer_marker")
    return "+".join(signatures) if signatures else "none"


def normalize_formula_token(token: str) -> str:
    return token.translate(DIGIT_TRANS).replace(" ", "")


def formula_tokens(text: str) -> list[str]:
    normalized_text = text.translate(DIGIT_TRANS)
    tokens: list[str] = []
    for regex in (
        LATEX_COMMAND_RE,
        CHEMICAL_TOKEN_RE,
        ANNOTATED_NUMBER_RE,
        ANNOTATED_UNIT_RE,
        FRACTION_RE,
        ARITHMETIC_EXPR_RE,
    ):
        tokens.extend(normalize_formula_token(token) for token in regex.findall(normalized_text))
    return sorted(tokens)


def compare_item(row: dict[str, Any], comparison: tuple[str, str, str, str]) -> dict[str, Any]:
    comparison_name, left_variant, right_variant, role = comparison
    left_text = str(row.get(left_variant, ""))
    right_text = str(row.get(right_variant, ""))
    left_options = option_labels(left_text)
    right_options = option_labels(right_text)
    left_digits = normalize_digits(left_text)
    right_digits = normalize_digits(right_text)
    left_formulas = formula_tokens(left_text)
    right_formulas = formula_tokens(right_text)
    left_instruction = instruction_signature(left_text)
    right_instruction = instruction_signature(right_text)

    option_labels_preserved = left_options == right_options
    digit_sequence_preserved = left_digits == right_digits
    formula_tokens_preserved = left_formulas == right_formulas
    answer_instruction_preserved = left_instruction == right_instruction
    structural_mismatch = not (
        option_labels_preserved
        and digit_sequence_preserved
        and formula_tokens_preserved
        and answer_instruction_preserved
    )

    mismatch_codes = []
    if not option_labels_preserved:
        mismatch_codes.append("options")
    if not digit_sequence_preserved:
        mismatch_codes.append("digits")
    if not formula_tokens_preserved:
        mismatch_codes.append("formulas")
    if not answer_instruction_preserved:
        mismatch_codes.append("instruction")

    return {
        "id": row.get("id", ""),
        "dataset": row.get("dataset", ""),
        "task_type": row.get("task_type", ""),
        "domain": row.get("domain", ""),
        "quality_status": row.get("quality_status", ""),
        "comparison": comparison_name,
        "comparison_role": role,
        "left_variant": left_variant,
        "right_variant": right_variant,
        "left_option_labels": " ".join(left_options),
        "right_option_labels": " ".join(right_options),
        "option_labels_preserved": option_labels_preserved,
        "left_digit_sequence": " ".join(left_digits),
        "right_digit_sequence": " ".join(right_digits),
        "digit_sequence_preserved": digit_sequence_preserved,
        "left_formula_tokens": " ".join(left_formulas),
        "right_formula_tokens": " ".join(right_formulas),
        "formula_tokens_preserved": formula_tokens_preserved,
        "left_answer_instruction": left_instruction,
        "right_answer_instruction": right_instruction,
        "answer_instruction_preserved": answer_instruction_preserved,
        "structural_mismatch": structural_mismatch,
        "primary_pair_hard_fail": role == "primary" and structural_mismatch,
        "diagnostic_warning": role == "diagnostic" and structural_mismatch,
        "mismatch_codes": " ".join(mismatch_codes),
        "left_preview": left_text[:180].replace("\n", " "),
        "right_preview": right_text[:180].replace("\n", " "),
    }


def group_specs(item_rows: list[dict[str, Any]]) -> list[tuple[str, str]]:
    datasets = sorted({str(row["dataset"]) for row in item_rows})
    specs = [("all", "all")]
    for dataset in datasets:
        specs.append((dataset, "all"))
        task_types = sorted(
            {str(row["task_type"]) for row in item_rows if row["dataset"] == dataset}
        )
        for task_type in task_types:
            specs.append((dataset, task_type))
    return specs


def filtered_rows(
    rows: list[dict[str, Any]], comparison: str, dataset: str, task_type: str
) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["comparison"] == comparison]
    if dataset != "all":
        selected = [row for row in selected if row["dataset"] == dataset]
    if task_type != "all":
        selected = [row for row in selected if row["task_type"] == task_type]
    return selected


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    specs = group_specs(rows)
    for comparison_name, left_variant, right_variant, role in COMPARISONS:
        for dataset, task_type in specs:
            selected = filtered_rows(rows, comparison_name, dataset, task_type)
            if not selected:
                continue
            mismatch_counter: Counter[str] = Counter()
            for row in selected:
                mismatch_counter.update(row["mismatch_codes"].split())
            n = len(selected)
            summary.append(
                {
                    "comparison": comparison_name,
                    "comparison_role": role,
                    "left_variant": left_variant,
                    "right_variant": right_variant,
                    "dataset": dataset,
                    "task_type": task_type,
                    "n": n,
                    "structural_mismatch": sum(int(row["structural_mismatch"]) for row in selected),
                    "primary_pair_hard_fail": sum(
                        int(row["primary_pair_hard_fail"]) for row in selected
                    ),
                    "diagnostic_warning": sum(int(row["diagnostic_warning"]) for row in selected),
                    "option_label_mismatch": sum(
                        int(not row["option_labels_preserved"]) for row in selected
                    ),
                    "digit_sequence_mismatch": sum(
                        int(not row["digit_sequence_preserved"]) for row in selected
                    ),
                    "formula_token_mismatch": sum(
                        int(not row["formula_tokens_preserved"]) for row in selected
                    ),
                    "answer_instruction_mismatch": sum(
                        int(not row["answer_instruction_preserved"]) for row in selected
                    ),
                    "mismatch_rate": round(
                        sum(int(row["structural_mismatch"]) for row in selected) / n, 4
                    ),
                    "mismatch_codes": " ".join(
                        f"{key}:{count}" for key, count in sorted(mismatch_counter.items())
                    ),
                }
            )
    return summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def find_summary(
    rows: list[dict[str, Any]], comparison: str, dataset: str, task_type: str
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["comparison"] == comparison
        and row["dataset"] == dataset
        and row["task_type"] == task_type
    )


def write_report(
    report_path: Path,
    input_path: Path,
    items_path: Path,
    summary_path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    primary_all = find_summary(summary_rows, "bangla_vs_banglish", "all", "all")
    english_all = find_summary(summary_rows, "bangla_vs_english", "all", "all")
    banglish_english_all = find_summary(summary_rows, "banglish_vs_english", "all", "all")
    primary_failures = [
        row for row in item_rows if row["comparison"] == "bangla_vs_banglish" and row["structural_mismatch"]
    ]
    diagnostic_warnings = [
        row for row in item_rows if row["comparison_role"] == "diagnostic" and row["structural_mismatch"]
    ]

    lines = [
        "# V5 Source-Variant Structural Parity Audit",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Frozen v5 slice: `{repo_path(input_path)}`",
        f"- Item audit CSV: `{repo_path(items_path)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        "",
        "## Headline",
        "",
        (
            "- Bangla vs reviewed Banglish has "
            f"{primary_all['structural_mismatch']}/{primary_all['n']} structural mismatches "
            f"and {primary_all['primary_pair_hard_fail']} primary hard-fail rows across "
            "option labels, digit sequences, formula-like tokens, and answer instructions."
        ),
        (
            "- Bangla vs English has "
            f"{english_all['structural_mismatch']}/{english_all['n']} diagnostic warnings; "
            "these are retained as source-translation caveats, not as the main paired claim."
        ),
        (
            "- Reviewed Banglish vs English has "
            f"{banglish_english_all['structural_mismatch']}/{banglish_english_all['n']} "
            "diagnostic warnings."
        ),
        "",
        "## Summary",
        "",
        "| Comparison | Role | Dataset | Task type | n | Mismatch | Options | Digits | Formulas | Instruction |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {comparison} | {comparison_role} | {dataset} | {task_type} | {n} | "
            "{structural_mismatch} | {option_label_mismatch} | {digit_sequence_mismatch} | "
            "{formula_token_mismatch} | {answer_instruction_mismatch} |".format(**row)
        )

    if primary_failures:
        lines.extend(["", "## Primary Pair Hard Fails", ""])
        for row in primary_failures[:25]:
            lines.append(
                f"- `{row['id']}` `{row['dataset']}` codes={row['mismatch_codes']} "
                f"left_digits=`{row['left_digit_sequence']}` right_digits=`{row['right_digit_sequence']}`"
            )
    else:
        lines.extend(
            [
                "",
                "## Primary Pair Hard Fails",
                "",
                "None. This supports using Bangla vs reviewed Banglish as the",
                "primary paired comparison without a structural source-mismatch",
                "exclusion rule.",
            ]
        )

    if diagnostic_warnings:
        lines.extend(["", "## First Diagnostic Warnings", ""])
        for row in diagnostic_warnings[:20]:
            lines.append(
                f"- `{row['id']}` `{row['comparison']}` codes={row['mismatch_codes']} "
                f"left_digits=`{row['left_digit_sequence']}` right_digits=`{row['right_digit_sequence']}`"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The strict preservation gate is applied to the Bangla-vs-reviewed-Banglish",
            "source pair because that pair carries the main script-robustness claim.",
            "English is still valuable privileged diagnostic evidence, but the source",
            "English field can contain upstream translation differences; structural",
            "warnings in English comparisons should be cited as caveats rather than",
            "used to discard the primary Bangla-vs-Banglish result.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    item_rows = [
        compare_item(row, comparison)
        for row in rows
        for comparison in COMPARISONS
    ]
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        args.input,
        args.items_output,
        args.summary_output,
        item_rows,
        summary_rows,
    )
    primary_failures = sum(int(row["primary_pair_hard_fail"]) for row in item_rows)
    diagnostic_warnings = sum(int(row["diagnostic_warning"]) for row in item_rows)
    print(
        " | ".join(
            [
                f"item_rows={len(item_rows)}",
                f"summary_rows={len(summary_rows)}",
                f"primary_pair_hard_fail={primary_failures}",
                f"diagnostic_warnings={diagnostic_warnings}",
                f"report={args.report_output}",
            ]
        )
    )


if __name__ == "__main__":
    main()
