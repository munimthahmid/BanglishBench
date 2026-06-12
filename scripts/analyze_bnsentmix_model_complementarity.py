#!/usr/bin/env python3
"""Analyze model complementarity on the BnSentMix external-validation slice."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/bnsentmix_external_validation_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/bnsentmix_model_complementarity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/bnsentmix_model_complementarity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/bnsentmix_model_complementarity.md"
MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
LABELS = ("positive", "negative", "neutral", "mixed")
BOOTSTRAP_ITERATIONS = 5000
BOOTSTRAP_SEED = 20260603


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
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
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


def percent(count: int, denominator: int) -> str:
    return f"{100 * count / denominator:.1f}%" if denominator else "0.0%"


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def exact_binomial_cdf(k: int, n: int) -> float:
    if n <= 0:
        return 1.0
    return sum(math.comb(n, i) for i in range(k + 1)) / (2**n)


def exact_two_sided_pvalue(left_only: int, right_only: int) -> float:
    discordant = left_only + right_only
    if discordant == 0:
        return 1.0
    smaller = min(left_only, right_only)
    return min(1.0, 2.0 * exact_binomial_cdf(smaller, discordant))


def format_p(value: Any) -> str:
    p = float(value)
    if p < 0.0001:
        return "<0.0001"
    return f"{p:.4f}"


def load_item_rows(path: Path) -> list[dict[str, Any]]:
    rows = read_csv(path)
    by_id: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        model = row["model"]
        if model not in MODELS:
            continue
        by_id.setdefault(row["id"], {})[model] = row
    if not by_id:
        raise SystemExit(f"No BnSentMix rows found in {path}")

    out: list[dict[str, Any]] = []
    for item_id in sorted(by_id):
        model_rows = by_id[item_id]
        missing = [model for model in MODELS if model not in model_rows]
        if missing:
            raise SystemExit(f"{item_id} is missing model rows: {missing}")
        first = model_rows[MODELS[0]]
        gold = first["gold"]
        correct_flags = {model: truthy(model_rows[model]["correct"]) for model in MODELS}
        parsed = {model: model_rows[model]["parsed"] for model in MODELS}
        parsed_counts = Counter(parsed.values())
        majority_prediction = ""
        majority_count = 0
        if parsed_counts:
            majority_prediction, majority_count = parsed_counts.most_common(1)[0]
            if majority_count < 2:
                majority_prediction = ""
        correct_count = sum(int(correct_flags[model]) for model in MODELS)
        row: dict[str, Any] = {
            "id": item_id,
            "source_row": first["source_row"],
            "gold": gold,
            "correct_model_count": correct_count,
            "any_model_correct": correct_count > 0,
            "at_least_two_models_correct": correct_count >= 2,
            "all_models_correct": correct_count == len(MODELS),
            "all_models_wrong": correct_count == 0,
            "majority_prediction": majority_prediction,
            "majority_prediction_count": majority_count if majority_prediction else 0,
            "majority_prediction_correct": majority_prediction == gold if majority_prediction else False,
            "all_predictions_different": len(set(parsed.values())) == len(MODELS),
        }
        for model in MODELS:
            key = model.lower().replace(".", "").replace("-", "_").replace(" ", "_")
            row[f"{key}_parsed"] = parsed[model]
            row[f"{key}_correct"] = correct_flags[model]
        out.append(row)
    return out


def add(summary: list[dict[str, Any]], section: str, metric: str, **values: Any) -> None:
    summary.append({"section": section, "metric": metric, **values})


def model_key(model: str) -> str:
    return model.lower().replace(".", "").replace("-", "_").replace(" ", "_")


def build_summary_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    n = len(items)

    for model in MODELS:
        key = model_key(model)
        correct = sum(truthy(row[f"{key}_correct"]) for row in items)
        predictions = Counter(str(row[f"{key}_parsed"]) for row in items)
        add(
            summary,
            "model_headline",
            model,
            n=n,
            correct=correct,
            accuracy=f"{correct / n:.6f}",
            positive_predictions=predictions["positive"],
            negative_predictions=predictions["negative"],
            neutral_predictions=predictions["neutral"],
            mixed_predictions=predictions["mixed"],
        )

    count_distribution = Counter(int(row["correct_model_count"]) for row in items)
    for correct_count in range(len(MODELS) + 1):
        add(
            summary,
            "correct_count_distribution",
            str(correct_count),
            n=count_distribution[correct_count],
            denominator=n,
            rate=f"{count_distribution[correct_count] / n:.6f}",
        )

    any_correct = sum(truthy(row["any_model_correct"]) for row in items)
    at_least_two = sum(truthy(row["at_least_two_models_correct"]) for row in items)
    all_correct = sum(truthy(row["all_models_correct"]) for row in items)
    all_wrong = sum(truthy(row["all_models_wrong"]) for row in items)
    add(summary, "triad_oracle", "any_model_oracle", n=n, correct=any_correct, accuracy=f"{any_correct / n:.6f}")
    add(summary, "triad_oracle", "at_least_two_models_correct", n=n, correct=at_least_two, accuracy=f"{at_least_two / n:.6f}")
    add(summary, "triad_oracle", "all_models_correct", n=n, correct=all_correct, accuracy=f"{all_correct / n:.6f}")
    add(summary, "triad_oracle", "all_models_wrong", n=n, correct=all_wrong, accuracy=f"{all_wrong / n:.6f}")

    best_model = max(
        MODELS,
        key=lambda model: sum(truthy(row[f"{model_key(model)}_correct"]) for row in items),
    )
    best_key = model_key(best_model)
    observed, low, high, p_opposite = bootstrap_delta(
        [
            (
                truthy(row[f"{best_key}_correct"]),
                truthy(row["any_model_correct"]),
            )
            for row in items
        ],
        BOOTSTRAP_ITERATIONS,
        BOOTSTRAP_SEED,
    )
    add(
        summary,
        "triad_oracle",
        "oracle_minus_best_single",
        best_single_model=best_model,
        n=n,
        best_single_correct=sum(truthy(row[f"{best_key}_correct"]) for row in items),
        oracle_correct=any_correct,
        delta_oracle_minus_best_single=f"{observed:.6f}",
        ci95_low=f"{low:.6f}",
        ci95_high=f"{high:.6f}",
        bootstrap_p_opposite_direction=f"{p_opposite:.6f}",
    )

    majority_rows = [row for row in items if row["majority_prediction"]]
    majority_correct = sum(truthy(row["majority_prediction_correct"]) for row in majority_rows)
    add(
        summary,
        "majority_vote",
        "majority_only_abstain_on_three_way_disagreement",
        n=len(majority_rows),
        denominator=n,
        correct=majority_correct,
        coverage=f"{len(majority_rows) / n:.6f}",
        accuracy_on_covered=f"{majority_correct / len(majority_rows):.6f}" if majority_rows else "0.000000",
        accuracy_all_items_if_abstain_wrong=f"{majority_correct / n:.6f}",
    )
    for fallback_model in MODELS:
        fallback_key = model_key(fallback_model)
        correct = 0
        fallback_rows = 0
        for row in items:
            if row["majority_prediction"]:
                prediction = row["majority_prediction"]
            else:
                fallback_rows += 1
                prediction = row[f"{fallback_key}_parsed"]
            correct += prediction == row["gold"]
        pairs = [
            (
                truthy(row[f"{fallback_key}_correct"]),
                (
                    row["majority_prediction"] == row["gold"]
                    if row["majority_prediction"]
                    else truthy(row[f"{fallback_key}_correct"])
                ),
            )
            for row in items
        ]
        observed, low, high, p_opposite = bootstrap_delta(
            pairs, BOOTSTRAP_ITERATIONS, BOOTSTRAP_SEED + 17 + MODELS.index(fallback_model)
        )
        add(
            summary,
            "majority_vote",
            f"majority_with_{fallback_model}_fallback",
            fallback_model=fallback_model,
            n=n,
            correct=correct,
            accuracy=f"{correct / n:.6f}",
            fallback_rows=fallback_rows,
            delta_vs_fallback_model=f"{observed:.6f}",
            ci95_low=f"{low:.6f}",
            ci95_high=f"{high:.6f}",
            bootstrap_p_opposite_direction=f"{p_opposite:.6f}",
        )

    for idx, left in enumerate(MODELS):
        for right in MODELS[idx + 1 :]:
            left_key = model_key(left)
            right_key = model_key(right)
            left_correct = sum(truthy(row[f"{left_key}_correct"]) for row in items)
            right_correct = sum(truthy(row[f"{right_key}_correct"]) for row in items)
            both_correct = sum(
                truthy(row[f"{left_key}_correct"]) and truthy(row[f"{right_key}_correct"])
                for row in items
            )
            left_only = sum(
                truthy(row[f"{left_key}_correct"]) and not truthy(row[f"{right_key}_correct"])
                for row in items
            )
            right_only = sum(
                truthy(row[f"{right_key}_correct"]) and not truthy(row[f"{left_key}_correct"])
                for row in items
            )
            neither = n - both_correct - left_only - right_only
            prediction_agreement = sum(
                row[f"{left_key}_parsed"] == row[f"{right_key}_parsed"] for row in items
            )
            agreement_correct = sum(
                row[f"{left_key}_parsed"] == row[f"{right_key}_parsed"] == row["gold"]
                for row in items
            )
            pairs = [
                (truthy(row[f"{left_key}_correct"]), truthy(row[f"{right_key}_correct"]))
                for row in items
            ]
            observed, low, high, p_opposite = bootstrap_delta(
                pairs, BOOTSTRAP_ITERATIONS, BOOTSTRAP_SEED + 101 + idx
            )
            add(
                summary,
                "pairwise",
                f"{left} vs {right}",
                left_model=left,
                right_model=right,
                n=n,
                left_correct=left_correct,
                right_correct=right_correct,
                right_minus_left=f"{observed:.6f}",
                ci95_low=f"{low:.6f}",
                ci95_high=f"{high:.6f}",
                bootstrap_p_opposite_direction=f"{p_opposite:.6f}",
                left_only=left_only,
                right_only=right_only,
                both_correct=both_correct,
                neither_correct=neither,
                pair_oracle_correct=both_correct + left_only + right_only,
                prediction_agreement=prediction_agreement,
                agreement_correct=agreement_correct,
                exact_sign_p_two_sided=f"{exact_two_sided_pvalue(left_only, right_only):.6f}",
            )

    for label in LABELS:
        selected = [row for row in items if row["gold"] == label]
        add(
            summary,
            "label_oracle",
            label,
            n=len(selected),
            any_model_correct=sum(truthy(row["any_model_correct"]) for row in selected),
            at_least_two_models_correct=sum(truthy(row["at_least_two_models_correct"]) for row in selected),
            all_models_wrong=sum(truthy(row["all_models_wrong"]) for row in selected),
            all_models_correct=sum(truthy(row["all_models_correct"]) for row in selected),
        )

    return summary


def find(summary: list[dict[str, Any]], section: str, metric: str) -> dict[str, Any]:
    return next(row for row in summary if row["section"] == section and row["metric"] == metric)


def write_report(
    path: Path,
    input_path: Path,
    items_output: Path,
    summary_output: Path,
    summary: list[dict[str, Any]],
) -> None:
    model_rows = [row for row in summary if row["section"] == "model_headline"]
    pair_rows = [row for row in summary if row["section"] == "pairwise"]
    label_rows = [row for row in summary if row["section"] == "label_oracle"]
    majority_rows = [row for row in summary if row["section"] == "majority_vote"]
    oracle = find(summary, "triad_oracle", "any_model_oracle")
    oracle_delta = find(summary, "triad_oracle", "oracle_minus_best_single")
    count_rows = [row for row in summary if row["section"] == "correct_count_distribution"]
    lines = [
        "# BnSentMix Model Complementarity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend analysis asks whether the three BnSentMix model rows fail",
        "on the same natural code-mixed sentiment items, or whether their errors",
        "are complementary. It uses the existing 200-row balanced BnSentMix slice",
        "and the already completed Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B",
        "Kaggle outputs.",
        "",
        f"- Source item rows: `{repo_path(input_path)}`",
        f"- Complementarity items: `{repo_path(items_output)}`",
        f"- Complementarity summary: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        "| Result | Count | Interpretation |",
        "| --- | ---: | --- |",
        f"| Best single model | {oracle_delta['best_single_correct']}/{oracle_delta['n']} | {oracle_delta['best_single_model']} is the strongest single row. |",
        f"| Any-model oracle | {oracle['correct']}/{oracle['n']} | Diagnostic upper bound: at least one of the three models is correct. |",
        f"| Oracle minus best single | {points(oracle_delta['delta_oracle_minus_best_single'])} pts | CI [{points(oracle_delta['ci95_low'])}, {points(oracle_delta['ci95_high'])}]. |",
        "",
        "The natural code-mixed layer is therefore not just a single-model ranking:",
        "many items are recoverable by another model even when the strongest single",
        "row fails. This is diagnostic complementarity, not deployable accuracy.",
        "",
        "## Single Models",
        "",
        "| Model | Correct | Accuracy | Positive pred | Negative pred | Neutral pred | Mixed pred |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in model_rows:
        lines.append(
            f"| {row['metric']} | {row['correct']}/{row['n']} | "
            f"{percent(int(row['correct']), int(row['n']))} | "
            f"{row['positive_predictions']} | {row['negative_predictions']} | "
            f"{row['neutral_predictions']} | {row['mixed_predictions']} |"
        )
    lines.extend(
        [
            "",
            "## Correct-Model Count",
            "",
            "| Correct models on an item | Items |",
            "| ---: | ---: |",
        ]
    )
    for row in sorted(count_rows, key=lambda r: int(r["metric"])):
        lines.append(f"| {row['metric']} | {row['n']}/{row['denominator']} |")
    lines.extend(
        [
            "",
            "## Pairwise Complementarity",
            "",
            "| Pair | Left | Right | Delta right-left | Left only | Right only | Both correct | Neither | Pair oracle | Agreement correct | Sign p |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in pair_rows:
        lines.append(
            f"| {row['metric']} | {row['left_correct']}/{row['n']} | "
            f"{row['right_correct']}/{row['n']} | "
            f"{points(row['right_minus_left'])} pts "
            f"[{points(row['ci95_low'])}, {points(row['ci95_high'])}] | "
            f"{row['left_only']} | {row['right_only']} | {row['both_correct']} | "
            f"{row['neither_correct']} | {row['pair_oracle_correct']}/{row['n']} | "
            f"{row['agreement_correct']}/{row['prediction_agreement']} | "
            f"{format_p(row['exact_sign_p_two_sided'])} |"
        )
    lines.extend(
        [
            "",
            "## Majority Vote",
            "",
            "| Strategy | Correct | Detail |",
            "| --- | ---: | --- |",
        ]
    )
    for row in majority_rows:
        if row["metric"] == "majority_only_abstain_on_three_way_disagreement":
            lines.append(
                f"| Majority only | {row['correct']}/{row['n']} covered rows | "
                f"Covers {percent(int(row['n']), int(row['denominator']))}; "
                f"{100 * float(row['accuracy_on_covered']):.1f}% accuracy on covered rows. |"
            )
        else:
            lines.append(
                f"| {row['metric']} | {row['correct']}/{row['n']} | "
                f"Fallback rows {row['fallback_rows']}; delta vs fallback model "
                f"{points(row['delta_vs_fallback_model'])} pts "
                f"[{points(row['ci95_low'])}, {points(row['ci95_high'])}]. |"
            )
    lines.extend(
        [
            "",
            "## Label-Level Oracle Coverage",
            "",
            "| Gold label | Any model correct | At least two correct | All wrong | All correct |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in label_rows:
        lines.append(
            f"| {row['metric']} | {row['any_model_correct']}/{row['n']} | "
            f"{row['at_least_two_models_correct']}/{row['n']} | "
            f"{row['all_models_wrong']}/{row['n']} | "
            f"{row['all_models_correct']}/{row['n']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Contract",
            "",
            "- The any-model oracle is diagnostic. It uses gold labels to choose the",
            "  successful model after the fact and is not a deployable method.",
            "- Pairwise and majority-vote rows are behavioral evidence about error",
            "  overlap on the same natural items.",
            "- BnSentMix remains unpaired by script, so this report does not estimate",
            "  a Bangla-vs-Banglish script penalty.",
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
    items = load_item_rows(args.input)
    summary = build_summary_rows(items)
    write_csv(args.items_output, items)
    write_csv(args.summary_output, summary)
    write_report(args.report_output, args.input, args.items_output, args.summary_output, summary)
    print(f"items={len(items)}")
    print(f"summary_rows={len(summary)}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
