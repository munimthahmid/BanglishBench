#!/usr/bin/env python3
"""Export qualitative recoverable Banglish-miss examples for BEnQA extension runs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("bangla", "banglish_clean", "english")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def compact(text: str, limit: int = 220) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def read_items(path: Path) -> dict[str, dict[str, object]]:
    items: dict[str, dict[str, object]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            items[str(row["id"])] = row
    return items


def read_results(path: Path) -> dict[str, dict[str, dict[str, object]]]:
    by_item: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            row = json.loads(line)
            item_id = str(row["id"])
            variant = str(row["variant"])
            if variant not in VARIANTS:
                continue
            if variant in by_item[item_id]:
                raise ValueError(f"{path}:{line_no} duplicate {item_id} {variant}")
            by_item[item_id][variant] = row
    return by_item


def build_rows(
    items: dict[str, dict[str, object]],
    results: dict[str, dict[str, dict[str, object]]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item_id in sorted(results):
        variants = results[item_id]
        if not all(variant in variants for variant in VARIANTS):
            continue
        banglish_correct = bool(variants["banglish_clean"]["correct"])
        bangla_correct = bool(variants["bangla"]["correct"])
        english_correct = bool(variants["english"]["correct"])
        if banglish_correct or not (bangla_correct or english_correct):
            continue
        item = items.get(item_id, {})
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
        rows.append(
            {
                "id": item_id,
                "answer": str(item.get("answer", variants["banglish_clean"].get("gold", ""))),
                "subject": str(metadata.get("subject", item.get("domain", ""))),
                "domain": str(item.get("domain", "")),
                "bangla_correct": "1" if bangla_correct else "0",
                "banglish_correct": "0",
                "english_correct": "1" if english_correct else "0",
                "bangla_parsed": str(variants["bangla"].get("parsed", "")),
                "banglish_parsed": str(variants["banglish_clean"].get("parsed", "")),
                "english_parsed": str(variants["english"].get("parsed", "")),
                "bangla_prompt": compact(str(item.get("bangla", ""))),
                "banglish_prompt": compact(str(item.get("banglish_clean", ""))),
                "english_prompt": compact(str(item.get("english", ""))),
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "answer",
        "subject",
        "domain",
        "bangla_correct",
        "banglish_correct",
        "english_correct",
        "bangla_parsed",
        "banglish_parsed",
        "english_parsed",
        "bangla_prompt",
        "banglish_prompt",
        "english_prompt",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, str]], report: Path, output: Path, title: str, limit: int) -> None:
    both = sum(1 for row in rows if row["bangla_correct"] == "1" and row["english_correct"] == "1")
    english_only = sum(1 for row in rows if row["bangla_correct"] == "0" and row["english_correct"] == "1")
    bangla_only = sum(1 for row in rows if row["bangla_correct"] == "1" and row["english_correct"] == "0")
    lines = [
        f"# {title}",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Recoverable reviewed-Banglish misses exported: {len(rows)}",
        f"- Bangla and English correct: {both}",
        f"- English-only recovery: {english_only}",
        f"- Bangla-only recovery: {bangla_only}",
        f"- CSV: `{rel(output)}`",
        "",
        "These are qualitative examples, not a separate statistical test. They are",
        "useful for defense slides and error-analysis prose because they show the",
        "same item becoming answerable under another script view.",
        "",
        "## Example Rows",
        "",
        "| ID | Gold | Correct scripts | Parsed answers | Banglish prompt snippet |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows[:limit]:
        correct_scripts = []
        if row["bangla_correct"] == "1":
            correct_scripts.append("Bangla")
        if row["english_correct"] == "1":
            correct_scripts.append("English")
        parsed = (
            f"BN={row['bangla_parsed']}; "
            f"BG={row['banglish_parsed']}; "
            f"EN={row['english_parsed']}"
        )
        snippet = row["banglish_prompt"].replace("|", "\\|")
        lines.append(
            f"| `{row['id']}` | {row['answer']} | {', '.join(correct_scripts)} | {parsed} | {snippet} |"
        )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--limit", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items_path = args.items if args.items.is_absolute() else ROOT / args.items
    results_path = args.results if args.results.is_absolute() else ROOT / args.results
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    rows = build_rows(read_items(items_path), read_results(results_path))
    write_csv(rows, output_path)
    write_report(rows, report_path, output_path, args.title, args.limit)
    print(f"recoverable={len(rows)} output={output_path} report={report_path}")


if __name__ == "__main__":
    main()
