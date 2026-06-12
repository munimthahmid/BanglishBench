#!/usr/bin/env python3
"""Build a thesis-facing frontier API panel summary."""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_CSV = ROOT / "results/analysis/frontier_api_panel_validation200_v5.csv"
REPORT = ROOT / "reports/frontier_api_panel_validation200_v5.md"

MODELS = [
    {
        "label": "Gemini 3.5 Flash",
        "provider": "Google",
        "family": "Gemini",
        "summary": ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_summary.csv",
        "paired": ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_paired_gaps.csv",
        "raw": ROOT / "results/api_audit/gemini_3_5_flash_validation200_v5_raw.jsonl",
        "report": ROOT / "reports/gemini_3_5_flash_validation200_v5_results.md",
        "input_cost_per_mtok": 1.50,
        "output_cost_per_mtok": 9.00,
    },
    {
        "label": "GPT-5.5 low",
        "provider": "OpenAI",
        "family": "GPT",
        "summary": ROOT / "results/analysis/openai_gpt55_low_validation200_v5_cap1024_summary.csv",
        "paired": ROOT / "results/analysis/openai_gpt55_low_validation200_v5_cap1024_paired_gaps.csv",
        "raw": ROOT / "results/api_audit/openai_gpt55_low_validation200_v5_cap1024_raw.jsonl",
        "report": ROOT / "reports/openai_gpt55_low_validation200_v5_cap1024_results.md",
        "input_cost_per_mtok": 5.00,
        "output_cost_per_mtok": 30.00,
    },
    {
        "label": "Claude Sonnet 4.6",
        "provider": "Anthropic",
        "family": "Claude",
        "summary": ROOT / "results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_summary.csv",
        "paired": ROOT / "results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_paired_gaps.csv",
        "raw": ROOT / "results/api_audit/claude_sonnet_4_6_validation200_v5_cap1024_raw.jsonl",
        "report": ROOT / "reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md",
        "input_cost_per_mtok": 3.00,
        "output_cost_per_mtok": 15.00,
    },
    {
        "label": "DeepSeek V4 Flash",
        "provider": "DeepSeek",
        "family": "DeepSeek",
        "summary": ROOT / "results/analysis/deepseek_v4_flash_validation200_v5_summary.csv",
        "paired": ROOT / "results/analysis/deepseek_v4_flash_validation200_v5_paired_gaps.csv",
        "raw": ROOT / "results/api_audit/deepseek_v4_flash_validation200_v5_raw.jsonl",
        "report": ROOT / "reports/deepseek_v4_flash_validation200_v5_results.md",
        "input_cost_per_mtok": 0.14,
        "output_cost_per_mtok": 0.28,
    },
    {
        "label": "Groq Llama 3.3 70B",
        "provider": "Groq",
        "family": "Llama",
        "summary": ROOT / "results/analysis/groq_llama33_70b_validation200_v5_summary.csv",
        "paired": ROOT / "results/analysis/groq_llama33_70b_validation200_v5_paired_gaps.csv",
        "raw": ROOT / "results/api_audit/groq_llama33_70b_validation200_v5_raw.jsonl",
        "report": ROOT / "reports/groq_llama33_70b_validation200_v5_results.md",
        "input_cost_per_mtok": 0.59,
        "output_cost_per_mtok": 0.79,
    },
]

VARIANTS = ("bangla", "banglish_clean", "english")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


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


def by_dataset_variant(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["dataset"], row["variant"]): row for row in rows}


def paired_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["score_mode"], row["dataset"], row["comparison"]): row
        for row in rows
    }


def optional_int(value: Any) -> int:
    if value in ("", None):
        return 0
    return int(value)


def cost(raw_rows: list[dict[str, Any]], input_rate: float, output_rate: float) -> tuple[int, int, int, float]:
    input_tokens = sum(optional_int(row.get("usage_input_tokens")) for row in raw_rows)
    output_tokens = sum(optional_int(row.get("usage_output_tokens")) for row in raw_rows)
    reasoning_tokens = sum(optional_int(row.get("usage_thoughts_tokens")) for row in raw_rows)
    dollars = input_tokens / 1_000_000 * input_rate + output_tokens / 1_000_000 * output_rate
    return input_tokens, output_tokens, reasoning_tokens, dollars


def panel_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        summary = by_dataset_variant(read_csv(model["summary"]))
        paired = paired_lookup(read_csv(model["paired"]))
        raw = read_jsonl(model["raw"])
        input_tokens, output_tokens, reasoning_tokens, dollars = cost(
            raw,
            float(model["input_cost_per_mtok"]),
            float(model["output_cost_per_mtok"]),
        )
        finish_counts = Counter(str(row.get("finish_reason", "")) for row in raw)
        for score_mode, correct_key, acc_key in (
            ("strict", "strict_correct", "strict_accuracy"),
            ("secondary", "secondary_correct", "secondary_accuracy"),
        ):
            out: dict[str, Any] = {
                "model": model["label"],
                "provider": model["provider"],
                "family": model["family"],
                "score_mode": score_mode,
                "n": summary.get(("all", "bangla"), {}).get("n", ""),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "reasoning_tokens": reasoning_tokens,
                "estimated_cost_usd": f"{dollars:.4f}",
                "finish_stop": finish_counts.get("STOP", 0),
                "finish_max_tokens": finish_counts.get("MAX_TOKENS", 0),
                "raw_rows": len(raw),
                "report": rel(model["report"]),
            }
            for variant in VARIANTS:
                row = summary.get(("all", variant), {})
                out[f"{variant}_correct"] = row.get(correct_key, "")
                out[f"{variant}_accuracy"] = row.get(acc_key, "")
                out[f"{variant}_parsed_empty"] = row.get("parsed_empty", "")
                out[f"{variant}_format_max_tokens"] = row.get("finish_max_tokens", "")
            for comparison, slug in (
                ("Banglish - Bangla", "banglish_minus_bangla"),
                ("Banglish - English", "banglish_minus_english"),
            ):
                row = paired.get((score_mode, "all", comparison), {})
                out[f"{slug}_points"] = row.get("delta_points", "")
                out[f"{slug}_p"] = row.get("exact_binomial_p_two_sided", "")
            rows.append(out)
    return rows


