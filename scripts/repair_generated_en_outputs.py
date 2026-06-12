#!/usr/bin/env python3
"""Repair generated-English views with strict preservation fallbacks."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audit_generated_view_outputs import (
    ANSWER_MARKER_RE,
    BN_RE,
    OPTION_RE,
    formulas,
    normalize_digits,
    option_labels,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS = (
    ROOT / "data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl"
)
DEFAULT_OUTPUTS = (
    ROOT / "results/generated_views/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq.jsonl"
)
DEFAULT_OUTPUT = (
    ROOT / "results/generated_views/qwen3_4b_selftranslate_guarded_v5_dev50_benqa_mcq_generated_en.jsonl"
)
DEFAULT_REPORT = (
    ROOT / "reports/qwen3_4b_selftranslate_guarded_v5_generated_en_dev50_benqa_mcq.md"
)
ANSWER_FORMAT_LINE_RE = re.compile(r"^Answer with only .*$", flags=re.IGNORECASE)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def output_text(row: dict[str, Any]) -> str:
    for field in [
        "generated_text",
        "generation_output",
        "rewritten_text",
        "translated_text",
        "output_text",
        "output",
        "text",
        "raw_output",
    ]:
        value = row.get(field)
        if value is not None:
            return str(value).strip()
    return ""


def source_tail_lines(source: str) -> list[str]:
    tail: list[str] = []
    for line in source.splitlines():
        stripped = line.strip()
        if OPTION_RE.match(line) or ANSWER_FORMAT_LINE_RE.match(stripped):
            tail.append(line.rstrip())
    return tail


def generated_stem_lines(generated: str) -> list[str]:
    stem: list[str] = []
    for line in generated.splitlines():
        stripped = line.strip()
        if OPTION_RE.match(line) or ANSWER_FORMAT_LINE_RE.match(stripped):
            continue
        if stripped:
            stem.append(line.rstrip())
    return stem


def answer_marker_count(text: str) -> int:
    return len(ANSWER_MARKER_RE.findall(text))


def hard_preservation_fail(source: str, candidate: str) -> bool:
    return (
        not candidate.strip()
        or option_labels(source) != option_labels(candidate)
        or normalize_digits(source) != normalize_digits(candidate)
        or formulas(source) != formulas(candidate)
        or answer_marker_count(candidate) > answer_marker_count(source)
        or bool(BN_RE.search(candidate))
    )


def repair_one(source: str, generated: str) -> tuple[str, str]:
    stem = generated_stem_lines(generated)
    tail = source_tail_lines(source)
    candidate_lines = [*stem, *tail]
    candidate = "\n".join(line for line in candidate_lines if line.strip()).strip()
    if candidate and not hard_preservation_fail(source, candidate):
        return candidate, "translated_stem_source_tail"
    return source.strip(), "source_fallback_after_failed_repair"


def repair(
    prompts: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    generator_label: str,
) -> list[dict[str, Any]]:
    output_by_id = {
        str(row.get("id", "")): output_text(row)
        for row in outputs
        if str(row.get("target_view", "")) == "generated_en"
    }
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        if str(prompt.get("target_view", "")) != "generated_en":
            continue
        item_id = str(prompt["id"])
        source = str(prompt.get("source_text", ""))
        generated = output_by_id.get(item_id, "")
        repaired, strategy = repair_one(source, generated)
        rows.append(
            {
                "id": item_id,
                "target_view": "generated_en",
                "generator": generator_label,
                "repair_strategy": strategy,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "source_text": source,
                "generated_text": repaired,
                "original_generated_text": generated,
            }
        )
    return rows


def write_report(
    path: Path,
    prompts_path: Path,
    outputs_path: Path,
    output_path: Path,
    rows: list[dict[str, Any]],
) -> None:
    counts = Counter(row["repair_strategy"] for row in rows)
    lines = [
        "# Guarded Generated-English Repair",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Purpose",
        "",
        "This deterministic repair creates a conservative generated-English view",
        "from Qwen3 self-translation outputs. It restores source option and",
        "answer-format lines, keeps a translated stem only if the hard",
        "preservation gate still passes, and otherwise falls back to the original",
        "Banglish item. This is a dev diagnostic, not a claim that the fallback",
        "rows are translated English.",
        "",
        "## Artifacts",
        "",
        f"- Prompt set: `{repo_path(prompts_path)}`",
        f"- Input generated-English outputs: `{repo_path(outputs_path)}`",
        f"- Repaired output JSONL: `{repo_path(output_path)}`",
        "",
        "## Counts",
        "",
        f"- Rows: {len(rows)}",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Decision Rule",
            "",
            "Run `scripts/audit_generated_view_outputs.py` on this file before any",
            "answer audit. Even if the gate passes, use the results only as a",
            "conservative generated-English diagnostic because fallback rows are",
            "the original Banglish view.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--outputs", type=Path, default=DEFAULT_OUTPUTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--generator-label",
        default="qwen3_4b_selftranslate_guarded_source_tail_fallback",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = repair(load_jsonl(args.prompts), load_jsonl(args.outputs), args.generator_label)
    write_jsonl(args.output, rows)
    write_report(args.report_output, args.prompts, args.outputs, args.output, rows)
    counts = Counter(row["repair_strategy"] for row in rows)
    print(f"rows={len(rows)}")
    for key, value in sorted(counts.items()):
        print(f"{key}={value}")
    print(f"output={args.output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
