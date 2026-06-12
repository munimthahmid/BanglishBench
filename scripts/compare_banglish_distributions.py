#!/usr/bin/env python3
"""Compare controlled Banglish with real Romanized Bangla corpora."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


LATIN_RE = re.compile(r"[A-Za-z]")
BN_RE = re.compile(r"[\u0980-\u09ff]")
DIGIT_RE = re.compile(r"[0-9\u09e6-\u09ef]")
WORD_RE = re.compile(r"[A-Za-z\u0980-\u09ff0-9\u09e6-\u09ef]+")
OPTION_LINE_RE = re.compile(r"^\s*[A-D][\).]\s+")


def char_ratio(pattern: re.Pattern[str], text: str) -> float:
    chars = [ch for ch in text if not ch.isspace()]
    if not chars:
        return 0.0
    return round(len(pattern.findall(text)) / len(chars), 4)


def row_metrics(source: str, item_id: str, text: str) -> dict[str, Any]:
    words = WORD_RE.findall(text)
    latin_ratio = char_ratio(LATIN_RE, text)
    bengali_ratio = char_ratio(BN_RE, text)
    return {
        "source": source,
        "id": item_id,
        "text": text,
        "chars": len(text),
        "words": len(words),
        "latin_ratio": latin_ratio,
        "bengali_ratio": bengali_ratio,
        "has_digits": bool(DIGIT_RE.search(text)),
        "mixed_latin_bengali": latin_ratio > 0 and bengali_ratio > 0,
    }


def load_validation(path: Path, variant: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            text = str(item.get(variant, ""))
            if text:
                rows.append(row_metrics(f"validation:{variant}:raw", str(item["id"]), text))
                content_text = strip_eval_scaffold(text)
                if content_text:
                    rows.append(
                        row_metrics(
                            f"validation:{variant}:content",
                            str(item["id"]),
                            content_text,
                        )
                    )
    return rows


def strip_eval_scaffold(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Answer with only"):
            continue
        if stripped.startswith("Return only"):
            continue
        if OPTION_LINE_RE.match(stripped):
            continue
        kept.append(stripped)
    return "\n".join(kept)


def load_banglatlit(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                item_id = str(row.get("id", ""))
                text = str(row.get("text_transliterated", ""))
                if text:
                    rows.append(row_metrics(f"banglatlit:{path.stem}", item_id, text))
    return rows


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_source.setdefault(str(row["source"]), []).append(row)

    out: list[dict[str, Any]] = []
    for source, items in sorted(by_source.items()):
        n = len(items)
        out.append(
            {
                "source": source,
                "n": n,
                "mean_chars": round(sum(int(row["chars"]) for row in items) / n, 4),
                "mean_words": round(sum(int(row["words"]) for row in items) / n, 4),
                "mean_latin_ratio": round(
                    sum(float(row["latin_ratio"]) for row in items) / n, 4
                ),
                "mean_bengali_ratio": round(
                    sum(float(row["bengali_ratio"]) for row in items) / n, 4
                ),
                "digit_row_share": round(
                    sum(int(row["has_digits"]) for row in items) / n, 4
                ),
                "mixed_latin_bengali_share": round(
                    sum(int(row["mixed_latin_bengali"]) for row in items) / n, 4
                ),
            }
        )
    return out


def top_words(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    counters: dict[str, Counter[str]] = {}
    for row in rows:
        source = str(row["source"])
        counters.setdefault(source, Counter())
        counters[source].update(word.lower() for word in WORD_RE.findall(str(row["text"])))

    out: list[dict[str, Any]] = []
    for source, counter in sorted(counters.items()):
        for rank, (word, count) in enumerate(counter.most_common(limit), start=1):
            out.append({"source": source, "rank": rank, "word": word, "count": count})
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
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--validation-variant", default="banglish_clean")
    parser.add_argument("--banglatlit", type=Path, nargs="+", required=True)
    parser.add_argument("--items-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--top-words-output", type=Path, required=True)
    parser.add_argument("--top-words", type=int, default=30)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_validation(args.validation, args.validation_variant)
    rows.extend(load_banglatlit(args.banglatlit))
    write_csv(args.items_output, rows)
    write_csv(args.summary_output, summarize(rows))
    write_csv(args.top_words_output, top_words(rows, args.top_words))
    print(f"items={len(rows)}")
    print(f"wrote={args.items_output}")
    print(f"wrote={args.summary_output}")
    print(f"wrote={args.top_words_output}")


if __name__ == "__main__":
    main()
