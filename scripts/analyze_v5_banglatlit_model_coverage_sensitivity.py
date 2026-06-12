#!/usr/bin/env python3
"""Per-model sensitivity of the frozen-v5 gap to BanglaTLit lexical coverage."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE_ITEMS = ROOT / "results/analysis/v5_banglatlit_lexical_coverage_items.csv"
DEFAULT_FRAGILITY_ITEMS = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_DATASET_INTERVALS = ROOT / "results/analysis/v5_dataset_gap_intervals.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_banglatlit_model_coverage_sensitivity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_banglatlit_model_coverage_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglatlit_model_coverage_sensitivity.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
DATASETS = ("all", "benqa", "banglamath")
BOOTSTRAPS = 5000
SEED = 20260531


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def to_int(value: Any) -> int:
    return int(str(value).strip() or 0)


def to_float(value: Any) -> float:
    return float(str(value).strip() or 0)


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def pct(value: Any) -> str:
    return f"{float(value) * 100:.1f}"


def stable_seed(label: str) -> int:
    return SEED + sum((idx + 1) * ord(ch) for idx, ch in enumerate(label))


def quartile_labels(rows: list[dict[str, str]], dataset: str) -> dict[str, str]:
    selected = rows if dataset == "all" else [row for row in rows if row["dataset"] == dataset]
    sorted_rows = sorted(selected, key=lambda row: (to_float(row["token_coverage"]), row["id"]))
    labels: dict[str, str] = {}
    n = len(sorted_rows)
    for index in range(4):
        start = index * n // 4
        end = (index + 1) * n // 4
        for row in sorted_rows[start:end]:
            labels[row["id"]] = f"q{index + 1}"
    return labels


def build_item_rows(
    coverage_rows: list[dict[str, str]],
    fragility_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    fragility_by_id = {row["id"]: row for row in fragility_rows}
    all_labels = quartile_labels(coverage_rows, "all")
    dataset_labels = {
        dataset: quartile_labels(coverage_rows, dataset) for dataset in ("benqa", "banglamath")
    }
    out: list[dict[str, Any]] = []
    for coverage in coverage_rows:
        fragility = fragility_by_id[coverage["id"]]
        dataset = coverage["dataset"]
        for model in MODELS:
            bangla = truthy(fragility.get(f"{model}_bangla_correct", ""))
            banglish = truthy(fragility.get(f"{model}_banglish_correct", ""))
            english = truthy(fragility.get(f"{model}_english_correct", ""))
            out.append(
                {
                    "id": coverage["id"],
                    "dataset": dataset,
                    "domain": coverage["domain"],
                    "subject": coverage["subject"],
                    "grade": coverage["grade"],
                    "task_type": coverage["task_type"],
                    "quality_status": coverage["quality_status"],
                    "review_label": coverage["review_label"],
                    "content_token_count": to_int(coverage["content_token_count"]),
                    "token_coverage": to_float(coverage["token_coverage"]),
                    "unique_token_coverage": to_float(coverage["unique_token_coverage"]),
                    "frequent_token_coverage": to_float(coverage["frequent_token_coverage"]),
                    "coverage_quartile_all": all_labels[coverage["id"]],
                    "coverage_quartile_dataset": dataset_labels[dataset][coverage["id"]],
                    "model": model,
                    "bangla_correct": bangla,
                    "banglish_correct": banglish,
                    "english_correct": english,
                    "banglish_fragile": (not banglish) and (bangla or english),
                    "strict_bangla_english_fragile": (not banglish) and bangla and english,
                    "all_script_hard": (not bangla) and (not banglish) and (not english),
                }
            )
    return out


def select_rows(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    model: str,
) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["model"] == model]
    if dataset != "all":
        selected = [row for row in selected if row["dataset"] == dataset]
    if section == "coverage_quartile_all":
        selected = [row for row in selected if row["coverage_quartile_all"] == bucket]
    elif section == "coverage_quartile_by_dataset":
        selected = [row for row in selected if row["coverage_quartile_dataset"] == bucket]
    elif section != "dataset_overall":
        raise SystemExit(f"Unknown section: {section}")
    return selected


def interval(
    rows: list[dict[str, Any]], left_key: str, right_key: str, seed_label: str
) -> tuple[float, float, float]:
    pairs = [(bool(row[left_key]), bool(row[right_key])) for row in rows]
    observed, low, high, _p = bootstrap_delta(
        pairs,
        samples=BOOTSTRAPS,
        seed=stable_seed(seed_label),
    )
    return observed, low, high


def summarize_selected(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    model: str,
    detail: str,
) -> dict[str, Any]:
    if not rows:
        raise SystemExit(f"Empty summary bucket: {section} {dataset} {bucket} {model}")
    n = len(rows)
    bangla = sum(int(row["bangla_correct"]) for row in rows)
    banglish = sum(int(row["banglish_correct"]) for row in rows)
    english = sum(int(row["english_correct"]) for row in rows)
    bangla_delta = interval(rows, "bangla_correct", "banglish_correct", f"{section}:{dataset}:{bucket}:{model}:bn")
    english_delta = interval(
        rows, "english_correct", "banglish_correct", f"{section}:{dataset}:{bucket}:{model}:en"
    )
    return {
        "section": section,
        "dataset": dataset,
        "bucket": bucket,
        "model": model,
        "n_items": n,
        "mean_token_coverage": round(sum(float(row["token_coverage"]) for row in rows) / n, 4),
        "mean_unique_token_coverage": round(
            sum(float(row["unique_token_coverage"]) for row in rows) / n, 4
        ),
        "mean_frequent_token_coverage": round(
            sum(float(row["frequent_token_coverage"]) for row in rows) / n, 4
        ),
        "bangla_correct": bangla,
        "banglish_correct": banglish,
        "english_correct": english,
        "bangla_accuracy": rate(bangla, n),
        "banglish_accuracy": rate(banglish, n),
        "english_accuracy": rate(english, n),
        "banglish_minus_bangla": round(bangla_delta[0], 4),
        "banglish_minus_bangla_ci95_low": round(bangla_delta[1], 4),
        "banglish_minus_bangla_ci95_high": round(bangla_delta[2], 4),
        "banglish_minus_english": round(english_delta[0], 4),
        "banglish_minus_english_ci95_low": round(english_delta[1], 4),
        "banglish_minus_english_ci95_high": round(english_delta[2], 4),
        "banglish_fragile_items": sum(int(row["banglish_fragile"]) for row in rows),
        "strict_bangla_english_fragile_items": sum(
            int(row["strict_bangla_english_fragile"]) for row in rows
        ),
        "all_script_hard_items": sum(int(row["all_script_hard"]) for row in rows),
        "detail": detail,
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for dataset in DATASETS:
        for model in MODELS:
            selected = select_rows(item_rows, "dataset_overall", dataset, "all", model)
            summary.append(
                summarize_selected(selected, "dataset_overall", dataset, "all", model, "all rows")
            )
    for bucket in ("q1", "q2", "q3", "q4"):
        for model in MODELS:
            selected = select_rows(item_rows, "coverage_quartile_all", "all", bucket, model)
            summary.append(
                summarize_selected(
                    selected,
                    "coverage_quartile_all",
                    "all",
                    bucket,
                    model,
                    "quartiles over all validation-200 items by exact BanglaTLit token coverage",
                )
            )
    for dataset in ("benqa", "banglamath"):
        for bucket in ("q1", "q2", "q3", "q4"):
            for model in MODELS:
                selected = select_rows(
                    item_rows, "coverage_quartile_by_dataset", dataset, bucket, model
                )
                summary.append(
                    summarize_selected(
                        selected,
                        "coverage_quartile_by_dataset",
                        dataset,
                        bucket,
                        model,
                        f"quartiles within {dataset} by exact BanglaTLit token coverage",
                    )
                )
    return summary


def apply_main_interval_overrides(
    summary_rows: list[dict[str, Any]], interval_rows: list[dict[str, str]]
) -> None:
    intervals = {
        (row["model"], row["dataset"], row["comparison"]): row for row in interval_rows
    }
    for row in summary_rows:
        if row["section"] != "dataset_overall":
            continue
        key_bangla = (row["model"], row["dataset"], "banglish_minus_bangla")
        key_english = (row["model"], row["dataset"], "banglish_minus_english")
        if key_bangla in intervals:
            source = intervals[key_bangla]
            row["banglish_minus_bangla"] = source["delta_right_minus_left"]
            row["banglish_minus_bangla_ci95_low"] = source["ci95_low"]
            row["banglish_minus_bangla_ci95_high"] = source["ci95_high"]
        if key_english in intervals:
            source = intervals[key_english]
            row["banglish_minus_english"] = source["delta_right_minus_left"]
            row["banglish_minus_english_ci95_low"] = source["ci95_low"]
            row["banglish_minus_english_ci95_high"] = source["ci95_high"]


def row_for(
    rows: list[dict[str, Any]], section: str, dataset: str, bucket: str, model: str
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == section
        and row["dataset"] == dataset
        and row["bucket"] == bucket
        and row["model"] == model
    )


def ci_cell(row: dict[str, Any], prefix: str) -> str:
    return (
        f"{points(row[prefix])} pts "
        f"[{points(row[prefix + '_ci95_low'])}, {points(row[prefix + '_ci95_high'])}]"
    )


def add_model_table(
    lines: list[str],
    summary_rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    title: str,
) -> None:
    lines.extend(
        [
            f"### {title}",
            "",
            "| Model | n | Mean coverage | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |",
        ]
    )
    for model in MODELS:
        row = row_for(summary_rows, section, dataset, bucket, model)
        lines.append(
            f"| {model} | {row['n_items']} | {pct(row['mean_token_coverage'])}% | "
            f"{row['bangla_correct']}/{row['n_items']} | "
            f"{row['banglish_correct']}/{row['n_items']} | "
            f"{row['english_correct']}/{row['n_items']} | "
            f"{ci_cell(row, 'banglish_minus_bangla')} | "
            f"{ci_cell(row, 'banglish_minus_english')} | "
            f"{row['banglish_fragile_items']} |"
        )
    lines.append("")


def add_quartile_direction_table(
    lines: list[str], summary_rows: list[dict[str, Any]]
) -> None:
    lines.extend(
        [
            "## All-200 Quartile Direction Check",
            "",
            "| Coverage bucket | Model | n | Bangla | Banglish | English | Direction |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for bucket in ("q1", "q2", "q3", "q4"):
        for model in MODELS:
            row = row_for(summary_rows, "coverage_quartile_all", "all", bucket, model)
            direction = (
                "below Bangla and English"
                if int(row["banglish_correct"]) < int(row["bangla_correct"])
                and int(row["banglish_correct"]) < int(row["english_correct"])
                else "mixed"
            )
            lines.append(
                f"| `{bucket}` | {model} | {row['n_items']} | "
                f"{row['bangla_correct']} | {row['banglish_correct']} | "
                f"{row['english_correct']} | {direction} |"
            )
    lines.append("")


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    coverage_items: Path,
    fragility_items: Path,
    interval_path: Path,
    items_output: Path,
    summary_output: Path,
) -> None:
    q4_rows = [
        row_for(summary_rows, "coverage_quartile_all", "all", "q4", model) for model in MODELS
    ]
    all_q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in q4_rows
    )
    all_quartile_direction_ok = all(
        int(row_for(summary_rows, "coverage_quartile_all", "all", bucket, model)["banglish_correct"])
        < int(row_for(summary_rows, "coverage_quartile_all", "all", bucket, model)["bangla_correct"])
        and int(row_for(summary_rows, "coverage_quartile_all", "all", bucket, model)["banglish_correct"])
        < int(row_for(summary_rows, "coverage_quartile_all", "all", bucket, model)["english_correct"])
        for bucket in ("q1", "q2", "q3", "q4")
        for model in MODELS
    )
    lines = [
        "# V5 BanglaTLit Model-Coverage Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Inputs And Outputs",
        "",
        f"- Lexical coverage items: `{repo_path(coverage_items)}`",
        f"- Fragility/correctness items: `{repo_path(fragility_items)}`",
        f"- Main dataset intervals for all-item rows: `{repo_path(interval_path)}`",
        f"- Per-model item output: `{repo_path(items_output)}`",
        f"- Per-model summary output: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        "- This audit expands the BanglaTLit lexical-coverage result from a",
        "  Qwen-family aggregate to separate rows for Qwen2.5-3B, Qwen2.5-7B,",
        "  and Qwen3-4B.",
        (
            "- In the highest-coverage all-200 quartile, reviewed Banglish remains "
            "below both Bangla and English for every thesis-facing Qwen row."
            if all_q4_direction_ok
            else "- The highest-coverage all-200 quartile has a mixed per-model direction."
        ),
        (
            "- The same below-Bangla-and-English direction holds in every all-200 "
            "coverage quartile for every thesis-facing Qwen row."
            if all_quartile_direction_ok
            else "- Some all-200 coverage quartiles have mixed per-model direction."
        ),
        "- This weakens a model-specific explanation that only rare or low-coverage",
        "  Banglish vocabulary drives the frozen-v5 gap.",
        "",
    ]
    add_model_table(
        lines,
        summary_rows,
        "dataset_overall",
        "all",
        "all",
        "All Frozen-V5 Items",
    )
    add_model_table(
        lines,
        summary_rows,
        "coverage_quartile_all",
        "all",
        "q4",
        "Highest-Coverage All-200 Quartile",
    )
    add_model_table(
        lines,
        summary_rows,
        "coverage_quartile_by_dataset",
        "benqa",
        "q4",
        "Highest-Coverage BEnQA Quartile",
    )
    add_quartile_direction_table(lines, summary_rows)
    lines.extend(
        [
            "## Interpretation",
            "",
            "The existing lexical-coverage audit already shows that frozen-v5 Banglish",
            "is not a natural-chat benchmark. This per-model sensitivity adds a",
            "narrower robustness check: even among items whose content tokens overlap",
            "most with BanglaTLit, each thesis-facing Qwen row still performs worse",
            "on reviewed Banglish than on Bangla or English. Coverage buckets are",
            "descriptive; they should not be presented as a causal lexical mechanism.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_banglatlit_model_coverage_sensitivity.py`",
            f"- Per-model item rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "- Quartiles reuse exact-token BanglaTLit coverage from",
            "  `reports/v5_banglatlit_lexical_coverage.md`.",
            "- Bootstrap: paired item resampling within each model/bucket, 5,000 samples.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-items", type=Path, default=DEFAULT_COVERAGE_ITEMS)
    parser.add_argument("--fragility-items", type=Path, default=DEFAULT_FRAGILITY_ITEMS)
    parser.add_argument("--dataset-intervals", type=Path, default=DEFAULT_DATASET_INTERVALS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coverage_rows = read_csv(args.coverage_items)
    fragility_rows = read_csv(args.fragility_items)
    item_rows = build_item_rows(coverage_rows, fragility_rows)
    summary_rows = build_summary_rows(item_rows)
    apply_main_interval_overrides(summary_rows, read_csv(args.dataset_intervals))
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        item_rows,
        summary_rows,
        args.coverage_items,
        args.fragility_items,
        args.dataset_intervals,
        args.items_output,
        args.summary_output,
    )
    q4_rows = [
        row_for(summary_rows, "coverage_quartile_all", "all", "q4", model) for model in MODELS
    ]
    q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in q4_rows
    )
    print(
        " | ".join(
            [
                f"items={len(item_rows)}",
                f"summary_rows={len(summary_rows)}",
                f"all_q4_direction_ok={q4_direction_ok}",
                f"report={args.report_output}",
            ]
        )
    )


if __name__ == "__main__":
    main()
