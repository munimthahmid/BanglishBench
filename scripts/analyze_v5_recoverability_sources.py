#!/usr/bin/env python3
"""Decompose frozen-v5 Banglish misses by alternate-script recovery source."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_recoverability_source_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_recoverability_source_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_recoverability_source_decomposition.md"

MODEL_IDS = (
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen3-4B-Instruct-2507",
)
MODEL_LABELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}
DATASETS = ("all", "benqa", "banglamath")
PATTERNS = (
    "all_wrong",
    "bangla_only_correct",
    "english_only_correct",
    "bangla_english_correct_banglish_wrong",
    "banglish_only_correct",
    "bangla_banglish_correct_english_wrong",
    "banglish_english_correct_bangla_wrong",
    "all_correct",
)
PATTERN_DETAILS = {
    "all_wrong": "No script view is correct",
    "bangla_only_correct": "Only native Bangla is correct",
    "english_only_correct": "Only English is correct",
    "bangla_english_correct_banglish_wrong": "Bangla and English are correct; Banglish is wrong",
    "banglish_only_correct": "Only reviewed Banglish is correct",
    "bangla_banglish_correct_english_wrong": "Bangla and Banglish are correct; English is wrong",
    "banglish_english_correct_bangla_wrong": "Banglish and English are correct; Bangla is wrong",
    "all_correct": "All three script views are correct",
}
BANGLISH_CORRECT_PATTERNS = {
    "banglish_only_correct",
    "bangla_banglish_correct_english_wrong",
    "banglish_english_correct_bangla_wrong",
    "all_correct",
}
RECOVERABLE_MISS_PATTERNS = {
    "bangla_only_correct",
    "english_only_correct",
    "bangla_english_correct_banglish_wrong",
}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def percent(count: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * count / denominator:.1f}%"


def source_class(pattern: str) -> str:
    if pattern == "all_wrong":
        return "all_script_hard"
    if pattern == "bangla_only_correct":
        return "bangla_only_recovery"
    if pattern == "english_only_correct":
        return "english_only_recovery"
    if pattern == "bangla_english_correct_banglish_wrong":
        return "both_alternate_recovery"
    if pattern == "banglish_only_correct":
        return "banglish_unique_success"
    if pattern == "bangla_banglish_correct_english_wrong":
        return "banglish_and_bangla_success"
    if pattern == "banglish_english_correct_bangla_wrong":
        return "banglish_and_english_success"
    if pattern == "all_correct":
        return "all_scripts_success"
    return "unknown"


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        pattern = row["pattern"]
        if pattern not in PATTERNS:
            raise SystemExit(f"Unexpected pattern {pattern!r} for {row.get('id', '<unknown>')}")
        bangla_correct = truthy(row["bangla_correct"])
        banglish_correct = truthy(row["banglish_clean_correct"])
        english_correct = truthy(row["english_correct"])
        out.append(
            {
                "model": MODEL_LABELS.get(row["model"], row["model"]),
                "model_id": row["model"],
                "dataset": row["dataset"],
                "task_type": row.get("task_type", ""),
                "answer_type": row.get("answer_type", ""),
                "id": row["id"],
                "domain": row.get("domain", ""),
                "subject": row.get("subject", ""),
                "grade": row.get("grade", ""),
                "pattern": pattern,
                "source_class": source_class(pattern),
                "bangla_correct": bangla_correct,
                "banglish_correct": banglish_correct,
                "english_correct": english_correct,
                "banglish_wrong": not banglish_correct,
                "recoverable_banglish_miss": (not banglish_correct) and (bangla_correct or english_correct),
                "bangla_only_recovery": pattern == "bangla_only_correct",
                "english_only_recovery": pattern == "english_only_correct",
                "both_alternate_recovery": pattern == "bangla_english_correct_banglish_wrong",
                "bangla_any_recovery": (not banglish_correct) and bangla_correct,
                "english_any_recovery": (not banglish_correct) and english_correct,
                "all_script_hard": pattern == "all_wrong",
                "banglish_unique_success": pattern == "banglish_only_correct",
                "gold": row.get("gold", ""),
            }
        )
    return out


def add_summary(
    rows: list[dict[str, Any]],
    model_group: str,
    dataset: str,
    metric: str,
    n: int,
    denominator: int,
    detail: str,
) -> None:
    rows.append(
        {
            "model_group": model_group,
            "dataset": dataset,
            "metric": metric,
            "n": n,
            "denominator": denominator,
            "rate": round(n / denominator, 4) if denominator else 0.0,
            "detail": detail,
        }
    )


def summarize_group(rows: list[dict[str, Any]], model_group: str, dataset: str) -> list[dict[str, Any]]:
    pattern_counts = Counter(str(row["pattern"]) for row in rows)
    n_rows = len(rows)
    banglish_correct = sum(pattern_counts[pattern] for pattern in BANGLISH_CORRECT_PATTERNS)
    banglish_wrong = n_rows - banglish_correct
    recoverable = sum(pattern_counts[pattern] for pattern in RECOVERABLE_MISS_PATTERNS)
    bangla_only = pattern_counts["bangla_only_correct"]
    english_only = pattern_counts["english_only_correct"]
    both_alternate = pattern_counts["bangla_english_correct_banglish_wrong"]
    all_hard = pattern_counts["all_wrong"]
    bangla_any = bangla_only + both_alternate
    english_any = english_only + both_alternate
    out: list[dict[str, Any]] = []

    for pattern in PATTERNS:
        add_summary(
            out,
            model_group,
            dataset,
            f"pattern:{pattern}",
            pattern_counts[pattern],
            n_rows,
            PATTERN_DETAILS[pattern],
        )

    count_metrics = [
        ("banglish_correct", banglish_correct, n_rows, "Reviewed Banglish correct model-item slots"),
        ("banglish_wrong", banglish_wrong, n_rows, "Reviewed Banglish incorrect model-item slots"),
        ("recoverable_banglish_miss", recoverable, n_rows, "Banglish miss where Bangla or English is correct"),
        ("all_script_hard", all_hard, n_rows, "No script view is correct"),
        ("bangla_any_recovery", bangla_any, n_rows, "Banglish miss recoverable by native Bangla"),
        ("english_any_recovery", english_any, n_rows, "Banglish miss recoverable by English"),
        ("bangla_only_recovery", bangla_only, n_rows, "Only native Bangla recovers the Banglish miss"),
        ("english_only_recovery", english_only, n_rows, "Only English recovers the Banglish miss"),
        ("both_alternate_recovery", both_alternate, n_rows, "Both Bangla and English recover the Banglish miss"),
        ("banglish_unique_success", pattern_counts["banglish_only_correct"], n_rows, "Only Banglish is correct"),
    ]
    for metric, count, denominator, detail in count_metrics:
        add_summary(out, model_group, dataset, metric, count, denominator, detail)

    miss_share_metrics = [
        ("miss_share:recoverable_banglish_miss", recoverable, "Share of Banglish misses recoverable by Bangla or English"),
        ("miss_share:all_script_hard", all_hard, "Share of Banglish misses with no script correct"),
        ("miss_share:bangla_any_recovery", bangla_any, "Share of Banglish misses recoverable by native Bangla"),
        ("miss_share:english_any_recovery", english_any, "Share of Banglish misses recoverable by English"),
        ("miss_share:bangla_only_recovery", bangla_only, "Share of Banglish misses recoverable only by native Bangla"),
        ("miss_share:english_only_recovery", english_only, "Share of Banglish misses recoverable only by English"),
        ("miss_share:both_alternate_recovery", both_alternate, "Share of Banglish misses recovered by both alternate scripts"),
    ]
    for metric, count, detail in miss_share_metrics:
        add_summary(out, model_group, dataset, metric, count, banglish_wrong, detail)
    return out


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    groups: list[tuple[str, list[dict[str, Any]]]] = [("all_models", item_rows)]
    for model_id in MODEL_IDS:
        groups.append(
            (
                MODEL_LABELS[model_id],
                [row for row in item_rows if row["model_id"] == model_id],
            )
        )

    for model_group, group_rows in groups:
        for dataset in DATASETS:
            rows = group_rows if dataset == "all" else [
                row for row in group_rows if row["dataset"] == dataset
            ]
            summary.extend(summarize_group(rows, model_group, dataset))
    return summary


def metric(
    summary_rows: list[dict[str, Any]],
    model_group: str,
    dataset: str,
    metric_name: str,
) -> dict[str, Any]:
    return next(
        row
        for row in summary_rows
        if row["model_group"] == model_group
        and row["dataset"] == dataset
        and row["metric"] == metric_name
    )


def count(
    summary_rows: list[dict[str, Any]],
    model_group: str,
    dataset: str,
    metric_name: str,
) -> int:
    return int(metric(summary_rows, model_group, dataset, metric_name)["n"])


def count_rate(
    summary_rows: list[dict[str, Any]],
    model_group: str,
    dataset: str,
    metric_name: str,
) -> str:
    row = metric(summary_rows, model_group, dataset, metric_name)
    return f"{row['n']}/{row['denominator']} ({percent(int(row['n']), int(row['denominator']))})"


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    all_misses = count(summary_rows, "all_models", "all", "banglish_wrong")
    all_recoverable = count(summary_rows, "all_models", "all", "recoverable_banglish_miss")
    all_hard = count(summary_rows, "all_models", "all", "all_script_hard")
    all_bangla_any = count(summary_rows, "all_models", "all", "bangla_any_recovery")
    all_english_any = count(summary_rows, "all_models", "all", "english_any_recovery")
    all_bangla_only = count(summary_rows, "all_models", "all", "bangla_only_recovery")
    all_english_only = count(summary_rows, "all_models", "all", "english_only_recovery")
    all_both = count(summary_rows, "all_models", "all", "both_alternate_recovery")
    all_unique = count(summary_rows, "all_models", "all", "banglish_unique_success")

    lines = [
        "# Frozen-V5 Recoverability Source Decomposition",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit decomposes every thesis-facing Qwen model-item slot",
        "by which script views are correct on the same frozen-v5 item. It turns",
        "the cross-script oracle into a source attribution table: native Bangla",
        "only, English only, both alternate scripts, or no script view correct.",
        "",
        f"- Input failure rows: `{repo_path(DEFAULT_INPUT)}`",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "Counts are descriptive and paired by item/model. They do not define a",
        "deployable route because Bangla and English views are benchmark-provided.",
        "",
        "## Overall Source Decomposition",
        "",
        "| Dataset | Banglish wrong | Recoverable by Bangla/English | All-script hard | Bangla-only recovery | English-only recovery | Both alternates | Banglish-only success |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for dataset in DATASETS:
        lines.append(
            f"| {dataset} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'banglish_wrong')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'recoverable_banglish_miss')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'all_script_hard')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'bangla_only_recovery')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'english_only_recovery')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'both_alternate_recovery')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'banglish_unique_success')} |"
        )

    lines.extend(
        [
            "",
            "## By Model",
            "",
            "| Model | Banglish correct | Banglish wrong | Recoverable miss | All-script hard | Bangla-only | English-only | Both alternates | Banglish-only success |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in (MODEL_LABELS[model_id] for model_id in MODEL_IDS):
        lines.append(
            f"| {model} | "
            f"{count_rate(summary_rows, model, 'all', 'banglish_correct')} | "
            f"{count_rate(summary_rows, model, 'all', 'banglish_wrong')} | "
            f"{count_rate(summary_rows, model, 'all', 'recoverable_banglish_miss')} | "
            f"{count_rate(summary_rows, model, 'all', 'all_script_hard')} | "
            f"{count_rate(summary_rows, model, 'all', 'bangla_only_recovery')} | "
            f"{count_rate(summary_rows, model, 'all', 'english_only_recovery')} | "
            f"{count_rate(summary_rows, model, 'all', 'both_alternate_recovery')} | "
            f"{count_rate(summary_rows, model, 'all', 'banglish_unique_success')} |"
        )

    lines.extend(
        [
            "",
            "## Miss-Conditioned Shares",
            "",
            "| Dataset | Recoverable share of Banglish misses | All-script-hard share | Native Bangla participates | English participates |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for dataset in DATASETS:
        lines.append(
            f"| {dataset} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'miss_share:recoverable_banglish_miss')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'miss_share:all_script_hard')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'miss_share:bangla_any_recovery')} | "
            f"{count_rate(summary_rows, 'all_models', dataset, 'miss_share:english_any_recovery')} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Across 600 model-item slots, reviewed Banglish is wrong in",
            f"  {all_misses}/600 slots. Of those misses, {all_recoverable}/{all_misses}",
            f"  ({percent(all_recoverable, all_misses)}) are recoverable by native",
            f"  Bangla or English, while {all_hard}/{all_misses}",
            f"  ({percent(all_hard, all_misses)}) are all-script hard.",
            f"- Recovery is not just an English-only effect: native Bangla participates",
            f"  in {all_bangla_any}/{all_recoverable} recoverable misses, English",
            f"  participates in {all_english_any}/{all_recoverable}, and",
            f"  {all_both}/{all_recoverable} are recovered by both alternate scripts.",
            f"- English-only recovery is still the largest single source",
            f"  ({all_english_only}/{all_recoverable}), followed by both-alternate",
            f"  recovery ({all_both}/{all_recoverable}) and Bangla-only recovery",
            f"  ({all_bangla_only}/{all_recoverable}).",
            f"- Banglish-only success exists on {all_unique}/600 slots. Keep that",
            "  counterevidence in the limitations: the result is a robust aggregate",
            "  gap, not a claim that Banglish is always worse item by item.",
            "- BEnQA contains most recoverable misses, while BanglaMATH is dominated by",
            "  all-script-hard rows; that supports using BanglaMATH as a stress-test",
            "  slice rather than the cleanest source-attribution stratum.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_recoverability_sources.py`",
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
    rows = read_csv(args.input)
    if len(rows) != 600:
        raise SystemExit(f"Expected 600 model-item failure rows, got {len(rows)}")
    item_rows = build_item_rows(rows)
    summary_rows = build_summary_rows(item_rows)
    item_fields = list(item_rows[0])
    summary_fields = ["model_group", "dataset", "metric", "n", "denominator", "rate", "detail"]
    write_csv(args.items_output, item_rows, item_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
