#!/usr/bin/env python3
"""Exact paired sign tests for frozen-v5 script gaps."""

from __future__ import annotations

import argparse
import csv
import math
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAILURES = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
DEFAULT_OUTPUT = ROOT / "results/analysis/v5_paired_sign_tests.csv"
DEFAULT_REPORT = ROOT / "reports/v5_paired_sign_tests.md"

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
    ("banglish_minus_bangla", "bangla_correct", "banglish_clean_correct", "Bangla"),
    ("banglish_minus_english", "english_correct", "banglish_clean_correct", "English"),
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


def pvalue(value: Any) -> str:
    p = float(value)
    if p < 0.0001:
        return "<0.0001"
    return f"{p:.4f}"


def p_clause(value: Any) -> str:
    formatted = pvalue(value)
    if formatted.startswith("<"):
        return f"p{formatted}"
    return f"p={formatted}"


def exact_binomial_cdf(k: int, n: int) -> float:
    if n <= 0:
        return 1.0
    return sum(math.comb(n, i) for i in range(k + 1)) / (2**n)


def exact_two_sided_pvalue(gains: int, losses: int) -> float:
    discordant = gains + losses
    if discordant == 0:
        return 1.0
    smaller = min(gains, losses)
    return min(1.0, 2.0 * exact_binomial_cdf(smaller, discordant))


def exact_one_sided_banglish_lower(gains: int, losses: int) -> float:
    discordant = gains + losses
    if discordant == 0:
        return 1.0
    # Under the null, Banglish wins and losses are equally likely. A low number
    # of gains supports the directional alternative that Banglish is worse.
    return exact_binomial_cdf(gains, discordant)


def summarize(
    rows: list[dict[str, str]],
    model: str,
    dataset: str,
    comparison: str,
    left_col: str,
    right_col: str,
    left_label: str,
) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["model"] == model and (dataset == "all" or row["dataset"] == dataset)
    ]
    pairs = [(truthy(row[left_col]), truthy(row[right_col])) for row in selected]
    left_correct = sum(int(left) for left, _right in pairs)
    right_correct = sum(int(right) for _left, right in pairs)
    gains = sum((not left) and right for left, right in pairs)
    losses = sum(left and (not right) for left, right in pairs)
    ties_both_correct = sum(left and right for left, right in pairs)
    ties_both_wrong = sum((not left) and (not right) for left, right in pairs)
    discordant = gains + losses
    delta = (right_correct - left_correct) / len(pairs) if pairs else 0.0
    return {
        "model": MODEL_LABELS.get(model, model),
        "dataset": dataset,
        "comparison": comparison,
        "baseline_script": left_label,
        "candidate_script": "Reviewed Banglish",
        "n": len(pairs),
        "baseline_correct": left_correct,
        "candidate_correct": right_correct,
        "delta_candidate_minus_baseline": round(delta, 4),
        "banglish_gains": gains,
        "banglish_losses": losses,
        "discordant_pairs": discordant,
        "ties_both_correct": ties_both_correct,
        "ties_both_wrong": ties_both_wrong,
        "exact_sign_p_two_sided": round(exact_two_sided_pvalue(gains, losses), 6),
        "exact_sign_p_banglish_lower": round(exact_one_sided_banglish_lower(gains, losses), 6),
        "loss_to_gain_ratio_haldane": round((losses + 0.5) / (gains + 0.5), 4),
    }


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for dataset in DATASETS:
            for comparison, left_col, right_col, left_label in COMPARISONS:
                out.append(summarize(rows, model, dataset, comparison, left_col, right_col, left_label))
    return out


