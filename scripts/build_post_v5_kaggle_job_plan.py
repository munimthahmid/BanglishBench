#!/usr/bin/env python3
"""Build a gated post-v5 Kaggle rerun job plan without launching jobs."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def readiness_status(path: Path) -> tuple[bool, list[str]]:
    rows = read_csv(path)
    failed = [f"{row['gate']}: {row['detail']}" for row in rows if row["status"] != "pass"]
    return not failed, failed


def packager_command(
    *,
    account: int,
    model: str,
    job_name: str,
    kernel_slug: str,
    title: str,
    output_name: str,
    load_in_8bit: bool = False,
    disable_thinking: bool = False,
) -> str:
    parts = [
        "python3",
        "scripts/prepare_kaggle_model_run.py",
        "--account",
        str(account),
        "--model",
        model,
        "--dataset-slug",
        "validation-200-v5-assets",
        "--dataset-title",
        '"Validation 200 v5 assets"',
        "--items-path",
        "data/slices/validation_200_v5.jsonl",
        "--assets-job-name",
        f"validation_200_v5_assets_account{account}",
        "--job-name",
        job_name,
        "--kernel-slug",
        kernel_slug,
        "--title",
        f'"{title}"',
        "--output-name",
        output_name,
        "--limit",
        "0",
        "--variants",
        "banglish_clean",
        "--max-new-tokens",
        "128",
    ]
    if load_in_8bit:
        parts.append("--load-in-8bit")
    if disable_thinking:
        parts.append("--disable-thinking")
    return " ".join(parts)


def planned_jobs(ready: bool) -> list[dict[str, str]]:
    blocked_status = "ready_to_prepare" if ready else "blocked_by_readiness"
    jobs = [
        {
            "priority": "1",
            "run_id": "qwen25_3b_validation200_v5_banglish",
            "model": "Qwen/Qwen2.5-3B-Instruct",
            "account": "1",
            "variant": "banglish_clean",
            "slice": "validation_200_v5_full200",
            "quantization": "none",
            "condition": "required_after_readiness",
            "status": blocked_status,
            "command": packager_command(
                account=1,
                model="Qwen/Qwen2.5-3B-Instruct",
                job_name="qwen25_3b_validation200_v5_banglish",
                kernel_slug="qwen25-3b-validation200-v5-banglish",
                title="Qwen2.5 3B validation-200 v5 Banglish",
                output_name="qwen2_5_3b_validation200_v5_banglish",
            ),
        },
        {
            "priority": "2",
            "run_id": "qwen3_4b_validation200_v5_banglish",
            "model": "Qwen/Qwen3-4B-Instruct-2507",
            "account": "1",
            "variant": "banglish_clean",
            "slice": "validation_200_v5_full200",
            "quantization": "none",
            "condition": "required_after_readiness",
            "status": blocked_status,
            "command": packager_command(
                account=1,
                model="Qwen/Qwen3-4B-Instruct-2507",
                job_name="qwen3_4b_validation200_v5_banglish",
                kernel_slug="qwen3-4b-validation200-v5-banglish",
                title="Qwen3 4B validation-200 v5 Banglish",
                output_name="qwen3_4b_validation200_v5_banglish",
                disable_thinking=True,
            ),
        },
        {
            "priority": "3",
            "run_id": "qwen25_7b_8bit_validation200_v5_banglish",
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "account": "1",
            "variant": "banglish_clean",
            "slice": "validation_200_v5_full200_or_test150",
            "quantization": "8-bit",
            "condition": "conditional_if_v5_changes_main_table_or_7b_remains_primary",
            "status": "conditional_manual_decision" if ready else "blocked_by_readiness",
            "command": packager_command(
                account=1,
                model="Qwen/Qwen2.5-7B-Instruct",
                job_name="qwen25_7b_8bit_validation200_v5_banglish",
                kernel_slug="qwen25-7b-8bit-validation200-v5-banglish",
                title="Qwen2.5 7B 8-bit validation-200 v5 Banglish",
                output_name="qwen2_5_7b_8bit_validation200_v5_banglish",
                load_in_8bit=True,
            ),
        },
    ]
    return jobs


def write_jobs_csv(path: Path, jobs: list[dict[str, str]]) -> None:
    fieldnames = [
        "priority",
        "run_id",
        "model",
        "account",
        "variant",
        "slice",
        "quantization",
        "condition",
        "status",
        "command",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)


def build_report(ready: bool, failed: list[str], jobs: list[dict[str, str]]) -> str:
    lines = [
        "# Post-v5 Kaggle Job Plan",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        f"Readiness status: `{'ready' if ready else 'not_ready'}`",
        "",
        "Compute budget companion: `reports/post_v5_compute_budget.md`",
        "",
    ]
    if failed:
        lines.append("Do not prepare or launch these jobs yet. Blocking reasons:")
        lines.append("")
        for reason in failed:
            lines.append(f"- `{reason}`")
        lines.append("")
    else:
        lines.append(
            "The required v5 review and freeze gates pass. Prepare jobs in priority order."
        )
        lines.append("")

    lines.extend(
        [
            "## Planned Jobs",
            "",
            "| Priority | Run id | Model | Variant | Quantization | Status | Condition |",
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for job in jobs:
        lines.append(
            "| "
            f"{job['priority']} | `{job['run_id']}` | `{job['model']}` | "
            f"`{job['variant']}` | `{job['quantization']}` | "
            f"`{job['status']}` | `{job['condition']}` |"
        )

    lines.extend(["", "## Packaging Commands", ""])
    for job in jobs:
        lines.append(f"### {job['priority']}. `{job['run_id']}`")
        lines.append("")
        lines.append(f"Status: `{job['status']}`")
        lines.append("")
        lines.append("```bash")
        lines.append(job["command"])
        lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## Launch Rule",
            "",
            "Only run a packaging command after:",
            "",
            "1. `python3 scripts/validate_banglish_review_queue.py --require-complete` passes.",
            "2. `scripts/apply_banglish_review.py` creates `data/slices/validation_200_v5.jsonl`.",
            "3. `scripts/audit_banglish_artifacts.py` creates the v5 artifact audit files.",
            "4. `python3 scripts/check_post_v5_rerun_readiness.py` reports `ready`.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--readiness",
        type=Path,
        default=ROOT / "results/analysis/post_v5_rerun_readiness.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/post_v5_kaggle_job_plan.md",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/post_v5_kaggle_job_plan.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ready, failed = readiness_status(args.readiness)
    jobs = planned_jobs(ready)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(ready, failed, jobs), encoding="utf-8")
    write_jobs_csv(args.csv_output, jobs)
    print(f"wrote={args.output}")
    print(f"wrote={args.csv_output}")
    print(f"ready={ready} jobs={len(jobs)}")


if __name__ == "__main__":
    main()
