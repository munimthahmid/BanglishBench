#!/usr/bin/env python3
"""Analyze the LoRA Banglish-mitigation experiment.

Reads the dev-sanity and frozen validation-200 v5 triad runs for base / arm A
(Banglish-only) / arm B (mixed), and reports:
  - dev200 sanity: did the adapter beat base on Banglish dev rows?
  - frozen v5: per-arm Bangla/Banglish/English accuracy and the Banglish-Bangla
    gap, with the three key deltas vs base (Banglish, Bangla, English), each with
    a paired bootstrap CI and a McNemar exact test.

Headline metric is gap shrinkage, not Banglish accuracy: only a Banglish-Bangla
gap moving toward zero while Bangla/English hold counts as script mitigation.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "results/runs/lora_eval"
ANALYSIS = ROOT / "results/analysis"
FAILURES = ANALYSIS / "validation200_v5_cross_script_failure_patterns_items.csv"
SEED = 20260611

DEV = {
    "base": RUNS / "lora_dev_base.jsonl",
    "armA": RUNS / "lora_dev_armA.jsonl",
    "armB": RUNS / "lora_dev_armB.jsonl",
}
V5 = {
    "armA": RUNS / "lora_v5_armA.jsonl",
    "armB": RUNS / "lora_v5_armB.jsonl",
}
VIEWS = ("bangla", "banglish_clean", "english")


def truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes"}


def load_run(path: Path) -> dict[str, dict[str, int]]:
    by_item: dict[str, dict[str, int]] = defaultdict(dict)
    for line in path.open(encoding="utf-8"):
        r = json.loads(line)
        by_item[r["id"]][r["variant"]] = int(bool(r["correct"]))
    return by_item


def base_v5() -> dict[str, dict[str, int]]:
    by_item: dict[str, dict[str, int]] = defaultdict(dict)
    with FAILURES.open(encoding="utf-8", newline="") as h:
        for r in csv.DictReader(h):
            if r["model"] != "Qwen/Qwen2.5-3B-Instruct":
                continue
            by_item[r["id"]]["bangla"] = int(truthy(r["bangla_correct"]))
            by_item[r["id"]]["banglish_clean"] = int(truthy(r["banglish_clean_correct"]))
            by_item[r["id"]]["english"] = int(truthy(r["english_correct"]))
    return by_item


def acc(by_item, view) -> tuple[int, int]:
    vals = [v[view] for v in by_item.values() if view in v]
    return sum(vals), len(vals)


def paired_delta_ci(a_run, b_run, view, iters=10000):
    """b minus a (points) over shared items, paired bootstrap CI."""
    ids = [i for i in a_run if view in a_run[i] and i in b_run and view in b_run[i]]
    pairs = [(a_run[i][view], b_run[i][view]) for i in ids]
    n = len(pairs)
    point = 100.0 * sum(b - a for a, b in pairs) / n
    rng = random.Random(SEED)
    deltas = []
    for _ in range(iters):
        idxs = [rng.randrange(n) for _ in range(n)]
        deltas.append(100.0 * sum(pairs[i][1] - pairs[i][0] for i in idxs) / n)
    deltas.sort()
    b_only = sum((not a) and bb for a, bb in pairs)
    a_only = sum(a and (not bb) for a, bb in pairs)
    nn = a_only + b_only
    p = 1.0 if nn == 0 else min(1.0, 2.0 * sum(math.comb(nn, k) for k in range(min(a_only, b_only) + 1)) / (2**nn))
    return point, deltas[int(0.025 * iters)], deltas[int(0.975 * iters)], p


def gap(by_item):
    bn, n = acc(by_item, "bangla")
    bg, _ = acc(by_item, "banglish_clean")
    return 100.0 * (bg - bn) / n


def main() -> None:
    missing = [p for p in list(DEV.values()) + list(V5.values()) if not p.exists()]
    if missing:
        raise SystemExit("Missing LoRA eval outputs: " + ", ".join(str(m) for m in missing))

    dev = {k: load_run(p) for k, p in DEV.items()}
    v5 = {"base": base_v5(), "armA": load_run(V5["armA"]), "armB": load_run(V5["armB"])}

    lines = [
        "# LoRA Banglish-Mitigation Results (Qwen2.5-3B)",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "Arm A trains on Banglish-only completions; arm B on a 1:1:1 Bangla/",
        "Banglish/English mix. Training data is disjoint from validation-200 v5 and",
        "the 1,000-row extension (asserted in the build). Headline metric is gap",
        "shrinkage, not Banglish accuracy.",
        "",
        "## Dev-200 sanity (held-out, never trained)",
        "",
        "| Condition | Bangla | Banglish | English |",
        "| --- | ---: | ---: | ---: |",
    ]
    for k in ("base", "armA", "armB"):
        d = dev[k]
        row = " | ".join(f"{acc(d, v)[0]}/{acc(d, v)[1]}" for v in VIEWS)
        lines.append(f"| {k} | {row} |")
    # dev banglish deltas vs base
    da_pt, da_lo, da_hi, da_p = paired_delta_ci(dev["base"], dev["armA"], "banglish_clean")
    db_pt, db_lo, db_hi, db_p = paired_delta_ci(dev["base"], dev["armB"], "banglish_clean")
    lines += [
        "",
        f"Dev Banglish gain vs base: arm A {da_pt:+.1f} pts (CI [{da_lo:+.1f}, {da_hi:+.1f}], "
        f"McNemar p={da_p:.4f}); arm B {db_pt:+.1f} pts (CI [{db_lo:+.1f}, {db_hi:+.1f}], p={db_p:.4f}).",
        "",
        "## Frozen validation-200 v5 triad",
        "",
        "| Condition | Bangla | Banglish | English | Banglish-Bangla gap |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for k in ("base", "armA", "armB"):
        b = v5[k]
        bn, n = acc(b, "bangla")
        bg, _ = acc(b, "banglish_clean")
        en, _ = acc(b, "english")
        lines.append(f"| {k} | {bn}/{n} | {bg}/{n} | {en}/{n} | {gap(b):+.1f} pts |")

    lines += [
        "",
        "## Deltas vs base on frozen v5 (paired bootstrap CI, McNemar exact p)",
        "",
        "| Arm | View | Delta vs base | 95% CI | McNemar p |",
        "| --- | --- | ---: | --- | ---: |",
    ]
    rows_csv = []
    for arm in ("armA", "armB"):
        for view, vlabel in (("banglish_clean", "Banglish"), ("bangla", "Bangla"), ("english", "English")):
            pt, lo, hi, p = paired_delta_ci(v5["base"], v5[arm], view)
            lines.append(f"| {arm} | {vlabel} | {pt:+.1f} pts | [{lo:+.1f}, {hi:+.1f}] | {p:.4f} |")
            rows_csv.append({"arm": arm, "view": vlabel, "delta_pts": round(pt, 2),
                             "ci_low": round(lo, 2), "ci_high": round(hi, 2), "mcnemar_p": round(p, 6)})

    base_gap = gap(v5["base"])
    lines += [
        "",
        "## Interpretation",
        "",
        f"Base Banglish-Bangla gap: {base_gap:+.1f} pts. "
        f"Arm A gap: {gap(v5['armA']):+.1f} pts. Arm B gap: {gap(v5['armB']):+.1f} pts.",
        "",
        "Script mitigation requires the Banglish-Bangla gap to move toward zero",
        "while Bangla and English do not significantly regress. If all three views",
        "rise by a similar amount, the adapter learned the task, not the script.",
    ]
    (ROOT / "reports/lora_mitigation_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (ANALYSIS / "lora_mitigation_deltas.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows_csv[0]))
        w.writeheader()
        w.writerows(rows_csv)
    print("wrote reports/lora_mitigation_results.md")
    for k in ("base", "armA", "armB"):
        b = v5[k]
        print(f"  v5 {k}: BN {acc(b,'bangla')[0]} BG {acc(b,'banglish_clean')[0]} EN {acc(b,'english')[0]} gap {gap(b):+.1f}")


if __name__ == "__main__":
    main()
