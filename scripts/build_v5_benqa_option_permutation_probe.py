#!/usr/bin/env python3
"""Build a reviewed-v5 BEnQA dev probe with counterfactual option rotations."""

from __future__ import annotations

import argparse
import copy
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_ID_SOURCE = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_OUTPUT = (
    ROOT / "data/slices/validation200_v5_dev50_benqa_option_permutations.jsonl"
)
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_permutation_probe.md"

OPTIONS = ("A", "B", "C", "D")
OPTION_LINE_RE = re.compile(r"^([ABCD])\.\s*(.*)$", flags=re.MULTILINE)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


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


def option_map(shift: int) -> tuple[dict[str, str], dict[str, str]]:
    old_to_new = {
        option: OPTIONS[(index + shift) % len(OPTIONS)]
        for index, option in enumerate(OPTIONS)
    }
    new_to_old = {new: old for old, new in old_to_new.items()}
    return old_to_new, new_to_old


def parse_options(text: str, item_id: str, variant: str) -> dict[str, str]:
    options = {
        match.group(1): match.group(2).strip()
        for match in OPTION_LINE_RE.finditer(text)
    }
    if set(options) != set(OPTIONS):
        raise SystemExit(
            f"Could not parse exactly four options for {item_id} variant={variant}: "
            f"{sorted(options)}"
        )
    return options


def permute_text(text: str, item_id: str, variant: str, shift: int) -> str:
    options = parse_options(text, item_id, variant)
    _, new_to_old = option_map(shift)

    def replace(match: re.Match[str]) -> str:
        new_label = match.group(1)
        return f"{new_label}. {options[new_to_old[new_label]]}"

    return OPTION_LINE_RE.sub(replace, text)


def permute_choice_metadata(
    metadata: dict[str, Any], shift: int
) -> dict[str, Any]:
    out = copy.deepcopy(metadata)
    _, new_to_old = option_map(shift)
    for field in ("choices_bangla", "choices_english"):
        choices = out.get(field)
        if isinstance(choices, dict) and set(choices) == set(OPTIONS):
            out[field] = {
                new_label: choices[new_to_old[new_label]]
                for new_label in OPTIONS
            }
    return out


def build_rows(validation: Path, id_source: Path) -> list[dict[str, Any]]:
    dev_ids = {str(row["id"]) for row in load_jsonl(id_source)}
    source_rows = [
        row
        for row in load_jsonl(validation)
        if str(row["id"]) in dev_ids
        and row.get("dataset") == "benqa"
        and row.get("answer_type") == "choice"
    ]
    if len(source_rows) != 36:
        raise SystemExit(f"Expected 36 dev BEnQA MCQs, got {len(source_rows)}")

    rows: list[dict[str, Any]] = []
    for source in sorted(source_rows, key=lambda row: str(row["id"])):
        original_answer = str(source["answer"]).strip().upper()
        if original_answer not in OPTIONS:
            raise SystemExit(f"Invalid choice answer for {source['id']}: {original_answer}")
        for shift in range(len(OPTIONS)):
            old_to_new, new_to_old = option_map(shift)
            row = copy.deepcopy(source)
            source_id = str(source["id"])
            row["id"] = f"{source_id}__perm{shift}"
            row["source_id"] = source_id
            row["permutation_shift"] = shift
            row["option_old_to_new"] = old_to_new
            row["option_new_to_old"] = new_to_old
            row["original_answer"] = original_answer
            row["answer"] = old_to_new[original_answer]
            for variant in ("bangla", "banglish_clean", "banglish_noisy", "english"):
                value = row.get(variant)
                if value:
                    row[variant] = permute_text(
                        str(value), source_id, variant, shift
                    )
            row["metadata"] = permute_choice_metadata(
                dict(row.get("metadata", {})), shift
            )
            row["option_permutation_probe"] = {
                "design": "cyclic_content_rotation",
                "source_id": source_id,
                "shift": shift,
                "old_to_new": old_to_new,
                "new_to_old": new_to_old,
            }
            rows.append(row)
    if len(rows) != 144:
        raise SystemExit(f"Expected 144 permuted rows, got {len(rows)}")
    return rows


def write_report(
    path: Path,
    validation: Path,
    id_source: Path,
    output: Path,
    rows: list[dict[str, Any]],
) -> None:
    source_ids = {str(row["source_id"]) for row in rows}
    shifts = Counter(int(row["permutation_shift"]) for row in rows)
    gold = Counter(str(row["answer"]) for row in rows)
    lines = [
        "# Frozen-V5 BEnQA Option-Permutation Probe",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This controlled dev-only probe rotates each reviewed-Banglish BEnQA MCQ",
        "option content through labels A/B/C/D while remapping the gold label.",
        "It distinguishes semantic-option tracking from fixed-label attraction.",
        "The probe is diagnostic and does not launch held-out test150.",
        "",
        "## Inputs",
        "",
        f"- Frozen validation: `{repo_path(validation)}`",
        f"- Dev-id source: `{repo_path(id_source)}`",
        f"- Probe JSONL: `{repo_path(output)}`",
        "",
        "## Counts",
        "",
        f"- Source dev BEnQA MCQs: {len(source_ids)}",
        f"- Counterfactual rows: {len(rows)}",
        f"- Rotations per item: {len(shifts)}",
        f"- Rows per rotation: {', '.join(f'{key}={shifts[key]}' for key in sorted(shifts))}",
        f"- Remapped gold labels: {', '.join(f'{key}={gold[key]}' for key in OPTIONS)}",
        "",
        "## Interpretation Contract",
        "",
        "- If a prediction follows the option content after rotation, it supports",
        "  semantic-option tracking.",
        "- If a prediction remains attached to label D after the original content",
        "  moves away from D, it supports a positional D-attractor.",
        "- Treat all results as dev-only behavioral evidence, not an internal",
        "  causal-mechanism proof.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--id-source", type=Path, default=DEFAULT_ID_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(args.validation, args.id_source)
    write_jsonl(args.output, rows)
    write_report(
        args.report_output,
        args.validation,
        args.id_source,
        args.output,
        rows,
    )
    print(f"rows={len(rows)}")
    print(f"output={args.output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
