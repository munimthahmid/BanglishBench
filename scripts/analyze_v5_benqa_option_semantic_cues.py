#!/usr/bin/env python3
"""Audit BEnQA option-label bias against simple option semantic cues."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_SWITCH_ITEMS = ROOT / "results/analysis/v5_benqa_option_switching_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_option_semantic_cues_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_option_semantic_cues_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_semantic_cues.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
OPTIONS = ("A", "B", "C", "D")
BASELINES = ("bangla", "english")
BASELINE_LABELS = {"bangla": "Bangla", "english": "English"}
OPTION_LINE_RE = re.compile(r"^([ABCD])\.\s*(.+)$", flags=re.MULTILINE)
ROMAN_MARKER_RE = re.compile(r"(?<![A-Za-z])(?:i|ii|iii|iv)(?![A-Za-z])", re.I)
MATH_OR_NUMERIC_RE = re.compile(
    r"(?:\\frac|\\degree|\\circ|\\AA|\\|[\^_{}=+\-−*/<>]|\d|degree)",
    re.I,
)
ALL_NONE_RE = re.compile(r"\b(?:sob|shob|sokol|konoti|kono|none|all|both|ubhoi)\b", re.I)


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


def valid_option(value: Any) -> str:
    parsed = str(value).strip().upper()
    return parsed if parsed in OPTIONS else ""


def is_composite(text: str) -> bool:
    lowered = f" {text.lower()} "
    return bool(ROMAN_MARKER_RE.search(text)) and (
        "," in text or "&" in text or " o " in lowered or " and " in lowered
    )


def cue_flags(text: str) -> dict[str, bool]:
    composite = is_composite(text)
    math_or_numeric = bool(MATH_OR_NUMERIC_RE.search(text))
    all_none = bool(ALL_NONE_RE.search(text))
    return {
        "composite": composite,
        "roman_marker": bool(ROMAN_MARKER_RE.search(text)),
        "math_or_numeric": math_or_numeric,
        "all_none_both": all_none,
        "semantic_cue": composite or math_or_numeric or all_none,
    }


def load_features(path: Path) -> dict[str, dict[str, Any]]:
    features: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("dataset") != "benqa":
                continue
            options = {
                match.group(1): match.group(2).strip()
                for match in OPTION_LINE_RE.finditer(row["banglish_clean"])
            }
            if set(options) != set(OPTIONS):
                raise SystemExit(f"Could not parse all options for {row['id']}")
            cues = {option: cue_flags(text) for option, text in options.items()}
            features[str(row["id"])] = {
                "id": row["id"],
                "gold": valid_option(row["answer"]),
                "subject": str(row.get("metadata", {}).get("subject") or row.get("domain", "")),
                **{f"{option}_text": options[option] for option in OPTIONS},
                **{
                    f"{option}_{flag}": cues[option][flag]
                    for option in OPTIONS
                    for flag in (
                        "composite",
                        "roman_marker",
                        "math_or_numeric",
                        "all_none_both",
                        "semantic_cue",
                    )
                },
            }
            for flag in ("composite", "math_or_numeric", "semantic_cue"):
                count = sum(cues[option][flag] for option in OPTIONS)
                features[str(row["id"])][f"D_unique_{flag}"] = cues["D"][flag] and count == 1
            features[str(row["id"])]["any_composite"] = any(
                cues[option]["composite"] for option in OPTIONS
            )
            features[str(row["id"])]["all_composite"] = all(
                cues[option]["composite"] for option in OPTIONS
            )
    if len(features) != 144:
        raise SystemExit(f"Expected 144 BEnQA feature rows, got {len(features)}")
    return features


def switch_index(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["model"], row["baseline_variant"], row["id"]): row
        for row in read_csv(path)
    }


def build_item_rows(choice_items: Path, switch_items: Path, validation: Path) -> list[dict[str, Any]]:
    features = load_features(validation)
    switches = switch_index(switch_items)
    rows: list[dict[str, Any]] = []
    for choice in read_csv(choice_items):
        model = choice["model"]
        if model not in MODELS:
            continue
        item_id = choice["id"]
        feature = features[item_id]
        row: dict[str, Any] = {
            "model": model,
            "id": item_id,
            "subject": feature["subject"],
            "gold": feature["gold"],
            "pred_option": valid_option(choice["banglish_clean_parsed_option"]) or "invalid",
            "correct": truthy(choice["banglish_clean_correct"]),
            "D_composite": feature["D_composite"],
            "D_math_or_numeric": feature["D_math_or_numeric"],
            "D_all_none_both": feature["D_all_none_both"],
            "D_semantic_cue": feature["D_semantic_cue"],
            "D_no_semantic_cue": not feature["D_semantic_cue"],
            "D_unique_composite": feature["D_unique_composite"],
            "D_unique_math_or_numeric": feature["D_unique_math_or_numeric"],
            "any_composite": feature["any_composite"],
            "all_composite": feature["all_composite"],
            "D_text": feature["D_text"],
        }
        for baseline in BASELINES:
            switch = switches[(model, baseline, item_id)]
            prefix = f"{baseline}_"
            row[f"{prefix}baseline_option"] = switch["baseline_option"]
            row[f"{prefix}baseline_correct_non_d"] = truthy(
                switch["baseline_correct_non_d"]
            )
            row[f"{prefix}non_d_to_D"] = truthy(switch["switched_non_d_to_d"])
            row[f"{prefix}correct_non_d_to_wrong_D"] = truthy(
                switch["baseline_correct_non_d_to_d_wrong"]
            )
        rows.append(row)
    expected = len(MODELS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} item rows, got {len(rows)}")
    return sorted(rows, key=lambda row: (row["model"], row["id"]))


def summarize_features(rows: list[dict[str, Any]]) -> dict[str, Any]:
    selected = [row for row in rows if row["model"] == MODELS[0]]
    return {
        "section": "item_features",
        "model": "all_items",
        "baseline_variant": "",
        "scope": "all",
        "scope_label": "All BEnQA items",
        "n": len(selected),
        "D_composite": sum(row["D_composite"] for row in selected),
        "D_math_or_numeric": sum(row["D_math_or_numeric"] for row in selected),
        "D_all_none_both": sum(row["D_all_none_both"] for row in selected),
        "D_semantic_cue": sum(row["D_semantic_cue"] for row in selected),
        "D_no_semantic_cue": sum(row["D_no_semantic_cue"] for row in selected),
        "D_unique_composite": sum(row["D_unique_composite"] for row in selected),
        "D_unique_math_or_numeric": sum(
            row["D_unique_math_or_numeric"] for row in selected
        ),
        "any_composite": sum(row["any_composite"] for row in selected),
        "all_composite": sum(row["all_composite"] for row in selected),
    }


def model_scopes() -> tuple[tuple[str, str, str], ...]:
    return (
        ("D_composite", "D is composite", "D_composite"),
        ("D_math_or_numeric", "D is numeric/formula-like", "D_math_or_numeric"),
        ("D_semantic_cue", "D has any semantic cue", "D_semantic_cue"),
        ("D_no_semantic_cue", "D has no semantic cue", "D_no_semantic_cue"),
    )


def switch_scopes() -> tuple[tuple[str, str, str], ...]:
    return (
        ("correct_non_d_D_semantic_cue", "Correct non-D baseline, D has cue", "D_semantic_cue"),
        (
            "correct_non_d_D_no_semantic_cue",
            "Correct non-D baseline, D has no cue",
            "D_no_semantic_cue",
        ),
    )


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = [summarize_features(rows)]
    for model in MODELS:
        model_rows = [row for row in rows if row["model"] == model]
        for scope, label, flag in model_scopes():
            selected = [row for row in model_rows if row[flag]]
            out.append(
                {
                    "section": "model_cue_bucket",
                    "model": model,
                    "baseline_variant": "",
                    "scope": scope,
                    "scope_label": label,
                    "n": len(selected),
                    "correct": sum(row["correct"] for row in selected),
                    "pred_D": sum(row["pred_option"] == "D" for row in selected),
                }
            )
        for baseline in BASELINES:
            prefix = f"{baseline}_"
            for scope, label, flag in switch_scopes():
                selected = [
                    row
                    for row in model_rows
                    if row[flag] and row[f"{prefix}baseline_correct_non_d"]
                ]
                out.append(
                    {
                        "section": "switch_cue_bucket",
                        "model": model,
                        "baseline_variant": baseline,
                        "baseline_label": BASELINE_LABELS[baseline],
                        "scope": scope,
                        "scope_label": label,
                        "n": len(selected),
                        "correct_non_d_to_wrong_D": sum(
                            row[f"{prefix}correct_non_d_to_wrong_D"]
                            for row in selected
                        ),
                    }
                )
    return out


def row_for(
    rows: list[dict[str, Any]],
    section: str,
    model: str,
    scope: str,
    baseline: str = "",
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == section
        and row["model"] == model
        and row["scope"] == scope
        and row.get("baseline_variant", "") == baseline
    )


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100 * num / den:.1f}%"


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    features = summary_rows[0]
    q3_no_cue = row_for(summary_rows, "model_cue_bucket", "Qwen3-4B", "D_no_semantic_cue")
    q25_3b_no_cue = row_for(
        summary_rows, "model_cue_bucket", "Qwen2.5-3B", "D_no_semantic_cue"
    )
    q25_7b_no_cue = row_for(
        summary_rows, "model_cue_bucket", "Qwen2.5-7B 8-bit", "D_no_semantic_cue"
    )
    q3_bangla_no_cue = row_for(
        summary_rows,
        "switch_cue_bucket",
        "Qwen3-4B",
        "correct_non_d_D_no_semantic_cue",
        "bangla",
    )
    q3_english_no_cue = row_for(
        summary_rows,
        "switch_cue_bucket",
        "Qwen3-4B",
        "correct_non_d_D_no_semantic_cue",
        "english",
    )
    q25_3b_bangla_no_cue = row_for(
        summary_rows,
        "switch_cue_bucket",
        "Qwen2.5-3B",
        "correct_non_d_D_no_semantic_cue",
        "bangla",
    )
    q25_7b_bangla_no_cue = row_for(
        summary_rows,
        "switch_cue_bucket",
        "Qwen2.5-7B 8-bit",
        "correct_non_d_D_no_semantic_cue",
        "bangla",
    )

    lines = [
        "# Frozen-V5 BEnQA Option Semantic-Cue Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the Qwen3 reviewed-Banglish BEnQA",
        "D-attractor is reducible to simple option cues: composite roman-marker",
        "answers such as `i, ii, o iii`, numeric/formula-like strings, or",
        "all/none/both markers. It uses only frozen-v5 option text plus existing",
        "choice-bias and option-switching rows.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            f"- D has a composite/numeric/formula cue on {features['D_semantic_cue']}/144 "
            f"BEnQA rows, leaving {features['D_no_semantic_cue']}/144 rows where D has no "
            "simple semantic cue under this audit."
        ),
        (
            "- On those no-cue rows, Qwen3 still predicts D on "
            f"{q3_no_cue['pred_D']}/{q3_no_cue['n']} rows "
            f"({pct(int(q3_no_cue['pred_D']), int(q3_no_cue['n']))}), versus "
            f"{q25_3b_no_cue['pred_D']}/{q25_3b_no_cue['n']} for Qwen2.5-3B and "
            f"{q25_7b_no_cue['pred_D']}/{q25_7b_no_cue['n']} for Qwen2.5-7B."
        ),
        (
            "- Among correct non-D alternate-script predictions where D has no cue, "
            "Qwen3 switches to wrong reviewed-Banglish D on "
            f"{q3_bangla_no_cue['correct_non_d_to_wrong_D']}/{q3_bangla_no_cue['n']} "
            f"Bangla rows and {q3_english_no_cue['correct_non_d_to_wrong_D']}/"
            f"{q3_english_no_cue['n']} English rows."
        ),
        (
            "- The corresponding Bangla-side Qwen2.5 counts are only "
            f"{q25_3b_bangla_no_cue['correct_non_d_to_wrong_D']}/"
            f"{q25_3b_bangla_no_cue['n']} and "
            f"{q25_7b_bangla_no_cue['correct_non_d_to_wrong_D']}/"
            f"{q25_7b_bangla_no_cue['n']}."
        ),
        "",
        "## No-Cue Bucket",
        "",
        "| Model | Correct | Pred D on D-no-cue rows | Bangla correct non-D -> wrong D | English correct non-D -> wrong D |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        cue = row_for(summary_rows, "model_cue_bucket", model, "D_no_semantic_cue")
        bangla = row_for(
            summary_rows, "switch_cue_bucket", model, "correct_non_d_D_no_semantic_cue", "bangla"
        )
        english = row_for(
            summary_rows, "switch_cue_bucket", model, "correct_non_d_D_no_semantic_cue", "english"
        )
        lines.append(
            "| {model} | {correct}/{n} | {pred_D}/{n} | {bd}/{bn} | {ed}/{en} |".format(
                model=model,
                correct=cue["correct"],
                pred_D=cue["pred_D"],
                n=cue["n"],
                bd=bangla["correct_non_d_to_wrong_D"],
                bn=bangla["n"],
                ed=english["correct_non_d_to_wrong_D"],
                en=english["n"],
            )
        )
    lines.extend(
        [
            "",
            "## Cue Feature Counts",
            "",
            f"- D composite: {features['D_composite']}/144.",
            f"- D numeric/formula-like: {features['D_math_or_numeric']}/144.",
            f"- D all/none/both marker: {features['D_all_none_both']}/144.",
            f"- Any option composite: {features['any_composite']}/144; all four options composite: {features['all_composite']}/144.",
            "",
            "## Interpretation",
            "",
            "- Composite and numeric/formula-like options are real local features, but",
            "  they do not explain away Qwen3's D-attractor: the strongest model still",
            "  over-selects D when D lacks these cues.",
            "- The audit is cue-based and behavioral. It should be cited as a confound",
            "  check, not as proof of an internal semantic mechanism.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_benqa_option_semantic_cues.py`",
            f"- Item rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--switch-items", type=Path, default=DEFAULT_SWITCH_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.choice_items, args.switch_items, args.validation)
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    q3_no_cue = row_for(summary_rows, "model_cue_bucket", "Qwen3-4B", "D_no_semantic_cue")
    q3_bangla_no_cue = row_for(
        summary_rows,
        "switch_cue_bucket",
        "Qwen3-4B",
        "correct_non_d_D_no_semantic_cue",
        "bangla",
    )
    q3_english_no_cue = row_for(
        summary_rows,
        "switch_cue_bucket",
        "Qwen3-4B",
        "correct_non_d_D_no_semantic_cue",
        "english",
    )
    print(
        "items={items} | summary_rows={summary} | "
        "qwen3_D_no_cue_predD={pred}/{n} | "
        "qwen3_correct_nonD_D_no_cue_wrongD=bangla:{bangla}/{bangla_n},"
        "english:{english}/{english_n} | report={report}".format(
            items=len(item_rows),
            summary=len(summary_rows),
            pred=q3_no_cue["pred_D"],
            n=q3_no_cue["n"],
            bangla=q3_bangla_no_cue["correct_non_d_to_wrong_D"],
            bangla_n=q3_bangla_no_cue["n"],
            english=q3_english_no_cue["correct_non_d_to_wrong_D"],
            english_n=q3_english_no_cue["n"],
            report=args.report_output,
        )
    )


if __name__ == "__main__":
    main()
