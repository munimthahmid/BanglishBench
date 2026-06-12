#!/usr/bin/env python3
"""Summarize BEnQA MCQ prediction-diversity collapse for frozen-v5 rows."""

from __future__ import annotations

import argparse
import csv
import math
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHOICE_SUMMARY = ROOT / "results/analysis/v5_benqa_choice_bias_summary.csv"
DEFAULT_SUBJECT_SUMMARY = ROOT / "results/analysis/v5_benqa_subject_option_bias_summary.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_prediction_diversity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_prediction_diversity.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
VARIANTS = ("bangla", "banglish_clean", "english")
VARIANT_LABELS = {
    "bangla": "Bangla",
    "banglish_clean": "Reviewed Banglish",
    "english": "English",
}
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
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    return int(float(value)) if value != "" else 0


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value != "" else 0.0


def percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def normalized_entropy_from_counts(counts: list[int]) -> float:
    n = sum(counts)
    if n == 0:
        return 0.0
    entropy = 0.0
    for count in counts:
        if count:
            p = count / n
            entropy -= p * math.log(p)
    return entropy / math.log(len(counts))


def effective_options(normalized_entropy: float) -> float:
    return len(OPTIONS) ** normalized_entropy


def hhi(counts: list[int]) -> float:
    n = sum(counts)
    if n == 0:
        return 0.0
    return sum((count / n) ** 2 for count in counts)


def choice_row(
    rows: list[dict[str, str]], model: str, variant: str
) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if row.get("section") == "variant_distribution"
        and row.get("model") == model
        and row.get("variant") == variant
    ]
    if len(matches) != 1:
        raise SystemExit(f"Expected one choice row for {model} {variant}, got {len(matches)}")
    return matches[0]


