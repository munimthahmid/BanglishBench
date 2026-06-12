#!/usr/bin/env python3
"""Estimate Romanized spelling variation from aligned BanglaTLit rows."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


LATIN_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
BANGLA_TOKEN_RE = re.compile(r"[\u0980-\u09ff0-9\u09e6-\u09ef]+")


def read_rows(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                rows.append(
                    {
                        "source": path.stem,
                        "id": str(row.get("id", "")),
                        "latin": str(row.get("text_transliterated", "")),
                        "bangla": str(row.get("text_bengali", "")),
                    }
                )
    return rows


def analyze(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pair_counts: dict[str, Counter[str]] = defaultdict(Counter)
    stats = Counter()

    for row in rows:
        stats["rows_total"] += 1
        latin_tokens = [tok.lower() for tok in LATIN_TOKEN_RE.findall(row["latin"])]
        bangla_tokens = BANGLA_TOKEN_RE.findall(row["bangla"])
        stats["latin_tokens_total"] += len(latin_tokens)
        stats["bangla_tokens_total"] += len(bangla_tokens)
        if latin_tokens and len(latin_tokens) == len(bangla_tokens):
            stats["rows_token_aligned"] += 1
            stats["aligned_token_pairs"] += len(latin_tokens)
            for latin_token, bangla_token in zip(latin_tokens, bangla_tokens):
                pair_counts[bangla_token][latin_token] += 1

    variation_rows: list[dict[str, Any]] = []
    for bangla_token, variants in pair_counts.items():
        total = sum(variants.values())
        unique = len(variants)
        repeated_variants = {
            latin_token: count for latin_token, count in variants.items() if count >= 2
        }
        if total < 3:
            continue
        top = "; ".join(f"{word}:{count}" for word, count in variants.most_common(12))
        top_repeated = "; ".join(
            f"{word}:{count}"
            for word, count in Counter(repeated_variants).most_common(12)
        )
        variation_rows.append(
            {
                "bangla_token": bangla_token,
                "total_count": total,
                "unique_latin_variants": unique,
                "repeated_latin_variants": len(repeated_variants),
                "top_latin_variants": top,
                "top_repeated_latin_variants": top_repeated,
            }
        )
    variation_rows.sort(
        key=lambda row: (
            int(row["repeated_latin_variants"]),
            int(row["unique_latin_variants"]),
            int(row["total_count"]),
            str(row["bangla_token"]),
        ),
        reverse=True,
    )

    tokens_with_variants = sum(
        1 for variants in pair_counts.values() if sum(variants.values()) >= 3 and len(variants) >= 2
    )
    tokens_with_repeated_variants = sum(
        1
        for variants in pair_counts.values()
        if sum(variants.values()) >= 3
        and sum(1 for count in variants.values() if count >= 2) >= 2
    )
    summary = [
        {"metric": "rows_total", "value": stats["rows_total"]},
        {"metric": "rows_token_aligned", "value": stats["rows_token_aligned"]},
        {
            "metric": "row_token_alignment_share",
            "value": round(stats["rows_token_aligned"] / stats["rows_total"], 4)
            if stats["rows_total"]
            else 0,
        },
        {"metric": "aligned_token_pairs", "value": stats["aligned_token_pairs"]},
        {"metric": "unique_bangla_tokens_aligned", "value": len(pair_counts)},
        {
            "metric": "bangla_tokens_with_2plus_latin_variants_min3",
            "value": tokens_with_variants,
        },
        {
            "metric": "bangla_tokens_with_2plus_repeated_latin_variants_min3",
            "value": tokens_with_repeated_variants,
        },
    ]
    return summary, variation_rows


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
    parser.add_argument("--banglatlit", type=Path, nargs="+", required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--variation-output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary, variation_rows = analyze(read_rows(args.banglatlit))
    write_csv(args.summary_output, summary)
    write_csv(args.variation_output, variation_rows)
    print(f"wrote={args.summary_output}")
    print(f"wrote={args.variation_output}")


if __name__ == "__main__":
    main()
