#!/usr/bin/env python3
"""Leave-one-model-out stability for frozen-v5 item consensus."""

from __future__ import annotations

import argparse
import csv
import itertools
import random
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_consensus_stability_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_consensus_stability_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_consensus_stability.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
SCRIPTS = ("bangla", "banglish", "english")
SCRIPT_LABELS = {
    "bangla": "Bangla",
    "banglish": "Reviewed Banglish",
    "english": "English",
}
DATASETS = ("all", "benqa", "banglamath")
BOOTSTRAP_ITERATIONS = 5000
BOOTSTRAP_SEED = 20260531


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


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def points(value: float) -> str:
    value *= 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def model_subsets() -> list[tuple[str, ...]]:
    subsets: list[tuple[str, ...]] = []
    for size in range(1, len(MODELS) + 1):
        subsets.extend(itertools.combinations(MODELS, size))
    return subsets


def subset_label(models: tuple[str, ...]) -> str:
    return " + ".join(models)


def stable_seed(label: str) -> int:
    return BOOTSTRAP_SEED + sum((index + 1) * ord(char) for index, char in enumerate(label))


def count_correct(row: dict[str, str], models: tuple[str, ...], script: str) -> int:
    return sum(truthy(row.get(f"{model}_{script}_correct", "")) for model in models)


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for models in model_subsets():
        label = subset_label(models)
        for row in rows:
            counts = {script: count_correct(row, models, script) for script in SCRIPTS}
            alternate_best = max(counts["bangla"], counts["english"])
            strong_alternate_threshold = 1 if len(models) == 1 else len(models)
            low_banglish_threshold = 0 if len(models) == 1 else len(models) - 1
            out.append(
                {
                    "model_subset": label,
                    "subset_size": len(models),
                    "id": row["id"],
                    "dataset": row["dataset"],
                    "domain": row.get("domain", ""),
                    "subject": row.get("subject", ""),
                    "task_type": row.get("task_type", ""),
                    "review_label": row.get("review_label", ""),
                    "bangla_correct": counts["bangla"],
                    "banglish_correct": counts["banglish"],
                    "english_correct": counts["english"],
                    "banglish_minus_bangla": counts["banglish"] - counts["bangla"],
                    "banglish_minus_english": counts["banglish"] - counts["english"],
                    "alternate_best_correct": alternate_best,
                    "strong_alternate_low_banglish": alternate_best >= strong_alternate_threshold
                    and counts["banglish"] <= low_banglish_threshold,
                    "zero_banglish_any_alternate": counts["banglish"] == 0
                    and alternate_best >= 1,
                    "banglish_beats_alternate": counts["banglish"] > alternate_best,
                }
            )
    return out


def bootstrap_delta(
    rows: list[dict[str, Any]],
    candidate_key: str,
    baseline_key: str,
    denominator: int,
    seed_label: str,
) -> tuple[float, float, float]:
    observed = sum(int(row[candidate_key]) - int(row[baseline_key]) for row in rows) / denominator
    rng = random.Random(stable_seed(seed_label))
    draws: list[float] = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        total = 0
        for _i in range(len(rows)):
            row = rng.choice(rows)
            total += int(row[candidate_key]) - int(row[baseline_key])
        draws.append(total / denominator)
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    return observed, low, high


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for models in model_subsets():
        label = subset_label(models)
        subset_rows = [row for row in item_rows if row["model_subset"] == label]
        for dataset in DATASETS:
            rows = [
                row for row in subset_rows if dataset == "all" or row["dataset"] == dataset
            ]
            n_items = len(rows)
            denominator = n_items * len(models)
            if n_items == 0:
                continue
            totals = {
                script: sum(int(row[f"{script}_correct"]) for row in rows)
                for script in SCRIPTS
            }
            delta_bangla = bootstrap_delta(
                rows,
                "banglish_correct",
                "bangla_correct",
                denominator,
                f"{label}:{dataset}:bangla",
            )
            delta_english = bootstrap_delta(
                rows,
                "banglish_correct",
                "english_correct",
                denominator,
                f"{label}:{dataset}:english",
            )
            summary.append(
                {
                    "model_subset": label,
                    "subset_size": len(models),
                    "dataset": dataset,
                    "n_items": n_items,
                    "model_item_slots": denominator,
                    "bangla_correct": totals["bangla"],
                    "banglish_correct": totals["banglish"],
                    "english_correct": totals["english"],
                    "bangla_accuracy": round(totals["bangla"] / denominator, 4),
                    "banglish_accuracy": round(totals["banglish"] / denominator, 4),
                    "english_accuracy": round(totals["english"] / denominator, 4),
                    "banglish_minus_bangla": round(delta_bangla[0], 4),
                    "banglish_minus_bangla_ci95_low": round(delta_bangla[1], 4),
                    "banglish_minus_bangla_ci95_high": round(delta_bangla[2], 4),
                    "banglish_minus_english": round(delta_english[0], 4),
                    "banglish_minus_english_ci95_low": round(delta_english[1], 4),
                    "banglish_minus_english_ci95_high": round(delta_english[2], 4),
                    "strong_alternate_low_banglish_items": sum(
                        bool(row["strong_alternate_low_banglish"]) for row in rows
                    ),
                    "zero_banglish_any_alternate_items": sum(
                        bool(row["zero_banglish_any_alternate"]) for row in rows
                    ),
                    "banglish_beats_alternate_items": sum(
                        bool(row["banglish_beats_alternate"]) for row in rows
                    ),
                }
            )
    return summary