def variant_diversity(choice_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for variant in VARIANTS:
            row = choice_row(choice_rows, model, variant)
            n = as_int(row, "n")
            pred_counts = [as_int(row, f"pred_{option}") for option in OPTIONS]
            gold_counts = [as_int(row, f"gold_{option}") for option in OPTIONS]
            entropy = as_float(row, "option_entropy")
            d_share = pred_counts[3] / n
            gold_d_share = gold_counts[3] / n
            out.append(
                {
                    "section": "variant_diversity",
                    "model": model,
                    "variant": variant,
                    "variant_label": VARIANT_LABELS[variant],
                    "n": n,
                    "correct": as_int(row, "correct"),
                    "pred_A": pred_counts[0],
                    "pred_B": pred_counts[1],
                    "pred_C": pred_counts[2],
                    "pred_D": pred_counts[3],
                    "gold_A": gold_counts[0],
                    "gold_B": gold_counts[1],
                    "gold_C": gold_counts[2],
                    "gold_D": gold_counts[3],
                    "majority_option": row["majority_option"],
                    "majority_share": round(as_float(row, "majority_share"), 4),
                    "normalized_entropy": round(entropy, 4),
                    "effective_options": round(effective_options(entropy), 2),
                    "hhi": round(hhi(pred_counts), 4),
                    "simpson_diversity": round(1 - hhi(pred_counts), 4),
                    "d_share": round(d_share, 4),
                    "gold_d_share": round(gold_d_share, 4),
                    "d_excess_over_gold": round(d_share - gold_d_share, 4),
                    "tvd_pred_vs_gold": round(as_float(row, "tvd_pred_vs_gold"), 4),
                    "accuracy": round(as_int(row, "correct") / n, 4),
                }
            )
    return out


def gold_distribution(choice_rows: list[dict[str, str]]) -> dict[str, Any]:
    row = choice_row(choice_rows, "Qwen2.5-3B", "bangla")
    counts = [as_int(row, f"gold_{option}") for option in OPTIONS]
    n = sum(counts)
    entropy = normalized_entropy_from_counts(counts)
    return {
        "section": "gold_distribution",
        "model": "gold",
        "variant": "gold",
        "variant_label": "Gold labels",
        "n": n,
        "gold_A": counts[0],
        "gold_B": counts[1],
        "gold_C": counts[2],
        "gold_D": counts[3],
        "normalized_entropy": round(entropy, 4),
        "effective_options": round(effective_options(entropy), 2),
        "hhi": round(hhi(counts), 4),
        "simpson_diversity": round(1 - hhi(counts), 4),
        "gold_d_share": round(counts[3] / n, 4),
    }


def banglish_deltas(variant_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index = {(row["model"], row["variant"]): row for row in variant_rows}
    out: list[dict[str, Any]] = []
    for model in MODELS:
        banglish = index[(model, "banglish_clean")]
        for baseline in ("bangla", "english"):
            base = index[(model, baseline)]
            out.append(
                {
                    "section": "banglish_delta",
                    "model": model,
                    "variant": f"{baseline}_to_banglish_clean",
                    "variant_label": f"{VARIANT_LABELS[baseline]} -> Reviewed Banglish",
                    "n": banglish["n"],
                    "accuracy_delta": round(banglish["accuracy"] - base["accuracy"], 4),
                    "normalized_entropy_delta": round(
                        banglish["normalized_entropy"] - base["normalized_entropy"], 4
                    ),
                    "effective_options_delta": round(
                        banglish["effective_options"] - base["effective_options"], 2
                    ),
                    "majority_share_delta": round(
                        banglish["majority_share"] - base["majority_share"], 4
                    ),
                    "d_share_delta": round(banglish["d_share"] - base["d_share"], 4),
                    "tvd_delta": round(
                        banglish["tvd_pred_vs_gold"] - base["tvd_pred_vs_gold"], 4
                    ),
                }
            )
    return out


def subject_rollups(subject_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        for variant in VARIANTS:
            selected = [
                row
                for row in subject_rows
                if row.get("model") == model
                and row.get("variant") == variant
                and row.get("section") == "subject_variant"
            ]
            if len(selected) != 13:
                raise SystemExit(f"Expected 13 subject rows for {model} {variant}, got {len(selected)}")
            entropies = [as_float(row, "option_entropy") for row in selected]
            d_shares = [as_float(row, "d_share") for row in selected]
            out.append(
                {
                    "section": "subject_rollup",
                    "model": model,
                    "variant": variant,
                    "variant_label": VARIANT_LABELS[variant],
                    "subject_count": len(selected),
                    "majority_d_subjects": sum(
                        1 for row in selected if row.get("majority_d") == "True"
                    ),
                    "mean_subject_entropy": round(sum(entropies) / len(entropies), 4),
                    "min_subject_entropy": round(min(entropies), 4),
                    "mean_subject_d_share": round(sum(d_shares) / len(d_shares), 4),
                    "max_subject_d_share": round(max(d_shares), 4),
                }
            )
    return out


def row_for(rows: list[dict[str, Any]], section: str, model: str, variant: str) -> dict[str, Any]:
    matches = [
        row
        for row in rows
        if row.get("section") == section
        and row.get("model") == model
        and row.get("variant") == variant
    ]
    if len(matches) != 1:
        raise SystemExit(f"Expected one {section} row for {model} {variant}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    summary_output: Path,
) -> None:
    gold = row_for(summary_rows, "gold_distribution", "gold", "gold")
    q3_bn = row_for(summary_rows, "variant_diversity", "Qwen3-4B", "bangla")
    q3_bg = row_for(summary_rows, "variant_diversity", "Qwen3-4B", "banglish_clean")
    q3_en = row_for(summary_rows, "variant_diversity", "Qwen3-4B", "english")
    q25_3_bg = row_for(summary_rows, "variant_diversity", "Qwen2.5-3B", "banglish_clean")
    q25_7_bg = row_for(summary_rows, "variant_diversity", "Qwen2.5-7B 8-bit", "banglish_clean")
    q3_delta_bn = row_for(
        summary_rows, "banglish_delta", "Qwen3-4B", "bangla_to_banglish_clean"
    )
    q3_sub = row_for(summary_rows, "subject_rollup", "Qwen3-4B", "banglish_clean")
    q3_sub_bn = row_for(summary_rows, "subject_rollup", "Qwen3-4B", "bangla")
    q3_sub_en = row_for(summary_rows, "subject_rollup", "Qwen3-4B", "english")

    lines = [
        "# Frozen-V5 BEnQA Prediction-Diversity Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit summarizes whether BEnQA MCQ option predictions retain",
        "normal label diversity or collapse toward one label. It reuses the frozen-v5",
        "choice-bias and subject option-bias summaries, so it adds no new model",
        "inference and no manual review.",
        "",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- Gold labels are close to balanced: "
            f"A={gold['gold_A']}, B={gold['gold_B']}, C={gold['gold_C']}, D={gold['gold_D']}; "
            f"normalized entropy {gold['normalized_entropy']:.3f} and "
            f"{gold['effective_options']:.2f} effective options."
        ),
        (
            "- Qwen3-4B reviewed Banglish collapses to D: "
            f"predictions are A={q3_bg['pred_A']}, B={q3_bg['pred_B']}, "
            f"C={q3_bg['pred_C']}, D={q3_bg['pred_D']}; normalized entropy "
            f"{q3_bg['normalized_entropy']:.3f} and {q3_bg['effective_options']:.2f} "
            "effective options."
        ),
        (
            "- The same Qwen3 row has "
            f"{q3_bn['effective_options']:.2f} effective options in Bangla and "
            f"{q3_en['effective_options']:.2f} in English; reviewed Banglish loses "
            f"{abs(q3_delta_bn['effective_options_delta']):.2f} effective options versus Bangla."
        ),
        (
            "- Qwen2.5 reviewed Banglish retains high diversity: "
            f"{q25_3_bg['effective_options']:.2f} and {q25_7_bg['effective_options']:.2f} "
            "effective options for the 3B and 7B rows."
        ),
        (
            "- Subject rollup shows Qwen3 reviewed Banglish majority-D in "
            f"{q3_sub['majority_d_subjects']}/13 subjects with mean subject entropy "
            f"{q3_sub['mean_subject_entropy']:.3f}, versus {q3_sub_bn['mean_subject_entropy']:.3f} "
            f"Bangla and {q3_sub_en['mean_subject_entropy']:.3f} English."
        ),
        "",
        "## Variant Distribution",
        "",
        "| Model | Variant | Correct | Pred A | Pred B | Pred C | Pred D | Entropy | Effective options | D excess vs gold | TVD vs gold |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        for variant in VARIANTS:
            row = row_for(summary_rows, "variant_diversity", model, variant)
            lines.append(
                f"| {model} | {row['variant_label']} | {row['correct']}/{row['n']} | "
                f"{row['pred_A']} | {row['pred_B']} | {row['pred_C']} | {row['pred_D']} | "
                f"{row['normalized_entropy']:.2f} | {row['effective_options']:.2f} | "
                f"{percent(row['d_excess_over_gold'])} | {row['tvd_pred_vs_gold']:.2f} |"
            )
    lines.extend(
        [
            "",
            "## Subject Rollup",
            "",
            "| Model | Variant | Majority-D subjects | Mean subject entropy | Max subject D share |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for model in MODELS:
        for variant in VARIANTS:
            row = row_for(summary_rows, "subject_rollup", model, variant)
            lines.append(
                f"| {model} | {row['variant_label']} | "
                f"{row['majority_d_subjects']}/{row['subject_count']} | "
                f"{row['mean_subject_entropy']:.2f} | {percent(row['max_subject_d_share'])} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Qwen3's reviewed-Banglish BEnQA behavior is not just lower accuracy; it",
            "  is a sharp reduction in prediction diversity relative to gold labels and",
            "  to the same model's Bangla/English rows.",
            "- Qwen2.5 rows preserve near-normal option diversity, so the Qwen3 collapse",
            "  is a model-specific failure mode rather than an unavoidable property of",
            "  Latin-script Banglish prompts.",
            "- This is behavioral evidence only. It supports the failure analysis but",
            "  does not identify an internal model mechanism.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_prediction_diversity.py`",
            f"- Summary table: `{repo_path(summary_output)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--choice-summary", type=Path, default=DEFAULT_CHOICE_SUMMARY)
    parser.add_argument("--subject-summary", type=Path, default=DEFAULT_SUBJECT_SUMMARY)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    choice_rows = read_csv(args.choice_summary)
    subject_rows = read_csv(args.subject_summary)
    variant_rows = variant_diversity(choice_rows)
    summary_rows = [gold_distribution(choice_rows)] + variant_rows + banglish_deltas(variant_rows) + subject_rollups(subject_rows)
    if len(summary_rows) != 25:
        raise SystemExit(f"Expected 25 summary rows, got {len(summary_rows)}")
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.summary_output)

    q3_bg = row_for(summary_rows, "variant_diversity", "Qwen3-4B", "banglish_clean")
    q3_sub = row_for(summary_rows, "subject_rollup", "Qwen3-4B", "banglish_clean")
    print(
        "summary_rows=25 "
        f"qwen3_banglish_effective_options={q3_bg['effective_options']:.2f} "
        f"qwen3_banglish_entropy={q3_bg['normalized_entropy']:.4f} "
        f"qwen3_banglish_D={q3_bg['pred_D']}/144 "
        f"qwen3_majorityD_subjects={q3_sub['majority_d_subjects']}/13 "
        f"report={args.report_output}"
    )


if __name__ == "__main__":
    main()
