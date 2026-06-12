#!/usr/bin/env python3
"""Generic analyzer for paid API audit results."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from analyze_gemini_api_audit_results import (
    DATASETS,
    VARIANTS,
    VARIANT_LABELS,
    build_item_rows,
    exact_binomial_two_sided,
    paired_rows,
    read_jsonl,
    recoverability_rows,
    repo_path,
    summarize,
    summary_lookup,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPORTED = ROOT / "results/analysis/openai_gpt55_low_diagnostic_60_v5_imported.jsonl"
DEFAULT_RAW = ROOT / "results/api_audit/openai_gpt55_low_diagnostic_60_v5_raw.jsonl"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/openai_gpt55_low_diagnostic_60_v5_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/openai_gpt55_low_diagnostic_60_v5_summary.csv"
DEFAULT_PAIRED_OUTPUT = ROOT / "results/analysis/openai_gpt55_low_diagnostic_60_v5_paired_gaps.csv"
DEFAULT_RECOVERY_OUTPUT = ROOT / "results/analysis/openai_gpt55_low_diagnostic_60_v5_recoverability_items.csv"
DEFAULT_COMPARISON_OUTPUT = ROOT / "results/analysis/openai_gpt55_low_diagnostic_60_v5_gemini_comparison.csv"
DEFAULT_REPORT = ROOT / "reports/openai_gpt55_low_diagnostic_60_v5_results.md"
DEFAULT_REFERENCE_ITEMS = ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_items.csv"


def pct(count: int, n: int) -> str:
    if not n:
        return "0.0%"
    return f"{100 * count / n:.1f}%"


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def optional_int(value: Any) -> int:
    if value in ("", None):
        return 0
    return int(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def format_accuracy(summary: list[dict[str, Any]], dataset: str, variant: str, key: str) -> str:
    row = summary_lookup(summary, dataset, variant)
    correct = int(row[key])
    n = int(row["n"])
    return f"{correct}/{n} ({pct(correct, n)})"


def reference_rows_for_requests(
    reference_items_path: Path,
    request_ids: set[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(reference_items_path):
        if row.get("request_id") not in request_ids:
            continue
        converted: dict[str, Any] = dict(row)
        for key in ("strict_correct", "secondary_correct", "parsed_empty", "choice_invalid", "raw_multiline", "long_response_gt120"):
            converted[key] = as_bool(converted.get(key, ""))
        for key in ("raw_chars", "raw_line_count", "usage_input_tokens", "usage_output_tokens", "usage_total_tokens"):
            converted[key] = optional_int(converted.get(key, ""))
        rows.append(converted)
    return rows


def compact_model_summary(
    model_label: str,
    summary: list[dict[str, Any]],
    score_mode: str,
) -> dict[str, Any]:
    key = "strict_correct" if score_mode == "strict" else "secondary_correct"
    n = int(summary_lookup(summary, "all", "bangla")["n"])
    bangla = int(summary_lookup(summary, "all", "bangla")[key])
    banglish = int(summary_lookup(summary, "all", "banglish_clean")[key])
    english = int(summary_lookup(summary, "all", "english")[key])
    return {
        "model": model_label,
        "score_mode": score_mode,
        "n": n,
        "bangla": bangla,
        "banglish_clean": banglish,
        "english": english,
        "banglish_minus_bangla_points": round(100 * (banglish - bangla) / n, 1) if n else 0.0,
        "banglish_minus_english_points": round(100 * (banglish - english) / n, 1) if n else 0.0,
    }


def build_comparison_rows(
    model_label: str,
    summary: list[dict[str, Any]],
    reference_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if reference_items:
        reference_summary = summarize(reference_items)
        rows.append(compact_model_summary("Gemini 3.5 Flash", reference_summary, "strict"))
        rows.append(compact_model_summary("Gemini 3.5 Flash", reference_summary, "secondary"))
    rows.append(compact_model_summary(model_label, summary, "strict"))
    rows.append(compact_model_summary(model_label, summary, "secondary"))
    return rows


def matched_model_delta_rows(
    model_rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    model_label: str,
) -> list[dict[str, Any]]:
    if not reference_rows:
        return []
    reference_by_request = {str(row["request_id"]): row for row in reference_rows}
    output: list[dict[str, Any]] = []
    for score_mode, key in (("strict", "strict_correct"), ("secondary", "secondary_correct")):
        for variant in VARIANTS:
            paired = [
                (row, reference_by_request[str(row["request_id"])])
                for row in model_rows
                if row["variant"] == variant and str(row["request_id"]) in reference_by_request
            ]
            model_correct = sum(as_bool(row[key]) for row, _ in paired)
            reference_correct = sum(as_bool(ref[key]) for _, ref in paired)
            model_only = sum(as_bool(row[key]) and not as_bool(ref[key]) for row, ref in paired)
            reference_only = sum(not as_bool(row[key]) and as_bool(ref[key]) for row, ref in paired)
            discordant = model_only + reference_only
            n = len(paired)
            output.append(
                {
                    "score_mode": score_mode,
                    "variant": variant,
                    "variant_label": VARIANT_LABELS[variant],
                    "n": n,
                    "model": model_label,
                    "reference_model": "Gemini 3.5 Flash",
                    "model_correct": model_correct,
                    "reference_correct": reference_correct,
                    "model_minus_reference_points": round(100 * (model_correct - reference_correct) / n, 1)
                    if n
                    else 0.0,
                    "model_only": model_only,
                    "reference_only": reference_only,
                    "exact_binomial_p_two_sided": exact_binomial_two_sided(reference_only, discordant),
                }
            )
    return output


def write_comparison_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    write_csv(path, rows)


def write_report(
    path: Path,
    model_label: str,
    report_title: str,
    scope_description: str,
    cost_label: str,
    input_cost_per_mtok: float,
    output_cost_per_mtok: float,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    paired: list[dict[str, Any]],
    recoveries: list[dict[str, Any]],
    comparison: list[dict[str, Any]],
    matched_delta: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
    paired_output: Path,
    recovery_output: Path,
    comparison_output: Path,
    raw_path: Path,
    imported_path: Path,
) -> None:
    finish_counts = Counter(str(row["finish_reason"]) for row in rows)
    key_counts = Counter(str(row["key_name"]) for row in rows)
    recovery_counts = Counter(str(row["secondary_reason"]) for row in recoveries)
    input_tokens = sum(optional_int(row.get("usage_input_tokens")) for row in rows)
    output_tokens = sum(optional_int(row.get("usage_output_tokens")) for row in rows)
    reasoning_tokens = sum(optional_int(row.get("usage_thoughts_tokens")) for row in rows)
    total_seconds = sum(float(row.get("seconds") or 0) for row in rows)
    estimated_standard_cost = (
        input_tokens / 1_000_000 * input_cost_per_mtok
        + output_tokens / 1_000_000 * output_cost_per_mtok
    )
    scope_lines = scope_description.splitlines()

    lines = [
        f"# {report_title}",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        *scope_lines,
        "",
        f"- Raw API responses: `{repo_path(raw_path)}`",
        f"- Imported strict rows: `{repo_path(imported_path)}`",
        f"- Item audit CSV: `{repo_path(items_output)}`",
        f"- Summary CSV: `{repo_path(summary_output)}`",
        f"- Paired gap CSV: `{repo_path(paired_output)}`",
        f"- Recoverability CSV: `{repo_path(recovery_output)}`",
        f"- Gemini comparison CSV: `{repo_path(comparison_output)}`",
        "",
        "## Headline",
        "",
        "- Strict accuracy on this evaluation scope is "
        f"{format_accuracy(summary, 'all', 'bangla', 'strict_correct')} Bangla, "
        f"{format_accuracy(summary, 'all', 'banglish_clean', 'strict_correct')} reviewed Banglish, and "
        f"{format_accuracy(summary, 'all', 'english', 'strict_correct')} English.",
        "- Secondary parser/unit sensitivity is "
        f"{format_accuracy(summary, 'all', 'bangla', 'secondary_correct')} Bangla, "
        f"{format_accuracy(summary, 'all', 'banglish_clean', 'secondary_correct')} reviewed Banglish, and "
        f"{format_accuracy(summary, 'all', 'english', 'secondary_correct')} English.",
    ]
    if matched_delta:
        strict_banglish = next(
            row
            for row in matched_delta
            if row["score_mode"] == "strict" and row["variant"] == "banglish_clean"
        )
        secondary_banglish = next(
            row
            for row in matched_delta
            if row["score_mode"] == "secondary" and row["variant"] == "banglish_clean"
        )
        lines.extend(
            [
                "- Against Gemini on the matched Banglish requests, "
                f"{model_label} strict delta is {strict_banglish['model_minus_reference_points']:+.1f} points; "
                f"secondary delta is {secondary_banglish['model_minus_reference_points']:+.1f} points.",
            ]
        )
    lines.extend(
        [
            "",
            "## Accuracy",
            "",
            "| Dataset | Score | Bangla | Reviewed Banglish | English |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for dataset in DATASETS:
        if not any(row["dataset"] == dataset for row in summary):
            continue
        label = "All" if dataset == "all" else ("BEnQA" if dataset == "benqa" else "BanglaMATH")
        lines.append(
            f"| {label} | Strict | {format_accuracy(summary, dataset, 'bangla', 'strict_correct')} | "
            f"{format_accuracy(summary, dataset, 'banglish_clean', 'strict_correct')} | "
            f"{format_accuracy(summary, dataset, 'english', 'strict_correct')} |"
        )
        lines.append(
            f"| {label} | Secondary | {format_accuracy(summary, dataset, 'bangla', 'secondary_correct')} | "
            f"{format_accuracy(summary, dataset, 'banglish_clean', 'secondary_correct')} | "
            f"{format_accuracy(summary, dataset, 'english', 'secondary_correct')} |"
        )

    lines.extend(
        [
            "",
            "## Paired Script Gaps",
            "",
            "| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in paired:
        if row["dataset"] == "all" or row["dataset"] == "banglamath":
            dataset_label = "All" if row["dataset"] == "all" else "BanglaMATH"
            lines.append(
                f"| {row['score_mode']} | {dataset_label} | {row['comparison']} | "
                f"{row['delta_points']:+.1f} | {row['left_only']} | {row['right_only']} | "
                f"{row['exact_binomial_p_two_sided']} |"
            )

    lines.extend(
        [
            "",
            "## Same-Slice Model Comparison",
            "",
            "| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in comparison:
        lines.append(
            f"| {row['model']} | {row['score_mode']} | {row['bangla']}/{row['n']} | "
            f"{row['banglish_clean']}/{row['n']} | {row['english']}/{row['n']} | "
            f"{row['banglish_minus_bangla_points']:+.1f} pts |"
        )

    if matched_delta:
        lines.extend(
            [
                "",
                "## Matched Gemini Delta",
                "",
                "| Score | Variant | Delta | Model-only | Gemini-only | p |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in matched_delta:
            lines.append(
                f"| {row['score_mode']} | {row['variant_label']} | "
                f"{row['model_minus_reference_points']:+.1f} | {row['model_only']} | "
                f"{row['reference_only']} | {row['exact_binomial_p_two_sided']} |"
            )

    lines.extend(
        [
            "",
            "## Format And Cost Signals",
            "",
            f"- Finish reasons: {', '.join(f'{key}={value}' for key, value in sorted(finish_counts.items()))}.",
            f"- Key usage by environment variable name: {', '.join(f'{key}={value}' for key, value in sorted(key_counts.items()))}.",
            f"- Recoverable non-strict rows: {len(recoveries)} total "
            f"({', '.join(f'{key}={value}' for key, value in sorted(recovery_counts.items()))}).",
            f"- Reported input tokens: {input_tokens}.",
            f"- Reported output tokens: {output_tokens}.",
            f"- Reported reasoning tokens: {reasoning_tokens}.",
            f"- Approximate {cost_label} text-token cost: ${estimated_standard_cost:.4f}.",
            f"- Total API wall time summed across requests: {total_seconds:.1f}s.",
            "",
            "| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for variant in VARIANTS:
        row = summary_lookup(summary, "all", variant)
        lines.append(
            f"| {VARIANT_LABELS[variant]} | {row['parsed_empty']} | "
            f"{row['finish_max_tokens']} | {row['long_response_gt120']} | "
            f"{row['mean_output_tokens']} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imported", type=Path, default=DEFAULT_IMPORTED)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--model-label", default="GPT-5.5 low")
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--paired-output", type=Path, default=DEFAULT_PAIRED_OUTPUT)
    parser.add_argument("--recovery-output", type=Path, default=DEFAULT_RECOVERY_OUTPUT)
    parser.add_argument("--comparison-output", type=Path, default=DEFAULT_COMPARISON_OUTPUT)
    parser.add_argument("--reference-items", type=Path, default=DEFAULT_REFERENCE_ITEMS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--report-title")
    parser.add_argument("--cost-label", default="standard GPT-5.5")
    parser.add_argument("--input-cost-per-mtok", type=float, default=5.0)
    parser.add_argument("--output-cost-per-mtok", type=float, default=30.0)
    parser.add_argument(
        "--scope-description",
        default=(
            "This is a targeted frontier-model diagnostic slice, not the final full SOTA\n"
            "audit. It uses the same strict parser as the open-model and Gemini runs,\n"
            "with secondary parser/unit sensitivity reported separately."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    imported_rows = read_jsonl(args.imported)
    raw_rows = read_jsonl(args.raw)
    raw_by_request = {str(row["request_id"]): row for row in raw_rows}
    if len(raw_by_request) != len(raw_rows):
        raise SystemExit("Duplicate raw response request_id")

    item_rows = build_item_rows(imported_rows, raw_by_request)
    summary_rows = summarize(item_rows)
    paired_gap_rows = paired_rows(item_rows)
    recovery_rows = recoverability_rows(item_rows)
    reference_rows = reference_rows_for_requests(
        args.reference_items,
        {str(row["request_id"]) for row in item_rows},
    )
    comparison_rows = build_comparison_rows(args.model_label, summary_rows, reference_rows)
    matched_delta_rows = matched_model_delta_rows(item_rows, reference_rows, args.model_label)

    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_csv(args.paired_output, paired_gap_rows)
    write_csv(args.recovery_output, recovery_rows)
    write_comparison_csv(args.comparison_output, comparison_rows + matched_delta_rows)
    write_report(
        args.report,
        args.model_label,
        args.report_title or f"{args.model_label} Diagnostic Results",
        args.scope_description,
        args.cost_label,
        args.input_cost_per_mtok,
        args.output_cost_per_mtok,
        item_rows,
        summary_rows,
        paired_gap_rows,
        recovery_rows,
        comparison_rows,
        matched_delta_rows,
        args.items_output,
        args.summary_output,
        args.paired_output,
        args.recovery_output,
        args.comparison_output,
        args.raw,
        args.imported,
    )
    print(f"items={len(item_rows)}")
    print(f"recoverable_non_strict={len(recovery_rows)}")
    print(f"summary={args.summary_output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
