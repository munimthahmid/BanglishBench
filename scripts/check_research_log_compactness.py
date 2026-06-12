#!/usr/bin/env python3
"""Check that the restart research log stays compact and complete enough."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "research_log.md"
DEFAULT_OUTPUT = ROOT / "results/analysis/research_log_compactness_check.csv"
DEFAULT_REPORT = ROOT / "reports/research_log_compactness_check.md"
MAX_LINES = 300
MAX_BYTES = 20_000
REQUIRED_HEADINGS = [
    "## Fast Restart",
    "## Thesis Claim",
    "## Frozen Dataset",
    "## Main Results",
    "## Supporting Evidence",
    "## Model Breadth",
    "## Compute And QA",
    "## Immediate Queue",
]
REQUIRED_REFERENCES = [
    "reports/current_research_status_dashboard.md",
    "reports/next_experiment_decision_queue.md",
    "results/tables/main_script_gap_validation200_v5.csv",
    "reports/v5_recoverability_source_decomposition.md",
    "reports/v5_dataset_gap_intervals.md",
    "reports/v5_paired_sign_tests.md",
    "reports/v5_clustered_gap_robustness.md",
    "reports/v5_benqa_subject_stability.md",
    "reports/v5_benqa_subject_balance.md",
    "reports/cross_script_diagnostics_validation200_v5.md",
    "reports/v5_cross_script_transfer.md",
    "reports/v5_review_label_sensitivity.md",
    "reports/v5_banglish_fragility_feature_analysis.md",
    "reports/v5_qwen_scaling_transfer.md",
    "reports/v5_item_consensus.md",
    "reports/v5_difficulty_conditioned_gap.md",
    "reports/v5_consensus_stability.md",
    "reports/v5_composition_sensitivity.md",
    "reports/v5_answer_format_audit.md",
    "reports/v5_response_style_drift.md",
    "reports/v5_banglamath_numeric_sensitivity.md",
    "reports/v5_banglamath_numeric_transfer.md",
    "reports/v5_benqa_choice_bias.md",
    "reports/v5_benqa_subject_option_bias.md",
    "reports/v5_benqa_prediction_diversity.md",
    "reports/v5_benqa_option_position_content.md",
    "reports/v5_benqa_option_switching.md",
    "reports/v5_benqa_cross_script_option_agreement.md",
    "reports/v5_benqa_cross_model_banglish_agreement.md",
    "reports/v5_benqa_order_confound.md",
    "reports/v5_benqa_review_label_option_bias.md",
    "reports/v5_benqa_length_token_confound.md",
    "reports/v5_benqa_option_coverage_confound.md",
    "reports/v5_benqa_option_switch_confound.md",
    "reports/v5_benqa_option_semantic_cues.md",
    "reports/v5_benqa_multiconfound_residual.md",
    "reports/v5_benqa_distractor_transition.md",
    "reports/v5_benqa_label_balance.md",
    "reports/v5_benqa_option_permutation_probe_results.md",
    "reports/bnsentmix_external_validation_results.md",
    "reports/bnsentmix_model_complementarity.md",
    "reports/bnsentmix_routing_devtest.md",
    "reports/generated_view_diagnostics_summary.md",
    "reports/real_banglish_distribution_comparison.md",
    "reports/v5_banglatlit_lexical_coverage.md",
    "reports/v5_benqa_option_lexical_coverage.md",
    "reports/v5_banglatlit_model_coverage_sensitivity.md",
    "reports/v5_banglatlit_spelling_variation_sensitivity.md",
    "reports/v5_source_variant_structural_parity.md",
    "reports/v5_english_warning_sensitivity.md",
    "reports/v5_review_edit_distance_sensitivity.md",
    "reports/final_api_audit_cost_plan.md",
]
REQUIRED_PATTERNS = {
    "main_qwen25_3b": r"Qwen2\.5-3B\s*\|\s*54/200\s*\|\s*41/200",
    "main_qwen25_7b": r"Qwen2\.5-7B 8-bit\s*\|\s*65/200\s*\|\s*47/200",
    "main_qwen3_4b": r"Qwen3-4B\s*\|\s*80/200\s*\|\s*49/200",
    "fragility_events": r"185/600 model-item slots",
    "api_manifest_check": r"18/18 checks",
    "api_import_roundtrip": r"16/16 checks",
    "bnsentmix_external": r"BnSentMix[\s\S]*89/200[\s\S]*98/200[\s\S]*99/200",
    "bnsentmix_complementarity": r"BnSentMix[\s\S]*154/200[\s\S]*\+27\.5",
    "bnsentmix_routing": r"BnSentMix[\s\S]*106/200[\s\S]*84/200",
}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def add(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, rows: list[dict[str, str]], csv_path: Path, log_path: Path) -> None:
    issues = [row for row in rows if row["status"] != "ok"]
    lines = [
        "# Research Log Compactness Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This check keeps `research_log.md` as a compact restart ledger while",
        "guarding against accidental removal of thesis-critical results.",
        "",
        f"- Log: `{repo_path(log_path)}`",
        f"- Machine-readable checks: `{repo_path(csv_path)}`",
        "",
        "## Summary",
        "",
        f"- Checks: {len(rows)}",
        f"- Issues: {len(issues)}",
        "",
    ]
    if issues:
        lines.extend(["## Issues", ""])
        for row in issues:
            lines.append(f"- `{row['check']}`: {row['detail']}")
        lines.append("")
    else:
        lines.extend(["No research-log compactness issues found.", ""])
    lines.extend(["## Checks", "", "| Check | Status | Detail |", "| --- | --- | --- |"])
    for row in rows:
        lines.append(f"| `{row['check']}` | `{row['status']}` | {row['detail']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--max-lines", type=int, default=MAX_LINES)
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checks: list[dict[str, str]] = []
    exists = args.log.exists()
    add(checks, "exists", "ok" if exists else "error", repo_path(args.log) if exists else "missing")
    if not exists:
        write_csv(args.output_csv, checks)
        write_report(args.report_output, checks, args.output_csv, args.log)
        sys.exit(1)

    text = args.log.read_text(encoding="utf-8")
    lines = text.splitlines()
    byte_count = len(text.encode("utf-8"))
    add(
        checks,
        "line_count",
        "ok" if len(lines) <= args.max_lines else "error",
        f"lines={len(lines)} max={args.max_lines}",
    )
    add(
        checks,
        "byte_count",
        "ok" if byte_count <= args.max_bytes else "error",
        f"bytes={byte_count} max={args.max_bytes}",
    )
    for heading in REQUIRED_HEADINGS:
        add(
            checks,
            f"heading:{heading[3:]}",
            "ok" if heading in text else "error",
            "present" if heading in text else "missing",
        )
    for reference in REQUIRED_REFERENCES:
        add(
            checks,
            f"reference:{reference}",
            "ok" if reference in text else "error",
            "present" if reference in text else "missing",
        )
    for label, pattern in REQUIRED_PATTERNS.items():
        add(
            checks,
            f"pattern:{label}",
            "ok" if re.search(pattern, text) else "error",
            "present" if re.search(pattern, text) else "missing",
        )

    write_csv(args.output_csv, checks)
    write_report(args.report_output, checks, args.output_csv, args.log)
    issues = [row for row in checks if row["status"] != "ok"]
    print(f"checks={len(checks)} issues={len(issues)} report={args.report_output}")
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
