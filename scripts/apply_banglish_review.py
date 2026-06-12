#!/usr/bin/env python3
"""Apply human-reviewed Banglish corrections to a JSONL slice."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_LABELS = {"ok", "minor_edit", "major_edit", "bad"}


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


def load_reviews(path: Path) -> dict[str, dict[str, str]]:
    reviews: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            item_id = str(row.get("id", "")).strip()
            if not item_id:
                continue
            reviews[item_id] = row
    return reviews


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def apply_reviews(
    items: list[dict[str, Any]],
    reviews: dict[str, dict[str, str]],
    quality_status: str,
    drop_bad: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    counts: Counter[str] = Counter()
    audit_rows: list[dict[str, Any]] = []
    reviewed_ids = set(reviews)
    output: list[dict[str, Any]] = []

    for row in items:
        item = dict(row)
        item_id = str(item.get("id", ""))
        review = reviews.get(item_id)
        old_banglish = str(item.get("banglish_clean", ""))
        new_banglish = old_banglish
        label = ""
        notes = ""
        action = "not_reviewed"
        include_item = True

        if review is None:
            counts["not_reviewed"] += 1
        else:
            counts["review_rows_matched"] += 1
            label = str(review.get("quality_label", "")).strip()
            notes = str(review.get("review_notes", "")).strip()
            replacement = str(review.get("reviewed_banglish", "")).strip()
            if label and label not in ALLOWED_LABELS:
                raise ValueError(f"{item_id}: invalid quality_label {label!r}")
            if replacement and not label:
                raise ValueError(f"{item_id}: reviewed_banglish requires quality_label")
            if label == "ok" and replacement:
                raise ValueError(f"{item_id}: ok rows must not include reviewed_banglish")
            if label in {"minor_edit", "major_edit"} and not replacement:
                raise ValueError(f"{item_id}: {label} requires reviewed_banglish")
            if label == "bad" and replacement:
                raise ValueError(f"{item_id}: bad rows must not include reviewed_banglish")

            if label in {"minor_edit", "major_edit"}:
                new_banglish = replacement
                item["banglish_clean"] = new_banglish
                item["quality_status"] = quality_status
                action = "replaced"
                counts["replaced"] += 1
            elif label == "ok":
                item["quality_status"] = quality_status
                action = "accepted_current"
                counts["accepted_current"] += 1
            elif label == "bad":
                item["quality_status"] = "human_review_bad_banglish"
                if drop_bad:
                    action = "dropped_bad"
                    include_item = False
                    counts["dropped_bad"] += 1
                else:
                    action = "marked_bad"
                    counts["marked_bad"] += 1
            else:
                action = "blank_review"
                counts["blank_review"] += 1

            if action != "blank_review":
                item["banglish_review"] = {
                    "label": label,
                    "notes": notes,
                    "reviewed_banglish_provided": bool(replacement),
                    "source_file": review.get("source_file", ""),
                }

        audit_rows.append(
            {
                "id": item_id,
                "dataset": item.get("dataset", ""),
                "action": action,
                "quality_label": label,
                "old_banglish": old_banglish,
                "new_banglish": new_banglish,
                "changed": old_banglish != new_banglish,
            }
        )
        if include_item:
            output.append(item)

    item_ids = {str(item.get("id", "")) for item in items}
    counts["review_rows_unmatched"] = len(reviewed_ids - item_ids)
    counts["items"] = len(items)
    return output, audit_rows, counts


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path)
    parser.add_argument("--quality-status", default="human_reviewed_banglish_v5")
    parser.add_argument(
        "--drop-bad",
        action="store_true",
        help="Exclude rows labeled bad from the output JSONL instead of keeping them flagged.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = load_jsonl(args.input)
    reviews = load_reviews(args.review)
    output, audit_rows, counts = apply_reviews(
        items, reviews, args.quality_status, args.drop_bad
    )
    write_jsonl(args.output, output)

    audit_output = args.audit_output or args.output.with_suffix(".review_audit.csv")
    write_csv(audit_output, audit_rows)

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(args.input),
        "review": repo_path(args.review),
        "output": repo_path(args.output),
        "audit_output": repo_path(audit_output),
        "drop_bad": args.drop_bad,
        "output_items": len(output),
        "same_item_order": [row.get("id") for row in items] == [row.get("id") for row in output],
        "quality_status": args.quality_status,
        "counts": dict(sorted(counts.items())),
        "notes": [
            "Only banglish_clean, quality_status, and banglish_review metadata may change.",
            "banglish_noisy is not regenerated by this script.",
            "Rows with blank review fields are recorded but left unchanged.",
            "Rows labeled bad are kept and flagged unless --drop-bad is set.",
        ],
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
