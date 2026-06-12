#!/usr/bin/env python3
"""Validate generated thesis table artifacts."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TABLES = {
    "main_script_gap_validation200_v5.csv": ("Frozen V5 Main Script Gap", 3),
    "main_script_gap_validation200.csv": ("Main Script Gap", 3),
    "model_family_scaling_validation200.csv": ("Model Family And Scaling", 7),
    "selfnorm_validation200.csv": ("Self-Normalization", 3),
    "answer_signal_routing_test150.csv": ("Answer-Signal Routing", 2),
    "cross_script_answer_agreement.csv": ("Cross-Script Answer Agreement", 3),
    "generated_view_preservation_v2.csv": ("Generated-View Preservation Gates", 4),
    "deterministic_generated_view_smokes.csv": ("Deterministic Generated-View Smokes", 10),
    "generated_bn_candidate_preservation.csv": ("Generated-BN Candidate Preservation", 11),
    "generated_bn_reference_similarity_dev50.csv": ("Generated-BN Reference Similarity Dev50", 3),
    "generated_bn_answer_audit_dev50.csv": ("Generated-BN Answer Audit Dev50", 18),
    "generated_view_agreement_route_dev.csv": ("Generated-View Agreement Route Dev", 3),
    "v5_benqa_option_permutation_dev50.csv": ("V5 BEnQA Option Permutation Dev50", 2),
    "bnsentmix_external_validation.csv": ("BnSentMix External Validation", 3),
    "bnsentmix_model_complementarity.csv": ("BnSentMix Model Complementarity", 6),
    "bnsentmix_routing_devtest.csv": ("BnSentMix Routing Dev-Test", 3),
    "diagnostic_model_pilots.csv": ("Diagnostic Model Pilots", 3),
    "real_banglish_distribution.csv": ("Real Banglish Distribution", 4),
    "auto_suggested_banglish_sensitivity.csv": ("Auto-Suggested Banglish Sensitivity", 2),
    "v5_reviewed_banglish_sensitivity.csv": ("V5 Reviewed Banglish Sensitivity", 3),
    "v5_bad_row_policy_sensitivity.csv": ("V5 Flagged-Bad Policy Sensitivity", 9),
}


def add(rows: list[dict[str, str]], artifact: str, check: str, status: str, detail: str) -> None:
    rows.append({"artifact": artifact, "check": check, "status": status, "detail": detail})


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_csv(table_dir: Path, name: str, expected_rows: int, rows: list[dict[str, str]]) -> None:
    path = table_dir / name
    rel = str(path.relative_to(ROOT))
    if not path.exists():
        add(rows, rel, "exists", "error", "missing")
        return
    table_rows = read_rows(path)
    add(rows, rel, "exists", "ok", "present")
    add(
        rows,
        rel,
        "row_count",
        "ok" if len(table_rows) == expected_rows else "error",
        f"rows={len(table_rows)} expected={expected_rows}",
    )
    headers = list(table_rows[0].keys()) if table_rows else []
    add(rows, rel, "headers", "ok" if headers else "error", ",".join(headers))


def validate_markdown(table_dir: Path, rows: list[dict[str, str]]) -> None:
    path = table_dir / "thesis_tables.md"
    rel = str(path.relative_to(ROOT))
    if not path.exists():
        add(rows, rel, "exists", "error", "missing")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    add(rows, rel, "exists", "ok", "present")
    for _name, (section, _expected_rows) in EXPECTED_TABLES.items():
        add(
            rows,
            rel,
            f"section_{section}",
            "ok" if f"## {section}" in text else "error",
            section,
        )
    add(
        rows,
        rel,
        "regen_command",
        "ok" if "python3 scripts/build_thesis_tables.py" in text else "error",
        "python3 scripts/build_thesis_tables.py",
    )


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["artifact", "check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, str]], output: Path, csv_path: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    issues = [row for row in rows if row["status"] != "ok"]
    lines = [
        "# Thesis Table Integrity Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report validates generated thesis table CSVs and the consolidated",
        "Markdown table bundle.",
        "",
        f"Machine-readable check: `{csv_path.relative_to(ROOT)}`.",
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
            lines.append(f"- `{row['artifact']}` `{row['check']}`: {row['detail']}")
        lines.append("")
    else:
        lines.extend(["No thesis table integrity issues found.", ""])
    lines.extend(["## Checks", "", "| Artifact | Check | Status | Detail |", "| --- | --- | --- | --- |"])
    for row in rows:
        lines.append(f"| `{row['artifact']}` | `{row['check']}` | `{row['status']}` | {row['detail']} |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table-dir", type=Path, default=ROOT / "results/tables")
    parser.add_argument("--output-csv", type=Path, default=ROOT / "results/analysis/thesis_table_integrity_check.csv")
    parser.add_argument("--output-md", type=Path, default=ROOT / "reports/thesis_table_integrity_check.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows: list[dict[str, str]] = []
    for name, (_section, expected_rows) in EXPECTED_TABLES.items():
        validate_csv(args.table_dir, name, expected_rows, rows)
    validate_markdown(args.table_dir, rows)
    write_csv(rows, args.output_csv)
    write_report(rows, args.output_md, args.output_csv)
    issues = [row for row in rows if row["status"] != "ok"]
    print(f"checks={len(rows)} issues={len(issues)} report={args.output_md}")
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
