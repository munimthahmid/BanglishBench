#!/usr/bin/env python3
"""Build frozen-v5 paired script-gap intervals by dataset."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAILURES = (
    ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
)
DEFAULT_OUTPUT = ROOT / "results/analysis/v5_dataset_gap_intervals.csv"
DEFAULT_REPORT = ROOT / "reports/v5_dataset_gap_intervals.md"

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
DATASETS = ("all", "benqa", "banglamath")
COMPARISONS = (
    ("banglish_minus_bangla", "bangla_correct", "banglish_clean_correct"),
    ("banglish_minus_english", "english_correct", "banglish_clean_correct"),
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def summarize(
    rows: list[dict[str, str]],
    model: str,
    dataset: str,
    comparison: str,
    left_col: str,
    right_col: str,
    samples: int,
    seed: int,
) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["model"] == model and (dataset == "all" or row["dataset"] == dataset)
    ]
    pairs = [(truthy(row[left_col]), truthy(row[right_col])) for row in selected]
    observed, low, high, p_opposite = bootstrap_delta(pairs, samples=samples, seed=seed)
    left_correct = sum(int(left) for left, _right in pairs)
    right_correct = sum(int(right) for _left, right in pairs)
    return {
        "model": MODEL_LABELS.get(model, model),
        "dataset": dataset,
        "comparison": comparison,
        "n": len(pairs),
        "left_correct": left_correct,
        "right_correct": right_correct,
        "delta_right_minus_left": round(observed, 4),
        "ci95_low": round(low, 4),
        "ci95_high": round(high, 4),
        "bootstrap_p_opposite_direction": round(p_opposite, 4),
        "gains": sum((not left) and right for left, right in pairs),
        "losses": sum(left and (not right) for left, right in pairs),
        "samples": samples,
        "seed": seed,
    }


def build_rows(rows: list[dict[str, str]], samples: int, seed: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for dataset in DATASETS:
            for comparison, left_col, right_col in COMPARISONS:
                out.append(
                    summarize(rows, model, dataset, comparison, left_col, right_col, samples, seed)
                )
    return out


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    output_csv: Path,
    source: Path,
) -> None:
    lines = [
        "# Frozen-V5 Dataset-Level Script-Gap Intervals",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend report adds paired bootstrap intervals to the Chapter 4",
        "dataset-level split. It uses the frozen-v5 cross-script failure table,",
        "so Bangla and English are the unchanged controlled outputs and Banglish",
        "is the reviewed-v5 rerun.",
        "",
        f"- Machine-readable summary: `{repo_path(output_csv)}`",
        f"- Source failure table: `{repo_path(source)}`",
        "",
        "## Banglish Minus Bangla",
        "",
        "| Model | Dataset | Bangla | Reviewed Banglish | Delta | 95% CI | Gains | Losses |",
        "| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in rows:
        if row["comparison"] != "banglish_minus_bangla":
            continue
        lines.append(
            f"| {row['model']} | `{row['dataset']}` | {row['left_correct']}/{row['n']} | "
            f"{row['right_correct']}/{row['n']} | {points(row['delta_right_minus_left'])} pts | "
            f"[{points(row['ci95_low'])}, {points(row['ci95_high'])}] | "
            f"{row['gains']} | {row['losses']} |"
        )

    lines.extend(
        [
            "",
            "## Banglish Minus English",
            "",
            "| Model | Dataset | English | Reviewed Banglish | Delta | 95% CI | Gains | Losses |",
            "| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for row in rows:
        if row["comparison"] != "banglish_minus_english":
            continue
        lines.append(
            f"| {row['model']} | `{row['dataset']}` | {row['left_correct']}/{row['n']} | "
            f"{row['right_correct']}/{row['n']} | {points(row['delta_right_minus_left'])} pts | "
            f"[{points(row['ci95_low'])}, {points(row['ci95_high'])}] | "
            f"{row['gains']} | {row['losses']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- BEnQA is the clearest dataset-level source of the reviewed-v5",
            "  Banglish-below-Bangla signal: Qwen3-4B has a clearly negative paired",
            "  interval, while Qwen2.5-3B and Qwen2.5-7B 8-bit are directionally",
            "  negative but their BEnQA intervals reach zero.",
            "- BanglaMATH remains a low-accuracy stress test. Its Banglish-Bangla",
            "  deltas are negative or near zero, but the intervals are wide and the",
            "  models answer very few BanglaMATH items correctly in any script.",
            "- Banglish is below English in BEnQA for all three thesis-facing Qwen",
            "  rows. BanglaMATH again has wide, low-accuracy intervals.",
            "",
            "Thesis-safe phrasing:",
            "",
            "> The release-facing script gap is clearest on BEnQA, where the models",
            "> have enough task competence for paired script differences to be",
            "> meaningful. BanglaMATH should remain a hard stress test rather than",
            "> the basis for fine-grained dataset-level claims.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260531)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = read_csv(args.failure_items)
    if len(source_rows) != 600:
        raise SystemExit(f"Expected 600 source rows, got {len(source_rows)}")
    rows = build_rows(source_rows, args.samples, args.seed)
    if len(rows) != 18:
        raise SystemExit(f"Expected 18 summary rows, got {len(rows)}")
    expected_counts = {"all": 200, "benqa": 144, "banglamath": 56}
    for row in rows:
        if int(row["n"]) != expected_counts[row["dataset"]]:
            raise SystemExit(f"Unexpected n for {row['model']} {row['dataset']}: {row['n']}")
    write_csv(args.output, rows)
    write_report(args.report_output, rows, args.output, args.failure_items)
    print(f"rows={len(rows)} report={args.report_output} csv={args.output}")


if __name__ == "__main__":
    main()
