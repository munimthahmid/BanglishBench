#!/usr/bin/env python3
"""Analyze frozen-v5 item-level consensus across thesis-facing Qwen rows."""

from __future__ import annotations

import argparse
import csv
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_item_consensus_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_item_consensus_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_item_consensus.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
SCRIPTS = ("bangla", "banglish", "english")
SCRIPT_LABELS = {
    "bangla": "Bangla",
    "banglish": "Reviewed Banglish",
    "english": "English",
}
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


def points(rate: float) -> str:
    value = rate * 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def percent(count: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * count / denominator:.1f}%"


def group_by(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row[key])].append(row)
    return dict(grouped)


def count_script_correct(row: dict[str, str], script: str) -> int:
    return sum(truthy(row.get(f"{model}_{script}_correct", "")) for model in MODELS)


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        counts = {script: count_script_correct(row, script) for script in SCRIPTS}
        alternate_best = max(counts["bangla"], counts["english"])
        alternate_total = counts["bangla"] + counts["english"]
        consensus_row: dict[str, Any] = {
            "id": row["id"],
            "dataset": row["dataset"],
            "domain": row.get("domain", ""),
            "subject": row.get("subject", ""),
            "grade": row.get("grade", ""),
            "task_type": row.get("task_type", ""),
            "review_label": row.get("review_label", ""),
            "bangla_model_correct_count": counts["bangla"],
            "banglish_model_correct_count": counts["banglish"],
            "english_model_correct_count": counts["english"],
            "alternate_best_correct_count": alternate_best,
            "alternate_total_correct_count": alternate_total,
            "banglish_minus_bangla_model_count": counts["banglish"] - counts["bangla"],
            "banglish_minus_english_model_count": counts["banglish"] - counts["english"],
            "banglish_minus_alternate_best": counts["banglish"] - alternate_best,
            "strong_alternate_low_banglish": alternate_best >= 2 and counts["banglish"] <= 1,
            "zero_banglish_any_alternate": counts["banglish"] == 0 and alternate_best >= 1,
            "zero_banglish_strong_alternate": counts["banglish"] == 0 and alternate_best >= 2,
            "banglish_beats_alternate": counts["banglish"] > alternate_best,
            "banglish_ties_best_script": counts["banglish"]
            == max(counts["bangla"], counts["banglish"], counts["english"]),
            "all_scripts_zero": max(counts.values()) == 0,
            "all_three_banglish_correct": counts["banglish"] == len(MODELS),
            "fragility_events": row.get("banglish_fragility_events", ""),
            "strict_fragility_events": row.get("strict_bangla_english_fragility_events", ""),
            "banglish_preview": row.get("banglish_preview", ""),
        }
        out.append(consensus_row)
    return out


def add_summary(
    rows: list[dict[str, Any]],
    section: str,
    key: str,
    dataset: str,
    n: int,
    denominator: int,
    detail: str = "",
    ci95_low: float | str = "",
    ci95_high: float | str = "",
) -> None:
    rows.append(
        {
            "section": section,
            "key": key,
            "dataset": dataset,
            "n": n,
            "denominator": denominator,
            "rate": round(n / denominator, 4) if denominator else 0.0,
            "ci95_low": ci95_low,
            "ci95_high": ci95_high,
            "detail": detail,
        }
    )


def bootstrap_delta(
    rows: list[dict[str, Any]],
    candidate_key: str,
    baseline_key: str,
    seed_offset: int,
    iterations: int = BOOTSTRAP_ITERATIONS,
) -> tuple[float, float, float]:
    denominator = len(rows) * len(MODELS)
    observed = sum(int(row[candidate_key]) - int(row[baseline_key]) for row in rows) / denominator
    rng = random.Random(BOOTSTRAP_SEED + seed_offset)
    draws: list[float] = []
    for _ in range(iterations):
        total = 0
        for _i in range(len(rows)):
            row = rng.choice(rows)
            total += int(row[candidate_key]) - int(row[baseline_key])
        draws.append(total / denominator)
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    return observed, low, high


