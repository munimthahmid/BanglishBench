#!/usr/bin/env python3
"""Compute tokenization and Unicode-size metrics for benchmark variants."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/pilot/items.jsonl"
DEFAULT_OUT = ROOT / "results/tokenization_audit.csv"
DEFAULT_SUMMARY_OUT = ROOT / "results/tokenization_audit_summary.csv"
BANGLA_RE = re.compile(r"[\u0980-\u09ff]")
LATIN_RE = re.compile(r"[A-Za-z]")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def simple_metrics(text: str) -> dict[str, float | int]:
    words = text.split()
    return {
        "chars": len(text),
        "utf8_bytes": len(text.encode("utf-8")),
        "words": len(words),
        "bangla_chars": len(BANGLA_RE.findall(text)),
        "latin_chars": len(LATIN_RE.findall(text)),
        "bytes_per_word": len(text.encode("utf-8")) / max(1, len(words)),
        "chars_per_word": len(text) / max(1, len(words)),
    }


def load_tokenizers(names: list[str]) -> dict[str, Any]:
    if not names:
        return {}
    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise SystemExit(
            "transformers is required for --hf-tokenizer. Install it or run without HF tokenizers."
        ) from exc

    tokenizers = {}
    for name in names:
        tokenizers[name] = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    return tokenizers


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["dataset"], row["variant"], row["tokenizer"])].append(row)

    summary = []
    for (dataset, variant, tokenizer), group in sorted(grouped.items()):
        summary.append(
            {
                "dataset": dataset,
                "variant": variant,
                "tokenizer": tokenizer,
                "items": len(group),
                "mean_words": round(mean(float(r["words"]) for r in group), 4),
                "mean_chars": round(mean(float(r["chars"]) for r in group), 4),
                "mean_utf8_bytes": round(mean(float(r["utf8_bytes"]) for r in group), 4),
                "mean_bytes_per_word": round(
                    mean(float(r["bytes_per_word"]) for r in group), 4
                ),
                "mean_hf_tokens": round(mean(float(r["hf_tokens"]) for r in group), 4)
                if group[0].get("hf_tokens") != ""
                else "",
                "mean_hf_tokens_per_word": round(
                    mean(float(r["hf_tokens_per_word"]) for r in group), 4
                )
                if group[0].get("hf_tokens_per_word") != ""
                else "",
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument(
        "--variants",
        nargs="+",
        default=["bangla", "banglish_clean", "banglish_noisy", "english"],
    )
    parser.add_argument("--hf-tokenizer", action="append", default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_jsonl(args.input)
    tokenizers = load_tokenizers(args.hf_tokenizer)

    rows: list[dict[str, Any]] = []
    for item in items:
        for variant in args.variants:
            text = item.get(variant) or ""
            if not text:
                continue
            base = {
                "id": item["id"],
                "dataset": item["dataset"],
                "task_type": item["task_type"],
                "variant": variant,
                "tokenizer": "unicode_baseline",
                "hf_tokens": "",
                "hf_tokens_per_word": "",
            }
            base.update(simple_metrics(text))
            rows.append(base)

            for tok_name, tokenizer in tokenizers.items():
                metrics = simple_metrics(text)
                token_count = len(tokenizer.encode(text, add_special_tokens=False))
                rows.append(
                    {
                        "id": item["id"],
                        "dataset": item["dataset"],
                        "task_type": item["task_type"],
                        "variant": variant,
                        "tokenizer": tok_name,
                        **metrics,
                        "hf_tokens": token_count,
                        "hf_tokens_per_word": token_count / max(1, metrics["words"]),
                    }
                )

    write_csv(args.out, rows)
    write_csv(args.summary_out, summarize(rows))
    print(f"Wrote {len(rows)} audit rows to {args.out}")
    print(f"Wrote summary to {args.summary_out}")


if __name__ == "__main__":
    main()
