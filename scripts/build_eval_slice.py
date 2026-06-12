#!/usr/bin/env python3
"""Build deterministic evaluation slices from the pilot JSONL."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/pilot/items.jsonl"


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


def stratum_key(row: dict[str, Any]) -> str:
    if row["dataset"] == "benqa":
        metadata = row.get("metadata") or {}
        return str(metadata.get("subject") or row.get("domain") or "unknown")
    if row["dataset"] == "banglamath":
        metadata = row.get("metadata") or {}
        return str(metadata.get("grade") or "unknown")
    return str(row.get("domain") or "unknown")


def round_robin_sample(rows: list[dict[str, Any]], count: int, rng: random.Random) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[stratum_key(row)].append(row)

    buckets = {key: value[:] for key, value in sorted(groups.items())}
    for bucket in buckets.values():
        rng.shuffle(bucket)

    sampled: list[dict[str, Any]] = []
    while len(sampled) < count and any(buckets.values()):
        for key in list(buckets):
            if len(sampled) >= count:
                break
            if buckets[key]:
                sampled.append(buckets[key].pop())
    return sampled


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_items": len(rows),
        "counts_by_dataset": dict(sorted(Counter(row["dataset"] for row in rows).items())),
        "counts_by_task_type": dict(sorted(Counter(row["task_type"] for row in rows).items())),
        "english_available": sum(1 for row in rows if row.get("english")),
        "counts_by_dataset_stratum": dict(
            sorted(Counter(f"{row['dataset']}:{stratum_key(row)}" for row in rows).items())
        ),
        "quality_status": dict(sorted(Counter(row.get("quality_status", "") for row in rows).items())),
    }


def parse_counts(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Expected DATASET=COUNT, got {value!r}")
        key, raw_count = value.split("=", 1)
        counts[key.strip()] = int(raw_count)
    return counts


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--counts", nargs="+", default=["benqa=60", "banglamath=40"])
    parser.add_argument("--seed", type=int, default=20260527)
    parser.add_argument("--require-english", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    rows = load_jsonl(args.input)
    counts = parse_counts(args.counts)

    selected: list[dict[str, Any]] = []
    for dataset, count in sorted(counts.items()):
        candidates = [row for row in rows if row["dataset"] == dataset]
        if args.require_english:
            candidates = [row for row in candidates if row.get("english")]
        if len(candidates) < count:
            raise SystemExit(
                f"Need {count} {dataset} rows, but only {len(candidates)} candidates available."
            )
        selected.extend(round_robin_sample(candidates, count, rng))

    rng.shuffle(selected)
    write_jsonl(args.output, selected)

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(args.input),
        "output": repo_path(args.output),
        "seed": args.seed,
        "requested_counts": counts,
        "require_english": args.require_english,
        "summary": summarize(selected),
        "notes": [
            "This slice is deterministic and should be treated as the first fixed validation set.",
            "Banglish variants are still bootstrap romanizations unless quality_status says otherwise.",
        ],
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(selected)} items to {args.output}")
    print(f"Wrote manifest to {manifest_path}")
    print(json.dumps(manifest["summary"], ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
