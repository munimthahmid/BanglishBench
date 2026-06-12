#!/usr/bin/env python3
"""Run bnbphoneticparser over generated-Bengali prompt rows."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl"
)
DEFAULT_OUTPUT = (
    ROOT / "results/generated_views/bnbphoneticparser_dev50_benqa_mcq_generated_bn.jsonl"
)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    try:
        from bnbphoneticparser import BanglishToBengali
    except ImportError as exc:
        raise SystemExit(
            "Install bnbphoneticparser==0.1.5 or put its source package on "
            "PYTHONPATH before running this smoke test."
        ) from exc

    args = parse_args()
    parser = BanglishToBengali()
    rows = []
    for prompt in load_jsonl(args.input):
        if prompt.get("target_view") != "generated_bn":
            continue
        rows.append(
            {
                "id": prompt["id"],
                "target_view": prompt["target_view"],
                "generator": "bnbphoneticparser==0.1.5",
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "source_text": prompt.get("source_text", ""),
                "generated_text": parser.parse(str(prompt.get("source_text", ""))),
            }
        )
    write_jsonl(args.output, rows)
    print(f"rows={len(rows)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
