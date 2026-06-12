#!/usr/bin/env python3
"""Export provider-neutral prompts for a paid API audit without making calls."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import load_jsonl, make_prompt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/api_audit_smoke_10_v5.jsonl"
DEFAULT_OUTPUT = ROOT / "data/api_audit/api_audit_smoke_10_v5_requests.jsonl"
DEFAULT_REPORT = ROOT / "reports/api_audit_prompt_manifest_v5.md"
DEFAULT_SYSTEM_MESSAGE = "You are a careful evaluation model. Output only the final answer."


def approx_tokens(text: str) -> int:
    return math.ceil(len(text) / 4)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def build_requests(
    items: list[dict[str, Any]],
    variants: list[str],
    prompt_mode: str,
    max_output_tokens: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        for variant in variants:
            if not item.get(variant):
                raise SystemExit(f"Missing variant {variant!r} for item {item['id']}")
            request_id = f"{item['id']}::{variant}::{prompt_mode}"
            if request_id in seen:
                raise SystemExit(f"Duplicate request id: {request_id}")
            seen.add(request_id)
            prompt = make_prompt(item, variant, prompt_mode)
            rows.append(
                {
                    "request_id": request_id,
                    "id": item["id"],
                    "dataset": item.get("dataset", ""),
                    "task_type": item.get("task_type", ""),
                    "answer_type": item["answer_type"],
                    "variant": variant,
                    "prompt_mode": prompt_mode,
                    "system_message": DEFAULT_SYSTEM_MESSAGE,
                    "prompt": prompt,
                    "max_output_tokens": max_output_tokens,
                    "prompt_chars": len(prompt),
                    "approx_prompt_tokens": approx_tokens(prompt),
                }
            )
    return rows


def write_report(path: Path, input_path: Path, output_path: Path, rows: list[dict[str, Any]]) -> None:
    variants = Counter(str(row["variant"]) for row in rows)
    lines = [
        "# API Audit Prompt Manifest",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This provider-neutral manifest freezes the exact paid-audit prompts without",
        "calling any external API. Gold answers are intentionally excluded from the",
        "request records.",
        "",
        "## Artifacts",
        "",
        f"- Input slice: `{repo_path(input_path)}`",
        f"- Request JSONL: `{repo_path(output_path)}`",
        f"- Requests: {len(rows)}",
        f"- Approximate prompt tokens: {sum(int(row['approx_prompt_tokens']) for row in rows)}",
        "",
        "## Variant Counts",
        "",
        "| Variant | Requests |",
        "| --- | ---: |",
    ]
    for variant, count in sorted(variants.items()):
        lines.append(f"| `{variant}` | {count} |")
    lines.extend(
        [
            "",
            "## Response Import Contract",
            "",
            "Each provider response JSONL row must include `request_id` and `raw_output`.",
            "Optional fields are `provider_response_id`, `usage_input_tokens`,",
            "`usage_output_tokens`, and `seconds`. Import responses with",
            "`scripts/import_api_audit_responses.py`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--variants", nargs="+", default=["bangla", "banglish_clean", "english"]
    )
    parser.add_argument("--prompt-mode", default="baseline")
    parser.add_argument("--max-output-tokens", type=int, default=128)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_requests(
        load_jsonl(args.input),
        args.variants,
        args.prompt_mode,
        args.max_output_tokens,
    )
    write_jsonl(args.output, rows)
    write_report(args.report, args.input, args.output, rows)
    print(f"requests={len(rows)}")
    print(f"output={args.output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
