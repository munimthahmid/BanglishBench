#!/usr/bin/env python3
"""Audit whether Qwen3 BEnQA D-collapse is an order/run-position artifact."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_FORMAT_ITEMS = ROOT / "results/analysis/v5_answer_format_audit_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_order_confound_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_order_confound_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_order_confound.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
ORDER_AXES = (
    ("validation_order", "Frozen validation-200 order"),
    ("benqa_order", "BEnQA-only order"),
    ("run_line", "Reviewed-Banglish output line"),
)


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


def load_benqa_metadata(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    benqa_order = 0
    with path.open("r", encoding="utf-8") as handle:
        for validation_order, line in enumerate(handle, start=1):
            item = json.loads(line)
            if item.get("dataset") != "benqa":
                continue
            benqa_order += 1
            metadata = item.get("metadata", {})
            rows[item["id"]] = {
                "validation_order": validation_order,
                "benqa_order": benqa_order,
                "subject": metadata.get("subject", ""),
                "grade": metadata.get("grade", ""),
                "domain": item.get("domain", ""),
                "source_file": item.get("source_file", ""),
                "source_row": item.get("source_row", ""),
            }
    if len(rows) != 144:
        raise SystemExit(f"Expected 144 BEnQA items, got {len(rows)}")
    return rows


def build_item_rows(
    slice_path: Path,
    choice_items_path: Path,
    format_items_path: Path,
) -> list[dict[str, Any]]:
    metadata = load_benqa_metadata(slice_path)
    choice_rows = read_csv(choice_items_path)
    format_rows = read_csv(format_items_path)
    format_index = {
        (row["model"], row["variant"], row["id"]): row
        for row in format_rows
        if row.get("dataset") == "benqa" and row.get("answer_type") == "choice"
    }
    if len(choice_rows) != len(MODELS) * 144:
        raise SystemExit(f"Expected {len(MODELS) * 144} choice-bias item rows, got {len(choice_rows)}")

    out: list[dict[str, Any]] = []
    for row in choice_rows:
        model = row["model"]
        item_id = row["id"]
        key = (model, "banglish_clean", item_id)
        if item_id not in metadata:
            raise SystemExit(f"Missing slice metadata for {item_id}")
        if key not in format_index:
            raise SystemExit(f"Missing answer-format row for {key}")
        meta = metadata[item_id]
        format_row = format_index[key]
        option = row["banglish_clean_parsed_option"]
        correct = truthy(row["banglish_clean_correct"])
        out.append(
            {
                "model": model,
                "id": item_id,
                "gold": row["gold"],
                "subject": meta["subject"],
                "grade": meta["grade"],
                "domain": meta["domain"],
                "source_file": meta["source_file"],
                "source_row": meta["source_row"],
                "validation_order": meta["validation_order"],
                "benqa_order": meta["benqa_order"],
                "run_line": int(format_row["line"]),
                "banglish_option": option,
                "banglish_correct": correct,
                "banglish_D": option == "D",
                "banglish_wrong_D": option == "D" and not correct,
                "banglish_invalid": option == "invalid",
            }
        )
    return out


def quartile_rows(rows: list[dict[str, Any]], axis: str) -> list[tuple[str, list[dict[str, Any]]]]:
    ordered = sorted(rows, key=lambda row: int(row[axis]))
    n = len(ordered)
    chunks: list[tuple[str, list[dict[str, Any]]]] = []
    for index in range(4):
        start = index * n // 4
        end = (index + 1) * n // 4
        chunks.append((f"q{index + 1}", ordered[start:end]))
    return chunks


def summarize_bucket(
    model: str,
    axis: str,
    axis_label: str,
    bucket: str,
    selected: list[dict[str, Any]],
) -> dict[str, Any]:
    n = len(selected)
    d_count = sum(bool(row["banglish_D"]) for row in selected)
    wrong_d = sum(bool(row["banglish_wrong_D"]) for row in selected)
    correct = sum(bool(row["banglish_correct"]) for row in selected)
    return {
        "section": "order_quartile",
        "model": model,
        "axis": axis,
        "axis_label": axis_label,
        "bucket": bucket,
        "n": n,
        "min_position": min(int(row[axis]) for row in selected),
        "max_position": max(int(row[axis]) for row in selected),
        "banglish_correct": correct,
        "banglish_D": d_count,
        "banglish_wrong_D": wrong_d,
        "banglish_invalid": sum(bool(row["banglish_invalid"]) for row in selected),
    }


def contiguous_runs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(rows, key=lambda row: int(row["run_line"]))
    runs: list[dict[str, Any]] = []
    for row in ordered:
        is_d = bool(row["banglish_D"])
        if not runs or runs[-1]["is_D"] != is_d:
            runs.append(
                {
                    "is_D": is_d,
                    "length": 1,
                    "start_id": row["id"],
                    "end_id": row["id"],
                    "start_line": row["run_line"],
                    "end_line": row["run_line"],
                }
            )
        else:
            runs[-1]["length"] += 1
            runs[-1]["end_id"] = row["id"]
            runs[-1]["end_line"] = row["run_line"]
    return runs


def summarize_run_sequence(model: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    runs = contiguous_runs(rows)
    d_runs = [run for run in runs if run["is_D"]]
    non_d_runs = [run for run in runs if not run["is_D"]]
    longest_d = max(d_runs, key=lambda run: int(run["length"])) if d_runs else None
    return {
        "section": "run_sequence",
        "model": model,
        "axis": "run_line",
        "axis_label": "Reviewed-Banglish output line",
        "bucket": "all",
        "n": len(rows),
        "min_position": min(int(row["run_line"]) for row in rows),
        "max_position": max(int(row["run_line"]) for row in rows),
        "banglish_correct": sum(bool(row["banglish_correct"]) for row in rows),
        "banglish_D": sum(bool(row["banglish_D"]) for row in rows),
        "banglish_wrong_D": sum(bool(row["banglish_wrong_D"]) for row in rows),
        "banglish_invalid": sum(bool(row["banglish_invalid"]) for row in rows),
        "d_run_count": len(d_runs),
        "non_d_run_count": len(non_d_runs),
        "longest_d_run": int(longest_d["length"]) if longest_d else 0,
        "longest_d_start_line": longest_d["start_line"] if longest_d else "",
        "longest_d_end_line": longest_d["end_line"] if longest_d else "",
        "longest_d_start_id": longest_d["start_id"] if longest_d else "",
        "longest_d_end_id": longest_d["end_id"] if longest_d else "",
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [row for row in item_rows if row["model"] == model]
        for axis, axis_label in ORDER_AXES:
            for bucket, selected in quartile_rows(model_rows, axis):
                rows.append(summarize_bucket(model, axis, axis_label, bucket, selected))
        rows.append(summarize_run_sequence(model, model_rows))
    return rows


def row_for(rows: list[dict[str, Any]], model: str, section: str, axis: str, bucket: str) -> dict[str, Any]:
    matches = [
        row
        for row in rows
        if row["model"] == model
        and row["section"] == section
        and row["axis"] == axis
        and row["bucket"] == bucket
    ]
    if len(matches) != 1:
        raise SystemExit(f"Expected one row for {model} {section} {axis} {bucket}, got {len(matches)}")
    return matches[0]


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_q1 = row_for(summary_rows, "Qwen3-4B", "order_quartile", "run_line", "q1")
    q3_q2 = row_for(summary_rows, "Qwen3-4B", "order_quartile", "run_line", "q2")
    q3_q3 = row_for(summary_rows, "Qwen3-4B", "order_quartile", "run_line", "q3")
    q3_q4 = row_for(summary_rows, "Qwen3-4B", "order_quartile", "run_line", "q4")
    q3_seq = row_for(summary_rows, "Qwen3-4B", "run_sequence", "run_line", "all")
    q25_3_seq = row_for(summary_rows, "Qwen2.5-3B", "run_sequence", "run_line", "all")
    q25_7_seq = row_for(summary_rows, "Qwen2.5-7B 8-bit", "run_sequence", "run_line", "all")

    q3_quartile_counts = [q3_q1, q3_q2, q3_q3, q3_q4]
    q3_d_values = [int(row["banglish_D"]) for row in q3_quartile_counts]
    q3_wrong_d_values = [int(row["banglish_wrong_D"]) for row in q3_quartile_counts]
    q3_d_text = ", ".join(f"{row['banglish_D']}/{row['n']}" for row in q3_quartile_counts)
    q3_wrong_d_text = ", ".join(f"{row['banglish_wrong_D']}/{row['n']}" for row in q3_quartile_counts)

    lines = [
        "# Frozen-V5 BEnQA Order-Confound Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit checks whether the Qwen3-4B reviewed-Banglish BEnQA",
        "D-attractor can be reduced to item order, BEnQA-only order, or output",
        "run position. It joins the frozen-v5 item order, reviewed-Banglish",
        "answer-format run-line metadata, and the BEnQA choice-bias item table.",
        "",
        f"- Item table: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- By reviewed-Banglish output-line quartile, Qwen3-4B predicts D on "
            f"{q3_d_text} rows; every quartile is at least "
            f"{min(q3_d_values)}/36 ({percent(min(q3_d_values), 36)})."
        ),
        (
            "- Wrong-D counts by the same quartiles are "
            f"{q3_wrong_d_text}; the first and last quartiles are "
            f"{q3_q1['banglish_wrong_D']}/36 and {q3_q4['banglish_wrong_D']}/36."
        ),
        (
            "- Qwen3-4B has D on "
            f"{q3_seq['banglish_D']}/144 rows overall with {q3_seq['d_run_count']} "
            f"separate D-runs; its longest contiguous D-run is "
            f"{q3_seq['longest_d_run']} rows."
        ),
        (
            "- The two Qwen2.5 reviewed-Banglish rows have much lower D totals and "
            f"shorter D-runs: {q25_3_seq['banglish_D']}/144 with longest run "
            f"{q25_3_seq['longest_d_run']}, and {q25_7_seq['banglish_D']}/144 "
            f"with longest run {q25_7_seq['longest_d_run']}."
        ),
        "",
        "## Run-Line Quartiles",
        "",
        "| Model | Q1 D | Q2 D | Q3 D | Q4 D | Q1 wrong D | Q4 wrong D | Longest D-run |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        q1 = row_for(summary_rows, model, "order_quartile", "run_line", "q1")
        q2 = row_for(summary_rows, model, "order_quartile", "run_line", "q2")
        q3 = row_for(summary_rows, model, "order_quartile", "run_line", "q3")
        q4 = row_for(summary_rows, model, "order_quartile", "run_line", "q4")
        seq = row_for(summary_rows, model, "run_sequence", "run_line", "all")
        lines.append(
            f"| {model} | {q1['banglish_D']}/{q1['n']} | {q2['banglish_D']}/{q2['n']} | "
            f"{q3['banglish_D']}/{q3['n']} | {q4['banglish_D']}/{q4['n']} | "
            f"{q1['banglish_wrong_D']}/{q1['n']} | {q4['banglish_wrong_D']}/{q4['n']} | "
            f"{seq['longest_d_run']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Qwen3's reviewed-Banglish D-attractor is visible from the first",
            "  output-line quartile and remains visible in the last, so it is not",
            "  a simple late-run degradation or a single terminal corruption block.",
            "- The repeated D-runs are longer for Qwen3 than for Qwen2.5, but they",
            "  are distributed across the run rather than confined to one segment.",
            "- This audit addresses an execution/order confound. It remains behavioral",
            "  evidence over fixed outputs and does not identify an internal mechanism.",
            "",
            "## Artifacts",
            "",
            "- Builder: `scripts/analyze_v5_benqa_order_confound.py`",
            f"- Item table: `{repo_path(items_output)}`",
            f"- Summary table: `{repo_path(summary_output)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--format-items", type=Path, default=DEFAULT_FORMAT_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.items, args.choice_items, args.format_items)
    summary_rows = build_summary_rows(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    q3_seq = row_for(summary_rows, "Qwen3-4B", "run_sequence", "run_line", "all")
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"qwen3_D={q3_seq['banglish_D']}/144 "
        f"qwen3_longest_D_run={q3_seq['longest_d_run']} report={args.report_output}"
    )


if __name__ == "__main__":
    main()
