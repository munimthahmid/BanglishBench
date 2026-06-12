#!/usr/bin/env python3
"""Paired sensitivity analysis between two Banglish evaluation result files."""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEV = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_TEST = ROOT / "data/slices/validation_200_v4_test150.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not {"id", "model", "variant"}.issubset(row):
                continue
            row.setdefault("prompt_mode", "baseline")
            raw_or_parsed = str(row.get("raw_output", row.get("parsed", "")))
            row["parsed"] = parse_answer(raw_or_parsed, str(row.get("answer_type", "")))
            row["correct"] = is_correct(
                str(row.get("parsed", "")),
                str(row.get("gold", "")),
                str(row.get("answer_type", "")),
            )
            row["_source"] = str(path)
            row["_line"] = line_no
            rows.append(row)
    return rows


def load_split_map(dev_path: Path, test_path: Path) -> dict[str, str]:
    split_by_id: dict[str, str] = {}
    for split, path in [("dev", dev_path), ("test", test_path)]:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                split_by_id[str(row["id"])] = split
    return split_by_id


def index_rows(
    rows: list[dict[str, Any]],
    model: str,
    variant: str,
    prompt_mode: str,
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if (
            row.get("model") == model
            and row.get("variant") == variant
            and row.get("prompt_mode") == prompt_mode
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
    low = percentile(deltas, 0.025)
    high = percentile(deltas, 0.975)
    if observed >= 0:
        p_opposite = sum(1 for delta in deltas if delta <= 0) / samples
    else:
        p_opposite = sum(1 for delta in deltas if delta >= 0) / samples
    return observed, low, high, p_opposite


def change_label(before: bool, after: bool) -> str:
    if before and after:
        return "same_correct"
    if not before and not after:
        return "same_wrong"
    if not before and after:
        return "gain"
    return "loss"


def summarize_group(
    rows: list[dict[str, Any]],
    group: str,
    samples: int,
    seed: int,
) -> dict[str, Any]:
    pairs = [
        (bool(row["baseline_correct"]), bool(row["candidate_correct"])) for row in rows
    ]
    observed, low, high, p_opposite = bootstrap_delta(pairs, samples, seed)
    return {
        "group": group,
        "n": len(rows),
        "baseline_correct": sum(int(left) for left, _ in pairs),
        "candidate_correct": sum(int(right) for _, right in pairs),
        "delta_candidate_minus_baseline": round(observed, 4),
        "ci95_low": round(low, 4),
        "ci95_high": round(high, 4),
        "bootstrap_p_opposite_direction": round(p_opposite, 4),
        "gains": sum(row["change"] == "gain" for row in rows),
        "losses": sum(row["change"] == "loss" for row in rows),
        "same_correct": sum(row["change"] == "same_correct" for row in rows),
        "same_wrong": sum(row["change"] == "same_wrong" for row in rows),
        "samples": samples,
        "seed": seed,
    }


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


def repo_paths(paths: list[Path]) -> str:
    return "`, `".join(repo_path(path) for path in paths)


def write_report(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, Any]],
    item_rows: list[dict[str, Any]],
    summary_path: Path,
    items_path: Path,
) -> None:
    overall = next(row for row in summary_rows if row["group"] == "overall")
    lines = [
        f"# {args.model_label} Banglish Variant Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Baseline `{args.baseline_name}`: `{repo_paths(args.baseline_results)}`",
        f"- Candidate `{args.candidate_name}`: `{repo_paths(args.candidate_results)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        f"- Item CSV: `{repo_path(items_path)}`",
        "",
        "## Overall",
        "",
        "| Baseline | Candidate | Delta | 95% CI | Gains | Losses |",
        "| ---: | ---: | ---: | --- | ---: | ---: |",
        "| {base}/{n} | {cand}/{n} | {delta:+.1f} pts | [{low:+.1f}, {high:+.1f}] | {gains} | {losses} |".format(
            base=overall["baseline_correct"],
            cand=overall["candidate_correct"],
            n=overall["n"],
            delta=float(overall["delta_candidate_minus_baseline"]) * 100,
            low=float(overall["ci95_low"]) * 100,
            high=float(overall["ci95_high"]) * 100,
            gains=overall["gains"],
            losses=overall["losses"],
        ),
        "",
        "## Groups",
        "",
        "| Group | n | Baseline | Candidate | Delta | 95% CI | Gains | Losses |",
        "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in summary_rows:
        if row["group"] == "overall":
            continue
        lines.append(
            "| {group} | {n} | {base} | {cand} | {delta:+.1f} pts | [{low:+.1f}, {high:+.1f}] | {gains} | {losses} |".format(
                group=row["group"],
                n=row["n"],
                base=row["baseline_correct"],
                cand=row["candidate_correct"],
                delta=float(row["delta_candidate_minus_baseline"]) * 100,
                low=float(row["ci95_low"]) * 100,
                high=float(row["ci95_high"]) * 100,
                gains=row["gains"],
                losses=row["losses"],
            )
        )

    changed = [row for row in item_rows if row["change"] in {"gain", "loss"}]
    lines.extend(["", "## Changed Items", ""])
    for row in changed[:50]:
        lines.append(
            f"- `{row['change']}` `{row['id']}` `{row['split']}` `{row['dataset']}` "
            f"gold=`{row['gold']}` {args.baseline_name}=`{row['baseline_parsed']}` "
            f"{args.candidate_name}=`{row['candidate_parsed']}`"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-results", type=Path, nargs="+", required=True)
    parser.add_argument("--candidate-results", type=Path, nargs="+", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--baseline-name", default="baseline")
    parser.add_argument("--candidate-name", default="candidate")
    parser.add_argument("--variant", default="banglish_clean")
    parser.add_argument("--prompt-mode", default="baseline")
    parser.add_argument("--dev-slice", type=Path, default=DEFAULT_DEV)
    parser.add_argument("--test-slice", type=Path, default=DEFAULT_TEST)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    baseline_rows = [
        row for path in args.baseline_results for row in load_jsonl(path)
    ]
    candidate_rows = [
        row for path in args.candidate_results for row in load_jsonl(path)
    ]
    baseline = index_rows(baseline_rows, args.model, args.variant, args.prompt_mode)
    candidate = index_rows(candidate_rows, args.model, args.variant, args.prompt_mode)
    keys = sorted(set(baseline) & set(candidate))
    if not keys:
        raise SystemExit("No overlapping paired rows found.")
    split_by_id = load_split_map(args.dev_slice, args.test_slice)

    item_rows: list[dict[str, Any]] = []
    for item_id in keys:
        left = baseline[item_id]
        right = candidate[item_id]
        base_correct = bool(left.get("correct"))
        cand_correct = bool(right.get("correct"))
        item_rows.append(
            {
                "model": args.model_label,
                "id": item_id,
                "split": split_by_id.get(item_id, "unknown"),
                "dataset": right.get("dataset", left.get("dataset", "")),
                "task_type": right.get("task_type", left.get("task_type", "")),
                "answer_type": right.get("answer_type", left.get("answer_type", "")),
                "gold": right.get("gold", left.get("gold", "")),
                "baseline_correct": base_correct,
                "candidate_correct": cand_correct,
                "change": change_label(base_correct, cand_correct),
                "baseline_parsed": left.get("parsed", ""),
                "candidate_parsed": right.get("parsed", ""),
                "baseline_seconds": left.get("seconds", ""),
                "candidate_seconds": right.get("seconds", ""),
                "baseline_source": left.get("_source", ""),
                "candidate_source": right.get("_source", ""),
            }
        )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    grouped["overall"] = item_rows
    for row in item_rows:
        grouped[f"split={row['split']}"].append(row)
        grouped[f"dataset={row['dataset']}"].append(row)
        grouped[f"split={row['split']};dataset={row['dataset']}"].append(row)

    summary_rows: list[dict[str, Any]] = []
    for index, (group, rows) in enumerate(grouped.items()):
        summary_rows.append(
            summarize_group(rows, group, samples=args.samples, seed=args.seed + index)
        )

    prefix = args.output_prefix
    summary_path = prefix.with_name(prefix.name + "_summary.csv")
    items_path = prefix.with_name(prefix.name + "_items.csv")
    report_path = prefix.with_name(prefix.name + ".md")
    write_csv(summary_path, summary_rows)
    write_csv(items_path, item_rows)
    write_report(report_path, args, summary_rows, item_rows, summary_path, items_path)
    print(f"summary={summary_path}")
    print(f"items={items_path}")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
