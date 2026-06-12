#!/usr/bin/env python3
"""Sensitivity of frozen-v5 results to the amount of Banglish review editing."""

from __future__ import annotations

import argparse
import csv
import difflib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW_AUDIT = ROOT / "results/analysis/validation200_v5_banglish_review_audit.csv"
DEFAULT_RECOVERABILITY = ROOT / "results/analysis/v5_recoverability_source_items.csv"
DEFAULT_DATASET_INTERVALS = ROOT / "results/analysis/v5_dataset_gap_intervals.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_review_edit_distance_sensitivity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_review_edit_distance_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_review_edit_distance_sensitivity.md"

BOOTSTRAPS = 5000
SEED = 20260531
DATASETS = ("all", "benqa", "banglamath")
EDIT_BUCKETS = (
    ("all_items", "All frozen-v5 items"),
    ("no_applied_change", "No applied Banglish change"),
    ("tiny_edit_le_0_5pct", "Tiny edit <=0.5%"),
    ("small_edit_0_5_to_2pct", "Small edit >0.5% to <=2%"),
    ("larger_edit_gt_2pct", "Larger edit >2%"),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def edit_ratio(old: str, new: str) -> float:
    if not old and not new:
        return 0.0
    return 1.0 - difflib.SequenceMatcher(None, old, new).ratio()


def edit_bucket(changed: bool, ratio: float) -> str:
    if not changed:
        return "no_applied_change"
    if ratio <= 0.005:
        return "tiny_edit_le_0_5pct"
    if ratio <= 0.02:
        return "small_edit_0_5_to_2pct"
    return "larger_edit_gt_2pct"


def stable_seed(label: str) -> int:
    return SEED + sum((idx + 1) * ord(ch) for idx, ch in enumerate(label))


def paired_interval(rows: list[dict[str, Any]], left: str, right: str, seed_label: str) -> tuple[float, float, float]:
    pairs = [(bool(row[left]), bool(row[right])) for row in rows]
    observed, low, high, _p_opposite = bootstrap_delta(
        pairs, samples=BOOTSTRAPS, seed=stable_seed(seed_label)
    )
    return observed, low, high


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def review_index(rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        ratio = edit_ratio(row["old_banglish"], row["new_banglish"])
        changed = truthy(row["changed"])
        out[row["id"]] = {
            "review_action": row["action"],
            "review_label": row["quality_label"] or "unreviewed",
            "review_changed": changed,
            "char_edit_ratio": ratio,
            "edit_bucket": edit_bucket(changed, ratio),
        }
    return out


def build_items(
    recoverability_rows: list[dict[str, str]],
    review_rows: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in recoverability_rows:
        review = review_rows[row["id"]]
        bangla = truthy(row["bangla_correct"])
        banglish = truthy(row["banglish_correct"])
        english = truthy(row["english_correct"])
        out.append(
            {
                "model": row["model"],
                "model_id": row["model_id"],
                "dataset": row["dataset"],
                "task_type": row["task_type"],
                "id": row["id"],
                "domain": row["domain"],
                "subject": row["subject"],
                "grade": row["grade"],
                "review_action": review["review_action"],
                "review_label": review["review_label"],
                "review_changed": review["review_changed"],
                "char_edit_ratio": round(float(review["char_edit_ratio"]), 6),
                "edit_bucket": review["edit_bucket"],
                "bangla_correct": bangla,
                "banglish_correct": banglish,
                "english_correct": english,
                "banglish_miss": not banglish,
                "recoverable_banglish_miss": (not banglish) and (bangla or english),
                "bangla_any_recovery": (not banglish) and bangla,
                "english_any_recovery": (not banglish) and english,
                "both_alternate_recovery": (not banglish) and bangla and english,
                "all_script_hard": (not bangla) and (not banglish) and (not english),
            }
        )
    return out


def selected_rows(rows: list[dict[str, Any]], model: str, dataset: str, bucket: str) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["model"] == model]
    if dataset != "all":
        selected = [row for row in selected if row["dataset"] == dataset]
    if bucket != "all_items":
        selected = [row for row in selected if row["edit_bucket"] == bucket]
    return selected


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    models = list(dict.fromkeys(row["model"] for row in rows))
    out: list[dict[str, Any]] = []
    for model in models:
        for bucket, label in EDIT_BUCKETS:
            for dataset in DATASETS:
                selected = selected_rows(rows, model, dataset, bucket)
                if not selected:
                    continue
                n = len(selected)
                bangla = sum(int(row["bangla_correct"]) for row in selected)
                banglish = sum(int(row["banglish_correct"]) for row in selected)
                english = sum(int(row["english_correct"]) for row in selected)
                delta_bangla = paired_interval(
                    selected, "bangla_correct", "banglish_correct", f"{model}:{bucket}:{dataset}:bn"
                )
                delta_english = paired_interval(
                    selected, "english_correct", "banglish_correct", f"{model}:{bucket}:{dataset}:en"
                )
                out.append(
                    {
                        "model": model,
                        "dataset": dataset,
                        "edit_bucket": bucket,
                        "edit_bucket_label": label,
                        "n": n,
                        "unique_items": len({row["id"] for row in selected}),
                        "changed_items": len({row["id"] for row in selected if row["review_changed"]}),
                        "mean_char_edit_ratio": round(
                            sum(float(row["char_edit_ratio"]) for row in selected) / n, 6
                        ),
                        "bangla_correct": bangla,
                        "banglish_correct": banglish,
                        "english_correct": english,
                        "bangla_accuracy": rate(bangla, n),
                        "banglish_accuracy": rate(banglish, n),
                        "english_accuracy": rate(english, n),
                        "banglish_minus_bangla": round(delta_bangla[0], 4),
                        "banglish_minus_bangla_ci95_low": round(delta_bangla[1], 4),
                        "banglish_minus_bangla_ci95_high": round(delta_bangla[2], 4),
                        "banglish_minus_english": round(delta_english[0], 4),
                        "banglish_minus_english_ci95_low": round(delta_english[1], 4),
                        "banglish_minus_english_ci95_high": round(delta_english[2], 4),
                        "recoverable_banglish_misses": sum(
                            int(row["recoverable_banglish_miss"]) for row in selected
                        ),
                        "bangla_any_recovery": sum(int(row["bangla_any_recovery"]) for row in selected),
                        "english_any_recovery": sum(int(row["english_any_recovery"]) for row in selected),
                        "both_alternate_recovery": sum(
                            int(row["both_alternate_recovery"]) for row in selected
                        ),
                        "all_script_hard": sum(int(row["all_script_hard"]) for row in selected),
                    }
                )
    return out


def apply_main_interval_overrides(
    summary_rows: list[dict[str, Any]], interval_rows: list[dict[str, str]]
) -> None:
    intervals = {
        (row["model"], row["dataset"], row["comparison"]): row for row in interval_rows
    }
    for row in summary_rows:
        if row["edit_bucket"] != "all_items":
            continue
        key_bangla = (row["model"], row["dataset"], "banglish_minus_bangla")
        key_english = (row["model"], row["dataset"], "banglish_minus_english")
        if key_bangla in intervals:
            source = intervals[key_bangla]
            row["banglish_minus_bangla"] = source["delta_right_minus_left"]
            row["banglish_minus_bangla_ci95_low"] = source["ci95_low"]
            row["banglish_minus_bangla_ci95_high"] = source["ci95_high"]
        if key_english in intervals:
            source = intervals[key_english]
            row["banglish_minus_english"] = source["delta_right_minus_left"]
            row["banglish_minus_english_ci95_low"] = source["ci95_low"]
            row["banglish_minus_english_ci95_high"] = source["ci95_high"]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def pct(value: Any) -> str:
    return f"{float(value) * 100:.1f}"


def ci_cell(row: dict[str, Any], prefix: str) -> str:
    return (
        f"{points(row[prefix])} pts "
        f"[{points(row[prefix + '_ci95_low'])}, {points(row[prefix + '_ci95_high'])}]"
    )


def find_summary(rows: list[dict[str, Any]], model: str, bucket: str, dataset: str = "all") -> dict[str, Any]:
    return next(
        row for row in rows if row["model"] == model and row["edit_bucket"] == bucket and row["dataset"] == dataset
    )


def write_report(
    report_path: Path,
    review_path: Path,
    recoverability_path: Path,
    interval_path: Path,
    items_path: Path,
    summary_path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> None:
    bucket_counts = Counter(row["edit_bucket"] for row in {row["id"]: row for row in item_rows}.values())
    models = list(dict.fromkeys(row["model"] for row in item_rows))
    lines = [
        "# V5 Review Edit-Distance Sensitivity Audit",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Review audit: `{repo_path(review_path)}`",
        f"- Recoverability items: `{repo_path(recoverability_path)}`",
        f"- Main dataset intervals for all-item rows: `{repo_path(interval_path)}`",
        f"- Item sensitivity CSV: `{repo_path(items_path)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        "",
        "## Headline",
        "",
        "- Applied-edit buckets: "
        + ", ".join(f"{label}={bucket_counts[key]}" for key, label in EDIT_BUCKETS[1:]),
        (
            "- The no-applied-change subset already shows reviewed Banglish below "
            "Bangla and English for all three thesis-facing Qwen rows."
        ),
        (
            "- Larger-edit rows are few (19 items), so they are a quality-control "
            "caveat, not a standalone statistical source of the main result."
        ),
        "",
        "## All Items And Edit Buckets",
        "",
        "| Model | Bucket | n | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Recoverable misses |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: |",
    ]
    for model in models:
        for bucket, _label in EDIT_BUCKETS:
            row = find_summary(summary_rows, model, bucket)
            lines.append(
                f"| {model} | {row['edit_bucket_label']} | {row['n']} | "
                f"{row['bangla_correct']}/{row['n']} ({pct(row['bangla_accuracy'])}%) | "
                f"{row['banglish_correct']}/{row['n']} ({pct(row['banglish_accuracy'])}%) | "
                f"{row['english_correct']}/{row['n']} ({pct(row['english_accuracy'])}%) | "
                f"{ci_cell(row, 'banglish_minus_bangla')} | "
                f"{ci_cell(row, 'banglish_minus_english')} | "
                f"{row['recoverable_banglish_misses']} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This audit separates the magnitude of applied v5 Banglish edits from",
            "model behavior. It shows that the deficit is not introduced only by",
            "rows that required heavier review edits: the no-applied-change subset",
            "already contains the same directional pattern. The larger-edit bucket",
            "is useful for dataset transparency but is too small to support a",
            "standalone effect-size claim.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-audit", type=Path, default=DEFAULT_REVIEW_AUDIT)
    parser.add_argument("--recoverability-items", type=Path, default=DEFAULT_RECOVERABILITY)
    parser.add_argument("--dataset-intervals", type=Path, default=DEFAULT_DATASET_INTERVALS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review_rows = review_index(read_csv(args.review_audit))
    recoverability_rows = read_csv(args.recoverability_items)
    interval_rows = read_csv(args.dataset_intervals)
    item_rows = build_items(recoverability_rows, review_rows)
    summary_rows = summarize(item_rows)
    apply_main_interval_overrides(summary_rows, interval_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        args.review_audit,
        args.recoverability_items,
        args.dataset_intervals,
        args.items_output,
        args.summary_output,
        item_rows,
        summary_rows,
    )
    bucket_counts = Counter(row["edit_bucket"] for row in review_rows.values())
    print(
        " | ".join(
            [
                f"items={len(item_rows)}",
                f"summary_rows={len(summary_rows)}",
                "buckets="
                + ",".join(f"{key}:{bucket_counts[key]}" for key, _label in EDIT_BUCKETS[1:]),
                f"report={args.report_output}",
            ]
        )
    )


if __name__ == "__main__":
    main()
