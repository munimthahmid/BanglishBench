#!/usr/bin/env python3
"""Freeze the BEnQA extension after human review decisions.

Input decisions may be JSONL exported from the fast dashboard or CSV using the
same field names. The script writes:

- a full 1,000-row human-reviewed audit slice;
- a gold/pass slice containing only accepted or edited rows;
- a markdown report with counts and blocked rows.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl"
DEFAULT_DECISIONS = ROOT / "results/analysis/benqa_extended_1000_v1_human_review_decisions.jsonl"
DEFAULT_FULL_OUTPUT = ROOT / "data/slices/benqa_extended_1000_v1_human_reviewed.jsonl"
DEFAULT_GOLD_OUTPUT = ROOT / "data/slices/benqa_extended_1000_v1_human_gold.jsonl"
DEFAULT_REPORT = ROOT / "reports/benqa_extended_1000_v1_human_review_freeze.md"

ACCEPT_DECISIONS = {"accept", "edited"}
ALL_DECISIONS = {"accept", "edited", "reject", "unsure"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_decisions(path: Path) -> dict[str, dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    else:
        rows = load_jsonl(path)

    decisions: dict[str, dict[str, Any]] = {}
    for row in rows:
        item_id = str(row.get("id") or "").strip()
        if not item_id:
            continue
        decision = str(row.get("decision") or "").strip().lower()
        if not decision:
            continue
        decisions[item_id] = {
            "id": item_id,
            "queue_index": row.get("queue_index", ""),
            "decision": decision,
            "reviewed_banglish": str(row.get("reviewed_banglish") or ""),
            "notes": str(row.get("notes") or ""),
            "reviewed_at_local": str(row.get("reviewed_at_local") or ""),
        }
    return decisions


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


def freeze(
    source_rows: list[dict[str, Any]],
    decisions: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]], Counter[str]]:
    frozen_at = datetime.now(timezone.utc).isoformat()
    full_rows: list[dict[str, Any]] = []
    gold_rows: list[dict[str, Any]] = []
    blocked: list[dict[str, str]] = []
    counts: Counter[str] = Counter()

    seen_ids: set[str] = set()
    for source_index, row in enumerate(source_rows, start=1):
        item_id = str(row.get("id") or "")
        seen_ids.add(item_id)
        decision = decisions.get(item_id)

        if not decision:
            counts["missing"] += 1
            blocked.append({"id": item_id, "reason": "missing_decision"})
            item = dict(row)
            item["human_review_status"] = "human_review_missing_v1"
            full_rows.append(item)
            continue

        label = decision["decision"]
        if label not in ALL_DECISIONS:
            counts["invalid"] += 1
            blocked.append({"id": item_id, "reason": f"invalid_decision:{label}"})
            item = dict(row)
            item["human_review_status"] = "human_review_invalid_v1"
            full_rows.append(item)
            continue

        reviewed_banglish = decision["reviewed_banglish"].strip()
        if label == "accept" and not reviewed_banglish:
            reviewed_banglish = str(row.get("banglish_clean") or "").strip()
        if label == "edited" and not reviewed_banglish:
            counts["invalid"] += 1
            blocked.append({"id": item_id, "reason": "edited_without_banglish"})
            item = dict(row)
            item["human_review_status"] = "human_review_invalid_v1"
            full_rows.append(item)
            continue

        item = dict(row)
        metadata = dict(item.get("metadata") or {})
        metadata["human_review"] = {
            "version": "human_review_v1",
            "reviewed_at_utc": frozen_at,
            "source_decision_queue_index": decision.get("queue_index", ""),
            "decision": label,
            "notes": decision.get("notes", ""),
            "reviewed_at_local": decision.get("reviewed_at_local", ""),
        }
        item["metadata"] = metadata
        item["human_review_status"] = f"human_review_{label}_v1"

        if label in ACCEPT_DECISIONS:
            item["banglish_clean"] = reviewed_banglish
            item["quality_status"] = f"human_review_{label}_v1"
            gold_rows.append(item)
        full_rows.append(item)
        counts[label] += 1

    extra_decisions = sorted(set(decisions) - seen_ids)
    for item_id in extra_decisions:
        counts["extra_decision"] += 1
        blocked.append({"id": item_id, "reason": "decision_id_not_in_source"})

    return full_rows, gold_rows, blocked, counts


def write_report(
    path: Path,
    source: Path,
    decisions_path: Path,
    full_output: Path,
    gold_output: Path,
    source_rows: list[dict[str, Any]],
    full_rows: list[dict[str, Any]],
    gold_rows: list[dict[str, Any]],
    blocked: list[dict[str, str]],
    counts: Counter[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# BEnQA 1,000 Human Review Freeze",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Files",
        "",
        f"- Source: `{repo_path(source)}`",
        f"- Human decisions: `{repo_path(decisions_path)}`",
        f"- Full reviewed audit slice: `{repo_path(full_output)}`",
        f"- Gold/pass slice: `{repo_path(gold_output)}`",
        "",
        "## Counts",
        "",
        f"- Source rows: {len(source_rows)}",
        f"- Full reviewed rows: {len(full_rows)}",
        f"- Gold/pass rows accepted for evaluation: {len(gold_rows)}",
        "",
        "| Decision | Count |",
        "| --- | ---: |",
    ]
    for key in ["accept", "edited", "reject", "unsure", "missing", "invalid", "extra_decision"]:
        if counts.get(key, 0):
            lines.append(f"| {key} | {counts[key]} |")

    lines.extend(["", "## Freeze Status", ""])
    if blocked:
        lines.append("Freeze has blocked rows. Resolve these before calling the extension complete.")
        lines.extend(["", "| ID | Reason |", "| --- | --- |"])
        for row in blocked[:200]:
            lines.append(f"| `{row['id']}` | {row['reason']} |")
        if len(blocked) > 200:
            lines.append(f"| ... | {len(blocked) - 200} more blocked rows omitted |")
    else:
        lines.append("Freeze is complete. Every source row has a valid human decision.")
        lines.append("")
        lines.append("Rows marked `accept` or `edited` are included in the gold/pass output.")
        lines.append("Rows marked `reject` or `unsure` remain in the audit slice but are excluded from the gold/pass output.")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--full-output", type=Path, default=DEFAULT_FULL_OUTPUT)
    parser.add_argument("--gold-output", type=Path, default=DEFAULT_GOLD_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="Write outputs even if some rows are missing/invalid. Without this, blocked rows exit nonzero.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = load_jsonl(args.source)
    decisions = load_decisions(args.decisions)
    full_rows, gold_rows, blocked, counts = freeze(source_rows, decisions)
    write_jsonl(args.full_output, full_rows)
    write_jsonl(args.gold_output, gold_rows)
    write_report(
        args.report,
        args.source,
        args.decisions,
        args.full_output,
        args.gold_output,
        source_rows,
        full_rows,
        gold_rows,
        blocked,
        counts,
    )
    print(f"source_rows={len(source_rows)} gold_rows={len(gold_rows)} blocked={len(blocked)}")
    print(f"full_output={repo_path(args.full_output)}")
    print(f"gold_output={repo_path(args.gold_output)}")
    print(f"report={repo_path(args.report)}")
    if blocked and not args.allow_incomplete:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
