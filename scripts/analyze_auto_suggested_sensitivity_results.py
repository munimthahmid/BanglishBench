#!/usr/bin/env python3
"""Summarize validation-200 v4 auto-suggested Banglish sensitivity results."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]


MODEL_CONFIGS = [
    {
        "label": "Qwen2.5-3B",
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "v3": ROOT
        / "results/runs/qwen2_5_3b_validation200_v3_128/results/runs/qwen2_5_3b_validation200_v3_128.jsonl",
        "v4": ROOT
        / "results/runs/qwen2_5_3b_validation200_v4_banglish/results/runs/qwen2_5_3b_validation200_v4_banglish.jsonl",
        "auto": ROOT
        / "results/runs/qwen2_5_3b_validation200_v4_auto_suggested_banglish/results/runs/qwen2_5_3b_validation200_v4_auto_suggested_banglish.jsonl",
    },
    {
        "label": "Qwen3-4B",
        "model": "Qwen/Qwen3-4B-Instruct-2507",
        "v3": ROOT
        / "results/runs/qwen3_4b_validation200_v3_128/results/runs/qwen3_4b_validation200_v3_128.jsonl",
        "v4": ROOT
        / "results/runs/qwen3_4b_validation200_v4_banglish/results/runs/qwen3_4b_validation200_v4_banglish.jsonl",
        "auto": ROOT
        / "results/runs/qwen3_4b_validation200_v4_auto_suggested_banglish/results/runs/qwen3_4b_validation200_v4_auto_suggested_banglish.jsonl",
    },
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Missing expected result file: {path}")
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not {"id", "model", "variant", "correct"}.issubset(row):
                continue
            row.setdefault("prompt_mode", "baseline")
            row["parsed"] = parse_answer(
                str(row.get("raw_output", row.get("parsed", ""))),
                str(row.get("answer_type", "")),
            )
            row["correct"] = is_correct(
                str(row.get("parsed", "")),
                str(row.get("gold", "")),
                str(row.get("answer_type", "")),
            )
            row["_source"] = str(path)
            row["_line"] = line_no
            rows.append(row)
    return rows


def index_banglish(rows: list[dict[str, Any]], model: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if (
            row.get("model") == model
            and row.get("variant") == "banglish_clean"
            and row.get("prompt_mode") == "baseline"
        ):
            out[row["id"]] = row
    return out


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    pos = (len(values) - 1) * q
    low = int(pos)
    high = min(low + 1, len(values) - 1)
    frac = pos - low
    return values[low] * (1 - frac) + values[high] * frac


def bootstrap_delta(
    pairs: list[tuple[bool, bool]],
    samples: int,
    seed: int,
) -> tuple[float, float, float, float]:
    rng = random.Random(seed)
    n = len(pairs)
    deltas: list[float] = []
    for _ in range(samples):
        left = right = 0
        for _ in range(n):
            left_correct, right_correct = pairs[rng.randrange(n)]
            left += int(left_correct)
            right += int(right_correct)
        deltas.append(right / n - left / n)
    observed = (
        sum(int(right) for _, right in pairs) / n
        - sum(int(left) for left, _ in pairs) / n
    )
    lower = percentile(deltas, 0.025)
    upper = percentile(deltas, 0.975)
    if observed >= 0:
        p_opposite = sum(1 for delta in deltas if delta <= 0) / samples
    else:
        p_opposite = sum(1 for delta in deltas if delta >= 0) / samples
    return observed, lower, upper, p_opposite


def change_label(before: bool, after: bool) -> str:
    if before and after:
        return "same_correct"
    if not before and not after:
        return "same_wrong"
    if not before and after:
        return "gain"
    return "loss"


def analyze_model(
    config: dict[str, Any],
    samples: int,
    seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    v3 = index_banglish(load_jsonl(config["v3"]), config["model"])
    v4 = index_banglish(load_jsonl(config["v4"]), config["model"])
    auto = index_banglish(load_jsonl(config["auto"]), config["model"])
    keys = sorted(set(v3) & set(v4) & set(auto))
    if not keys:
        raise SystemExit(f"No overlapping rows for {config['label']}")

    item_rows: list[dict[str, Any]] = []
    for item_id in keys:
        r3 = v3[item_id]
        r4 = v4[item_id]
        ra = auto[item_id]
        item_rows.append(
            {
                "model": config["label"],
                "id": item_id,
                "dataset": ra.get("dataset", r4.get("dataset", "")),
                "task_type": ra.get("task_type", r4.get("task_type", "")),
                "answer_type": ra.get("answer_type", r4.get("answer_type", "")),
                "gold": ra.get("gold", r4.get("gold", "")),
                "v3_correct": bool(r3.get("correct")),
                "v4_correct": bool(r4.get("correct")),
                "auto_correct": bool(ra.get("correct")),
                "v4_vs_v3": change_label(bool(r3.get("correct")), bool(r4.get("correct"))),
                "auto_vs_v4": change_label(bool(r4.get("correct")), bool(ra.get("correct"))),
                "v3_parsed": r3.get("parsed", ""),
                "v4_parsed": r4.get("parsed", ""),
                "auto_parsed": ra.get("parsed", ""),
                "v4_seconds": r4.get("seconds", ""),
                "auto_seconds": ra.get("seconds", ""),
                "auto_source": ra.get("_source", ""),
            }
        )

    pairs_v4_auto = [
        (bool(row["v4_correct"]), bool(row["auto_correct"])) for row in item_rows
    ]
    pairs_v3_auto = [
        (bool(row["v3_correct"]), bool(row["auto_correct"])) for row in item_rows
    ]
    v4_auto = bootstrap_delta(pairs_v4_auto, samples=samples, seed=seed)
    v3_auto = bootstrap_delta(pairs_v3_auto, samples=samples, seed=seed + 1)

    summary = {
        "model": config["label"],
        "n": len(item_rows),
        "v3_correct": sum(int(row["v3_correct"]) for row in item_rows),
        "v4_correct": sum(int(row["v4_correct"]) for row in item_rows),
        "auto_correct": sum(int(row["auto_correct"]) for row in item_rows),
        "auto_minus_v4_delta": round(v4_auto[0], 4),
        "auto_minus_v4_ci95_low": round(v4_auto[1], 4),
        "auto_minus_v4_ci95_high": round(v4_auto[2], 4),
        "auto_minus_v4_p_opposite": round(v4_auto[3], 4),
        "auto_minus_v3_delta": round(v3_auto[0], 4),
        "auto_minus_v3_ci95_low": round(v3_auto[1], 4),
        "auto_minus_v3_ci95_high": round(v3_auto[2], 4),
        "auto_minus_v3_p_opposite": round(v3_auto[3], 4),
        "auto_vs_v4_gains": sum(row["auto_vs_v4"] == "gain" for row in item_rows),
        "auto_vs_v4_losses": sum(row["auto_vs_v4"] == "loss" for row in item_rows),
        "samples": samples,
        "seed": seed,
    }
    return item_rows, summary


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


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def write_report(
    path: Path,
    summary_rows: list[dict[str, Any]],
    item_rows: list[dict[str, Any]],
    summary_output: Path,
    items_output: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Auto-Suggested Banglish Sensitivity Results\n\n")
        f.write("Updated: 2026-05-28\n\n")
        f.write("## Artifacts\n\n")
        f.write(f"- Summary CSV: `{repo_path(summary_output)}`\n")
        f.write(f"- Item CSV: `{repo_path(items_output)}`\n\n")
        f.write("## Main Table\n\n")
        f.write(
            "| Model | v3 | v4 | auto-suggested | auto-v4 delta | 95% CI | gains | losses |\n"
        )
        f.write("| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |\n")
        for row in summary_rows:
            f.write(
                f"| {row['model']} | {row['v3_correct']}/{row['n']} | "
                f"{row['v4_correct']}/{row['n']} | {row['auto_correct']}/{row['n']} | "
                f"{row['auto_minus_v4_delta']:+.4f} | "
                f"[{row['auto_minus_v4_ci95_low']:+.4f}, "
                f"{row['auto_minus_v4_ci95_high']:+.4f}] | "
                f"{row['auto_vs_v4_gains']} | {row['auto_vs_v4_losses']} |\n"
            )
        f.write("\n")
        f.write("## Caveat\n\n")
        f.write(
            "The auto-suggested slice is heuristic and unreviewed. Use this only "
            "as a sensitivity analysis until the human-review workflow freezes a "
            "v5 slice.\n\n"
        )
        f.write("## Auto-v4 Changed Items\n\n")
        changed = [row for row in item_rows if row["auto_vs_v4"] in {"gain", "loss"}]
        for row in changed[:30]:
            f.write(
                f"- `{row['model']}` `{row['id']}` `{row['dataset']}` "
                f"{row['auto_vs_v4']}: v4=`{row['v4_parsed']}`, "
                f"auto=`{row['auto_parsed']}`, gold=`{row['gold']}`\n"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT
        / "results/analysis/validation200_v4_auto_suggested_sensitivity_summary.csv",
    )
    parser.add_argument(
        "--items-output",
        type=Path,
        default=ROOT
        / "results/analysis/validation200_v4_auto_suggested_sensitivity_items.csv",
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=ROOT / "reports/validation200_v4_auto_suggested_sensitivity.md",
    )
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    all_items: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for config in MODEL_CONFIGS:
        item_rows, summary = analyze_model(config, args.samples, args.seed)
        all_items.extend(item_rows)
        summaries.append(summary)
    write_csv(args.items_output, all_items)
    write_csv(args.summary_output, summaries)
    write_report(args.report_output, summaries, all_items, args.summary_output, args.items_output)
    print(f"wrote={args.summary_output}")
    print(f"wrote={args.items_output}")
    print(f"wrote={args.report_output}")
    for row in summaries:
        print(
            f"{row['model']}: v4={row['v4_correct']}/{row['n']} "
            f"auto={row['auto_correct']}/{row['n']} "
            f"delta={row['auto_minus_v4_delta']:+.4f}"
        )


if __name__ == "__main__":
    main()
