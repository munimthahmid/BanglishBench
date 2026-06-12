#!/usr/bin/env python3
"""Audit answer parsing and formatting for thesis-facing frozen-v5 rows."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "results/analysis/v5_answer_format_audit_items.csv"
DEFAULT_SUMMARY = ROOT / "results/analysis/v5_answer_format_audit_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_answer_format_audit.md"
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


def clip(text: Any, limit: int = 160) -> str:
    value = " ".join(str(text).split())
    return value if len(value) <= limit else value[: limit - 3] + "..."


def is_choice_format_failure(row: dict[str, Any], parsed: str) -> bool:
    return str(row.get("answer_type", "")) == "choice" and parsed.strip().upper() not in {
        "A",
        "B",
        "C",
        "D",
    }


def format_row(row: dict[str, Any]) -> dict[str, Any]:
    raw = str(row.get("raw_output", ""))
    parsed = parse_answer(raw, str(row.get("answer_type", ""))) if raw else str(row.get("parsed", ""))
    parsed_empty = not parsed.strip()
    choice_invalid = is_choice_format_failure(row, parsed)
    correct = is_correct(parsed, str(row.get("gold", "")), str(row.get("answer_type", "")))
    raw_lines = [line for line in raw.splitlines() if line.strip()]
    return {
        "model": MODEL_LABELS[str(row["model"])],
        "model_id": row["model"],
        "variant": row["variant"],
        "variant_label": VARIANT_LABELS.get(str(row["variant"]), row["variant"]),
        "dataset": row.get("dataset", ""),
        "task_type": row.get("task_type", ""),
        "answer_type": row.get("answer_type", ""),
        "id": row.get("id", ""),
        "gold": row.get("gold", ""),
        "correct": correct,
        "parsed": parsed,
        "parsed_empty": parsed_empty,
        "choice_invalid": choice_invalid,
        "format_failure": parsed_empty or choice_invalid,
        "raw_chars": len(raw),
        "parsed_chars": len(parsed),
        "raw_line_count": len(raw_lines),
        "raw_multiline": len(raw_lines) > 1,
        "raw_long_gt120": len(raw) > 120,
        "source": row.get("_source", ""),
        "line": row.get("_line", ""),
        "raw_excerpt": clip(raw),
    }


def load_main_rows(inputs: list[Path]) -> list[dict[str, Any]]:
    indexed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for path in inputs:
        for row in read_jsonl(path):
            if row.get("model") not in MODELS or row.get("variant") not in VARIANTS:
                continue
            key = (str(row["model"]), str(row["id"]), str(row["variant"]))
            indexed[key] = format_row(row)
    rows = list(indexed.values())
    expected = len(MODELS) * 200 * len(VARIANTS)
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} model-item-variant rows, got {len(rows)}")
    return sorted(rows, key=lambda row: (row["model"], row["dataset"], row["id"], row["variant"]))


def summarize_group(rows: list[dict[str, Any]], model: str, dataset: str, variant: str) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["model"] == model
        and row["variant"] == variant
        and (dataset == "all" or row["dataset"] == dataset)
    ]
    if not selected:
        raise SystemExit(f"No rows for {model} {dataset} {variant}")
    n = len(selected)
    return {
        "model": model,
        "dataset": dataset,
        "variant": variant,
        "variant_label": VARIANT_LABELS.get(variant, variant),
        "n": n,
        "correct": sum(bool(row["correct"]) for row in selected),
        "format_failures": sum(bool(row["format_failure"]) for row in selected),
        "parsed_empty": sum(bool(row["parsed_empty"]) for row in selected),
        "choice_invalid": sum(bool(row["choice_invalid"]) for row in selected),
        "raw_long_gt120": sum(bool(row["raw_long_gt120"]) for row in selected),
        "raw_multiline": sum(bool(row["raw_multiline"]) for row in selected),
        "mean_raw_chars": round(mean(int(row["raw_chars"]) for row in selected), 1),
        "mean_parsed_chars": round(mean(int(row["parsed_chars"]) for row in selected), 1),
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODEL_LABELS.values():
        for dataset in ("all", "benqa", "banglamath"):
            for variant in VARIANTS:
                out.append(summarize_group(rows, model, dataset, variant))
    return out


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


def row_for(summary: list[dict[str, Any]], model: str, dataset: str, variant: str) -> dict[str, Any]:
    return next(
        row
        for row in summary
        if row["model"] == model and row["dataset"] == dataset and row["variant"] == variant
    )


def points(items: int, n: int = 200) -> str:
    value = items / n * 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    output_items: Path,
    output_summary: Path,
) -> None:
    lines = [
        "# Frozen-V5 Answer Format Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the release-facing script gap could be",
        "explained by answer parsing or malformed answer formatting. It reuses the",
        "same thesis-facing Qwen rows as the frozen-v5 main table: unchanged Bangla",
        "and English outputs plus reviewed-v5 Banglish reruns.",
        "",
        f"- Item-level audit: `{repo_path(output_items)}`",
        f"- Summary table: `{repo_path(output_summary)}`",
        "",
        "Format failure is defined as an empty parsed answer, or a BEnQA MCQ parsed",
        "answer outside `A`/`B`/`C`/`D`. Long free-form BanglaMATH answers are",
        "reported separately because they are parseable but indicate answer-format",
        "drift.",
        "",
        "## Main Gap Stress Test",
        "",
        "| Model | Bangla correct | Reviewed Banglish correct | Banglish-Bangla gap | Bangla format failures | Banglish format failures | Gap if all Banglish format failures were correct |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODEL_LABELS.values():
        bangla = row_for(summary, model, "all", "bangla")
        banglish = row_for(summary, model, "all", "banglish_clean")
        raw_gap = int(banglish["correct"]) - int(bangla["correct"])
        optimistic_gap = int(banglish["correct"]) + int(banglish["format_failures"]) - int(
            bangla["correct"]
        )
        lines.append(
            f"| {model} | {bangla['correct']}/200 | {banglish['correct']}/200 | "
            f"{points(raw_gap)} pts | {bangla['format_failures']} | "
            f"{banglish['format_failures']} | {points(optimistic_gap)} pts |"
        )

    lines.extend(
        [
            "",
            "## Format Failures By Dataset",
            "",
            "| Model | Dataset | Bangla | Reviewed Banglish | English |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for model in MODEL_LABELS.values():
        for dataset in ("benqa", "banglamath"):
            values = [
                row_for(summary, model, dataset, variant)["format_failures"] for variant in VARIANTS
            ]
            lines.append(
                f"| {model} | `{dataset}` | {values[0]} | {values[1]} | {values[2]} |"
            )

    lines.extend(
        [
            "",
            "## Long Raw Outputs",
            "",
            "| Model | Dataset | Bangla | Reviewed Banglish | English |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for model in MODEL_LABELS.values():
        for dataset in ("benqa", "banglamath"):
            values = [row_for(summary, model, dataset, variant)["raw_long_gt120"] for variant in VARIANTS]
            lines.append(
                f"| {model} | `{dataset}` | {values[0]} | {values[1]} | {values[2]} |"
            )

    failure_rows = [row for row in rows if row["format_failure"]]
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Qwen2.5-3B has zero format failures across all 600 thesis-facing outputs.",
            "- Qwen2.5-7B 8-bit has two format failures, both reviewed-Banglish BEnQA",
            "  MCQ rows. Even if both were credited as correct, its all-200",
            "  Banglish-Bangla deficit remains -8.0 points.",
            "- Qwen3-4B format failures are not Banglish-specific: BEnQA has 4 Bangla,",
            "  3 reviewed-Banglish, and 8 English format failures.",
            "- Long raw answers are concentrated in Qwen3 BanglaMATH across every",
            "  script, supporting the existing claim that BanglaMATH is a low-accuracy",
            "  stress test rather than a clean fine-grained script-gap source.",
            "",
            "Thesis-safe phrasing:",
            "",
            "> The frozen-v5 script gap is not an artifact of empty parsing or MCQ",
            "> answer-format failures. Parse/format failures are rare for Qwen2.5,",
            "> and for Qwen3 they are at least as common in English and Bangla as in",
            "> reviewed Banglish.",
            "",
            f"Total format-failure rows: {len(failure_rows)}.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--inputs", type=Path, nargs="*", default=INPUTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_main_rows(args.inputs)
    summary = build_summary(rows)
    if len(summary) != 27:
        raise SystemExit(f"Expected 27 summary rows, got {len(summary)}")
    write_csv(args.output, rows)
    write_csv(args.summary_output, summary)
    write_report(args.report_output, rows, summary, args.output, args.summary_output)
    print(
        f"items={len(rows)} summary_rows={len(summary)} "
        f"report={args.report_output} csv={args.summary_output}"
    )


if __name__ == "__main__":
    main()
