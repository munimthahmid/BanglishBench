#!/usr/bin/env python3
"""Subject-macro BEnQA script-gap sensitivity for frozen-v5 rows."""

from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAILURES = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
DEFAULT_SUBJECT_OUTPUT = ROOT / "results/analysis/v5_benqa_subject_balance_subjects.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_subject_balance_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_subject_balance.md"

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
VARIANTS = ("bangla", "banglish_clean", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}
COMPARISONS = (
    ("banglish_minus_bangla", "bangla", "banglish_clean", "Bangla"),
    ("banglish_minus_english", "english", "banglish_clean", "English"),
)
BOOTSTRAP_ITERATIONS = 10_000
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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def percent(value: float) -> str:
    return f"{100 * value:.1f}%"


def points(value: float) -> str:
    scaled = 100 * value
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    low = int(pos)
    high = min(low + 1, len(ordered) - 1)
    frac = pos - low
    return ordered[low] * (1 - frac) + ordered[high] * frac


def subject_accuracy(row: dict[str, Any], variant: str) -> float:
    return int(row[f"{variant}_correct"]) / int(row["n"])


def build_subject_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [
            row for row in rows if row["model"] == model and row["dataset"] == "benqa"
        ]
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in model_rows:
            grouped[row["subject"]].append(row)
        if len(grouped) != 13:
            raise SystemExit(f"Expected 13 BEnQA subjects for {model}, got {len(grouped)}")
        for subject, subject_rows in sorted(grouped.items()):
            n = len(subject_rows)
            item: dict[str, Any] = {
                "model": MODEL_LABELS[model],
                "model_id": model,
                "subject": subject,
                "n": n,
            }
            for variant in VARIANTS:
                item[f"{variant}_correct"] = sum(
                    truthy(row[f"{variant}_correct"]) for row in subject_rows
                )
                item[f"{variant}_accuracy"] = round(item[f"{variant}_correct"] / n, 4)
            for comparison, baseline, candidate, _baseline_label in COMPARISONS:
                item[f"{comparison}_delta"] = round(
                    item[f"{candidate}_accuracy"] - item[f"{baseline}_accuracy"],
                    4,
                )
                item[f"{comparison}_gains"] = sum(
                    (not truthy(row[f"{baseline}_correct"]))
                    and truthy(row[f"{candidate}_correct"])
                    for row in subject_rows
                )
                item[f"{comparison}_losses"] = sum(
                    truthy(row[f"{baseline}_correct"])
                    and (not truthy(row[f"{candidate}_correct"]))
                    for row in subject_rows
                )
            out.append(item)
    return out


def bootstrap_subject_macro_delta(
    subject_rows: list[dict[str, Any]],
    comparison: str,
    iterations: int,
    seed: int,
) -> tuple[float, float, float]:
    rng = random.Random(seed)
    deltas = [float(row[f"{comparison}_delta"]) for row in subject_rows]
    observed = sum(deltas) / len(deltas)
    draws: list[float] = []
    for _ in range(iterations):
        draw = [rng.choice(deltas) for _i in range(len(deltas))]
        draws.append(sum(draw) / len(draw))
    return observed, percentile(draws, 0.025), percentile(draws, 0.975)


