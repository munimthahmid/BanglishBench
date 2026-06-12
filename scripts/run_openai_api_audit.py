#!/usr/bin/env python3
"""Run OpenAI Responses API audit requests from a provider-neutral manifest.

The script writes raw provider responses in the contract expected by
`scripts/import_api_audit_responses.py`. It never prints API key values.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUESTS = ROOT / "data/api_audit/openai_gpt55_diagnostic_60_v5_requests.jsonl"
DEFAULT_OUTPUT = ROOT / "results/api_audit/openai_gpt55_low_diagnostic_60_v5_raw.jsonl"
DEFAULT_MODEL = "gpt-5.5"
DEFAULT_KEY_NAMES = ("OPENAI_API_KEY", "OPENAI_API_KEY2", "OPENAI_API_KEY3")
RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504}


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def collect_keys(names: list[str]) -> list[tuple[str, str]]:
    keys: list[tuple[str, str]] = []
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            keys.append((name, value))
    if not keys:
        raise SystemExit(f"No OpenAI API keys found in: {', '.join(names)}")
    return keys


def selected_requests(
    rows: list[dict[str, Any]],
    limit: int | None,
    request_ids: set[str],
) -> list[dict[str, Any]]:
    selected = [row for row in rows if not request_ids or str(row["request_id"]) in request_ids]
    if limit is not None:
        selected = selected[:limit]
    if not selected:
        raise SystemExit("No requests selected")
    return selected


def existing_request_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids: set[str] = set()
    for row in load_jsonl(path):
        request_id = str(row.get("request_id", ""))
        if request_id:
            ids.add(request_id)
    return ids


def input_messages(request: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": [{"type": "input_text", "text": str(request.get("system_message", ""))}],
        },
        {
            "role": "user",
            "content": [{"type": "input_text", "text": str(request["prompt"])}],
        },
    ]


def extract_text(data: dict[str, Any]) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    texts: list[str] = []
    for item in data.get("output", []) or []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                texts.append(text)
    return "".join(texts).strip()


def finish_reason(data: dict[str, Any]) -> str:
    status = str(data.get("status", "")).lower()
    incomplete = data.get("incomplete_details") or {}
    reason = str(incomplete.get("reason", "")).lower() if isinstance(incomplete, dict) else ""
    if reason == "max_output_tokens":
        return "MAX_TOKENS"
    if status == "completed":
        return "STOP"
    return status.upper() or reason.upper()


def call_openai(
    request: dict[str, Any],
    model: str,
    key: str,
    reasoning_effort: str,
    max_output_tokens_override: int | None,
    timeout: int,
) -> tuple[dict[str, Any], float]:
    max_output_tokens = int(max_output_tokens_override or request.get("max_output_tokens") or 128)
    payload: dict[str, Any] = {
        "model": model,
        "input": input_messages(request),
        "reasoning": {"effort": reasoning_effort},
        "max_output_tokens": max_output_tokens,
        "store": False,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    api_request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    started = time.monotonic()
    with urllib.request.urlopen(api_request, timeout=timeout, context=ssl.create_default_context()) as response:
        data = json.loads(response.read().decode("utf-8"))
    seconds = time.monotonic() - started
    return data, seconds


def response_row(
    request: dict[str, Any],
    model: str,
    key_name: str,
    data: dict[str, Any],
    seconds: float,
    max_output_tokens: int,
    reasoning_effort: str,
) -> dict[str, Any]:
    usage = data.get("usage", {}) or {}
    output_details = usage.get("output_tokens_details", {}) or {}
    return {
        "request_id": request["request_id"],
        "provider_response_id": str(data.get("id", "")),
        "provider_model_version": str(data.get("model", model)),
        "raw_output": extract_text(data),
        "finish_reason": finish_reason(data),
        "requested_max_output_tokens": max_output_tokens,
        "requested_reasoning_effort": reasoning_effort,
        "usage_input_tokens": usage.get("input_tokens", ""),
        "usage_output_tokens": usage.get("output_tokens", ""),
        "usage_thoughts_tokens": output_details.get("reasoning_tokens", ""),
        "usage_total_tokens": usage.get("total_tokens", ""),
        "seconds": f"{seconds:.3f}",
        "key_name": key_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def run_requests(
    requests: list[dict[str, Any]],
    keys: list[tuple[str, str]],
    model: str,
    reasoning_effort: str,
    max_output_tokens_override: int | None,
    retries_per_key: int,
    sleep_seconds: float,
    timeout: int,
    incremental_output: Path | None,
    progress_every: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    key_index = 0
    for index, request in enumerate(requests, start=1):
        last_error = ""
        attempts = 0
        max_attempts = len(keys) * (retries_per_key + 1)
        while attempts < max_attempts:
            key_name, key = keys[key_index % len(keys)]
            key_index += 1
            attempts += 1
            try:
                data, seconds = call_openai(
                    request,
                    model,
                    key,
                    reasoning_effort,
                    max_output_tokens_override,
                    timeout,
                )
                requested_max_output_tokens = int(
                    max_output_tokens_override or request.get("max_output_tokens") or 128
                )
                row = response_row(
                    request,
                    model,
                    key_name,
                    data,
                    seconds,
                    requested_max_output_tokens,
                    reasoning_effort,
                )
                rows.append(row)
                if incremental_output is not None:
                    append_jsonl(incremental_output, row)
                if progress_every <= 1 or index == 1 or index == len(requests) or index % progress_every == 0:
                    print(
                        f"{index}/{len(requests)} {request['request_id']} "
                        f"finish={row['finish_reason']} parsed_text={bool(row['raw_output'])} "
                        f"in={row['usage_input_tokens']} out={row['usage_output_tokens']} "
                        f"reasoning={row['usage_thoughts_tokens']} key={key_name}",
                        flush=True,
                    )
                break
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")[:500]
                last_error = f"HTTP {exc.code}: {body}"
                if exc.code not in RETRYABLE_STATUS:
                    raise SystemExit(f"{request['request_id']} failed: {last_error}") from exc
                time.sleep(sleep_seconds)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = repr(exc)
                time.sleep(sleep_seconds)
        else:
            raise SystemExit(f"{request['request_id']} failed after {attempts} attempts: {last_error}")
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, default=DEFAULT_REQUESTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--key-env", nargs="+", default=list(DEFAULT_KEY_NAMES))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--request-id", action="append", default=[])
    parser.add_argument(
        "--reasoning-effort",
        choices=["none", "low", "medium", "high", "xhigh"],
        default="low",
    )
    parser.add_argument("--max-output-tokens-override", type=int)
    parser.add_argument("--retries-per-key", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=2.0)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--write-each", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--progress-every", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv(ROOT / ".env")
    keys = collect_keys(args.key_env)
    requests = selected_requests(load_jsonl(args.requests), args.limit, set(args.request_id))
    if args.resume:
        done = existing_request_ids(args.output)
        requests = [request for request in requests if str(request["request_id"]) not in done]
        if not requests:
            print("No requests remaining; output already contains selected request ids.")
            return
    if args.write_each and args.output.exists() and not args.resume:
        raise SystemExit(f"Output exists; use --resume or remove it first: {args.output}")
    rows = run_requests(
        requests,
        keys,
        args.model,
        args.reasoning_effort,
        args.max_output_tokens_override,
        args.retries_per_key,
        args.sleep_seconds,
        args.timeout,
        args.output if args.write_each else None,
        args.progress_every,
    )
    if not args.write_each:
        write_jsonl(args.output, rows)
    print(f"wrote={len(rows)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
