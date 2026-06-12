#!/usr/bin/env python3
"""Summarize why generated-view agreement routing is weak on dev."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROVENANCE = ROOT / "results/analysis/guarded_generated_en_repair_provenance_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/generated_view_route_bottleneck_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/generated_view_route_bottleneck_summary.csv"
DEFAULT_REPORT = ROOT / "reports/generated_view_route_bottleneck_analysis.md"

DEFAULT_ROUTE_SPECS = [
    (
        "Qwen3 historical protected-v1 BNB + raw self-translate EN",
        ROOT / "results/analysis/qwen3_4b_generated_view_agreement_route_dev_items.csv",
        "raw_self_translate",
    ),
    (
        "Qwen3 protected-v3 BNB + guarded EN",
        ROOT / "results/analysis/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev_items.csv",
        "guarded",
    ),
    (
        "Qwen2.5 protected-v3 phonetic + guarded EN",
        ROOT / "results/analysis/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev_items.csv",
        "guarded",
    ),
]


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


def load_repair_strategy(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return {row["id"]: row.get("repair_strategy", "") for row in read_csv(path)}


def build_item_rows(provenance_path: Path) -> list[dict[str, Any]]:
    repair_strategy = load_repair_strategy(provenance_path)
    out: list[dict[str, Any]] = []
    for route_name, path, en_source in DEFAULT_ROUTE_SPECS:
        if not path.exists():
            continue
        for row in read_csv(path):
            banglish_correct = truthy(row.get("banglish_correct"))
            bn_correct = truthy(row.get("generated_bn_correct"))
            en_correct = truthy(row.get("generated_en_correct"))
            routed_correct = truthy(row.get("routed_correct"))
            bn_answer = row.get("generated_bn_parsed", "")
            en_answer = row.get("generated_en_parsed", "")
            banglish_answer = row.get("banglish_parsed", "")
            generated_agreement = bool(bn_answer and en_answer and bn_answer == en_answer)
            generated_agreement_correct = generated_agreement and (bn_correct or en_correct)
            generated_view_oracle_correct = bn_correct or en_correct
            triad_oracle_correct = banglish_correct or generated_view_oracle_correct
            baseline_wrong_generated_oracle = (not banglish_correct) and generated_view_oracle_correct
            baseline_wrong_agreement_correct = (
                (not banglish_correct) and generated_agreement_correct
            )
            baseline_correct_agreement_wrong = (
                banglish_correct
                and generated_agreement
                and not generated_agreement_correct
                and bn_answer != banglish_answer
            )
            generated_disagreement = bool(bn_answer and en_answer and bn_answer != en_answer)
            generated_disagreement_any_correct = generated_disagreement and generated_view_oracle_correct
            if en_source == "guarded":
                strategy = repair_strategy.get(row["id"], "guarded_unknown")
            else:
                strategy = en_source
            out.append(
                {
                    "route": route_name,
                    "id": row["id"],
                    "gold": row.get("gold", ""),
                    "repair_strategy": strategy,
                    "banglish_parsed": banglish_answer,
                    "generated_bn_parsed": bn_answer,
                    "generated_en_parsed": en_answer,
                    "banglish_correct": banglish_correct,
                    "generated_bn_correct": bn_correct,
                    "generated_en_correct": en_correct,
                    "generated_view_oracle_correct": generated_view_oracle_correct,
                    "triad_oracle_correct": triad_oracle_correct,
                    "generated_agreement": generated_agreement,
                    "generated_agreement_correct": generated_agreement_correct,
                    "baseline_wrong_generated_oracle": baseline_wrong_generated_oracle,
                    "baseline_wrong_agreement_correct": baseline_wrong_agreement_correct,
                    "baseline_correct_agreement_wrong": baseline_correct_agreement_wrong,
                    "generated_disagreement": generated_disagreement,
                    "generated_disagreement_any_correct": generated_disagreement_any_correct,
                    "route_action": row.get("route_action", ""),
                    "routed_correct": routed_correct,
                }
            )
    return out


def summarize_group(route: str, group: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    route_counts = Counter(row["route_action"] for row in rows)
    banglish = sum(int(row["banglish_correct"]) for row in rows)
    routed = sum(int(row["routed_correct"]) for row in rows)
    baseline_wrong_generated_oracle = sum(
        int(row["baseline_wrong_generated_oracle"]) for row in rows
    )
    baseline_wrong_agreement_correct = sum(
        int(row["baseline_wrong_agreement_correct"]) for row in rows
    )
    return {
        "route": route,
        "group": group,
        "n": n,
        "banglish_correct": banglish,
        "generated_bn_correct": sum(int(row["generated_bn_correct"]) for row in rows),
        "generated_en_correct": sum(int(row["generated_en_correct"]) for row in rows),
        "generated_view_oracle_correct": sum(
            int(row["generated_view_oracle_correct"]) for row in rows
        ),
        "triad_oracle_correct": sum(int(row["triad_oracle_correct"]) for row in rows),
        "generated_agreement_items": sum(int(row["generated_agreement"]) for row in rows),
        "generated_agreement_correct": sum(
            int(row["generated_agreement_correct"]) for row in rows
        ),
        "baseline_wrong_generated_oracle": baseline_wrong_generated_oracle,
        "baseline_wrong_agreement_correct": baseline_wrong_agreement_correct,
        "missed_generated_oracle_by_agreement": (
            baseline_wrong_generated_oracle - baseline_wrong_agreement_correct
        ),
        "baseline_correct_agreement_wrong": sum(
            int(row["baseline_correct_agreement_wrong"]) for row in rows
        ),
        "generated_disagreement_items": sum(
            int(row["generated_disagreement"]) for row in rows
        ),
        "generated_disagreement_any_correct": sum(
            int(row["generated_disagreement_any_correct"]) for row in rows
        ),
        "current_routed_items": route_counts["route_to_generated_agreement"],
        "current_routed_correct": routed,
        "current_routed_minus_banglish": routed - banglish,
    }


def summarize(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in items:
        grouped[(row["route"], "all")].append(row)
        if row["repair_strategy"] != "raw_self_translate":
            grouped[(row["route"], row["repair_strategy"])].append(row)
    summaries: list[dict[str, Any]] = []
    for (route, group), rows in sorted(grouped.items()):
        summaries.append(summarize_group(route, group, rows))
    return summaries


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


def compact_summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "Route": row["route"],
            "Group": row["group"],
            "Banglish": f"{row['banglish_correct']}/{row['n']}",
            "Generated-view oracle": f"{row['generated_view_oracle_correct']}/{row['n']}",
            "Triad oracle": f"{row['triad_oracle_correct']}/{row['n']}",
            "Generated agreement": f"{row['generated_agreement_correct']}/{row['generated_agreement_items']}",
            "Recoverable by generated views": row["baseline_wrong_generated_oracle"],
            "Recovered by agreement": row["baseline_wrong_agreement_correct"],
            "Missed by agreement": row["missed_generated_oracle_by_agreement"],
            "Disagree+one-correct": row["generated_disagreement_any_correct"],
            "Current route": f"{row['current_routed_correct']}/{row['n']}",
            "Route delta": row["current_routed_minus_banglish"],
        }
        for row in rows
        if row["group"] == "all"
    ]


def write_report(path: Path, summary_rows: list[dict[str, Any]], items_path: Path, summary_path: Path) -> None:
    all_rows = [row for row in summary_rows if row["group"] == "all"]
    lines = [
        "# Generated-View Route Bottleneck Analysis",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This dev-only analysis asks why protected generated-BN plus generated-EN",
        "agreement routing is weak. It compares the current conservative agreement",
        "route with two upper bounds: generated-view oracle and triad oracle.",
        "",
        "## Artifacts",
        "",
        f"- Item CSV: `{repo_path(items_path)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        "",
        "## Route Summary",
        "",
        *markdown_table(compact_summary_rows(all_rows)),
        "",
        "## Reading The Columns",
        "",
        "- Generated-view oracle counts rows where either generated-BN or generated-EN is correct.",
        "- Triad oracle counts rows where Banglish, generated-BN, or generated-EN is correct.",
        "- Recoverable by generated views counts baseline-wrong rows where at least one generated view is correct.",
        "- Recovered by agreement is the subset where generated-BN and generated-EN agree on the correct answer.",
        "- Disagree+one-correct shows recoverable rows missed by a strict agreement rule.",
        "",
        "## Interpretation",
        "",
    ]
    for row in all_rows:
        lines.append(
            f"- {row['route']}: generated views contain {row['baseline_wrong_generated_oracle']} "
            f"baseline-wrong recoveries, but agreement recovers only "
            f"{row['baseline_wrong_agreement_correct']} and misses "
            f"{row['missed_generated_oracle_by_agreement']}."
        )
    lines.extend(
        [
            "- The bottleneck is not only preservation. The generated views often do not",
            "  agree when one of them is correct, so the conservative route is sparse.",
            "- This supports the current decision not to launch generated-view test150",
            "  until a better generated-English source or a pre-registered stronger",
            "  routing signal is available.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provenance-items", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(args.provenance_items)
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    print(f"items={len(item_rows)}")
    print(f"summary={args.summary_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
