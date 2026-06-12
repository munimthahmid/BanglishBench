#!/usr/bin/env python3
"""Build frozen-v5 tokenization/failure-pattern mechanism report."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from analyze_cross_script_token_patterns import (
    build_token_index,
    join_rows,
    read_csv,
    summarize,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY = (
    ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
)
DEFAULT_TOKENIZATION_AUDIT = ROOT / "results/tokenization/validation200_v5/audit.csv"
DEFAULT_TOKENIZATION_SUMMARY = ROOT / "results/tokenization/validation200_v5/summary.csv"
DEFAULT_ITEMS_OUTPUT = (
    ROOT / "results/analysis/validation200_v5_cross_script_token_patterns_items.csv"
)
DEFAULT_SUMMARY_OUTPUT = (
    ROOT / "results/analysis/validation200_v5_cross_script_token_patterns_summary.csv"
)
DEFAULT_REPORT = ROOT / "reports/tokenization_cross_script_failure_patterns.md"

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
DATASET_LABELS = {
    "benqa": "BEnQA",
    "banglamath": "BanglaMATH",
}
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


def fnum(row: dict[str, Any], key: str) -> float:
    value = row.get(key, 0)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def fmt(value: Any, places: int = 1) -> str:
    return f"{float(value):.{places}f}"


def row_index(
    rows: list[dict[str, Any]], group: str, *keys: str
) -> dict[tuple[str, ...], dict[str, Any]]:
    return {
        tuple(str(row[key]) for key in keys): row
        for row in rows
        if row.get("group") == group
    }


def tokenization_summary_table(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if row["tokenizer"] != "unicode_baseline"
        and row["tokenizer"] == "Qwen/Qwen3-4B-Instruct-2507"
    ]
    grouped = {(row["dataset"], row["variant"]): row for row in selected}
    out: list[dict[str, str]] = []
    for dataset in ("benqa", "banglamath"):
        record = {"dataset": DATASET_LABELS[dataset]}
        for variant in ("bangla", "banglish_clean", "english"):
            record[variant] = grouped[(dataset, variant)]["mean_hf_tokens_per_word"]
        out.append(record)
    return out


def tokenizer_consistency(rows: list[dict[str, str]]) -> tuple[int, int, list[str]]:
    grouped: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    tokenizers: set[str] = set()
    for row in rows:
        tokenizer = row["tokenizer"]
        if tokenizer == "unicode_baseline":
            continue
        tokenizers.add(tokenizer)
        grouped[(row["id"], row["variant"])][tokenizer] = row["hf_tokens"]
    mismatches = sum(1 for values in grouped.values() if len(set(values.values())) > 1)
    return mismatches, len(grouped), sorted(tokenizers)


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    token_summary_rows: list[dict[str, str]],
    token_audit_rows: list[dict[str, str]],
    taxonomy: Path,
    tokenization_audit: Path,
    items_output: Path,
    summary_output: Path,
) -> None:
    token_mismatches, token_groups, tokenizers = tokenizer_consistency(token_audit_rows)
    recoverable = row_index(
        summary_rows,
        "by_model_dataset_banglish_wrong_other_correct",
        "model",
        "dataset",
        "banglish_wrong_other_correct",
    )
    strict = row_index(
        summary_rows,
        "by_model_dataset_pattern",
        "model",
        "dataset",
        "pattern",
    )
    lines = [
        "# Tokenization vs Cross-Script Failure Patterns",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This report joins the frozen-v5 cross-script failure taxonomy with",
        "validation-200 v5 tokenizer metrics. The mechanism question is narrow:",
        "",
        "> Are reviewed-Banglish failures that are recoverable under Bangla or",
        "> English simply the long/token-heavy Banglish prompts?",
        "",
        "The answer remains no under the frozen-v5 evidence.",
        "",
        "## Artifacts",
        "",
        f"- Builder: `scripts/build_v5_tokenization_failure_patterns.py`",
        f"- Joined item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        f"- Source taxonomy: `{repo_path(taxonomy)}`",
        f"- Source tokenization audit: `{repo_path(tokenization_audit)}`",
        "- Source tokenization summary: `results/tokenization/validation200_v5/summary.csv`",
        "",
        "## Tokenization Summary",
        "",
        "The three thesis-facing Qwen tokenizers produce identical item-level",
        f"token counts for {token_groups} frozen-v5 item/variant pairs",
        f"({token_mismatches} mismatches across tokenizers).",
        "",
        "Tokenizers audited:",
    ]
    lines.extend([f"- `{tokenizer}`" for tokenizer in tokenizers])
    lines.extend(
        [
            "",
            "Mean HF tokens per word:",
            "",
            "| Dataset | Bangla | Reviewed Banglish | English |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in tokenization_summary_table(token_summary_rows):
        lines.append(
            f"| {row['dataset']} | {fmt(row['bangla'], 4)} | "
            f"{fmt(row['banglish_clean'], 4)} | {fmt(row['english'], 4)} |"
        )
    lines.extend(
        [
            "",
            "## Recoverable Banglish Misses",
            "",
            "Rows where `banglish_wrong_other_correct=True` are items where reviewed",
            "Banglish is wrong but at least one other script variant is correct.",
            "",
            "| Model | Dataset | Recoverable? | n | Mean Bangla tokens | Mean Banglish tokens | Banglish/Bangla token ratio | Banglish tokens/word |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        for dataset in ("banglamath", "benqa"):
            for value in ("False", "True"):
                row = recoverable[(model, dataset, value)]
                lines.append(
                    f"| {MODEL_LABELS[model]} | {DATASET_LABELS[dataset]} | "
                    f"{'yes' if value == 'True' else 'no'} | {row['n']} | "
                    f"{fmt(row['mean_bangla_tokens'])} | "
                    f"{fmt(row['mean_banglish_tokens'])} | "
                    f"{fmt(row['mean_banglish_over_bangla_tokens'], 3)} | "
                    f"{fmt(row['mean_banglish_tokens_per_word'], 3)} |"
                )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- Recoverable reviewed-Banglish misses are not longer in Banglish token",
            "  count.",
            "- In BEnQA, recoverable misses are shorter on average than other rows for",
            "  all three thesis-facing Qwen models.",
            "- BanglaMATH recoverable groups are small, so they are descriptive only.",
            "",
            "## Strongest Script-Specific Pattern",
            "",
            "For `bangla_english_correct_banglish_wrong`, both Bangla and English are",
            "correct while reviewed Banglish is wrong.",
            "",
            "| Model | Dataset | n | Mean Bangla tokens | Mean Banglish tokens | Banglish/Bangla token ratio | Banglish tokens/word |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        for dataset in ("banglamath", "benqa"):
            row = strict[(model, dataset, "bangla_english_correct_banglish_wrong")]
            lines.append(
                f"| {MODEL_LABELS[model]} | {DATASET_LABELS[dataset]} | "
                f"{row['n']} | {fmt(row['mean_bangla_tokens'])} | "
                f"{fmt(row['mean_banglish_tokens'])} | "
                f"{fmt(row['mean_banglish_over_bangla_tokens'], 3)} | "
                f"{fmt(row['mean_banglish_tokens_per_word'], 3)} |"
            )
    lines.extend(
        [
            "",
            "These are the cleanest script-specific failures, and they are still",
            "token-cheaper in reviewed Banglish than native Bangla.",
            "",
            "## Thesis-Safe Claim",
            "",
            "Use:",
            "",
            "> Token count does not explain the cross-script Banglish failures. The",
            "> script-specific reviewed-Banglish misses are not the longest Banglish",
            "> prompts; many are token-cheaper than the corresponding native Bangla",
            "> prompts and shorter than non-recoverable items.",
            "",
            "Avoid:",
            "",
            "- Claiming tokenization has no role at all.",
            "- Claiming this proves an internal mechanism.",
            "- Treating small BanglaMATH pattern groups as standalone statistical",
            "  evidence.",
            "",
            "## Implication",
            "",
            "The failure is more consistent with representation, lexical grounding,",
            "training distribution, or script-conditioned task interpretation than",
            "with a simple context-budget or token-length bottleneck.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--tokenization-audit", type=Path, default=DEFAULT_TOKENIZATION_AUDIT)
    parser.add_argument(
        "--tokenization-summary", type=Path, default=DEFAULT_TOKENIZATION_SUMMARY
    )
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in [args.taxonomy, args.tokenization_audit, args.tokenization_summary]:
        if not path.exists():
            raise SystemExit(f"Missing required input: {path}")
    token_audit_rows = read_csv(args.tokenization_audit)
    token_rows = build_token_index(token_audit_rows)
    joined = join_rows(read_csv(args.taxonomy), token_rows)
    summary = summarize(joined)
    if len(joined) != 600:
        raise SystemExit(f"Expected 600 joined rows, got {len(joined)}")
    if len(summary) != 78:
        raise SystemExit(f"Expected 78 summary rows, got {len(summary)}")
    mismatches, token_groups, _ = tokenizer_consistency(token_audit_rows)
    if token_groups != 600:
        raise SystemExit(f"Expected 600 tokenized item/variant groups, got {token_groups}")
    if mismatches != 0:
        raise SystemExit(f"Expected identical Qwen tokenizer counts, got {mismatches} mismatches")
    write_csv(args.items_output, joined)
    write_csv(args.summary_output, summary)
    write_report(
        args.report_output,
        summary,
        read_csv(args.tokenization_summary),
        token_audit_rows,
        args.taxonomy,
        args.tokenization_audit,
        args.items_output,
        args.summary_output,
    )
    print(f"joined={len(joined)}")
    print(f"summary_rows={len(summary)}")
    print(f"tokenizer_mismatches={mismatches}/{token_groups}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
