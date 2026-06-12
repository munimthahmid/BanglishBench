#!/usr/bin/env python3
"""Within-family Qwen scaling curve for the Banglish-Bangla gap on frozen v5.

Combines the newly run small-model triads (0.5B/1.5B Qwen2.5, 0.6B/1.7B Qwen3,
no-thinking) with the three thesis-facing models (3B/7B Qwen2.5, 4B Qwen3) from
the frozen validation-200 v5 failure-pattern matrix. Reports per-model paired
bootstrap CIs and McNemar exact tests for the Banglish-minus-Bangla gap, and
emits a gap-versus-size figure.
"""

from __future__ import annotations

import csv
import json
import math
import random
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "results/runs"
ANALYSIS = ROOT / "results/analysis"
FAILURES = ANALYSIS / "validation200_v5_cross_script_failure_patterns_items.csv"
FIGDIR = ROOT / "Thesis Template UG/figures"
SEED = 20260611

# (label, family, params_billion, source) ordered by size within family.
SMALL_RUNS = {
    "Qwen2.5-0.5B": (RUNS / "qwen2_5_0_5b_validation200_v5/results/runs/qwen2_5_0_5b_validation200_v5.jsonl"),
    "Qwen2.5-1.5B": (RUNS / "qwen2_5_1_5b_validation200_v5/results/runs/qwen2_5_1_5b_validation200_v5.jsonl"),
    "Qwen3-0.6B": (RUNS / "qwen3_0_6b_nothink_validation200_v5/results/runs/qwen3_0_6b_nothink_validation200_v5.jsonl"),
    "Qwen3-1.7B": (RUNS / "qwen3_1_7b_nothink_validation200_v5/results/runs/qwen3_1_7b_nothink_validation200_v5.jsonl"),
}
FAILURE_MODELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}
META = {
    "Qwen2.5-0.5B": ("Qwen2.5", 0.49),
    "Qwen2.5-1.5B": ("Qwen2.5", 1.54),
    "Qwen2.5-3B": ("Qwen2.5", 3.09),
    "Qwen2.5-7B": ("Qwen2.5", 7.62),
    "Qwen3-0.6B": ("Qwen3", 0.60),
    "Qwen3-1.7B": ("Qwen3", 1.72),
    "Qwen3-4B": ("Qwen3", 4.02),
}


def truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes"}


