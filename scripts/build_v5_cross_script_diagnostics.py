#!/usr/bin/env python3
"""Refresh cross-script diagnostics with frozen-v5 reviewed Banglish outputs."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Any

from analyze_cross_script_answer_agreement import (
    build_item_rows as build_agreement_items,
)
from analyze_cross_script_answer_agreement import load_rows as load_agreement_rows
from analyze_cross_script_answer_agreement import summarize as summarize_agreement
from analyze_cross_script_answer_agreement import write_csv as write_agreement_csv
from analyze_cross_script_failure_patterns import (
    build_item_rows as build_failure_items,
)
from analyze_cross_script_failure_patterns import load_eval_rows as load_failure_rows
from analyze_cross_script_failure_patterns import load_items
from analyze_cross_script_failure_patterns import summarize as summarize_failures
from analyze_cross_script_failure_patterns import write_csv as write_failure_csv
from oracle_union_variants import load_rows as load_oracle_rows
from oracle_union_variants import summarize as summarize_oracle
from oracle_union_variants import write_csv as write_oracle_csv


ROOT = Path(__file__).resolve().parents[1]
SLICE = ROOT / "data/slices/validation_200_v5.jsonl"
AGREEMENT_ITEMS = ROOT / "results/analysis/validation200_v5_cross_script_answer_agreement_items.csv"
AGREEMENT_BUCKETS = ROOT / "results/analysis/validation200_v5_cross_script_answer_agreement_buckets.csv"
AGREEMENT_ROUTES = ROOT / "results/analysis/validation200_v5_cross_script_answer_agreement_routes.csv"
FAILURE_ITEMS = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
FAILURE_SUMMARY = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_summary.csv"
ORACLE_SUMMARY = ROOT / "results/analysis/validation200_v5_cross_script_oracle_union.csv"
DIAGNOSTIC_SUMMARY = ROOT / "results/analysis/validation200_v5_cross_script_diagnostics_summary.csv"
REPORT = ROOT / "reports/cross_script_diagnostics_validation200_v5.md"
HISTORICAL_ROUTES = ROOT / "results/analysis/validation200_cross_script_answer_agreement_routes.csv"

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

MODELS = [
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen3-4B-Instruct-2507",
]
MODEL_LABELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def points(value: Any) -> str:
    value = float(value) * 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def route_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row["model"]), str(row["route"])): row
        for row in rows
        if row["dataset"] == "all"
    }


def oracle_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(str(row["model"]), str(row["dataset"])): row for row in rows}


def failure_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str, str], dict[str, Any]]:
    return {
        (str(row["model"]), str(row["dataset"]), str(row["pattern"])): row
        for row in rows
    }


def sum_oracle(oracle: dict[tuple[str, str], dict[str, Any]], model: str, key: str) -> int:
    return sum(int(oracle[(model, dataset)][key]) for dataset in ["benqa", "banglamath"])


def build_summary(
    route_rows: list[dict[str, Any]],
    oracle_rows: list[dict[str, Any]],
    failure_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    routes = route_index(route_rows)
    oracle = oracle_index(oracle_rows)
    failures = failure_index(failure_rows)
    historical = route_index(read_csv(HISTORICAL_ROUTES))
    out: list[dict[str, Any]] = []
    for model in MODELS:
        route = routes[(model, "bangla_english_agreement_route")]
        historical_route = historical[(model, "bangla_english_agreement_route")]
        overall_failure = failures[(model, "all", "all_wrong")]
        out.append(
            {
                "model": MODEL_LABELS[model],
                "n": route["n"],
                "bangla_correct": sum_oracle(oracle, model, "bangla_correct"),
                "reviewed_banglish_correct": route["banglish_correct"],
                "english_correct": sum_oracle(oracle, model, "english_correct"),
                "agreement_route_correct": route["route_correct"],
                "agreement_route_delta": round(float(route["delta_route_minus_banglish"]), 4),
                "agreement_route_ci95_low": round(float(route["ci95_low"]), 4),
                "agreement_route_ci95_high": round(float(route["ci95_high"]), 4),
                "oracle_correct": sum_oracle(oracle, model, "oracle_correct"),
                "recoverable_banglish_misses": overall_failure[
                    "banglish_wrong_other_correct_total"
                ],
                "bangla_english_correct_banglish_wrong": failures[
                    (model, "all", "bangla_english_correct_banglish_wrong")
                ]["n"],
                "historical_banglish_correct": historical_route["banglish_correct"],
                "historical_agreement_route_correct": historical_route["route_correct"],
            }
        )
    return out


def write_report(summary: list[dict[str, Any]], oracle_rows: list[dict[str, Any]]) -> None:
    oracle = oracle_index(oracle_rows)
    lines = [
        "# Frozen-V5 Cross-Script Diagnostics",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This report refreshes the diagnostic cross-script oracle, failure taxonomy,",
        "and privileged Bangla+English agreement route against frozen-v5 reviewed",
        "Banglish outputs. Bangla and English outputs are reused because those fields",
        "did not change. No new model inference or paid API call is required.",
        "",
        "The agreement route remains diagnostic rather than deployable: it uses",
        "benchmark-provided alternate-script views.",
        "",
        "## Reviewed-V5 Route Result",
        "",
        "| Model | Reviewed Banglish | Agreement route | Delta | 95% CI | Any-script oracle |",
        "| --- | ---: | ---: | ---: | --- | ---: |",
    ]
    for row in summary:
        lines.append(
            f"| {row['model']} | {row['reviewed_banglish_correct']}/{row['n']} | "
            f"{row['agreement_route_correct']}/{row['n']} | "
            f"{points(row['agreement_route_delta'])} pts | "
            f"[{points(row['agreement_route_ci95_low'])}, {points(row['agreement_route_ci95_high'])}] | "
            f"{row['oracle_correct']}/{row['n']} |"
        )
    lines.extend(
        [
            "",
            "## Historical-To-Reviewed Comparison",
            "",
            "| Model | Historical Banglish | Historical route | Reviewed Banglish | Reviewed route |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary:
        lines.append(
            f"| {row['model']} | {row['historical_banglish_correct']}/{row['n']} | "
            f"{row['historical_agreement_route_correct']}/{row['n']} | "
            f"{row['reviewed_banglish_correct']}/{row['n']} | "
            f"{row['agreement_route_correct']}/{row['n']} |"
        )
    lines.extend(
        [
            "",
            "## Reviewed-V5 Failure Taxonomy",
            "",
            "| Model | Banglish misses recoverable under Bangla or English | Bangla+English correct, Banglish wrong |",
            "| --- | ---: | ---: |",
        ]
    )
    for row in summary:
        lines.append(
            f"| {row['model']} | {row['recoverable_banglish_misses']}/{row['n']} | "
            f"{row['bangla_english_correct_banglish_wrong']}/{row['n']} |"
        )
    lines.extend(
        [
            "",
            "## Reviewed-V5 Oracle By Dataset",
            "",
            "| Model | Dataset | Bangla | Reviewed Banglish | English | Any-script oracle |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        for dataset in ["benqa", "banglamath"]:
            row = oracle[(model, dataset)]
            lines.append(
                f"| {MODEL_LABELS[model]} | {dataset} | {row['bangla_correct']}/{row['n']} | "
                f"{row['banglish_clean_correct']}/{row['n']} | {row['english_correct']}/{row['n']} | "
                f"{row['oracle_correct']}/{row['n']} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Reviewed cleanup does not remove cross-script recoverability.",
            "- The privileged agreement route remains clearly positive for Qwen2.5-7B",
            "  8-bit and Qwen3-4B.",
            "- Qwen2.5-3B retains a +4.0-point route gain, but its reviewed-v5 interval",
            "  crosses zero. Keep that uncertainty explicit.",
            "- Oracle headroom remains large for every thesis-facing Qwen row.",
            "- Use these results as mitigation-design evidence, not deployed accuracy.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/build_v5_cross_script_diagnostics.py`",
            f"- Summary: `{DIAGNOSTIC_SUMMARY.relative_to(ROOT)}`",
            f"- Agreement items: `{AGREEMENT_ITEMS.relative_to(ROOT)}`",
            f"- Agreement buckets: `{AGREEMENT_BUCKETS.relative_to(ROOT)}`",
            f"- Agreement routes: `{AGREEMENT_ROUTES.relative_to(ROOT)}`",
            f"- Failure items: `{FAILURE_ITEMS.relative_to(ROOT)}`",
            f"- Failure summary: `{FAILURE_SUMMARY.relative_to(ROOT)}`",
            f"- Oracle summary: `{ORACLE_SUMMARY.relative_to(ROOT)}`",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    for path in [SLICE, HISTORICAL_ROUTES, *INPUTS]:
        if not path.exists():
            raise SystemExit(f"Missing required input: {path}")

    agreement_rows = load_agreement_rows(INPUTS, rescore=True)
    agreement_items = build_agreement_items(agreement_rows)
    bucket_rows, route_rows = summarize_agreement(agreement_items, samples=10000, seed=42)
    failure_items = build_failure_items(
        load_failure_rows(INPUTS, rescore=True),
        load_items(SLICE),
        ["bangla", "banglish_clean", "english"],
    )
    failure_rows = summarize_failures(failure_items)
    oracle_rows = summarize_oracle(
        load_oracle_rows(INPUTS, rescore=True),
        ["bangla", "banglish_clean", "english"],
    )
    if len(agreement_items) != 600 or len(failure_items) != 600 or len(oracle_rows) != 6:
        raise SystemExit(
            "Unexpected diagnostic sizes: "
            f"agreement={len(agreement_items)} failure={len(failure_items)} oracle={len(oracle_rows)}"
        )

    write_agreement_csv(AGREEMENT_ITEMS, agreement_items)
    write_agreement_csv(AGREEMENT_BUCKETS, bucket_rows)
    write_agreement_csv(AGREEMENT_ROUTES, route_rows)
    write_failure_csv(FAILURE_ITEMS, failure_items)
    write_failure_csv(FAILURE_SUMMARY, failure_rows)
    write_oracle_csv(ORACLE_SUMMARY, oracle_rows)
    summary = build_summary(route_rows, oracle_rows, failure_rows)
    write_csv(DIAGNOSTIC_SUMMARY, summary)
    write_report(summary, oracle_rows)
    print(f"items={len(agreement_items)}")
    print(f"summary={DIAGNOSTIC_SUMMARY}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