def row_for(rows: list[dict[str, Any]], subset: str, dataset: str) -> dict[str, Any]:
    return next(
        row for row in rows if row["model_subset"] == subset and row["dataset"] == dataset
    )


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    pair_rows = [
        row for row in summary_rows if row["subset_size"] == 2 and row["dataset"] == "all"
    ]
    benqa_pair_rows = [
        row for row in summary_rows if row["subset_size"] == 2 and row["dataset"] == "benqa"
    ]
    all_row = row_for(summary_rows, subset_label(MODELS), "all")
    all_pairs_negative = all(
        float(row["banglish_minus_bangla"]) < 0 and float(row["banglish_minus_english"]) < 0
        for row in pair_rows
    )
    benqa_pairs_negative = all(
        float(row["banglish_minus_bangla"]) < 0 and float(row["banglish_minus_english"]) < 0
        for row in benqa_pair_rows
    )
    lines = [
        "# Frozen-V5 Consensus Stability Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit stress-tests the item-consensus result by recomputing",
        "model-item accuracy for every non-empty subset of the three",
        "thesis-facing Qwen rows. The two-model rows are the leave-one-model-out",
        "test: if every pair still shows a reviewed-Banglish deficit, the",
        "consensus result is not carried by one model.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "Bootstrap intervals resample validation items as paired clusters within",
        "each model subset.",
        "",
        "## Leave-One-Model-Out Result",
        "",
        "| Model subset | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in pair_rows:
        denominator = int(row["model_item_slots"])
        lines.append(
            f"| {row['model_subset']} | "
            f"{row['bangla_correct']}/{denominator} ({percent(int(row['bangla_correct']), denominator)}) | "
            f"{row['banglish_correct']}/{denominator} ({percent(int(row['banglish_correct']), denominator)}) | "
            f"{row['english_correct']}/{denominator} ({percent(int(row['english_correct']), denominator)}) | "
            f"{points(float(row['banglish_minus_bangla']))} pts "
            f"[{points(float(row['banglish_minus_bangla_ci95_low']))}, "
            f"{points(float(row['banglish_minus_bangla_ci95_high']))}] | "
            f"{points(float(row['banglish_minus_english']))} pts "
            f"[{points(float(row['banglish_minus_english_ci95_low']))}, "
            f"{points(float(row['banglish_minus_english_ci95_high']))}] |"
        )

    lines.extend(
        [
            "",
            "## Dataset Stress Test",
            "",
            "| Dataset | Two-model subsets negative vs Bangla and English | Strong alternate, low Banglish range | Banglish beats alternate range |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    for dataset in DATASETS:
        rows = [
            row
            for row in summary_rows
            if row["subset_size"] == 2 and row["dataset"] == dataset
        ]
        negative = all(
            float(row["banglish_minus_bangla"]) < 0
            and float(row["banglish_minus_english"]) < 0
            for row in rows
        )
        pressure_values = [int(row["strong_alternate_low_banglish_items"]) for row in rows]
        win_values = [int(row["banglish_beats_alternate_items"]) for row in rows]
        lines.append(
            f"| {dataset} | {'yes' if negative else 'no'} | "
            f"{min(pressure_values)}-{max(pressure_values)} | "
            f"{min(win_values)}-{max(win_values)} |"
        )

    denominator = int(all_row["model_item_slots"])
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- The all-model consensus result is {all_row['banglish_correct']}/{denominator}",
            f"  reviewed-Banglish successes versus {all_row['bangla_correct']}/{denominator}",
            f"  Bangla and {all_row['english_correct']}/{denominator} English.",
            "- All three leave-one-model-out pairs keep reviewed Banglish below both",
            f"  Bangla and English on the all-200 slice: {'yes' if all_pairs_negative else 'no'}.",
            "- The same pairwise negative ordering holds on BEnQA, the clearest",
            f"  competent dataset slice: {'yes' if benqa_pairs_negative else 'no'}.",
            "- BanglaMATH pair rows are also negative, but the absolute accuracy is",
            "  low across scripts; keep BanglaMATH framed as a hard stress test.",
            "- This is still Qwen-family stability, not independent family",
            "  replication. Use it to answer the narrower criticism that the",
            "  consensus audit is driven by one Qwen row.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_consensus_stability.py`",
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
    if len(rows) != 200:
        raise SystemExit(f"Expected 200 frozen-v5 item rows, got {len(rows)}")
    item_rows = build_item_rows(rows)
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows, list(item_rows[0]))
    write_csv(args.summary_output, summary_rows, list(summary_rows[0]))
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
