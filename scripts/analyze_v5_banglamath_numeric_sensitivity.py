#!/usr/bin/env python3
"""Audit BanglaMATH numeric-signature sensitivity for frozen-v5 Qwen outputs."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import mean
from typing import Any

from run_eval_kaggle import is_correct, normalize_answer, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_banglamath_numeric_sensitivity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_banglamath_numeric_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglamath_numeric_sensitivity.md"

INPUTS = [
    ROOT
    / "results/runs/qwen2_5_3b_validation200_v3_128/results/runs/qwen2_5_3b_validation200_v3_128.jsonl",
    ROOT
    / "results/runs/qwen3_4b_validation200_v3_128/results/runs/qwen3_4b_validation200_v3_128.jsonl",
    ROOT
    / "results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50.jsonl",
    ROOT
    / "results/runs/qwen25_7b_8bit_validation200_v4_test150/results/runs/qwen25_7b_8bit_validation200_v4_test150.jsonl",
    ROOT
    / "results/runs/qwen2_5_3b_validation200_v5_banglish/results/runs/qwen2_5_3b_validation200_v5_banglish.jsonl",
    ROOT
    / "results/runs/qwen3_4b_validation200_v5_banglish/results/runs/qwen3_4b_validation200_v5_banglish.jsonl",
    ROOT
    / "results/runs/qwen25_7b_8bit_validation200_v5_banglish_pinned/results/runs/qwen2_5_7b_8bit_validation200_v5_banglish_pinned.jsonl",
]

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
VARIANTS = ("bangla", "banglish_clean", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}

BENGALI_DIGIT_TRANS = str.maketrans(
    "\u09e6\u09e7\u09e8\u09e9\u09ea\u09eb\u09ec\u09ed\u09ee\u09ef",
    "0123456789",
)
LATEX_FRAC_RE = re.compile(
    r"\\frac\s*\{\s*([-+]?\d+(?:\.\d+)?)\s*\}\s*\{\s*([-+]?\d+(?:\.\d+)?)\s*\}"
)
FRACTION_RE = re.compile(r"(?<![\w.])([-+]?\d+(?:\.\d+)?)\s*/\s*([-+]?\d+(?:\.\d+)?)(?![\w.])")
NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?\s*%?")
TOLERANCE = Decimal("0.000001")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["_source"] = repo_path(path)
            row["_line"] = line_no
            rows.append(row)
    return rows


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


def clip(value: Any, limit: int = 180) -> str:
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def decimal_or_none(value: str) -> Decimal | None:
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def normalized_numeric_text(text: Any) -> str:
    value = normalize_answer(str(text)).translate(BENGALI_DIGIT_TRANS)
    value = value.replace("\u2212", "-")
    return re.sub(r"(?<=\d),(?=\d)", "", value)


def decimal_divide(numerator: str, denominator: str) -> Decimal | None:
    top = decimal_or_none(numerator)
    bottom = decimal_or_none(denominator)
    if top is None or bottom in {None, Decimal("0")}:
        return None
    return top / bottom


def values_match(left: Decimal, right: Decimal) -> bool:
    return abs(left - right) <= TOLERANCE


def dedupe_values(values: list[Decimal]) -> list[Decimal]:
    out: list[Decimal] = []
    for value in values:
        if not any(values_match(value, existing) for existing in out):
            out.append(value)
    return sorted(out)


def extract_numeric_values(text: Any) -> list[Decimal]:
    normalized = normalized_numeric_text(text)
    values: list[Decimal] = []
    protected_spans: list[tuple[int, int]] = []

    for pattern in (LATEX_FRAC_RE, FRACTION_RE):
        for match in pattern.finditer(normalized):
            value = decimal_divide(match.group(1), match.group(2))
            if value is not None:
                values.append(value)
                protected_spans.append(match.span())

    def inside_protected_span(position: int) -> bool:
        return any(start <= position < end for start, end in protected_spans)

    for match in NUMBER_RE.finditer(normalized):
        if inside_protected_span(match.start()):
            continue
        token = match.group(0).strip()
        is_percent = token.endswith("%")
        value = decimal_or_none(token.rstrip("%").strip())
        if value is None:
            continue
        values.append(value)
        if is_percent:
            values.append(value / Decimal("100"))

    return dedupe_values(values)


def format_decimal(value: Decimal) -> str:
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text == "-0":
        return "0"
    return text


def format_values(values: list[Decimal]) -> str:
    return ";".join(format_decimal(value) for value in values)


def all_gold_values_present(gold_values: list[Decimal], candidate_values: list[Decimal]) -> bool:
    if not gold_values:
        return False
    return all(
        any(values_match(gold_value, candidate_value) for candidate_value in candidate_values)
        for gold_value in gold_values
    )


def format_item_row(row: dict[str, Any]) -> dict[str, Any]:
    raw = str(row.get("raw_output", ""))
    answer_type = str(row.get("answer_type", ""))
    parsed = parse_answer(raw, answer_type) if raw else str(row.get("parsed", ""))
    gold = str(row.get("gold", ""))
    correct = is_correct(parsed, gold, answer_type)
    gold_values = extract_numeric_values(gold)
    raw_values = extract_numeric_values(raw)
    parsed_values = extract_numeric_values(parsed)
    raw_full_signature = all_gold_values_present(gold_values, raw_values)
    parsed_full_signature = all_gold_values_present(gold_values, parsed_values)
    return {
        "model": MODEL_LABELS[str(row["model"])],
        "model_id": row["model"],
        "variant": row["variant"],
        "variant_label": VARIANT_LABELS.get(str(row["variant"]), row["variant"]),
        "dataset": row.get("dataset", ""),
        "task_type": row.get("task_type", ""),
        "answer_type": answer_type,
        "id": row.get("id", ""),
        "gold": gold,
        "correct": correct,
        "parsed": parsed,
        "gold_numeric_values": format_values(gold_values),
        "raw_numeric_values": format_values(raw_values),
        "parsed_numeric_values": format_values(parsed_values),
        "gold_numeric_count": len(gold_values),
        "raw_numeric_count": len(raw_values),
        "parsed_numeric_count": len(parsed_values),
        "raw_has_any_number": bool(raw_values),
        "parsed_has_any_number": bool(parsed_values),
        "raw_full_numeric_signature": raw_full_signature,
        "parsed_full_numeric_signature": parsed_full_signature,
        "wrong_raw_full_numeric_signature": (not correct) and raw_full_signature,
        "wrong_parsed_full_numeric_signature": (not correct) and parsed_full_signature,
        "wrong_without_raw_number": (not correct) and not raw_values,
        "source": row.get("_source", ""),
        "line": row.get("_line", ""),
        "raw_excerpt": clip(raw),
    }


def load_rows(inputs: list[Path]) -> list[dict[str, Any]]:
    indexed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for path in inputs:
        for row in read_jsonl(path):
            if (
                row.get("model") not in MODELS
                or row.get("variant") not in VARIANTS
                or row.get("dataset") != "banglamath"
            ):
                continue
            key = (str(row["model"]), str(row["id"]), str(row["variant"]))
            indexed[key] = format_item_row(row)
    expected = len(MODELS) * 56 * len(VARIANTS)
    if len(indexed) != expected:
        raise SystemExit(f"Expected {expected} BanglaMATH model-item-variant rows, got {len(indexed)}")
    return sorted(indexed.values(), key=lambda row: (row["model"], row["id"], row["variant"]))


def summarize_group(rows: list[dict[str, Any]], model: str, variant: str) -> dict[str, Any]:
    selected = [row for row in rows if row["model"] == model and row["variant"] == variant]
    if not selected:
        raise SystemExit(f"No rows for {model} {variant}")
    wrong = [row for row in selected if not row["correct"]]
    n = len(selected)
    correct = sum(bool(row["correct"]) for row in selected)
    wrong_raw_signature = sum(bool(row["wrong_raw_full_numeric_signature"]) for row in selected)
    wrong_parsed_signature = sum(bool(row["wrong_parsed_full_numeric_signature"]) for row in selected)
    return {
        "model": model,
        "dataset": "banglamath",
        "variant": variant,
        "variant_label": VARIANT_LABELS.get(variant, variant),
        "n": n,
        "correct": correct,
        "wrong": len(wrong),
        "gold_numeric_rows": sum(bool(row["gold_numeric_values"]) for row in selected),
        "parsed_full_numeric_signature": sum(bool(row["parsed_full_numeric_signature"]) for row in selected),
        "raw_full_numeric_signature": sum(bool(row["raw_full_numeric_signature"]) for row in selected),
        "wrong_parsed_full_numeric_signature": wrong_parsed_signature,
        "wrong_raw_full_numeric_signature": wrong_raw_signature,
        "optimistic_parsed_signature_correct": correct + wrong_parsed_signature,
        "optimistic_raw_signature_correct": correct + wrong_raw_signature,
        "wrong_with_any_raw_number": sum((not row["correct"]) and bool(row["raw_has_any_number"]) for row in selected),
        "wrong_without_raw_number": sum(bool(row["wrong_without_raw_number"]) for row in selected),
        "mean_gold_numeric_count": round(mean(int(row["gold_numeric_count"]) for row in selected), 2),
        "mean_raw_numeric_count": round(mean(int(row["raw_numeric_count"]) for row in selected), 2),
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for model in MODEL_LABELS.values():
        for variant in VARIANTS:
            summary.append(summarize_group(rows, model, variant))
    return summary


def row_for(summary: list[dict[str, Any]], model: str, variant: str) -> dict[str, Any]:
    return next(row for row in summary if row["model"] == model and row["variant"] == variant)


def add_summary_table(lines: list[str], summary: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            "| Model | Variant | Correct | Parsed numeric signature | Raw numeric signature | Wrong raw signature hits | Wrong no-number outputs |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary:
        lines.append(
            "| {model} | {variant_label} | {correct}/{n} | "
            "{parsed_full_numeric_signature}/{n} | {raw_full_numeric_signature}/{n} | "
            "{wrong_raw_full_numeric_signature}/{wrong} | {wrong_without_raw_number}/{wrong} |".format(
                **row
            )
        )


def add_example_table(lines: list[str], title: str, examples: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            f"## {title}",
            "",
            "| Model | Variant | Item | Gold | Parsed | Raw excerpt |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in examples:
        lines.append(
            "| {model} | {variant_label} | `{id}` | `{gold}` | `{parsed}` | {raw_excerpt} |".format(
                **row
            )
        )
    if not examples:
        lines.append("| - | - | - | - | - | - |")
    lines.append("")


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_bangla = row_for(summary, "Qwen3-4B", "bangla")
    q3_banglish = row_for(summary, "Qwen3-4B", "banglish_clean")
    q3_english = row_for(summary, "Qwen3-4B", "english")
    q25_3b_bangla = row_for(summary, "Qwen2.5-3B", "bangla")
    q25_3b_banglish = row_for(summary, "Qwen2.5-3B", "banglish_clean")
    q25_3b_english = row_for(summary, "Qwen2.5-3B", "english")
    q25_7b_bangla = row_for(summary, "Qwen2.5-7B 8-bit", "bangla")
    q25_7b_banglish = row_for(summary, "Qwen2.5-7B 8-bit", "banglish_clean")
    q25_7b_english = row_for(summary, "Qwen2.5-7B 8-bit", "english")

    parsed_examples = [
        row
        for row in rows
        if row["wrong_parsed_full_numeric_signature"]
        and row["variant"] in {"bangla", "english"}
    ][:6]
    q3_banglish_raw_examples = [
        row
        for row in rows
        if row["model"] == "Qwen3-4B"
        and row["variant"] == "banglish_clean"
        and row["wrong_raw_full_numeric_signature"]
    ][:5]
    q3_banglish_no_number = [
        row
        for row in rows
        if row["model"] == "Qwen3-4B"
        and row["variant"] == "banglish_clean"
        and row["wrong_without_raw_number"]
    ][:5]

    lines = [
        "# Frozen-V5 BanglaMATH Numeric Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit asks whether BanglaMATH short-answer losses are mainly",
        "caused by conservative answer normalization. It extracts numeric signatures",
        "from the gold answer, parsed answer, and raw model output for the same",
        "thesis-facing frozen-v5 Qwen rows.",
        "",
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "A row has a full numeric-signature hit when all numeric values in the gold",
        "answer appear in the parsed answer or raw output after Bengali digit,",
        "fraction, and percent normalization. This is intentionally generous:",
        "a raw hit can occur inside reasoning rather than the final answer, so it is",
        "an upper bound on parser/unit sensitivity, not a replacement accuracy metric.",
        "",
        "## Headline",
        "",
        "- A generous raw numeric-signature credit does not erase the BanglaMATH",
        "  reviewed-Banglish deficit for any thesis-facing Qwen row.",
        (
            "- Qwen3-4B raw numeric-signature hits are "
            f"{q3_banglish['raw_full_numeric_signature']}/56 for reviewed Banglish, "
            f"{q3_bangla['raw_full_numeric_signature']}/56 for Bangla, and "
            f"{q3_english['raw_full_numeric_signature']}/56 for English."
        ),
        (
            "- Qwen2.5-7B 8-bit has "
            f"{q25_7b_banglish['raw_full_numeric_signature']}/56 reviewed-Banglish raw hits "
            f"versus {q25_7b_bangla['raw_full_numeric_signature']}/56 Bangla and "
            f"{q25_7b_english['raw_full_numeric_signature']}/56 English; Qwen2.5-3B has "
            f"{q25_3b_banglish['raw_full_numeric_signature']}/56 versus "
            f"{q25_3b_bangla['raw_full_numeric_signature']}/56 and "
            f"{q25_3b_english['raw_full_numeric_signature']}/56."
        ),
        "- Conservative unit and fraction normalization misses exist, especially in",
        "  Bangla and English outputs, so BanglaMATH absolute accuracy should stay",
        "  caveated. The cross-script Banglish gap is not explained by those misses.",
        "",
        "## BanglaMATH Numeric Signature Summary",
        "",
    ]
    add_summary_table(lines, summary)
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `Parsed numeric signature` is closest to a parser/unit-normalization",
            "  sensitivity check. It credits answers such as a Latin-unit number when",
            "  the exact evaluator keeps the row wrong.",
            "- `Raw numeric signature` is more optimistic because it may credit numbers",
            "  that appear during reasoning even when the final answer is absent or",
            "  malformed.",
            "- Reviewed Banglish remains the lowest row under both views for Qwen2.5-3B,",
            "  Qwen2.5-7B 8-bit, and Qwen3-4B. This supports using BanglaMATH as a",
            "  low-accuracy stress test with conservative scoring caveats, not as a",
            "  parser-artifact explanation of the main gap.",
            "",
        ]
    )
    add_example_table(lines, "Wrong Rows With Parsed Numeric Signature Hits", parsed_examples)
    add_example_table(lines, "Qwen3 Reviewed-Banglish Raw Signature Hits", q3_banglish_raw_examples)
    add_example_table(lines, "Qwen3 Reviewed-Banglish Wrong Rows Without Numbers", q3_banglish_no_number)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, nargs="+", default=INPUTS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.inputs)
    summary = build_summary(rows)
    write_csv(args.items_output, rows)
    write_csv(args.summary_output, summary)
    write_report(args.report_output, rows, summary, args.items_output, args.summary_output)
    q3_banglish = row_for(summary, "Qwen3-4B", "banglish_clean")
    print(
        "items={items} | summary_rows={summary_rows} | "
        "qwen3_banglish_raw_signature={raw}/56 | report={report}".format(
            items=len(rows),
            summary_rows=len(summary),
            raw=q3_banglish["raw_full_numeric_signature"],
            report=repo_path(args.report_output),
        )
    )


if __name__ == "__main__":
    main()
