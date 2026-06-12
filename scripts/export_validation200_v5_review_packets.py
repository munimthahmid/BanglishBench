#!/usr/bin/env python3
"""Export Markdown review packets from the validation-200 v5 review queue."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/validation_200_v5_review_queue.csv"
DEFAULT_OUTPUT_DIR = ROOT / "reports/validation200_v5_review_packets"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for csv_row, row in enumerate(rows, start=2):
        row["_csv_row"] = str(csv_row)
    return rows


def load_rank_rows(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def fence(text: str) -> str:
    return "```text\n" + text.rstrip() + "\n```"


def row_status(row: dict[str, str]) -> str:
    label = row.get("quality_label", "").strip()
    if not label:
        return "pending"
    if row.get("reviewed_banglish", "").strip():
        return f"{label}: replacement provided"
    return label


def render_batch(
    rows: list[dict[str, str]],
    start_idx: int,
    batch_no: int,
    batch_count: int,
    input_path: Path,
) -> str:
    parts = [
        f"# Validation-200 v5 Review Packet {batch_no:02d}",
        "",
        f"Source queue: `{input_path.relative_to(ROOT)}`",
        f"Batch: {batch_no}/{batch_count}",
        f"Rows in batch: {len(rows)}",
        "",
        "Fill the source CSV, not this Markdown packet. Use this packet only for",
        "source/context reading while editing `reviewed_banglish`,",
        "`quality_label`, and `review_notes` in the queue.",
        "",
        "Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.",
        "",
    ]
    for offset, row in enumerate(rows, start=0):
        queue_row = row.get("_csv_row", str(start_idx + offset + 2))
        item_no = row.get("_packet_index", str(start_idx + offset + 1))
        impact_lines: list[str] = []
        if row.get("_impact_rank"):
            impact_lines = [
                f"- Impact rank: {row['_impact_rank']}",
                f"- Impact tier: `{row['_impact_tier']}`",
                f"- Impact score: {row['_impact_score']}",
                f"- Split: `{row['_split']}`",
                f"- Impact reasons: {row['_impact_reasons']}",
            ]
        parts.extend(
            [
                f"## {item_no}. {row['id']}",
                "",
                f"- CSV row: {queue_row}",
                f"- Dataset: `{row['dataset']}`",
                f"- Task type: `{row['task_type']}`",
                f"- Answer type: `{row['answer_type']}`",
                f"- Priority: `{row['priority_bucket']}`",
                f"- Replacement count: {row['replacement_count']}",
                f"- Artifact patterns: `{row['artifact_patterns'] or 'none'}`",
                f"- Status: `{row_status(row)}`",
                f"- Qwen2.5 v4 correct: `{row['qwen25_v4_correct']}`",
                f"- Qwen3 v4 correct: `{row['qwen3_v4_correct']}`",
                f"- Suggestion notes: {row['suggestion_notes']}",
                *impact_lines,
                "",
                "Bangla:",
                "",
                fence(row["bangla"]),
                "",
                "English:",
                "",
                fence(row["english"]),
                "",
                "Current Banglish:",
                "",
                fence(row["current_banglish_clean"]),
                "",
                "Auto-suggested Banglish:",
                "",
                fence(row["auto_suggested_banglish_clean"]),
                "",
                "Reviewed Banglish in queue:",
                "",
                fence(row.get("reviewed_banglish", "")),
                "",
                f"Quality label in queue: `{row.get('quality_label', '').strip() or 'blank'}`",
                "",
                f"Review notes in queue: {row.get('review_notes', '').strip() or 'blank'}",
                "",
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def write_index(
    output_dir: Path,
    input_path: Path,
    rows: list[dict[str, str]],
    packet_paths: list[Path],
    batch_size: int,
) -> None:
    status_counts = Counter(row_status(row) for row in rows)
    priority_counts = Counter(row.get("priority_bucket", "") for row in rows)
    dataset_counts = Counter(row.get("dataset", "") for row in rows)
    impact_tier_counts = Counter(
        row.get("_impact_tier", "") for row in rows if row.get("_impact_tier")
    )

    lines = [
        "# Validation-200 v5 Review Packets",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Purpose",
        "",
        "These Markdown packets make the source-aware v5 review queue easier to",
        "read in batches. They are read-only reviewer aids; the authoritative",
        "worksheet remains the CSV queue.",
        "",
    ]
    if impact_tier_counts:
        lines.extend(
            [
                "This packet set includes impact-rank metadata from the v5 review",
                "impact ranking CSV.",
                "",
            ]
        )
    lines.extend(
        [
            "## Inputs",
            "",
            f"- Queue: `{input_path.relative_to(ROOT)}`",
            f"- Batch size: {batch_size}",
            "",
            "## Progress",
            "",
            f"- Rows: {len(rows)}",
            f"- Packets: {len(packet_paths)}",
            "",
            "| Status | Rows |",
            "| --- | ---: |",
        ]
    )
    for key, value in status_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "| Priority bucket | Rows |", "| --- | ---: |"])
    for key, value in priority_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    if impact_tier_counts:
        lines.extend(["", "| Impact tier | Rows |", "| --- | ---: |"])
        for key, value in impact_tier_counts.most_common():
            lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "| Dataset | Rows |", "| --- | ---: |"])
    for key, value in dataset_counts.most_common():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Packet Files", ""])
    for path in packet_paths:
        lines.append(f"- `{path.relative_to(ROOT)}`")

    lines.extend(
        [
            "",
            "## Validation",
            "",
            "After editing the CSV queue, run:",
            "",
            "```bash",
            "python3 scripts/validate_banglish_review_queue.py",
            "```",
            "",
            "Before freezing v5, run:",
            "",
            "```bash",
            "python3 scripts/validate_banglish_review_queue.py --require-complete",
            "```",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument(
        "--rank-csv",
        type=Path,
        help="Optional impact ranking CSV from rank_validation200_v5_review_impact.py.",
    )
    parser.add_argument(
        "--sort-by-rank",
        action="store_true",
        help="Sort packet rows by impact rank. Requires --rank-csv.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be positive")
    rows = load_rows(args.input)
    if args.sort_by_rank and not args.rank_csv:
        raise SystemExit("--sort-by-rank requires --rank-csv")
    if args.rank_csv:
        rank_by_id = load_rank_rows(args.rank_csv)
        for row in rows:
            rank = rank_by_id.get(row["id"], {})
            if not rank:
                continue
            row["_impact_rank"] = rank["impact_rank"]
            row["_impact_score"] = rank["impact_score"]
            row["_impact_tier"] = rank["impact_tier"]
            row["_split"] = rank["split"]
            row["_impact_reasons"] = rank["impact_reasons"]
        if args.sort_by_rank:
            rows.sort(key=lambda row: int(row.get("_impact_rank", "999999")))
    for packet_index, row in enumerate(rows, start=1):
        row["_packet_index"] = str(packet_index)
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    batch_count = math.ceil(len(rows) / args.batch_size)
    packet_paths: list[Path] = []
    for batch_idx in range(batch_count):
        start = batch_idx * args.batch_size
        batch = rows[start : start + args.batch_size]
        packet_path = output_dir / f"batch_{batch_idx + 1:02d}.md"
        packet_path.write_text(
            render_batch(batch, start, batch_idx + 1, batch_count, args.input),
            encoding="utf-8",
        )
        packet_paths.append(packet_path)

    write_index(output_dir, args.input, rows, packet_paths, args.batch_size)
    print(f"rows={len(rows)}")
    print(f"packets={len(packet_paths)}")
    print(f"index={output_dir / 'README.md'}")


if __name__ == "__main__":
    main()
