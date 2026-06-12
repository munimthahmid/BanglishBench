#!/usr/bin/env python3
"""Audit wrong-option transitions for frozen-v5 BEnQA Banglish misses."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_distractor_transition_items.csv"
DEFAULT_CONSENSUS_OUTPUT = ROOT / "results/analysis/v5_benqa_distractor_transition_item_consensus.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_distractor_transition_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_distractor_transition.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
OPTIONS = ("A", "B", "C", "D")


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


def option(value: Any) -> str:
    value = str(value).strip().upper()
    return value if value in OPTIONS else "invalid"


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def load_rows(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    expected = len(MODELS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} BEnQA choice-bias rows, got {len(rows)}")
    return rows


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        bangla_correct = truthy(row["bangla_correct"])
        banglish_correct = truthy(row["banglish_clean_correct"])
        english_correct = truthy(row["english_correct"])
        banglish_option = option(row["banglish_clean_parsed_option"])
        alternate_correct_count = int(bangla_correct) + int(english_correct)
        recoverable = (not banglish_correct) and alternate_correct_count > 0
        valid_recoverable = recoverable and banglish_option != "invalid"
        out.append(
            {
                "model": row["model"],
                "id": row["id"],
                "gold": option(row["gold"]),
                "bangla_option": option(row["bangla_parsed_option"]),
                "banglish_option": banglish_option,
                "english_option": option(row["english_parsed_option"]),
                "bangla_correct": bangla_correct,
                "banglish_correct": banglish_correct,
                "english_correct": english_correct,
                "alternate_correct_count": alternate_correct_count,
                "recoverable_banglish_miss": recoverable,
                "strict_recoverable_banglish_miss": recoverable and alternate_correct_count == 2,
                "valid_recoverable_banglish_miss": valid_recoverable,
                "invalid_recoverable_banglish_miss": recoverable and banglish_option == "invalid",
                "wrong_transition": f"{option(row['gold'])}->{banglish_option}"
                if valid_recoverable
                else "",
                "banglish_matches_bangla_option": banglish_option == option(row["bangla_parsed_option"]),
                "banglish_matches_english_option": banglish_option == option(row["english_parsed_option"]),
            }
        )
    return out


def build_consensus_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in item_rows:
        grouped[str(row["id"])].append(row)

    out: list[dict[str, Any]] = []
    for item_id in sorted(grouped):
        rows = grouped[item_id]
        if len(rows) != len(MODELS):
            raise SystemExit(f"Expected {len(MODELS)} model rows for {item_id}, got {len(rows)}")
        valid_recoverable = [row for row in rows if row["valid_recoverable_banglish_miss"]]
        wrong_counts = Counter(row["banglish_option"] for row in valid_recoverable)
        top_wrong, top_count = ("", 0)
        if wrong_counts:
            top_wrong, top_count = wrong_counts.most_common(1)[0]
        bangla_correct_count = sum(row["bangla_correct"] for row in rows)
        banglish_correct_count = sum(row["banglish_correct"] for row in rows)
        english_correct_count = sum(row["english_correct"] for row in rows)
        alternate_best_correct_count = max(bangla_correct_count, english_correct_count)
        out.append(
            {
                "id": item_id,
                "gold": rows[0]["gold"],
                "bangla_correct_models": bangla_correct_count,
                "banglish_correct_models": banglish_correct_count,
                "english_correct_models": english_correct_count,
                "alternate_best_correct_models": alternate_best_correct_count,
                "recoverable_banglish_miss_models": sum(
                    row["recoverable_banglish_miss"] for row in rows
                ),
                "valid_recoverable_banglish_miss_models": len(valid_recoverable),
                "top_recoverable_wrong_option": top_wrong,
                "top_recoverable_wrong_count": top_count,
                "two_plus_models_same_wrong_option": top_count >= 2,
                "all_three_models_same_wrong_option": top_count == 3,
                "strong_alternate_low_banglish": (
                    alternate_best_correct_count >= 2 and banglish_correct_count <= 1
                ),
                "zero_banglish_strong_alternate": (
                    alternate_best_correct_count >= 2 and banglish_correct_count == 0
                ),
                "wrong_option_counts": ";".join(
                    f"{choice}:{wrong_counts[choice]}" for choice in OPTIONS if wrong_counts[choice]
                ),
            }
        )
    return out


def add_summary(
    rows: list[dict[str, Any]],
    section: str,
    model: str = "",
    bucket: str = "",
    gold: str = "",
    n: int = 0,
    denominator: int = 0,
    recoverable_misses: int = 0,
    strict_recoverable_misses: int = 0,
    valid_recoverable_misses: int = 0,
    invalid_recoverable_misses: int = 0,
    pred_counts: Counter[str] | None = None,
    repeated_wrong_option_items: int = 0,
    all_three_same_wrong_option_items: int = 0,
    detail: str = "",
) -> None:
    pred_counts = pred_counts or Counter()
    top_wrong, top_wrong_count = ("", 0)
    valid_counts = Counter({choice: pred_counts[choice] for choice in OPTIONS})
    if sum(valid_counts.values()):
        top_wrong, top_wrong_count = valid_counts.most_common(1)[0]
    rows.append(
        {
            "section": section,
            "model": model,
            "bucket": bucket,
            "gold": gold,
            "n": n,
            "denominator": denominator,
            "rate": round(n / denominator, 4) if denominator else "",
            "recoverable_misses": recoverable_misses,
            "strict_recoverable_misses": strict_recoverable_misses,
            "valid_recoverable_misses": valid_recoverable_misses,
            "invalid_recoverable_misses": invalid_recoverable_misses,
            "pred_A": pred_counts["A"],
            "pred_B": pred_counts["B"],
            "pred_C": pred_counts["C"],
            "pred_D": pred_counts["D"],
            "pred_invalid": pred_counts["invalid"],
            "top_wrong_option": top_wrong,
            "top_wrong_count": top_wrong_count,
            "repeated_wrong_option_items": repeated_wrong_option_items,
            "all_three_same_wrong_option_items": all_three_same_wrong_option_items,
            "detail": detail,
        }
    )


def build_summary_rows(
    item_rows: list[dict[str, Any]], consensus_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for model in MODELS:
        rows = [row for row in item_rows if row["model"] == model]
        recoverable = [row for row in rows if row["recoverable_banglish_miss"]]
        valid_recoverable = [row for row in recoverable if row["valid_recoverable_banglish_miss"]]
        add_summary(
            summary,
            section="model_overall",
            model=model,
            bucket="all_recoverable",
            n=len(valid_recoverable),
            denominator=len(recoverable),
            recoverable_misses=len(recoverable),
            strict_recoverable_misses=sum(row["strict_recoverable_banglish_miss"] for row in rows),
            valid_recoverable_misses=len(valid_recoverable),
            invalid_recoverable_misses=sum(row["invalid_recoverable_banglish_miss"] for row in rows),
            pred_counts=Counter(row["banglish_option"] for row in recoverable),
            detail="Reviewed-Banglish wrong while Bangla or English is correct",
        )
        for gold in OPTIONS:
            gold_recoverable = [row for row in recoverable if row["gold"] == gold]
            add_summary(
                summary,
                section="model_gold_transition",
                model=model,
                bucket="recoverable_by_gold",
                gold=gold,
                n=len(gold_recoverable),
                denominator=len(recoverable),
                recoverable_misses=len(gold_recoverable),
                strict_recoverable_misses=sum(
                    row["strict_recoverable_banglish_miss"] for row in gold_recoverable
                ),
                valid_recoverable_misses=sum(
                    row["valid_recoverable_banglish_miss"] for row in gold_recoverable
                ),
                invalid_recoverable_misses=sum(
                    row["invalid_recoverable_banglish_miss"] for row in gold_recoverable
                ),
                pred_counts=Counter(row["banglish_option"] for row in gold_recoverable),
                detail=f"Gold {gold} recoverable Banglish misses",
            )

    for bucket, selected in (
        (
            "any_model_recoverable_valid",
            [
                row
                for row in consensus_rows
                if int(row["valid_recoverable_banglish_miss_models"]) >= 1
            ],
        ),
        (
            "two_plus_models_recoverable_valid",
            [
                row
                for row in consensus_rows
                if int(row["valid_recoverable_banglish_miss_models"]) >= 2
            ],
        ),
        (
            "three_models_recoverable_valid",
            [
                row
                for row in consensus_rows
                if int(row["valid_recoverable_banglish_miss_models"]) == 3
            ],
        ),
    ):
        add_summary(
            summary,
            section="cross_model_convergence",
            bucket=bucket,
            n=len(selected),
            denominator=len(consensus_rows),
            repeated_wrong_option_items=sum(row["two_plus_models_same_wrong_option"] for row in selected),
            all_three_same_wrong_option_items=sum(
                row["all_three_models_same_wrong_option"] for row in selected
            ),
            detail="BEnQA items with valid recoverable Banglish misses across models",
        )

    for bucket, selected in (
        (
            "strong_alternate_low_banglish",
            [row for row in consensus_rows if row["strong_alternate_low_banglish"]],
        ),
        (
            "zero_banglish_strong_alternate",
            [row for row in consensus_rows if row["zero_banglish_strong_alternate"]],
        ),
    ):
        add_summary(
            summary,
            section="item_support_bucket",
            bucket=bucket,
            n=len(selected),
            denominator=len(consensus_rows),
            repeated_wrong_option_items=sum(row["two_plus_models_same_wrong_option"] for row in selected),
            all_three_same_wrong_option_items=sum(
                row["all_three_models_same_wrong_option"] for row in selected
            ),
            detail="Cross-model alternate-script support with low Banglish success",
        )

    return summary


def row_for(summary: list[dict[str, Any]], section: str, **criteria: str) -> dict[str, Any]:
    for row in summary:
        if row["section"] != section:
            continue
        if all(str(row.get(key, "")) == value for key, value in criteria.items()):
            return row
    raise KeyError((section, criteria))


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    consensus_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    consensus_output: Path,
    summary_output: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    model_rows = [row for row in summary_rows if row["section"] == "model_overall"]
    total_recoverable = sum(int(row["recoverable_misses"]) for row in model_rows)
    total_valid = sum(int(row["valid_recoverable_misses"]) for row in model_rows)
    total_invalid = sum(int(row["invalid_recoverable_misses"]) for row in model_rows)
    qwen3 = row_for(summary_rows, "model_overall", model="Qwen3-4B")
    two_plus = row_for(
        summary_rows,
        "cross_model_convergence",
        bucket="two_plus_models_recoverable_valid",
    )
    three = row_for(
        summary_rows,
        "cross_model_convergence",
        bucket="three_models_recoverable_valid",
    )

    lines = [
        "# Frozen-V5 BEnQA Distractor-Transition Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit extends the BEnQA choice-bias analysis by asking",
        "what reviewed Banglish predicts when it is wrong even though Bangla or",
        "English is correct. It uses only the frozen-v5 BEnQA MCQ rows and the",
        "three thesis-facing Qwen models.",
        "",
        f"- Per-model item table: `{repo_path(items_output)}`",
        f"- Cross-model item table: `{repo_path(consensus_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            f"- Recoverable reviewed-Banglish BEnQA misses are almost always valid "
            f"distractor choices: {total_valid}/{total_recoverable} valid, "
            f"with {total_invalid} invalid choices."
        ),
        (
            "- Qwen2.5 rows do not collapse to one distractor label: their most "
            "common recoverable wrong option is B, but it accounts for "
            f"{row_for(summary_rows, 'model_overall', model='Qwen2.5-3B')['top_wrong_count']}/"
            f"{row_for(summary_rows, 'model_overall', model='Qwen2.5-3B')['recoverable_misses']} "
            "and "
            f"{row_for(summary_rows, 'model_overall', model='Qwen2.5-7B 8-bit')['top_wrong_count']}/"
            f"{row_for(summary_rows, 'model_overall', model='Qwen2.5-7B 8-bit')['recoverable_misses']} "
            "recoverable misses."
        ),
        (
            "- Qwen3-4B has a much sharper script-conditioned distractor mode: "
            f"D is selected on {qwen3['pred_D']}/{qwen3['recoverable_misses']} "
            "recoverable reviewed-Banglish misses."
        ),
        (
            "- Cross-model convergence is nontrivial: "
            f"{two_plus['n']} items have at least two valid recoverable Banglish "
            f"misses, and {two_plus['repeated_wrong_option_items']} of them share "
            "the same wrong option across at least two models."
        ),
        (
            f"- {three['n']} items have all three models making valid recoverable "
            f"Banglish misses; {three['all_three_same_wrong_option_items']} choose "
            "the same wrong option across all three models."
        ),
        "",
        "## Recoverable Misses By Model",
        "",
        "| Model | Recoverable misses | Valid distractors | Invalid | Top wrong option | Pred A | Pred B | Pred C | Pred D |",
        "| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in model_rows:
        lines.append(
            "| {model} | {recoverable_misses} | {valid_recoverable_misses} | "
            "{invalid_recoverable_misses} | {top_wrong_option} "
            "({top_wrong_count}) | {pred_A} | {pred_B} | {pred_C} | {pred_D} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Gold-To-Wrong Transitions",
            "",
            "| Model | Gold | Recoverable misses | Pred A | Pred B | Pred C | Pred D | Invalid | Top wrong option |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in [row for row in summary_rows if row["section"] == "model_gold_transition"]:
        lines.append(
            "| {model} | {gold} | {recoverable_misses} | {pred_A} | {pred_B} | "
            "{pred_C} | {pred_D} | {pred_invalid} | {top_wrong_option} "
            "({top_wrong_count}) |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Cross-Model Wrong-Option Convergence",
            "",
            "| Bucket | Items | Repeated wrong option | All-three same wrong option |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in [row for row in summary_rows if row["section"] == "cross_model_convergence"]:
        lines.append(
            "| `{bucket}` | {n}/{denominator} | {repeated_wrong_option_items} | "
            "{all_three_same_wrong_option_items} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The BEnQA script gap is not mainly an MCQ parser artifact. When reviewed",
            "Banglish loses items that Bangla or English can answer, it usually still",
            "emits a valid option label. For Qwen2.5 models the wrong choices remain",
            "distributed, so the gap cannot be reduced to a single label prior. For",
            "Qwen3-4B, the reviewed-Banglish row has a sharp D-attractor failure mode,",
            "which is itself a script-conditioned behavior.",
            "",
            "The cross-model convergence counts show that some BEnQA items pull more",
            "than one model toward the same wrong distractor under Banglish. Treat this",
            "as behavioral evidence of script-conditioned distractor attraction, not as",
            "a causal mechanism for internal representations.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_benqa_distractor_transition.py`",
            f"- Per-model item rows: {len(item_rows)}",
            f"- Cross-model item rows: {len(consensus_rows)}",
            f"- Summary rows: {len(summary_rows)}",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--consensus-output", type=Path, default=DEFAULT_CONSENSUS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_rows(args.input)
    item_rows = build_item_rows(rows)
    consensus_rows = build_consensus_rows(item_rows)
    summary_rows = build_summary_rows(item_rows, consensus_rows)

    item_fields = [
        "model",
        "id",
        "gold",
        "bangla_option",
        "banglish_option",
        "english_option",
        "bangla_correct",
        "banglish_correct",
        "english_correct",
        "alternate_correct_count",
        "recoverable_banglish_miss",
        "strict_recoverable_banglish_miss",
        "valid_recoverable_banglish_miss",
        "invalid_recoverable_banglish_miss",
        "wrong_transition",
        "banglish_matches_bangla_option",
        "banglish_matches_english_option",
    ]
    consensus_fields = [
        "id",
        "gold",
        "bangla_correct_models",
        "banglish_correct_models",
        "english_correct_models",
        "alternate_best_correct_models",
        "recoverable_banglish_miss_models",
        "valid_recoverable_banglish_miss_models",
        "top_recoverable_wrong_option",
        "top_recoverable_wrong_count",
        "two_plus_models_same_wrong_option",
        "all_three_models_same_wrong_option",
        "strong_alternate_low_banglish",
        "zero_banglish_strong_alternate",
        "wrong_option_counts",
    ]
    summary_fields = [
        "section",
        "model",
        "bucket",
        "gold",
        "n",
        "denominator",
        "rate",
        "recoverable_misses",
        "strict_recoverable_misses",
        "valid_recoverable_misses",
        "invalid_recoverable_misses",
        "pred_A",
        "pred_B",
        "pred_C",
        "pred_D",
        "pred_invalid",
        "top_wrong_option",
        "top_wrong_count",
        "repeated_wrong_option_items",
        "all_three_same_wrong_option_items",
        "detail",
    ]

    write_csv(args.items_output, item_rows, item_fields)
    write_csv(args.consensus_output, consensus_rows, consensus_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(
        args.report_output,
        item_rows,
        consensus_rows,
        summary_rows,
        args.items_output,
        args.consensus_output,
        args.summary_output,
    )
    print(
        "items={items} | consensus_rows={consensus} | summary_rows={summary} | "
        "report={report}".format(
            items=len(item_rows),
            consensus=len(consensus_rows),
            summary=len(summary_rows),
            report=args.report_output,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
