#!/usr/bin/env python3
"""Rebuild Banglish fields for an existing JSONL slice while preserving ids."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bn_romanize import romanize_bangla, romanize_noisy


ROOT = Path(__file__).resolve().parents[1]


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


def rebuild(rows: list[dict[str, Any]], method: str, quality_status: str) -> tuple[list[dict[str, Any]], Counter[str]]:
    counts: Counter[str] = Counter()
    rebuilt: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        old_clean = str(item.get("banglish_clean", ""))
        old_noisy = str(item.get("banglish_noisy", ""))
        bangla = str(item.get("bangla", ""))
        new_clean = romanize_bangla(bangla)
        new_noisy = romanize_noisy(bangla)
        item["banglish_clean"] = new_clean
        item["banglish_noisy"] = new_noisy
        item["transliteration_method"] = method
        item["quality_status"] = quality_status
        if old_clean != new_clean:
            counts["changed_clean"] += 1
        if old_noisy != new_noisy:
            counts["changed_noisy"] += 1
        counts[f"dataset:{item.get('dataset', 'unknown')}"] += 1
        rebuilt.append(item)
    return rebuilt, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--method", default="rule_based_bootstrap_v4")
    parser.add_argument("--quality-status", default="auto_romanized_unverified_v4")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    rebuilt, counts = rebuild(rows, args.method, args.quality_status)
    write_jsonl(args.output, rebuilt)

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(args.input),
        "output": repo_path(args.output),
        "items": len(rebuilt),
        "same_item_order": [row.get("id") for row in rows] == [row.get("id") for row in rebuilt],
        "transliteration_method": args.method,
        "quality_status": args.quality_status,
        "counts": dict(sorted(counts.items())),
        "notes": [
            "Only Banglish fields and transliteration metadata are rebuilt.",
            "Item ids, answers, Bangla prompts, English prompts, and source metadata are preserved.",
        ],
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
