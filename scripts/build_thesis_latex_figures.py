#!/usr/bin/env python3
"""Build the four main thesis figures as vector PDFs for the LaTeX build.

Figures:
  1. fig_pipeline.pdf       — benchmark construction / evaluation pipeline
  2. fig_paired_gaps.pdf    — per-model script accuracies + Banglish-Bangla gap CIs
  3. fig_recoverability.pdf — recoverability decomposition of Banglish misses
  4. fig_token_cost.pdf     — token cost vs accuracy scatter (BEnQA, Qwen triad)

Run with the analysis venv:
  .venv-analysis/bin/python scripts/build_thesis_latex_figures.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "results/analysis"
FIGDIR = ROOT / "Thesis Template UG/figures"

COLORS = {"bangla": "#2a9d8f", "banglish": "#e76f51", "english": "#457b9d"}
SEED = 20260611

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 150,
    }
)


def truthy(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- data loading

QWEN_MODELS = [
    ("Qwen/Qwen2.5-3B-Instruct", "Qwen2.5-3B"),
    ("Qwen/Qwen2.5-7B-Instruct", "Qwen2.5-7B\n8-bit"),
    ("Qwen/Qwen3-4B-Instruct-2507", "Qwen3-4B"),
]
API_FILES = [
    ("gemini_3_5_flash_validation200_v5_items.csv", "Gemini 3.5\nFlash"),
    ("openai_gpt55_low_validation200_v5_cap1024_items.csv", "GPT-5.5\nlow"),
    ("claude_sonnet_4_6_validation200_v5_cap1024_items.csv", "Claude\nSonnet 4.6"),
    ("deepseek_v4_flash_validation200_v5_items.csv", "DeepSeek\nV4 Flash"),
    ("groq_llama33_70b_validation200_v5_items.csv", "Groq Llama\n3.3 70B"),
]


def load_pairs() -> dict[str, dict[str, list[tuple[bool, bool, bool]]]]:
    """model label -> list of (bangla, banglish, english) correctness per item."""
    out: dict[str, list[tuple[bool, bool, bool]]] = {}
    qwen_rows = read_csv(ANALYSIS / "validation200_v5_cross_script_failure_patterns_items.csv")
    for key, label in QWEN_MODELS:
        sel = [r for r in qwen_rows if r["model"] == key]
        out[label] = [
            (truthy(r["bangla_correct"]), truthy(r["banglish_clean_correct"]), truthy(r["english_correct"]))
            for r in sel
        ]
    for fname, label in API_FILES:
        rows = read_csv(ANALYSIS / fname)
        by_variant: dict[str, dict[str, bool]] = {}
        for r in rows:
            by_variant.setdefault(r["variant"], {})[r["id"]] = truthy(r["strict_correct"])
        ids = sorted(by_variant["banglish_clean"])
        out[label] = [
            (by_variant["bangla"][i], by_variant["banglish_clean"][i], by_variant["english"][i])
            for i in ids
        ]
    return out


def bootstrap_gap_ci(pairs: list[tuple[bool, bool, bool]], iters: int = 10000) -> tuple[float, float, float]:
    """Paired bootstrap CI for Banglish minus Bangla accuracy (points)."""
    rng = random.Random(SEED)
    n = len(pairs)
    point = 100.0 * sum(b - a for a, b, _ in pairs) / n
    deltas = []
    for _ in range(iters):
        s = 0
        for _ in range(n):
            a, b, _e = pairs[rng.randrange(n)]
            s += b - a
        deltas.append(100.0 * s / n)
    deltas.sort()
    return point, deltas[int(0.025 * iters)], deltas[int(0.975 * iters)]


# ------------------------------------------------------------------- figure 1


def fig_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#f2f4f7", ec="#30363d", bold=False, fs=8.6):
        ax.add_patch(
            FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.6", facecolor=fc, edgecolor=ec, linewidth=1.1
            )
        )
        ax.text(
            x + w / 2,
            y + h / 2,
            text,
            ha="center",
            va="center",
            fontsize=fs,
            fontweight="bold" if bold else "normal",
        )

    def arrow(x1, y1, x2, y2):
        ax.add_patch(
            FancyArrowPatch(
                (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color="#30363d", linewidth=1.2
            )
        )

    # Core track (top)
    box(1, 38, 16, 12, "Source tasks\nBEnQA 144 MCQ\nBanglaMATH 56 math")
    box(23, 38, 15, 12, "Rule-based\nromanizer\n(bn_romanize)")
    box(44, 38, 15, 12, "Targeted v5\nhuman review\n(high-impact rows)")
    box(65, 38, 15, 12, "Frozen\nvalidation-200 v5\n(all-200 policy)", fc="#dff0ec", bold=True)
    arrow(17.6, 44, 22.4, 44)
    arrow(38.6, 44, 43.4, 44)
    arrow(59.6, 44, 64.4, 44)

    # Extension track (bottom)
    box(1, 16, 16, 12, "BEnQA pool\n4,939 eligible rows\n(core excluded)")
    box(23, 16, 15, 12, "Subject-balanced\n1,000-row sample\n+ romanizer")
    box(44, 16, 15, 12, "Full human review\n618 accept / 356 edit\n/ 26 reject")
    box(65, 16, 15, 12, "BEnQA human-gold\n974 extension", fc="#dff0ec", bold=True)
    arrow(17.6, 22, 22.4, 22)
    arrow(38.6, 22, 43.4, 22)
    arrow(59.6, 22, 64.4, 22)

    # Shared evaluation stage (right)
    box(85.5, 27, 13.5, 18, "Paired triad\nevaluation\nBN / BG / EN\n\nstrict +\nsecondary", fc="#fdeee9", bold=True, fs=8.0)
    arrow(80.6, 44, 84.9, 39)
    arrow(80.6, 22, 84.9, 31)

    # Analyses ribbon (bottom)
    box(
        2,
        1,
        87,
        9,
        "Analyses: paired gaps + bootstrap CIs  |  McNemar exact tests  |  recoverability\n"
        "tokenization  |  subject breakdown  |  mitigation probes",
        fc="#eef1f6",
        fs=8.2,
    )
    arrow(92.2, 26.2, 80.0, 10.8)

    fig.savefig(FIGDIR / "fig_pipeline.pdf", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------- figure 2


def fig_paired_gaps(pairs: dict[str, list[tuple[bool, bool, bool]]]) -> None:
    labels = list(pairs)
    n_models = len(labels)
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9.4, 6.4), gridspec_kw={"height_ratios": [1.35, 1.0], "hspace": 0.42}
    )

    # Panel A: accuracies
    width = 0.26
    xs = list(range(n_models))
    for off, (script, key) in enumerate([("Bangla", 0), ("Reviewed Banglish", 1), ("English", 2)]):
        vals = [100.0 * sum(p[key] for p in pairs[m]) / len(pairs[m]) for m in labels]
        color = [COLORS["bangla"], COLORS["banglish"], COLORS["english"]][off]
        ax1.bar([x + (off - 1) * width for x in xs], vals, width, label=script, color=color)
    ax1.set_xticks(xs)
    ax1.set_xticklabels(labels, fontsize=8.5)
    ax1.set_ylabel("Strict accuracy (%)")
    ax1.set_ylim(0, 118)
    ax1.set_yticks([0, 20, 40, 60, 80, 100])
    ax1.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.02), fontsize=9)
    ax1.set_title("(a) Validation-200 v5 strict accuracy by script view", fontsize=10, pad=14)
    ax1.axvline(2.5, color="#aaaaaa", linestyle=":", linewidth=1)
    ax1.text(1.0, 102, "open Qwen triad", fontsize=8, color="#555555", ha="center", style="italic")
    ax1.text(5.5, 102, "frontier / API panel", fontsize=8, color="#555555", ha="center", style="italic")

    # Panel B: Banglish - Bangla gap with bootstrap CIs
    points, los, his = [], [], []
    for m in labels:
        pt, lo, hi = bootstrap_gap_ci(pairs[m])
        points.append(pt)
        los.append(pt - lo)
        his.append(hi - pt)
    ax2.errorbar(
        xs,
        points,
        yerr=[los, his],
        fmt="o",
        color=COLORS["banglish"],
        ecolor="#30363d",
        elinewidth=1.2,
        capsize=4,
        markersize=6,
    )
    ax2.axhline(0, color="#30363d", linewidth=1)
    ax2.axvline(2.5, color="#aaaaaa", linestyle=":", linewidth=1)
    ax2.set_xticks(xs)
    ax2.set_xticklabels(labels, fontsize=8.5)
    ax2.set_ylabel("Banglish $-$ Bangla (pts)")
    ax2.set_title("(b) Reviewed-Banglish minus Bangla gap with paired bootstrap 95% CI", fontsize=10)
    fig.savefig(FIGDIR / "fig_paired_gaps.pdf", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------- figure 3


def fig_recoverability() -> None:
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    ax.set_xlim(0, 600)
    ax.set_ylim(-0.4, 2.3)
    ax.axis("off")

    def seg(y, x0, w, color, label, count, text_color="white"):
        ax.barh(y, w, left=x0, height=0.52, color=color, edgecolor="white")
        if w > 40:
            ax.text(x0 + w / 2, y, f"{label}\n{count}", ha="center", va="center", fontsize=8.2, color=text_color)
        else:
            ax.text(x0 + w / 2, y + 0.45, f"{label}: {count}", ha="center", va="bottom", fontsize=7.6, color="#30363d")

    # Top bar: all 600 slots
    seg(1.8, 0, 137, "#8ab17d", "Banglish correct", "137/600")
    seg(1.8, 137, 463, "#d1495b", "Reviewed Banglish wrong", "463/600")

    # Bottom bar: decomposition of the 463 misses
    x = 137.0
    seg(0.6, x, 28, "#2a9d8f", "Bangla-only\nrecovery", 28)
    seg(0.6, x + 28, 81, "#457b9d", "English-only\nrecovery", 81)
    seg(0.6, x + 109, 76, "#6d597a", "Both\nrecover", 76)
    seg(0.6, x + 185, 278, "#6c757d", "All-script hard", 278)

    # connectors
    for x0, x1 in [(137, 137), (600, 600)]:
        ax.plot([x0, x1], [1.54, 0.87], color="#aaaaaa", linewidth=0.9, linestyle=":")
    ax.text(
        137 + 185 / 2,
        -0.32,
        "recoverable misses: 185/463 (40%)",
        ha="center",
        fontsize=8.6,
        color="#30363d",
        fontweight="bold",
    )
    ax.plot([137, 322], [-0.12, -0.12], color="#30363d", linewidth=1.4)
    ax.set_title(
        "Recoverability of reviewed-Banglish misses over 600 Qwen model-item slots (validation-200 v5)",
        fontsize=10,
    )
    fig.savefig(FIGDIR / "fig_recoverability.pdf", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------- figure 4


def fig_token_cost(pairs: dict[str, list[tuple[bool, bool, bool]]]) -> None:
    # BEnQA tokens-per-word (identical across the audited Qwen tokenizers)
    tokens_per_word = {"Bangla": 4.0242, "Reviewed Banglish": 2.4942, "English": 1.9545}
    qwen_rows = read_csv(ANALYSIS / "validation200_v5_cross_script_failure_patterns_items.csv")
    markers = {"Qwen2.5-3B": "o", "Qwen2.5-7B 8-bit": "s", "Qwen3-4B": "^"}
    model_keys = {
        "Qwen2.5-3B": "Qwen/Qwen2.5-3B-Instruct",
        "Qwen2.5-7B 8-bit": "Qwen/Qwen2.5-7B-Instruct",
        "Qwen3-4B": "Qwen/Qwen3-4B-Instruct-2507",
    }
    script_cols = {
        "Bangla": ("bangla_correct", COLORS["bangla"]),
        "Reviewed Banglish": ("banglish_clean_correct", COLORS["banglish"]),
        "English": ("english_correct", COLORS["english"]),
    }
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    for model_label, marker in markers.items():
        sel = [r for r in qwen_rows if r["model"] == model_keys[model_label] and r["dataset"] == "benqa"]
        for script, (col, color) in script_cols.items():
            acc = 100.0 * sum(truthy(r[col]) for r in sel) / len(sel)
            ax.scatter(
                tokens_per_word[script], acc, s=85, marker=marker, color=color, edgecolor="#30363d", zorder=3
            )
    # legends
    from matplotlib.lines import Line2D

    script_handles = [
        Line2D([], [], marker="o", linestyle="", color=c, markeredgecolor="#30363d", label=s)
        for s, (_col, c) in script_cols.items()
    ]
    model_handles = [
        Line2D([], [], marker=m, linestyle="", color="#888888", markeredgecolor="#30363d", label=lbl)
        for lbl, m in markers.items()
    ]
    leg1 = ax.legend(handles=script_handles, loc="upper right", frameon=False, fontsize=8.6, title="Script view")
    ax.add_artist(leg1)
    ax.legend(handles=model_handles, loc="lower left", frameon=False, fontsize=8.6, title="Model")
    ax.set_xlabel("Mean tokens per word (BEnQA, Qwen tokenizers)")
    ax.set_ylabel("BEnQA strict accuracy (%)")
    ax.set_title("Reviewed Banglish is token-cheaper than Bangla yet less accurate", fontsize=10)
    ax.annotate(
        "cheaper but worse",
        xy=(2.55, 30.5),
        xytext=(3.05, 27.5),
        fontsize=8.8,
        color="#d1495b",
        arrowprops=dict(arrowstyle="->", color="#d1495b"),
    )
    ax.set_xlim(1.5, 4.5)
    ax.set_ylim(24, 64)
    fig.savefig(FIGDIR / "fig_token_cost.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIGDIR.mkdir(parents=True, exist_ok=True)
    pairs = load_pairs()
    fig_pipeline()
    fig_paired_gaps(pairs)
    fig_recoverability()
    fig_token_cost(pairs)
    for name in ("fig_pipeline", "fig_paired_gaps", "fig_recoverability", "fig_token_cost"):
        path = FIGDIR / f"{name}.pdf"
        print(f"{path} {'OK' if path.exists() else 'MISSING'} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
