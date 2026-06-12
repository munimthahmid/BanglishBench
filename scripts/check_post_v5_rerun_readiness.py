#!/usr/bin/env python3
"""Check whether validation-200 v5 post-review reruns are ready to launch."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_LABELS = {"ok", "minor_edit", "major_edit", "bad"}


REQUIRED_FREEZE_ARTIFACTS = [
    ROOT / "data/slices/validation_200_v5.jsonl",
    ROOT / "results/analysis/validation200_v5_banglish_review_audit.csv",
    ROOT / "results/analysis/validation200_v5_banglish_artifact_summary.csv",
    ROOT / "results/analysis/validation200_v5_banglish_artifact_examples.csv",
]


REQUIRED_PROTOCOL_ARTIFACTS = [
    ROOT / "reports/v5_analysis_preregistration.md",
    ROOT / "reports/post_v5_rerun_protocol.md",
    ROOT / "reports/reproducibility_release_checklist.md",
    ROOT / "reports/validation200_v5_review_session_log.md",
    ROOT / "reports/validation200_v5_review_session_plan.md",
    ROOT / "results/analysis/validation200_v5_review_session_plan.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def queue_status(queue: Path) -> tuple[Counter[str], list[str]]:
    rows = read_csv(queue)
    counts: Counter[str] = Counter()
    issues: list[str] = []
    for row in rows:
        label = row.get("quality_label", "").strip()
        if not label:
            counts["pending"] += 1
            continue
        if label not in VALID_LABELS:
            counts["invalid_label"] += 1
            issues.append(f"{row['id']}: invalid label {label!r}")
            continue
        counts[label] += 1
        replacement = row.get("reviewed_banglish", "").strip()
        notes = row.get("review_notes", "").strip()
        if label in {"minor_edit", "major_edit"} and not replacement:
            counts["missing_replacement"] += 1
            issues.append(f"{row['id']}: {label} without reviewed_banglish")
        if label in {"ok", "bad"} and replacement:
            counts["unexpected_replacement"] += 1
            issues.append(f"{row['id']}: {label} should not have reviewed_banglish")
        if label == "bad" and not notes:
            counts["bad_without_review_notes"] += 1
            issues.append(f"{row['id']}: bad without review_notes")
    counts["total"] = len(rows)
    return counts, issues


def status_rows(queue: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    counts, issues = queue_status(queue)
    rows.append(
        {
            "gate": "review_queue_complete",
            "status": "pass" if counts["pending"] == 0 else "fail",
            "detail": f"pending={counts['pending']} total={counts['total']}",
        }
    )
    rows.append(
        {
            "gate": "review_queue_labels_valid",
            "status": "pass" if not issues else "fail",
            "detail": f"issues={len(issues)}",
        }
    )
    for artifact in REQUIRED_FREEZE_ARTIFACTS:
        rows.append(
            {
                "gate": "freeze_artifact_exists",
                "status": "pass" if artifact.exists() else "fail",
                "detail": str(artifact.relative_to(ROOT)),
            }
        )
    for artifact in REQUIRED_PROTOCOL_ARTIFACTS:
        rows.append(
            {
                "gate": "protocol_artifact_exists",
                "status": "pass" if artifact.exists() else "fail",
                "detail": str(artifact.relative_to(ROOT)),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["gate", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def build_report(rows: list[dict[str, str]], queue: Path) -> str:
    failed = [row for row in rows if row["status"] != "pass"]
    ready = not failed
    queue_counts, queue_issues = queue_status(queue)
    lines = [
        "# Post-v5 Rerun Readiness",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report checks whether validation-200 v5 is ready for the minimal",
        "post-review clean-Banglish Kaggle reruns.",
        "",
        f"Overall status: `{'ready' if ready else 'not_ready'}`",
        "",
        "## Review Queue",
        "",
        "| Label | Rows |",
        "| --- | ---: |",
    ]
    for key in [
        "total",
        "pending",
        "ok",
        "minor_edit",
        "major_edit",
        "bad",
        "invalid_label",
        "missing_replacement",
        "unexpected_replacement",
        "bad_without_review_notes",
    ]:
        lines.append(f"| `{key}` | {queue_counts.get(key, 0)} |")
    lines.append("")
    if queue_issues:
        lines.append("Queue issues:")
        lines.append("")
        for issue in queue_issues[:20]:
            lines.append(f"- {issue}")
        if len(queue_issues) > 20:
            lines.append(f"- ... {len(queue_issues) - 20} more")
        lines.append("")

    lines.extend(
        [
            "## Gates",
            "",
            "| Gate | Status | Detail |",
            "| --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(f"| `{row['gate']}` | `{row['status']}` | `{row['detail']}` |")
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    if ready:
        lines.append("Post-v5 reruns may be packaged according to `reports/post_v5_rerun_protocol.md`.")
    else:
        lines.append("Do not launch post-v5 Kaggle reruns yet.")
        lines.append("")
        lines.append("Blocking reasons:")
        lines.append("")
        for row in failed:
            lines.append(f"- `{row['gate']}`: {row['detail']}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queue",
        type=Path,
        default=ROOT / "data/slices/validation_200_v5_review_queue.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/post_v5_rerun_readiness.md",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/post_v5_rerun_readiness.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = status_rows(args.queue)
    report = build_report(rows, args.queue)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    write_csv(args.csv_output, rows)
    print(f"wrote={args.output}")
    print(f"wrote={args.csv_output}")


if __name__ == "__main__":
    main()
