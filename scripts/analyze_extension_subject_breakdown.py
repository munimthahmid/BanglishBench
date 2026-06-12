#!/usr/bin/env python3
"""Per-subject script-gap breakdown for the BEnQA human-gold 974 extension.

Parses the macro subject (Biology / Chemistry / Physics / Math / Science)
from each extension item id, then reports per-model per-subject accuracy in
all three script views, the Banglish-minus-Bangla point gap, and a
within-subject McNemar exact p-value. This answers whether the extension
script gap concentrates in particular subjects.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "results/analysis"
DEFAULT_OUTPUT = ANALYSIS / "benqa_human_gold_974_subject_breakdown.csv"
DEFAULT_REPORT = ROOT / "reports/benqa_human_gold_974_subject_breakdown.md"
DEFAULT_TABLE = ROOT / "results/analysis/benqa_human_gold_974_subject_breakdown_table.csv"

MODELS = {
    "Qwen2.5-3B": "qwen25_3b_benqa_human_gold_974_item_matrix.csv",
    "Gemini 3.5 Flash": "gemini_3_5_flash_benqa_human_gold_974_item_matrix.csv",
    "GPT-5.5 none": "openai_gpt55_none_benqa_human_gold_974_item_matrix.csv",
    "Claude Sonnet 4.6": "claude_sonnet_4_6_benqa_human_gold_974_item_matrix.csv",
    "DeepSeek V4 Flash": "deepseek_v4_flash_benqa_human_gold_974_item_matrix.csv",
    "Groq Llama 3.3 70B": "groq_llama33_70b_benqa_human_gold_974_item_matrix.csv",
}

MACRO_SUBJECTS = ("Biology", "Chemistry", "Physics", "Math", "Science")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def macro_subject(item_id: str) -> str:
    stem = re.sub(r"^benqa_ext_", "", item_id)
    stem = re.sub(r"_\d+$", "", stem)
    for subject in MACRO_SUBJECTS:
        if subject.lower() in stem.lower():
            return subject
    raise ValueError(f"Cannot map id to macro subject: {item_id}")


def exact_binomial_cdf(k: int, n: int) -> float:
    return sum(math.comb(n, i) for i in range(k + 1)) / (2**n)


def mcnemar_exact_p(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2.0 * exact_binomial_cdf(min(b, c), n))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--table-output", type=Path, default=DEFAULT_TABLE)
    args = parser.parse_args()

    out_rows: list[dict[str, Any]] = []
    for label, name in MODELS.items():
        with (ANALYSIS / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 974:
            raise SystemExit(f"{label}: expected 974 rows, got {len(rows)}")
        groups: dict[str, list[dict[str, str]]] = {s: [] for s in MACRO_SUBJECTS}
        for row in rows:
            groups[macro_subject(row["id"])].append(row)
        for subject in MACRO_SUBJECTS:
            selected = groups[subject]
            n = len(selected)
            bn = sum(truthy(r["bangla_correct"]) for r in selected)
            bg = sum(truthy(r["banglish_clean_correct"]) for r in selected)
            en = sum(truthy(r["english_correct"]) for r in selected)
            losses = sum(
                truthy(r["bangla_correct"]) and not truthy(r["banglish_clean_correct"])
                for r in selected
            )
            gains = sum(
                (not truthy(r["bangla_correct"])) and truthy(r["banglish_clean_correct"])
                for r in selected
            )
            out_rows.append(
                {
                    "model": label,
                    "subject": subject,
                    "n": n,
                    "bangla_correct": bn,
                    "banglish_correct": bg,
                    "english_correct": en,
                    "bangla_acc": round(100 * bn / n, 2),
                    "banglish_acc": round(100 * bg / n, 2),
                    "english_acc": round(100 * en / n, 2),
                    "gap_banglish_minus_bangla_pts": round(100 * (bg - bn) / n, 2),
                    "banglish_losses_b": losses,
                    "banglish_gains_c": gains,
                    "mcnemar_exact_p": round(mcnemar_exact_p(losses, gains), 6),
                }
            )

    for path in (args.output, args.table_output):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(out_rows[0]))
            writer.writeheader()
            writer.writerows(out_rows)

    lines = [
        "# BEnQA Human-Gold 974 Per-Subject Script Gap",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "Macro-subject breakdown of the 974-row extension triads. The gap",
        "column is reviewed-Banglish accuracy minus Bangla accuracy in points;",
        "the p-value is a within-subject McNemar exact test.",
        "",
        f"- Machine-readable summary: `{args.output.relative_to(ROOT)}`",
        "- Builder: `scripts/analyze_extension_subject_breakdown.py`",
        "",
    ]
    for label in MODELS:
        lines += [
            f"## {label}",
            "",
            "| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for row in out_rows:
            if row["model"] != label:
                continue
            lines.append(
                f"| {row['subject']} | {row['n']} | {row['bangla_acc']}% | "
                f"{row['banglish_acc']}% | {row['english_acc']}% | "
                f"{row['gap_banglish_minus_bangla_pts']:+.2f} | "
                f"{row['banglish_losses_b']} | {row['banglish_gains_c']} | "
                f"{row['mcnemar_exact_p']:.4f} |"
            )
        lines.append("")
    args.report_output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"rows={len(out_rows)} report={args.report_output}")


if __name__ == "__main__":
    main()
