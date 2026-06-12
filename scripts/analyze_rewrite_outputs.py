#!/usr/bin/env python3
"""Analyze intermediate rewrite/translation outputs from mitigation runs."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


BN_RE = re.compile(r"[\u0980-\u09ff]")
LATIN_RE = re.compile(r"[A-Za-z]")
DIGIT_RE = re.compile(r"[0-9\u09e6-\u09ef]")
OPTION_RE = re.compile(r"^\s*([A-D])[\).]\s+", re.MULTILINE)
FORMULA_RE = re.compile(r"\b[A-Z][A-Za-z]?[0-9]*(?:[A-Z][A-Za-z]?[0-9]*)+\b")
ANSWER_MARKER_RE = re.compile(
    r"\bfinal\s+answer\s*:|\banswer\s*:|সঠিক\s+উত্তর|উত্তর\s*:",
    flags=re.IGNORECASE,
)
DIGIT_TRANS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_eval_rows(inputs: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in jsonl_paths(inputs):
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not row.get("rewrite_output"):
                    continue
                if rescore:
                    if row.get("raw_output"):
                        row["parsed"] = parse_answer(
                            str(row.get("raw_output", "")),
                            str(row.get("answer_type", "")),
                        )
                    row["correct"] = is_correct(
                        str(row.get("parsed", "")),
                        str(row.get("gold", "")),
                        str(row.get("answer_type", "")),
                    )
                row["_source"] = str(path)
                row["_line"] = line_no
                rows.append(row)
    return rows


def index_items(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in items}


def ratio(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def digit_sequence(text: str) -> list[str]:
    return [digit.translate(DIGIT_TRANS) for digit in DIGIT_RE.findall(text)]


def analyze_row(row: dict[str, Any], item: dict[str, Any] | None) -> dict[str, Any]:
    rewrite = str(row.get("rewrite_output", ""))
    variant = str(row.get("variant", ""))
    source_text = str(item.get(variant, "")) if item else ""
    chars = len(rewrite)
    bn_chars = len(BN_RE.findall(rewrite))
    latin_chars = len(LATIN_RE.findall(rewrite))
    source_options = OPTION_RE.findall(source_text)
    rewrite_options = OPTION_RE.findall(rewrite)
    source_formulas = sorted(set(FORMULA_RE.findall(source_text)))
    rewrite_formulas = sorted(set(FORMULA_RE.findall(rewrite)))
    source_digit_sequence = digit_sequence(source_text)
    rewrite_digit_sequence = digit_sequence(rewrite)
    source_digits = len(source_digit_sequence)
    rewrite_digits = len(rewrite_digit_sequence)
    source_answer_markers = ANSWER_MARKER_RE.findall(source_text)
    rewrite_answer_markers = ANSWER_MARKER_RE.findall(rewrite)
    source_line_count = len(source_text.splitlines())
    rewrite_line_count = len(rewrite.splitlines())
    return {
        "model": row.get("model", ""),
        "prompt_mode": row.get("prompt_mode", ""),
        "dataset": row.get("dataset", ""),
        "variant": variant,
        "id": row.get("id", ""),
        "correct": bool(row.get("correct")),
        "rewrite_chars": chars,
        "bengali_ratio": ratio(bn_chars, chars),
        "latin_ratio": ratio(latin_chars, chars),
        "empty_rewrite": not rewrite.strip(),
        "source_option_count": len(source_options),
        "rewrite_option_count": len(rewrite_options),
        "options_preserved": source_options == rewrite_options,
        "source_digit_count": source_digits,
        "rewrite_digit_count": rewrite_digits,
        "digit_count_preserved": source_digits == rewrite_digits,
        "source_digit_sequence": " ".join(source_digit_sequence),
        "rewrite_digit_sequence": " ".join(rewrite_digit_sequence),
        "digit_sequence_preserved": source_digit_sequence == rewrite_digit_sequence,
        "source_formulas": " ".join(source_formulas),
        "rewrite_formulas": " ".join(rewrite_formulas),
        "formulas_preserved": source_formulas == rewrite_formulas,
        "source_line_count": source_line_count,
        "rewrite_line_count": rewrite_line_count,
        "line_count_preserved": source_line_count == rewrite_line_count,
        "source_answer_marker_count": len(source_answer_markers),
        "rewrite_answer_marker_count": len(rewrite_answer_markers),
        "extra_answer_markers": len(rewrite_answer_markers)
        > len(source_answer_markers),
        "rewrite_preview": rewrite[:220].replace("\n", " "),
        "source": row.get("_source", ""),
        "line": row.get("_line", ""),
    }


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row["model"], row["prompt_mode"], row["dataset"], row["variant"])
        groups[key].append(row)

    out: list[dict[str, Any]] = []
    for key, items in sorted(groups.items()):
        n = len(items)
        out.append(
            {
                "model": key[0],
                "prompt_mode": key[1],
                "dataset": key[2],
                "variant": key[3],
                "n": n,
                "correct": sum(int(row["correct"]) for row in items),
                "mean_bengali_ratio": round(
                    sum(float(row["bengali_ratio"]) for row in items) / n, 4
                ),
                "mean_latin_ratio": round(
                    sum(float(row["latin_ratio"]) for row in items) / n, 4
                ),
                "empty_rewrites": sum(int(row["empty_rewrite"]) for row in items),
                "options_not_preserved": sum(
                    int(not row["options_preserved"]) for row in items
                ),
                "digit_count_not_preserved": sum(
                    int(not row["digit_count_preserved"]) for row in items
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
                "extra_answer_marker_count": sum(
                    int(row["extra_answer_markers"]) for row in items
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
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = index_items(load_jsonl(args.items))
    eval_rows = load_eval_rows(args.inputs, args.rescore)
    analyzed = [
        analyze_row(row, items.get(str(row.get("id", "")))) for row in eval_rows
    ]
    summary = summarize(analyzed)
    write_csv(args.items_output, analyzed)
    write_csv(args.summary_output, summary)
    for row in summary:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print(f"Wrote {args.items_output}")
    print(f"Wrote {args.summary_output}")


if __name__ == "__main__":
    main()
