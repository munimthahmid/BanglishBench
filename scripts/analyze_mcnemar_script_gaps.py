#!/usr/bin/env python3
"""McNemar exact tests with Holm correction for all Bangla-vs-Banglish contrasts.

Covers three panels:
  A. Frozen validation-200 v5 Qwen triad (strict scoring).
  B. Frozen validation-200 v5 frontier/API panel (strict and secondary scoring).
  C. BEnQA human-reviewed gold 974 extension (strict scoring).

For each model we form paired binary outcomes per item under two conditions
(Bangla prompt vs reviewed-Banglish prompt; English vs Banglish as secondary
contrast). The McNemar exact test uses only the discordant pairs:
  b = Bangla-only correct (Banglish loses), c = Banglish-only correct (gains).
Exact two-sided p is the binomial tail doubling over b + c trials at 0.5.
The McNemar odds ratio is b / c (Haldane-corrected when a cell is zero),
with a 95% CI from the log-odds normal approximation.
Holm correction is applied across models within each panel/scoring family.
"""

from __future__ import annotations

import argparse
import csv
import math
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "results/analysis"
DEFAULT_OUTPUT = ANALYSIS / "mcnemar_script_gaps.csv"
DEFAULT_REPORT = ROOT / "reports/mcnemar_script_gaps.md"

QWEN_FAILURES = ANALYSIS / "validation200_v5_cross_script_failure_patterns_items.csv"
QWEN_MODELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}

API_FILES = {
    "Gemini 3.5 Flash": "gemini_3_5_flash_validation200_v5_items.csv",
    "GPT-5.5 low": "openai_gpt55_low_validation200_v5_cap1024_items.csv",
    "Claude Sonnet 4.6": "claude_sonnet_4_6_validation200_v5_cap1024_items.csv",
    "DeepSeek V4 Flash": "deepseek_v4_flash_validation200_v5_items.csv",
    "Groq Llama 3.3 70B": "groq_llama33_70b_validation200_v5_items.csv",
}

EXT_FILES = {
    "Qwen2.5-3B": "qwen25_3b_benqa_human_gold_974_item_matrix.csv",
    "Gemini 3.5 Flash": "gemini_3_5_flash_benqa_human_gold_974_item_matrix.csv",
    "GPT-5.5 none": "openai_gpt55_none_benqa_human_gold_974_item_matrix.csv",
    "Claude Sonnet 4.6": "claude_sonnet_4_6_benqa_human_gold_974_item_matrix.csv",
    "DeepSeek V4 Flash": "deepseek_v4_flash_benqa_human_gold_974_item_matrix.csv",
    "Groq Llama 3.3 70B": "groq_llama33_70b_benqa_human_gold_974_item_matrix.csv",
}

COMPARISONS = (("bangla", "Bangla"), ("english", "English"))


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def exact_binomial_cdf(k: int, n: int) -> float:
    return sum(math.comb(n, i) for i in range(k + 1)) / (2**n)


def mcnemar_exact_p(b: int, c: int) -> float:
    """Exact two-sided McNemar p over discordant pairs b (losses) and c (gains)."""
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2.0 * exact_binomial_cdf(min(b, c), n))


def odds_ratio_ci(b: int, c: int) -> tuple[float, float, float]:
    """McNemar conditional odds ratio b/c with Haldane correction and 95% CI."""
    bb, cc = b + 0.5, c + 0.5
    orr = bb / cc
    se = math.sqrt(1.0 / bb + 1.0 / cc)
    lo = math.exp(math.log(orr) - 1.96 * se)
    hi = math.exp(math.log(orr) + 1.96 * se)
    return orr, lo, hi


