#!/usr/bin/env python3
"""Validate the human Banglish review queue before freezing a new slice."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_SOURCE = ROOT / "data/slices/validation_200_v4.jsonl"
DEFAULT_ISSUES = ROOT / "results/analysis/validation200_v5_review_validation_issues.csv"
DEFAULT_REPORT = ROOT / "reports/validation200_v5_review_validation.md"

REQUIRED_COLUMNS = [
    "id",
    "dataset",
    "answer_type",
    "answer",
    "bangla",
    "english",
    "current_banglish_clean",
    "auto_suggested_banglish_clean",
    "reviewed_banglish",
    "quality_label",
    "review_notes",
]
ALLOWED_LABELS = {"ok", "minor_edit", "major_edit", "bad"}

BN_RE = re.compile(r"[\u0980-\u09ff]")
DIGIT_RE = re.compile(r"[0-9\u09e6-\u09ef]")
OPTION_RE = re.compile(r"^\s*([A-D])[\).]\s+", re.MULTILINE)
FORMULA_RE = re.compile(r"\b[A-Z][A-Za-z]?[0-9]*(?:[A-Z][A-Za-z]?[0-9]*)+\b")
ANSWER_MARKER_RE = re.compile(
    r"\bfinal\s+answer\s*:|\banswer\s*:|সঠিক\s+উত্তর|উত্তর\s*:",
    flags=re.IGNORECASE,
)
DIGIT_TRANS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def normalize_digits(text: str) -> list[str]:
    return [match.translate(DIGIT_TRANS) for match in DIGIT_RE.findall(text)]


def option_labels(text: str) -> list[str]:
    return OPTION_RE.findall(text)


def formulas(text: str) -> list[str]:
    return sorted(set(FORMULA_RE.findall(text)))


def answer_marker_count(text: str) -> int:
    return len(ANSWER_MARKER_RE.findall(text))


def instruction_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip().lower().startswith("return only")
    ]


def candidate_text(row: dict[str, str]) -> str:
    replacement = row.get("reviewed_banglish", "").strip()
    return replacement or row.get("current_banglish_clean", "")


def add_issue(
    issues: list[dict[str, str]],
    row: dict[str, str],
    severity: str,
    code: str,
    message: str,
) -> None:
    issues.append(
        {
            "severity": severity,
            "code": code,
            "id": row.get("id", ""),
            "dataset": row.get("dataset", ""),
            "quality_label": row.get("quality_label", "").strip(),
            "message": message,
        }
    )


def validate_columns(fieldnames: list[str]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    for column in missing:
        issues.append(
            {
                "severity": "error",
                "code": "missing_column",
                "id": "",
                "dataset": "",
                "quality_label": "",
                "message": f"Required column is missing: {column}",
            }
        )
    return issues


def validate_row(
    row: dict[str, str],
    source_by_id: dict[str, dict[str, Any]],
    seen_ids: set[str],
    issues: list[dict[str, str]],
) -> None:
    item_id = row.get("id", "").strip()
    label = row.get("quality_label", "").strip()
    replacement = row.get("reviewed_banglish", "").strip()
    notes = row.get("review_notes", "").strip()
    current = row.get("current_banglish_clean", "")
    candidate = candidate_text(row)

    if not item_id:
        add_issue(issues, row, "error", "missing_id", "Review row has no id.")
    elif item_id in seen_ids:
        add_issue(issues, row, "error", "duplicate_id", "Duplicate review id.")
    seen_ids.add(item_id)

    source = source_by_id.get(item_id)
    if source is None:
        add_issue(
            issues,
            row,
            "error",
            "source_id_missing",
            "Review id does not exist in the source JSONL slice.",
        )
    elif str(source.get("banglish_clean", "")) != current:
        add_issue(
            issues,
            row,
            "warning",
            "current_banglish_mismatch",
            "Queue current_banglish_clean differs from source banglish_clean.",
        )

    if not label:
        if replacement:
            add_issue(
                issues,
                row,
                "error",
                "replacement_without_label",
                "Replacement is present but quality_label is blank.",
            )
        else:
            add_issue(
                issues,
                row,
                "pending",
                "blank_review",
                "Review fields are still blank.",
            )
        return

    if label not in ALLOWED_LABELS:
        add_issue(
            issues,
            row,
            "error",
            "invalid_quality_label",
            f"Invalid quality_label: {label}",
        )
        return

    if label == "ok" and replacement:
        add_issue(
            issues,
            row,
            "warning",
            "ok_with_replacement",
            "quality_label is ok, but reviewed_banglish is populated.",
        )
    if label in {"minor_edit", "major_edit"} and not replacement:
        add_issue(
            issues,
            row,
            "error",
            "edit_label_without_replacement",
            "minor_edit/major_edit requires reviewed_banglish.",
        )
    if label == "bad" and replacement:
        add_issue(
            issues,
            row,
            "error",
            "bad_with_replacement",
            "bad rows must not include reviewed_banglish; the freeze script would replace them.",
        )
    if label == "bad" and not notes:
        add_issue(
            issues,
            row,
            "warning",
            "bad_without_review_notes",
            "bad rows should include a short reason in review_notes.",
        )

    if not candidate.strip():
        add_issue(issues, row, "error", "empty_candidate", "Candidate text is empty.")
        return

    if BN_RE.search(candidate):
        add_issue(
            issues,
            row,
            "error",
            "bengali_script_in_banglish",
            "Candidate Banglish contains Bengali-script characters.",
        )

    source_digits = normalize_digits(row.get("bangla", ""))
    candidate_digits = normalize_digits(candidate)
    if source_digits != candidate_digits:
        add_issue(
            issues,
            row,
            "error",
            "digit_sequence_changed",
            "Candidate digit sequence does not match the Bengali source.",
        )

    current_options = option_labels(current)
    candidate_options = option_labels(candidate)
    if current_options != candidate_options:
        add_issue(
            issues,
            row,
            "error",
            "option_labels_changed",
            "Candidate option labels differ from current Banglish.",
        )

    current_formulas = formulas(current)
    candidate_formulas = formulas(candidate)
    if current_formulas != candidate_formulas:
        add_issue(
            issues,
            row,
            "error",
            "formulas_changed",
            "Candidate formula-like tokens differ from current Banglish.",
        )

    current_instructions = instruction_lines(current)
    candidate_instructions = instruction_lines(candidate)
    if current_instructions != candidate_instructions:
        add_issue(
            issues,
            row,
            "error",
            "answer_instruction_changed",
            "Candidate answer-format instruction differs from current Banglish.",
        )

    if answer_marker_count(candidate) > answer_marker_count(current):
        add_issue(
            issues,
            row,
            "error",
            "extra_answer_marker",
            "Candidate appears to add an answer marker.",
        )

    current_line_count = len(current.splitlines())
    candidate_line_count = len(candidate.splitlines())
    if current_line_count != candidate_line_count:
        add_issue(
            issues,
            row,
            "warning",
            "line_count_changed",
            "Candidate line count differs from current Banglish.",
        )


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["severity", "code", "id", "dataset", "quality_label", "message"]
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
    review_path: Path,
    source_path: Path,
    rows: list[dict[str, str]],
    issues: list[dict[str, str]],
    issues_path: Path,
    require_complete: bool,
) -> None:
    severity_counts = Counter(issue["severity"] for issue in issues)
    code_counts = Counter(issue["code"] for issue in issues)
    label_counts = Counter(row.get("quality_label", "").strip() or "blank" for row in rows)
    reviewed_rows = len(rows) - label_counts["blank"]
    replacement_rows = sum(1 for row in rows if row.get("reviewed_banglish", "").strip())

    lines = [
        "# Validation-200 v5 Review Validation",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Review queue: `{repo_path(review_path)}`",
        f"- Source slice: `{repo_path(source_path)}`",
        f"- Issue CSV: `{repo_path(issues_path)}`",
        f"- Require complete: `{require_complete}`",
        "",
        "## Progress",
        "",
        f"- Rows: {len(rows)}",
        f"- Reviewed rows: {reviewed_rows}",
        f"- Pending rows: {label_counts['blank']}",
        f"- Rows with replacement text: {replacement_rows}",
        "",
        "| Quality label | Rows |",
        "| --- | ---: |",
    ]
    for label, count in label_counts.most_common():
        lines.append(f"| `{label}` | {count} |")

    lines.extend(["", "## Issue Counts", "", "| Severity | Issues |", "| --- | ---: |"])
    for severity in ["error", "warning", "pending"]:
        lines.append(f"| `{severity}` | {severity_counts[severity]} |")

    lines.extend(["", "| Code | Issues |", "| --- | ---: |"])
    for code, count in code_counts.most_common():
        lines.append(f"| `{code}` | {count} |")

    errors = [issue for issue in issues if issue["severity"] == "error"]
    warnings = [issue for issue in issues if issue["severity"] == "warning"]
    if errors or warnings:
        lines.extend(["", "## First Blocking/Warning Issues", ""])
        for issue in (errors + warnings)[:25]:
            lines.append(
                f"- `{issue['severity']}` `{issue['code']}` `{issue['id']}`: {issue['message']}"
            )

    lines.extend(
        [
            "",
            "## Freeze Rule",
            "",
            "Run the freeze only after this validator has zero `error` rows and",
            "zero `pending` rows under `--require-complete`. Warnings should be",
            "read before freezing; line-count warnings can be acceptable when the",
            "answer-format line and semantic content are preserved.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--issues-output", type=Path, default=DEFAULT_ISSUES)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Treat pending blank review rows as a validation failure.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = load_jsonl(args.source)
    source_by_id = {str(row.get("id", "")): row for row in source_rows}
    fieldnames, rows = load_csv(args.review)

    issues = validate_columns(fieldnames)
    seen_ids: set[str] = set()
    for row in rows:
        validate_row(row, source_by_id, seen_ids, issues)

    source_ids = set(source_by_id)
    review_ids = {row.get("id", "").strip() for row in rows}
    for missing_id in sorted(review_ids - source_ids):
        if missing_id:
            issues.append(
                {
                    "severity": "error",
                    "code": "source_id_missing",
                    "id": missing_id,
                    "dataset": "",
                    "quality_label": "",
                    "message": "Review id does not exist in the source JSONL slice.",
                }
            )

    write_csv(args.issues_output, issues)
    write_report(
        args.report_output,
        args.review,
        args.source,
        rows,
        issues,
        args.issues_output,
        args.require_complete,
    )

    counts = Counter(issue["severity"] for issue in issues)
    print(
        " | ".join(
            [
                f"rows={len(rows)}",
                f"errors={counts['error']}",
                f"warnings={counts['warning']}",
                f"pending={counts['pending']}",
                f"issues={args.issues_output}",
                f"report={args.report_output}",
            ]
        )
    )
    if counts["error"] or (args.require_complete and counts["pending"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
