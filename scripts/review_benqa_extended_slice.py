#!/usr/bin/env python3
"""AI-assisted quality triage for the BEnQA extended slice.

This is not a human-review tool. It performs deterministic row-by-row checks
and writes transparent AI-assisted review metadata so the extension can be used
honestly as a silver/triaged layer.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/benqa_extended_1000_v1.jsonl"
DEFAULT_OUTPUT = ROOT / "data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl"
DEFAULT_PASS_OUTPUT = ROOT / "data/slices/benqa_extended_1000_v1_ai_pass.jsonl"
DEFAULT_QUEUE = ROOT / "results/analysis/benqa_extended_1000_v1_ai_review_queue.csv"
DEFAULT_REPORT = ROOT / "reports/benqa_extended_1000_v1_ai_review.md"

BN_CHAR_RE = re.compile(r"[\u0980-\u09ff]")
ASCII_DIGIT_RE = re.compile(r"\d+")
OPTION_RE = re.compile(r"^([ABCD])\.\s*(.*)$")
ANSWER_LINE = "Answer with only A, B, C, or D."
REVIEW_VERSION = "ai_assisted_review_v1"

BENGALI_DIGITS = str.maketrans(
    {
        "০": "0",
        "১": "1",
        "২": "2",
        "৩": "3",
        "৪": "4",
        "৫": "5",
        "৬": "6",
        "৭": "7",
        "৮": "8",
        "৯": "9",
    }
)

# These are high-risk romanizer leftovers, not proof of error by themselves.
SUSPICIOUS_PATTERNS = [
    r"\btb[a-z]+",
    r"\bdb[a-z]+",
    r"\boja[a-z]+",
    r"\bkhady[a-z]+",
    r"\bdurotb[a-z]*",
    r"\bgurutb[a-z]*",
    r"\bdharokotb[a-z]*",
    r"\bboijnanik\b",
    r"\s{2,}",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def option_lines(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in text.splitlines():
        match = OPTION_RE.match(line.strip())
        if match:
            found[match.group(1)] = match.group(2).strip()
    return found


def normalized_digits(text: str) -> list[str]:
    return ASCII_DIGIT_RE.findall(text.translate(BENGALI_DIGITS))


def formulaish_tokens(text: str) -> set[str]:
    tokens = set()
    for token in re.findall(r"[A-Za-z0-9\\/%°+\-=<>.]+", text.translate(BENGALI_DIGITS)):
        if any(ch.isdigit() for ch in token) or "\\" in token or "%" in token or "°" in token:
            tokens.add(token.lower().strip(".,;:()[]{}"))
    return {token for token in tokens if token}


def content_without_answer_line(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if line.strip() != ANSWER_LINE)


def review_row(row: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    if row.get("dataset") != "benqa":
        issues.append("not_benqa")
    if row.get("task_type") != "mcq":
        issues.append("not_mcq")
    if row.get("answer") not in {"A", "B", "C", "D"}:
        issues.append("invalid_answer")

    bangla = str(row.get("bangla") or "")
    banglish = str(row.get("banglish_clean") or "")
    english = str(row.get("english") or "")
    if not bangla or not banglish or not english:
        issues.append("missing_script_view")

    for view_name, text in (("bangla", bangla), ("banglish", banglish), ("english", english)):
        options = option_lines(text)
        missing = sorted(set("ABCD") - set(options))
        extra = sorted(set(options) - set("ABCD"))
        if missing:
            issues.append(f"{view_name}_missing_options:{''.join(missing)}")
        if extra:
            issues.append(f"{view_name}_extra_options:{''.join(extra)}")
        if text.count(ANSWER_LINE) != 1:
            issues.append(f"{view_name}_answer_instruction_count:{text.count(ANSWER_LINE)}")
        if len(set(options.values())) < len(options):
            warnings.append(f"{view_name}_duplicate_option_text")

    bn_leak_count = len(BN_CHAR_RE.findall(banglish))
    if bn_leak_count:
        issues.append(f"banglish_bengali_char_leak:{bn_leak_count}")

    bangla_digits = normalized_digits(bangla)
    banglish_digits = normalized_digits(banglish)
    english_digits = normalized_digits(english)
    if bangla_digits != banglish_digits:
        issues.append("bangla_banglish_digit_mismatch")
    if bangla_digits and english_digits and bangla_digits != english_digits:
        warnings.append("bangla_english_digit_mismatch")

    bangla_formulaish = formulaish_tokens(bangla)
    banglish_formulaish = formulaish_tokens(banglish)
    if bangla_formulaish != banglish_formulaish:
        warnings.append("bangla_banglish_formulaish_token_mismatch")

    bangla_content_len = max(1, len(content_without_answer_line(bangla)))
    banglish_content_len = len(content_without_answer_line(banglish))
    length_ratio = banglish_content_len / bangla_content_len
    if length_ratio < 0.45 or length_ratio > 1.75:
        warnings.append(f"banglish_length_ratio_outlier:{length_ratio:.2f}")

    lower_banglish = banglish.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, lower_banglish):
            warnings.append(f"suspicious_romanization_pattern:{pattern}")

    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    choices_bangla = metadata.get("choices_bangla") if isinstance(metadata.get("choices_bangla"), dict) else {}
    choices_english = metadata.get("choices_english") if isinstance(metadata.get("choices_english"), dict) else {}
    if set(choices_bangla) != set("ABCD") or set(choices_english) != set("ABCD"):
        issues.append("metadata_choice_key_mismatch")

    status = "ai_assisted_review_pass_v1"
    if issues:
        status = "ai_assisted_review_fail_v1"
    elif warnings:
        status = "ai_assisted_review_warn_v1"

    return {
        "review_status": status,
        "issues": issues,
        "warnings": warnings,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "banglish_bengali_char_count": bn_leak_count,
        "banglish_length_ratio": round(length_ratio, 3),
        "bangla_digits": "|".join(bangla_digits),
        "banglish_digits": "|".join(banglish_digits),
        "english_digits": "|".join(english_digits),
    }


def apply_review(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    reviewed: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    reviewed_at = datetime.now(timezone.utc).isoformat()
    for index, row in enumerate(rows, start=1):
        review = review_row(row)
        item = dict(row)
        item["quality_status"] = review["review_status"]
        metadata = dict(item.get("metadata") or {})
        metadata["ai_assisted_review"] = {
            "version": REVIEW_VERSION,
            "reviewed_at_utc": reviewed_at,
            "disclosure": "Deterministic AI-assisted structural and romanization triage; not human review.",
            "issues": review["issues"],
            "warnings": review["warnings"],
            "banglish_length_ratio": review["banglish_length_ratio"],
        }
        item["metadata"] = metadata
        reviewed.append(item)

        counts[review["review_status"]] += 1
        counts["issues"] += review["issue_count"]
        counts["warnings"] += review["warning_count"]
        queue_rows.append(
            {
                "index": index,
                "id": item.get("id", ""),
                "source_file": item.get("source_file", ""),
                "source_row": item.get("source_row", ""),
                "grade": metadata.get("grade", ""),
                "subject": metadata.get("subject", ""),
                "answer": item.get("answer", ""),
                "review_status": review["review_status"],
                "issue_count": review["issue_count"],
                "warning_count": review["warning_count"],
                "issues": ";".join(review["issues"]),
                "warnings": ";".join(review["warnings"]),
                "banglish_bengali_char_count": review["banglish_bengali_char_count"],
                "banglish_length_ratio": review["banglish_length_ratio"],
                "bangla_digits": review["bangla_digits"],
                "banglish_digits": review["banglish_digits"],
                "english_digits": review["english_digits"],
            }
        )
    return reviewed, queue_rows, counts


def write_queue(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "index",
        "id",
        "source_file",
        "source_row",
        "grade",
        "subject",
        "answer",
        "review_status",
        "issue_count",
        "warning_count",
        "issues",
        "warnings",
        "banglish_bengali_char_count",
        "banglish_length_ratio",
        "bangla_digits",
        "banglish_digits",
        "english_digits",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    input_path: Path,
    output_path: Path,
    pass_output_path: Path,
    queue_path: Path,
    queue_rows: list[dict[str, Any]],
    counts: Counter[str],
) -> None:
    by_subject = Counter(str(row["subject"]) for row in queue_rows)
    by_warning: Counter[str] = Counter()
    for row in queue_rows:
        for warning in str(row["warnings"]).split(";"):
            if warning:
                by_warning[warning] += 1
    flagged = [row for row in queue_rows if row["review_status"] != "ai_assisted_review_pass_v1"]
    warning_examples = flagged[:20]
    lines = [
        "# BEnQA Extended 1000 V1 AI-Assisted Review",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Scope",
        "",
        "This is deterministic AI-assisted review/triage, not human review. It",
        "checks every row for MCQ structure, answer instruction integrity, digit",
        "parity, formula-like token parity, Bengali-character leakage in Banglish,",
        "and high-risk romanization artifacts.",
        "",
        "## Files",
        "",
        f"- Input slice: `{repo_path(input_path)}`",
        f"- Reviewed slice: `{repo_path(output_path)}`",
        f"- Pass-only slice: `{repo_path(pass_output_path)}`",
        f"- Review queue CSV: `{repo_path(queue_path)}`",
        "",
        "## Summary",
        "",
        f"- Rows reviewed: {len(queue_rows)}.",
        f"- Pass rows: {counts['ai_assisted_review_pass_v1']}.",
        f"- Warning rows: {counts['ai_assisted_review_warn_v1']}.",
        f"- Fail rows: {counts['ai_assisted_review_fail_v1']}.",
        f"- Total structural issues: {counts['issues']}.",
        f"- Total warnings: {counts['warnings']}.",
        f"- Conservative pass-only evaluation rows: {counts['ai_assisted_review_pass_v1']}.",
        "",
        "## Subject Coverage",
        "",
        "| Subject | Rows |",
        "| --- | ---: |",
    ]
    for subject, count in sorted(by_subject.items()):
        lines.append(f"| {subject} | {count} |")

    lines.extend(
        [
            "",
            "## Warning Taxonomy",
            "",
            "| Warning | Rows |",
            "| --- | ---: |",
        ]
    )
    if by_warning:
        for warning, count in sorted(by_warning.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| `{warning}` | {count} |")
    else:
        lines.append("| - | 0 |")

    lines.extend(
        [
            "",
            "## First Flagged Rows",
            "",
            "| ID | Status | Issues | Warnings |",
            "| --- | --- | --- | --- |",
        ]
    )
    if warning_examples:
        for row in warning_examples:
            lines.append(
                f"| `{row['id']}` | {row['review_status']} | {row['issues'] or '-'} | "
                f"{row['warnings'] or '-'} |"
            )
    else:
        lines.append("| - | - | - | - |")

    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "Use this as a silver, AI-triaged extension layer. The frozen",
            "`validation_200_v5` slice remains the human-reviewed gold core. If this",
            "extension is used in thesis or publication claims, state that Banglish",
            "was generated by the rule-based romanizer and then AI-assisted",
            "structurally reviewed, not human-reviewed.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--pass-output", type=Path, default=DEFAULT_PASS_OUTPUT)
    parser.add_argument("--queue-output", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--fail-on-structural-issue", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    reviewed, queue_rows, counts = apply_review(rows)
    write_jsonl(args.output, reviewed)
    write_jsonl(
        args.pass_output,
        [row for row in reviewed if row.get("quality_status") == "ai_assisted_review_pass_v1"],
    )
    write_queue(args.queue_output, queue_rows)
    write_report(
        args.report,
        args.input,
        args.output,
        args.pass_output,
        args.queue_output,
        queue_rows,
        counts,
    )
    print(f"reviewed={len(reviewed)}")
    print(f"pass={counts['ai_assisted_review_pass_v1']}")
    print(f"warn={counts['ai_assisted_review_warn_v1']}")
    print(f"fail={counts['ai_assisted_review_fail_v1']}")
    print(f"output={repo_path(args.output)}")
    print(f"pass_output={repo_path(args.pass_output)}")
    print(f"report={repo_path(args.report)}")
    if args.fail_on_structural_issue and counts["ai_assisted_review_fail_v1"]:
        raise SystemExit("AI-assisted review found structural failures")


if __name__ == "__main__":
    main()
