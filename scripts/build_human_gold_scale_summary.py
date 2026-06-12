#!/usr/bin/env python3
"""Combine human-reviewed BEnQA extension scale summaries into one table."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "results/analysis/benqa_human_gold_974_scale_summary.csv"
DEFAULT_REPORT = ROOT / "reports/benqa_human_gold_974_scale_summary.md"

INPUTS = [
    (
        "Qwen2.5-3B",
        ROOT / "results/analysis/qwen25_3b_benqa_human_gold_974_summary.csv",
        ROOT / "reports/qwen25_3b_benqa_human_gold_974.md",
    ),
    (
        "Groq Llama 3.3 70B",
        ROOT / "results/analysis/groq_llama33_70b_benqa_human_gold_974_summary.csv",
        ROOT / "reports/groq_llama33_70b_benqa_human_gold_974.md",
    ),
    (
        "DeepSeek V4 Flash",
        ROOT / "results/analysis/deepseek_v4_flash_benqa_human_gold_974_summary.csv",
        ROOT / "reports/deepseek_v4_flash_benqa_human_gold_974.md",
    ),
]


def repo_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def read_summary(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(value: str) -> str:
    return f"{float(value) * 100:.2f}"


def model_row(model: str, summary_path: Path, report_path: Path) -> dict[str, str] | None:
    if not summary_path.exists():
        return None
    rows = read_summary(summary_path)
    variants = {row["label"]: row for row in rows if row["metric"] == "variant_accuracy"}
    gaps = {row["label"]: row for row in rows if row["metric"] == "paired_gap"}
    return {
        "model": model,
        "items": variants["bangla"]["n"],
        "bangla_correct": variants["bangla"]["correct"],
        "bangla_accuracy": pct(variants["bangla"]["accuracy"]),
        "banglish_correct": variants["banglish_clean"]["correct"],
        "banglish_accuracy": pct(variants["banglish_clean"]["accuracy"]),
        "english_correct": variants["english"]["correct"],
        "english_accuracy": pct(variants["english"]["accuracy"]),
        "banglish_minus_bangla_pts": pct(gaps["banglish_minus_bangla"]["accuracy"]),
        "banglish_minus_bangla_ci": (
            f"[{pct(gaps['banglish_minus_bangla']['ci95_low'])}, "
            f"{pct(gaps['banglish_minus_bangla']['ci95_high'])}]"
        ),
        "banglish_minus_english_pts": pct(gaps["banglish_minus_english"]["accuracy"]),
        "banglish_minus_english_ci": (
            f"[{pct(gaps['banglish_minus_english']['ci95_low'])}, "
            f"{pct(gaps['banglish_minus_english']['ci95_high'])}]"
        ),
        "report": repo_path(report_path),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "model",
        "items",
        "bangla_correct",
        "bangla_accuracy",
        "banglish_correct",
        "banglish_accuracy",
        "english_correct",
        "english_accuracy",
        "banglish_minus_bangla_pts",
        "banglish_minus_bangla_ci",
        "banglish_minus_english_pts",
        "banglish_minus_english_ci",
        "report",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, output_csv: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# BEnQA Human-Reviewed Gold 974 Scale Summary",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This table summarizes completed model runs on the frozen 974-row",
        "human-reviewed BEnQA extension. The full 1,000-row audit slice has 26",
        "human-rejected rows; accepted and edited rows form the gold/pass",
        "evaluation set.",
        "",
        f"- Summary CSV: `{repo_path(output_csv)}`",
        "",
        "## Results",
        "",
        "| Model | Bangla | Reviewed Banglish | English | BG-Bangla | BG-English |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['model']} | "
            f"{row['bangla_correct']}/{row['items']} ({row['bangla_accuracy']}%) | "
            f"{row['banglish_correct']}/{row['items']} ({row['banglish_accuracy']}%) | "
            f"{row['english_correct']}/{row['items']} ({row['english_accuracy']}%) | "
            f"{row['banglish_minus_bangla_pts']} pts {row['banglish_minus_bangla_ci']} | "
            f"{row['banglish_minus_english_pts']} pts {row['banglish_minus_english_ci']} |"
        )
    lines.extend(
        [
            "",
            "## Source Reports",
            "",
        ]
    )
    for row in rows:
        lines.append(f"- {row['model']}: `{row['report']}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [row for model, summary, report in INPUTS if (row := model_row(model, summary, report))]
    write_csv(args.output, rows)
    write_report(args.report, args.output, rows)
    print(f"models={len(rows)}")
    print(f"output={repo_path(args.output)}")
    print(f"report={repo_path(args.report)}")


if __name__ == "__main__":
    main()
