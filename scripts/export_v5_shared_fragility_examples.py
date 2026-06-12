#!/usr/bin/env python3
"""Export thesis-ready qualitative examples for frozen-v5 shared fragility."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_OVERLAP = ROOT / "results/analysis/v5_banglish_fragility_model_overlap_items.csv"
DEFAULT_FAILURES = (
    ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
)
DEFAULT_OUTPUT_CSV = ROOT / "results/analysis/v5_shared_fragility_examples.csv"
DEFAULT_OUTPUT_MD = ROOT / "reports/v5_shared_fragility_examples.md"

STRICT_PATTERN = "bangla_english_correct_banglish_wrong"
MODELS = (
    ("Qwen/Qwen2.5-3B-Instruct", "Qwen2.5-3B"),
    ("Qwen/Qwen2.5-7B-Instruct", "Qwen2.5-7B 8-bit"),
    ("Qwen/Qwen3-4B-Instruct-2507", "Qwen3-4B"),
)
SHORT_MODEL_LABEL = {
    "Qwen2.5-3B": "Qwen2.5-3B",
    "Qwen2.5-7B": "Qwen2.5-7B 8-bit",
    "Qwen3-4B": "Qwen3-4B",
}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                out[str(row["id"])] = row
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def clip(value: Any, limit: int = 190) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def md_cell(value: Any) -> str:
    text = str(value or "")
    return text.replace("\n", " ").replace("|", "\\|")


def code(value: Any) -> str:
    text = md_cell(value)
    return "`" + text.replace("`", "\\`") + "`"


def task_label(row: dict[str, str]) -> str:
    if row.get("dataset") == "banglamath":
        return f"BanglaMATH {row.get('grade') or 'unknown grade'}"
    subject = row.get("subject") or row.get("domain") or "unknown subject"
    grade = row.get("grade") or "unknown grade"
    return f"BEnQA {grade} {subject}"


def split_models(value: str) -> list[str]:
    return [model for model in value.split(";") if model]


def format_model_list(value: str) -> str:
    models = [SHORT_MODEL_LABEL.get(model, model) for model in split_models(value)]
    return ", ".join(models)


def select_main_rows(overlap_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    strict_rows = [row for row in overlap_rows if truthy(row.get("all_models_strict"))]
    banglamath = sorted(
        [row for row in strict_rows if row["dataset"] == "banglamath"],
        key=lambda row: row["id"],
    )
    non_math_mcq = sorted(
        [
            row
            for row in strict_rows
            if row["dataset"] == "benqa" and row.get("domain") != "math"
        ],
        key=lambda row: (row.get("grade", ""), row.get("subject", ""), row["id"]),
    )
    selected = banglamath[:2] + non_math_mcq[:1]
    seen = {row["id"] for row in selected}
    selected.extend(row for row in sorted(strict_rows, key=lambda row: row["id"]) if row["id"] not in seen)
    return selected


def failure_index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["model"], row["id"]): row for row in rows}


def first_failure_for_item(
    index: dict[tuple[str, str], dict[str, str]], item_id: str
) -> dict[str, str]:
    for full_model, _label in MODELS:
        row = index.get((full_model, item_id))
        if row:
            return row
    return {}


def build_example_rows(
    overlap_rows: list[dict[str, str]],
    items: dict[str, dict[str, Any]],
    failures: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    shared_strict = [
        row for row in overlap_rows if truthy(row.get("shared_strict_fragility"))
    ]
    ordered = sorted(
        shared_strict,
        key=lambda row: (
            0 if truthy(row.get("all_models_strict")) else 1,
            -int(row.get("strict_model_count", "0") or 0),
            row.get("dataset", ""),
            row.get("domain", ""),
            row["id"],
        ),
    )
    out: list[dict[str, Any]] = []
    for row in ordered:
        item = items.get(row["id"], {})
        first = first_failure_for_item(failures, row["id"])
        record: dict[str, Any] = {
            "tier": "main_all_three_strict"
            if truthy(row.get("all_models_strict"))
            else "appendix_shared_strict",
            "id": row["id"],
            "dataset": row["dataset"],
            "domain": row["domain"],
            "subject": row["subject"],
            "grade": row["grade"],
            "task_type": row["task_type"],
            "review_label": row["review_label"],
            "gold": first.get("gold", item.get("answer", "")),
            "fragile_model_count": row["fragile_model_count"],
            "strict_model_count": row["strict_model_count"],
            "fragile_models": format_model_list(row["fragile_models"]),
            "strict_models": format_model_list(row["strict_models"]),
            "bangla_prompt": clip(item.get("bangla", ""), 240),
            "banglish_prompt": clip(item.get("banglish_clean", ""), 240),
            "english_prompt": clip(item.get("english", ""), 240),
        }
        for full_model, label in MODELS:
            failure = failures.get((full_model, row["id"]), {})
            prefix = label.replace(" ", "_").replace(".", "").replace("-", "_").lower()
            record[f"{prefix}_pattern"] = failure.get("pattern", "")
            record[f"{prefix}_bangla_parsed"] = failure.get("bangla_parsed", "")
            record[f"{prefix}_banglish_parsed"] = failure.get("banglish_clean_parsed", "")
            record[f"{prefix}_english_parsed"] = failure.get("english_parsed", "")
        out.append(record)
    return out


def parsed_for(row: dict[str, Any], label: str, variant: str) -> str:
    prefix = label.replace(" ", "_").replace(".", "").replace("-", "_").lower()
    return str(row.get(f"{prefix}_{variant}_parsed", ""))


def pattern_for(row: dict[str, Any], label: str) -> str:
    prefix = label.replace(" ", "_").replace(".", "").replace("-", "_").lower()
    return str(row.get(f"{prefix}_pattern", ""))


def write_detail(lines: list[str], row: dict[str, Any]) -> None:
    lines.extend(
        [
            f"### {row['id']}",
            "",
            f"- Task: {task_label(row)}",
            f"- Gold: {code(row['gold'])}",
            f"- Review label: `{row['review_label']}`",
            f"- Strict models: {row['strict_models']}",
            "",
            "| Script | Prompt snippet |",
            "| --- | --- |",
            f"| Bangla | {code(row['bangla_prompt'])} |",
            f"| Reviewed Banglish | {code(row['banglish_prompt'])} |",
            f"| English | {code(row['english_prompt'])} |",
            "",
            "| Model | Pattern | Bangla parsed | Banglish parsed | English parsed |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for _full_model, label in MODELS:
        lines.append(
            f"| {label} | `{pattern_for(row, label)}` | "
            f"{code(parsed_for(row, label, 'bangla'))} | "
            f"{code(parsed_for(row, label, 'banglish'))} | "
            f"{code(parsed_for(row, label, 'english'))} |"
        )
    lines.extend(
        [
            "",
            "Use this as a qualitative illustration only; the aggregate overlap and",
            "failure-taxonomy reports remain the evidence for the claim.",
            "",
        ]
    )


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, str]],
    output_csv: Path,
    overlap_path: Path,
    failures_path: Path,
) -> None:
    all_strict = [row for row in rows if row["tier"] == "main_all_three_strict"]
    main_body = select_main_rows(
        [row for row in overlap_rows if truthy(row.get("all_models_strict"))]
    )[:3]
    main_ids = {row["id"] for row in main_body}
    main_lookup = {row["id"]: row for row in rows}
    appendix = [row for row in rows if row["tier"] == "appendix_shared_strict"]

    shared_fragility = sum(1 for row in overlap_rows if truthy(row.get("shared_fragility")))
    all_models_fragile = sum(1 for row in overlap_rows if truthy(row.get("all_models_fragile")))
    shared_strict = sum(1 for row in overlap_rows if truthy(row.get("shared_strict_fragility")))

    lines = [
        "# Frozen-V5 Shared Fragility Examples",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This reproducible packet selects qualitative examples from the frozen-v5",
        "model-overlap table. The cleanest examples are items where every",
        "thesis-facing Qwen row is correct in Bangla and English but wrong in",
        "reviewed Banglish.",
        "",
        f"- Machine-readable examples: `{repo_path(output_csv)}`",
        f"- Overlap source: `{repo_path(overlap_path)}`",
        f"- Failure-pattern source: `{repo_path(failures_path)}`",
        "",
        "## Summary",
        "",
        f"- Shared fragility: {shared_fragility}/200 items affect at least two Qwen rows.",
        f"- All-three fragility: {all_models_fragile}/200 items affect all three Qwen rows.",
        f"- Shared strict fragility: {shared_strict}/200 items affect at least two rows",
        "  under the strongest Bangla+English-correct/Banglish-wrong pattern.",
        f"- All-three strict examples: {len(all_strict)}/200 items.",
        "",
        "## Recommended Main-Body Shortlist",
        "",
        "| Item | Task | Gold | Why it belongs |",
        "| --- | --- | --- | --- |",
    ]
    for item_id in sorted(main_ids, key=lambda value: [row["id"] for row in main_body].index(value)):
        row = main_lookup[item_id]
        why = (
            "short arithmetic failure"
            if row["dataset"] == "banglamath"
            else "non-arithmetic MCQ failure with simple option parsing"
        )
        lines.append(
            f"| `{row['id']}` | {md_cell(task_label(row))} | {code(row['gold'])} | "
            f"All three Qwen rows are strict; {why}. |"
        )
    lines.extend(
        [
            "",
            "## All-Three Strict Cases",
            "",
            "| Item | Task | Gold | Reviewed-Banglish parsed answers |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in all_strict:
        banglish_answers = "; ".join(
            f"{label}: {parsed_for(row, label, 'banglish')}" for _full_model, label in MODELS
        )
        lines.append(
            f"| `{row['id']}` | {md_cell(task_label(row))} | {code(row['gold'])} | "
            f"{code(banglish_answers)} |"
        )

    lines.extend(["", "## Detailed Main-Body Examples", ""])
    for item_id in [row["id"] for row in main_body]:
        write_detail(lines, main_lookup[item_id])

    lines.extend(
        [
            "## Appendix Shared-Strict Candidates",
            "",
            "These rows are still strong qualitative candidates, but not all three",
            "models satisfy the strict pattern. Use them when the appendix needs",
            "broader domain coverage.",
            "",
            "| Item | Task | Gold | Strict models | Fragile models |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in appendix:
        lines.append(
            f"| `{row['id']}` | {md_cell(task_label(row))} | {code(row['gold'])} | "
            f"{md_cell(row['strict_models'])} | {md_cell(row['fragile_models'])} |"
        )

    lines.extend(
        [
            "",
            "## Thesis Boundary",
            "",
            "Use these examples to make the aggregate script-gap and overlap results",
            "concrete. Do not treat a small qualitative packet as standalone proof",
            "of the mechanism; cite the frozen-v5 diagnostics and overlap counts for",
            "the evidentiary claim.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--overlap-items", type=Path, default=DEFAULT_OVERLAP)
    parser.add_argument("--failure-items", type=Path, default=DEFAULT_FAILURES)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_items(args.items)
    overlap_rows = read_csv(args.overlap_items)
    failure_rows = failure_index(read_csv(args.failure_items))
    example_rows = build_example_rows(overlap_rows, items, failure_rows)
    fieldnames = [
        "tier",
        "id",
        "dataset",
        "domain",
        "subject",
        "grade",
        "task_type",
        "review_label",
        "gold",
        "fragile_model_count",
        "strict_model_count",
        "fragile_models",
        "strict_models",
        "bangla_prompt",
        "banglish_prompt",
        "english_prompt",
    ]
    for _full_model, label in MODELS:
        prefix = label.replace(" ", "_").replace(".", "").replace("-", "_").lower()
        fieldnames.extend(
            [
                f"{prefix}_pattern",
                f"{prefix}_bangla_parsed",
                f"{prefix}_banglish_parsed",
                f"{prefix}_english_parsed",
            ]
        )

    write_csv(args.output_csv, example_rows, fieldnames)
    write_report(
        args.output_md,
        example_rows,
        overlap_rows,
        args.output_csv,
        args.overlap_items,
        args.failure_items,
    )
    all_strict = sum(1 for row in example_rows if row["tier"] == "main_all_three_strict")
    print(
        f"wrote={args.output_md} rows={len(example_rows)} all_three_strict={all_strict} "
        f"csv={args.output_csv}"
    )


if __name__ == "__main__":
    main()
