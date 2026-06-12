#!/usr/bin/env python3
"""Build deterministic evaluation subsets from the BEnQA extension pass slice."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/benqa_extended_1000_v1_ai_pass.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "data/slices"
DEFAULT_REPORT = ROOT / "reports/benqa_extension_eval_subsets.md"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def subject(row: dict[str, Any]) -> str:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(metadata.get("subject") or row.get("domain") or "unknown")


def balanced_subject_sample(
    rows: list[dict[str, Any]],
    per_subject: int,
    rng: random.Random,
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[subject(row)].append(row)

    selected: list[dict[str, Any]] = []
    for key in sorted(grouped):
        bucket = grouped[key][:]
        rng.shuffle(bucket)
        if len(bucket) < per_subject:
            raise SystemExit(f"Subject {key} has {len(bucket)} rows, need {per_subject}")
        selected.extend(bucket[:per_subject])
    rng.shuffle(selected)
    return selected


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "rows": len(rows),
        "requests_for_triad": len(rows) * 3,
        "by_subject": dict(sorted(Counter(subject(row) for row in rows).items())),
        "quality_status": dict(sorted(Counter(row.get("quality_status", "") for row in rows).items())),
    }


def write_manifest(
    path: Path,
    input_path: Path,
    rows: list[dict[str, Any]],
    per_subject: int,
    seed: int,
) -> None:
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(input_path),
        "output": repo_path(path),
        "seed": seed,
        "per_subject": per_subject,
        "summary": summarize(rows),
        "notes": [
            "Built from the conservative BEnQA extension pass-only slice.",
            "Balanced by BEnQA subject file.",
            "Use smoke before launching larger Kaggle/API jobs.",
        ],
    }
    path.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_report(
    path: Path,
    input_path: Path,
    smoke_path: Path,
    pilot_path: Path,
    full_path: Path,
    smoke_rows: list[dict[str, Any]],
    pilot_rows: list[dict[str, Any]],
    full_rows: list[dict[str, Any]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# BEnQA Extension Evaluation Subsets",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Purpose",
        "",
        "These subsets turn the BEnQA extension into evaluation-ready units. The",
        "gold-core validation-200 result remains the primary thesis claim; these",
        "subsets are for scale-checking that BEnQA behavior beyond the gold core",
        "points in the same direction.",
        "",
        "## Files",
        "",
        f"- Source pass-only slice: `{repo_path(input_path)}`",
        f"- Smoke subset: `{repo_path(smoke_path)}`",
        f"- Pilot subset: `{repo_path(pilot_path)}`",
        f"- Full pass-only slice: `{repo_path(full_path)}`",
        "",
        "## Subset Sizes",
        "",
        "| Subset | Rows | Triad requests | Purpose |",
        "| --- | ---: | ---: | --- |",
        f"| Smoke | {len(smoke_rows)} | {len(smoke_rows) * 3} | Parser/prompt/runtime smoke. |",
        f"| Pilot | {len(pilot_rows)} | {len(pilot_rows) * 3} | First open-model scale check. |",
        f"| Full pass-only | {len(full_rows)} | {len(full_rows) * 3} | Conservative extension evaluation. |",
        "",
        "## Smoke Subject Balance",
        "",
        "| Subject | Rows |",
        "| --- | ---: |",
    ]
    for key, value in summarize(smoke_rows)["by_subject"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Recommended Launch Order",
            "",
            "1. Run dry-run prompt rendering locally on the smoke subset.",
            "2. Run one Qwen2.5-3B Kaggle smoke on the smoke subset.",
            "3. If parser/runtime is clean, run Qwen2.5-3B on the 130-row pilot.",
            "4. Only then decide whether to run all three Qwen rows on the full",
            "   851-row pass-only extension.",
            "",
            "Do not spend frontier API budget on the full extension unless a specific",
            "paper-review question requires it.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--smoke-per-subject", type=int, default=2)
    parser.add_argument("--pilot-per-subject", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    rows = load_jsonl(args.input)
    smoke_rows = balanced_subject_sample(rows, args.smoke_per_subject, rng)
    pilot_rows = balanced_subject_sample(rows, args.pilot_per_subject, rng)

    smoke_path = args.output_dir / "benqa_extended_1000_v1_ai_pass_smoke26.jsonl"
    pilot_path = args.output_dir / "benqa_extended_1000_v1_ai_pass_pilot130.jsonl"
    write_jsonl(smoke_path, smoke_rows)
    write_jsonl(pilot_path, pilot_rows)
    write_manifest(smoke_path, args.input, smoke_rows, args.smoke_per_subject, args.seed)
    write_manifest(pilot_path, args.input, pilot_rows, args.pilot_per_subject, args.seed)
    write_report(args.report, args.input, smoke_path, pilot_path, args.input, smoke_rows, pilot_rows, rows, args)
    print(f"smoke={len(smoke_rows)} {repo_path(smoke_path)}")
    print(f"pilot={len(pilot_rows)} {repo_path(pilot_path)}")
    print(f"full={len(rows)} {repo_path(args.input)}")
    print(f"report={repo_path(args.report)}")


if __name__ == "__main__":
    main()
