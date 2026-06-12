#!/usr/bin/env python3
"""Describe item/domain features associated with reviewed-v5 Banglish fragility."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_FAILURE_ITEMS = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
DEFAULT_ITEM_OUTPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_GROUP_OUTPUT = ROOT / "results/analysis/v5_banglish_fragility_feature_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglish_fragility_feature_analysis.md"

MODEL_LABELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}
MODEL_ORDER = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def compact_preview(text: str, limit: int = 130) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def count_regex(pattern: str, text: str, flags: int = 0) -> int:
    return len(re.findall(pattern, text, flags=flags))


def text_features(item: dict[str, Any]) -> dict[str, Any]:
    banglish = str(item.get("banglish_clean", ""))
    bangla = str(item.get("bangla", ""))
    english = str(item.get("english", ""))
    option_lines = [
        line for line in banglish.splitlines() if re.match(r"^[A-D][\).]\s+", line.strip())
    ]
    latex_marker_count = count_regex(r"[\\_^{}]", banglish)
    operator_count = count_regex(r"(?:[=+\-*/]|\\times|\\frac|\\sqrt|\\int|\\Delta)", banglish)
    digit_count = count_regex(r"[0-9\u09e6-\u09ef]", banglish)
    roman_statement = bool(re.search(r"(^|\s)i\.\s+.*\sii\.\s+", banglish, flags=re.IGNORECASE))
    science_symbol = bool(
        re.search(r"\b(?:CO|Na|Ca|Ag|Ni|CH|NH|HF|HCl|HCI|HBr|HI|O_?2|CaF|COONa)\b", banglish)
    )
    return {
        "banglish_chars": len(banglish),
        "banglish_words": len(re.findall(r"\S+", banglish)),
        "banglish_lines": len(banglish.splitlines()),
        "banglish_option_lines": len(option_lines),
        "bangla_chars": len(bangla),
        "english_chars": len(english),
        "digit_count": digit_count,
        "latex_marker_count": latex_marker_count,
        "operator_count": operator_count,
        "has_digits": digit_count > 0,
        "has_latex_markers": latex_marker_count > 0,
        "has_formula_or_operator": latex_marker_count > 0 or operator_count > 0,
        "has_roman_statement_list": roman_statement,
        "has_science_symbol": science_symbol,
        "has_review_label": bool((item.get("banglish_review") or {}).get("label")),
    }


def item_base_row(item: dict[str, Any]) -> dict[str, Any]:
    metadata = item.get("metadata") or {}
    review = item.get("banglish_review") or {}
    row = {
        "id": item["id"],
        "dataset": item.get("dataset", ""),
        "domain": item.get("domain", ""),
        "subject": metadata.get("subject", ""),
        "grade": metadata.get("grade", ""),
        "task_type": item.get("task_type", ""),
        "answer_type": item.get("answer_type", ""),
        "quality_status": item.get("quality_status", ""),
        "review_label": review.get("label", "unreviewed"),
        "reviewed_banglish_provided": bool(review.get("reviewed_banglish_provided", False)),
        "answer": item.get("answer", ""),
        "banglish_preview": compact_preview(str(item.get("banglish_clean", ""))),
    }
    row.update(text_features(item))
    return row


def quartile_threshold(values: list[int], q: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    pos = (len(values) - 1) * q
    low = int(pos)
    high = min(low + 1, len(values) - 1)
    frac = pos - low
    return values[low] * (1 - frac) + values[high] * frac


def build_item_rows(
    items: list[dict[str, Any]],
    failure_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    by_item: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in failure_rows:
        label = MODEL_LABELS.get(row["model"], row["model"])
        by_item[row["id"]][label] = row

    base_rows = [item_base_row(item) for item in items]
    q75_words = quartile_threshold([int(row["banglish_words"]) for row in base_rows], 0.75)
    q75_chars = quartile_threshold([int(row["banglish_chars"]) for row in base_rows], 0.75)
    out: list[dict[str, Any]] = []
    for row in base_rows:
        item_model_rows = by_item.get(str(row["id"]), {})
        fragility_events = 0
        strict_events = 0
        all_wrong_events = 0
        banglish_only_events = 0
        banglish_correct_models = 0
        bangla_correct_models = 0
        english_correct_models = 0
        any_correct_models = 0
        for model in MODEL_ORDER:
            model_row = item_model_rows.get(model, {})
            pattern = model_row.get("pattern", "missing")
            bangla_correct = truthy(model_row.get("bangla_correct", ""))
            banglish_correct = truthy(model_row.get("banglish_clean_correct", ""))
            english_correct = truthy(model_row.get("english_correct", ""))
            fragile = (not banglish_correct) and (bangla_correct or english_correct)
            strict = pattern == "bangla_english_correct_banglish_wrong"
            fragility_events += int(fragile)
            strict_events += int(strict)
            all_wrong_events += int(pattern == "all_wrong")
            banglish_only_events += int(pattern == "banglish_only_correct")
            banglish_correct_models += int(banglish_correct)
            bangla_correct_models += int(bangla_correct)
            english_correct_models += int(english_correct)
            any_correct_models += int(bangla_correct or banglish_correct or english_correct)
            row[f"{model}_pattern"] = pattern
            row[f"{model}_bangla_correct"] = bangla_correct
            row[f"{model}_banglish_correct"] = banglish_correct
            row[f"{model}_english_correct"] = english_correct
            row[f"{model}_fragility_event"] = fragile

        row["n_models"] = len(MODEL_ORDER)
        row["banglish_fragility_events"] = fragility_events
        row["strict_bangla_english_fragility_events"] = strict_events
        row["all_wrong_events"] = all_wrong_events
        row["banglish_only_correct_events"] = banglish_only_events
        row["bangla_correct_models"] = bangla_correct_models
        row["banglish_correct_models"] = banglish_correct_models
        row["english_correct_models"] = english_correct_models
        row["any_script_correct_models"] = any_correct_models
        row["any_model_fragile"] = fragility_events > 0
        row["all_models_fragile"] = fragility_events == len(MODEL_ORDER)
        row["long_banglish_words_q4"] = int(row["banglish_words"]) >= q75_words
        row["long_banglish_chars_q4"] = int(row["banglish_chars"]) >= q75_chars
        out.append(row)
    return out


def group_summary(
    item_rows: list[dict[str, Any]],
    feature: str,
    value_name: str,
    min_items: int = 1,
) -> dict[str, Any] | None:
    rows = [row for row in item_rows if str(row.get(feature, "")) == str(value_name)]
    n = len(rows)
    if n < min_items:
        return None
    model_slots = n * len(MODEL_ORDER)
    fragility_events = sum(int(row["banglish_fragility_events"]) for row in rows)
    strict_events = sum(int(row["strict_bangla_english_fragility_events"]) for row in rows)
    all_wrong_events = sum(int(row["all_wrong_events"]) for row in rows)
    banglish_correct = sum(int(row["banglish_correct_models"]) for row in rows)
    return {
        "feature": feature,
        "value": str(value_name),
        "n_items": n,
        "model_slots": model_slots,
        "fragility_events": fragility_events,
        "fragility_event_rate": round(fragility_events / model_slots, 4) if model_slots else 0.0,
        "strict_fragility_events": strict_events,
        "strict_fragility_event_rate": round(strict_events / model_slots, 4) if model_slots else 0.0,
        "items_any_fragile": sum(int(row["any_model_fragile"]) for row in rows),
        "items_any_fragile_rate": round(
            sum(int(row["any_model_fragile"]) for row in rows) / n, 4
        )
        if n
        else 0.0,
        "items_all_models_fragile": sum(int(row["all_models_fragile"]) for row in rows),
        "all_wrong_event_rate": round(all_wrong_events / model_slots, 4) if model_slots else 0.0,
        "banglish_correct_model_rate": round(banglish_correct / model_slots, 4) if model_slots else 0.0,
    }


def build_group_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    feature_values: list[tuple[str, list[Any], int]] = []
    categorical = [
        "dataset",
        "task_type",
        "domain",
        "subject",
        "grade",
        "quality_status",
        "review_label",
    ]
    binary = [
        "has_digits",
        "has_latex_markers",
        "has_formula_or_operator",
        "has_roman_statement_list",
        "has_science_symbol",
        "has_review_label",
        "reviewed_banglish_provided",
        "long_banglish_words_q4",
        "long_banglish_chars_q4",
    ]
    for feature in categorical:
        values = sorted({row.get(feature, "") for row in item_rows})
        min_items = 1 if feature in {"dataset", "task_type", "quality_status", "review_label"} else 3
        feature_values.append((feature, values, min_items))
    for feature in binary:
        feature_values.append((feature, [True, False], 1))

    rows: list[dict[str, Any]] = []
    for feature, values, min_items in feature_values:
        for value in values:
            summary = group_summary(item_rows, feature, value, min_items=min_items)
            if summary is not None:
                rows.append(summary)
    rows.sort(
        key=lambda row: (
            row["feature"],
            -float(row["fragility_event_rate"]),
            -int(row["n_items"]),
            row["value"],
        )
    )
    return rows


def top_rows(
    rows: list[dict[str, Any]],
    *,
    feature: str | None = None,
    min_items: int = 5,
    limit: int = 8,
) -> list[dict[str, Any]]:
    filtered = [
        row
        for row in rows
        if int(row["n_items"]) >= min_items and (feature is None or row["feature"] == feature)
    ]
    return sorted(
        filtered,
        key=lambda row: (-float(row["fragility_event_rate"]), -int(row["n_items"]), row["value"]),
    )[:limit]


def selected_feature_rows(group_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    wanted = [
        ("dataset", "benqa"),
        ("dataset", "banglamath"),
        ("task_type", "mcq"),
        ("task_type", "short_answer"),
        ("review_label", "unreviewed"),
        ("review_label", "minor_edit"),
        ("review_label", "major_edit"),
        ("has_digits", "True"),
        ("has_digits", "False"),
        ("has_formula_or_operator", "True"),
        ("has_formula_or_operator", "False"),
        ("has_roman_statement_list", "True"),
        ("has_science_symbol", "True"),
        ("long_banglish_words_q4", "True"),
    ]
    index = {(row["feature"], row["value"]): row for row in group_rows}
    return [index[key] for key in wanted if key in index]


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    group_rows: list[dict[str, Any]],
    items_path: Path,
    failure_path: Path,
    item_output: Path,
    group_output: Path,
) -> None:
    model_slots = len(item_rows) * len(MODEL_ORDER)
    fragility_events = sum(int(row["banglish_fragility_events"]) for row in item_rows)
    strict_events = sum(int(row["strict_bangla_english_fragility_events"]) for row in item_rows)
    any_fragile = sum(int(row["any_model_fragile"]) for row in item_rows)
    all_fragile = sum(int(row["all_models_fragile"]) for row in item_rows)
    all_wrong_events = sum(int(row["all_wrong_events"]) for row in item_rows)
    top_domain_rows = top_rows(group_rows, feature="domain", min_items=5, limit=8)
    feature_rows = selected_feature_rows(group_rows)
    brittle_items = sorted(
        item_rows,
        key=lambda row: (
            -int(row["banglish_fragility_events"]),
            -int(row["strict_bangla_english_fragility_events"]),
            -int(row["any_script_correct_models"]),
            row["id"],
        ),
    )[:10]

    lines = [
        "# Reviewed-V5 Banglish Fragility Feature Analysis",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend analysis joins the frozen-v5 cross-script failure rows with",
        "validation-item metadata. A fragility event means a thesis-facing Qwen",
        "model answered reviewed Banglish incorrectly while answering Bangla or",
        "English correctly on the same item. Counts are descriptive; they are not",
        "used as a deployable routing rule.",
        "",
        f"- Items: `{repo_path(items_path)}`",
        f"- Failure rows: `{repo_path(failure_path)}`",
        f"- Item output: `{repo_path(item_output)}`",
        f"- Feature summary: `{repo_path(group_output)}`",
        "",
        "## Overall",
        "",
        f"- Items: {len(item_rows)}",
        f"- Model-item slots: {model_slots}",
        f"- Banglish fragility events: {fragility_events}/{model_slots} ({percent(fragility_events / model_slots)})",
        f"- Strict Bangla+English-correct/Banglish-wrong events: {strict_events}/{model_slots} ({percent(strict_events / model_slots)})",
        f"- Items with at least one fragile model: {any_fragile}/{len(item_rows)} ({percent(any_fragile / len(item_rows))})",
        f"- Items fragile for all three thesis-facing models: {all_fragile}/{len(item_rows)} ({percent(all_fragile / len(item_rows))})",
        f"- All-script-wrong events: {all_wrong_events}/{model_slots} ({percent(all_wrong_events / model_slots)})",
        "",
        "## Highest Fragility Domains",
        "",
        "| Domain | Items | Fragility events | Event rate | Any fragile | Strict events |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in top_domain_rows:
        lines.append(
            f"| {row['value']} | {row['n_items']} | {row['fragility_events']}/{row['model_slots']} | "
            f"{percent(float(row['fragility_event_rate']))} | "
            f"{row['items_any_fragile']}/{row['n_items']} | {row['strict_fragility_events']} |"
        )
    lines.extend(
        [
            "",
            "## Feature Signals",
            "",
            "| Feature | Value | Items | Fragility events | Event rate | All-script-wrong event rate | Any fragile |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in feature_rows:
        lines.append(
            f"| `{row['feature']}` | `{row['value']}` | {row['n_items']} | "
            f"{row['fragility_events']}/{row['model_slots']} | "
            f"{percent(float(row['fragility_event_rate']))} | "
            f"{percent(float(row['all_wrong_event_rate']))} | "
            f"{row['items_any_fragile']}/{row['n_items']} |"
        )
    lines.extend(
        [
            "",
            "## Most Fragile Items",
            "",
            "| Item | Domain | Events | Strict | Patterns | Banglish preview |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in brittle_items:
        patterns = ", ".join(f"{model}: {row[f'{model}_pattern']}" for model in MODEL_ORDER)
        preview = str(row["banglish_preview"]).replace("|", "\\|")
        lines.append(
            f"| `{row['id']}` | {row['domain']} | {row['banglish_fragility_events']} | "
            f"{row['strict_bangla_english_fragility_events']} | {patterns} | {preview} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Banglish fragility is not confined to one dataset: the item-level output",
            "  records both the concentrated domains and the all-script-wrong cases.",
            "- Recoverable Banglish-specific fragility is concentrated in BEnQA MCQ",
            "  science domains, especially biology and chemistry subjects.",
            "- BanglaMATH short-answer rows show fewer recoverable fragility events",
            "  because many are all-script-wrong; that is difficulty headroom rather",
            "  than evidence that Banglish is solved for math.",
            "- Digit/formula prompts remain a preservation-audit surface for generated",
            "  views, but in the completed open-model outputs they more often appear as",
            "  all-script difficulty than as recoverable Banglish-only fragility.",
            "- The analysis strengthens the thesis failure-analysis chapter, but it does",
            "  not change the main accuracy table or authorize any new held-out routing.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURE_ITEMS)
    parser.add_argument("--item-output", type=Path, default=DEFAULT_ITEM_OUTPUT)
    parser.add_argument("--group-output", type=Path, default=DEFAULT_GROUP_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = read_jsonl(args.items)
    failure_rows = read_csv(args.failure_items)
    item_rows = build_item_rows(items, failure_rows)
    group_rows = build_group_rows(item_rows)
    if len(item_rows) != 200:
        raise SystemExit(f"Expected 200 item rows, got {len(item_rows)}")
    expected_failure_rows = len(item_rows) * len(MODEL_ORDER)
    if len(failure_rows) != expected_failure_rows:
        raise SystemExit(
            f"Expected {expected_failure_rows} failure rows, got {len(failure_rows)}"
        )

    item_fields = list(item_rows[0])
    group_fields = list(group_rows[0])
    write_csv(args.item_output, item_rows, item_fields)
    write_csv(args.group_output, group_rows, group_fields)
    write_report(
        args.report_output,
        item_rows,
        group_rows,
        args.items,
        args.failure_items,
        args.item_output,
        args.group_output,
    )
    fragility_events = sum(int(row["banglish_fragility_events"]) for row in item_rows)
    strict_events = sum(int(row["strict_bangla_english_fragility_events"]) for row in item_rows)
    print(f"items={len(item_rows)}")
    print(f"fragility_events={fragility_events}")
    print(f"strict_events={strict_events}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
