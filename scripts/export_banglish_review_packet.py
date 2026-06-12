#!/usr/bin/env python3
"""Export a human-readable Banglish review packet from the priority CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fence(text: str) -> str:
    return f"```text\n{text.strip()}\n```"


def render(rows: list[dict[str, str]], limit: int) -> str:
    if limit:
        rows = rows[:limit]

    parts = [
        "# Banglish Human Review Packet v2",
        "",
        "Fill `Reviewed Banglish`, `Quality Label`, and `Review Notes` for each item.",
        "Quality labels: `ok`, `minor_edit`, `major_edit`, `bad`.",
        "",
        f"Items in packet: {len(rows)}",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        parts.extend(
            [
                f"## {idx}. {row['id']}",
                "",
                f"- Source: `{row['source_file']}`",
                f"- Dataset: `{row['dataset']}`",
                f"- Task type: `{row['task_type']}`",
                f"- Patterns: `{row['patterns']}`",
                "",
                "Bangla:",
                "",
                fence(row["bangla"]),
                "",
                "Current Banglish:",
                "",
                fence(row["banglish_clean"]),
                "",
                "English reference:",
                "",
                fence(row["english"]),
                "",
                "Reviewed Banglish:",
                "",
                "```text",
                "",
                "```",
                "",
                "Quality Label:",
                "",
                "Review Notes:",
                "",
            ]
        )
    return "\n".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(rows, args.limit), encoding="utf-8")
    print(f"rows={len(rows)}")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
