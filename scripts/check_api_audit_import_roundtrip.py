#!/usr/bin/env python3
"""No-spend round-trip check for the API audit response importer."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from import_api_audit_responses import load_jsonl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/api_audit_smoke_10_v5.jsonl"
DEFAULT_REQUESTS = ROOT / "data/api_audit/api_audit_smoke_10_v5_requests.jsonl"
DEFAULT_OUTPUT_CSV = ROOT / "results/analysis/api_audit_import_roundtrip_check.csv"
DEFAULT_REPORT = ROOT / "reports/api_audit_import_roundtrip_check.md"
EXPECTED_VARIANTS = ("bangla", "banglish_clean", "english")
MOCK_PROVIDER = "roundtrip-mock"
MOCK_MODEL = "gold-answer-fixture-v1"
REQUIRED_IMPORTED_FIELDS = {
    "request_id",
    "provider",
    "provider_response_id",
    "model",
    "id",
    "dataset",
    "task_type",
    "answer_type",
    "variant",
    "prompt_mode",
    "raw_output",
    "parsed",
    "gold",
    "correct",
    "rewrite_output",
    "seconds",
    "usage_input_tokens",
    "usage_output_tokens",
}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def add(rows: list[dict[str, str]], check: str, status: str, detail: str) -> None:
    rows.append({"check": check, "status": status, "detail": detail})


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def make_mock_responses(
    requests: list[dict[str, Any]], items_by_id: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], int, int]:
    responses: list[dict[str, Any]] = []
    input_usage = 0
    output_usage = 0
    for index, request in enumerate(requests, start=1):
        item = items_by_id[str(request["id"])]
        answer = str(item["answer"])
        usage_input = int(request.get("approx_prompt_tokens", 0)) + 1
        usage_output = max(1, len(answer.split()) + 2)
        input_usage += usage_input
        output_usage += usage_output
        responses.append(
            {
                "request_id": request["request_id"],
                "provider_response_id": f"mock-response-{index:03d}",
                "raw_output": f"Final answer: {answer}",
                "seconds": "0.001",
                "usage_input_tokens": usage_input,
                "usage_output_tokens": usage_output,
            }
        )
    return responses, input_usage, output_usage


def run_importer(
    requests_path: Path,
    responses_path: Path,
    source_items_path: Path,
    output_path: Path,
    report_path: Path,
) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "scripts/import_api_audit_responses.py",
        "--requests",
        str(requests_path),
        "--responses",
        str(responses_path),
        "--source-items",
        str(source_items_path),
        "--provider",
        MOCK_PROVIDER,
        "--model",
        MOCK_MODEL,
        "--output",
        str(output_path),
        "--report",
        str(report_path),
        "--require-complete",
    ]
    return subprocess.run(
        cmd,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def validate_roundtrip(
    requests: list[dict[str, Any]],
    items_by_id: dict[str, dict[str, Any]],
    imported_rows: list[dict[str, Any]],
    expected_input_usage: int,
    expected_output_usage: int,
    importer_report: Path,
    checks: list[dict[str, str]],
) -> None:
    request_ids = [str(row["request_id"]) for row in requests]
    imported_ids = [str(row.get("request_id", "")) for row in imported_rows]
    imported_by_id = {str(row.get("request_id", "")): row for row in imported_rows}
    missing_imports = sorted(set(request_ids) - set(imported_ids))
    extra_imports = sorted(set(imported_ids) - set(request_ids))
    duplicate_import_ids = sorted(
        request_id for request_id, count in Counter(imported_ids).items() if count > 1
    )
    missing_fields = [
        f"{row.get('request_id', '<missing>')}:missing={','.join(sorted(REQUIRED_IMPORTED_FIELDS - set(row)))}"
        for row in imported_rows
        if REQUIRED_IMPORTED_FIELDS - set(row)
    ]
    parsed_empty = [str(row.get("request_id", "")) for row in imported_rows if not str(row.get("parsed", "")).strip()]
    incorrect = [str(row.get("request_id", "")) for row in imported_rows if not bool(row.get("correct"))]
    provider_model_issues = [
        str(row.get("request_id", ""))
        for row in imported_rows
        if row.get("provider") != MOCK_PROVIDER or row.get("model") != MOCK_MODEL
    ]
    gold_issues = []
    for request_id, row in imported_by_id.items():
        item_id = str(row.get("id", ""))
        item = items_by_id.get(item_id)
        if item is None or str(row.get("gold", "")) != str(item.get("answer", "")):
            gold_issues.append(request_id)
    variant_counts = Counter(str(row.get("variant", "")) for row in imported_rows)
    input_usage = sum(int(row.get("usage_input_tokens") or 0) for row in imported_rows)
    output_usage = sum(int(row.get("usage_output_tokens") or 0) for row in imported_rows)

    add(checks, "request_count", "ok" if len(requests) == 30 else "error", f"requests={len(requests)} expected=30")
    add(
        checks,
        "imported_count",
        "ok" if len(imported_rows) == len(requests) else "error",
        f"imported={len(imported_rows)} expected={len(requests)}",
    )
    add(
        checks,
        "imported_request_ids_unique",
        "ok" if not duplicate_import_ids else "error",
        "duplicates=0" if not duplicate_import_ids else ",".join(duplicate_import_ids[:10]),
    )
    add(
        checks,
        "request_id_coverage",
        "ok" if not missing_imports and not extra_imports else "error",
        "complete"
        if not missing_imports and not extra_imports
        else f"missing={len(missing_imports)} extra={len(extra_imports)}",
    )
    add(
        checks,
        "required_imported_fields",
        "ok" if not missing_fields else "error",
        "all present" if not missing_fields else ";".join(missing_fields[:10]),
    )
    add(
        checks,
        "parsed_non_empty",
        "ok" if not parsed_empty else "error",
        "parsed_empty=0" if not parsed_empty else ",".join(parsed_empty[:10]),
    )
    add(
        checks,
        "gold_answer_correctness",
        "ok" if not incorrect else "error",
        f"correct={len(imported_rows) - len(incorrect)}/{len(imported_rows)}"
        if not incorrect
        else ",".join(incorrect[:10]),
    )
    add(
        checks,
        "gold_join",
        "ok" if not gold_issues else "error",
        "all imported gold values match source items" if not gold_issues else ",".join(gold_issues[:10]),
    )
    add(
        checks,
        "variant_counts",
        "ok" if all(variant_counts[variant] == 10 for variant in EXPECTED_VARIANTS) else "error",
        ",".join(f"{variant}={variant_counts[variant]}" for variant in EXPECTED_VARIANTS),
    )
    add(
        checks,
        "provider_model_fields",
        "ok" if not provider_model_issues else "error",
        "all rows carry mock provider/model" if not provider_model_issues else ",".join(provider_model_issues[:10]),
    )
    add(
        checks,
        "usage_input_tokens",
        "ok" if input_usage == expected_input_usage else "error",
        f"imported={input_usage} expected={expected_input_usage}",
    )
    add(
        checks,
        "usage_output_tokens",
        "ok" if output_usage == expected_output_usage else "error",
        f"imported={output_usage} expected={expected_output_usage}",
    )
    add(
        checks,
        "importer_report",
        "ok" if importer_report.exists() and importer_report.stat().st_size > 0 else "error",
        "temporary importer report written" if importer_report.exists() else "missing",
    )


def write_report(
    path: Path,
    checks: list[dict[str, str]],
    csv_path: Path,
    source_items: Path,
    requests_path: Path,
) -> None:
    issues = [row for row in checks if row["status"] != "ok"]
    lines = [
        "# API Audit Import Round-Trip Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This no-spend check synthesizes parser-friendly mock provider responses",
        "for the frozen-v5 API smoke requests, runs the normal response importer",
        "with `--require-complete`, and verifies that imported rows line up with",
        "the open-model result schema.",
        "",
        f"- Source items: `{repo_path(source_items)}`",
        f"- Request manifest: `{repo_path(requests_path)}`",
        f"- Machine-readable checks: `{repo_path(csv_path)}`",
        "",
        "Mock responses are written only inside a temporary directory; no fake paid",
        "provider output JSONL is persisted.",
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
        lines.extend(["No API audit import round-trip issues found.", ""])
    lines.extend(["## Checks", "", "| Check | Status | Detail |", "| --- | --- | --- |"])
    for row in checks:
        detail = row["detail"].replace("|", "\\|")
        lines.append(f"| `{row['check']}` | `{row['status']}` | {detail} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--requests", type=Path, default=DEFAULT_REQUESTS)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checks: list[dict[str, str]] = []
    for path in (args.input, args.requests):
        add(
            checks,
            f"exists:{repo_path(path)}",
            "ok" if path.exists() else "error",
            "present" if path.exists() else "missing",
        )
    if any(row["status"] != "ok" for row in checks):
        write_csv(args.output_csv, checks)
        write_report(args.report_output, checks, args.output_csv, args.input, args.requests)
        sys.exit(1)

    items = load_jsonl(args.input)
    requests = load_jsonl(args.requests)
    items_by_id = {str(row["id"]): row for row in items}
    mock_responses, expected_input_usage, expected_output_usage = make_mock_responses(
        requests, items_by_id
    )

    with tempfile.TemporaryDirectory(prefix="api-audit-roundtrip-") as tmpdir:
        tmp = Path(tmpdir)
        responses_path = tmp / "mock_responses.jsonl"
        imported_path = tmp / "imported.jsonl"
        importer_report = tmp / "import_report.md"
        write_jsonl(responses_path, mock_responses)
        completed = run_importer(
            args.requests,
            responses_path,
            args.input,
            imported_path,
            importer_report,
        )
        add(
            checks,
            "importer_cli",
            "ok" if completed.returncode == 0 else "error",
            "returncode=0"
            if completed.returncode == 0
            else f"returncode={completed.returncode} stderr={completed.stderr.strip()[:200]}",
        )
        imported_rows = read_jsonl(imported_path) if imported_path.exists() else []
        validate_roundtrip(
            requests,
            items_by_id,
            imported_rows,
            expected_input_usage,
            expected_output_usage,
            importer_report,
            checks,
        )

    write_csv(args.output_csv, checks)
    write_report(args.report_output, checks, args.output_csv, args.input, args.requests)
    issues = [row for row in checks if row["status"] != "ok"]
    print(f"checks={len(checks)} issues={len(issues)} report={args.report_output}")
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
