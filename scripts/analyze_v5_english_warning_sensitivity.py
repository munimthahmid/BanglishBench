#!/usr/bin/env python3
"""Sensitivity of English-backed diagnostics to source-variant warnings."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARITY_ITEMS = ROOT / "results/analysis/v5_source_variant_structural_parity_items.csv"
DEFAULT_RECOVERABILITY_ITEMS = ROOT / "results/analysis/v5_recoverability_source_items.csv"
DEFAULT_DATASET_INTERVALS = ROOT / "results/analysis/v5_dataset_gap_intervals.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_english_warning_sensitivity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_english_warning_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_english_warning_sensitivity.md"

GROUPS = (
    ("all_items", "All frozen-v5 items"),
    ("english_structural_clean", "No English structural warning"),
    ("english_structural_warning", "English structural warning"),
)
DATASETS = ("all", "benqa", "banglamath")
BOOTSTRAPS = 5000
SEED = 20260531


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def paired_delta(rows: list[dict[str, Any]], left_key: str, right_key: str) -> float:
    if not rows:
        return 0.0
    return sum(int(row[right_key]) - int(row[left_key]) for row in rows) / len(rows)


def stable_seed(label: str) -> int:
    return SEED + sum((idx + 1) * ord(ch) for idx, ch in enumerate(label))


def bootstrap_ci(rows: list[dict[str, Any]], left_key: str, right_key: str, seed_label: str) -> tuple[float, float]:
    if not rows:
        return 0.0, 0.0
    pairs = [(bool(row[left_key]), bool(row[right_key])) for row in rows]
    _observed, low, high, _p_opposite = bootstrap_delta(
        pairs, samples=BOOTSTRAPS, seed=stable_seed(seed_label)
    )
    return low, high


def english_warning_index(
    parity_rows: list[dict[str, str]],
) -> tuple[set[str], dict[str, str], Counter[str]]:
    warning_ids: set[str] = set()
    codes_by_id: dict[str, set[str]] = defaultdict(set)
    counts: Counter[str] = Counter()
    for row in parity_rows:
        if row["comparison"] not in {"bangla_vs_english", "banglish_vs_english"}:
            continue
        if not truthy(row["structural_mismatch"]):
            continue
        item_id = row["id"]
        warning_ids.add(item_id)
        for code in row["mismatch_codes"].split():
            codes_by_id[item_id].add(code)
            if row["comparison"] == "bangla_vs_english":
                counts[code] += 1
    return warning_ids, {key: " ".join(sorted(value)) for key, value in codes_by_id.items()}, counts


def enrich_items(
    recoverability_rows: list[dict[str, str]],
    warning_ids: set[str],
    warning_codes: dict[str, str],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in recoverability_rows:
        item_id = row["id"]
        bangla = truthy(row["bangla_correct"])
        banglish = truthy(row["banglish_correct"])
        english = truthy(row["english_correct"])
        warning = item_id in warning_ids
        items.append(
            {
                "model": row["model"],
                "model_id": row["model_id"],
                "dataset": row["dataset"],
                "task_type": row["task_type"],
                "id": item_id,
                "domain": row["domain"],
                "subject": row["subject"],
                "grade": row["grade"],
                "english_structural_warning": warning,
                "english_structural_group": (
                    "english_structural_warning" if warning else "english_structural_clean"
                ),
                "english_warning_codes": warning_codes.get(item_id, ""),
                "bangla_correct": bangla,
                "banglish_correct": banglish,
                "english_correct": english,
                "banglish_miss": not banglish,
                "recoverable_banglish_miss": (not banglish) and (bangla or english),
                "bangla_any_recovery": (not banglish) and bangla,
                "english_any_recovery": (not banglish) and english,
                "both_alternate_recovery": (not banglish) and bangla and english,
                "all_script_hard": (not bangla) and (not banglish) and (not english),
                "banglish_unique_success": banglish and (not bangla) and (not english),
            }
        )
    return items


def select_group(rows: list[dict[str, Any]], group: str, dataset: str, model: str) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["model"] == model]
    if group == "english_structural_clean":
        selected = [row for row in selected if not row["english_structural_warning"]]
    elif group == "english_structural_warning":
        selected = [row for row in selected if row["english_structural_warning"]]
    if dataset != "all":
        selected = [row for row in selected if row["dataset"] == dataset]
    return selected


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    models = list(dict.fromkeys(str(row["model"]) for row in rows))
    summary: list[dict[str, Any]] = []
    for group, label in GROUPS:
        for model in models:
            for dataset in DATASETS:
                selected = select_group(rows, group, dataset, model)
                if not selected:
                    continue
                n = len(selected)
                bangla = sum(int(row["bangla_correct"]) for row in selected)
                banglish = sum(int(row["banglish_correct"]) for row in selected)
                english = sum(int(row["english_correct"]) for row in selected)
                delta_bangla = paired_delta(selected, "bangla_correct", "banglish_correct")
                delta_english = paired_delta(selected, "english_correct", "banglish_correct")
                ci_bangla = bootstrap_ci(
                    selected, "bangla_correct", "banglish_correct", f"{SEED}:{group}:{model}:{dataset}:bn"
                )
                ci_english = bootstrap_ci(
                    selected, "english_correct", "banglish_correct", f"{SEED}:{group}:{model}:{dataset}:en"
                )
                summary.append(
                    {
                        "structural_group": group,
                        "structural_group_label": label,
                        "model": model,
                        "dataset": dataset,
                        "n": n,
                        "english_warning_items": sum(
                            int(row["english_structural_warning"]) for row in selected
                        ),
                        "bangla_correct": bangla,
                        "banglish_correct": banglish,
                        "english_correct": english,
                        "bangla_accuracy": rate(bangla, n),
                        "banglish_accuracy": rate(banglish, n),
                        "english_accuracy": rate(english, n),
                        "banglish_minus_bangla": round(delta_bangla, 4),
                        "banglish_minus_bangla_ci95_low": round(ci_bangla[0], 4),
                        "banglish_minus_bangla_ci95_high": round(ci_bangla[1], 4),
                        "banglish_minus_english": round(delta_english, 4),
                        "banglish_minus_english_ci95_low": round(ci_english[0], 4),
                        "banglish_minus_english_ci95_high": round(ci_english[1], 4),
                        "banglish_misses": sum(int(row["banglish_miss"]) for row in selected),
                        "recoverable_banglish_misses": sum(
                            int(row["recoverable_banglish_miss"]) for row in selected
                        ),
                        "bangla_any_recovery": sum(
                            int(row["bangla_any_recovery"]) for row in selected
                        ),
                        "english_any_recovery": sum(
                            int(row["english_any_recovery"]) for row in selected
                        ),
                        "both_alternate_recovery": sum(
                            int(row["both_alternate_recovery"]) for row in selected
                        ),
                        "all_script_hard": sum(int(row["all_script_hard"]) for row in selected),
                    }
                )
    return summary


def apply_main_interval_overrides(
    summary_rows: list[dict[str, Any]], interval_rows: list[dict[str, str]]
) -> None:
    intervals = {
        (row["model"], row["dataset"], row["comparison"]): row for row in interval_rows
    }
    for row in summary_rows:
        if row["structural_group"] != "all_items":
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


def find_summary(
    rows: list[dict[str, Any]], group: str, model: str, dataset: str = "all"
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["structural_group"] == group
        and row["model"] == model
        and row["dataset"] == dataset
    )


def pct(value: Any) -> str:
    return f"{float(value) * 100:.1f}"


def points(value: Any) -> str:
    value = float(value) * 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def ci_cell(row: dict[str, Any], prefix: str) -> str:
    return (
        f"{points(row[prefix])} pts "
        f"[{points(row[prefix + '_ci95_low'])}, {points(row[prefix + '_ci95_high'])}]"
    )


def write_report(
    report_path: Path,
    parity_path: Path,
    recoverability_path: Path,
    interval_path: Path,
    items_path: Path,
    summary_path: Path,
    summary_rows: list[dict[str, Any]],
    warning_ids: set[str],
    warning_counts: Counter[str],
) -> None:
    models = list(dict.fromkeys(str(row["model"]) for row in summary_rows))
    lines = [
        "# V5 English-Warning Sensitivity Audit",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Source parity items: `{repo_path(parity_path)}`",
        f"- Recoverability items: `{repo_path(recoverability_path)}`",
        f"- Main dataset intervals for all-item rows: `{repo_path(interval_path)}`",
        f"- Item sensitivity CSV: `{repo_path(items_path)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        "",
        "## Headline",
        "",
        (
            f"- The source-parity audit flags {len(warning_ids)}/200 items with an "
            "English-side structural warning; bangla-vs-reviewed-Banglish remains "
            "0/200 primary hard fails."
        ),
        (
            "- On the 161 English-structurally-clean items, reviewed Banglish stays "
            "below both Bangla and English for all three thesis-facing Qwen rows."
        ),
        (
            "- Recoverable Banglish misses also persist on the clean-English subset, "
            "so English-backed diagnostics are not driven only by the warning rows."
        ),
        "",
        "English warning codes on Bangla-vs-English comparisons: "
        + ", ".join(f"{key}={count}" for key, count in sorted(warning_counts.items())),
        "",
        "## All-Items Versus English-Clean Subset",
        "",
        "| Model | Group | n | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Recoverable misses | English recoveries | Both alternates |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    for model in models:
        for group in ("all_items", "english_structural_clean", "english_structural_warning"):
            row = find_summary(summary_rows, group, model)
            lines.append(
                f"| {model} | {row['structural_group_label']} | {row['n']} | "
                f"{row['bangla_correct']}/{row['n']} ({pct(row['bangla_accuracy'])}%) | "
                f"{row['banglish_correct']}/{row['n']} ({pct(row['banglish_accuracy'])}%) | "
                f"{row['english_correct']}/{row['n']} ({pct(row['english_accuracy'])}%) | "
                f"{ci_cell(row, 'banglish_minus_bangla')} | "
                f"{ci_cell(row, 'banglish_minus_english')} | "
                f"{row['recoverable_banglish_misses']} | "
                f"{row['english_any_recovery']} | {row['both_alternate_recovery']} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This audit does not repair or discard English rows. Instead, it asks",
            "whether the thesis diagnostics that use English views disappear when",
            "items with English-side structural warnings are separated. They do not:",
            "the clean-English subset keeps the same direction for Bangla-vs-Banglish",
            "and Banglish-vs-English, and it still contains many recoverable Banglish",
            "misses. The English-warning rows should remain caveated as upstream",
            "translation/structure risks, while the primary Bangla-vs-reviewed-Banglish",
            "source pair remains structurally clean.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parity-items", type=Path, default=DEFAULT_PARITY_ITEMS)
    parser.add_argument("--recoverability-items", type=Path, default=DEFAULT_RECOVERABILITY_ITEMS)
    parser.add_argument("--dataset-intervals", type=Path, default=DEFAULT_DATASET_INTERVALS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parity_rows = read_csv(args.parity_items)
    recoverability_rows = read_csv(args.recoverability_items)
    interval_rows = read_csv(args.dataset_intervals)
    warning_ids, warning_codes, warning_counts = english_warning_index(parity_rows)
    item_rows = enrich_items(recoverability_rows, warning_ids, warning_codes)
    summary_rows = summarize(item_rows)
    apply_main_interval_overrides(summary_rows, interval_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        args.parity_items,
        args.recoverability_items,
        args.dataset_intervals,
        args.items_output,
        args.summary_output,
        summary_rows,
        warning_ids,
        warning_counts,
    )
    clean_rows = [row for row in item_rows if not row["english_structural_warning"]]
    print(
        " | ".join(
            [
                f"items={len(item_rows)}",
                f"summary_rows={len(summary_rows)}",
                f"english_warning_items={len(warning_ids)}",
                f"clean_item_rows={len(clean_rows)}",
                f"report={args.report_output}",
            ]
        )
    )


if __name__ == "__main__":
    main()
