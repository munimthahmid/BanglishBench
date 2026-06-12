#!/usr/bin/env python3
"""Build a controlled Bangla/Banglish/English MGSM slice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from bn_romanize import romanize_bangla, romanize_noisy


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BN = ROOT / "literature/data/mgsm/mgsm_bn.tsv"
DEFAULT_EN = ROOT / "literature/data/mgsm/mgsm_en.tsv"
DEFAULT_OUTPUT = ROOT / "data/slices/mgsm_bn_50_v1.jsonl"


def load_tsv(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                raise ValueError(f"{path}:{line_no}: expected 2 tab-separated columns")
            rows.append((parts[0], parts[1]))
    return rows


def with_instruction(question: str) -> str:
    return f"{question.strip()}\nReturn only the final answer."


def build_items(bn_rows: list[tuple[str, str]], en_rows: list[tuple[str, str]], limit: int) -> list[dict[str, Any]]:
    if len(bn_rows) != len(en_rows):
        raise ValueError(f"BN/EN length mismatch: {len(bn_rows)} vs {len(en_rows)}")
    items: list[dict[str, Any]] = []
    for idx, ((bn_question, bn_answer), (en_question, en_answer)) in enumerate(
        zip(bn_rows, en_rows), start=1
    ):
        if limit and len(items) >= limit:
            break
        if bn_answer != en_answer:
            raise ValueError(
                f"Answer mismatch at row {idx}: BN={bn_answer!r}, EN={en_answer!r}"
            )
        bangla = with_instruction(bn_question)
        english = with_instruction(en_question)
        items.append(
            {
                "id": f"mgsm_bn_{idx:04d}",
                "dataset": "mgsm",
                "task_type": "math_word_problem",
                "domain": "grade_school_math",
                "difficulty": "unknown",
                "answer_type": "short_answer",
                "answer": bn_answer,
                "bangla": bangla,
                "banglish_clean": with_instruction(romanize_bangla(bn_question)),
                "banglish_noisy": with_instruction(romanize_noisy(bn_question)),
                "english": english,
                "english_available": True,
                "quality_status": "auto_romanized_unverified",
                "transliteration_method": "rule_based_bootstrap",
                "source_file": str(DEFAULT_BN.relative_to(ROOT)),
                "source_row": idx,
                "source_url": "https://huggingface.co/datasets/juletxara/mgsm",
                "license_notes": "See upstream MGSM dataset card/source.",
                "metadata": {
                    "english_answer": en_answer,
                    "source_language": "bn",
                },
            }
        )
    return items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bn", type=Path, default=DEFAULT_BN)
    parser.add_argument("--en", type=Path, default=DEFAULT_EN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=50)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bn_rows = load_tsv(args.bn)
    en_rows = load_tsv(args.en)
    items = build_items(bn_rows, en_rows, args.limit)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Wrote {len(items)} items to {args.output}")


if __name__ == "__main__":
    main()

