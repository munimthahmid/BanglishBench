#!/usr/bin/env python3
"""Import paid API responses into the open-model result schema."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, load_jsonl, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUESTS = ROOT / "data/api_audit/api_audit_smoke_10_v5_requests.jsonl"
DEFAULT_ITEMS = ROOT / "data/slices/api_audit_smoke_10_v5.jsonl"


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(path)


def index_unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = str(row.get(key, ""))
        if not value:
            raise SystemExit(f"{label} row missing {key!r}")
        if value in indexed:
            raise SystemExit(f"Duplicate {label} {key}: {value}")
        indexed[value] = row
    return indexed


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def optional_int(row: dict[str, Any], key: str) -> int | str:
    value = row.get(key, "")
    if value in ("", None):
        return ""
    return int(value)


def import_rows(
    requests: list[dict[str, Any]],
    responses_by_id: dict[str, dict[str, Any]],
    items_by_id: dict[str, dict[str, Any]],
    provider: str,
    model: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for request in requests:
        request_id = str(request["request_id"])
        response = responses_by_id.get(request_id)
        if response is None:
            continue
        item = items_by_id[str(request["id"])]
        raw_output = str(response.get("raw_output", ""))
        answer_type = str(item["answer_type"])
        parsed = parse_answer(raw_output, answer_type)
        rows.append(
            {
                "request_id": request_id,
                "provider": provider,
                "provider_response_id": str(response.get("provider_response_id", "")),
                "model": model,
                "id": item["id"],
                "dataset": item.get("dataset", ""),
                "task_type": item.get("task_type", ""),
                "answer_type": answer_type,
                "variant": request["variant"],
                "prompt_mode": request["prompt_mode"],
                "raw_output": raw_output,
                "parsed": parsed,
                "gold": item["answer"],
                "correct": is_correct(parsed, str(item["answer"]), answer_type),
                "rewrite_output": "",
                "seconds": response.get("seconds", ""),
                "usage_input_tokens": optional_int(response, "usage_input_tokens"),
                "usage_output_tokens": optional_int(response, "usage_output_tokens"),
            }
        )
    return rows


def write_report(
    path: Path,
    requests_path: Path,
    responses_path: Path,
    output_path: Path,
    provider: str,
    model: str,
    expected: int,
    rows: list[dict[str, Any]],
) -> None:
    input_usage = sum(int(row["usage_input_tokens"] or 0) for row in rows)
    output_usage = sum(int(row["usage_output_tokens"] or 0) for row in rows)
    lines = [
        "# API Audit Response Import",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        f"- Provider: `{provider}`",
        f"- Model: `{model}`",
        f"- Requests: `{repo_path(requests_path)}`",
        f"- Raw responses: `{repo_path(responses_path)}`",
        f"- Imported results: `{repo_path(output_path)}`",
        "",
        "## Validation",
        "",
        f"- Expected requests: {expected}",
        f"- Imported responses: {len(rows)}",
        f"- Parsed-empty responses: {sum(not str(row['parsed']).strip() for row in rows)}",
        f"- Correct responses: {sum(bool(row['correct']) for row in rows)}",
        f"- Reported input tokens: {input_usage}",
        f"- Reported output tokens: {output_usage}",
        "",
        "Imported rows use the same `raw_output`, `parsed`, `gold`, and `correct`",
        "fields as the open-model evaluation outputs.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests", type=Path, default=DEFAULT_REQUESTS)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--source-items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--require-complete", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requests = load_jsonl(args.requests)
    responses = load_jsonl(args.responses)
    requests_by_id = index_unique(requests, "request_id", "request")
    responses_by_id = index_unique(responses, "request_id", "response")
    items_by_id = index_unique(load_jsonl(args.source_items), "id", "source item")

    unknown = sorted(set(responses_by_id) - set(requests_by_id))
    if unknown:
        raise SystemExit(f"Unknown response request ids: {', '.join(unknown[:5])}")
    missing = sorted(set(requests_by_id) - set(responses_by_id))
    if args.require_complete and missing:
        raise SystemExit(f"Missing {len(missing)} responses; first: {missing[0]}")

    rows = import_rows(requests, responses_by_id, items_by_id, args.provider, args.model)
    write_jsonl(args.output, rows)
    write_report(
        args.report,
        args.requests,
        args.responses,
        args.output,
        args.provider,
        args.model,
        len(requests),
        rows,
    )
    print(f"requests={len(requests)}")
    print(f"responses={len(responses_by_id)}")
    print(f"imported={len(rows)}")
    print(f"missing={len(missing)}")
    print(f"output={args.output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
