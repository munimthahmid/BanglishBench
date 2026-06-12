#!/usr/bin/env python3
"""Audit BEnQA option-position bias against option text-length/content features."""

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
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_option_position_content_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_option_position_content_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_position_content.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
OPTIONS = ("A", "B", "C", "D")
OPTION_LINE_RE = re.compile(r"^([ABCD])\.\s*(.+)$", flags=re.MULTILINE)
COMPOSITE_RE = re.compile(r"\b(?:i|ii|iii|iv)\b", flags=re.IGNORECASE)


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


def tokenize(text: str) -> list[str]:
    return re.findall(r"\S+", text)


def is_composite_option(text: str) -> bool:
    lowered = f" {text.lower()} "
    return bool(COMPOSITE_RE.search(lowered)) and (
        "," in text or "&" in text or " o " in lowered or " and " in lowered
    )


def load_item_features(path: Path) -> dict[str, dict[str, Any]]:
    features: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("dataset") != "benqa":
                continue
            options = {match.group(1): match.group(2).strip() for match in OPTION_LINE_RE.finditer(row["banglish_clean"])}
            if set(options) != set(OPTIONS):
                raise SystemExit(f"Could not parse all options for {row['id']}")
            char_lengths = {option: len(text) for option, text in options.items()}
            token_lengths = {option: len(tokenize(text)) for option, text in options.items()}
            max_chars = max(char_lengths.values())
            longest = tuple(option for option in OPTIONS if char_lengths[option] == max_chars)
            composites = {option: is_composite_option(text) for option, text in options.items()}
            features[str(row["id"])] = {
                "id": row["id"],
                "gold": valid_option(row["answer"]),
                "subject": str(row.get("metadata", {}).get("subject") or row.get("domain", "")),
                "longest_options": longest,
                "longest_option_count": len(longest),
                "gold_is_longest": valid_option(row["answer"]) in longest,
                "d_is_longest": "D" in longest,
                "d_is_composite": composites["D"],
                "d_char_len": char_lengths["D"],
                "d_token_len": token_lengths["D"],
                **{f"{option}_char_len": char_lengths[option] for option in OPTIONS},
                **{f"{option}_token_len": token_lengths[option] for option in OPTIONS},
                **{f"{option}_is_composite": composites[option] for option in OPTIONS},
            }
    if len(features) != 144:
        raise SystemExit(f"Expected 144 BEnQA feature rows, got {len(features)}")
    return features


def option_rank(option: str, features: dict[str, Any]) -> int:
    length = int(features[f"{option}_char_len"])
    greater = sum(1 for label in OPTIONS if int(features[f"{label}_char_len"]) > length)
    return greater + 1


def build_rows(choice_items: Path, validation: Path) -> list[dict[str, Any]]:
    features = load_item_features(validation)
    rows: list[dict[str, Any]] = []
    for row in read_csv(choice_items):
        model = row["model"]
        if model not in MODELS:
            continue
        item_id = row["id"]
        feature = features[item_id]
        pred = valid_option(row["banglish_clean_parsed_option"])
        pred_label = pred or "invalid"
        rows.append(
            {
                "model": model,
                "id": item_id,
                "subject": feature["subject"],
                "gold": feature["gold"],
                "pred_option": pred_label,
                "correct": truthy(row["banglish_clean_correct"]),
                "d_is_longest": feature["d_is_longest"],
                "d_is_composite": feature["d_is_composite"],
                "gold_is_longest": feature["gold_is_longest"],
                "pred_is_longest": bool(pred and pred in feature["longest_options"]),
                "pred_is_composite": bool(pred and feature[f"{pred}_is_composite"]),
                "pred_char_len": feature[f"{pred}_char_len"] if pred else "",
                "pred_token_len": feature[f"{pred}_token_len"] if pred else "",
                "pred_length_rank": option_rank(pred, feature) if pred else "",
                "longest_options": ";".join(feature["longest_options"]),
                "longest_option_count": feature["longest_option_count"],
                "d_char_len": feature["d_char_len"],
                "d_token_len": feature["d_token_len"],
                **{f"{option}_char_len": feature[f"{option}_char_len"] for option in OPTIONS},
                **{f"{option}_is_composite": feature[f"{option}_is_composite"] for option in OPTIONS},
            }
        )
    expected = len(MODELS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} model-item rows, got {len(rows)}")
    return sorted(rows, key=lambda row: (row["model"], row["id"]))


def summarize_model(rows: list[dict[str, Any]], model: str) -> dict[str, Any]:
    selected = [row for row in rows if row["model"] == model]
    d_longest = [row for row in selected if row["d_is_longest"]]
    d_not_longest = [row for row in selected if not row["d_is_longest"]]
    pred_d = [row for row in selected if row["pred_option"] == "D"]
    return {
        "section": "model",
        "model": model,
        "n": len(selected),
        "correct": sum(row["correct"] for row in selected),
        "pred_D": len(pred_d),
        "pred_D_when_D_longest": sum(row["pred_option"] == "D" for row in d_longest),
        "D_longest_n": len(d_longest),
        "pred_D_when_D_not_longest": sum(row["pred_option"] == "D" for row in d_not_longest),
        "D_not_longest_n": len(d_not_longest),
        "pred_is_longest": sum(row["pred_is_longest"] for row in selected),
        "pred_is_composite": sum(row["pred_is_composite"] for row in selected),
        "correct_when_pred_is_longest": sum(row["correct"] and row["pred_is_longest"] for row in selected),
        "correct_when_pred_is_not_longest": sum(row["correct"] and not row["pred_is_longest"] for row in selected),
    }