def holm(pvalues: list[float]) -> list[float]:
    """Holm step-down adjusted p-values."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj = min(1.0, (m - rank) * pvalues[idx])
        running_max = max(running_max, adj)
        adjusted[idx] = running_max
    return adjusted


def summarize_pairs(
    panel: str,
    scoring: str,
    model: str,
    comparison: str,
    pairs: list[tuple[bool, bool]],
) -> dict[str, Any]:
    """pairs: (baseline_correct, banglish_correct) per item."""
    n = len(pairs)
    base = sum(int(a) for a, _ in pairs)
    bang = sum(int(b) for _, b in pairs)
    losses = sum(a and not b for a, b in pairs)  # baseline-only correct
    gains = sum((not a) and b for a, b in pairs)  # banglish-only correct
    p = mcnemar_exact_p(losses, gains)
    orr, lo, hi = odds_ratio_ci(losses, gains)
    return {
        "panel": panel,
        "scoring": scoring,
        "model": model,
        "comparison": f"banglish_vs_{comparison}",
        "n": n,
        "baseline_correct": base,
        "banglish_correct": bang,
        "delta_pts": round(100.0 * (bang - base) / n, 2),
        "banglish_losses_b": losses,
        "banglish_gains_c": gains,
        "discordant": losses + gains,
        "mcnemar_exact_p": p,
        "odds_ratio": round(orr, 3),
        "odds_ratio_ci_low": round(lo, 3),
        "odds_ratio_ci_high": round(hi, 3),
    }


def qwen_panel() -> list[dict[str, Any]]:
    rows = read_csv(QWEN_FAILURES)
    if len(rows) != 600:
        raise SystemExit(f"Expected 600 Qwen failure rows, got {len(rows)}")
    out = []
    for model, label in QWEN_MODELS.items():
        selected = [r for r in rows if r["model"] == model]
        if len(selected) != 200:
            raise SystemExit(f"{label}: expected 200 rows, got {len(selected)}")
        for key, _ in COMPARISONS:
            col = "bangla_correct" if key == "bangla" else "english_correct"
            pairs = [(truthy(r[col]), truthy(r["banglish_clean_correct"])) for r in selected]
            out.append(summarize_pairs("validation200_v5_qwen", "strict", label, key, pairs))
    return out


def api_panel() -> list[dict[str, Any]]:
    out = []
    for label, name in API_FILES.items():
        rows = read_csv(ANALYSIS / name)
        for scoring, col in (("strict", "strict_correct"), ("secondary", "secondary_correct")):
            by_variant: dict[str, dict[str, bool]] = {}
            for r in rows:
                by_variant.setdefault(r["variant"], {})[r["id"]] = truthy(r[col])
            ids = sorted(by_variant["banglish_clean"])
            if len(ids) != 200:
                raise SystemExit(f"{label}: expected 200 ids, got {len(ids)}")
            for key, _ in COMPARISONS:
                pairs = [(by_variant[key][i], by_variant["banglish_clean"][i]) for i in ids]
                out.append(summarize_pairs("validation200_v5_api", scoring, label, key, pairs))
    return out


def extension_panel() -> list[dict[str, Any]]:
    out = []
    for label, name in EXT_FILES.items():
        rows = read_csv(ANALYSIS / name)
        if len(rows) != 974:
            raise SystemExit(f"{label}: expected 974 rows, got {len(rows)}")
        for key, _ in COMPARISONS:
            col = "bangla_correct" if key == "bangla" else "english_correct"
            pairs = [(truthy(r[col]), truthy(r["banglish_clean_correct"])) for r in rows]
            out.append(summarize_pairs("benqa_human_gold_974", "strict", label, key, pairs))
    return out


def apply_holm(rows: list[dict[str, Any]]) -> None:
    """Holm across models within each (panel, scoring, comparison) family."""
    families: dict[tuple[str, str, str], list[int]] = {}
    for idx, row in enumerate(rows):
        families.setdefault((row["panel"], row["scoring"], row["comparison"]), []).append(idx)
    for indices in families.values():
        adjusted = holm([rows[i]["mcnemar_exact_p"] for i in indices])
        for i, adj in zip(indices, adjusted):
            rows[i]["mcnemar_p_holm"] = adj


def fmt_p(p: float) -> str:
    if p < 1e-4:
        return "<0.0001"
    return f"{p:.4f}"


def write_report(path: Path, rows: list[dict[str, Any]], output_csv: Path) -> None:
    lines = [
        "# McNemar Exact Tests for Script Gaps",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "Paired binary outcomes per item under two prompt scripts form the",
        "textbook McNemar setting. For each model we report the discordant-pair",
        "counts (b = baseline-script-only correct, c = Banglish-only correct),",
        "the exact two-sided McNemar p-value, the conditional odds ratio b/c",
        "(Haldane-corrected, 95% CI), and Holm-adjusted p-values across models",
        "within each panel/scoring family.",
        "",
        f"- Machine-readable summary: `{output_csv.relative_to(ROOT)}`",
        "- Builder: `scripts/analyze_mcnemar_script_gaps.py`",
        "",
    ]
    panels = [
        ("validation200_v5_qwen", "strict", "Validation-200 v5 Qwen triad (strict)"),
        ("validation200_v5_api", "strict", "Validation-200 v5 API panel (strict)"),
        ("validation200_v5_api", "secondary", "Validation-200 v5 API panel (secondary)"),
        ("benqa_human_gold_974", "strict", "BEnQA human-gold 974 extension (strict)"),
    ]
    for panel, scoring, title in panels:
        for comp, comp_label in COMPARISONS:
            selected = [
                r
                for r in rows
                if r["panel"] == panel
                and r["scoring"] == scoring
                and r["comparison"] == f"banglish_vs_{comp}"
            ]
            if not selected:
                continue
            lines += [
                f"## {title} — Banglish vs {comp_label}",
                "",
                f"| Model | {comp_label} | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |",
                "| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
            ]
            for r in selected:
                lines.append(
                    f"| {r['model']} | {r['baseline_correct']}/{r['n']} | "
                    f"{r['banglish_correct']}/{r['n']} | {r['delta_pts']:+.2f} pts | "
                    f"{r['banglish_losses_b']} | {r['banglish_gains_c']} | "
                    f"{r['odds_ratio']} [{r['odds_ratio_ci_low']}, {r['odds_ratio_ci_high']}] | "
                    f"{fmt_p(r['mcnemar_exact_p'])} | {fmt_p(r['mcnemar_p_holm'])} |"
                )
            lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = qwen_panel() + api_panel() + extension_panel()
    apply_holm(rows)
    for row in rows:
        row["mcnemar_exact_p"] = round(row["mcnemar_exact_p"], 6)
        row["mcnemar_p_holm"] = round(row["mcnemar_p_holm"], 6)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_report(args.report_output, rows, args.output)
    print(f"rows={len(rows)} report={args.report_output}")


if __name__ == "__main__":
    main()