def find_row(
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


def write_report(path: Path, rows: list[dict[str, Any]], output_csv: Path, source: Path) -> None:
    lines = [
        "# Frozen-V5 Paired Sign Tests",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit adds exact paired sign tests to the frozen-v5 script",
        "gap table. For each model, dataset, and comparison, it counts only",
        "discordant item pairs: rows where reviewed Banglish wins over the",
        "baseline script, and rows where the baseline script wins over reviewed",
        "Banglish. The exact two-sided p-value is a binomial sign test over those",
        "discordant pairs.",
        "",
        f"- Machine-readable summary: `{repo_path(output_csv)}`",
        f"- Source failure table: `{repo_path(source)}`",
        "",
        "These tests complement the bootstrap intervals. They are not a replacement",
        "for effect sizes, and they remain paired behavioral tests over a controlled",
        "benchmark.",
        "",
        "## Banglish Versus Bangla",
        "",
        "| Model | Dataset | Bangla | Reviewed Banglish | Delta | Banglish gains | Banglish losses | Discordant | Exact p |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODEL_LABELS.values():
        for dataset in DATASETS:
            row = find_row(rows, model, dataset, "banglish_minus_bangla")
            lines.append(
                f"| {model} | `{dataset}` | {row['baseline_correct']}/{row['n']} | "
                f"{row['candidate_correct']}/{row['n']} | "
                f"{points(row['delta_candidate_minus_baseline'])} pts | "
                f"{row['banglish_gains']} | {row['banglish_losses']} | "
                f"{row['discordant_pairs']} | {pvalue(row['exact_sign_p_two_sided'])} |"
            )

    lines.extend(
        [
            "",
            "## Banglish Versus English",
            "",
            "| Model | Dataset | English | Reviewed Banglish | Delta | Banglish gains | Banglish losses | Discordant | Exact p |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODEL_LABELS.values():
        for dataset in DATASETS:
            row = find_row(rows, model, dataset, "banglish_minus_english")
            lines.append(
                f"| {model} | `{dataset}` | {row['baseline_correct']}/{row['n']} | "
                f"{row['candidate_correct']}/{row['n']} | "
                f"{points(row['delta_candidate_minus_baseline'])} pts | "
                f"{row['banglish_gains']} | {row['banglish_losses']} | "
                f"{row['discordant_pairs']} | {pvalue(row['exact_sign_p_two_sided'])} |"
            )

    qwen25_3b = find_row(rows, "Qwen2.5-3B", "all", "banglish_minus_bangla")
    qwen25_7b = find_row(rows, "Qwen2.5-7B 8-bit", "all", "banglish_minus_bangla")
    qwen3 = find_row(rows, "Qwen3-4B", "all", "banglish_minus_bangla")
    qwen3_benqa = find_row(rows, "Qwen3-4B", "benqa", "banglish_minus_bangla")
    english_all = [
        find_row(rows, model, "all", "banglish_minus_english")
        for model in MODEL_LABELS.values()
    ]
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Qwen2.5-7B 8-bit has {qwen25_7b['banglish_gains']} Banglish-over-Bangla",
            f"  gains versus {qwen25_7b['banglish_losses']} losses on all-200",
            f"  (two-sided exact {p_clause(qwen25_7b['exact_sign_p_two_sided'])}).",
            f"  Qwen3-4B has {qwen3['banglish_gains']} gains versus",
            f"  {qwen3['banglish_losses']} losses ({p_clause(qwen3['exact_sign_p_two_sided'])}).",
            f"- Qwen2.5-3B is again the weakest all-200 row: {qwen25_3b['banglish_gains']}",
            f"  gains versus {qwen25_3b['banglish_losses']} losses,",
            f"  {p_clause(qwen25_3b['exact_sign_p_two_sided'])}. Keep the existing",
            "  CI-reaches-zero qualification.",
            f"- Qwen3-4B BEnQA remains strongly asymmetric: {qwen3_benqa['banglish_gains']}",
            f"  gains versus {qwen3_benqa['banglish_losses']} losses,",
            f"  {p_clause(qwen3_benqa['exact_sign_p_two_sided'])}.",
            "- Banglish-versus-English asymmetry is exact-test strong on all-200 for",
            "  all three thesis-facing Qwen rows: "
            + "; ".join(
                f"{row['model']} {p_clause(row['exact_sign_p_two_sided'])}"
                for row in english_all
            )
            + ".",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_paired_sign_tests.py`",
            f"- Summary table: `{repo_path(output_csv)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = read_csv(args.failure_items)
    if len(source_rows) != 600:
        raise SystemExit(f"Expected 600 source rows, got {len(source_rows)}")
    rows = build_rows(source_rows)
    if len(rows) != 18:
        raise SystemExit(f"Expected 18 sign-test rows, got {len(rows)}")
    write_csv(args.output, rows)
    write_report(args.report_output, rows, args.output, args.failure_items)
    print(f"rows={len(rows)} report={args.report_output}")


if __name__ == "__main__":
    main()
