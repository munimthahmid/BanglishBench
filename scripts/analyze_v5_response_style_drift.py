#!/usr/bin/env python3
"""Audit raw response style drift for thesis-facing frozen-v5 outputs."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_response_style_drift_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_response_style_drift_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_response_style_drift.md"

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
DATASETS = ("all", "benqa", "banglamath")
META_PATTERN = re.compile(
    r"\b(?:"
    r"cannot|can't|unable|insufficient|unclear|invalid|"
    r"not enough|not clear|not provided|not possible|not specified|"
    r"cannot be determined|cannot determine|cannot be derived|"
    r"no valid|does not contain|not meaningful|lack of clarity|appears"
    r")\b",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"\S+")
LATIN_RE = re.compile(r"[A-Za-z]")
BENGALI_RE = re.compile(r"[\u0980-\u09ff]")
DIGIT_RE = re.compile(r"[0-9\u09e6-\u09ef]")


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


def style_class(raw: str) -> str:
    has_latin = bool(LATIN_RE.search(raw))
    has_bengali = bool(BENGALI_RE.search(raw))
    if has_latin and has_bengali:
        return "mixed_bengali_latin"
    if has_latin:
        return "latin_only"
    if has_bengali:
        return "bengali_only"
    return "no_letters"


def format_item_row(row: dict[str, Any]) -> dict[str, Any]:
    raw = str(row.get("raw_output", ""))
    answer_type = str(row.get("answer_type", ""))
    parsed = parse_answer(raw, answer_type) if raw else str(row.get("parsed", ""))
    correct = is_correct(parsed, str(row.get("gold", "")), answer_type)
    raw_lines = [line for line in raw.splitlines() if line.strip()]
    raw_words = WORD_RE.findall(raw)
    meta = bool(META_PATTERN.search(raw))
    parsed_empty = not parsed.strip()
    choice_invalid = answer_type == "choice" and parsed.strip().upper() not in {"A", "B", "C", "D"}
    return {
        "model": MODEL_LABELS[str(row["model"])],
        "model_id": row["model"],
        "variant": row["variant"],
        "variant_label": VARIANT_LABELS.get(str(row["variant"]), row["variant"]),
        "dataset": row.get("dataset", ""),
        "task_type": row.get("task_type", ""),
        "answer_type": answer_type,
        "id": row.get("id", ""),
        "gold": row.get("gold", ""),
        "correct": correct,
        "parsed": parsed,
        "parsed_empty": parsed_empty,
        "choice_invalid": choice_invalid,
        "format_failure": parsed_empty or choice_invalid,
        "meta_uncertainty": meta,
        "long_response_gt120": len(raw) > 120,
        "raw_multiline": len(raw_lines) > 1,
        "raw_chars": len(raw),
        "raw_words": len(raw_words),
        "raw_line_count": len(raw_lines),
        "contains_bengali": bool(BENGALI_RE.search(raw)),
        "contains_latin": bool(LATIN_RE.search(raw)),
        "contains_digit": bool(DIGIT_RE.search(raw)),
        "script_class": style_class(raw),
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
            indexed[key] = format_item_row(row)
    expected = len(MODELS) * 200 * len(VARIANTS)
    if len(indexed) != expected:
        raise SystemExit(f"Expected {expected} model-item-variant rows, got {len(indexed)}")
    return sorted(indexed.values(), key=lambda row: (row["model"], row["dataset"], row["id"], row["variant"]))


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
    wrong = [row for row in selected if not row["correct"]]
    n = len(selected)
    return {
        "model": model,
        "dataset": dataset,
        "variant": variant,
        "variant_label": VARIANT_LABELS.get(variant, variant),
        "n": n,
        "correct": sum(bool(row["correct"]) for row in selected),
        "wrong": len(wrong),
        "format_failures": sum(bool(row["format_failure"]) for row in selected),
        "meta_uncertainty": sum(bool(row["meta_uncertainty"]) for row in selected),
        "wrong_meta_uncertainty": sum(bool(row["meta_uncertainty"]) for row in wrong),
        "long_response_gt120": sum(bool(row["long_response_gt120"]) for row in selected),
        "raw_multiline": sum(bool(row["raw_multiline"]) for row in selected),
        "contains_bengali": sum(bool(row["contains_bengali"]) for row in selected),
        "contains_latin": sum(bool(row["contains_latin"]) for row in selected),
        "mixed_bengali_latin": sum(row["script_class"] == "mixed_bengali_latin" for row in selected),
        "latin_only": sum(row["script_class"] == "latin_only" for row in selected),
        "bengali_only": sum(row["script_class"] == "bengali_only" for row in selected),
        "no_letters": sum(row["script_class"] == "no_letters" for row in selected),
        "mean_raw_chars": round(mean(int(row["raw_chars"]) for row in selected), 1),
        "mean_raw_words": round(mean(int(row["raw_words"]) for row in selected), 1),
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for model in MODEL_LABELS.values():
        for dataset in DATASETS:
            for variant in VARIANTS:
                summary.append(summarize_group(rows, model, dataset, variant))
    return summary


def row_for(summary: list[dict[str, Any]], model: str, dataset: str, variant: str) -> dict[str, Any]:
    return next(
        row
        for row in summary
        if row["model"] == model and row["dataset"] == dataset and row["variant"] == variant
    )


def example_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [
        row
        for row in rows
        if row["model"] == "Qwen3-4B"
        and row["dataset"] == "banglamath"
        and row["variant"] == "banglish_clean"
        and row["meta_uncertainty"]
    ]
    return sorted(selected, key=lambda row: (-int(row["raw_chars"]), str(row["id"])))[:5]


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    qwen3_bangla_math = row_for(summary, "Qwen3-4B", "banglamath", "bangla")
    qwen3_banglish_math = row_for(summary, "Qwen3-4B", "banglamath", "banglish_clean")
    qwen3_english_math = row_for(summary, "Qwen3-4B", "banglamath", "english")
    qwen25_3b_banglish_math = row_for(summary, "Qwen2.5-3B", "banglamath", "banglish_clean")
    qwen25_7b_banglish_math = row_for(summary, "Qwen2.5-7B 8-bit", "banglamath", "banglish_clean")
    lines = [
        "# Frozen-V5 Response-Style Drift Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks raw model responses, not just parsed correctness.",
        "It asks whether reviewed Banglish changes response style: verbosity,",
        "script of the output, and meta/uncertainty language such as `cannot`,",
        "`unclear`, or `appears`. It uses the same thesis-facing frozen-v5 Qwen",
        "rows as the main table.",
        "",
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "This is behavioral failure analysis. It is not a causal mechanism, and it",
        "does not replace correctness, parser, or answer-format audits.",
        "",
        "## Headline",
        "",
        f"- Qwen3-4B BanglaMATH reviewed Banglish has {qwen3_banglish_math['meta_uncertainty']}/56",
        f"  meta/uncertainty outputs, versus {qwen3_bangla_math['meta_uncertainty']}/56",
        f"  for Bangla and {qwen3_english_math['meta_uncertainty']}/56 for English.",
        f"- Qwen3-4B is verbose on BanglaMATH across scripts, but reviewed Banglish",
        f"  is the clearest meta-confusion case: mean raw length {qwen3_banglish_math['mean_raw_chars']}",
        f"  chars and {qwen3_banglish_math['long_response_gt120']}/56 outputs over 120 chars.",
        f"- Qwen2.5 rows do not show the same BanglaMATH meta pattern:",
        f"  Qwen2.5-3B reviewed Banglish has {qwen25_3b_banglish_math['meta_uncertainty']}/56",
        f"  meta outputs and Qwen2.5-7B has {qwen25_7b_banglish_math['meta_uncertainty']}/56.",
        "- Therefore response-style drift is a model-specific failure mode, not a",
        "  complete explanation of the Banglish gap.",
        "",
        "## BanglaMATH Response Style",
        "",
        "| Model | Variant | Correct | Meta/uncertainty | Wrong meta | Long >120 chars | Mean raw chars | Bengali output | Latin output | Mixed output |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODEL_LABELS.values():
        for variant in VARIANTS:
            row = row_for(summary, model, "banglamath", variant)
            lines.append(
                f"| {model} | {row['variant_label']} | {row['correct']}/{row['n']} | "
                f"{row['meta_uncertainty']}/{row['n']} | "
                f"{row['wrong_meta_uncertainty']}/{row['wrong']} | "
                f"{row['long_response_gt120']}/{row['n']} | "
                f"{row['mean_raw_chars']} | {row['contains_bengali']} | "
                f"{row['contains_latin']} | {row['mixed_bengali_latin']} |"
            )

    lines.extend(
        [
            "",
            "## All-200 Summary",
            "",
            "| Model | Variant | Correct | Meta/uncertainty | Long >120 chars | Mean raw chars |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODEL_LABELS.values():
        for variant in VARIANTS:
            row = row_for(summary, model, "all", variant)
            lines.append(
                f"| {model} | {row['variant_label']} | {row['correct']}/{row['n']} | "
                f"{row['meta_uncertainty']}/{row['n']} | "
                f"{row['long_response_gt120']}/{row['n']} | {row['mean_raw_chars']} |"
            )

    examples = example_rows(rows)
    lines.extend(
        [
            "",
            "## Qwen3 BanglaMATH Banglish Meta Examples",
            "",
            "| Item | Gold | Parsed | Raw excerpt |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in examples:
        lines.append(
            f"| `{row['id']}` | `{row['gold']}` | `{clip(row['parsed'], 40)}` | "
            f"{row['raw_excerpt']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- BEnQA MCQ outputs are mostly one-letter answers, so response-style drift is",
            "  not the main BEnQA parser explanation; choice-bias and distractor audits",
            "  are the better BEnQA failure-analysis sources.",
            "- BanglaMATH has low accuracy across scripts, but Qwen3 reviewed Banglish",
            "  often elicits meta/uncertainty prose instead of a direct short answer.",
            "- This supports the broader robustness framing: script choice can alter not",
            "  only correctness but also answer behavior. Because Qwen2.5 does not show",
            "  the same meta pattern, keep the claim model-specific.",
            "",
            "## Reproducibility",
            "",
            f"- Builder: `{repo_path(Path(__file__))}`",
            f"- Item rows: {len(rows)}",
            f"- Summary rows: {len(summary)}",
            "- Meta/uncertainty detection is regex-based and intentionally conservative.",
        ]
    )
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
    rows = load_main_rows(args.inputs)
    summary = build_summary(rows)
    write_csv(args.items_output, rows)
    write_csv(args.summary_output, summary)
    write_report(args.report_output, rows, summary, args.items_output, args.summary_output)
    qwen3_banglish_math = row_for(summary, "Qwen3-4B", "banglamath", "banglish_clean")
    print(
        f"items={len(rows)} | summary_rows={len(summary)} | "
        f"qwen3_math_banglish_meta={qwen3_banglish_math['meta_uncertainty']}/56 | "
        f"report={repo_path(args.report_output)}"
    )


if __name__ == "__main__":
    main()
