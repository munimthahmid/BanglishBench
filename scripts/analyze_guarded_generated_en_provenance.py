#!/usr/bin/env python3
"""Analyze guarded generated-English repair provenance and answer effects."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPAIR_OUTPUT = (
    ROOT
    / "results/generated_views/qwen3_4b_selftranslate_guarded_v5_dev50_benqa_mcq_generated_en.jsonl"
)
DEFAULT_RAW_AUDIT = (
    ROOT
    / "results/analysis/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq_audit_items.csv"
)
DEFAULT_QWEN3_COMPARE = (
    ROOT / "results/analysis/qwen3_4b_guarded_generated_en_v5_dev50_item_compare.csv"
)
DEFAULT_QWEN25_COMPARE = (
    ROOT / "results/analysis/qwen25_3b_guarded_generated_en_v5_dev50_item_compare.csv"
)
DEFAULT_QWEN3_ROUTE = (
    ROOT / "results/analysis/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev_items.csv"
)
DEFAULT_QWEN25_ROUTE = (
    ROOT / "results/analysis/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev_items.csv"
)
DEFAULT_ITEMS_OUTPUT = (
    ROOT / "results/analysis/guarded_generated_en_repair_provenance_items.csv"
)
DEFAULT_SUMMARY_OUTPUT = (
    ROOT / "results/analysis/guarded_generated_en_repair_provenance_summary.csv"
)
DEFAULT_REPORT = ROOT / "reports/guarded_generated_en_repair_provenance.md"


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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
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
    return str(value).strip().lower() == "true"


def index_by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("id", "")): row for row in rows}


def failure_labels(row: dict[str, str]) -> str:
    labels: list[str] = []
    if not truthy(row.get("digit_sequence_preserved", "True")):
        labels.append("digits")
    if not truthy(row.get("formulas_preserved", "True")):
        labels.append("formulas")
    if not truthy(row.get("line_count_preserved", "True")):
        labels.append("line_count")
    if truthy(row.get("extra_answer_marker", "False")):
        labels.append("extra_answer_marker")
    if not truthy(row.get("target_script_ok", "True")):
        labels.append("target_script")
    return ",".join(labels)


def compare_fields(row: dict[str, str], prefix: str) -> dict[str, Any]:
    baseline_correct = truthy(row.get("baseline_correct"))
    generated_correct = truthy(row.get("generated_correct"))
    return {
        f"{prefix}_baseline_correct": baseline_correct,
        f"{prefix}_guarded_en_correct": generated_correct,
        f"{prefix}_change": row.get("change", ""),
        f"{prefix}_baseline_parsed": row.get("baseline_parsed", ""),
        f"{prefix}_guarded_en_parsed": row.get("generated_parsed", ""),
    }


def route_fields(row: dict[str, str], prefix: str) -> dict[str, Any]:
    return {
        f"{prefix}_route_action": row.get("route_action", ""),
        f"{prefix}_routed_correct": truthy(row.get("routed_correct")),
        f"{prefix}_generated_bn_correct": truthy(row.get("generated_bn_correct")),
    }


def build_items(
    repair_rows: list[dict[str, Any]],
    raw_audit_rows: list[dict[str, str]],
    qwen3_compare_rows: list[dict[str, str]],
    qwen25_compare_rows: list[dict[str, str]],
    qwen3_route_rows: list[dict[str, str]],
    qwen25_route_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    raw_audit = index_by_id(raw_audit_rows)
    qwen3_compare = index_by_id(qwen3_compare_rows)
    qwen25_compare = index_by_id(qwen25_compare_rows)
    qwen3_route = index_by_id(qwen3_route_rows)
    qwen25_route = index_by_id(qwen25_route_rows)
    items: list[dict[str, Any]] = []
    for row in sorted(repair_rows, key=lambda r: str(r.get("id", ""))):
        item_id = str(row.get("id", ""))
        raw = raw_audit.get(item_id, {})
        out = {
            "id": item_id,
            "repair_strategy": row.get("repair_strategy", ""),
            "raw_hard_fail": truthy(raw.get("hard_fail", "False")),
            "raw_warning": truthy(raw.get("warning", "False")),
            "raw_failure_labels": failure_labels(raw) if raw else "",
        }
        out.update(compare_fields(qwen3_compare.get(item_id, {}), "qwen3"))
        out.update(compare_fields(qwen25_compare.get(item_id, {}), "qwen25"))
        out.update(route_fields(qwen3_route.get(item_id, {}), "qwen3"))
        out.update(route_fields(qwen25_route.get(item_id, {}), "qwen25"))
        items.append(out)
    return items


def summarize(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in items:
        groups[str(row["repair_strategy"])].append(row)
    groups["all"].extend(items)
    summary: list[dict[str, Any]] = []
    for strategy in sorted(groups, key=lambda key: (key != "all", key)):
        rows = groups[strategy]
        raw_failures = Counter()
        for row in rows:
            for label in str(row.get("raw_failure_labels", "")).split(","):
                if label:
                    raw_failures[label] += 1
        qwen3_baseline = sum(int(row["qwen3_baseline_correct"]) for row in rows)
        qwen3_guarded = sum(int(row["qwen3_guarded_en_correct"]) for row in rows)
        qwen25_baseline = sum(int(row["qwen25_baseline_correct"]) for row in rows)
        qwen25_guarded = sum(int(row["qwen25_guarded_en_correct"]) for row in rows)
        qwen3_agreement_rows = [
            row for row in rows if row["qwen3_route_action"] == "route_to_generated_agreement"
        ]
        qwen25_agreement_rows = [
            row for row in rows if row["qwen25_route_action"] == "route_to_generated_agreement"
        ]
        summary.append(
            {
                "repair_strategy": strategy,
                "n": len(rows),
                "raw_hard_fail": sum(int(row["raw_hard_fail"]) for row in rows),
                "raw_warning": sum(int(row["raw_warning"]) for row in rows),
                "raw_digit_fail": raw_failures["digits"],
                "raw_formula_fail": raw_failures["formulas"],
                "raw_line_count_warn": raw_failures["line_count"],
                "qwen3_banglish_correct": qwen3_baseline,
                "qwen3_guarded_en_correct": qwen3_guarded,
                "qwen3_delta": qwen3_guarded - qwen3_baseline,
                "qwen3_gains": sum(1 for row in rows if row["qwen3_change"] == "gain"),
                "qwen3_losses": sum(1 for row in rows if row["qwen3_change"] == "loss"),
                "qwen3_agreement_routed_items": len(qwen3_agreement_rows),
                "qwen3_agreement_routed_correct": sum(
                    int(row["qwen3_routed_correct"]) for row in qwen3_agreement_rows
                ),
                "qwen3_route_total_correct": sum(int(row["qwen3_routed_correct"]) for row in rows),
                "qwen25_banglish_correct": qwen25_baseline,
                "qwen25_guarded_en_correct": qwen25_guarded,
                "qwen25_delta": qwen25_guarded - qwen25_baseline,
                "qwen25_gains": sum(1 for row in rows if row["qwen25_change"] == "gain"),
                "qwen25_losses": sum(1 for row in rows if row["qwen25_change"] == "loss"),
                "qwen25_agreement_routed_items": len(qwen25_agreement_rows),
                "qwen25_agreement_routed_correct": sum(
                    int(row["qwen25_routed_correct"]) for row in qwen25_agreement_rows
                ),
                "qwen25_route_total_correct": sum(
                    int(row["qwen25_routed_correct"]) for row in rows
                ),
            }
        )
    return summary


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def markdown_table(rows: list[dict[str, Any]]) -> list[str]:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return lines


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    all_row = next(row for row in summary_rows if row["repair_strategy"] == "all")
    fallback = next(
        row
        for row in summary_rows
        if row["repair_strategy"] == "source_fallback_after_failed_repair"
    )
    translated = next(
        row
        for row in summary_rows
        if row["repair_strategy"] == "translated_stem_source_tail"
    )
    lines = [
        "# Guarded Generated-English Repair Provenance",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report separates the guarded generated-English answer effects by",
        "repair strategy. The guarded view is preservation-safe, but not all rows",
        "are actual translated-English stems.",
        "",
        "## Artifacts",
        "",
        f"- Item CSV: `{repo_path(items_output)}`",
        f"- Summary CSV: `{repo_path(summary_output)}`",
        "",
        "## Summary",
        "",
        *markdown_table(summary_rows),
        "",
        "## Interpretation",
        "",
        (
            f"- Overall, guarded EN is Qwen3 {all_row['qwen3_guarded_en_correct']}/"
            f"{all_row['n']} vs Banglish {all_row['qwen3_banglish_correct']}/"
            f"{all_row['n']}, and Qwen2.5 {all_row['qwen25_guarded_en_correct']}/"
            f"{all_row['n']} vs Banglish {all_row['qwen25_banglish_correct']}/"
            f"{all_row['n']}."
        ),
        (
            f"- Translated-stem rows: n={translated['n']}, Qwen3 delta "
            f"{translated['qwen3_delta']}, Qwen2.5 delta {translated['qwen25_delta']}."
        ),
        (
            f"- Source-fallback rows: n={fallback['n']}, Qwen3 delta "
            f"{fallback['qwen3_delta']}, Qwen2.5 delta {fallback['qwen25_delta']}."
        ),
        (
            f"- Agreement routing fires on {all_row['qwen3_agreement_routed_items']} "
            f"Qwen3 item and {all_row['qwen25_agreement_routed_items']} Qwen2.5 item."
        ),
        "- The guarded route should remain dev-only because source fallback dilutes",
        "  the generated-English intervention and the agreement route is too sparse.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair-output", type=Path, default=DEFAULT_REPAIR_OUTPUT)
    parser.add_argument("--raw-audit-items", type=Path, default=DEFAULT_RAW_AUDIT)
    parser.add_argument("--qwen3-compare", type=Path, default=DEFAULT_QWEN3_COMPARE)
    parser.add_argument("--qwen25-compare", type=Path, default=DEFAULT_QWEN25_COMPARE)
    parser.add_argument("--qwen3-route", type=Path, default=DEFAULT_QWEN3_ROUTE)
    parser.add_argument("--qwen25-route", type=Path, default=DEFAULT_QWEN25_ROUTE)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = build_items(
        read_jsonl(args.repair_output),
        read_csv(args.raw_audit_items),
        read_csv(args.qwen3_compare),
        read_csv(args.qwen25_compare),
        read_csv(args.qwen3_route),
        read_csv(args.qwen25_route),
    )
    summary_rows = summarize(items)
    write_csv(args.items_output, items)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    print(f"items={len(items)}")
    print(f"summary={args.summary_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
