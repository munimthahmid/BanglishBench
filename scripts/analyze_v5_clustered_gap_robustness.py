#!/usr/bin/env python3
"""Cluster-bootstrap frozen-v5 script gaps by curriculum stratum."""

from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_CLUSTER_OUTPUT = ROOT / "results/analysis/v5_clustered_gap_clusters.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_clustered_gap_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_clustered_gap_robustness.md"

MODELS = (
    ("Qwen2.5-3B", "Qwen2.5-3B"),
    ("Qwen2.5-7B 8-bit", "Qwen2.5-7B"),
    ("Qwen3-4B", "Qwen3-4B"),
)
DATASETS = ("all", "benqa", "banglamath")
COMPARISONS = (
    ("banglish_minus_bangla", "bangla", "banglish", "Bangla", "Reviewed Banglish"),
    ("banglish_minus_english", "english", "banglish", "English", "Reviewed Banglish"),
)
BOOTSTRAP_ITERATIONS = 10000
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


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def percent(count: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * count / denominator:.1f}%"


def cluster_key(row: dict[str, str]) -> str:
    dataset = row["dataset"]
    if dataset == "benqa":
        return f"benqa:{row.get('subject', '').strip() or row.get('domain', '').strip()}"
    if dataset == "banglamath":
        return f"banglamath:{row.get('grade', '').strip().lower() or 'unknown'}"
    return f"{dataset}:unknown"


def select_rows(rows: list[dict[str, str]], dataset: str) -> list[dict[str, str]]:
    if dataset == "all":
        return rows
    return [row for row in rows if row["dataset"] == dataset]


def column(model_column_prefix: str, script: str) -> str:
    return f"{model_column_prefix}_{script}_correct"


def row_diff(row: dict[str, str], model_column_prefix: str, left_script: str, right_script: str) -> int:
    left = truthy(row[column(model_column_prefix, left_script)])
    right = truthy(row[column(model_column_prefix, right_script)])
    return int(right) - int(left)


def build_cluster_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model_label, model_column_prefix in MODELS:
        for dataset in DATASETS:
            selected = select_rows(rows, dataset)
            grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
            for row in selected:
                grouped[cluster_key(row)].append(row)
            for comparison, left_script, right_script, left_label, right_label in COMPARISONS:
                for key, cluster_rows in sorted(grouped.items()):
                    n = len(cluster_rows)
                    left_correct = sum(
                        truthy(row[column(model_column_prefix, left_script)]) for row in cluster_rows
                    )
                    right_correct = sum(
                        truthy(row[column(model_column_prefix, right_script)]) for row in cluster_rows
                    )
                    delta = (right_correct - left_correct) / n if n else 0.0
                    out.append(
                        {
                            "model": model_label,
                            "dataset": dataset,
                            "comparison": comparison,
                            "left_script": left_label,
                            "right_script": right_label,
                            "cluster_key": key,
                            "n": n,
                            "left_correct": left_correct,
                            "right_correct": right_correct,
                            "delta_right_minus_left": round(delta, 4),
                            "gains": sum(
                                (not truthy(row[column(model_column_prefix, left_script)]))
                                and truthy(row[column(model_column_prefix, right_script)])
                                for row in cluster_rows
                            ),
                            "losses": sum(
                                truthy(row[column(model_column_prefix, left_script)])
                                and (not truthy(row[column(model_column_prefix, right_script)]))
                                for row in cluster_rows
                            ),
                        }
                    )
    return out


def bootstrap_cluster_delta(
    cluster_rows: list[dict[str, Any]],
    seed: int,
    iterations: int,
) -> tuple[float, float, float, float]:
    observed_denominator = sum(int(row["n"]) for row in cluster_rows)
    observed_numerator = sum(
        int(row["right_correct"]) - int(row["left_correct"]) for row in cluster_rows
    )
    observed = observed_numerator / observed_denominator
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(iterations):
        numerator = 0
        denominator = 0
        for _index in range(len(cluster_rows)):
            row = rng.choice(cluster_rows)
            numerator += int(row["right_correct"]) - int(row["left_correct"])
            denominator += int(row["n"])
        draws.append(numerator / denominator if denominator else 0.0)
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    if observed < 0:
        p_opposite = sum(draw >= 0 for draw in draws) / len(draws)
    elif observed > 0:
        p_opposite = sum(draw <= 0 for draw in draws) / len(draws)
    else:
        p_opposite = 1.0
    return observed, low, high, p_opposite


