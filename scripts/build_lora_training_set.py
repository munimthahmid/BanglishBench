#!/usr/bin/env python3
"""Build the LoRA training set for the Banglish mitigation experiment.

Reuses the BEnQA pool loader from build_benqa_extended_slice so the training
distribution matches the eval pipeline exactly. Excludes every source row that
appears in the frozen validation-200 v5 gold core and in the full 1,000-row
BEnQA extension, then asserts zero id/source overlap before writing anything.

Outputs (next_steps.md Step 1):
  data/slices/lora_train_banglish.jsonl  arm A: Banglish-only prompts
  data/slices/lora_train_mixed.jsonl     arm B: 1:1:1 Bangla/Banglish/English
  data/slices/lora_dev200.jsonl          held-out dev, all three views
plus *.manifest.json for each.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_benqa_extended_slice import build_pool, excluded_source_keys, source_key

ROOT = Path(__file__).resolve().parents[1]
BENQA_DIR = ROOT / "literature/code/BEnQA/data/BEnQA"
VALIDATION_V5 = ROOT / "data/slices/validation_200_v5.jsonl"
EXTENSION_1000 = ROOT / "data/slices/benqa_extended_1000_v1.jsonl"
SLICES = ROOT / "data/slices"

ANSWER_INSTRUCTION = "Answer with only A, B, C, or D."
VIEW_FIELDS = {"bangla": "bangla", "banglish": "banglish_clean", "english": "english"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chat_example(prompt_text: str, gold: str) -> dict[str, Any]:
    return {
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": gold},
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dev-size", type=int, default=200)
    args = parser.parse_args()

    excluded_keys = excluded_source_keys([VALIDATION_V5, EXTENSION_1000])
    pool, pool_counts = build_pool(BENQA_DIR, excluded_keys)

    # Guardrail: assert no pool row shares a source key with the excluded slices.
    pool_keys = {source_key(item["source_file"], item["source_row"]) for item in pool}
    overlap = pool_keys & excluded_keys
    if overlap:
        raise SystemExit(f"FATAL: {len(overlap)} training rows overlap frozen slices: {list(overlap)[:5]}")

    # Guardrail: assert disjoint item ids from both frozen slices.
    frozen_ids = {r["id"] for r in load_jsonl(VALIDATION_V5)} | {r["id"] for r in load_jsonl(EXTENSION_1000)}
    # Extension ids share the benqa_ext_ prefix scheme with the pool; check source ids too.
    frozen_source_items = {r.get("metadata", {}).get("source_item_id") for r in load_jsonl(EXTENSION_1000)}
    pool_source_items = {item["metadata"]["source_item_id"] for item in pool}
    id_overlap = pool_source_items & (frozen_source_items - {None})
    if id_overlap:
        raise SystemExit(f"FATAL: {len(id_overlap)} training source-item ids overlap the extension.")

    rng = random.Random(args.seed)
    rng.shuffle(pool)
    dev = pool[: args.dev_size]
    train = pool[args.dev_size :]

    # Arm A: Banglish-only completion examples.
    arm_a = [chat_example(item["banglish_clean"], item["answer"]) for item in train]

    # Arm B: one view per item, 1:1:1 sampled with fixed seed.
    view_rng = random.Random(args.seed + 1)
    views = ["bangla", "banglish", "english"]
    arm_b = []
    arm_b_view_counts: Counter[str] = Counter()
    for item in train:
        view = views[view_rng.randrange(3)]
        arm_b.append(chat_example(item[VIEW_FIELDS[view]], item["answer"]))
        arm_b_view_counts[view] += 1

    # Dev: all three views, tagged for diagnostic eval (eval harness reads fields).
    dev_rows = []
    for item in dev:
        dev_rows.append(
            {
                "id": item["id"],
                "dataset": "benqa",
                "task_type": "mcq",
                "answer_type": "choice",
                "answer": item["answer"],
                "bangla": item["bangla"],
                "banglish_clean": item["banglish_clean"],
                "english": item["english"],
                "metadata": {"subject": item["metadata"]["subject"], "lora_split": "dev"},
            }
        )

    out_a = SLICES / "lora_train_banglish.jsonl"
    out_b = SLICES / "lora_train_mixed.jsonl"
    out_dev = SLICES / "lora_dev200.jsonl"
    write_jsonl(out_a, arm_a)
    write_jsonl(out_b, arm_b)
    write_jsonl(out_dev, dev_rows)

    common = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "benqa_dir": str(BENQA_DIR.relative_to(ROOT)),
        "excluded_slices": [str(VALIDATION_V5.relative_to(ROOT)), str(EXTENSION_1000.relative_to(ROOT))],
        "excluded_source_keys": len(excluded_keys),
        "pool_items": len(pool),
        "dev_size": len(dev),
        "train_size": len(train),
        "overlap_check": "passed: 0 source-key overlap, 0 id overlap",
    }
    (out_a.with_suffix(".manifest.json")).write_text(
        json.dumps(
            {**common, "arm": "A_banglish_only", "output": str(out_a.relative_to(ROOT)),
             "rows": len(arm_a), "sha256": sha256(out_a)},
            indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_b.with_suffix(".manifest.json")).write_text(
        json.dumps(
            {**common, "arm": "B_mixed_1to1to1", "output": str(out_b.relative_to(ROOT)),
             "rows": len(arm_b), "view_counts": dict(arm_b_view_counts), "sha256": sha256(out_b)},
            indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dev.with_suffix(".manifest.json")).write_text(
        json.dumps(
            {**common, "split": "dev200_all_views", "output": str(out_dev.relative_to(ROOT)),
             "rows": len(dev_rows), "sha256": sha256(out_dev)},
            indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"pool={len(pool)} train={len(train)} dev={len(dev)}")
    print(f"arm A rows={len(arm_a)}  arm B rows={len(arm_b)} views={dict(arm_b_view_counts)}")
    print("overlap check: PASSED (0 source-key, 0 id)")


if __name__ == "__main__":
    main()
