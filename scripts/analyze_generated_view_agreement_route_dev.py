#!/usr/bin/env python3
"""Analyze dev-only generated-BN + generated-EN agreement routing."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = (
    ROOT
    / "data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl"
)
DEFAULT_BN_EVAL = (
    ROOT
    / "results/runs/qwen3_4b_generated_bn_answer_audit_dev50/results/runs/qwen3_4b_generated_bn_answer_audit_dev50.jsonl"
)
DEFAULT_EN_EVAL = (
    ROOT
    / "results/runs/qwen3_4b_generated_en_selftranslate_dev50/results/runs/qwen3_4b_generated_en_selftranslate_dev50.jsonl"
)
DEFAULT_ITEMS_OUTPUT = (
    ROOT / "results/analysis/qwen3_4b_generated_view_agreement_route_dev_items.csv"
)
DEFAULT_SUMMARY_OUTPUT = (
    ROOT / "results/analysis/qwen3_4b_generated_view_agreement_route_dev_summary.csv"
)
DEFAULT_REPORT = ROOT / "reports/qwen3_4b_generated_view_agreement_route_dev.md"
DEFAULT_EN_AUDIT = (
    ROOT / "results/analysis/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq_audit_items.csv"
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_eval(path: Path, rescore: bool) -> list[dict[str, Any]]:
    rows = load_jsonl(path)
    for row in rows:
        if rescore:
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
    return rows


def index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(str(row.get("id", "")), str(row.get("variant", ""))): row for row in rows}


def load_failed_generated_views(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    failed: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if str(row.get("hard_fail", "")).lower() == "true":
                failed.add(str(row.get("id", "")))
    return failed


def route_answer(banglish: str, bn: str, en: str, en_hard_fail: bool) -> tuple[str, str]:
    if en_hard_fail:
        return banglish, "fallback_generated_en_gate"
    if bn and en and bn == en and banglish != bn:
        return bn, "route_to_generated_agreement"
    return banglish, "fallback_banglish"


def analyze(
    items: dict[str, dict[str, Any]],
    bn_rows: list[dict[str, Any]],
    en_rows: list[dict[str, Any]],
    en_failed_ids: set[str],
    baseline_variant: str,
    bn_variant: str,
    en_variant: str,
) -> list[dict[str, Any]]:
    bn = index(bn_rows)
    en = index(en_rows)
    out: list[dict[str, Any]] = []
    for item_id in sorted(items):
        baseline = bn.get((item_id, baseline_variant))
        generated_bn = bn.get((item_id, bn_variant))
        generated_en = en.get((item_id, en_variant))
        if not baseline or not generated_bn or not generated_en:
            continue
        en_hard_fail = item_id in en_failed_ids
        routed, action = route_answer(
            str(baseline.get("parsed", "")),
            str(generated_bn.get("parsed", "")),
            str(generated_en.get("parsed", "")),
            en_hard_fail,
        )
        gold = str(baseline.get("gold", ""))
        out.append(
            {
                "id": item_id,
                "gold": gold,
                "banglish_parsed": baseline.get("parsed", ""),
                "generated_bn_parsed": generated_bn.get("parsed", ""),
                "generated_en_parsed": generated_en.get("parsed", ""),
                "route_action": action,
                "routed_parsed": routed,
                "banglish_correct": bool(baseline.get("correct")),
                "generated_bn_correct": bool(generated_bn.get("correct")),
                "generated_en_correct": bool(generated_en.get("correct")),
                "generated_en_hard_fail": en_hard_fail,
                "routed_correct": is_correct(routed, gold, "choice"),
                "generated_en_rewrite_preview": str(generated_en.get("rewrite_output", ""))[:260].replace("\n", " "),
            }
        )
    return out


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    n = len(rows)
    counts = Counter(row["route_action"] for row in rows)
    return [
        {
            "n": n,
            "banglish_correct": sum(int(row["banglish_correct"]) for row in rows),
            "generated_bn_correct": sum(int(row["generated_bn_correct"]) for row in rows),
            "generated_en_correct": sum(int(row["generated_en_correct"]) for row in rows),
            "routed_correct": sum(int(row["routed_correct"]) for row in rows),
            "routed_minus_banglish": sum(int(row["routed_correct"]) for row in rows)
            - sum(int(row["banglish_correct"]) for row in rows),
            "route_to_generated_agreement": counts["route_to_generated_agreement"],
            "fallback_generated_en_gate": counts["fallback_generated_en_gate"],
            "fallback_banglish": counts["fallback_banglish"],
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def write_report(
    path: Path,
    bn_eval: Path,
    en_eval: Path,
    items_output: Path,
    summary_output: Path,
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    bn_label: str,
    en_label: str,
    decision_note: str,
    report_title: str,
) -> None:
    routed_rows = [row for row in rows if row["route_action"] == "route_to_generated_agreement"]
    lines = [
        f"# {report_title}",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Generated-BN answer audit: `{repo_path(bn_eval)}`",
        f"- Generated-EN self-translate audit: `{repo_path(en_eval)}`",
        f"- Item route CSV: `{repo_path(items_output)}`",
        f"- Summary CSV: `{repo_path(summary_output)}`",
        "",
        "## Result",
        "",
        f"- n: {summary['n']}",
        f"- Banglish: {summary['banglish_correct']}/{summary['n']}",
        f"- {bn_label}: {summary['generated_bn_correct']}/{summary['n']}",
        f"- {en_label}: {summary['generated_en_correct']}/{summary['n']}",
        f"- Agreement routed: {summary['routed_correct']}/{summary['n']}",
        f"- Routed minus Banglish: {summary['routed_minus_banglish']}",
        f"- Routed items: {summary['route_to_generated_agreement']}",
        f"- Fallback due generated-EN hard gate: {summary['fallback_generated_en_gate']}",
        f"- Fallback Banglish items: {summary['fallback_banglish']}",
        "",
        "## Routed Items",
        "",
    ]
    if routed_rows:
        for row in routed_rows:
            lines.append(
                f"- `{row['id']}` gold={row['gold']} banglish={row['banglish_parsed']} "
                f"bn={row['generated_bn_parsed']} en={row['generated_en_parsed']} "
                f"routed={row['routed_parsed']} correct={row['routed_correct']}"
            )
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Decision Rule",
            "",
            "This is a dev-only diagnostic using generated-BN plus generated-EN.",
            decision_note,
            "Do not launch test150 unless the generation method, preservation",
            "gates, and routing rule are frozen in advance.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--bn-eval", type=Path, default=DEFAULT_BN_EVAL)
    parser.add_argument("--en-eval", type=Path, default=DEFAULT_EN_EVAL)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--en-audit-items", type=Path, default=DEFAULT_EN_AUDIT)
    parser.add_argument("--baseline-variant", default="banglish_clean")
    parser.add_argument("--bn-variant", default="generated_bn_bnb_protected")
    parser.add_argument("--en-variant", default="banglish_clean")
    parser.add_argument("--bn-label", default="Historical protected-v1 BNB generated-BN")
    parser.add_argument("--en-label", default="Generated English self-translate")
    parser.add_argument(
        "--report-title",
        default="Qwen3-4B Generated-View Agreement Route: Dev",
    )
    parser.add_argument(
        "--decision-note",
        default=(
            "The generated-BN input is historical protected-v1 and fails the "
            "tightened scientific-token gate; it is not route-ready evidence."
        ),
    )
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = {str(row["id"]): row for row in load_jsonl(args.items)}
    rows = analyze(
        items,
        load_eval(args.bn_eval, args.rescore),
        load_eval(args.en_eval, args.rescore),
        load_failed_generated_views(args.en_audit_items),
        args.baseline_variant,
        args.bn_variant,
        args.en_variant,
    )
    summary_rows = summarize(rows)
    write_csv(args.items_output, rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        args.bn_eval,
        args.en_eval,
        args.items_output,
        args.summary_output,
        rows,
        summary_rows[0],
        args.bn_label,
        args.en_label,
        args.decision_note,
        args.report_title,
    )
    print(f"rows={len(rows)}")
    print(f"summary={args.summary_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
