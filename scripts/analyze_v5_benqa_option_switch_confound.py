#!/usr/bin/env python3
"""Check BEnQA option switches after controlling for D length and gold label."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SWITCH_ITEMS = ROOT / "results/analysis/v5_benqa_option_switching_items.csv"
DEFAULT_POSITION_ITEMS = ROOT / "results/analysis/v5_benqa_option_position_content_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_option_switch_confound_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_option_switch_confound_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_switch_confound.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
BASELINES = ("bangla", "english")
BASELINE_LABELS = {"bangla": "Bangla", "english": "English"}


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


def build_item_rows(switch_items: Path, position_items: Path) -> list[dict[str, Any]]:
    position_by_model_id = {
        (row["model"], row["id"]): row
        for row in read_csv(position_items)
    }
    rows: list[dict[str, Any]] = []
    for switch in read_csv(switch_items):
        key = (switch["model"], switch["id"])
        if key not in position_by_model_id:
            raise SystemExit(f"Missing option-position features for {key}")
        features = position_by_model_id[key]
        baseline_non_d = truthy(switch["baseline_non_d"])
        baseline_correct_non_d = truthy(switch["baseline_correct_non_d"])
        d_is_longest = truthy(features["d_is_longest"])
        gold_not_d = switch["gold"] != "D"
        switched_non_d_to_d = truthy(switch["switched_non_d_to_d"])
        correct_non_d_to_wrong_d = truthy(switch["baseline_correct_non_d_to_d_wrong"])
        rows.append(
            {
                **switch,
                "d_is_longest": d_is_longest,
                "d_is_composite": truthy(features["d_is_composite"]),
                "gold_is_longest": truthy(features["gold_is_longest"]),
                "d_char_len": features["d_char_len"],
                "d_token_len": features["d_token_len"],
                "longest_options": features["longest_options"],
                "baseline_non_d_and_d_not_longest": baseline_non_d and not d_is_longest,
                "baseline_non_d_and_gold_not_d": baseline_non_d and gold_not_d,
                "baseline_non_d_gold_not_d_d_not_longest": (
                    baseline_non_d and gold_not_d and not d_is_longest
                ),
                "baseline_correct_non_d_and_d_not_longest": (
                    baseline_correct_non_d and not d_is_longest
                ),
                "switch_non_d_to_d_when_d_not_longest": (
                    switched_non_d_to_d and not d_is_longest
                ),
                "correct_non_d_to_wrong_d_when_d_not_longest": (
                    correct_non_d_to_wrong_d and not d_is_longest
                ),
            }
        )
    expected = len(MODELS) * len(BASELINES) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} joined rows, got {len(rows)}")
    return rows


def scopes() -> list[tuple[str, str, Callable[[dict[str, Any]], bool]]]:
    return [
        (
            "baseline_non_d",
            "Baseline predicts non-D",
            lambda row: truthy(row["baseline_non_d"]),
        ),
        (
            "d_not_longest",
            "Baseline non-D and D not longest",
            lambda row: truthy(row["baseline_non_d_and_d_not_longest"]),
        ),
        (
            "gold_not_d",
            "Baseline non-D and gold not D",
            lambda row: truthy(row["baseline_non_d_and_gold_not_d"]),
        ),
        (
            "gold_not_d_d_not_longest",
            "Baseline non-D, gold not D, D not longest",
            lambda row: truthy(row["baseline_non_d_gold_not_d_d_not_longest"]),
        ),
        (
            "correct_non_d",
            "Baseline correct non-D",
            lambda row: truthy(row["baseline_correct_non_d"]),
        ),
        (
            "correct_non_d_d_not_longest",
            "Baseline correct non-D and D not longest",
            lambda row: truthy(row["baseline_correct_non_d_and_d_not_longest"]),
        ),
    ]


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for baseline in BASELINES:
            selected = [
                row
                for row in rows
                if row["model"] == model and row["baseline_variant"] == baseline
            ]
            for scope, label, predicate in scopes():
                scoped = [row for row in selected if predicate(row)]
                non_d_to_d = sum(truthy(row["switched_non_d_to_d"]) for row in scoped)
                wrong_d_after_correct = sum(
                    truthy(row["baseline_correct_non_d_to_d_wrong"]) for row in scoped
                )
                out.append(
                    {
                        "section": "scope",
                        "model": model,
                        "baseline_variant": baseline,
                        "baseline_label": BASELINE_LABELS[baseline],
                        "scope": scope,
                        "scope_label": label,
                        "n": len(scoped),
                        "non_d_to_D": non_d_to_d,
                        "non_d_to_D_rate": round(non_d_to_d / len(scoped), 4)
                        if scoped
                        else "",
                        "correct_non_d_to_wrong_D": wrong_d_after_correct,
                        "correct_non_d_to_wrong_D_rate": round(
                            wrong_d_after_correct / len(scoped), 4
                        )
                        if scoped
                        else "",
                    }
                )
    return out


def row_for(
    rows: list[dict[str, Any]],
    model: str,
    baseline: str,
    scope: str,
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["model"] == model
        and row["baseline_variant"] == baseline
        and row["scope"] == scope
    )


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_bangla_nonlong = row_for(
        summary_rows, "Qwen3-4B", "bangla", "correct_non_d_d_not_longest"
    )
    q3_english_nonlong = row_for(
        summary_rows, "Qwen3-4B", "english", "correct_non_d_d_not_longest"
    )
    q3_bangla_strict = row_for(
        summary_rows, "Qwen3-4B", "bangla", "gold_not_d_d_not_longest"
    )
    q3_english_strict = row_for(
        summary_rows, "Qwen3-4B", "english", "gold_not_d_d_not_longest"
    )
    q25_3b_bangla_nonlong = row_for(
        summary_rows, "Qwen2.5-3B", "bangla", "correct_non_d_d_not_longest"
    )
    q25_7b_bangla_nonlong = row_for(
        summary_rows, "Qwen2.5-7B 8-bit", "bangla", "correct_non_d_d_not_longest"
    )

    lines = [
        "# Frozen-V5 BEnQA Option-Switch Confound Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit joins the BEnQA option-switching rows with the",
        "option position/content features. It asks whether Qwen3's reviewed-",
        "Banglish non-D-to-D switches persist after controlling for D being the",
        "longest option and for gold-D rows.",
        "",
        f"- Joined item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- When the alternate-script prediction is correct, non-D, and D is not "
            "the longest option, Qwen3 still switches to a wrong reviewed-Banglish "
            f"D on {q3_bangla_nonlong['correct_non_d_to_wrong_D']}/"
            f"{q3_bangla_nonlong['n']} Bangla rows and "
            f"{q3_english_nonlong['correct_non_d_to_wrong_D']}/"
            f"{q3_english_nonlong['n']} English rows."
        ),
        (
            "- In the broader non-D, gold-not-D, D-not-longest scope, Qwen3 switches "
            f"to D on {q3_bangla_strict['non_d_to_D']}/{q3_bangla_strict['n']} "
            f"Bangla rows and {q3_english_strict['non_d_to_D']}/"
            f"{q3_english_strict['n']} English rows."
        ),
        (
            "- The corresponding correct-non-D and D-not-longest Bangla-side counts "
            "for Qwen2.5 are only "
            f"{q25_3b_bangla_nonlong['correct_non_d_to_wrong_D']}/"
            f"{q25_3b_bangla_nonlong['n']} and "
            f"{q25_7b_bangla_nonlong['correct_non_d_to_wrong_D']}/"
            f"{q25_7b_bangla_nonlong['n']}."
        ),
        "",
        "## Strict Scope Summary",
        "",
        "| Model | Baseline | Non-D/gold-not-D/D-not-longest: switched to D | Correct non-D/D-not-longest: wrong D |",
        "| --- | --- | ---: | ---: |",
    ]
    for model in MODELS:
        for baseline in BASELINES:
            strict = row_for(summary_rows, model, baseline, "gold_not_d_d_not_longest")
            correct = row_for(summary_rows, model, baseline, "correct_non_d_d_not_longest")
            lines.append(
                "| {model} | {baseline_label} | {strict_switch}/{strict_n} ({strict_pct}) | "
                "{correct_wrong}/{correct_n} ({correct_pct}) |".format(
                    model=model,
                    baseline_label=BASELINE_LABELS[baseline],
                    strict_switch=strict["non_d_to_D"],
                    strict_n=strict["n"],
                    strict_pct=percent(int(strict["non_d_to_D"]), int(strict["n"])),
                    correct_wrong=correct["correct_non_d_to_wrong_D"],
                    correct_n=correct["n"],
                    correct_pct=percent(
                        int(correct["correct_non_d_to_wrong_D"]), int(correct["n"])
                    ),
                )
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- D being a long option is a real BEnQA confound, but it does not remove",
            "  the Qwen3 switching result: many Qwen3 non-D alternate-script choices",
            "  still become reviewed-Banglish D when D is not longest.",
            "- Excluding gold-D rows also preserves the pattern, so the switch is not",
            "  merely a route to the correct gold-D label.",
            "- Treat this as a confound audit for the Qwen3 BEnQA failure mode, not as",
            "  a causal internal-mechanism claim.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_benqa_option_switch_confound.py`",
            f"- Joined item rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--switch-items", type=Path, default=DEFAULT_SWITCH_ITEMS)
    parser.add_argument("--position-items", type=Path, default=DEFAULT_POSITION_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.switch_items, args.position_items)
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    q3_bangla = row_for(summary_rows, "Qwen3-4B", "bangla", "correct_non_d_d_not_longest")
    q3_english = row_for(summary_rows, "Qwen3-4B", "english", "correct_non_d_d_not_longest")
    print(
        "items={items} | summary_rows={summary} | "
        "qwen3_correct_nonD_D_not_longest_wrongD=bangla:{bangla}/{bangla_n},"
        "english:{english}/{english_n} | report={report}".format(
            items=len(item_rows),
            summary=len(summary_rows),
            bangla=q3_bangla["correct_non_d_to_wrong_D"],
            bangla_n=q3_bangla["n"],
            english=q3_english["correct_non_d_to_wrong_D"],
            english_n=q3_english["n"],
            report=args.report_output,
        )
    )


if __name__ == "__main__":
    main()
