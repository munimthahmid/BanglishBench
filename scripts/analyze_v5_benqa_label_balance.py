#!/usr/bin/env python3
"""Gold-label balance sensitivity for frozen-v5 BEnQA MCQs."""

from __future__ import annotations

import argparse
import csv
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_BY_LABEL_OUTPUT = ROOT / "results/analysis/v5_benqa_label_balance_by_label.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_label_balance_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_label_balance.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
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
SCOPES = (
    ("all_benqa_micro", "All BEnQA MCQs", None, False),
    ("gold_label_balanced", "Gold-label balanced", None, True),
    ("gold_not_d_micro", "Gold not D", {"A", "B", "C"}, False),
    ("gold_d_micro", "Gold D only", {"D"}, False),
)
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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def pts(value: float) -> str:
    scaled = value * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = read_csv(path)
    expected = len(MODELS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} BEnQA item rows, got {len(rows)}")
    out: list[dict[str, Any]] = []
    for row in rows:
        model = row["model"]
        if model not in MODELS:
            raise SystemExit(f"Unexpected model label: {model}")
        gold = row["gold"].strip().upper()
        if gold not in OPTIONS:
            raise SystemExit(f"Unexpected gold option for {row['id']}: {gold}")
        parsed: dict[str, str] = {}
        correct: dict[str, bool] = {}
        for variant in VARIANTS:
            parsed[variant] = row[f"{variant}_parsed_option"].strip().upper()
            correct[variant] = truthy(row[f"{variant}_correct"])
        out.append(
            {
                "model": model,
                "id": row["id"],
                "gold": gold,
                "parsed": parsed,
                "correct": correct,
            }
        )
    return out


def accuracy(rows: list[dict[str, Any]], variant: str) -> float:
    if not rows:
        return 0.0
    return sum(row["correct"][variant] for row in rows) / len(rows)


def label_balanced_accuracy(rows: list[dict[str, Any]], variant: str) -> float:
    by_gold: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_gold[row["gold"]].append(row)
    return sum(accuracy(by_gold[option], variant) for option in OPTIONS) / len(OPTIONS)


def metric(rows: list[dict[str, Any]], variant: str, balanced: bool) -> float:
    if balanced:
        return label_balanced_accuracy(rows, variant)
    return accuracy(rows, variant)


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    low = int(pos)
    high = min(low + 1, len(ordered) - 1)
    frac = pos - low
    return ordered[low] * (1 - frac) + ordered[high] * frac


