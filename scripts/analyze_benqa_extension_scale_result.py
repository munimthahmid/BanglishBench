#!/usr/bin/env python3
"""Analyze paired script gaps for BEnQA extension model outputs."""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("bangla", "banglish_clean", "english")
COMPARISONS = (
    ("banglish_minus_bangla", "banglish_clean", "bangla"),
    ("banglish_minus_english", "banglish_clean", "english"),
    ("english_minus_bangla", "english", "bangla"),
)


def read_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            missing = {"id", "variant", "correct", "parsed"} - set(row)
            if missing:
                raise ValueError(f"{path}:{line_no} missing fields: {sorted(missing)}")
            rows.append(row)
    return rows


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    idx = int(round((len(sorted_values) - 1) * p))
    return sorted_values[max(0, min(idx, len(sorted_values) - 1))]


def bootstrap_ci(
    diffs: list[int],
    *,
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    if not diffs:
        return 0.0, 0.0
    if iterations <= 0:
        point = sum(diffs) / len(diffs)
        return point, point
    rng = random.Random(seed)
    n = len(diffs)
    samples: list[float] = []
    for _ in range(iterations):
        total = 0
        for _idx in range(n):
            total += diffs[rng.randrange(n)]
        samples.append(total / n)
    samples.sort()
    return percentile(samples, 0.025), percentile(samples, 0.975)


def build_item_matrix(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    by_item: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in rows:
        item_id = str(row["id"])
        variant = str(row["variant"])
        if variant not in VARIANTS:
            continue
        if variant in by_item[item_id]:
            raise ValueError(f"duplicate row for item={item_id} variant={variant}")
        by_item[item_id][variant] = row

    matrix: list[dict[str, str]] = []
    for item_id in sorted(by_item):
        variants = by_item[item_id]
        out = {"id": item_id}
        for variant in VARIANTS:
            row = variants.get(variant)
            if row is None:
                out[f"{variant}_present"] = "0"
                out[f"{variant}_correct"] = ""
                out[f"{variant}_parsed"] = ""
            else:
                out[f"{variant}_present"] = "1"
                out[f"{variant}_correct"] = "1" if bool(row.get("correct")) else "0"
                out[f"{variant}_parsed"] = str(row.get("parsed", ""))
        matrix.append(out)
    return matrix


def variant_summary(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        variant = str(row["variant"])
        counts[variant]["n"] += 1
        if bool(row["correct"]):
            counts[variant]["correct"] += 1
        if str(row.get("parsed", "")).strip() == "":
            counts[variant]["parsed_empty"] += 1

    summary: list[dict[str, str]] = []
    for variant in VARIANTS:
        n = counts[variant]["n"]
        correct = counts[variant]["correct"]
        summary.append(
            {
                "metric": "variant_accuracy",
                "label": variant,
                "n": str(n),
                "correct": str(correct),
                "accuracy": f"{correct / n:.6f}" if n else "0.000000",
                "ci95_low": "",
                "ci95_high": "",
                "candidate_only": "",
                "baseline_only": "",
                "both_correct": "",
                "both_wrong": "",
                "parsed_empty": str(counts[variant]["parsed_empty"]),
            }
        )
    return summary


def paired_summary(
    matrix: list[dict[str, str]],
    *,
    bootstrap: int,
    seed: int,
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for label, candidate, baseline in COMPARISONS:
        diffs: list[int] = []
        candidate_only = 0
        baseline_only = 0
        both_correct = 0
        both_wrong = 0
        for row in matrix:
            if row[f"{candidate}_present"] != "1" or row[f"{baseline}_present"] != "1":
                continue
            cand = row[f"{candidate}_correct"] == "1"
            base = row[f"{baseline}_correct"] == "1"
            diffs.append(int(cand) - int(base))
            if cand and base:
                both_correct += 1
            elif cand and not base:
                candidate_only += 1
            elif base and not cand:
                baseline_only += 1
            else:
                both_wrong += 1
        n = len(diffs)
        delta = sum(diffs) / n if n else 0.0
        ci_low, ci_high = bootstrap_ci(diffs, iterations=bootstrap, seed=seed)
        out.append(
            {
                "metric": "paired_gap",
                "label": label,
                "n": str(n),
                "correct": "",
                "accuracy": f"{delta:.6f}",
                "ci95_low": f"{ci_low:.6f}",
                "ci95_high": f"{ci_high:.6f}",
                "candidate_only": str(candidate_only),
                "baseline_only": str(baseline_only),
                "both_correct": str(both_correct),
                "both_wrong": str(both_wrong),
                "parsed_empty": "",
            }
        )
    return out


def write_csv(rows: list[dict[str, str]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    *,
    title: str,
    input_path: Path,
    summary_path: Path,
    items_path: Path,
    report_path: Path,
    summary_rows: list[dict[str, str]],
    bootstrap: int,
) -> None:
    variants = [row for row in summary_rows if row["metric"] == "variant_accuracy"]
    paired = [row for row in summary_rows if row["metric"] == "paired_gap"]
    lines = [
        f"# {title}",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Result rows: `{rel(input_path)}`",
        f"- Summary CSV: `{rel(summary_path)}`",
        f"- Item matrix CSV: `{rel(items_path)}`",
        f"- Bootstrap iterations: {bootstrap}",
        "",
        "## Variant Accuracy",
        "",
        "| Variant | Correct | Total | Accuracy | Parsed empty |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in variants:
        n = int(row["n"])
        correct = int(row["correct"])
        lines.append(
            f"| {row['label']} | {correct} | {n} | {pct(correct / n) if n else '0.00%'} | {row['parsed_empty']} |"
        )
    lines.extend(
        [
            "",
            "## Paired Gaps",
            "",
            "Positive gaps mean the first named variant is more accurate than the second",
            "on the same paired items.",
            "",
            "| Gap | Items | Delta | 95% bootstrap CI | Candidate-only | Baseline-only | Both correct | Both wrong |",
            "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in paired:
        lines.append(
            "| "
            f"{row['label']} | {row['n']} | {pct(float(row['accuracy']))} | "
            f"[{pct(float(row['ci95_low']))}, {pct(float(row['ci95_high']))}] | "
            f"{row['candidate_only']} | {row['baseline_only']} | "
            f"{row['both_correct']} | {row['both_wrong']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Use this report as paired descriptive evidence for the extension run. For a",
            "26-row smoke, use only the operational/parser result and treat paired gaps",
            "as exploratory. For the 130-row pilot or 851-row full pass-only extension,",
            "the paired gaps become the scale-check evidence for the BEnQA component.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-summary", type=Path, required=True)
    parser.add_argument("--output-items", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--bootstrap", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260605)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    summary_path = args.output_summary if args.output_summary.is_absolute() else ROOT / args.output_summary
    items_path = args.output_items if args.output_items.is_absolute() else ROOT / args.output_items
    report_path = args.report if args.report.is_absolute() else ROOT / args.report

    rows = read_rows(input_path)
    matrix = build_item_matrix(rows)
    summary_rows = variant_summary(rows) + paired_summary(
        matrix,
        bootstrap=args.bootstrap,
        seed=args.seed,
    )
    fieldnames = [
        "metric",
        "label",
        "n",
        "correct",
        "accuracy",
        "ci95_low",
        "ci95_high",
        "candidate_only",
        "baseline_only",
        "both_correct",
        "both_wrong",
        "parsed_empty",
    ]
    item_fieldnames = ["id"]
    for variant in VARIANTS:
        item_fieldnames.extend(
            [
                f"{variant}_present",
                f"{variant}_correct",
                f"{variant}_parsed",
            ]
        )
    write_csv(summary_rows, summary_path, fieldnames)
    write_csv(matrix, items_path, item_fieldnames)
    write_report(
        title=args.title,
        input_path=input_path,
        summary_path=summary_path,
        items_path=items_path,
        report_path=report_path,
        summary_rows=summary_rows,
        bootstrap=args.bootstrap,
    )
    print(
        f"rows={len(rows)} items={len(matrix)} summary={summary_path} "
        f"items_csv={items_path} report={report_path}"
    )


if __name__ == "__main__":
    main()