def build_summary_rows(
    subject_rows: list[dict[str, Any]],
    iterations: int,
    seed: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seed_offset = 0
    for model in MODEL_LABELS.values():
        model_subjects = [row for row in subject_rows if row["model"] == model]
        for comparison, baseline, candidate, baseline_label in COMPARISONS:
            seed_offset += 1
            observed, low, high = bootstrap_subject_macro_delta(
                model_subjects,
                comparison,
                iterations,
                seed + seed_offset,
            )
            n = sum(int(row["n"]) for row in model_subjects)
            baseline_correct = sum(int(row[f"{baseline}_correct"]) for row in model_subjects)
            candidate_correct = sum(int(row[f"{candidate}_correct"]) for row in model_subjects)
            baseline_macro = sum(subject_accuracy(row, baseline) for row in model_subjects) / len(model_subjects)
            candidate_macro = sum(subject_accuracy(row, candidate) for row in model_subjects) / len(model_subjects)
            out.append(
                {
                    "model": model,
                    "comparison": comparison,
                    "baseline_variant": baseline,
                    "baseline_label": baseline_label,
                    "candidate_variant": candidate,
                    "candidate_label": VARIANT_LABELS[candidate],
                    "n": n,
                    "subjects": len(model_subjects),
                    "baseline_correct": baseline_correct,
                    "candidate_correct": candidate_correct,
                    "baseline_micro_accuracy": round(baseline_correct / n, 4),
                    "candidate_micro_accuracy": round(candidate_correct / n, 4),
                    "micro_delta": round((candidate_correct - baseline_correct) / n, 4),
                    "baseline_subject_macro_accuracy": round(baseline_macro, 4),
                    "candidate_subject_macro_accuracy": round(candidate_macro, 4),
                    "subject_macro_delta": round(observed, 4),
                    "subject_macro_ci95_low": round(low, 4),
                    "subject_macro_ci95_high": round(high, 4),
                    "subjects_negative": sum(
                        float(row[f"{comparison}_delta"]) < 0 for row in model_subjects
                    ),
                    "subjects_positive": sum(
                        float(row[f"{comparison}_delta"]) > 0 for row in model_subjects
                    ),
                    "subjects_zero": sum(
                        float(row[f"{comparison}_delta"]) == 0 for row in model_subjects
                    ),
                    "gains": sum(int(row[f"{comparison}_gains"]) for row in model_subjects),
                    "losses": sum(int(row[f"{comparison}_losses"]) for row in model_subjects),
                    "iterations": iterations,
                    "seed": seed + seed_offset,
                }
            )
    return out


def find_summary(rows: list[dict[str, Any]], model: str, comparison: str) -> dict[str, Any]:
    return next(row for row in rows if row["model"] == model and row["comparison"] == comparison)


def write_report(
    path: Path,
    subject_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    source: Path,
    subject_output: Path,
    summary_output: Path,
    iterations: int,
) -> None:
    lines = [
        "# Frozen-V5 BEnQA Subject-Macro Balance",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit asks whether the BEnQA part of the frozen-v5 gap",
        "depends on subject-size weighting. It computes each subject's script",
        "accuracy, then averages the 13 BEnQA subjects equally. Bootstrap",
        "intervals resample subjects, not individual items.",
        "",
        f"- Source failure table: `{repo_path(source)}`",
        f"- Per-subject table: `{repo_path(subject_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        f"- Bootstrap iterations: {iterations}",
        "",
        "## Subject-Macro Summary",
        "",
        "| Model | Comparison | Micro delta | Subject-macro delta | Subject-macro CI | Negative subjects | Gains/Losses |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODEL_LABELS.values():
        for comparison, _baseline, _candidate, baseline_label in COMPARISONS:
            row = find_summary(summary_rows, model, comparison)
            lines.append(
                f"| {model} | Banglish - {baseline_label} | "
                f"{points(row['micro_delta'])} pts | "
                f"{points(row['subject_macro_delta'])} pts | "
                f"[{points(row['subject_macro_ci95_low'])}, "
                f"{points(row['subject_macro_ci95_high'])}] pts | "
                f"{row['subjects_negative']}/{row['subjects']} | "
                f"{row['gains']}/{row['losses']} |"
            )

    lines.extend(
        [
            "",
            "## Per-Subject Accuracy",
            "",
            "| Model | Subject | n | Bangla | Reviewed Banglish | English | Banglish-Bangla |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in subject_rows:
        lines.append(
            f"| {row['model']} | `{row['subject']}` | {row['n']} | "
            f"{row['bangla_correct']}/{row['n']} ({percent(row['bangla_accuracy'])}) | "
            f"{row['banglish_clean_correct']}/{row['n']} ({percent(row['banglish_clean_accuracy'])}) | "
            f"{row['english_correct']}/{row['n']} ({percent(row['english_accuracy'])}) | "
            f"{points(row['banglish_minus_bangla_delta'])} pts |"
        )

    q3 = find_summary(summary_rows, "Qwen3-4B", "banglish_minus_bangla")
    q25_7b = find_summary(summary_rows, "Qwen2.5-7B 8-bit", "banglish_minus_bangla")
    q25_3b = find_summary(summary_rows, "Qwen2.5-3B", "banglish_minus_bangla")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Equal-weighting BEnQA subjects keeps reviewed Banglish below Bangla",
            "  for all three thesis-facing Qwen rows.",
            f"- Qwen3-4B remains the clearest subject-balanced BEnQA case:",
            f"  {points(q3['subject_macro_delta'])} pts, CI",
            f"  [{points(q3['subject_macro_ci95_low'])}, {points(q3['subject_macro_ci95_high'])}].",
            f"- Qwen2.5-7B 8-bit is directionally negative under subject balancing",
            f"  ({points(q25_7b['subject_macro_delta'])} pts), while Qwen2.5-3B",
            f"  remains the weaker row ({points(q25_3b['subject_macro_delta'])} pts).",
            "- This complements the leave-one-subject check: BEnQA is not only",
            "  negative after dropping subjects, but also negative when subjects",
            "  are given equal macro weight.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--subject-output", type=Path, default=DEFAULT_SUBJECT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--bootstrap-iterations", type=int, default=BOOTSTRAP_ITERATIONS)
    parser.add_argument("--seed", type=int, default=BOOTSTRAP_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = read_csv(args.failure_items)
    if len(source_rows) != 600:
        raise SystemExit(f"Expected 600 source rows, got {len(source_rows)}")
    subject_rows = build_subject_rows(source_rows)
    summary_rows = build_summary_rows(subject_rows, args.bootstrap_iterations, args.seed)
    write_csv(args.subject_output, subject_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        subject_rows,
        summary_rows,
        args.failure_items,
        args.subject_output,
        args.summary_output,
        args.bootstrap_iterations,
    )
    print(
        f"subjects={len(subject_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