def pct(value: str) -> str:
    if value == "":
        return ""
    return f"{float(value) * 100:.1f}%"


def write_report(rows: list[dict[str, Any]]) -> None:
    strict = [row for row in rows if row["score_mode"] == "strict"]
    secondary = [row for row in rows if row["score_mode"] == "secondary"]
    lines = [
        "# Frontier API Panel Validation-200 v5",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This report puts the completed paid/hosted frontier API audits on one",
        "frozen validation-200 v5 protocol. It is the main cross-family table for",
        "claim-boundary writing, not a leaderboard.",
        "",
        f"- Machine-readable panel CSV: `{rel(OUTPUT_CSV)}`",
        "- Scoring: strict parser plus secondary parser/unit sensitivity.",
        "- Prompting: provider-neutral answer-only manifest.",
        "- Claude Sonnet 4.6 uses the same 1024 output-token cap as the GPT-5.5",
        "  validation-200 audit.",
        "",
        "## Strict Accuracy And Gaps",
        "",
        "| Model | Bangla | Reviewed Banglish | English | BG-BN | BG-EN | MAX_TOKENS | Cost |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in strict:
        lines.append(
            f"| {row['model']} | {row['bangla_correct']}/200 ({pct(str(row['bangla_accuracy']))}) | "
            f"{row['banglish_clean_correct']}/200 ({pct(str(row['banglish_clean_accuracy']))}) | "
            f"{row['english_correct']}/200 ({pct(str(row['english_accuracy']))}) | "
            f"{float(row['banglish_minus_bangla_points']):+.1f} pts | "
            f"{float(row['banglish_minus_english_points']):+.1f} pts | "
            f"{row['finish_max_tokens']} | ${row['estimated_cost_usd']} |"
        )

    lines.extend(
        [
            "",
            "## Secondary Accuracy And Gaps",
            "",
            "| Model | Bangla | Reviewed Banglish | English | BG-BN | BG-EN |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in secondary:
        lines.append(
            f"| {row['model']} | {row['bangla_correct']}/200 ({pct(str(row['bangla_accuracy']))}) | "
            f"{row['banglish_clean_correct']}/200 ({pct(str(row['banglish_clean_accuracy']))}) | "
            f"{row['english_correct']}/200 ({pct(str(row['english_accuracy']))}) | "
            f"{float(row['banglish_minus_bangla_points']):+.1f} pts | "
            f"{float(row['banglish_minus_english_points']):+.1f} pts |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- GPT-5.5 low is the strongest boundary case: the reviewed-Banglish",
            "  population gap nearly collapses under secondary scoring.",
            "- Gemini 3.5 Flash remains strong but still has a strict",
            "  reviewed-Banglish deficit.",
            "- Claude Sonnet 4.6 is strong in absolute accuracy, but still has a",
            "  reviewed-Banglish deficit and is visibly less format-disciplined under",
            "  answer-only prompts.",
            "- DeepSeek V4 Flash and Groq-hosted Llama 3.3 70B show that the frontier",
            "  story is not monotonic: strong/hosted models can still have large",
            "  reviewed-Banglish deficits under the same prompt/parser protocol.",
            "- Groq Llama 3.3 70B is useful as a hosted-open reference, but it is not a",
            "  frontier-closed model and should not be over-weighted against GPT/Gemini.",
            "",
            "## Cost And Scope Boundary",
            "",
            "Costs are approximate text-token estimates from provider pricing checked on",
            "2026-06-05 and reported API token usage. They exclude account-level free",
            "credits, taxes, and any provider-specific billing nuances.",
            "",
            "Do not run full851 across every API model. DeepSeek V4 Flash is the only",
            "authorized full851 follow-up because it is cheap, validation-clean, and",
            "answers a scale question for a non-Qwen family. Groq is blocked from full851",
            "by daily request limits; Claude is too expensive and too verbose to justify",
            "a silver full851 run unless the thesis later needs a Claude-specific scale",
            "claim.",
            "",
            "## Source Reports",
            "",
        ]
    )
    for model in MODELS:
        lines.append(f"- {model['label']}: `{rel(model['report'])}`")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = panel_rows()
    write_csv(OUTPUT_CSV, rows)
    write_report(rows)
    print(f"rows={len(rows)} output={OUTPUT_CSV} report={REPORT}")


if __name__ == "__main__":
    main()
