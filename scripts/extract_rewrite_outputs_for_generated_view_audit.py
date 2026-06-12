#!/usr/bin/env python3
"""Extract rewrite_output fields into generated-view audit JSONL rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_TARGET_VIEW = "generated_en"


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_eval_rows(inputs: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in jsonl_paths(inputs):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("rewrite_output"):
                    rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-view", default=DEFAULT_TARGET_VIEW)
    parser.add_argument("--generator-label", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out = []
    for row in load_eval_rows(args.inputs):
        out.append(
            {
                "id": row["id"],
                "target_view": args.target_view,
                "generated_text": row.get("rewrite_output", ""),
                "generator": args.generator_label or row.get("model", ""),
                "source_variant": row.get("variant", ""),
                "prompt_mode": row.get("prompt_mode", ""),
            }
        )
    if not out:
        raise SystemExit("No rewrite_output rows found.")
    write_jsonl(args.output, out)
    print(f"rows={len(out)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