def build_summary_rows(
    cluster_rows: list[dict[str, Any]],
    iterations: int,
    seed: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seed_offset = 0
    for model_label, _model_column_prefix in MODELS:
        for dataset in DATASETS:
            for comparison, _left_script, _right_script, left_label, right_label in COMPARISONS:
                selected = [
                    row
                    for row in cluster_rows
                    if row["model"] == model_label
                    and row["dataset"] == dataset
                    and row["comparison"] == comparison
                ]
                seed_offset += 1
                observed, low, high, p_opposite = bootstrap_cluster_delta(
                    selected,
                    seed + seed_offset,
                    iterations,
                )
                n = sum(int(row["n"]) for row in selected)
                left_correct = sum(int(row["left_correct"]) for row in selected)
                right_correct = sum(int(row["right_correct"]) for row in selected)
                out.append(
                    {
                        "model": model_label,
                        "dataset": dataset,
                        "comparison": comparison,
                        "left_script": left_label,
                        "right_script": right_label,
                        "n": n,
                        "clusters": len(selected),
                        "left_correct": left_correct,
                        "right_correct": right_correct,
                        "delta_right_minus_left": round(observed, 4),
                        "cluster_ci95_low": round(low, 4),
                        "cluster_ci95_high": round(high, 4),
                        "cluster_bootstrap_p_opposite_direction": round(p_opposite, 4),
                        "gains": sum(int(row["gains"]) for row in selected),
                        "losses": sum(int(row["losses"]) for row in selected),
                        "iterations": iterations,
                        "seed": seed + seed_offset,
                        "cluster_definition": "BEnQA subject plus BanglaMATH grade",
                    }
                )
    return out


def find_summary(
    rows: list[dict[str, Any]],
    model: str,
    dataset: str,
    comparison: str,
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["model"] == model and row["dataset"] == dataset and row["comparison"] == comparison
    )


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    cluster_rows: list[dict[str, Any]],
    summary_output: Path,
    cluster_output: Path,
    input_path: Path,
) -> None:
    lines = [
        "# Frozen-V5 Clustered Gap Robustness",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend robustness check recomputes the paired script gaps with a",
        "cluster bootstrap instead of an item bootstrap. The resampling unit is a",
        "curriculum stratum: BEnQA subject for BEnQA rows and BanglaMATH grade for",
        "BanglaMATH rows. It checks whether the release-facing gap depends on",
        "treating neighboring items inside the same subject/grade as independent.",
        "",
        f"- Source item table: `{repo_path(input_path)}`",
        f"- Cluster rows: `{repo_path(cluster_output)}`",
        f"- Summary rows: `{repo_path(summary_output)}`",
        "",
        "BanglaMATH has only three grade clusters, so its cluster intervals are",
        "coarse and should remain descriptive. The all-200 rows use 16 clusters",
        "(13 BEnQA subjects plus 3 BanglaMATH grades).",
        "",
        "## Banglish Minus Bangla",
        "",
        "| Model | Dataset | Clusters | Bangla | Reviewed Banglish | Delta | Cluster 95% CI | Gains | Losses |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for model_label, _prefix in MODELS:
        for dataset in DATASETS:
            row = find_summary(summary_rows, model_label, dataset, "banglish_minus_bangla")
            lines.append(
                f"| {model_label} | `{dataset}` | {row['clusters']} | "
                f"{row['left_correct']}/{row['n']} | {row['right_correct']}/{row['n']} | "
                f"{points(row['delta_right_minus_left'])} pts | "
                f"[{points(row['cluster_ci95_low'])}, {points(row['cluster_ci95_high'])}] | "
                f"{row['gains']} | {row['losses']} |"
            )

    lines.extend(
        [
            "",
            "## Banglish Minus English",
            "",
            "| Model | Dataset | Clusters | English | Reviewed Banglish | Delta | Cluster 95% CI | Gains | Losses |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for model_label, _prefix in MODELS:
        for dataset in DATASETS:
            row = find_summary(summary_rows, model_label, dataset, "banglish_minus_english")
            lines.append(
                f"| {model_label} | `{dataset}` | {row['clusters']} | "
                f"{row['left_correct']}/{row['n']} | {row['right_correct']}/{row['n']} | "
                f"{points(row['delta_right_minus_left'])} pts | "
                f"[{points(row['cluster_ci95_low'])}, {points(row['cluster_ci95_high'])}] | "
                f"{row['gains']} | {row['losses']} |"
            )

    qwen3_benqa = find_summary(summary_rows, "Qwen3-4B", "benqa", "banglish_minus_bangla")
    qwen7_all = find_summary(summary_rows, "Qwen2.5-7B 8-bit", "all", "banglish_minus_bangla")
    qwen3_all = find_summary(summary_rows, "Qwen3-4B", "all", "banglish_minus_bangla")
    qwen25_all = find_summary(summary_rows, "Qwen2.5-3B", "all", "banglish_minus_bangla")
    qwen25_benqa = find_summary(summary_rows, "Qwen2.5-3B", "benqa", "banglish_minus_bangla")
    qwen7_benqa = find_summary(summary_rows, "Qwen2.5-7B 8-bit", "benqa", "banglish_minus_bangla")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- The all-200 cluster bootstrap keeps Qwen2.5-7B 8-bit negative",
            f"  ({points(qwen7_all['delta_right_minus_left'])} pts, CI "
            f"[{points(qwen7_all['cluster_ci95_low'])}, {points(qwen7_all['cluster_ci95_high'])}])",
            f"  and Qwen3-4B negative ({points(qwen3_all['delta_right_minus_left'])} pts, CI",
            f"  [{points(qwen3_all['cluster_ci95_low'])}, {points(qwen3_all['cluster_ci95_high'])}]).",
            f"- Qwen2.5-3B remains directionally negative on all-200",
            f"  ({points(qwen25_all['delta_right_minus_left'])} pts), but its cluster",
            f"  interval reaches zero [{points(qwen25_all['cluster_ci95_low'])},",
            f"  {points(qwen25_all['cluster_ci95_high'])}], matching the existing",
            "  caution that the 3B all-200 result is weakest.",
            f"- On BEnQA, Qwen3-4B remains clearly negative under subject-cluster",
            f"  resampling ({points(qwen3_benqa['delta_right_minus_left'])} pts, CI",
            f"  [{points(qwen3_benqa['cluster_ci95_low'])}, {points(qwen3_benqa['cluster_ci95_high'])}]).",
            f"  The Qwen2.5 BEnQA rows also remain negative; Qwen2.5-3B reaches",
            f"  zero (CI [{points(qwen25_benqa['cluster_ci95_low'])},",
            f"  {points(qwen25_benqa['cluster_ci95_high'])}]), while Qwen2.5-7B",
            f"  stays below zero (CI [{points(qwen7_benqa['cluster_ci95_low'])},",
            f"  {points(qwen7_benqa['cluster_ci95_high'])}]).",
            "- BanglaMATH cluster intervals are intentionally treated as descriptive",
            "  because there are only three grade clusters and the slice is",
            "  low-accuracy across scripts.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_clustered_gap_robustness.py`",
            f"- Cluster rows: `{repo_path(cluster_output)}`",
            f"- Summary rows: `{repo_path(summary_output)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--cluster-output", type=Path, default=DEFAULT_CLUSTER_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--iterations", type=int, default=BOOTSTRAP_ITERATIONS)
    parser.add_argument("--seed", type=int, default=BOOTSTRAP_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_csv(args.input)
    if len(rows) != 200:
        raise SystemExit(f"Expected 200 item rows, got {len(rows)}")
    cluster_rows = build_cluster_rows(rows)
    summary_rows = build_summary_rows(cluster_rows, args.iterations, args.seed)
    if len(cluster_rows) != 192:
        raise SystemExit(f"Expected 192 cluster rows, got {len(cluster_rows)}")
    if len(summary_rows) != 18:
        raise SystemExit(f"Expected 18 summary rows, got {len(summary_rows)}")
    write_csv(args.cluster_output, cluster_rows, list(cluster_rows[0]))
    write_csv(args.summary_output, summary_rows, list(summary_rows[0]))
    write_report(
        args.report_output,
        summary_rows,
        cluster_rows,
        args.summary_output,
        args.cluster_output,
        args.input,
    )
    print(
        f"clusters={len(cluster_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
