#!/usr/bin/env python3
"""Build a conservative compute budget for gated post-v5 Kaggle reruns."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KAGGLE_ACCOUNTS = 4
HOURS_PER_ACCOUNT = 30.0


@dataclass(frozen=True)
class RuntimeEstimate:
    observed_wall_seconds: float
    observed_outputs: int
    planned_outputs: int
    setup_buffer_minutes: float
    contingency_multiplier: float
    evidence: str

    @property
    def estimated_hours(self) -> float:
        scaled_seconds = self.observed_wall_seconds * (self.planned_outputs / self.observed_outputs)
        return (scaled_seconds / 3600.0) + (self.setup_buffer_minutes / 60.0)

    @property
    def conservative_hours(self) -> float:
        return self.estimated_hours * self.contingency_multiplier


ESTIMATES = {
    "qwen25_3b_validation200_v5_banglish": RuntimeEstimate(
        observed_wall_seconds=334.2,
        observed_outputs=200,
        planned_outputs=200,
        setup_buffer_minutes=5.0,
        contingency_multiplier=2.0,
        evidence="qwen2_5_3b_validation200_v4_banglish Kaggle log ended at about 334 seconds",
    ),
    "qwen3_4b_validation200_v5_banglish": RuntimeEstimate(
        observed_wall_seconds=672.2,
        observed_outputs=200,
        planned_outputs=200,
        setup_buffer_minutes=5.0,
        contingency_multiplier=2.0,
        evidence="qwen3_4b_validation200_v4_banglish Kaggle log ended at about 672 seconds",
    ),
    "qwen25_7b_8bit_validation200_v5_banglish": RuntimeEstimate(
        observed_wall_seconds=1143.7,
        observed_outputs=450,
        planned_outputs=200,
        setup_buffer_minutes=10.0,
        contingency_multiplier=2.0,
        evidence="qwen25_7b_8bit_validation200_v4_test150 triad log ended at about 1144 seconds",
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def budget_rows(job_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for job in job_rows:
        estimate = ESTIMATES[job["run_id"]]
        rows.append(
            {
                "priority": job["priority"],
                "run_id": job["run_id"],
                "model": job["model"],
                "condition": job["condition"],
                "job_status": job["status"],
                "planned_outputs": str(estimate.planned_outputs),
                "estimated_gpu_hours": f"{estimate.estimated_hours:.3f}",
                "conservative_gpu_hours": f"{estimate.conservative_hours:.3f}",
                "account": job["account"],
                "evidence": estimate.evidence,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "priority",
        "run_id",
        "model",
        "condition",
        "job_status",
        "planned_outputs",
        "estimated_gpu_hours",
        "conservative_gpu_hours",
        "account",
        "evidence",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, rows: list[dict[str, str]], csv_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total_budget = KAGGLE_ACCOUNTS * HOURS_PER_ACCOUNT
    required = [row for row in rows if row["condition"] == "required_after_readiness"]
    required_conservative = sum(float(row["conservative_gpu_hours"]) for row in required)
    all_conservative = sum(float(row["conservative_gpu_hours"]) for row in rows)

    lines = [
        "# Post-v5 Compute Budget",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This budget estimates Kaggle GPU time for the readiness-gated post-v5",
        "reruns. It does not launch or prepare jobs.",
        "",
        f"Machine-readable budget: `{csv_path}`.",
        "",
        "## Summary",
        "",
        f"- Available Kaggle budget assumption: {KAGGLE_ACCOUNTS} accounts x {HOURS_PER_ACCOUNT:.0f}h = {total_budget:.0f} GPU-hours.",
        f"- Required post-v5 reruns, conservative: {required_conservative:.2f} GPU-hours.",
        f"- Required plus conditional 7B rerun, conservative: {all_conservative:.2f} GPU-hours.",
        f"- Required budget share: {(required_conservative / total_budget) * 100:.2f}% of assumed Kaggle hours.",
        f"- Required plus conditional budget share: {(all_conservative / total_budget) * 100:.2f}% of assumed Kaggle hours.",
        "",
        "## Job Budget",
        "",
        "| Priority | Run id | Condition | Status | Planned outputs | Estimate h | Conservative h | Evidence |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['priority']} | `{row['run_id']}` | `{row['condition']}` | "
            f"`{row['job_status']}` | {row['planned_outputs']} | "
            f"{row['estimated_gpu_hours']} | {row['conservative_gpu_hours']} | "
            f"{row['evidence']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The required v5 reruns are small relative to the available Kaggle budget.",
            "- The gating issue is not GPU-hour scarcity; it is the manual v5 review and",
            "  freeze/readiness path.",
            "- Keep Qwen2.5-7B 8-bit conditional unless v5 materially changes held-out",
            "  rows or the 7B result remains thesis-critical.",
            "- Do not use this budget as permission to launch jobs while",
            "  `reports/post_v5_kaggle_job_plan.md` is still `not_ready`.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--job-plan",
        type=Path,
        default=ROOT / "results/analysis/post_v5_kaggle_job_plan.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/post_v5_compute_budget.md",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/post_v5_compute_budget.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = budget_rows(read_csv(args.job_plan))
    write_csv(args.csv_output, rows)
    write_report(args.output, rows, args.csv_output.relative_to(ROOT))
    required = sum(
        float(row["conservative_gpu_hours"])
        for row in rows
        if row["condition"] == "required_after_readiness"
    )
    all_jobs = sum(float(row["conservative_gpu_hours"]) for row in rows)
    print(
        f"jobs={len(rows)} required_conservative_hours={required:.2f} "
        f"all_conservative_hours={all_jobs:.2f} report={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