def add_group_summaries(
    summary: list[dict[str, Any]],
    dataset: str,
    rows: list[dict[str, Any]],
    seed_offset: int,
) -> None:
    item_count = len(rows)
    model_item_denominator = item_count * len(MODELS)
    for script in SCRIPTS:
        key = f"{script}_model_correct_count"
        total = sum(int(row[key]) for row in rows)
        add_summary(
            summary,
            "model_item_success",
            script,
            dataset,
            total,
            model_item_denominator,
            f"{SCRIPT_LABELS[script]} correct model-item slots",
        )

    for index, (candidate, baseline) in enumerate(
        (("banglish", "bangla"), ("banglish", "english")),
        start=1,
    ):
        observed, low, high = bootstrap_delta(
            rows,
            f"{candidate}_model_correct_count",
            f"{baseline}_model_correct_count",
            seed_offset + index,
        )
        add_summary(
            summary,
            "paired_delta",
            f"{candidate}_minus_{baseline}",
            dataset,
            round(observed * model_item_denominator),
            model_item_denominator,
            "item-cluster bootstrap over validation items",
            round(low, 4),
            round(high, 4),
        )

    for script in SCRIPTS:
        counts = Counter(int(row[f"{script}_model_correct_count"]) for row in rows)
        for correct_count in range(len(MODELS) + 1):
            add_summary(
                summary,
                "consensus_distribution",
                f"{script}:{correct_count}_models_correct",
                dataset,
                counts[correct_count],
                item_count,
            )

    recoverability_checks = [
        ("all_scripts_zero", "all scripts have zero correct models"),
        ("zero_banglish_any_alternate", "Banglish zero, Bangla or English has at least one correct model"),
        ("zero_banglish_strong_alternate", "Banglish zero, Bangla or English has at least two correct models"),
        ("strong_alternate_low_banglish", "Bangla or English has at least two correct models; Banglish has at most one"),
        ("banglish_beats_alternate", "Banglish has more correct models than both Bangla and English"),
        ("banglish_ties_best_script", "Banglish ties the best script-level consensus count"),
    ]
    for key, detail in recoverability_checks:
        add_summary(
            summary,
            "recoverability",
            key,
            dataset,
            sum(bool(row[key]) for row in rows),
            item_count,
            detail,
        )

    for review_label, label_rows in sorted(group_by(rows, "review_label").items()):
        add_summary(
            summary,
            "review_label_recoverability",
            "strong_alternate_low_banglish",
            f"{dataset}:{review_label}",
            sum(bool(row["strong_alternate_low_banglish"]) for row in label_rows),
            len(label_rows),
            "within review label",
        )


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    add_group_summaries(summary, "all", item_rows, 0)
    for index, (dataset, rows) in enumerate(sorted(group_by(item_rows, "dataset").items()), start=10):
        add_group_summaries(summary, dataset, rows, index * 10)
    return summary


def find_summary(
    rows: list[dict[str, Any]],
    section: str,
    key: str,
    dataset: str,
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == section and row["key"] == key and row["dataset"] == dataset
    )


def count_for(
    rows: list[dict[str, Any]],
    section: str,
    key: str,
    dataset: str,
) -> int:
    return int(find_summary(rows, section, key, dataset)["n"])


def rate_for(
    rows: list[dict[str, Any]],
    section: str,
    key: str,
    dataset: str,
) -> float:
    return float(find_summary(rows, section, key, dataset)["rate"])


def delta_for(rows: list[dict[str, Any]], key: str, dataset: str) -> dict[str, Any]:
    return find_summary(rows, "paired_delta", key, dataset)