def load_small(path: Path) -> list[tuple[bool, bool]]:
    by_item: dict[str, dict[str, bool]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            r = json.loads(line)
            by_item.setdefault(r["id"], {})[r["variant"]] = bool(r["correct"])
    return [(by_item[i]["bangla"], by_item[i]["banglish_clean"]) for i in sorted(by_item)]


def load_failure(label_key: str) -> list[tuple[bool, bool]]:
    with FAILURES.open(encoding="utf-8", newline="") as handle:
        rows = [r for r in csv.DictReader(handle) if r["model"] == label_key]
    return [(truthy(r["bangla_correct"]), truthy(r["banglish_clean_correct"])) for r in rows]


def bootstrap_ci(pairs, iters=10000):
    rng = random.Random(SEED)
    n = len(pairs)
    point = 100.0 * sum(b - a for a, b in pairs) / n
    deltas = []
    for _ in range(iters):
        s = sum(pairs[rng.randrange(n)][1] - pairs[rng.randrange(n)][0] for _ in range(0))
        # paired: resample item index once per draw
        idxs = [rng.randrange(n) for _ in range(n)]
        s = sum(pairs[i][1] - pairs[i][0] for i in idxs)
        deltas.append(100.0 * s / n)
    deltas.sort()
    return point, deltas[int(0.025 * iters)], deltas[int(0.975 * iters)]


def mcnemar_p(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2.0 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / (2**n))


def main() -> None:
    data = {}
    for label, path in SMALL_RUNS.items():
        data[label] = load_small(path)
    for key, label in FAILURE_MODELS.items():
        data[label] = load_failure(key)

    rows = []
    for label, pairs in data.items():
        family, params = META[label]
        bn = sum(int(a) for a, _ in pairs)
        bg = sum(int(b) for _, b in pairs)
        losses = sum(a and not b for a, b in pairs)
        gains = sum((not a) and b for a, b in pairs)
        point, lo, hi = bootstrap_ci(pairs)
        rows.append(
            {
                "model": label,
                "family": family,
                "params_billion": params,
                "n": len(pairs),
                "bangla_correct": bn,
                "banglish_correct": bg,
                "gap_pts": round(point, 2),
                "ci_low": round(lo, 2),
                "ci_high": round(hi, 2),
                "mcnemar_p": round(mcnemar_p(losses, gains), 6),
            }
        )
    rows.sort(key=lambda r: (r["family"], r["params_billion"]))

    out_csv = ANALYSIS / "qwen_scaling_curve_v5.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Figure: gap vs params (log x), per family
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    colors = {"Qwen2.5": "#2a9d8f", "Qwen3": "#e76f51"}
    for family in ("Qwen2.5", "Qwen3"):
        fam = [r for r in rows if r["family"] == family]
        xs = [r["params_billion"] for r in fam]
        ys = [r["gap_pts"] for r in fam]
        los = [r["gap_pts"] - r["ci_low"] for r in fam]
        his = [r["ci_high"] - r["gap_pts"] for r in fam]
        ax.errorbar(xs, ys, yerr=[los, his], marker="o", color=colors[family],
                    capsize=3, label=family, linewidth=1.6, markersize=6)
        for r in fam:
            ax.annotate(r["model"].split("-")[-1], (r["params_billion"], r["gap_pts"]),
                        textcoords="offset points", xytext=(4, 5), fontsize=7.5, color=colors[family])
    ax.axhline(0, color="#30363d", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("Model size (billion parameters, log scale)")
    ax.set_ylabel("Banglish $-$ Bangla gap (pts)")
    ax.set_title("Within-family scaling: the Banglish gap widens with model size", fontsize=10)
    ax.legend(frameon=False, title="Family")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.savefig(FIGDIR / "fig_scaling_curve.pdf", bbox_inches="tight")
    plt.close(fig)

    # Report
    lines = [
        "# Within-Family Qwen Scaling Curve (frozen v5)",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "Banglish-minus-Bangla gap on the frozen validation-200 v5 slice across",
        "seven Qwen models. Small models (0.5B/1.5B Qwen2.5, 0.6B/1.7B Qwen3, all",
        "no-thinking for Qwen3) were run for this analysis; 3B/7B/4B reuse the",
        "frozen-v5 triad. CIs are paired bootstrap; p is McNemar exact.",
        "",
        f"- Table: `{out_csv.relative_to(ROOT)}`",
        "- Figure: `Thesis Template UG/figures/fig_scaling_curve.pdf`",
        "- Builder: `scripts/analyze_scaling_curve.py`",
        "",
        "| Model | Family | Params (B) | Bangla | Banglish | Gap (pts) | 95% CI | McNemar p |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |",
    ]
    for r in rows:
        lines.append(
            f"| {r['model']} | {r['family']} | {r['params_billion']} | "
            f"{r['bangla_correct']}/{r['n']} | {r['banglish_correct']}/{r['n']} | "
            f"{r['gap_pts']:+.1f} | [{r['ci_low']:+.1f}, {r['ci_high']:+.1f}] | {r['mcnemar_p']:.4f} |"
        )
    (ROOT / "reports/qwen_scaling_curve_v5.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"models={len(rows)} table={out_csv}")
    for r in rows:
        print(f"  {r['model']:14s} {r['params_billion']:>5}B gap {r['gap_pts']:+.1f} CI[{r['ci_low']:+.1f},{r['ci_high']:+.1f}] p={r['mcnemar_p']:.4f}")


if __name__ == "__main__":
    main()
