#!/usr/bin/env python3
"""Audit whether BEnQA D-collapse follows option lexical coverage."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
from typing import Any, Callable

import analyze_v5_benqa_option_lexical_coverage as lexical


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_option_coverage_confound_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_option_coverage_confound_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_coverage_confound.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
OPTIONS = ("A", "B", "C", "D")
BucketPredicate = Callable[[dict[str, Any]], bool]


BUCKETS: tuple[tuple[str, str, BucketPredicate], ...] = (
    ("overall", "All BEnQA rows", lambda row: True),
    (
        "all_options_same_coverage",
        "All four options have identical exact BanglaTLit coverage",
        lambda row: bool(row["all_options_same_coverage"]),
    ),
    (
        "d_among_highest_coverage",
        "D is among the highest-coverage options",
        lambda row: bool(row["d_among_highest_coverage"]),
    ),
    (
        "d_not_highest_coverage",
        "At least one option has higher exact coverage than D",
        lambda row: bool(row["d_not_highest_coverage"]),
    ),
    (
        "d_among_lowest_coverage",
        "D is among the lowest-coverage options",
        lambda row: bool(row["d_among_lowest_coverage"]),
    ),
    (
        "d_not_lowest_coverage",
        "At least one option has lower exact coverage than D",
        lambda row: bool(row["d_not_lowest_coverage"]),
    ),
    (
        "d_strict_highest_coverage",
        "D has strictly higher exact coverage than A/B/C",
        lambda row: bool(row["d_strict_highest_coverage"]),
    ),
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
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
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


def parse_option_texts(text: str, item_id: str) -> dict[str, str]:
    options: dict[str, str] = {}
    for line in text.splitlines():
        match = lexical.OPTION_RE.match(line.strip())
        if match:
            options[match.group(1)] = match.group(2)
    if set(options) != set(OPTIONS):
        raise SystemExit(f"Could not parse four BEnQA options for {item_id}")
    return options


def load_option_features(validation: Path, banglatlit_paths: list[Path]) -> dict[str, dict[str, Any]]:
    vocab, _rows = lexical.build_banglatlit_vocab(banglatlit_paths)
    features: dict[str, dict[str, Any]] = {}
    with validation.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("dataset") != "benqa":
                continue
            item_id = str(row["id"])
            option_texts = parse_option_texts(str(row.get("banglish_clean", "")), item_id)
            coverage: dict[str, float] = {}
            token_counts: dict[str, int] = {}
            seen_counts: dict[str, int] = {}
            for option in OPTIONS:
                surface = lexical.surface_features(option_texts[option], vocab)
                coverage[option] = float(surface["coverage"])
                token_counts[option] = int(surface["token_count"])
                seen_counts[option] = int(surface["seen_token_count"])
            max_coverage = max(coverage.values())
            min_coverage = min(coverage.values())
            higher_than_d = sum(coverage[option] > coverage["D"] for option in ("A", "B", "C"))
            lower_than_d = sum(coverage[option] < coverage["D"] for option in ("A", "B", "C"))
            highest_options = tuple(option for option in OPTIONS if coverage[option] == max_coverage)
            lowest_options = tuple(option for option in OPTIONS if coverage[option] == min_coverage)
            features[item_id] = {
                "gold": str(row.get("answer", "")),
                "highest_coverage_options": ";".join(highest_options),
                "lowest_coverage_options": ";".join(lowest_options),
                "max_option_coverage": round(max_coverage, 4),
                "min_option_coverage": round(min_coverage, 4),
                "d_coverage": round(coverage["D"], 4),
                "d_coverage_rank": 1 + higher_than_d,
                "d_among_highest_coverage": coverage["D"] == max_coverage,
                "d_not_highest_coverage": higher_than_d > 0,
                "d_among_lowest_coverage": coverage["D"] == min_coverage,
                "d_not_lowest_coverage": lower_than_d > 0,
                "d_strict_highest_coverage": lower_than_d == 3,
                "all_options_same_coverage": len(set(coverage.values())) == 1,
                **{f"{option}_coverage": round(coverage[option], 4) for option in OPTIONS},
                **{f"{option}_token_count": token_counts[option] for option in OPTIONS},
                **{f"{option}_seen_token_count": seen_counts[option] for option in OPTIONS},
            }
    if len(features) != 144:
        raise SystemExit(f"Expected 144 BEnQA feature rows, got {len(features)}")
    return features


def build_item_rows(choice_items: Path, option_features: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    choice_rows = read_csv(choice_items)
    if len(choice_rows) != len(MODELS) * 144:
        raise SystemExit(f"Expected {len(MODELS) * 144} choice-bias rows, got {len(choice_rows)}")

    rows: list[dict[str, Any]] = []
    for row in choice_rows:
        item_id = row["id"]
        if item_id not in option_features:
            raise SystemExit(f"Missing option-coverage features for {item_id}")
        pred = row["banglish_clean_parsed_option"]
        correct = truthy(row["banglish_clean_correct"])
        rows.append(
            {
                "model": row["model"],
                "id": item_id,
                "gold": row["gold"],
                "banglish_option": pred,
                "banglish_correct": correct,
                "banglish_D": pred == "D",
                "banglish_wrong_D": pred == "D" and not correct,
                "banglish_invalid": pred == "invalid",
                **option_features[item_id],
            }
        )
    return rows


def summarize_bucket(
    model: str,
    bucket: str,
    bucket_label: str,
    selected: list[dict[str, Any]],
) -> dict[str, Any]:
    n = len(selected)
    return {
        "section": "coverage_bucket",
        "model": model,
        "bucket": bucket,
        "bucket_label": bucket_label,
        "n": n,
        "gold_D": sum(row["gold"] == "D" for row in selected),
        "banglish_correct": sum(bool(row["banglish_correct"]) for row in selected),
        "banglish_D": sum(bool(row["banglish_D"]) for row in selected),
        "banglish_wrong_D": sum(bool(row["banglish_wrong_D"]) for row in selected),
        "banglish_invalid": sum(bool(row["banglish_invalid"]) for row in selected),
        "mean_D_coverage": round(sum(float(row["d_coverage"]) for row in selected) / n, 4)
        if n
        else 0.0,
        "mean_max_option_coverage": round(
            sum(float(row["max_option_coverage"]) for row in selected) / n, 4
        )
        if n
        else 0.0,
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [row for row in item_rows if row["model"] == model]
        for bucket, bucket_label, predicate in BUCKETS:
            selected = [row for row in model_rows if predicate(row)]
            rows.append(summarize_bucket(model, bucket, bucket_label, selected))
    return rows


def row_for(rows: list[dict[str, Any]], model: str, bucket: str) -> dict[str, Any]:
    matches = [row for row in rows if row["model"] == model and row["bucket"] == bucket]
    if len(matches) != 1:
        raise SystemExit(f"Expected one summary row for {model} {bucket}, got {len(matches)}")
    return matches[0]


def bucket_line(row: dict[str, Any]) -> str:
    return (
        f"| {row['model']} | {row['bucket']} | {row['n']} | "
        f"{row['gold_D']} | {row['banglish_D']} | {row['banglish_wrong_D']} | "
        f"{row['banglish_correct']} | {row['mean_D_coverage']} |"
    )


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_tie = row_for(summary_rows, "Qwen3-4B", "all_options_same_coverage")
    q25_3b_tie = row_for(summary_rows, "Qwen2.5-3B", "all_options_same_coverage")
    q25_7b_tie = row_for(summary_rows, "Qwen2.5-7B 8-bit", "all_options_same_coverage")
    q3_not_highest = row_for(summary_rows, "Qwen3-4B", "d_not_highest_coverage")
    q25_3b_not_highest = row_for(summary_rows, "Qwen2.5-3B", "d_not_highest_coverage")
    q25_7b_not_highest = row_for(summary_rows, "Qwen2.5-7B 8-bit", "d_not_highest_coverage")
    q3_strict_highest = row_for(summary_rows, "Qwen3-4B", "d_strict_highest_coverage")

    lines = [
        "# Frozen-V5 BEnQA Option-Coverage Confound Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether Qwen3-4B's reviewed-Banglish BEnQA",
        "D-attractor can be reduced to choosing the most lexically familiar",
        "answer option. It reuses the exact BanglaTLit vocabulary and tokenizer",
        "from the BEnQA option-lexical coverage audit, computes per-option",
        "coverage for A/B/C/D, and joins those features to frozen-v5 choice-bias",
        "rows.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- On rows where all four options have identical exact BanglaTLit "
            f"coverage, Qwen3-4B still predicts D on {q3_tie['banglish_D']}/"
            f"{q3_tie['n']} rows ({percent(int(q3_tie['banglish_D']), int(q3_tie['n']))}) "
            f"and wrong D on {q3_tie['banglish_wrong_D']}/{q3_tie['n']}."
        ),
        (
            "- The corresponding Qwen2.5 D counts in the same tied-coverage bucket "
            f"are {q25_3b_tie['banglish_D']}/{q25_3b_tie['n']} and "
            f"{q25_7b_tie['banglish_D']}/{q25_7b_tie['n']}."
        ),
        (
            "- When at least one option has higher exact coverage than D, Qwen3-4B "
            f"still predicts D on {q3_not_highest['banglish_D']}/{q3_not_highest['n']} "
            f"rows and wrong D on {q3_not_highest['banglish_wrong_D']}/"
            f"{q3_not_highest['n']}."
        ),
        (
            "- Qwen2.5 rows in that not-highest-D bucket predict D on "
            f"{q25_3b_not_highest['banglish_D']}/{q25_3b_not_highest['n']} and "
            f"{q25_7b_not_highest['banglish_D']}/{q25_7b_not_highest['n']} rows."
        ),
        (
            "- Only three items have D as a strictly highest-coverage option; Qwen3 "
            f"predicts D on {q3_strict_highest['banglish_D']}/"
            f"{q3_strict_highest['n']} of them."
        ),
        "",
        "## Bucket Summary",
        "",
        "| Model | Bucket | Rows | Gold D | Pred D | Wrong D | Correct | Mean D coverage |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for bucket, _bucket_label, _predicate in BUCKETS:
        for model in MODELS:
            lines.append(bucket_line(row_for(summary_rows, model, bucket)))

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Exact BanglaTLit option coverage is too tie-heavy to explain the D-attractor",
            "  as a simple highest-coverage-option heuristic.",
            "- The strongest slice is the 101-item tied-coverage bucket: option lexical",
            "  familiarity supplies no A/B/C/D distinction, but Qwen3 still collapses",
            "  toward D while Qwen2.5 does not.",
            "- This remains behavioral evidence over exact lexical overlap. It does not",
            "  identify the internal mechanism behind the Qwen3 failure mode.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--banglatlit", type=Path, nargs="+", default=lexical.DEFAULT_BANGLATLIT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    option_features = load_option_features(args.validation, args.banglatlit)
    item_rows = build_item_rows(args.choice_items, option_features)
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report, summary_rows, args.items_output, args.summary_output)

    q3_tie = row_for(summary_rows, "Qwen3-4B", "all_options_same_coverage")
    q3_not_highest = row_for(summary_rows, "Qwen3-4B", "d_not_highest_coverage")
    print(
        "items="
        f"{len(item_rows)} summary_rows={len(summary_rows)} "
        f"qwen3_tied_coverage_D={q3_tie['banglish_D']}/{q3_tie['n']} "
        f"qwen3_D_not_highest_coverage={q3_not_highest['banglish_D']}/{q3_not_highest['n']} "
        f"report={args.report}"
    )


if __name__ == "__main__":
    main()
