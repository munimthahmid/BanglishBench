#!/usr/bin/env python3
"""Build a publication-scale BEnQA-only extension slice.

The frozen validation-200 v5 slice remains the reviewed gold core. This script
creates a larger BEnQA extension from the cached upstream BEnQA CSV files,
excluding any source rows already present in the gold core.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bn_romanize import romanize_bangla, romanize_noisy


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENQA_DIR = ROOT / "literature/code/BEnQA/data/BEnQA"
DEFAULT_EXCLUDE = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_OUTPUT = ROOT / "data/slices/benqa_extended_1000_v1.jsonl"
DEFAULT_REPORT = ROOT / "reports/benqa_extended_1000_v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
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


def clean(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(value.replace("\r\n", "\n").replace("\r", "\n").split())


def format_mcq(question: str, choices: dict[str, str]) -> str:
    lines = [question.strip()]
    for key in ("A", "B", "C", "D"):
        lines.append(f"{key}. {choices[key].strip()}")
    lines.append("Answer with only A, B, C, or D.")
    return "\n".join(lines)


def source_item_id(source_name: str, row_idx: int) -> str:
    return f"benqa_{source_name}_{row_idx:04d}"


def source_key(source_file: str, source_row: int | str) -> str:
    return f"{source_file}:{int(source_row)}"


def excluded_source_keys(paths: list[Path]) -> set[str]:
    keys: set[str] = set()
    for path in paths:
        for row in load_jsonl(path):
            if row.get("dataset") != "benqa":
                continue
            source_file = str(row.get("source_file") or "")
            source_row = row.get("source_row")
            if source_file and source_row:
                keys.add(source_key(source_file, source_row))
    return keys


def round_robin_sample(
    grouped: dict[str, list[dict[str, Any]]],
    count: int,
    rng: random.Random,
) -> list[dict[str, Any]]:
    buckets = {key: rows[:] for key, rows in sorted(grouped.items())}
    for rows in buckets.values():
        rng.shuffle(rows)

    sampled: list[dict[str, Any]] = []
    while len(sampled) < count and any(buckets.values()):
        for key in list(buckets):
            if len(sampled) >= count:
                break
            if buckets[key]:
                sampled.append(buckets[key].pop())
    return sampled


def build_pool(benqa_dir: Path, excluded_keys: set[str]) -> tuple[list[dict[str, Any]], Counter[str]]:
    pool: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for csv_path in sorted(benqa_dir.glob("*.csv")):
        source_name = csv_path.stem
        relative_source = str(csv_path.relative_to(ROOT))
        grade = source_name.split("-", 1)[0]
        subject = source_name.split("-", 1)[1] if "-" in source_name else source_name
        for row_idx, row in enumerate(read_csv(csv_path), start=1):
            counts["source_rows_seen"] += 1
            if source_key(relative_source, row_idx) in excluded_keys:
                counts["excluded_gold_core"] += 1
                continue

            answer = clean(row.get("Correct Answer")).upper()[:1]
            if answer not in {"A", "B", "C", "D"}:
                counts["skipped_invalid_answer"] += 1
                continue

            en_question = clean(row.get("English Question"))
            bn_question = clean(row.get("Bengali Question"))
            en_choices = {key: clean(row.get(key)) for key in ("A", "B", "C", "D")}
            bn_choices = {
                "A": clean(row.get("A Bn")),
                "B": clean(row.get("B Bn")),
                "C": clean(row.get("C Bn")),
                "D": clean(row.get("D Bn")),
            }
            if not en_question or not bn_question:
                counts["skipped_missing_question"] += 1
                continue
            if not all(en_choices.values()) or not all(bn_choices.values()):
                counts["skipped_missing_choice"] += 1
                continue

            bangla = format_mcq(bn_question, bn_choices)
            english = format_mcq(en_question, en_choices)
            original_id = source_item_id(source_name, row_idx)
            item = {
                "id": f"benqa_ext_{source_name}_{row_idx:04d}",
                "dataset": "benqa",
                "task_type": "mcq",
                "answer_type": "choice",
                "answer": answer,
                "bangla": bangla,
                "banglish_clean": romanize_bangla(bangla),
                "banglish_noisy": romanize_noisy(bangla),
                "english": english,
                "english_available": True,
                "difficulty": "unknown",
                "domain": subject.lower(),
                "source_file": relative_source,
                "source_row": row_idx,
                "source_url": "https://github.com/sheikhshafayat/BEnQA",
                "license_notes": "See upstream BEnQA repository.",
                "quality_status": "auto_romanized_unverified_extended_v1",
                "transliteration_method": "rule_based_bootstrap_v4",
                "metadata": {
                    "extension": "benqa_extended_1000_v1",
                    "grade": grade,
                    "subject": subject,
                    "source_item_id": original_id,
                    "choices_bangla": bn_choices,
                    "choices_english": en_choices,
                },
            }
            pool.append(item)
            counts[f"pool_subject:{source_name}"] += 1
    counts["pool_items"] = len(pool)
    return pool, counts


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_items": len(rows),
        "counts_by_dataset": dict(sorted(Counter(row["dataset"] for row in rows).items())),
        "counts_by_grade": dict(sorted(Counter(row["metadata"]["grade"] for row in rows).items())),
        "counts_by_subject": dict(sorted(Counter(row["metadata"]["subject"] for row in rows).items())),
        "quality_status": dict(sorted(Counter(row["quality_status"] for row in rows).items())),
        "english_available": sum(1 for row in rows if row.get("english_available")),
    }


def write_manifest(
    output: Path,
    rows: list[dict[str, Any]],
    pool_counts: Counter[str],
    args: argparse.Namespace,
) -> None:
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "output": repo_path(output),
        "report": repo_path(args.report),
        "benqa_dir": repo_path(args.benqa_dir),
        "excluded_slices": [repo_path(path) for path in args.exclude],
        "seed": args.seed,
        "requested_count": args.count,
        "pool_counts": dict(sorted(pool_counts.items())),
        "summary": summarize(rows),
        "notes": [
            "This is an extended BEnQA-only publication-scale layer, not a replacement for validation-200 v5.",
            "Rows already present in the frozen validation-200 v5 BEnQA core are excluded by source file and row.",
            "Banglish fields are rule-based bootstrap romanizations until the AI-assisted review artifacts are applied.",
            "Do not describe this layer as human-reviewed unless a separate human review is completed and logged.",
        ],
    }
    manifest_path = output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_report(
    path: Path,
    output: Path,
    rows: list[dict[str, Any]],
    pool_counts: Counter[str],
    args: argparse.Namespace,
) -> None:
    summary = summarize(rows)
    lines = [
        "# BEnQA Extended 1000 V1",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Purpose",
        "",
        "This artifact adds a publication-scale BEnQA-only extension layer while",
        "keeping `validation_200_v5` as the frozen reviewed gold core. The extension",
        "is intended for scale and robustness checks, not as a replacement for the",
        "deeply audited 200-item paired benchmark.",
        "",
        "## Files",
        "",
        f"- Extended slice: `{repo_path(output)}`",
        f"- Manifest: `{repo_path(output.with_suffix('.manifest.json'))}`",
        "",
        "## Construction",
        "",
        f"- Upstream BEnQA source rows seen: {pool_counts['source_rows_seen']}.",
        f"- Frozen-core BEnQA rows excluded: {pool_counts['excluded_gold_core']}.",
        f"- Candidate pool after required-field filtering: {pool_counts['pool_items']}.",
        f"- Selected rows: {summary['total_items']}.",
        f"- Seed: {args.seed}.",
        "- Sampling: deterministic round-robin by BEnQA subject file.",
        "- Banglish generation: local rule-based bootstrap romanizer v4.",
        "",
        "## Selected Composition",
        "",
        "| Group | Count |",
        "| --- | ---: |",
    ]
    for subject, count in summary["counts_by_subject"].items():
        lines.append(f"| {subject} | {count} |")

    lines.extend(
        [
            "",
            "## Review Status",
            "",
            "This slice is not human-reviewed. It should be paired with the",
            "AI-assisted review/triage output before any thesis or paper claim uses",
            "it as quality-controlled evidence. Any future human review must be",
            "logged separately from AI-assisted review.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benqa-dir", type=Path, default=DEFAULT_BENQA_DIR)
    parser.add_argument("--exclude", type=Path, nargs="*", default=[DEFAULT_EXCLUDE])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260605)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    excluded_keys = excluded_source_keys(args.exclude)
    pool, pool_counts = build_pool(args.benqa_dir, excluded_keys)
    if len(pool) < args.count:
        raise SystemExit(f"Need {args.count} rows but only {len(pool)} candidates are available")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in pool:
        grouped[str(row["metadata"]["subject"])].append(row)
    selected = round_robin_sample(grouped, args.count, rng)
    rng.shuffle(selected)
    write_jsonl(args.output, selected)
    write_manifest(args.output, selected, pool_counts, args)
    write_report(args.report, args.output, selected, pool_counts, args)
    print(f"pool={len(pool)}")
    print(f"selected={len(selected)}")
    print(f"output={repo_path(args.output)}")
    print(f"report={repo_path(args.report)}")


if __name__ == "__main__":
    main()
