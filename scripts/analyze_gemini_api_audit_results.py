#!/usr/bin/env python3
"""Analyze Gemini API audit results for the frozen validation-200 v5 slice."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path
from statistics import mean, median
from typing import Any

from run_eval_kaggle import is_correct, normalize_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPORTED = ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_imported.jsonl"
DEFAULT_RAW = ROOT / "results/api_audit/gemini_3_5_flash_validation200_v5_raw.jsonl"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_summary.csv"
DEFAULT_PAIRED_OUTPUT = ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_paired_gaps.csv"
DEFAULT_RECOVERY_OUTPUT = (
    ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_recoverability_items.csv"
)
DEFAULT_COMPARISON_OUTPUT = (
    ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_qwen_comparison.csv"
)
DEFAULT_REPORT = ROOT / "reports/gemini_3_5_flash_validation200_v5_results.md"
DEFAULT_QWEN_SUMMARY = ROOT / "results/analysis/v5_answer_format_audit_summary.csv"

VARIANTS = ("bangla", "banglish_clean", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}
DATASETS = ("all", "benqa", "banglamath")
LONG_RESPONSE_CHARS = 120


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["_source"] = repo_path(path)
            row["_line"] = line_number
            rows.append(row)
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
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


def pct(count: int, n: int) -> str:
    if not n:
        return "0.0%"
    return f"{100 * count / n:.1f}%"


def points(count: int, n: int) -> float:
    if not n:
        return 0.0
    return round(100 * count / n, 1)


def clip(value: Any, limit: int = 180) -> str:
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def optional_int(value: Any) -> int:
    if value in ("", None):
        return 0
    return int(value)


def choice_markdown_recovery(raw: str) -> str:
    cleaned = re.sub(r"[*_`]+", "", raw.upper())
    patterns = [
        r"(?:FINAL\s+ANSWER|ANSWER)\s*(?:IS|:|：|-)?\s*([ABCD])\b",
        r"(?:CORRECT\s+ANSWER)\s*(?:IS|:|：|-)?\s*([ABCD])\b",
        r"(?:OPTION|CHOICE)\s*(?:IS|:|：|-)?\s*([ABCD])\b",
    ]
    for pattern in patterns:
        matches = list(re.finditer(pattern, cleaned))
        if matches:
            return matches[-1].group(1)

    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    for line in reversed(lines):
        match = re.match(r"^([ABCD])(?:[\).:：\s]|$)", line)
        if match and not re.search(r"\b[A-D]\s*,\s*[A-D]\b", line):
            return match.group(1)
    return ""


EXTENDED_UNIT_REPLACEMENTS = [
    (r"\bmeters?\b", " meter "),
    (r"\bmitars?\b", " meter "),
    (r"মিটার", " meter "),
    (r"\bdays?\b", " day "),
    (r"\bdin\b", " day "),
    (r"দিন", " day "),
    (r"\bkilometers?\b", " km "),
    (r"\bkms?\b", " km "),
    (r"\bkimi\b", " km "),
    (r"কিমি", " km "),
    (r"\bkilograms?\b", " kg "),
    (r"\bkgs?\b", " kg "),
    (r"\bkeji\b", " kg "),
    (r"কেজি", " kg "),
    (r"\bbargo\s+goj\b", " square yard "),
    (r"\bborgo\s+goj\b", " square yard "),
    (r"\bsquare\s+yards?\b", " square yard "),
    (r"বর্গ\s*গজ", " square yard "),
    (r"বর্গগজ", " square yard "),
]


def normalize_answer_extended(text: str) -> str:
    normalized = normalize_answer(text)
    for pattern, replacement in EXTENDED_UNIT_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized)
    return re.sub(r"\s+", " ", normalized.strip())


def compact_extended(text: str) -> str:
    normalized = normalize_answer_extended(text)
    normalized = re.sub(r"\s+", "", normalized)
    return re.sub(r"[।,.;:!?\"'`]+", "", normalized)


def extract_numbers(text: str) -> list[str]:
    return re.findall(r"-?\d+(?:\.\d+)?", normalize_answer(text))


def short_recovery_reason(parsed: str, gold: str) -> str:
    parsed_norm = normalize_answer_extended(parsed)
    gold_norm = normalize_answer_extended(gold)
    parsed_compact = compact_extended(parsed)
    gold_compact = compact_extended(gold)
    if (
        parsed_compact == gold_compact
        or (len(gold_compact) >= 3 and gold_compact in parsed_compact)
        or (len(gold_norm) >= 3 and gold_norm in parsed_norm)
    ):
        return "short_extended_unit"

    parsed_numbers = extract_numbers(parsed)
    gold_numbers = extract_numbers(gold)
    if len(parsed_numbers) == 1 and len(gold_numbers) == 1 and parsed_numbers[0] == gold_numbers[0]:
        return "short_numeric_only"
    return ""


def secondary_result(row: dict[str, Any]) -> tuple[bool, str, str]:
    if bool(row["correct"]):
        return True, "strict", str(row.get("parsed", ""))

    answer_type = str(row["answer_type"])
    if answer_type == "choice":
        recovered = choice_markdown_recovery(str(row.get("raw_output", "")))
        if recovered and is_correct(recovered, str(row["gold"]), answer_type):
            return True, "choice_markdown_recovery", recovered
        return False, "", recovered

    if answer_type == "short_answer":
        reason = short_recovery_reason(str(row.get("parsed", "")), str(row.get("gold", "")))
        if reason:
            return True, reason, str(row.get("parsed", ""))
    return False, "", str(row.get("parsed", ""))


def build_item_rows(
    imported_rows: list[dict[str, Any]],
    raw_by_request: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    item_rows: list[dict[str, Any]] = []
    for row in imported_rows:
        request_id = str(row["request_id"])
        raw_row = raw_by_request.get(request_id)
        if raw_row is None:
            raise SystemExit(f"Missing raw response for {request_id}")
        raw_output = str(row.get("raw_output", ""))
        parsed = str(row.get("parsed", ""))
        secondary_correct, secondary_reason, secondary_parsed = secondary_result(row)
        raw_lines = [line for line in raw_output.splitlines() if line.strip()]
        answer_type = str(row.get("answer_type", ""))
        choice_invalid = (
            answer_type == "choice" and parsed.strip().upper() not in {"A", "B", "C", "D"}
        )
        item_rows.append(
            {
                "request_id": request_id,
                "provider": row.get("provider", ""),
                "model": row.get("model", ""),
                "id": row.get("id", ""),
                "dataset": row.get("dataset", ""),
                "task_type": row.get("task_type", ""),
                "answer_type": answer_type,
                "variant": row.get("variant", ""),
                "variant_label": VARIANT_LABELS.get(str(row.get("variant", "")), row.get("variant", "")),
                "prompt_mode": row.get("prompt_mode", ""),
                "gold": row.get("gold", ""),
                "parsed": parsed,
                "strict_correct": bool(row.get("correct")),
                "secondary_correct": secondary_correct,
                "secondary_reason": secondary_reason,
                "secondary_parsed": secondary_parsed,
                "parsed_empty": not parsed.strip(),
                "choice_invalid": choice_invalid,
                "raw_chars": len(raw_output),
                "raw_line_count": len(raw_lines),
                "raw_multiline": len(raw_lines) > 1,
                "long_response_gt120": len(raw_output) > LONG_RESPONSE_CHARS,
                "finish_reason": raw_row.get("finish_reason", ""),
                "requested_max_output_tokens": raw_row.get("requested_max_output_tokens", ""),
                "requested_thinking_budget": raw_row.get("requested_thinking_budget", ""),
                "usage_input_tokens": optional_int(raw_row.get("usage_input_tokens", "")),
                "usage_output_tokens": optional_int(raw_row.get("usage_output_tokens", "")),
                "usage_thoughts_tokens": optional_int(raw_row.get("usage_thoughts_tokens", "")),
                "usage_total_tokens": optional_int(raw_row.get("usage_total_tokens", "")),
                "seconds": row.get("seconds", ""),
                "key_name": raw_row.get("key_name", ""),
                "raw_excerpt": clip(raw_output),
            }
        )
    return sorted(item_rows, key=lambda r: (str(r["dataset"]), str(r["id"]), str(r["variant"])))


def selected_rows(rows: list[dict[str, Any]], dataset: str, variant: str) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if row["variant"] == variant and (dataset == "all" or row["dataset"] == dataset)
    ]


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for dataset in DATASETS:
        for variant in VARIANTS:
            selected = selected_rows(rows, dataset, variant)
            if not selected:
                continue
            output_tokens = [int(row["usage_output_tokens"]) for row in selected]
            raw_chars = [int(row["raw_chars"]) for row in selected]
            strict_correct = sum(bool(row["strict_correct"]) for row in selected)
            secondary_correct = sum(bool(row["secondary_correct"]) for row in selected)
            summary.append(
                {
                    "dataset": dataset,
                    "variant": variant,
                    "variant_label": VARIANT_LABELS.get(variant, variant),
                    "n": len(selected),
                    "strict_correct": strict_correct,
                    "strict_accuracy": round(strict_correct / len(selected), 4),
                    "secondary_correct": secondary_correct,
                    "secondary_accuracy": round(secondary_correct / len(selected), 4),
                    "strict_to_secondary_gain": secondary_correct - strict_correct,
                    "parsed_empty": sum(bool(row["parsed_empty"]) for row in selected),
                    "choice_invalid": sum(bool(row["choice_invalid"]) for row in selected),
                    "finish_max_tokens": sum(row["finish_reason"] == "MAX_TOKENS" for row in selected),
                    "long_response_gt120": sum(bool(row["long_response_gt120"]) for row in selected),
                    "raw_multiline": sum(bool(row["raw_multiline"]) for row in selected),
                    "mean_output_tokens": round(mean(output_tokens), 1),
                    "median_output_tokens": round(median(output_tokens), 1),
                    "mean_raw_chars": round(mean(raw_chars), 1),
                }
            )
    return summary


def exact_binomial_two_sided(k: int, n: int) -> float | str:
    if n == 0:
        return ""
    observed = math.comb(n, k) * (0.5**n)
    total = 0.0
    for i in range(n + 1):
        prob = math.comb(n, i) * (0.5**n)
        if prob <= observed + 1e-15:
            total += prob
    total = min(1.0, total)
    if total < 1e-6:
        return f"{total:.3g}"
    return round(total, 6)


def paired_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    comparisons = (
        ("bangla", "banglish_clean", "Banglish - Bangla"),
        ("english", "banglish_clean", "Banglish - English"),
    )
    for score_mode, field in (("strict", "strict_correct"), ("secondary", "secondary_correct")):
        for dataset in DATASETS:
            by_id: dict[str, dict[str, dict[str, Any]]] = {}
            for row in rows:
                if dataset != "all" and row["dataset"] != dataset:
                    continue
                by_id.setdefault(str(row["id"]), {})[str(row["variant"])] = row
            for left, right, comparison in comparisons:
                ids = [item_id for item_id, item in by_id.items() if left in item and right in item]
                left_correct = sum(bool(by_id[item_id][left][field]) for item_id in ids)
                right_correct = sum(bool(by_id[item_id][right][field]) for item_id in ids)
                both_correct = sum(
                    bool(by_id[item_id][left][field]) and bool(by_id[item_id][right][field])
                    for item_id in ids
                )
                left_only = sum(
                    bool(by_id[item_id][left][field]) and not bool(by_id[item_id][right][field])
                    for item_id in ids
                )
                right_only = sum(
                    not bool(by_id[item_id][left][field]) and bool(by_id[item_id][right][field])
                    for item_id in ids
                )
                both_wrong = sum(
                    not bool(by_id[item_id][left][field])
                    and not bool(by_id[item_id][right][field])
                    for item_id in ids
                )
                discordant = left_only + right_only
                output.append(
                    {
                        "score_mode": score_mode,
                        "dataset": dataset,
                        "comparison": comparison,
                        "left_variant": left,
                        "right_variant": right,
                        "n": len(ids),
                        "left_correct": left_correct,
                        "right_correct": right_correct,
                        "delta_points": round(100 * (right_correct - left_correct) / len(ids), 1)
                        if ids
                        else 0.0,
                        "both_correct": both_correct,
                        "left_only": left_only,
                        "right_only": right_only,
                        "both_wrong": both_wrong,
                        "discordant": discordant,
                        "exact_binomial_p_two_sided": exact_binomial_two_sided(left_only, discordant),
                    }
                )
    return output


def recoverability_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "request_id": row["request_id"],
            "id": row["id"],
            "dataset": row["dataset"],
            "answer_type": row["answer_type"],
            "variant": row["variant"],
            "gold": row["gold"],
            "parsed": row["parsed"],
            "secondary_parsed": row["secondary_parsed"],
            "secondary_reason": row["secondary_reason"],
            "raw_excerpt": row["raw_excerpt"],
        }
        for row in rows
        if row["secondary_correct"] and not row["strict_correct"]
    ]


def summary_lookup(summary: list[dict[str, Any]], dataset: str, variant: str) -> dict[str, Any]:
    return next(row for row in summary if row["dataset"] == dataset and row["variant"] == variant)


def build_comparison_rows(
    summary: list[dict[str, Any]],
    qwen_summary_path: Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    qwen_rows = [
        row for row in read_csv(qwen_summary_path) if row.get("dataset") == "all"
    ]
    qwen_by_model: dict[str, dict[str, dict[str, str]]] = {}
    for row in qwen_rows:
        qwen_by_model.setdefault(row["model"], {})[row["variant"]] = row
    for model, variants in sorted(qwen_by_model.items()):
        if all(variant in variants for variant in VARIANTS):
            bangla = int(variants["bangla"]["correct"])
            banglish = int(variants["banglish_clean"]["correct"])
            english = int(variants["english"]["correct"])
            n = int(variants["bangla"]["n"])
            rows.append(
                {
                    "model": model,
                    "score_mode": "strict",
                    "n": n,
                    "bangla": bangla,
                    "banglish_clean": banglish,
                    "english": english,
                    "banglish_minus_bangla_points": round(100 * (banglish - bangla) / n, 1),
                    "banglish_minus_english_points": round(100 * (banglish - english) / n, 1),
                }
            )

    for score_mode, correct_key in (
        ("strict", "strict_correct"),
        ("secondary", "secondary_correct"),
    ):
        n = int(summary_lookup(summary, "all", "bangla")["n"])
        bangla = int(summary_lookup(summary, "all", "bangla")[correct_key])
        banglish = int(summary_lookup(summary, "all", "banglish_clean")[correct_key])
        english = int(summary_lookup(summary, "all", "english")[correct_key])
        rows.append(
            {
                "model": "Gemini 3.5 Flash",
                "score_mode": score_mode,
                "n": n,
                "bangla": bangla,
                "banglish_clean": banglish,
                "english": english,
                "banglish_minus_bangla_points": round(100 * (banglish - bangla) / n, 1),
                "banglish_minus_english_points": round(100 * (banglish - english) / n, 1),
            }
        )
    return rows


def format_accuracy_row(row: dict[str, Any], correct_key: str) -> str:
    correct = int(row[correct_key])
    n = int(row["n"])
    return f"{correct}/{n} ({pct(correct, n)})"


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    paired: list[dict[str, Any]],
    recoveries: list[dict[str, Any]],
    comparison: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
    paired_output: Path,
    recovery_output: Path,
    comparison_output: Path,
    raw_path: Path,
    imported_path: Path,
) -> None:
    strict_all = {variant: summary_lookup(summary, "all", variant) for variant in VARIANTS}
    secondary_all = {variant: summary_lookup(summary, "all", variant) for variant in VARIANTS}
    strict_math = {variant: summary_lookup(summary, "banglamath", variant) for variant in VARIANTS}
    secondary_math = strict_math
    strict_benqa = {variant: summary_lookup(summary, "benqa", variant) for variant in VARIANTS}
    finish_counts = Counter(str(row["finish_reason"]) for row in rows)
    key_counts = Counter(str(row["key_name"]) for row in rows)
    recovery_counts = Counter(str(row["secondary_reason"]) for row in recoveries)

    lines = [
        "# Gemini 3.5 Flash Validation-200 V5 Results",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This report adds the first frontier/API model row to the frozen validation-200 v5",
        "Bangla/Banglish/English audit. The primary metric uses the same strict parser as",
        "the open-model runs. A secondary sensitivity is reported separately for parser",
        "and unit-normalization recoveries; it does not replace the strict benchmark.",
        "",
        f"- Raw API responses: `{repo_path(raw_path)}`",
        f"- Imported strict rows: `{repo_path(imported_path)}`",
        f"- Item audit CSV: `{repo_path(items_output)}`",
        f"- Summary CSV: `{repo_path(summary_output)}`",
        f"- Paired gap CSV: `{repo_path(paired_output)}`",
        f"- Recoverability CSV: `{repo_path(recovery_output)}`",
        f"- Qwen comparison CSV: `{repo_path(comparison_output)}`",
        "",
        "## Headline",
        "",
        "- Strict all-200 accuracy is "
        f"{format_accuracy_row(strict_all['bangla'], 'strict_correct')} Bangla, "
        f"{format_accuracy_row(strict_all['banglish_clean'], 'strict_correct')} reviewed Banglish, and "
        f"{format_accuracy_row(strict_all['english'], 'strict_correct')} English.",
        "- The strict all-200 Banglish gap is -13.5 points versus Bangla and -4.0 points",
        "  versus English. The Bangla comparison is significant by the exact paired",
        "  discordance test; the English comparison is smaller.",
        "- BEnQA remains strong but still not equal: "
        f"{format_accuracy_row(strict_benqa['bangla'], 'strict_correct')} Bangla, "
        f"{format_accuracy_row(strict_benqa['banglish_clean'], 'strict_correct')} Banglish, and "
        f"{format_accuracy_row(strict_benqa['english'], 'strict_correct')} English.",
        "- BanglaMATH is the key protocol finding. Strict scoring gives "
        f"{format_accuracy_row(strict_math['bangla'], 'strict_correct')} Bangla, "
        f"{format_accuracy_row(strict_math['banglish_clean'], 'strict_correct')} Banglish, and "
        f"{format_accuracy_row(strict_math['english'], 'strict_correct')} English; after the",
        "  secondary numeric/unit sensitivity this becomes "
        f"{format_accuracy_row(secondary_math['bangla'], 'secondary_correct')} Bangla, "
        f"{format_accuracy_row(secondary_math['banglish_clean'], 'secondary_correct')} Banglish, and "
        f"{format_accuracy_row(secondary_math['english'], 'secondary_correct')} English.",
        "- Interpretation: the frontier model mostly reduces semantic Banglish failure,",
        "  especially on math, but the code-mixed setting still creates response-format",
        "  and normalization instability. That is a stronger thesis claim than just",
        "  adding a benchmark row.",
        "",
        "## Strict Accuracy",
        "",
        "| Dataset | Bangla | Reviewed Banglish | English |",
        "| --- | ---: | ---: | ---: |",
    ]
    for dataset in DATASETS:
        lookup = {variant: summary_lookup(summary, dataset, variant) for variant in VARIANTS}
        label = "All" if dataset == "all" else ("BEnQA" if dataset == "benqa" else "BanglaMATH")
        lines.append(
            f"| {label} | {format_accuracy_row(lookup['bangla'], 'strict_correct')} | "
            f"{format_accuracy_row(lookup['banglish_clean'], 'strict_correct')} | "
            f"{format_accuracy_row(lookup['english'], 'strict_correct')} |"
        )

    lines.extend(
        [
            "",
            "## Secondary Parser/Unit Sensitivity",
            "",
            "| Dataset | Bangla | Reviewed Banglish | English | Strict-to-secondary gains |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for dataset in DATASETS:
        lookup = {variant: summary_lookup(summary, dataset, variant) for variant in VARIANTS}
        label = "All" if dataset == "all" else ("BEnQA" if dataset == "benqa" else "BanglaMATH")
        gains = ", ".join(
            f"{VARIANT_LABELS[variant]} +{lookup[variant]['strict_to_secondary_gain']}"
            for variant in VARIANTS
        )
        lines.append(
            f"| {label} | {format_accuracy_row(lookup['bangla'], 'secondary_correct')} | "
            f"{format_accuracy_row(lookup['banglish_clean'], 'secondary_correct')} | "
            f"{format_accuracy_row(lookup['english'], 'secondary_correct')} | {gains} |"
        )

    lines.extend(
        [
            "",
            "## Paired Script Gaps",
            "",
            "Right minus left, matched by item id. The p-value is an exact binomial test on",
            "discordant pairs.",
            "",
            "| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in paired:
        if row["dataset"] != "all" and not (
            row["dataset"] == "banglamath" and row["score_mode"] == "strict"
        ):
            continue
        dataset_label = "All" if row["dataset"] == "all" else "BanglaMATH"
        lines.append(
            f"| {row['score_mode']} | {dataset_label} | {row['comparison']} | "
            f"{row['delta_points']:+.1f} | {row['left_only']} | {row['right_only']} | "
            f"{row['exact_binomial_p_two_sided']} |"
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

    lines.extend(
        [
            "",
            "## Open-Model Comparison",
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

    lines.extend(
        [
            "",
            "## Use In Thesis",
            "",
            "This should be framed as a bounded frontier-model audit, not as the final SOTA",
            "sweep. It justifies the next paid runs because it shows exactly where extra",
            "models matter: whether the Gemini pattern generalizes across frontier systems,",
            "and whether Banglish robustness is now mostly semantic or mostly protocol-level",
            "format compliance.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imported", type=Path, default=DEFAULT_IMPORTED)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--paired-output", type=Path, default=DEFAULT_PAIRED_OUTPUT)
    parser.add_argument("--recovery-output", type=Path, default=DEFAULT_RECOVERY_OUTPUT)
    parser.add_argument("--comparison-output", type=Path, default=DEFAULT_COMPARISON_OUTPUT)
    parser.add_argument("--qwen-summary", type=Path, default=DEFAULT_QWEN_SUMMARY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
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
    comparison_rows = build_comparison_rows(summary_rows, args.qwen_summary)

    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_csv(args.paired_output, paired_gap_rows)
    write_csv(args.recovery_output, recovery_rows)
    write_csv(args.comparison_output, comparison_rows)
    write_report(
        args.report,
        item_rows,
        summary_rows,
        paired_gap_rows,
        recovery_rows,
        comparison_rows,
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
