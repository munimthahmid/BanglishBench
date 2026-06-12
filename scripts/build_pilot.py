#!/usr/bin/env python3
"""Build a local pilot benchmark JSONL from cached Bangla datasets."""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bn_romanize import romanize_bangla, romanize_noisy


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENQA_DIR = ROOT / "literature/code/BEnQA/data/BEnQA"
DEFAULT_BANGLAMATH_CSV = (
    ROOT / "literature/code/BanglaMATH/BanglaMath - Bangla_Math_dataset.csv"
)
DEFAULT_BANGLAMATH_EN_CSV = (
    ROOT
    / "literature/code/BanglaMATH/BanglaMath - Mathproblem_translated_in_english.csv"
)
DEFAULT_OUT = ROOT / "data/pilot/items.jsonl"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def clean(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(value.replace("\r\n", "\n").replace("\r", "\n").split())


def format_mcq(question: str, choices: dict[str, str]) -> str:
    lines = [question.strip()]
    for key in ("A", "B", "C", "D"):
        lines.append(f"{key}. {choices[key].strip()}")
    lines.append("Answer with only A, B, C, or D.")
    return "\n".join(lines)


def format_short_answer(question: str) -> str:
    return f"{question.strip()}\nReturn only the final answer."


def round_robin_sample(
    groups: dict[str, list[dict[str, Any]]], count: int, rng: random.Random
) -> list[dict[str, Any]]:
    buckets = {key: rows[:] for key, rows in sorted(groups.items())}
    for rows in buckets.values():
        rng.shuffle(rows)

    sampled: list[dict[str, Any]] = []
    while len(sampled) < count and any(buckets.values()):
        for key in list(buckets):
            if len(sampled) >= count:
                break
            if buckets[key]:
                sampled.append(buckets[key].pop())
    return sampled


def build_benqa_items(benqa_dir: Path, count: int, rng: random.Random) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for csv_path in sorted(benqa_dir.glob("*.csv")):
        source_name = csv_path.stem
        for row_idx, row in enumerate(read_csv(csv_path), start=1):
            answer = clean(row.get("Correct Answer")).upper()[:1]
            if answer not in {"A", "B", "C", "D"}:
                continue

            en_question = clean(row.get("English Question"))
            bn_question = clean(row.get("Bengali Question"))
            en_choices = {key: clean(row.get(key)) for key in ("A", "B", "C", "D")}
            bn_choices = {
                "A": clean(row.get("A Bn")),
                "B": clean(row.get("B Bn")),
                "C": clean(row.get("C Bn")),
                "D": clean(row.get("D Bn")),
            }
            if not en_question or not bn_question:
                continue
            if not all(en_choices.values()) or not all(bn_choices.values()):
                continue

            grade = source_name.split("-", 1)[0]
            subject = source_name.split("-", 1)[1] if "-" in source_name else source_name
            bangla = format_mcq(bn_question, bn_choices)
            english = format_mcq(en_question, en_choices)
            item = {
                "id": f"benqa_{source_name}_{row_idx:04d}",
                "dataset": "benqa",
                "task_type": "mcq",
                "domain": subject.lower(),
                "difficulty": "unknown",
                "bangla": bangla,
                "english": english,
                "banglish_clean": romanize_bangla(bangla),
                "banglish_noisy": romanize_noisy(bangla),
                "answer": answer,
                "answer_type": "choice",
                "source_file": str(csv_path.relative_to(ROOT)),
                "source_row": row_idx,
                "source_url": "https://github.com/sheikhshafayat/BEnQA",
                "license_notes": "See upstream BEnQA repository.",
                "transliteration_method": "rule_based_bootstrap",
                "quality_status": "auto_romanized_unverified",
                "english_available": True,
                "metadata": {
                    "grade": grade,
                    "subject": subject,
                    "choices_bangla": bn_choices,
                    "choices_english": en_choices,
                },
            }
            grouped[source_name].append(item)

    return round_robin_sample(grouped, count, rng)


def load_banglamath_translations(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    translations: dict[str, str] = {}
    for row in read_csv(path):
        bn_question = clean(row.get("Math Problem (Bengali)") or row.get("Questions"))
        en_question = clean(row.get("Math Problem (English)"))
        if bn_question and en_question:
            translations[bn_question] = en_question
    return translations


def build_banglamath_items(
    csv_path: Path, english_csv_path: Path, count: int, rng: random.Random
) -> list[dict[str, Any]]:
    translations = load_banglamath_translations(english_csv_path)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row_idx, row in enumerate(read_csv(csv_path), start=1):
        question = clean(row.get("Question"))
        answer = clean(row.get("Answer"))
        if not question or not answer:
            continue
        english_question = translations.get(question, "")
        bangla = format_short_answer(question)
        english = format_short_answer(english_question) if english_question else ""
        grade = clean(row.get("Grade")) or "unknown"
        item = {
            "id": f"banglamath_{row_idx:04d}",
            "dataset": "banglamath",
            "task_type": "short_answer",
            "domain": "math",
            "difficulty": "unknown",
            "bangla": bangla,
            "english": english,
            "banglish_clean": romanize_bangla(bangla),
            "banglish_noisy": romanize_noisy(bangla),
            "answer": answer,
            "answer_type": "short_answer",
            "source_file": str(csv_path.relative_to(ROOT)),
            "source_row": row_idx,
            "source_url": "https://github.com/TabiaTanzin/BanglaMATH-A-Bangla-benchmark-dataset-for-testing-LLM-mathematical-reasoning-at-grades-6-7-and-8",
            "license_notes": "Research use; see upstream BanglaMATH repository.",
            "transliteration_method": "rule_based_bootstrap",
            "quality_status": "auto_romanized_unverified",
            "english_available": bool(english_question),
            "metadata": {
                "grade": grade,
                "steps": clean(row.get("Steps")),
                "digit": clean(row.get("Digit")),
                "explanation": clean(row.get("Explanation")),
            },
        }
        translated_prefix = "translated" if english_question else "untranslated"
        grouped[f"{translated_prefix}_{grade}"].append(item)

    # Prefer translated rows, but keep grade balance and fill from untranslated rows.
    translated = {k: v for k, v in grouped.items() if k.startswith("translated_")}
    untranslated = {k: v for k, v in grouped.items() if k.startswith("untranslated_")}
    sampled = round_robin_sample(translated, min(count, sum(map(len, translated.values()))), rng)
    if len(sampled) < count:
        sampled.extend(round_robin_sample(untranslated, count - len(sampled), rng))
    return sampled


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


def write_manifest(path: Path, rows: list[dict[str, Any]], args: argparse.Namespace) -> None:
    counts = Counter(row["dataset"] for row in rows)
    english_counts = Counter(
        f"{row['dataset']}:{'english' if row.get('english_available') else 'no_english'}"
        for row in rows
    )
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "output": repo_path(path),
        "seed": args.seed,
        "counts_by_dataset": dict(sorted(counts.items())),
        "english_availability": dict(sorted(english_counts.items())),
        "total_items": len(rows),
        "notes": [
            "Banglish fields are rule-based bootstrap romanizations and are not human verified.",
            "Use this pilot to test pipeline mechanics before expensive Kaggle runs.",
        ],
    }
    manifest_path = path.with_name("manifest.json")
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benqa-dir", type=Path, default=DEFAULT_BENQA_DIR)
    parser.add_argument("--banglamath-csv", type=Path, default=DEFAULT_BANGLAMATH_CSV)
    parser.add_argument("--banglamath-english-csv", type=Path, default=DEFAULT_BANGLAMATH_EN_CSV)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--benqa-count", type=int, default=200)
    parser.add_argument("--banglamath-count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=17)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)

    items: list[dict[str, Any]] = []
    if args.benqa_count:
        items.extend(build_benqa_items(args.benqa_dir, args.benqa_count, rng))
    if args.banglamath_count:
        items.extend(
            build_banglamath_items(
                args.banglamath_csv, args.banglamath_english_csv, args.banglamath_count, rng
            )
        )

    rng.shuffle(items)
    write_jsonl(args.out, items)
    write_manifest(args.out, items, args)
    print(f"Wrote {len(items)} items to {args.out}")


if __name__ == "__main__":
    main()