def format_count_rate(row: dict[str, Any]) -> str:
    return f"{row['n']}/{row['denominator']} ({percent(int(row['n']), int(row['denominator']))})"


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    lines = [
        "# Frozen-V5 Item Consensus Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit treats each validation item as a paired unit and",
        "counts how many of the three thesis-facing Qwen rows answer each script",
        "view correctly. It asks whether reviewed Banglish failures persist even",
        "when Bangla or English has cross-model support on the same item.",
        "",
        f"- Item-level table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "Bootstrap intervals below resample validation items, keeping the three",
        "model outcomes for an item together. They are descriptive robustness",
        "intervals for cross-model consensus, not a new independent model family.",
        "",
        "## Cross-Model Script Totals",
        "",
        "| Dataset | Bangla model-item successes | Reviewed Banglish | English | Banglish-Bangla delta | Banglish-English delta |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for dataset in ("all", "benqa", "banglamath"):
        bangla = find_summary(summary_rows, "model_item_success", "bangla", dataset)
        banglish = find_summary(summary_rows, "model_item_success", "banglish", dataset)
        english = find_summary(summary_rows, "model_item_success", "english", dataset)
        delta_bangla = delta_for(summary_rows, "banglish_minus_bangla", dataset)
        delta_english = delta_for(summary_rows, "banglish_minus_english", dataset)
        lines.append(
            f"| {dataset} | {format_count_rate(bangla)} | "
            f"{format_count_rate(banglish)} | {format_count_rate(english)} | "
            f"{points(float(delta_bangla['rate']))} pts "
            f"[{points(float(delta_bangla['ci95_low']))}, {points(float(delta_bangla['ci95_high']))}] | "
            f"{points(float(delta_english['rate']))} pts "
            f"[{points(float(delta_english['ci95_low']))}, {points(float(delta_english['ci95_high']))}] |"
        )

    lines.extend(
        [
            "",
            "## Consensus Distribution",
            "",
            "| Script | 0 models correct | 1 model | 2 models | 3 models |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for script in SCRIPTS:
        values = [
            count_for(summary_rows, "consensus_distribution", f"{script}:{count}_models_correct", "all")
            for count in range(len(MODELS) + 1)
        ]
        lines.append(
            f"| {SCRIPT_LABELS[script]} | {values[0]} | {values[1]} | {values[2]} | {values[3]} |"
        )

    lines.extend(
        [
            "",
            "## Recoverability Pressure",
            "",
            "| Dataset | All-script hard | Banglish zero, alternate works | Banglish zero, strong alternate | Strong alternate, <=1 Banglish model | Banglish beats alternates |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for dataset in ("all", "benqa", "banglamath"):
        denominator = len(item_rows) if dataset == "all" else sum(
            1 for row in item_rows if row["dataset"] == dataset
        )
        values = [
            count_for(summary_rows, "recoverability", "all_scripts_zero", dataset),
            count_for(summary_rows, "recoverability", "zero_banglish_any_alternate", dataset),
            count_for(summary_rows, "recoverability", "zero_banglish_strong_alternate", dataset),
            count_for(summary_rows, "recoverability", "strong_alternate_low_banglish", dataset),
            count_for(summary_rows, "recoverability", "banglish_beats_alternate", dataset),
        ]
        lines.append(
            f"| {dataset} | "
            + " | ".join(f"{value}/{denominator}" for value in values)
            + " |"
        )

    all_delta_bangla = delta_for(summary_rows, "banglish_minus_bangla", "all")
    all_delta_english = delta_for(summary_rows, "banglish_minus_english", "all")
    benqa_pressure = count_for(
        summary_rows,
        "recoverability",
        "strong_alternate_low_banglish",
        "benqa",
    )
    benqa_hard = count_for(summary_rows, "recoverability", "all_scripts_zero", "benqa")
    banglamath_hard = count_for(summary_rows, "recoverability", "all_scripts_zero", "banglamath")
    banglish_wins = count_for(summary_rows, "recoverability", "banglish_beats_alternate", "all")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Across 600 paired model-item slots, reviewed Banglish trails Bangla by "
            f"{points(float(all_delta_bangla['rate']))} points "
            f"(item-bootstrap CI [{points(float(all_delta_bangla['ci95_low']))}, "
            f"{points(float(all_delta_bangla['ci95_high']))}]) and English by "
            f"{points(float(all_delta_english['rate']))} points "
            f"(CI [{points(float(all_delta_english['ci95_low']))}, "
            f"{points(float(all_delta_english['ci95_high']))}]).",
            f"- BEnQA carries the cleanest recoverability signal: {benqa_pressure}/144",
            "  items have at least two-model support in Bangla or English while",
            "  reviewed Banglish has at most one correct model; only "
            f"{benqa_hard}/144 BEnQA items are all-script hard.",
            f"- BanglaMATH remains a stress-test slice: {banglamath_hard}/56 items are",
            "  all-script hard across the three Qwen rows, so its low Banglish score",
            "  should be interpreted with that difficulty caveat.",
            f"- Banglish is not uniformly worse: it beats both alternate scripts on",
            f"  {banglish_wins}/200 items. Keep this as counterevidence against",
            "  overclaiming, while the dominant consensus pattern remains negative.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_item_consensus.py`",
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
    item_fields = list(item_rows[0])
    summary_fields = [
        "section",
        "key",
        "dataset",
        "n",
        "denominator",
        "rate",
        "ci95_low",
        "ci95_high",
        "detail",
    ]
    write_csv(args.items_output, item_rows, item_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
