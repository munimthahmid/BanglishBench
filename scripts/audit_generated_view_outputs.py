#!/usr/bin/env python3
"""Audit generated alternate-script views before routing experiments."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS = (
    ROOT / "data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl"
)
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/generated_view_output_audit_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/generated_view_output_audit_summary.csv"
DEFAULT_REPORT = ROOT / "reports/generated_view_output_audit.md"

BN_RE = re.compile(r"[\u0980-\u09ff]")
LATIN_RE = re.compile(r"[A-Za-z]")
DIGIT_RE = re.compile(r"[0-9\u09e6-\u09ef]")
OPTION_RE = re.compile(r"^\s*([A-D])[\).]\s+", re.MULTILINE)
OPTION_PREFIX_SCRUB_RE = re.compile(r"^\s*[A-D][\).]\s+", re.MULTILINE)
SCIENTIFIC_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Z][a-z]?)+(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})*"
    r"(?![A-Za-z0-9_])"
)
ANNOTATED_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])[A-Za-z]+(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})+"
    r"(?![A-Za-z0-9_])"
)
LATEX_COMMAND_RE = re.compile(
    r"\\[A-Za-z]+(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})*"
)
FORMULAISH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9\\])"
    r"(?=[A-Za-z0-9\\_{}^+\-*/=().]*[\\_{}^+\-*/=()])"
    r"([A-Za-z0-9\\_{}^+\-*/=().]+)"
    r"(?![A-Za-z0-9])"
)
ISOLATED_UPPER_MATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:N|X)(?![A-Za-z0-9_])"
)
ROMAN_ENUM_RE = re.compile(r"(?<![A-Za-z])(?:i|ii|iii)(?![A-Za-z])")
MATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z])(?:cosx|sinx|ln|dx|ax|x|y|a|c|N|X|BC|RMS|gL|ms)(?![A-Za-z])"
)
ANSWER_MARKER_RE = re.compile(
    r"\bfinal\s+answer\s*:|\banswer\s*:|সঠিক\s+উত্তর|উত্তর\s*:",
    flags=re.IGNORECASE,
)
ANSWER_FORMAT_LINE_RE = re.compile(r"^Answer with only .*$", flags=re.MULTILINE)
LATIN_FRAGMENT_RE = re.compile(r"[A-Za-z]{2,}")
DIGIT_TRANS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
OUTPUT_FIELDS = [
    "generated_text",
    "generation_output",
    "rewritten_text",
    "translated_text",
    "output_text",
    "output",
    "text",
    "raw_output",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def output_text(row: dict[str, Any]) -> str:
    for field in OUTPUT_FIELDS:
        value = row.get(field)
        if value is not None:
            return str(value).strip()
    return ""


def key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("id", "")), str(row.get("target_view", ""))


def normalize_digits(text: str) -> list[str]:
    return [match.translate(DIGIT_TRANS) for match in DIGIT_RE.findall(text)]


def option_labels(text: str) -> list[str]:
    return OPTION_RE.findall(text)


def formulas(text: str) -> list[str]:
    scientific_tokens = [
        token
        for token in SCIENTIFIC_TOKEN_RE.findall(text)
        if len(token) >= 2 or "_" in token or "^" in token
    ]
    formulaish_tokens = [
        token
        for token in FORMULAISH_TOKEN_RE.findall(text)
        if any(ch.isalnum() or ch == "\\" for ch in token)
    ]
    return sorted(
        set(
            scientific_tokens
            + ANNOTATED_TOKEN_RE.findall(text)
            + LATEX_COMMAND_RE.findall(text)
            + ISOLATED_UPPER_MATH_TOKEN_RE.findall(text)
            + formulaish_tokens
        )
    )


def answer_marker_count(text: str) -> int:
    return len(ANSWER_MARKER_RE.findall(text))


def unexpected_generated_bn_latin_fragments(source: str, generated: str) -> list[str]:
    scrubbed = ANSWER_FORMAT_LINE_RE.sub("", generated)
    scrubbed = OPTION_PREFIX_SCRUB_RE.sub("", scrubbed)
    preserved_tokens = (
        formulas(source)
        + ROMAN_ENUM_RE.findall(source)
        + MATH_TOKEN_RE.findall(source)
    )
    for token in preserved_tokens:
        scrubbed = scrubbed.replace(token, "")
    allowed_fragments = {
        fragment
        for token in preserved_tokens
        for fragment in LATIN_FRAGMENT_RE.findall(token)
    }
    return sorted(
        {
            fragment
            for fragment in LATIN_FRAGMENT_RE.findall(scrubbed)
            if fragment not in allowed_fragments
        }
    )


def ratio(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def audit_row(prompt: dict[str, Any], generated: str, output_count: int) -> dict[str, Any]:
    source = str(prompt.get("source_text", ""))
    target_view = str(prompt.get("target_view", ""))
    source_options = option_labels(source)
    generated_options = option_labels(generated)
    source_digits = normalize_digits(source)
    generated_digits = normalize_digits(generated)
    source_formulas = formulas(source)
    generated_formulas = formulas(generated)
    source_line_count = len(source.splitlines())
    generated_line_count = len(generated.splitlines())
    generated_chars = len(generated)
    bn_chars = len(BN_RE.findall(generated))
    latin_chars = len(LATIN_RE.findall(generated))

    empty_output = not generated.strip()
    duplicate_output = output_count > 1
    options_preserved = source_options == generated_options
    digit_sequence_preserved = source_digits == generated_digits
    formulas_preserved = source_formulas == generated_formulas
    line_count_preserved = source_line_count == generated_line_count
    extra_answer_marker = answer_marker_count(generated) > answer_marker_count(source)
    unexpected_latin_fragments: list[str] = []
    if target_view == "generated_bn":
        unexpected_latin_fragments = unexpected_generated_bn_latin_fragments(
            source, generated
        )
    target_script_ok = True
    target_script_issue = ""
    if target_view == "generated_bn" and not empty_output and not BN_RE.search(generated):
        target_script_ok = False
        target_script_issue = "generated_bn_has_no_bengali_script"
    if target_view == "generated_en" and BN_RE.search(generated):
        target_script_ok = False
        target_script_issue = "generated_en_contains_bengali_script"

    hard_fail = (
        empty_output
        or duplicate_output
        or not options_preserved
        or not digit_sequence_preserved
        or not formulas_preserved
        or extra_answer_marker
        or not target_script_ok
    )
    warning = not line_count_preserved or bool(unexpected_latin_fragments)

    return {
        "id": prompt.get("id", ""),
        "dataset": prompt.get("dataset", ""),
        "answer_type": prompt.get("answer_type", ""),
        "target_view": target_view,
        "output_count": output_count,
        "empty_output": empty_output,
        "duplicate_output": duplicate_output,
        "source_option_labels": " ".join(source_options),
        "generated_option_labels": " ".join(generated_options),
        "options_preserved": options_preserved,
        "source_digit_sequence": " ".join(source_digits),
        "generated_digit_sequence": " ".join(generated_digits),
        "digit_sequence_preserved": digit_sequence_preserved,
        "source_formulas": " ".join(source_formulas),
        "generated_formulas": " ".join(generated_formulas),
        "formulas_preserved": formulas_preserved,
        "source_line_count": source_line_count,
        "generated_line_count": generated_line_count,
        "line_count_preserved": line_count_preserved,
        "extra_answer_marker": extra_answer_marker,
        "target_script_ok": target_script_ok,
        "target_script_issue": target_script_issue,
        "unexpected_latin_fragment_count": len(unexpected_latin_fragments),
        "unexpected_latin_fragments": " ".join(unexpected_latin_fragments),
        "bengali_ratio": ratio(bn_chars, generated_chars),
        "latin_ratio": ratio(latin_chars, generated_chars),
        "hard_fail": hard_fail,
        "warning": warning,
        "generated_preview": generated[:220].replace("\n", " "),
    }


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(str(row["dataset"]), str(row["target_view"]))].append(row)

    out: list[dict[str, Any]] = []
    for (dataset, target_view), items in sorted(groups.items()):
        n = len(items)
        out.append(
            {
                "dataset": dataset,
                "target_view": target_view,
                "n": n,
                "hard_fail": sum(int(row["hard_fail"]) for row in items),
                "warning": sum(int(row["warning"]) for row in items),
                "empty_output": sum(int(row["empty_output"]) for row in items),
                "duplicate_output": sum(int(row["duplicate_output"]) for row in items),
                "options_not_preserved": sum(
                    int(not row["options_preserved"]) for row in items
                ),
                "digit_sequence_not_preserved": sum(
                    int(not row["digit_sequence_preserved"]) for row in items
                ),
                "formulas_not_preserved": sum(
                    int(not row["formulas_preserved"]) for row in items
                ),
                "line_count_not_preserved": sum(
                    int(not row["line_count_preserved"]) for row in items
                ),
                "extra_answer_marker": sum(
                    int(row["extra_answer_marker"]) for row in items
                ),
                "target_script_issue": sum(
                    int(not row["target_script_ok"]) for row in items
                ),
                "unexpected_latin_fragment": sum(
                    int(bool(row["unexpected_latin_fragment_count"])) for row in items
                ),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
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
    prompts_path: Path,
    outputs_path: Path,
    items_path: Path,
    summary_path: Path,
    audited: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    missing_count: int,
    extra_count: int,
) -> None:
    hard_fails = [row for row in audited if row["hard_fail"]]
    warnings = [row for row in audited if row["warning"]]
    lines = [
        "# Generated-View Output Audit",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Prompt set: `{repo_path(prompts_path)}`",
        f"- Generator outputs: `{repo_path(outputs_path)}`",
        f"- Item audit CSV: `{repo_path(items_path)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        "",
        "## Counts",
        "",
        f"- Expected prompt rows: {len(audited)}",
        f"- Missing outputs: {missing_count}",
        f"- Extra output keys: {extra_count}",
        f"- Hard-fail rows: {len(hard_fails)}",
        f"- Warning rows: {len(warnings)}",
        "",
        "| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            "| {dataset} | {target_view} | {n} | {hard_fail} | {warning} | "
            "{options_not_preserved} | {digit_sequence_not_preserved} | "
            "{formulas_not_preserved} | {extra_answer_marker} | "
            "{target_script_issue} | {unexpected_latin_fragment} |".format(**row)
        )

    if hard_fails:
        lines.extend(["", "## First Hard Fails", ""])
        for row in hard_fails[:25]:
            fail_codes = []
            if row["empty_output"]:
                fail_codes.append("empty")
            if row["duplicate_output"]:
                fail_codes.append("duplicate")
            if not row["options_preserved"]:
                fail_codes.append("options")
            if not row["digit_sequence_preserved"]:
                fail_codes.append("digits")
            if not row["formulas_preserved"]:
                fail_codes.append("formulas")
            if row["extra_answer_marker"]:
                fail_codes.append("answer_marker")
            if not row["target_script_ok"]:
                fail_codes.append(str(row["target_script_issue"]))
            lines.append(
                f"- `{row['id']}` `{row['target_view']}` "
                f"failures={','.join(fail_codes)} preview={row['generated_preview']}"
            )

    latin_warnings = [
        row for row in audited if row["unexpected_latin_fragment_count"]
    ]
    if latin_warnings:
        lines.extend(["", "## First Generated-BN Latin-Fragment Warnings", ""])
        for row in latin_warnings[:25]:
            lines.append(
                f"- `{row['id']}` fragments={row['unexpected_latin_fragments']} "
                f"preview={row['generated_preview']}"
            )

    lines.extend(
        [
            "",
            "## Routing Rule",
            "",
            "Generated views with `hard_fail=True` must be excluded from",
            "agreement routing. Line-count warnings require inspection but are",
            "not automatically blocking if options, digits, formulas, target",
            "script, and answer-marker checks pass. Generated-BN Latin-fragment",
            "warnings also require inspection because formal preservation does",
            "not prove lexical quality.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--outputs", type=Path, required=True)
    parser.add_argument(
        "--target-views",
        nargs="+",
        help="Optional target_view subset to audit, e.g. generated_bn.",
    )
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--fail-on-hard-fail",
        action="store_true",
        help="Exit nonzero if any generated view fails a hard preservation gate.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prompts = load_jsonl(args.prompts)
    if args.target_views:
        target_views = set(args.target_views)
        prompts = [row for row in prompts if str(row.get("target_view", "")) in target_views]
        if not prompts:
            raise SystemExit(f"No prompt rows matched --target-views {args.target_views}")
    outputs = load_jsonl(args.outputs)

    output_lookup: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in outputs:
        output_lookup[key(row)].append(output_text(row))

    prompt_keys = {key(row) for row in prompts}
    output_keys = set(output_lookup)
    missing_keys = prompt_keys - output_keys
    extra_keys = output_keys - prompt_keys

    audited = []
    for prompt in prompts:
        texts = output_lookup.get(key(prompt), [])
        generated = texts[0] if texts else ""
        audited.append(audit_row(prompt, generated, len(texts)))

    summary = summarize(audited)
    write_csv(args.items_output, audited)
    write_csv(args.summary_output, summary)
    write_report(
        args.report_output,
        args.prompts,
        args.outputs,
        args.items_output,
        args.summary_output,
        audited,
        summary,
        len(missing_keys),
        len(extra_keys),
    )

    hard_fail_count = sum(int(row["hard_fail"]) for row in audited)
    print(
        " | ".join(
            [
                f"rows={len(audited)}",
                f"hard_fail={hard_fail_count}",
                f"missing={len(missing_keys)}",
                f"extra={len(extra_keys)}",
                f"items={args.items_output}",
                f"summary={args.summary_output}",
                f"report={args.report_output}",
            ]
        )
    )
    if args.fail_on_hard_fail and hard_fail_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
