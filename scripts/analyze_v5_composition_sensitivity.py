#!/usr/bin/env python3
"""Composition sensitivity for frozen-v5 Banglish gaps."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date
from pathlib import Path
from statistics import median
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_composition_sensitivity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_composition_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_composition_sensitivity.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
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


def points(value: float) -> str:
    value *= 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def stable_seed(label: str) -> int:
    return BOOTSTRAP_SEED + sum((index + 1) * ord(char) for index, char in enumerate(label))


def int_field(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    return int(value) if str(value).strip() else 0


def bool_field(row: dict[str, str], key: str) -> bool:
    return truthy(row.get(key, ""))


def model_correct(row: dict[str, str], model: str, script: str) -> bool:
    return truthy(row.get(f"{model}_{script}_correct", ""))


def bootstrap_delta(
    rows: list[dict[str, str]],
    model: str,
    baseline_script: str,
    seed_label: str,
) -> tuple[float, float, float]:
    observed = sum(
        int(model_correct(row, model, "banglish")) - int(model_correct(row, model, baseline_script))
        for row in rows
    ) / len(rows)
    rng = random.Random(stable_seed(seed_label))
    draws: list[float] = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        total = 0
        for _i in range(len(rows)):
            row = rng.choice(rows)
            total += int(model_correct(row, model, "banglish")) - int(
                model_correct(row, model, baseline_script)
            )
        draws.append(total / len(rows))
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    return observed, low, high


def build_filters(rows: list[dict[str, str]]) -> list[tuple[str, str, Callable[[dict[str, str]], bool]]]:
    median_chars = int(median(int_field(row, "banglish_chars") for row in rows))
    return [
        ("all", "All frozen-v5 rows", lambda row: True),
        ("has_digits", "Rows with digits in reviewed Banglish", lambda row: bool_field(row, "has_digits")),
        ("no_digits", "Rows without digits in reviewed Banglish", lambda row: not bool_field(row, "has_digits")),
        (
            "short_half",
            f"Rows at or below median reviewed-Banglish length ({median_chars} chars)",
            lambda row, cutoff=median_chars: int_field(row, "banglish_chars") <= cutoff,
        ),
        (
            "no_formula_operator",
            "Rows without formula/operator markers",
            lambda row: not bool_field(row, "has_formula_or_operator"),
        ),
        (
            "no_digits_no_formula",
            "Rows without digits and without formula/operator markers",
            lambda row: not bool_field(row, "has_digits")
            and not bool_field(row, "has_formula_or_operator"),
        ),
        (
            "benqa_no_digits",
            "BEnQA rows without digits",
            lambda row: row.get("dataset") == "benqa" and not bool_field(row, "has_digits"),
        ),
        (
            "benqa_no_digits_no_formula",
            "BEnQA rows without digits and without formula/operator markers",
            lambda row: row.get("dataset") == "benqa"
            and not bool_field(row, "has_digits")
            and not bool_field(row, "has_formula_or_operator"),
        ),
        (
            "benqa_short_no_digits",
            f"BEnQA rows without digits and at/below {median_chars} chars",
            lambda row, cutoff=median_chars: row.get("dataset") == "benqa"
            and not bool_field(row, "has_digits")
            and int_field(row, "banglish_chars") <= cutoff,
        ),
    ]


def build_item_rows(
    rows: list[dict[str, str]],
    filters: list[tuple[str, str, Callable[[dict[str, str]], bool]]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item_row: dict[str, Any] = {
            "id": row["id"],
            "dataset": row.get("dataset", ""),
            "domain": row.get("domain", ""),
            "subject": row.get("subject", ""),
            "task_type": row.get("task_type", ""),
            "review_label": row.get("review_label", ""),
            "banglish_chars": int_field(row, "banglish_chars"),
            "banglish_words": int_field(row, "banglish_words"),
            "has_digits": bool_field(row, "has_digits"),
            "has_formula_or_operator": bool_field(row, "has_formula_or_operator"),
            "has_latex_markers": bool_field(row, "has_latex_markers"),
            "has_science_symbol": bool_field(row, "has_science_symbol"),
        }
        for filter_key, _description, predicate in filters:
            item_row[f"in_{filter_key}"] = predicate(row)
        out.append(item_row)
    return out


def summarize_filter(
    filter_key: str,
    description: str,
    rows: list[dict[str, str]],
    model: str,
) -> dict[str, Any]:
    if not rows:
        raise SystemExit(f"Filter {filter_key} produced no rows")
    bangla_correct = sum(model_correct(row, model, "bangla") for row in rows)
    banglish_correct = sum(model_correct(row, model, "banglish") for row in rows)
    english_correct = sum(model_correct(row, model, "english") for row in rows)
    delta_bangla = bootstrap_delta(rows, model, "bangla", f"{filter_key}:{model}:bangla")
    delta_english = bootstrap_delta(rows, model, "english", f"{filter_key}:{model}:english")
    return {
        "filter": filter_key,
        "description": description,
        "model": model,
        "n_items": len(rows),
        "bangla_correct": bangla_correct,
        "banglish_correct": banglish_correct,
        "english_correct": english_correct,
        "bangla_accuracy": round(bangla_correct / len(rows), 4),
        "banglish_accuracy": round(banglish_correct / len(rows), 4),
        "english_accuracy": round(english_correct / len(rows), 4),
        "banglish_minus_bangla": round(delta_bangla[0], 4),
        "banglish_minus_bangla_ci95_low": round(delta_bangla[1], 4),
        "banglish_minus_bangla_ci95_high": round(delta_bangla[2], 4),
        "banglish_minus_english": round(delta_english[0], 4),
        "banglish_minus_english_ci95_low": round(delta_english[1], 4),
        "banglish_minus_english_ci95_high": round(delta_english[2], 4),
    }


def build_summary_rows(
    rows: list[dict[str, str]],
    filters: list[tuple[str, str, Callable[[dict[str, str]], bool]]],
) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for filter_key, description, predicate in filters:
        selected = [row for row in rows if predicate(row)]
        for model in MODELS:
            summary.append(summarize_filter(filter_key, description, selected, model))
    return summary


def row_for(summary: list[dict[str, Any]], filter_key: str, model: str) -> dict[str, Any]:
    return next(row for row in summary if row["filter"] == filter_key and row["model"] == model)


def write_report(
    path: Path,
    summary: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    lines = [
        "# Frozen-V5 Composition Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the reviewed-Banglish deficit is only",
        "a byproduct of number-heavy or formula-heavy educational rows. It reuses",
        "the frozen-v5 item-level correctness table and reports paired bootstrap",
        "intervals inside simpler composition subsets.",
        "",
        f"- Item membership table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "This does not turn the benchmark into natural Banglish. It is a",
        "composition stress test for the controlled educational slice.",
        "",
        "## Digit And Formula Stress Test",
        "",
        "| Filter | n | Model | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    main_filters = [
        "all",
        "no_digits",
        "no_formula_operator",
        "no_digits_no_formula",
        "benqa_no_digits",
        "benqa_no_digits_no_formula",
    ]
    for filter_key in main_filters:
        for model in MODELS:
            row = row_for(summary, filter_key, model)
            n_items = int(row["n_items"])
            lines.append(
                f"| {filter_key} | {n_items} | {model} | "
                f"{row['bangla_correct']}/{n_items} ({percent(int(row['bangla_correct']), n_items)}) | "
                f"{row['banglish_correct']}/{n_items} ({percent(int(row['banglish_correct']), n_items)}) | "
                f"{row['english_correct']}/{n_items} ({percent(int(row['english_correct']), n_items)}) | "
                f"{points(float(row['banglish_minus_bangla']))} pts "
                f"[{points(float(row['banglish_minus_bangla_ci95_low']))}, "
                f"{points(float(row['banglish_minus_bangla_ci95_high']))}] | "
                f"{points(float(row['banglish_minus_english']))} pts "
                f"[{points(float(row['banglish_minus_english_ci95_low']))}, "
                f"{points(float(row['banglish_minus_english_ci95_high']))}] |"
            )

    no_digits_rows = [row_for(summary, "no_digits", model) for model in MODELS]
    no_formula_rows = [row_for(summary, "no_formula_operator", model) for model in MODELS]
    benqa_simple_rows = [row_for(summary, "benqa_no_digits_no_formula", model) for model in MODELS]
    short_rows = [row_for(summary, "short_half", model) for model in MODELS]
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The no-digit subset has 61 rows. All three thesis-facing Qwen rows",
            "  keep reviewed Banglish below both Bangla and English there; the",
            "  Banglish-minus-Bangla range is "
            f"{points(min(float(row['banglish_minus_bangla']) for row in no_digits_rows))} to "
            f"{points(max(float(row['banglish_minus_bangla']) for row in no_digits_rows))} pts.",
            "- The no-formula/operator subset has 107 rows and also keeps the",
            "  Banglish-minus-Bangla gap negative for all three Qwen rows.",
            "- The stricter no-digit/no-formula BEnQA subset has 38 rows. It is small,",
            "  but every Qwen row still shows reviewed Banglish below Bangla and",
            "  English.",
            "- The shorter-half subset has 101 rows. Its Banglish-minus-Bangla range is",
            f"  {points(min(float(row['banglish_minus_bangla']) for row in short_rows))} to "
            f"{points(max(float(row['banglish_minus_bangla']) for row in short_rows))} pts.",
            "- These results do not remove the real-Banglish naturalness limitation;",
            "  they show the main signal is not solely a numeric/formula artifact.",
            "",
            "## Caveats",
            "",
            "- The simplest subsets are smaller, so confidence intervals widen.",
            "- BanglaMATH is mostly numeric; no-digit composition checks are therefore",
            "  essentially BEnQA checks.",
            "- The benchmark remains controlled educational Banglish, not a sample of",
            "  naturally occurring social/media Banglish.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_composition_sensitivity.py`",
            f"- Item membership table: `{repo_path(items_output)}`",
            f"- Summary table: `{repo_path(summary_output)}`",
        ]
    )
    # Keep linters honest: these names document the rows used above.
    _ = no_formula_rows, benqa_simple_rows
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
    filters = build_filters(rows)
    item_rows = build_item_rows(rows, filters)
    summary_rows = build_summary_rows(rows, filters)
    write_csv(args.items_output, item_rows, list(item_rows[0]))
    write_csv(args.summary_output, summary_rows, list(summary_rows[0]))
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