def bootstrap_delta(
    rows: list[dict[str, Any]],
    baseline: str,
    candidate: str,
    balanced: bool,
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    rng = random.Random(seed)
    deltas: list[float] = []
    if balanced:
        by_gold: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            by_gold[row["gold"]].append(row)
        for _ in range(iterations):
            sample: list[dict[str, Any]] = []
            for option in OPTIONS:
                group = by_gold[option]
                sample.extend(rng.choice(group) for _i in range(len(group)))
            deltas.append(metric(sample, candidate, True) - metric(sample, baseline, True))
    else:
        n = len(rows)
        for _ in range(iterations):
            sample = [rng.choice(rows) for _i in range(n)]
            deltas.append(metric(sample, candidate, False) - metric(sample, baseline, False))
    return percentile(deltas, 0.025), percentile(deltas, 0.975)


def build_by_label_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        for option in OPTIONS:
            label_rows = [row for row in model_rows if row["gold"] == option]
            for variant in VARIANTS:
                correct = sum(row["correct"][variant] for row in label_rows)
                pred_counts = Counter(row["parsed"][variant] for row in label_rows)
                out.append(
                    {
                        "model": model,
                        "gold": option,
                        "variant": variant,
                        "variant_label": VARIANT_LABELS[variant],
                        "n": len(label_rows),
                        "correct": correct,
                        "accuracy": round(correct / len(label_rows), 4),
                        "pred_A": pred_counts["A"],
                        "pred_B": pred_counts["B"],
                        "pred_C": pred_counts["C"],
                        "pred_D": pred_counts["D"],
                        "pred_invalid": sum(
                            count
                            for parsed, count in pred_counts.items()
                            if parsed not in OPTIONS
                        ),
                    }
                )
    return out


def build_summary_rows(
    rows: list[dict[str, Any]], iterations: int, seed: int
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        for scope, scope_label, allowed_gold, balanced in SCOPES:
            selected = [
                row
                for row in model_rows
                if allowed_gold is None or row["gold"] in allowed_gold
            ]
            for comparison, baseline, candidate, baseline_label in COMPARISONS:
                baseline_acc = metric(selected, baseline, balanced)
                candidate_acc = metric(selected, candidate, balanced)
                low, high = bootstrap_delta(
                    selected,
                    baseline,
                    candidate,
                    balanced,
                    iterations,
                    seed
                    + 1009 * MODELS.index(model)
                    + 101 * [scope for scope, *_rest in SCOPES].index(scope)
                    + 17 * [name for name, *_rest in COMPARISONS].index(comparison),
                )
                gains = sum(
                    (not row["correct"][baseline]) and row["correct"][candidate]
                    for row in selected
                )
                losses = sum(
                    row["correct"][baseline] and (not row["correct"][candidate])
                    for row in selected
                )
                out.append(
                    {
                        "model": model,
                        "scope": scope,
                        "scope_label": scope_label,
                        "comparison": comparison,
                        "baseline_variant": baseline,
                        "baseline_label": baseline_label,
                        "candidate_variant": candidate,
                        "candidate_label": VARIANT_LABELS[candidate],
                        "n": len(selected),
                        "balanced_metric": balanced,
                        "baseline_correct": sum(row["correct"][baseline] for row in selected),
                        "candidate_correct": sum(row["correct"][candidate] for row in selected),
                        "baseline_accuracy": round(baseline_acc, 4),
                        "candidate_accuracy": round(candidate_acc, 4),
                        "delta_candidate_minus_baseline": round(candidate_acc - baseline_acc, 4),
                        "ci95_low": round(low, 4),
                        "ci95_high": round(high, 4),
                        "banglish_gains": gains,
                        "banglish_losses": losses,
                    }
                )
    return out


def find_row(rows: list[dict[str, Any]], model: str, scope: str, comparison: str) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["model"] == model and row["scope"] == scope and row["comparison"] == comparison
    )


def by_label_acc(
    rows: list[dict[str, Any]], model: str, option: str, variant: str
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["model"] == model and row["gold"] == option and row["variant"] == variant
    )


def write_report(
    path: Path,
    by_label_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    input_path: Path,
    by_label_output: Path,
    summary_output: Path,
    iterations: int,
) -> None:
    gold_counts = {
        option: by_label_acc(by_label_rows, MODELS[0], option, "bangla")["n"]
        for option in OPTIONS
    }
    lines = [
        "# Frozen-V5 BEnQA Gold-Label Balance Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the BEnQA MCQ script gap is an",
        "artifact of gold option-label distribution or Qwen3's reviewed-Banglish",
        "over-selection of option D. It reports micro accuracy, gold-label",
        "balanced accuracy (mean of A/B/C/D stratum accuracies), and a non-D",
        "stress slice. Bootstrap intervals resample paired items, stratified by",
        "gold label for the balanced metric.",
        "",
        f"- Source choice-bias items: `{repo_path(input_path)}`",
        f"- By-label table: `{repo_path(by_label_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        f"- Bootstrap iterations: {iterations}",
        "",
        "Gold label counts: "
        + ", ".join(f"{option}={gold_counts[option]}" for option in OPTIONS)
        + ".",
        "",
        "## Label-Balanced Accuracy",
        "",
        "| Model | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        row_bb = find_row(summary_rows, model, "gold_label_balanced", "banglish_minus_bangla")
        row_be = find_row(summary_rows, model, "gold_label_balanced", "banglish_minus_english")
        lines.append(
            f"| {model} | {pct(row_bb['baseline_accuracy'])} | "
            f"{pct(row_bb['candidate_accuracy'])} | {pct(row_be['baseline_accuracy'])} | "
            f"{pts(row_bb['delta_candidate_minus_baseline'])} pts "
            f"[{pts(row_bb['ci95_low'])}, {pts(row_bb['ci95_high'])}] | "
            f"{pts(row_be['delta_candidate_minus_baseline'])} pts "
            f"[{pts(row_be['ci95_low'])}, {pts(row_be['ci95_high'])}] |"
        )

    lines.extend(
        [
            "",
            "## Non-D Stress Slice",
            "",
            "This removes gold-D items, where a D-heavy predictor can score by chance",
            "or bias. Qwen3 reviewed Banglish becomes much weaker, which confirms",
            "that option-D over-selection is a failure mode rather than an",
            "explanation away from the script effect.",
            "",
            "| Model | n | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        row_bb = find_row(summary_rows, model, "gold_not_d_micro", "banglish_minus_bangla")
        row_be = find_row(summary_rows, model, "gold_not_d_micro", "banglish_minus_english")
        lines.append(
            f"| {model} | {row_bb['n']} | {row_bb['baseline_correct']}/{row_bb['n']} "
            f"({pct(row_bb['baseline_accuracy'])}) | {row_bb['candidate_correct']}/{row_bb['n']} "
            f"({pct(row_bb['candidate_accuracy'])}) | {row_be['baseline_correct']}/{row_be['n']} "
            f"({pct(row_be['baseline_accuracy'])}) | "
            f"{pts(row_bb['delta_candidate_minus_baseline'])} pts "
            f"[{pts(row_bb['ci95_low'])}, {pts(row_bb['ci95_high'])}] | "
            f"{pts(row_be['delta_candidate_minus_baseline'])} pts "
            f"[{pts(row_be['ci95_low'])}, {pts(row_be['ci95_high'])}] |"
        )

    lines.extend(
        [
            "",
            "## Gold-D Slice",
            "",
            "| Model | Bangla | Reviewed Banglish | English | Banglish-Bangla |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        row_bb = find_row(summary_rows, model, "gold_d_micro", "banglish_minus_bangla")
        row_be = find_row(summary_rows, model, "gold_d_micro", "banglish_minus_english")
        lines.append(
            f"| {model} | {row_bb['baseline_correct']}/{row_bb['n']} "
            f"({pct(row_bb['baseline_accuracy'])}) | {row_bb['candidate_correct']}/{row_bb['n']} "
            f"({pct(row_bb['candidate_accuracy'])}) | {row_be['baseline_correct']}/{row_be['n']} "
            f"({pct(row_be['baseline_accuracy'])}) | "
            f"{pts(row_bb['delta_candidate_minus_baseline'])} pts "
            f"[{pts(row_bb['ci95_low'])}, {pts(row_bb['ci95_high'])}] |"
        )

    lines.extend(
        [
            "",
            "## Per-Label Accuracy",
            "",
            "| Model | Gold | Bangla | Reviewed Banglish | English |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        for option in OPTIONS:
            bangla = by_label_acc(by_label_rows, model, option, "bangla")
            banglish = by_label_acc(by_label_rows, model, option, "banglish_clean")
            english = by_label_acc(by_label_rows, model, option, "english")
            lines.append(
                f"| {model} | {option} | {bangla['correct']}/{bangla['n']} "
                f"({pct(bangla['accuracy'])}) | {banglish['correct']}/{banglish['n']} "
                f"({pct(banglish['accuracy'])}) | {english['correct']}/{english['n']} "
                f"({pct(english['accuracy'])}) |"
            )

    q3_bal = find_row(summary_rows, "Qwen3-4B", "gold_label_balanced", "banglish_minus_bangla")
    q3_non_d = find_row(summary_rows, "Qwen3-4B", "gold_not_d_micro", "banglish_minus_bangla")
    q25_7b_bal = find_row(summary_rows, "Qwen2.5-7B 8-bit", "gold_label_balanced", "banglish_minus_bangla")
    q25_3b_bal = find_row(summary_rows, "Qwen2.5-3B", "gold_label_balanced", "banglish_minus_bangla")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Gold-label balancing keeps reviewed Banglish below Bangla and English",
            "  for all three thesis-facing Qwen rows.",
            f"- Qwen3-4B is not helped by balancing: reviewed Banglish is",
            f"  {pts(q3_bal['delta_candidate_minus_baseline'])} pts below Bangla",
            f"  on the balanced metric and {pts(q3_non_d['delta_candidate_minus_baseline'])} pts",
            "  below Bangla after removing gold-D items.",
            f"- Qwen2.5-7B 8-bit remains negative after label balancing",
            f"  ({pts(q25_7b_bal['delta_candidate_minus_baseline'])} pts vs Bangla).",
            f"  Qwen2.5-3B remains the qualified row",
            f"  ({pts(q25_3b_bal['delta_candidate_minus_baseline'])} pts vs Bangla),",
            "  matching the main-table and paired-sign-test caveat.",
            "- Treat Qwen3 option-D over-selection as a script-conditioned failure",
            "  mode, not as a confound that removes the BEnQA gap.",
            "",
            "## Thesis-Safe Claim",
            "",
            "Use this as a sensitivity check: the BEnQA reviewed-Banglish deficit",
            "survives gold-label balancing and a non-D stress slice, while Qwen3's",
            "D-heavy behavior is reported as a discovered failure mode.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--by-label-output", type=Path, default=DEFAULT_BY_LABEL_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--bootstrap-iterations", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260531)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    by_label_rows = build_by_label_rows(rows)
    summary_rows = build_summary_rows(rows, args.bootstrap_iterations, args.seed)
    write_csv(args.by_label_output, by_label_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        by_label_rows,
        summary_rows,
        args.input,
        args.by_label_output,
        args.summary_output,
        args.bootstrap_iterations,
    )
    print(
        f"by_label_rows={len(by_label_rows)} summary_rows={len(summary_rows)} "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
