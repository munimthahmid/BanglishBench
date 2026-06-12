#!/usr/bin/env python3
"""Audit whether BEnQA reviewed-Banglish D-collapse is length/token driven."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_TOKEN_AUDIT = ROOT / "results/tokenization/validation200_v5/audit.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_length_token_confound_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_length_token_confound_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_length_token_confound.md"

TOKENIZER = "Qwen/Qwen3-4B-Instruct-2507"
MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
METRICS = (
    ("banglish_hf_tokens", "Reviewed-Banglish HF tokens"),
    ("banglish_chars", "Reviewed-Banglish characters"),
    ("banglish_words", "Reviewed-Banglish words"),
    ("banglish_hf_tokens_per_word", "Reviewed-Banglish HF tokens per word"),
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


def fnum(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def token_index(token_audit: Path) -> dict[str, dict[str, float]]:
    index: dict[str, dict[str, float]] = {}
    for row in read_csv(token_audit):
        if (
            row.get("dataset") == "benqa"
            and row.get("variant") == "banglish_clean"
            and row.get("tokenizer") == TOKENIZER
        ):
            index[row["id"]] = {
                "banglish_hf_tokens": fnum(row["hf_tokens"]),
                "banglish_chars": fnum(row["chars"]),
                "banglish_words": fnum(row["words"]),
                "banglish_hf_tokens_per_word": fnum(row["hf_tokens_per_word"]),
                "banglish_chars_per_word": fnum(row["chars_per_word"]),
                "banglish_bytes_per_word": fnum(row["bytes_per_word"]),
            }
    if len(index) != 144:
        raise SystemExit(f"Expected 144 BEnQA token rows, got {len(index)}")
    return index


def build_item_rows(choice_items: Path, token_audit: Path) -> list[dict[str, Any]]:
    token_rows = token_index(token_audit)
    choice_rows = read_csv(choice_items)
    if len(choice_rows) != len(MODELS) * 144:
        raise SystemExit(f"Expected {len(MODELS) * 144} choice-bias rows, got {len(choice_rows)}")

    rows: list[dict[str, Any]] = []
    for row in choice_rows:
        item_id = row["id"]
        if item_id not in token_rows:
            raise SystemExit(f"Missing tokenization row for {item_id}")
        option = row["banglish_clean_parsed_option"]
        correct = truthy(row["banglish_clean_correct"])
        rows.append(
            {
                "model": row["model"],
                "id": item_id,
                "gold": row["gold"],
                "banglish_option": option,
                "banglish_correct": correct,
                "banglish_D": option == "D",
                "banglish_wrong_D": option == "D" and not correct,
                "banglish_invalid": option == "invalid",
                **token_rows[item_id],
            }
        )
    return rows


def quartile_rows(rows: list[dict[str, Any]], metric: str) -> list[tuple[str, list[dict[str, Any]]]]:
    ordered = sorted(rows, key=lambda row: (float(row[metric]), str(row["id"])))
    n = len(ordered)
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for index in range(4):
        start = index * n // 4
        end = (index + 1) * n // 4
        out.append((f"q{index + 1}", ordered[start:end]))
    return out


def summarize_quartile(
    model: str,
    metric: str,
    metric_label: str,
    quartile: str,
    selected: list[dict[str, Any]],
) -> dict[str, Any]:
    n = len(selected)
    return {
        "section": "metric_quartile",
        "model": model,
        "metric": metric,
        "metric_label": metric_label,
        "quartile": quartile,
        "n": n,
        "min_metric": round(min(float(row[metric]) for row in selected), 4),
        "max_metric": round(max(float(row[metric]) for row in selected), 4),
        "mean_metric": round(sum(float(row[metric]) for row in selected) / n, 4) if n else 0,
        "banglish_correct": sum(bool(row["banglish_correct"]) for row in selected),
        "banglish_D": sum(bool(row["banglish_D"]) for row in selected),
        "banglish_wrong_D": sum(bool(row["banglish_wrong_D"]) for row in selected),
        "banglish_invalid": sum(bool(row["banglish_invalid"]) for row in selected),
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [row for row in item_rows if row["model"] == model]
        for metric, metric_label in METRICS:
            for quartile, selected in quartile_rows(model_rows, metric):
                rows.append(summarize_quartile(model, metric, metric_label, quartile, selected))
    return rows


def row_for(rows: list[dict[str, Any]], model: str, metric: str, quartile: str) -> dict[str, Any]:
    matches = [
        row
        for row in rows
        if row["model"] == model and row["metric"] == metric and row["quartile"] == quartile
    ]
    if len(matches) != 1:
        raise SystemExit(f"Expected one row for {model} {metric} {quartile}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_token_quartiles = [
        row_for(summary_rows, "Qwen3-4B", "banglish_hf_tokens", f"q{index}")
        for index in range(1, 5)
    ]
    q3_char_q1 = row_for(summary_rows, "Qwen3-4B", "banglish_chars", "q1")
    q3_char_q4 = row_for(summary_rows, "Qwen3-4B", "banglish_chars", "q4")
    q3_density_q1 = row_for(summary_rows, "Qwen3-4B", "banglish_hf_tokens_per_word", "q1")
    q3_density_q4 = row_for(summary_rows, "Qwen3-4B", "banglish_hf_tokens_per_word", "q4")
    q25_3_token_q1 = row_for(summary_rows, "Qwen2.5-3B", "banglish_hf_tokens", "q1")
    q25_7_token_q1 = row_for(summary_rows, "Qwen2.5-7B 8-bit", "banglish_hf_tokens", "q1")
    q25_3_token_q4 = row_for(summary_rows, "Qwen2.5-3B", "banglish_hf_tokens", "q4")
    q25_7_token_q4 = row_for(summary_rows, "Qwen2.5-7B 8-bit", "banglish_hf_tokens", "q4")

    q3_token_d = ", ".join(f"{row['banglish_D']}/{row['n']}" for row in q3_token_quartiles)
    q3_token_wrong_d = ", ".join(
        f"{row['banglish_wrong_D']}/{row['n']}" for row in q3_token_quartiles
    )
    min_q3_token_d = min(int(row["banglish_D"]) for row in q3_token_quartiles)

    lines = [
        "# Frozen-V5 BEnQA Length/Token Confound Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether Qwen3-4B's reviewed-Banglish BEnQA",
        "D-attractor can be reduced to prompt length or tokenization burden. It",
        "joins frozen-v5 BEnQA choice-bias rows with the reviewed-Banglish",
        "tokenization audit. The audited tokenizer is the Qwen3-4B tokenizer;",
        "prior tokenization checks showed the thesis-facing Qwen tokenizers have",
        "identical counts on frozen-v5 item/variant pairs.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- Across reviewed-Banglish HF-token quartiles, Qwen3-4B predicts D on "
            f"{q3_token_d} rows; every quartile is at least "
            f"{min_q3_token_d}/36 ({percent(min_q3_token_d, 36)})."
        ),
        (
            "- Wrong-D counts by the same token quartiles are "
            f"{q3_token_wrong_d}; the shortest-token quartile is "
            f"{q3_token_quartiles[0]['banglish_wrong_D']}/36."
        ),
        (
            "- By character-length quartile, Qwen3-4B still predicts D on "
            f"{q3_char_q1['banglish_D']}/{q3_char_q1['n']} shortest rows and "
            f"{q3_char_q4['banglish_D']}/{q3_char_q4['n']} longest rows."
        ),
        (
            "- By token-density quartile, Qwen3-4B predicts D on "
            f"{q3_density_q1['banglish_D']}/{q3_density_q1['n']} lowest-density rows and "
            f"{q3_density_q4['banglish_D']}/{q3_density_q4['n']} highest-density rows."
        ),
        (
            "- Qwen2.5 rows remain much lower in the shortest and longest HF-token "
            f"quartiles: {q25_3_token_q1['banglish_D']}/{q25_3_token_q1['n']} and "
            f"{q25_7_token_q1['banglish_D']}/{q25_7_token_q1['n']} in Q1; "
            f"{q25_3_token_q4['banglish_D']}/{q25_3_token_q4['n']} and "
            f"{q25_7_token_q4['banglish_D']}/{q25_7_token_q4['n']} in Q4."
        ),
        "",
        "## HF-Token Quartiles",
        "",
        "| Model | Q1 D | Q2 D | Q3 D | Q4 D | Q1 wrong D | Q4 wrong D |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        q1 = row_for(summary_rows, model, "banglish_hf_tokens", "q1")
        q2 = row_for(summary_rows, model, "banglish_hf_tokens", "q2")
        q3 = row_for(summary_rows, model, "banglish_hf_tokens", "q3")
        q4 = row_for(summary_rows, model, "banglish_hf_tokens", "q4")
        lines.append(
            f"| {model} | {q1['banglish_D']}/{q1['n']} | {q2['banglish_D']}/{q2['n']} | "
            f"{q3['banglish_D']}/{q3['n']} | {q4['banglish_D']}/{q4['n']} | "
            f"{q1['banglish_wrong_D']}/{q1['n']} | {q4['banglish_wrong_D']}/{q4['n']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The Qwen3 D-attractor is strongest in the shortest reviewed-Banglish",
            "  HF-token quartile, so it is not a simple long-prompt or token-heavy",
            "  failure mode.",
            "- Character length, word count, and token-density quartiles all keep the",
            "  Qwen3 D pattern visible, while Qwen2.5 rows remain far less D-heavy.",
            "- This complements the broader tokenization audit: reviewed Banglish is",
            "  token-cheaper than Bangla overall, and the option collapse is not",
            "  concentrated in token-heavy BEnQA rows.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_length_token_confound.py`",
            f"- Item table: `{repo_path(items_output)}`",
            f"- Summary table: `{repo_path(summary_output)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--token-audit", type=Path, default=DEFAULT_TOKEN_AUDIT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.choice_items, args.token_audit)
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    q3_q1 = row_for(summary_rows, "Qwen3-4B", "banglish_hf_tokens", "q1")
    q3_q4 = row_for(summary_rows, "Qwen3-4B", "banglish_hf_tokens", "q4")
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"qwen3_token_q1_D={q3_q1['banglish_D']}/{q3_q1['n']} "
        f"qwen3_token_q4_D={q3_q4['banglish_D']}/{q3_q4['n']} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
