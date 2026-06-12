#!/usr/bin/env python3
"""Split an existing evaluation JSONL into deterministic stratified subsets."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def stratum_key(row: dict[str, Any]) -> str:
    metadata = row.get("metadata") or {}
    if row.get("dataset") == "benqa":
        return f"benqa:{metadata.get('subject') or row.get('domain') or 'unknown'}"
    if row.get("dataset") == "banglamath":
        return f"banglamath:{metadata.get('grade') or 'unknown'}"
    return f"{row.get('dataset', 'unknown')}:{row.get('domain', 'unknown')}"


def proportional_counts(rows: list[dict[str, Any]], dev_size: int) -> dict[str, int]:
    counts = Counter(row["dataset"] for row in rows)
    raw = {dataset: dev_size * count / len(rows) for dataset, count in counts.items()}
    out = {dataset: int(value) for dataset, value in raw.items()}
    remaining = dev_size - sum(out.values())
    fractions = sorted(
        ((raw[dataset] - out[dataset], dataset) for dataset in counts), reverse=True
    )
    for _, dataset in fractions[:remaining]:
        out[dataset] += 1
    return out


def round_robin_sample(rows: list[dict[str, Any]], count: int, rng: random.Random) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[stratum_key(row)].append(row)
    buckets = {key: value[:] for key, value in sorted(groups.items())}
    for bucket in buckets.values():
        rng.shuffle(bucket)

    selected: list[dict[str, Any]] = []
    while len(selected) < count and any(buckets.values()):
        for key in list(buckets):
            if len(selected) >= count:
                break
            if buckets[key]:
                selected.append(buckets[key].pop())
    return selected


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "items": len(rows),
        "counts_by_dataset": dict(sorted(Counter(row["dataset"] for row in rows).items())),
        "counts_by_stratum": dict(sorted(Counter(stratum_key(row) for row in rows).items())),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--dev-output", type=Path, required=True)
    parser.add_argument("--test-output", type=Path, required=True)
    parser.add_argument("--dev-size", type=int, required=True)
    parser.add_argument("--seed", type=int, default=20260528)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(args.input)
    if args.dev_size <= 0 or args.dev_size >= len(rows):
        raise SystemExit("--dev-size must be between 1 and len(input)-1")
    rng = random.Random(args.seed)
    dataset_counts = proportional_counts(rows, args.dev_size)

    dev: list[dict[str, Any]] = []
    for dataset, count in sorted(dataset_counts.items()):
        candidates = [row for row in rows if row["dataset"] == dataset]
        dev.extend(round_robin_sample(candidates, count, rng))
    dev_ids = {row["id"] for row in dev}
    test = [row for row in rows if row["id"] not in dev_ids]
    rng.shuffle(dev)
    rng.shuffle(test)

    write_jsonl(args.dev_output, dev)
    write_jsonl(args.test_output, test)
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(args.input),
        "dev_output": repo_path(args.dev_output),
        "test_output": repo_path(args.test_output),
        "seed": args.seed,
        "dev": summarize(dev),
        "test": summarize(test),
    }
    manifest_path = args.dev_output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
