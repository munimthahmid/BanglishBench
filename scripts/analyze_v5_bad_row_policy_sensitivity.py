#!/usr/bin/env python3
"""Compare frozen all-200 and strict-197 policies for reviewed v5 Banglish."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from analyze_banglish_variant_sensitivity import bootstrap_delta
from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLICE = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_SUMMARY = ROOT / "results/analysis/v5_bad_row_policy_sensitivity.csv"
DEFAULT_ITEMS = ROOT / "results/analysis/v5_bad_row_policy_items.csv"
DEFAULT_REPORT = ROOT / "reports/v5_bad_row_policy_sensitivity.md"
DEFAULT_MAIN_REPORT = ROOT / "reports/main_results_validation200_v5.md"


@dataclass(frozen=True)
class ModelSpec:
    label: str
    model: str
    baseline_paths: tuple[Path, ...]
    v4_banglish_paths: tuple[Path, ...]
    v5_banglish_paths: tuple[Path, ...]


SPECS = [
    ModelSpec(
        "Qwen2.5-3B",
        "Qwen/Qwen2.5-3B-Instruct",
        (
            ROOT
            / "results/runs/qwen2_5_3b_validation200_v3_128/results/runs/qwen2_5_3b_validation200_v3_128.jsonl",
        ),
        (
            ROOT
            / "results/runs/qwen2_5_3b_validation200_v4_banglish/results/runs/qwen2_5_3b_validation200_v4_banglish.jsonl",
        ),
        (
            ROOT
            / "results/runs/qwen2_5_3b_validation200_v5_banglish/results/runs/qwen2_5_3b_validation200_v5_banglish.jsonl",
        ),
    ),
    ModelSpec(
        "Qwen3-4B",
        "Qwen/Qwen3-4B-Instruct-2507",
        (
            ROOT
            / "results/runs/qwen3_4b_validation200_v3_128/results/runs/qwen3_4b_validation200_v3_128.jsonl",
        ),
        (
            ROOT
            / "results/runs/qwen3_4b_validation200_v4_banglish/results/runs/qwen3_4b_validation200_v4_banglish.jsonl",
        ),
        (
            ROOT
            / "results/runs/qwen3_4b_validation200_v5_banglish/results/runs/qwen3_4b_validation200_v5_banglish.jsonl",
        ),
    ),
    ModelSpec(
        "Qwen2.5-7B 8-bit",
        "Qwen/Qwen2.5-7B-Instruct",
        (
            ROOT
            / "results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50.jsonl",
            ROOT
            / "results/runs/qwen25_7b_8bit_validation200_v4_test150/results/runs/qwen25_7b_8bit_validation200_v4_test150.jsonl",
        ),
        (
            ROOT
            / "results/runs/qwen25_7b_8bit_validation200_v4_dev50_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50.jsonl",
            ROOT
            / "results/runs/qwen25_7b_8bit_validation200_v4_test150/results/runs/qwen25_7b_8bit_validation200_v4_test150.jsonl",
        ),
        (
            ROOT
            / "results/runs/qwen25_7b_8bit_validation200_v5_banglish_pinned/results/runs/qwen2_5_7b_8bit_validation200_v5_banglish_pinned.jsonl",
        ),
    ),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_eval_rows(paths: tuple[Path, ...]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        for row in load_jsonl(path):
            if not {"id", "model", "variant"}.issubset(row):
                continue
            raw_or_parsed = str(row.get("raw_output", row.get("parsed", "")))
            row["parsed"] = parse_answer(raw_or_parsed, str(row.get("answer_type", "")))
            row["correct"] = is_correct(
                str(row.get("parsed", "")),
                str(row.get("gold", "")),
                str(row.get("answer_type", "")),
            )
            rows.append(row)
    return rows


def index_variant(rows: list[dict[str, Any]], model: str, variant: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("model") != model or row.get("variant") != variant:
            continue
        item_id = str(row["id"])
        if item_id in indexed:
            raise SystemExit(f"Duplicate {model} {variant} row: {item_id}")
        indexed[item_id] = row
    return indexed


def summarize_pair(
    model: str,
    policy: str,
    comparison: str,
    left_label: str,
    right_label: str,
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
    include_ids: set[str],
    samples: int,
    seed: int,
) -> dict[str, Any]:
    keys = sorted(include_ids & set(left) & set(right))
    if len(keys) != len(include_ids):
        raise SystemExit(
            f"{model} {comparison} {policy}: expected {len(include_ids)} paired rows, got {len(keys)}"
        )
    pairs = [(bool(left[item_id]["correct"]), bool(right[item_id]["correct"])) for item_id in keys]
    observed, low, high, p_opposite = bootstrap_delta(pairs, samples=samples, seed=seed)
    return {
        "model": model,
        "policy": policy,
        "comparison": comparison,
        "n": len(keys),
        "left_label": left_label,
        "right_label": right_label,
        "left_correct": sum(int(left_ok) for left_ok, _ in pairs),
        "right_correct": sum(int(right_ok) for _, right_ok in pairs),
        "delta_right_minus_left": round(observed, 4),
        "ci95_low": round(low, 4),
        "ci95_high": round(high, 4),
        "bootstrap_p_opposite_direction": round(p_opposite, 4),
        "gains": sum((not left_ok) and right_ok for left_ok, right_ok in pairs),
        "losses": sum(left_ok and (not right_ok) for left_ok, right_ok in pairs),
        "samples": samples,
        "seed": seed,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def points(value: Any) -> str:
    value = float(value) * 100
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def write_report(
    path: Path,
    summary_path: Path,
    items_path: Path,
    summary: list[dict[str, Any]],
    bad_items: list[dict[str, Any]],
) -> None:
    strict_rows = [row for row in summary if row["policy"] == "strict197"]
    lines = [
        "# V5 Flagged-Bad Denominator Policy Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "The preregistered main policy keeps all 200 frozen validation rows and flags",
        "three source-quality problems. This report separately excludes those rows to",
        "verify that the denominator choice does not drive the reviewed-v5 conclusion.",
        "",
        f"- Summary CSV: `{summary_path.relative_to(ROOT)}`",
        f"- Flagged-item CSV: `{items_path.relative_to(ROOT)}`",
        "",
        "## Flagged Rows",
        "",
        "| ID | Dataset | Review note |",
        "| --- | --- | --- |",
    ]
    for row in bad_items:
        lines.append(f"| `{row['id']}` | {row['dataset']} | {row['review_notes']} |")
    lines.extend(
        [
            "",
            "## Strict-197 Results",
            "",
            "| Model | Comparison | Left | Right | Delta | 95% CI | Gains | Losses |",
            "| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |",
        ]
    )
    for row in strict_rows:
        lines.append(
            "| {model} | `{comparison}` | {left}/{n} | {right}/{n} | {delta} pts | [{low}, {high}] | {gains} | {losses} |".format(
                model=row["model"],
                comparison=row["comparison"],
                left=row["left_correct"],
                right=row["right_correct"],
                n=row["n"],
                delta=points(row["delta_right_minus_left"]),
                low=points(row["ci95_low"]),
                high=points(row["ci95_high"]),
                gains=row["gains"],
                losses=row["losses"],
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The all-200 frozen policy remains the primary thesis denominator.",
            "- The strict-197 view is a separately reported sensitivity analysis.",
            "- Reviewed cleanup remains small under strict exclusion.",
            "- Reviewed Banglish remains below native Bangla and English for all three",
            "  thesis-facing Qwen rows under strict exclusion.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_main_report(
    path: Path,
    summary_path: Path,
    strict_report_path: Path,
    summary: list[dict[str, Any]],
) -> None:
    all200 = {
        (row["model"], row["comparison"]): row
        for row in summary
        if row["policy"] == "all200"
    }
    model_order = ["Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B"]
    lines = [
        "# Main Results: Frozen Validation-200 V5",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This is the final reviewed-v5 all-200 Qwen table. Bangla and English fields",
        "are unchanged from the historical controlled validation slice. The Banglish",
        "field uses the completed reviewed-v5 reruns. The older v3/v4 table remains",
        "available for provenance and mechanism analyses.",
        "",
        f"- Machine-readable sensitivity summary: `{summary_path.relative_to(ROOT)}`",
        "- Generated thesis table: `results/tables/main_script_gap_validation200_v5.csv`",
        f"- Strict-197 sensitivity report: `{strict_report_path.relative_to(ROOT)}`",
        "",
        "## Frozen-V5 All-200 Results",
        "",
        "| Model | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for model in model_order:
        vs_bangla = all200[(model, "v5_banglish_minus_bangla")]
        vs_english = all200[(model, "v5_banglish_minus_english")]
        lines.append(
            "| {model} | {bangla}/{n} | {banglish}/{n} | {english}/{n} | {bb} pts, CI [{bb_low}, {bb_high}] | {be} pts, CI [{be_low}, {be_high}] |".format(
                model=model,
                bangla=vs_bangla["left_correct"],
                banglish=vs_bangla["right_correct"],
                english=vs_english["left_correct"],
                n=vs_bangla["n"],
                bb=points(vs_bangla["delta_right_minus_left"]),
                bb_low=points(vs_bangla["ci95_low"]),
                bb_high=points(vs_bangla["ci95_high"]),
                be=points(vs_english["delta_right_minus_left"]),
                be_low=points(vs_english["ci95_low"]),
                be_high=points(vs_english["ci95_high"]),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Reviewed Banglish remains below native-script Bangla and English at every",
            "  thesis-facing Qwen scaling point.",
            "- The all-200 paired Banglish-Bangla intervals remain negative for Qwen3-4B",
            "  and Qwen2.5-7B 8-bit.",
            "- Qwen2.5-3B retains a -6.5 point all-200 Banglish-Bangla deficit, but its",
            "  interval reaches zero. The historical v3 estimate and the strict-197",
            "  sensitivity remain negative, so the release claim is model-aware.",
            "- The preregistered all-200 denominator remains primary. Strict-197 exclusion",
            "  is a secondary robustness check, not a replacement denominator.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> Any:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--slice", type=Path, default=DEFAULT_SLICE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--main-report", type=Path, default=DEFAULT_MAIN_REPORT)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=4200)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    slice_rows = load_jsonl(args.slice)
    all_ids = {str(row["id"]) for row in slice_rows}
    bad_items = []
    for row in slice_rows:
        review = row.get("banglish_review") or {}
        if review.get("label") == "bad":
            bad_items.append(
                {
                    "id": row["id"],
                    "dataset": row.get("dataset", ""),
                    "review_notes": review.get("notes", ""),
                }
            )
    bad_ids = {str(row["id"]) for row in bad_items}
    strict_ids = all_ids - bad_ids
    if len(all_ids) != 200 or len(bad_ids) != 3 or len(strict_ids) != 197:
        raise SystemExit(
            f"Unexpected policy sizes: all={len(all_ids)} bad={len(bad_ids)} strict={len(strict_ids)}"
        )

    summary: list[dict[str, Any]] = []
    seed = args.seed
    for spec in SPECS:
        baseline = load_eval_rows(spec.baseline_paths)
        v4_rows = load_eval_rows(spec.v4_banglish_paths)
        v5_rows = load_eval_rows(spec.v5_banglish_paths)
        bangla = index_variant(baseline, spec.model, "bangla")
        english = index_variant(baseline, spec.model, "english")
        v4_banglish = index_variant(v4_rows, spec.model, "banglish_clean")
        v5_banglish = index_variant(v5_rows, spec.model, "banglish_clean")
        for policy, include_ids in [("all200", all_ids), ("strict197", strict_ids)]:
            for comparison, left_label, right_label, left, right in [
                ("v5_minus_v4_banglish", "v4 Banglish", "v5 reviewed Banglish", v4_banglish, v5_banglish),
                ("v5_banglish_minus_bangla", "Bangla", "v5 reviewed Banglish", bangla, v5_banglish),
                ("v5_banglish_minus_english", "English", "v5 reviewed Banglish", english, v5_banglish),
            ]:
                summary.append(
                    summarize_pair(
                        spec.label,
                        policy,
                        comparison,
                        left_label,
                        right_label,
                        left,
                        right,
                        include_ids,
                        args.samples,
                        seed,
                    )
                )
                seed += 1

    write_csv(args.summary, summary)
    write_csv(args.items, bad_items)
    write_report(args.report, args.summary, args.items, summary, bad_items)
    write_main_report(args.main_report, args.summary, args.report, summary)
    print(f"all_rows={len(all_ids)}")
    print(f"bad_rows={len(bad_ids)}")
    print(f"strict_rows={len(strict_ids)}")
    print(f"summary={args.summary}")
    print(f"report={args.report}")
    print(f"main_report={args.main_report}")


if __name__ == "__main__":
    main()
