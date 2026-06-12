#!/usr/bin/env python3
"""Validate the provider-neutral API audit smoke manifest without paid calls."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/api_audit_smoke_10_v5.jsonl"
DEFAULT_REQUESTS = ROOT / "data/api_audit/api_audit_smoke_10_v5_requests.jsonl"
DEFAULT_BUDGET = ROOT / "results/analysis/api_audit_smoke_10_v5_prompt_budget_summary.csv"
DEFAULT_OUTPUT_CSV = ROOT / "results/analysis/api_audit_manifest_integrity_check.csv"
DEFAULT_REPORT = ROOT / "reports/api_audit_manifest_integrity_check.md"
EXPECTED_VARIANTS = ("bangla", "banglish_clean", "english")
REQUIRED_REQUEST_FIELDS = {
    "request_id",
    "id",
    "dataset",
    "task_type",
    "answer_type",
    "variant",
    "prompt_mode",
    "system_message",
    "prompt",
    "max_output_tokens",
    "prompt_chars",
    "approx_prompt_tokens",
}
FORBIDDEN_REQUEST_FIELDS = {"answer", "gold", "choices", "metadata", "source_file", "source_url"}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def add(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def validate_paths(rows: list[dict[str, str]], paths: list[Path]) -> bool:
    ok = True
    for path in paths:
        exists = path.exists()
        add(rows, f"exists:{repo_path(path)}", "ok" if exists else "error", "present" if exists else "missing")
        ok = ok and exists
    return ok


def validate_requests(
    items: list[dict[str, Any]],
    requests: list[dict[str, Any]],
    rows: list[dict[str, str]],
    expected_items: int | None,
    max_output_tokens_cap: int,
) -> None:
    item_ids = {str(row["id"]) for row in items}
    request_ids = [str(row.get("request_id", "")) for row in requests]
    request_id_counts = Counter(request_ids)
    duplicate_ids = sorted(request_id for request_id, count in request_id_counts.items() if count > 1)
    variants_by_item: dict[str, set[str]] = defaultdict(set)
    prompt_token_sum = 0
    prompt_char_sum = 0
    field_issues: list[str] = []
    forbidden_field_issues: list[str] = []
    malformed_request_ids: list[str] = []
    prompt_issues: list[str] = []
    max_output_issues: list[str] = []
    unknown_item_ids: list[str] = []
    for row in requests:
        request_id = str(row.get("request_id", ""))
        item_id = str(row.get("id", ""))
        variant = str(row.get("variant", ""))
        prompt_mode = str(row.get("prompt_mode", ""))
        variants_by_item[item_id].add(variant)
        missing = sorted(REQUIRED_REQUEST_FIELDS - set(row))
        if missing:
            field_issues.append(f"{request_id}:missing={','.join(missing)}")
        forbidden = sorted(FORBIDDEN_REQUEST_FIELDS & set(row))
        if forbidden:
            forbidden_field_issues.append(f"{request_id}:forbidden={','.join(forbidden)}")
        expected_request_id = f"{item_id}::{variant}::{prompt_mode}"
        if request_id != expected_request_id:
            malformed_request_ids.append(f"{request_id}!={expected_request_id}")
        if item_id not in item_ids:
            unknown_item_ids.append(item_id)
        prompt = str(row.get("prompt", ""))
        if "Answer the following evaluation item." not in prompt:
            prompt_issues.append(f"{request_id}:missing_eval_prefix")
        if "Answer with only A, B, C, or D." not in prompt and "Return only the final answer." not in prompt:
            prompt_issues.append(f"{request_id}:missing_answer_instruction")
        max_output_tokens = int(row.get("max_output_tokens", 0))
        if max_output_tokens <= 0 or max_output_tokens > max_output_tokens_cap:
            max_output_issues.append(f"{request_id}:{max_output_tokens}")
        prompt_token_sum += int(row.get("approx_prompt_tokens", 0))
        prompt_char_sum += int(row.get("prompt_chars", 0))
    variant_counts = Counter(str(row.get("variant", "")) for row in requests)
    missing_variant_items = sorted(
        item_id
        for item_id in item_ids
        if variants_by_item.get(item_id, set()) != set(EXPECTED_VARIANTS)
    )
    expected_request_count = len(items) * len(EXPECTED_VARIANTS)
    expected_item_count = expected_items if expected_items is not None else len(items)
    add(
        rows,
        "item_count",
        "ok" if len(items) == expected_item_count else "error",
        f"items={len(items)} expected={expected_item_count}",
    )
    add(
        rows,
        "request_count",
        "ok" if len(requests) == expected_request_count else "error",
        f"requests={len(requests)} expected={expected_request_count}",
    )
    add(
        rows,
        "request_id_unique",
        "ok" if not duplicate_ids else "error",
        "duplicates=0" if not duplicate_ids else ";".join(duplicate_ids[:10]),
    )
    add(
        rows,
        "request_id_format",
        "ok" if not malformed_request_ids else "error",
        "all id::variant::prompt_mode" if not malformed_request_ids else ";".join(malformed_request_ids[:10]),
    )
    add(
        rows,
        "request_item_ids",
        "ok" if not unknown_item_ids else "error",
        "all in input slice" if not unknown_item_ids else ",".join(sorted(set(unknown_item_ids))[:10]),
    )
    add(
        rows,
        "variants_per_item",
        "ok" if not missing_variant_items else "error",
        "all items have bangla,banglish_clean,english"
        if not missing_variant_items
        else ",".join(missing_variant_items[:10]),
    )
    add(
        rows,
        "variant_counts",
        "ok" if all(variant_counts[v] == len(items) for v in EXPECTED_VARIANTS) else "error",
        ",".join(f"{variant}={variant_counts[variant]}" for variant in EXPECTED_VARIANTS),
    )
    add(
        rows,
        "required_fields",
        "ok" if not field_issues else "error",
        "all present" if not field_issues else ";".join(field_issues[:10]),
    )
    add(
        rows,
        "gold_excluded",
        "ok" if not forbidden_field_issues else "error",
        "no answer/gold/source fields in request rows"
        if not forbidden_field_issues
        else ";".join(forbidden_field_issues[:10]),
    )
    add(
        rows,
        "prompt_contract",
        "ok" if not prompt_issues else "error",
        "all prompts include evaluation prefix and answer instruction"
        if not prompt_issues
        else ";".join(prompt_issues[:10]),
    )
    add(
        rows,
        "max_output_tokens",
        "ok" if not max_output_issues else "error",
        f"0 < max_output_tokens <= {max_output_tokens_cap}"
        if not max_output_issues
        else ";".join(max_output_issues[:10]),
    )
    add(rows, "prompt_chars_total", "ok", f"chars={prompt_char_sum}")
    add(rows, "approx_prompt_tokens_total", "ok", f"approx_tokens={prompt_token_sum}")


def validate_budget(
    requests: list[dict[str, Any]], budget_rows: list[dict[str, str]], rows: list[dict[str, str]]
) -> None:
    overall = next((row for row in budget_rows if row.get("group") == "overall"), None)
    if not overall:
        add(rows, "budget_overall_row", "error", "missing group=overall")
        return
    request_count = len(requests)
    token_sum = sum(int(row.get("approx_prompt_tokens", 0)) for row in requests)
    csv_calls = int(float(overall.get("calls", "0")))
    csv_tokens = int(float(overall.get("total_approx_tokens", "0")))
    add(
        rows,
        "budget_call_count",
        "ok" if csv_calls == request_count else "error",
        f"budget_calls={csv_calls} requests={request_count}",
    )
    add(
        rows,
        "budget_token_sum",
        "ok" if csv_tokens == token_sum else "error",
        f"budget_tokens={csv_tokens} request_tokens={token_sum}",
    )


def write_report(path: Path, checks: list[dict[str, str]], csv_path: Path) -> None:
    issues = [row for row in checks if row["status"] != "ok"]
    lines = [
        "# API Audit Manifest Integrity Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This no-spend check validates the provider-neutral API smoke request",
        "manifest before any paid call is made.",
        "",
        f"Machine-readable checks: `{repo_path(csv_path)}`.",
        "",
        "## Summary",
        "",
        f"- Checks: {len(checks)}",
        f"- Issues: {len(issues)}",
        "",
    ]
    if issues:
        lines.extend(["## Issues", ""])
        for row in issues:
            lines.append(f"- `{row['check']}`: {row['detail']}")
        lines.append("")
    else:
        lines.extend(["No API audit manifest integrity issues found.", ""])
    lines.extend(["## Checks", "", "| Check | Status | Detail |", "| --- | --- | --- |"])
    for row in checks:
        lines.append(f"| `{row['check']}` | `{row['status']}` | {row['detail']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--requests", type=Path, default=DEFAULT_REQUESTS)
    parser.add_argument("--budget-summary", type=Path, default=DEFAULT_BUDGET)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--expected-items", type=int)
    parser.add_argument("--max-output-tokens-cap", type=int, default=128)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checks: list[dict[str, str]] = []
    if not validate_paths(checks, [args.input, args.requests, args.budget_summary]):
        write_csv(args.output_csv, checks)
        write_report(args.report_output, checks, args.output_csv)
        sys.exit(1)
    items = load_jsonl(args.input)
    requests = load_jsonl(args.requests)
    validate_requests(
        items,
        requests,
        checks,
        args.expected_items,
        args.max_output_tokens_cap,
    )
    validate_budget(requests, read_csv(args.budget_summary), checks)
    write_csv(args.output_csv, checks)
    write_report(args.report_output, checks, args.output_csv)
    issues = [row for row in checks if row["status"] != "ok"]
    print(f"checks={len(checks)} issues={len(issues)} report={args.report_output}")
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
