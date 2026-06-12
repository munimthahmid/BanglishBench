#!/usr/bin/env python3
"""Analyze whether the Banglish-Bangla gap survives prompt/decoding changes.

Compares Qwen2.5-3B on validation-200 v5 under the frozen baseline (greedy)
against three robustness conditions: two neutral alternate prompt templates and
one temperature=0.7 decoding variant. If the Banglish-minus-Bangla gap stays
negative and similar across conditions, the gap is not a prompt or decoding
artifact.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "results/runs"
ANALYSIS = ROOT / "results/analysis"
FAILURES = ANALYSIS / "validation200_v5_cross_script_failure_patterns_items.csv"

CONDITIONS = {
    "baseline (greedy)": None,  # from frozen failure matrix
    "neutral template B": RUNS / "qwen25_3b_v5_promptsens/results/runs/qwen25_3b_v5_promptsens_neutral_terse_t0.jsonl",
    "neutral template C": RUNS / "qwen25_3b_v5_promptsens/results/runs/qwen25_3b_v5_promptsens_neutral_role_t0.jsonl",
    "temperature 0.7": RUNS / "qwen25_3b_v5_promptsens/results/runs/qwen25_3b_v5_promptsens_baseline_t07.jsonl",
}


def truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes"}


def baseline_counts():
    with FAILURES.open(encoding="utf-8", newline="") as h:
        rows = [r for r in csv.DictReader(h) if r["model"] == "Qwen/Qwen2.5-3B-Instruct"]
    bn = sum(truthy(r["bangla_correct"]) for r in rows)
    bg = sum(truthy(r["banglish_clean_correct"]) for r in rows)
    en = sum(truthy(r["english_correct"]) for r in rows)
    return bn, bg, en, len(rows)


def run_counts(path: Path):
    by_item: dict[str, dict[str, int]] = defaultdict(dict)
    for line in path.open(encoding="utf-8"):
        r = json.loads(line)
        by_item[r["id"]][r["variant"]] = int(bool(r["correct"]))
    bn = sum(v.get("bangla", 0) for v in by_item.values())
    bg = sum(v.get("banglish_clean", 0) for v in by_item.values())
    en = sum(v.get("english", 0) for v in by_item.values())
    return bn, bg, en, len(by_item)


def main() -> None:
    rows = []
    for label, path in CONDITIONS.items():
        if path is None:
            bn, bg, en, n = baseline_counts()
        elif path.exists():
            bn, bg, en, n = run_counts(path)
        else:
            print(f"SKIP {label}: {path} missing")
            continue
        rows.append({
            "condition": label, "n": n,
            "bangla": bn, "banglish": bg, "english": en,
            "gap_banglish_minus_bangla_pts": round(100 * (bg - bn) / n, 1),
            "gap_banglish_minus_english_pts": round(100 * (bg - en) / n, 1),
        })

    if len(rows) < 2:
        raise SystemExit("Need at least baseline + one condition.")

    out_csv = ANALYSIS / "prompt_sensitivity_summary.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    lines = [
        "# Prompt and Decoding Sensitivity (Qwen2.5-3B, validation-200 v5)",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "The Banglish-minus-Bangla gap under the frozen baseline versus two neutral",
        "alternate prompt templates and a temperature=0.7 decoding variant. Neutral",
        "templates contain no Banglish hint, so they test prompt-wording sensitivity.",
        "",
        f"- Table: `{out_csv.relative_to(ROOT)}`",
        "- Builder: `scripts/analyze_prompt_sensitivity.py`",
        "",
        "| Condition | Bangla | Banglish | English | Banglish-Bangla | Banglish-English |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in rows:
        lines.append(
            f"| {r['condition']} | {r['bangla']}/{r['n']} | {r['banglish']}/{r['n']} | "
            f"{r['english']}/{r['n']} | {r['gap_banglish_minus_bangla_pts']:+.1f} pts | "
            f"{r['gap_banglish_minus_english_pts']:+.1f} pts |"
        )
    (ROOT / "reports/prompt_sensitivity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote reports/prompt_sensitivity.md")
    for r in rows:
        print(f"  {r['condition']}: BG-BN {r['gap_banglish_minus_bangla_pts']:+.1f}")


if __name__ == "__main__":
    main()
