#!/usr/bin/env python3
"""Build prompts for generated alternate-script views from Banglish items."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_OUTPUT = (
    ROOT / "data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl"
)
DEFAULT_REPORT = ROOT / "reports/generated_view_prompt_set_dev50_benqa_mcq.md"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def make_bn_prompt(text: str) -> str:
    return (
        "Rewrite the following Latin-script Bangla/Banglish evaluation item in "
        "standard Bengali script. Preserve numbers, formulas, units, line breaks, "
        "and answer options exactly. Do not solve the item. Do not add an answer. "
        "Output only the rewritten item.\n\n"
        f"{text}"
    )


def make_en_prompt(text: str) -> str:
    return (
        "Translate the following Latin-script Bangla/Banglish evaluation item into "
        "clear English. Preserve numbers, formulas, units, line breaks, and answer "
        "options exactly. Do not solve the item. Do not add an answer. Output only "
        "the translated item.\n\n"
        f"{text}"
    )


def load_id_filter(path: Path | None) -> set[str] | None:
    if path is None:
        return None
    ids: set[str] = set()
    for row in load_jsonl(path):
        item_id = str(row.get("id", ""))
        if item_id:
            ids.add(item_id)
    return ids


def build_rows(
    items: list[dict[str, Any]],
    dataset: str,
    answer_type: str,
    id_filter: set[str] | None = None,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        if id_filter is not None and str(item.get("id", "")) not in id_filter:
            continue
        if dataset and item.get("dataset") != dataset:
            continue
        if answer_type and item.get("answer_type") != answer_type:
            continue
        source_text = item.get("banglish_clean", "")
        if not source_text:
            continue
        base = {
            "id": item["id"],
            "dataset": item.get("dataset", ""),
            "task_type": item.get("task_type", ""),
            "answer_type": item.get("answer_type", ""),
            "gold": item.get("answer", ""),
            "source_variant": "banglish_clean",
            "source_text": source_text,
        }
        out.append(
            {
                **base,
                "target_view": "generated_bn",
                "generation_prompt": make_bn_prompt(source_text),
            }
        )
        out.append(
            {
                **base,
                "target_view": "generated_en",
                "generation_prompt": make_en_prompt(source_text),
            }
        )
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(
    path: Path,
    input_path: Path,
    id_source: Path | None,
    output_path: Path,
    rows: list[dict[str, Any]],
    dataset: str,
    answer_type: str,
) -> None:
    item_ids = {row["id"] for row in rows}
    target_counts = Counter(row["target_view"] for row in rows)
    lines = [
        "# Generated-View Prompt Set: Dev50 BEnQA MCQ",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This prompt set prepares the first deployable consistency-routing",
        "experiment without launching a generator yet. It creates locked prompts",
        "for generated Bengali and generated English alternate views from",
        "Banglish-only inputs.",
        "",
        "## Artifacts",
        "",
        f"- Input slice: `{repo_path(input_path)}`",
    ]
    if id_source is not None:
        lines.append(f"- ID filter source: `{repo_path(id_source)}`")
    lines.extend(
        [
            f"- Output JSONL: `{repo_path(output_path)}`",
            "",
            "## Filter",
            "",
            f"- Dataset: `{dataset}`",
            f"- Answer type: `{answer_type}`",
            f"- Unique items: {len(item_ids)}",
            f"- Generation prompts: {len(rows)}",
        ]
    )
    for target, count in sorted(target_counts.items()):
        lines.append(f"- `{target}`: {count}")
    lines.extend(
        [
            "",
            "## Use",
            "",
            "Run a generator over `generation_prompt`, write its output beside the",
            "same `id` and `target_view`, then apply the preservation gates from",
            "`reports/generated_view_preservation_audit_v2.md` before answering",
            "generated views.",
            "",
            "Do not tune on test150 until generator prompts and routing are fixed",
            "on dev50.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--id-source",
        type=Path,
        help="Optional JSONL source whose item ids define the prompt subset.",
    )
    parser.add_argument("--dataset", default="benqa")
    parser.add_argument("--answer-type", default="choice")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_jsonl(args.input)
    id_filter = load_id_filter(args.id_source)
    rows = build_rows(items, args.dataset, args.answer_type, id_filter=id_filter)
    write_jsonl(args.output, rows)
    write_report(
        args.report_output,
        args.input,
        args.id_source,
        args.output,
        rows,
        args.dataset,
        args.answer_type,
    )
    print(f"items={len({row['id'] for row in rows})}")
    print(f"prompts={len(rows)}")
    print(f"wrote={args.output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