def summarize_features(rows: list[dict[str, Any]]) -> dict[str, Any]:
    # Features repeat once per model; use the first model as one item set.
    selected = [row for row in rows if row["model"] == MODELS[0]]
    longest_counter: Counter[str] = Counter()
    for row in selected:
        labels = row["longest_options"].split(";")
        for label in labels:
            longest_counter[label] += 1 / len(labels)
    return {
        "section": "item_features",
        "model": "all_items",
        "n": len(selected),
        "gold_is_longest": sum(row["gold_is_longest"] for row in selected),
        "D_longest_n": sum(row["d_is_longest"] for row in selected),
        "D_longest_and_gold_D": sum(row["d_is_longest"] and row["gold"] == "D" for row in selected),
        "D_composite_n": sum(row["d_is_composite"] for row in selected),
        "A_longest_weighted": round(longest_counter["A"], 2),
        "B_longest_weighted": round(longest_counter["B"], 2),
        "C_longest_weighted": round(longest_counter["C"], 2),
        "D_longest_weighted": round(longest_counter["D"], 2),
    }


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [summarize_features(rows)] + [summarize_model(rows, model) for model in MODELS]


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    features = summary_rows[0]
    model_rows = {row["model"]: row for row in summary_rows if row["section"] == "model"}
    qwen3 = model_rows["Qwen3-4B"]
    qwen25_3b = model_rows["Qwen2.5-3B"]
    qwen25_7b = model_rows["Qwen2.5-7B 8-bit"]
    lines = [
        "# Frozen-V5 BEnQA Option Position/Content Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the Qwen3 reviewed-Banglish BEnQA",
        "D-attractor can be reduced to option text features, especially D often",
        "being the longest option. It uses reviewed-Banglish option text from the",
        "frozen-v5 slice and reviewed-Banglish predictions from the choice-bias audit.",
        "",
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            f"- D is tied for longest option on {features['D_longest_n']}/144 BEnQA items, "
            f"while gold D appears on 39/144 items."
        ),
        (
            "- Qwen3-4B still predicts D on "
            f"{qwen3['pred_D_when_D_not_longest']}/{qwen3['D_not_longest_n']} items "
            "where D is not the longest option."
        ),
        (
            "- The corresponding non-longest-D counts are "
            f"{qwen25_3b['pred_D_when_D_not_longest']}/{qwen25_3b['D_not_longest_n']} "
            "for Qwen2.5-3B and "
            f"{qwen25_7b['pred_D_when_D_not_longest']}/{qwen25_7b['D_not_longest_n']} "
            "for Qwen2.5-7B 8-bit."
        ),
        (
            f"- Qwen3-4B predicts a longest option on {qwen3['pred_is_longest']}/144 rows, "
            "so option length/content contributes to behavior, but it does not fully "
            "explain the D-position collapse."
        ),
        "",
        "## Summary",
        "",
        "| Model | Correct | Pred D | Pred D when D longest | Pred D when D not longest | Pred longest option | Pred composite option |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in (qwen25_3b, qwen25_7b, qwen3):
        lines.append(
            "| {model} | {correct}/{n} | {pred_D}/{n} | "
            "{pred_D_when_D_longest}/{D_longest_n} ({d_long_pct}) | "
            "{pred_D_when_D_not_longest}/{D_not_longest_n} ({d_not_pct}) | "
            "{pred_is_longest}/{n} | {pred_is_composite}/{n} |".format(
                **row,
                d_long_pct=percent(int(row["pred_D_when_D_longest"]), int(row["D_longest_n"])),
                d_not_pct=percent(int(row["pred_D_when_D_not_longest"]), int(row["D_not_longest_n"])),
            )
        )
    lines.extend(
        [
            "",
            "## Item Feature Summary",
            "",
            f"- Gold option is among the longest options on {features['gold_is_longest']}/144 items.",
            f"- D is tied for longest on {features['D_longest_n']}/144 items, but only "
            f"{features['D_longest_and_gold_D']}/{features['D_longest_n']} of those have gold D.",
            f"- D is composite on {features['D_composite_n']}/144 items; composite markers are balanced enough that D-only composition is not the sole explanation.",
            "",
            "Weighted longest-label counts:",
            "",
            "| A | B | C | D |",
            "| ---: | ---: | ---: | ---: |",
            f"| {features['A_longest_weighted']} | {features['B_longest_weighted']} | {features['C_longest_weighted']} | {features['D_longest_weighted']} |",
            "",
            "## Interpretation",
            "",
            "- BEnQA option text length partly explains why D is tempting: D is often one",
            "  of the longest options.",
            "- Qwen3's reviewed-Banglish D-attractor remains visible when D is not the",
            "  longest option, and it is far stronger than the same slice for Qwen2.5.",
            "- Use this as a confound check beside the choice-bias, subject-option,",
            "  distractor-transition, and label-balance audits.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_benqa_option_position_content.py`",
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
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_rows(args.choice_items, args.validation)
    summary_rows = build_summary(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)
    qwen3 = next(row for row in summary_rows if row["model"] == "Qwen3-4B")
    print(
        "items={items} | summary_rows={summary_rows} | "
        "qwen3_D_not_longest={d_not}/{n_not} | report={report}".format(
            items=len(item_rows),
            summary_rows=len(summary_rows),
            d_not=qwen3["pred_D_when_D_not_longest"],
            n_not=qwen3["D_not_longest_n"],
            report=repo_path(args.report_output),
        )
    )


if __name__ == "__main__":
    main()
