#!/usr/bin/env python3
"""Analyze correctness variance across Banglish spelling variants.

For each item, the same question is shown under K+1 spellings (canonical spell0
plus spell1..K). We measure how often correctness flips across spellings of the
same item, the per-item correctness rate, and the swing (max-min) per item.
A large swing means Banglish robustness is unstable under realistic spelling
variation, upgrading the claim beyond "this one romanizer is harder".
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "results/runs"
ANALYSIS = ROOT / "results/analysis"
SPELLS = ["spell0", "spell1", "spell2", "spell3", "spell4"]

MODELS = {
    "Qwen2.5-3B": RUNS / "qwen25_3b_spelling_variants/results/runs/qwen25_3b_spelling_variants.jsonl",
    "Qwen3-4B": RUNS / "qwen3_4b_spelling_variants/results/runs/qwen3_4b_spelling_variants.jsonl",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-output", type=Path, default=ROOT / "reports/spelling_variation_robustness.md")
    args = parser.parse_args()

    summary_rows = []
    item_rows = []
    for label, path in MODELS.items():
        if not path.exists():
            print(f"SKIP {label}: {path} missing")
            continue
        by_item: dict[str, dict[str, int]] = defaultdict(dict)
        for line in path.open(encoding="utf-8"):
            r = json.loads(line)
            by_item[r["id"]][r["variant"]] = int(bool(r["correct"]))

        n_items = 0
        flip_items = 0  # items where correctness is not constant across spellings
        total_correct = 0
        total_slots = 0
        swing_sum = 0.0
        all_correct = 0
        all_wrong = 0
        per_spell_correct = {s: 0 for s in SPELLS}
        for item_id, vals in by_item.items():
            present = [s for s in SPELLS if s in vals]
            if len(present) < 2:
                continue
            n_items += 1
            cs = [vals[s] for s in present]
            for s in present:
                per_spell_correct[s] += vals[s]
            total_correct += sum(cs)
            total_slots += len(cs)
            rate = sum(cs) / len(cs)
            swing = max(cs) - min(cs)
            swing_sum += swing
            if swing > 0:
                flip_items += 1
            if all(cs):
                all_correct += 1
            if not any(cs):
                all_wrong += 1
            item_rows.append({"model": label, "id": item_id, "n_spellings": len(cs),
                              "correct_count": sum(cs), "rate": round(rate, 3), "flips": int(swing > 0)})

        summary_rows.append({
            "model": label,
            "items": n_items,
            "mean_correct_per_item": round(total_correct / n_items, 3),
            "overall_accuracy_pct": round(100 * total_correct / total_slots, 2),
            "items_with_flip": flip_items,
            "flip_rate_pct": round(100 * flip_items / n_items, 1),
            "all_spellings_correct": all_correct,
            "all_spellings_wrong": all_wrong,
            "mean_swing": round(swing_sum / n_items, 3),
            **{f"acc_{s}_pct": round(100 * per_spell_correct[s] / n_items, 1) for s in SPELLS},
        })

    if not summary_rows:
        raise SystemExit("No model outputs found yet.")

    out_csv = ANALYSIS / "spelling_variation_summary.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(summary_rows[0]))
        w.writeheader()
        w.writerows(summary_rows)
    with (ANALYSIS / "spelling_variation_items.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(item_rows[0]))
        w.writeheader()
        w.writerows(item_rows)

    lines = [
        "# Banglish Spelling-Variation Robustness",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "Each of 100 BEnQA items is evaluated under 5 spellings (canonical reviewed",
        "Banglish plus 4 seeded phonetic respellings that preserve digits, formulae,",
        "option labels, and the answer line). A flip means the model's correctness",
        "is not constant across spellings of the same item.",
        "",
        f"- Summary: `{out_csv.relative_to(ROOT)}`",
        "- Builder: `scripts/analyze_spelling_variation.py`",
        "",
        "| Model | Items | Acc % | Items with flip | Flip rate | All-correct | All-wrong | Mean swing |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in summary_rows:
        lines.append(
            f"| {r['model']} | {r['items']} | {r['overall_accuracy_pct']} | "
            f"{r['items_with_flip']} | {r['flip_rate_pct']}% | {r['all_spellings_correct']} | "
            f"{r['all_spellings_wrong']} | {r['mean_swing']} |"
        )
    lines += ["", "## Per-spelling accuracy", "",
              "| Model | " + " | ".join(SPELLS) + " |",
              "| --- | " + " | ".join(["---:"] * len(SPELLS)) + " |"]
    for r in summary_rows:
        lines.append("| " + r["model"] + " | " + " | ".join(f"{r[f'acc_{s}_pct']}%" for s in SPELLS) + " |")
    args.report_output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", args.report_output)
    for r in summary_rows:
        print(f"  {r['model']}: acc {r['overall_accuracy_pct']}% flip {r['flip_rate_pct']}% swing {r['mean_swing']}")


if __name__ == "__main__":
    main()
