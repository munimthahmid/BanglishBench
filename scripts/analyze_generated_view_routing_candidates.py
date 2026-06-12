#!/usr/bin/env python3
"""Evaluate deployable generated-view routing candidates on dev items."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "results/analysis/generated_view_route_bottleneck_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/generated_view_routing_candidate_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/generated_view_routing_candidate_summary.csv"
DEFAULT_REPORT = ROOT / "reports/generated_view_routing_candidate_scan.md"


RouteFn = Callable[[dict[str, str]], tuple[str, str]]


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


def is_correct(answer: str, gold: str) -> bool:
    return bool(answer) and answer.strip().upper() == gold.strip().upper()


def answers(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("banglish_parsed", "").strip().upper(),
        row.get("generated_bn_parsed", "").strip().upper(),
        row.get("generated_en_parsed", "").strip().upper(),
    )


def baseline(row: dict[str, str]) -> tuple[str, str]:
    banglish, _bn, _en = answers(row)
    return banglish, "baseline"


def strict_generated_agreement(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, en = answers(row)
    if bn and en and bn == en and bn != banglish:
        return bn, "bn_en_agree_nonbaseline"
    return banglish, "fallback_baseline"


def majority_or_baseline(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, en = answers(row)
    if banglish and banglish == bn:
        return banglish, "banglish_bn_majority"
    if banglish and banglish == en:
        return banglish, "banglish_en_majority"
    if bn and en and bn == en:
        return bn, "bn_en_majority"
    return banglish, "fallback_baseline"


def generated_bn_only(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, _en = answers(row)
    if bn:
        return bn, "use_generated_bn"
    return banglish, "fallback_baseline"


def generated_en_only(row: dict[str, str]) -> tuple[str, str]:
    banglish, _bn, en = answers(row)
    if en:
        return en, "use_generated_en"
    return banglish, "fallback_baseline"


def generated_bn_if_baseline_empty(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, _en = answers(row)
    if not banglish and bn:
        return bn, "baseline_empty_use_bn"
    return banglish, "fallback_baseline"


def generated_en_if_baseline_empty(row: dict[str, str]) -> tuple[str, str]:
    banglish, _bn, en = answers(row)
    if not banglish and en:
        return en, "baseline_empty_use_en"
    return banglish, "fallback_baseline"


def all_disagree_bn_tiebreak(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, en = answers(row)
    if bn and en and bn == en and bn != banglish:
        return bn, "bn_en_agree_nonbaseline"
    if banglish and bn and en and len({banglish, bn, en}) == 3:
        return bn, "all_disagree_use_bn"
    return banglish, "fallback_baseline"


def all_disagree_en_tiebreak(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, en = answers(row)
    if bn and en and bn == en and bn != banglish:
        return bn, "bn_en_agree_nonbaseline"
    if banglish and bn and en and len({banglish, bn, en}) == 3:
        return en, "all_disagree_use_en"
    return banglish, "fallback_baseline"


def generated_priority_nonbaseline(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, en = answers(row)
    if bn and en and bn == en and bn != banglish:
        return bn, "bn_en_agree_nonbaseline"
    if bn and bn != banglish:
        return bn, "bn_nonbaseline_priority"
    if en and en != banglish:
        return en, "en_nonbaseline_priority"
    return banglish, "fallback_baseline"


def generated_en_priority_nonbaseline(row: dict[str, str]) -> tuple[str, str]:
    banglish, bn, en = answers(row)
    if bn and en and bn == en and bn != banglish:
        return bn, "bn_en_agree_nonbaseline"
    if en and en != banglish:
        return en, "en_nonbaseline_priority"
    if bn and bn != banglish:
        return bn, "bn_nonbaseline_priority"
    return banglish, "fallback_baseline"


RULES: list[tuple[str, str, RouteFn]] = [
    ("baseline", "Use Banglish answer.", baseline),
    (
        "strict_generated_agreement",
        "Route only when generated-BN and generated-EN agree on a non-baseline answer.",
        strict_generated_agreement,
    ),
    ("three_view_majority", "Use any two-of-three answer majority, else baseline.", majority_or_baseline),
    ("generated_bn_only", "Always use generated-BN when parsed.", generated_bn_only),
    ("generated_en_only", "Always use generated-EN when parsed.", generated_en_only),
    (
        "generated_bn_if_baseline_empty",
        "Use generated-BN only when Banglish parsing is empty.",
        generated_bn_if_baseline_empty,
    ),
    (
        "generated_en_if_baseline_empty",
        "Use generated-EN only when Banglish parsing is empty.",
        generated_en_if_baseline_empty,
    ),
    (
        "all_disagree_bn_tiebreak",
        "Strict agreement, plus use generated-BN when all three views disagree.",
        all_disagree_bn_tiebreak,
    ),
    (
        "all_disagree_en_tiebreak",
        "Strict agreement, plus use generated-EN when all three views disagree.",
        all_disagree_en_tiebreak,
    ),
    (
        "generated_bn_priority_nonbaseline",
        "Strict agreement, else prefer generated-BN when it differs from baseline.",
        generated_priority_nonbaseline,
    ),
    (
        "generated_en_priority_nonbaseline",
        "Strict agreement, else prefer generated-EN when it differs from baseline.",
        generated_en_priority_nonbaseline,
    ),
]


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        gold = row.get("gold", "").strip().upper()
        baseline_correct = truthy(row.get("banglish_correct"))
        for rule_name, _description, route_fn in RULES:
            routed_answer, action = route_fn(row)
            routed_correct = is_correct(routed_answer, gold)
            changed_from_baseline = routed_answer != row.get("banglish_parsed", "").strip().upper()
            out.append(
                {
                    "route": row["route"],
                    "id": row["id"],
                    "gold": gold,
                    "rule": rule_name,
                    "action": action,
                    "routed_answer": routed_answer,
                    "routed_correct": routed_correct,
                    "baseline_correct": baseline_correct,
                    "delta_vs_baseline": int(routed_correct) - int(baseline_correct),
                    "changed_from_baseline": changed_from_baseline,
                    "banglish_parsed": row.get("banglish_parsed", ""),
                    "generated_bn_parsed": row.get("generated_bn_parsed", ""),
                    "generated_en_parsed": row.get("generated_en_parsed", ""),
                    "repair_strategy": row.get("repair_strategy", ""),
                }
            )
    return out


def summarize(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in item_rows:
        grouped[(row["route"], row["rule"])].append(row)
    summary: list[dict[str, Any]] = []
    description = {name: desc for name, desc, _fn in RULES}
    for (route, rule), rows in sorted(grouped.items()):
        n = len(rows)
        baseline_correct = sum(int(row["baseline_correct"]) for row in rows)
        routed_correct = sum(int(row["routed_correct"]) for row in rows)
        actions = sorted({str(row["action"]) for row in rows if row["action"] != "fallback_baseline"})
        routed_nonbaseline = sum(int(row["changed_from_baseline"]) for row in rows)
        summary.append(
            {
                "route": route,
                "rule": rule,
                "n": n,
                "baseline_correct": baseline_correct,
                "routed_correct": routed_correct,
                "delta_vs_baseline": routed_correct - baseline_correct,
                "gains": sum(1 for row in rows if row["delta_vs_baseline"] > 0),
                "losses": sum(1 for row in rows if row["delta_vs_baseline"] < 0),
                "routed_nonbaseline": routed_nonbaseline,
                "actions": ",".join(actions),
                "description": description[rule],
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
    headers = [
        "route",
        "rule",
        "baseline",
        "routed",
        "delta",
        "gains",
        "losses",
        "routed_nonbaseline",
    ]
    lines = [
        "| Route | Rule | Baseline | Routed | Delta | Gains | Losses | Routed nonbaseline |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["route"]),
                    str(row["rule"]),
                    f"{row['baseline_correct']}/{row['n']}",
                    f"{row['routed_correct']}/{row['n']}",
                    str(row["delta_vs_baseline"]),
                    str(row["gains"]),
                    str(row["losses"]),
                    str(row["routed_nonbaseline"]),
                ]
            )
            + " |"
        )
    return lines


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    best_by_route: list[dict[str, Any]] = []
    for route in sorted({row["route"] for row in summary_rows}):
        candidates = [row for row in summary_rows if row["route"] == route]
        best = max(
            candidates,
            key=lambda row: (
                int(row["delta_vs_baseline"]),
                -int(row["losses"]),
                -int(row["routed_nonbaseline"]),
            ),
        )
        best_by_route.append(best)
    lines = [
        "# Generated-View Routing Candidate Scan",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This dev-only scan evaluates simple deployable answer-routing rules over",
        "the existing Banglish, generated-BN, and generated-EN parsed answers. It",
        "does not authorize held-out testing; it identifies whether a rule family",
        "is promising enough to preregister later.",
        "",
        "## Artifacts",
        "",
        f"- Item CSV: `{repo_path(items_output)}`",
        f"- Summary CSV: `{repo_path(summary_output)}`",
        "",
        "## Best Rule Per Route",
        "",
        *markdown_table(best_by_route),
        "",
        "## Full Summary",
        "",
        *markdown_table(summary_rows),
        "",
        "## Decision",
        "",
        "No candidate is strong enough to justify generated-view test150.",
        "Rules that route more often can expose generated-view oracle signal, but",
        "they also add losses and are selected on the same small 36-item dev set.",
        "Keep the current generated-view branch as diagnostic evidence unless a",
        "better generated-English source and a pre-registered routing rule are",
        "available.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(read_csv(args.items))
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, summary_rows, args.items_output, args.summary_output)
    print(f"items={len(item_rows)}")
    print(f"summary={args.summary_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
