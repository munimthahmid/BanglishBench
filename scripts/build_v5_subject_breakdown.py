#!/usr/bin/env python3
"""Build frozen-v5 subject/grade breakdowns for thesis-facing Qwen rows."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_OUTPUT = ROOT / "results/analysis/validation200_v5_subject_breakdown.csv"
DEFAULT_TABLE = ROOT / "results/tables/subject_breakdown_validation200_v5.csv"
DEFAULT_REPORT = ROOT / "reports/subject_breakdown_validation200_v5.md"
INPUTS = [
    ROOT
    / "results/runs/qwen2_5_3b_validation200_v3_128/results/runs/qwen2_5_3b_validation200_v3_128.jsonl",
    ROOT
    / "results/runs/qwen3_4b_validation200_v3_128/results/runs/qwen3_4b_validation200_v3_128.jsonl",
    ROOT
    / "results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50.jsonl",
    ROOT
    / "results/runs/qwen25_7b_8bit_validation200_v4_test150/results/runs/qwen25_7b_8bit_validation200_v4_test150.jsonl",
    ROOT
    / "results/runs/qwen2_5_3b_validation200_v5_banglish/results/runs/qwen2_5_3b_validation200_v5_banglish.jsonl",
    ROOT
    / "results/runs/qwen3_4b_validation200_v5_banglish/results/runs/qwen3_4b_validation200_v5_banglish.jsonl",
    ROOT
    / "results/runs/qwen25_7b_8bit_validation200_v5_banglish_pinned/results/runs/qwen2_5_7b_8bit_validation200_v5_banglish_pinned.jsonl",
]
VARIANTS = ("bangla", "banglish_clean", "english")
MODELS = (
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen3-4B-Instruct-2507",
)
MODEL_LABELS = {
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    return {str(row["id"]): row for row in read_jsonl(path)}


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def stratum_for(item: dict[str, Any]) -> str:
    metadata = item.get("metadata") or {}
    if item.get("dataset") == "benqa":
        return str(metadata.get("subject") or item.get("domain") or "unknown")
    if item.get("dataset") == "banglamath":
        return str(metadata.get("grade") or "unknown")
    return str(item.get("domain") or "unknown")


def load_eval_rows(paths: list[Path], items: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    indexed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for path in jsonl_paths(paths):
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"id", "model", "variant", "correct"}.issubset(row):
                    continue
                if row.get("variant") not in VARIANTS or row.get("model") not in MODELS:
                    continue
                item = items.get(str(row["id"]))
                if item is None:
                    continue
                if row.get("raw_output"):
                    row["parsed"] = parse_answer(
                        str(row.get("raw_output", "")),
                        str(row.get("answer_type", "")),
                    )
                row["correct"] = is_correct(
                    str(row.get("parsed", "")),
                    str(row.get("gold", "")),
                    str(row.get("answer_type", "")),
                )
                joined = dict(row)
                metadata = item.get("metadata") or {}
                joined["dataset"] = item.get("dataset", joined.get("dataset", ""))
                joined["domain"] = item.get("domain", "")
                joined["subject"] = metadata.get("subject", "")
                joined["grade"] = metadata.get("grade", "")
                joined["stratum"] = stratum_for(item)
                joined["_source"] = repo_path(path)
                joined["_line"] = line_no
                key = (str(joined["model"]), str(joined["id"]), str(joined["variant"]))
                indexed[key] = joined
    return list(indexed.values())


def build_rows(eval_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in eval_rows:
        key = (str(row["model"]), str(row["dataset"]), str(row["stratum"]))
        groups[key][str(row["variant"])].append(row)

    rows: list[dict[str, Any]] = []
    for (model, dataset, stratum), by_variant in sorted(groups.items()):
        if not all(variant in by_variant for variant in VARIANTS):
            continue
        item_sets = {variant: {row["id"] for row in by_variant[variant]} for variant in VARIANTS}
        if len({frozenset(value) for value in item_sets.values()}) != 1:
            raise SystemExit(f"Mismatched item ids for {model} {dataset} {stratum}")
        n = len(item_sets["bangla"])
        counts = {
            variant: sum(1 for row in by_variant[variant] if bool(row.get("correct")))
            for variant in VARIANTS
        }
        parsed_empty = {
            variant: sum(1 for row in by_variant[variant] if not str(row.get("parsed", "")).strip())
            for variant in VARIANTS
        }
        rows.append(
            {
                "model": MODEL_LABELS[model],
                "model_id": model,
                "dataset": dataset,
                "stratum": stratum,
                "n": n,
                "bangla_correct": counts["bangla"],
                "reviewed_banglish_correct": counts["banglish_clean"],
                "english_correct": counts["english"],
                "banglish_minus_bangla_items": counts["banglish_clean"] - counts["bangla"],
                "banglish_minus_english_items": counts["banglish_clean"] - counts["english"],
                "bangla_accuracy": round(counts["bangla"] / n, 4) if n else 0.0,
                "reviewed_banglish_accuracy": round(counts["banglish_clean"] / n, 4) if n else 0.0,
                "english_accuracy": round(counts["english"] / n, 4) if n else 0.0,
                "bangla_parsed_empty": parsed_empty["bangla"],
                "banglish_parsed_empty": parsed_empty["banglish_clean"],
                "english_parsed_empty": parsed_empty["english"],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rows_for(rows: list[dict[str, Any]], model: str, dataset: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["model"] == model and row["dataset"] == dataset]


def broadness(rows: list[dict[str, Any]], model: str, dataset: str) -> tuple[int, int]:
    selected = rows_for(rows, model, dataset)
    below = sum(1 for row in selected if int(row["banglish_minus_bangla_items"]) < 0)
    return below, len(selected)


def write_report(path: Path, rows: list[dict[str, Any]], output: Path, table: Path) -> None:
    lines = [
        "# Frozen-V5 Subject And Grade Breakdown",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report refreshes the subject/grade spread analysis with the frozen-v5",
        "reviewed Banglish outputs used in the release-facing main table. Bangla",
        "and English outputs are reused because those fields did not change.",
        "",
        f"- Machine-readable summary: `{repo_path(output)}`",
        f"- Thesis table CSV: `{repo_path(table)}`",
        "",
        "## BEnQA Subject Breakdown",
        "",
    ]
    for model in MODEL_LABELS.values():
        below, total = broadness(rows, model, "benqa")
        lines.extend(
            [
                f"### {model}",
                "",
                f"Reviewed Banglish is below Bangla in {below}/{total} BEnQA subject strata.",
                "",
                "| Subject | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in rows_for(rows, model, "benqa"):
            lines.append(
                f"| {row['stratum']} | {row['n']} | {row['bangla_correct']} | "
                f"{row['reviewed_banglish_correct']} | {row['english_correct']} | "
                f"{int(row['banglish_minus_bangla_items']):+d} |"
            )
        lines.append("")
    lines.extend(["## BanglaMATH Grade Breakdown", ""])
    for model in MODEL_LABELS.values():
        below, total = broadness(rows, model, "banglamath")
        lines.extend(
            [
                f"### {model}",
                "",
                f"Reviewed Banglish is below Bangla in {below}/{total} BanglaMATH grade strata.",
                "",
                "| Grade | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in rows_for(rows, model, "banglamath"):
            lines.append(
                f"| {row['stratum']} | {row['n']} | {row['bangla_correct']} | "
                f"{row['reviewed_banglish_correct']} | {row['english_correct']} | "
                f"{int(row['banglish_minus_bangla_items']):+d} |"
            )
        lines.append("")
    qwen3_below, qwen3_total = broadness(rows, "Qwen3-4B", "benqa")
    qwen7_below, qwen7_total = broadness(rows, "Qwen2.5-7B 8-bit", "benqa")
    lines.extend(
        [
            "## Interpretation",
            "",
            f"- Qwen3-4B reviewed Banglish remains below native Bangla in {qwen3_below}/{qwen3_total} BEnQA subject strata.",
            f"- Qwen2.5-7B 8-bit reviewed Banglish is below native Bangla in {qwen7_below}/{qwen7_total} BEnQA subject strata.",
            "- Qwen2.5-3B is more mixed by subject, matching its weaker all-200 interval.",
            "- BanglaMATH grade strata remain low-accuracy and are better treated as",
            "  hard stress-test evidence than fine-grained subject evidence.",
            "- Subject and grade strata are small, so this is descriptive support rather",
            "  than a separate primary statistical claim.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--input", type=Path, nargs="*", default=INPUTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--table-output", type=Path, default=DEFAULT_TABLE)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in [args.items, *args.input]:
        if not path.exists():
            raise SystemExit(f"Missing required input: {path}")
    items = load_items(args.items)
    eval_rows = load_eval_rows(args.input, items)
    rows = build_rows(eval_rows)
    if len(eval_rows) != 1800:
        raise SystemExit(f"Expected 1800 eval rows, got {len(eval_rows)}")
    if len(rows) != 48:
        raise SystemExit(f"Expected 48 summary rows, got {len(rows)}")
    fieldnames = list(rows[0])
    write_csv(args.output, rows, fieldnames)
    write_csv(args.table_output, rows, fieldnames)
    write_report(args.report_output, rows, args.output, args.table_output)
    qwen3_below, qwen3_total = broadness(rows, "Qwen3-4B", "benqa")
    print(f"eval_rows={len(eval_rows)}")
    print(f"summary_rows={len(rows)}")
    print(f"qwen3_benqa_below={qwen3_below}/{qwen3_total}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
