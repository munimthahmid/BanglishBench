#!/usr/bin/env python3
"""Audit BanglaMATH numeric-signature transfer across scripts."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NUMERIC_ITEMS = ROOT / "results/analysis/v5_banglamath_numeric_sensitivity_items.csv"
DEFAULT_STYLE_ITEMS = ROOT / "results/analysis/v5_response_style_drift_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_banglamath_numeric_transfer_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_banglamath_numeric_transfer_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglamath_numeric_transfer.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
VARIANTS = ("bangla", "banglish_clean", "english")


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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def load_numeric_index(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    rows = [
        row
        for row in read_csv(path)
        if row.get("dataset") == "banglamath" and row.get("variant") in VARIANTS
    ]
    if len(rows) != len(MODELS) * 56 * len(VARIANTS):
        raise SystemExit(f"Expected {len(MODELS) * 56 * len(VARIANTS)} numeric rows, got {len(rows)}")
    return {(row["model"], row["id"], row["variant"]): row for row in rows}


def load_style_index(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    rows = [
        row
        for row in read_csv(path)
        if row.get("dataset") == "banglamath" and row.get("variant") in VARIANTS
    ]
    if len(rows) != len(MODELS) * 56 * len(VARIANTS):
        raise SystemExit(f"Expected {len(MODELS) * 56 * len(VARIANTS)} style rows, got {len(rows)}")
    return {(row["model"], row["id"], row["variant"]): row for row in rows}


def build_item_rows(
    numeric_index: dict[tuple[str, str, str], dict[str, str]],
    style_index: dict[tuple[str, str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        item_ids = sorted({item_id for row_model, item_id, _variant in numeric_index if row_model == model})
        if len(item_ids) != 56:
            raise SystemExit(f"Expected 56 BanglaMATH ids for {model}, got {len(item_ids)}")
        for item_id in item_ids:
            bangla = numeric_index[(model, item_id, "bangla")]
            banglish = numeric_index[(model, item_id, "banglish_clean")]
            english = numeric_index[(model, item_id, "english")]
            banglish_style = style_index[(model, item_id, "banglish_clean")]
            bangla_raw = truthy(bangla["raw_full_numeric_signature"])
            english_raw = truthy(english["raw_full_numeric_signature"])
            banglish_raw = truthy(banglish["raw_full_numeric_signature"])
            bangla_correct = truthy(bangla["correct"])
            english_correct = truthy(english["correct"])
            banglish_correct = truthy(banglish["correct"])
            alt_raw_any = bangla_raw or english_raw
            alt_raw_both = bangla_raw and english_raw
            alt_correct_any = bangla_correct or english_correct
            rows.append(
                {
                    "model": model,
                    "id": item_id,
                    "gold": banglish["gold"],
                    "gold_numeric_values": banglish["gold_numeric_values"],
                    "bangla_correct": bangla_correct,
                    "banglish_correct": banglish_correct,
                    "english_correct": english_correct,
                    "bangla_raw_full_numeric_signature": bangla_raw,
                    "banglish_raw_full_numeric_signature": banglish_raw,
                    "english_raw_full_numeric_signature": english_raw,
                    "bangla_parsed_full_numeric_signature": truthy(
                        bangla["parsed_full_numeric_signature"]
                    ),
                    "banglish_parsed_full_numeric_signature": truthy(
                        banglish["parsed_full_numeric_signature"]
                    ),
                    "english_parsed_full_numeric_signature": truthy(
                        english["parsed_full_numeric_signature"]
                    ),
                    "alt_raw_signature_any": alt_raw_any,
                    "alt_raw_signature_both": alt_raw_both,
                    "alt_correct_any": alt_correct_any,
                    "banglish_retains_alt_raw_signature": alt_raw_any and banglish_raw,
                    "banglish_drops_alt_raw_signature": alt_raw_any and not banglish_raw,
                    "banglish_correct_given_alt_raw_signature": alt_raw_any
                    and banglish_correct,
                    "banglish_wrong_without_raw_number_given_alt_raw_signature": alt_raw_any
                    and truthy(banglish["wrong_without_raw_number"]),
                    "banglish_meta_given_alt_raw_signature": alt_raw_any
                    and truthy(banglish_style["meta_uncertainty"]),
                    "banglish_raw_has_any_number": truthy(banglish["raw_has_any_number"]),
                    "banglish_wrong_without_raw_number": truthy(
                        banglish["wrong_without_raw_number"]
                    ),
                    "banglish_meta_uncertainty": truthy(banglish_style["meta_uncertainty"]),
                    "bangla_raw_numeric_values": bangla["raw_numeric_values"],
                    "banglish_raw_numeric_values": banglish["raw_numeric_values"],
                    "english_raw_numeric_values": english["raw_numeric_values"],
                    "banglish_raw_excerpt": banglish["raw_excerpt"],
                }
            )
    return rows


def summarize_model(rows: list[dict[str, Any]], model: str) -> dict[str, Any]:
    selected = [row for row in rows if row["model"] == model]
    alt_raw = [row for row in selected if row["alt_raw_signature_any"]]
    both_raw = [row for row in selected if row["alt_raw_signature_both"]]
    alt_correct = [row for row in selected if row["alt_correct_any"]]
    return {
        "section": "model_summary",
        "model": model,
        "n": len(selected),
        "bangla_raw_signature": sum(row["bangla_raw_full_numeric_signature"] for row in selected),
        "banglish_raw_signature": sum(
            row["banglish_raw_full_numeric_signature"] for row in selected
        ),
        "english_raw_signature": sum(
            row["english_raw_full_numeric_signature"] for row in selected
        ),
        "alt_raw_signature_any": len(alt_raw),
        "alt_raw_signature_both": len(both_raw),
        "alt_correct_any": len(alt_correct),
        "banglish_retains_alt_raw_signature": sum(
            row["banglish_retains_alt_raw_signature"] for row in alt_raw
        ),
        "banglish_drops_alt_raw_signature": sum(
            row["banglish_drops_alt_raw_signature"] for row in alt_raw
        ),
        "banglish_correct_given_alt_raw_signature": sum(
            row["banglish_correct_given_alt_raw_signature"] for row in alt_raw
        ),
        "banglish_wrong_without_raw_number_given_alt_raw_signature": sum(
            row["banglish_wrong_without_raw_number_given_alt_raw_signature"]
            for row in alt_raw
        ),
        "banglish_meta_given_alt_raw_signature": sum(
            row["banglish_meta_given_alt_raw_signature"] for row in alt_raw
        ),
        "banglish_raw_signature_given_both_alt_raw": sum(
            row["banglish_raw_full_numeric_signature"] for row in both_raw
        ),
        "banglish_correct_given_both_alt_raw": sum(row["banglish_correct"] for row in both_raw),
        "banglish_correct_given_alt_correct": sum(row["banglish_correct"] for row in alt_correct),
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [summarize_model(item_rows, model) for model in MODELS]


def row_for(summary_rows: list[dict[str, Any]], model: str) -> dict[str, Any]:
    matches = [row for row in summary_rows if row["model"] == model]
    if len(matches) != 1:
        raise SystemExit(f"Expected one summary row for {model}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q25_3b = row_for(summary_rows, "Qwen2.5-3B")
    q25_7b = row_for(summary_rows, "Qwen2.5-7B 8-bit")
    qwen3 = row_for(summary_rows, "Qwen3-4B")

    lines = [
        "# Frozen-V5 BanglaMATH Numeric Transfer Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether BanglaMATH numeric-answer evidence",
        "transfers from Bangla or English into reviewed Banglish. It joins the",
        "numeric-signature sensitivity audit with response-style metadata and",
        "uses only frozen-v5 thesis-facing Qwen outputs.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- Qwen3-4B has at least one alternate script with the full raw numeric "
            f"signature on {qwen3['alt_raw_signature_any']}/56 BanglaMATH items, "
            f"but reviewed Banglish retains the signature on only "
            f"{qwen3['banglish_retains_alt_raw_signature']}/"
            f"{qwen3['alt_raw_signature_any']} and is correct on "
            f"{qwen3['banglish_correct_given_alt_raw_signature']}/"
            f"{qwen3['alt_raw_signature_any']}."
        ),
        (
            "- Qwen2.5 rows show even weaker Banglish numeric transfer: "
            f"{q25_3b['banglish_retains_alt_raw_signature']}/"
            f"{q25_3b['alt_raw_signature_any']} retained for 3B and "
            f"{q25_7b['banglish_retains_alt_raw_signature']}/"
            f"{q25_7b['alt_raw_signature_any']} retained for 7B."
        ),
        (
            "- When both Bangla and English have the full raw numeric signature, "
            f"Qwen3 reviewed Banglish retains it on "
            f"{qwen3['banglish_raw_signature_given_both_alt_raw']}/"
            f"{qwen3['alt_raw_signature_both']} items; Qwen2.5 rows retain "
            f"{q25_3b['banglish_raw_signature_given_both_alt_raw']}/"
            f"{q25_3b['alt_raw_signature_both']} and "
            f"{q25_7b['banglish_raw_signature_given_both_alt_raw']}/"
            f"{q25_7b['alt_raw_signature_both']}."
        ),
        (
            "- In Qwen3's alternate-raw-signature slice, reviewed Banglish emits "
            f"meta/uncertainty language on {qwen3['banglish_meta_given_alt_raw_signature']}/"
            f"{qwen3['alt_raw_signature_any']} and wrong no-number outputs on "
            f"{qwen3['banglish_wrong_without_raw_number_given_alt_raw_signature']}/"
            f"{qwen3['alt_raw_signature_any']}."
        ),
        "",
        "## Model Summary",
        "",
        "| Model | Alt raw signature | Both alt raw | Banglish raw signature | Retains alt raw | Banglish correct in alt-raw slice | Meta in alt-raw slice | No-number wrong in alt-raw slice |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            f"| {row['model']} | {row['alt_raw_signature_any']}/{row['n']} | "
            f"{row['alt_raw_signature_both']}/{row['n']} | "
            f"{row['banglish_raw_signature']}/{row['n']} | "
            f"{row['banglish_retains_alt_raw_signature']}/"
            f"{row['alt_raw_signature_any']} | "
            f"{row['banglish_correct_given_alt_raw_signature']}/"
            f"{row['alt_raw_signature_any']} | "
            f"{row['banglish_meta_given_alt_raw_signature']}/"
            f"{row['alt_raw_signature_any']} | "
            f"{row['banglish_wrong_without_raw_number_given_alt_raw_signature']}/"
            f"{row['alt_raw_signature_any']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- BanglaMATH is a low-accuracy stress test, but alternate scripts often",
            "  contain the gold numeric values that reviewed Banglish drops.",
            "- This supports the thesis framing that many Banglish failures are",
            "  script-conditioned transfer failures rather than impossible items.",
            "- Numeric signatures are optimistic and can credit intermediate reasoning",
            "  numbers, so this should be cited as behavioral transfer evidence, not",
            "  as final-answer accuracy.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--numeric-items", type=Path, default=DEFAULT_NUMERIC_ITEMS)
    parser.add_argument("--style-items", type=Path, default=DEFAULT_STYLE_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    numeric_index = load_numeric_index(args.numeric_items)
    style_index = load_style_index(args.style_items)
    item_rows = build_item_rows(numeric_index, style_index)
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report, summary_rows, args.items_output, args.summary_output)

    qwen3 = row_for(summary_rows, "Qwen3-4B")
    print(
        "items="
        f"{len(item_rows)} summary_rows={len(summary_rows)} "
        f"qwen3_alt_raw={qwen3['alt_raw_signature_any']}/56 "
        f"qwen3_banglish_retains={qwen3['banglish_retains_alt_raw_signature']}/"
        f"{qwen3['alt_raw_signature_any']} "
        f"qwen3_banglish_correct_alt_raw="
        f"{qwen3['banglish_correct_given_alt_raw_signature']}/"
        f"{qwen3['alt_raw_signature_any']} "
        f"report={args.report}"
    )


if __name__ == "__main__":
    main()
