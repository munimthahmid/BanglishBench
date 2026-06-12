#!/usr/bin/env python3
"""Analyze counterfactual option rotations for the reviewed-v5 BEnQA dev probe."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = (
    ROOT / "data/slices/validation200_v5_dev50_benqa_option_permutations.jsonl"
)
DEFAULT_ITEM_OUTPUT = (
    ROOT / "results/analysis/v5_benqa_option_permutation_probe_items.csv"
)
DEFAULT_SUMMARY_OUTPUT = (
    ROOT / "results/analysis/v5_benqa_option_permutation_probe_summary.csv"
)
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_permutation_probe_results.md"

DEFAULT_EVALS = (
    (
        "Qwen3-4B",
        ROOT
        / "results/runs/qwen3_4b_v5_benqa_option_permutation_dev50/results/runs/qwen3_4b_v5_benqa_option_permutation_dev50.jsonl",
    ),
    (
        "Qwen2.5-3B",
        ROOT
        / "results/runs/qwen25_3b_v5_benqa_option_permutation_dev50/results/runs/qwen25_3b_v5_benqa_option_permutation_dev50.jsonl",
    ),
)

OPTIONS = ("A", "B", "C", "D")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
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


def parse_eval_specs(values: list[str]) -> list[tuple[str, Path]]:
    if not values:
        return list(DEFAULT_EVALS)
    specs: list[tuple[str, Path]] = []
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Expected MODEL=PATH for --eval, got: {value}")
        label, raw_path = value.split("=", 1)
        path = Path(raw_path)
        if not path.is_absolute():
            path = ROOT / path
        specs.append((label, path))
    return specs


def valid_option(value: Any) -> str:
    parsed = str(value).strip().upper()
    return parsed if parsed in OPTIONS else ""


def build_rows(
    items_path: Path, eval_specs: list[tuple[str, Path]]
) -> list[dict[str, Any]]:
    items = {str(row["id"]): row for row in load_jsonl(items_path)}
    if len(items) != 144:
        raise SystemExit(f"Expected 144 probe items, got {len(items)}")

    out: list[dict[str, Any]] = []
    for model_label, eval_path in eval_specs:
        eval_rows = load_jsonl(eval_path)
        if len(eval_rows) != len(items):
            raise SystemExit(
                f"Expected {len(items)} rows for {model_label}, got {len(eval_rows)}"
            )
        seen: set[str] = set()
        for result in eval_rows:
            item_id = str(result["id"])
            if item_id not in items:
                raise SystemExit(f"Unknown probe id in {eval_path}: {item_id}")
            if item_id in seen:
                raise SystemExit(f"Duplicate probe id in {eval_path}: {item_id}")
            seen.add(item_id)
            item = items[item_id]
            parsed = parse_answer(
                str(result.get("raw_output", "")), str(result["answer_type"])
            )
            parsed = valid_option(parsed)
            new_to_old = {
                str(key): str(value)
                for key, value in dict(item["option_new_to_old"]).items()
            }
            gold = valid_option(item["answer"])
            original_gold = valid_option(item["original_answer"])
            parsed_original = new_to_old.get(parsed, "")
            out.append(
                {
                    "model": model_label,
                    "id": item_id,
                    "source_id": item["source_id"],
                    "shift": int(item["permutation_shift"]),
                    "gold": gold,
                    "original_gold": original_gold,
                    "parsed": parsed or "invalid",
                    "parsed_original": parsed_original or "invalid",
                    "valid_option": bool(parsed),
                    "correct": is_correct(parsed, gold, "choice"),
                    "pred_D": parsed == "D",
                    "wrong_D": parsed == "D" and parsed != gold,
                    "selected_original_D": parsed_original == "D",
                    "raw_output": str(result.get("raw_output", ""))[:240].replace(
                        "\n", " "
                    ),
                    "seconds": result.get("seconds", ""),
                }
            )
        if seen != set(items):
            raise SystemExit(f"Missing probe ids for {model_label}")
    return sorted(out, key=lambda row: (row["model"], row["source_id"], row["shift"]))


def summarize_model(rows: list[dict[str, Any]], model: str) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["model"] == model]
    by_source: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        by_source[str(row["source_id"])][int(row["shift"])] = row
    if len(by_source) != 36 or any(set(group) != {0, 1, 2, 3} for group in by_source.values()):
        raise SystemExit(f"Incomplete source/rotation grid for {model}")

    identity = [group[0] for group in by_source.values()]
    rotated = [group[shift] for group in by_source.values() for shift in (1, 2, 3)]
    comparisons = [
        (group[0], group[shift])
        for group in by_source.values()
        for shift in (1, 2, 3)
    ]
    identity_d_groups = [
        group for group in by_source.values() if group[0]["parsed"] == "D"
    ]
    identity_wrong_d_groups = [
        group for group in by_source.values() if group[0]["wrong_D"]
    ]

    def persistence(group_rows: list[dict[int, dict[str, Any]]]) -> tuple[int, int, int, int]:
        rotated_rows = [group[shift] for group in group_rows for shift in (1, 2, 3)]
        label_d = sum(row["parsed"] == "D" for row in rotated_rows)
        semantic_d = sum(row["parsed_original"] == "D" for row in rotated_rows)
        invalid = sum(not row["valid_option"] for row in rotated_rows)
        return len(rotated_rows), label_d, semantic_d, invalid

    d_n, d_label, d_semantic, d_invalid = persistence(identity_d_groups)
    wrong_d_n, wrong_d_label, wrong_d_semantic, wrong_d_invalid = persistence(
        identity_wrong_d_groups
    )
    summary: list[dict[str, Any]] = [
        {
            "section": "headline",
            "model": model,
            "source_items": len(by_source),
            "eval_rows": len(selected),
            "valid_options": sum(row["valid_option"] for row in selected),
            "correct": sum(row["correct"] for row in selected),
            "pred_D": sum(row["pred_D"] for row in selected),
            "identity_correct": sum(row["correct"] for row in identity),
            "identity_pred_D": sum(row["pred_D"] for row in identity),
            "identity_wrong_D": sum(row["wrong_D"] for row in identity),
            "semantic_match_identity": sum(
                left["parsed_original"] == right["parsed_original"]
                and left["valid_option"]
                and right["valid_option"]
                for left, right in comparisons
            ),
            "semantic_match_identity_n": len(comparisons),
            "label_match_identity": sum(
                left["parsed"] == right["parsed"]
                and left["valid_option"]
                and right["valid_option"]
                for left, right in comparisons
            ),
            "label_match_identity_n": len(comparisons),
            "exact_semantic_equivariance_items": sum(
                len({group[shift]["parsed_original"] for shift in range(4)}) == 1
                and all(group[shift]["valid_option"] for shift in range(4))
                for group in by_source.values()
            ),
            "exact_label_persistence_items": sum(
                len({group[shift]["parsed"] for shift in range(4)}) == 1
                and all(group[shift]["valid_option"] for shift in range(4))
                for group in by_source.values()
            ),
            "identity_D_rotated_rows": d_n,
            "identity_D_label_persistence": d_label,
            "identity_D_semantic_persistence": d_semantic,
            "identity_D_invalid": d_invalid,
            "identity_wrong_D_rotated_rows": wrong_d_n,
            "identity_wrong_D_label_persistence": wrong_d_label,
            "identity_wrong_D_semantic_persistence": wrong_d_semantic,
            "identity_wrong_D_invalid": wrong_d_invalid,
        }
    ]
    for shift in range(4):
        rotation = [row for row in selected if row["shift"] == shift]
        summary.append(
            {
                "section": "rotation",
                "model": model,
                "shift": shift,
                "n": len(rotation),
                "valid_options": sum(row["valid_option"] for row in rotation),
                "correct": sum(row["correct"] for row in rotation),
                "pred_D": sum(row["pred_D"] for row in rotation),
                "wrong_D": sum(row["wrong_D"] for row in rotation),
                "selected_original_D": sum(
                    row["selected_original_D"] for row in rotation
                ),
            }
        )
    return summary


def build_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        summary
        for model in sorted({str(row["model"]) for row in rows})
        for summary in summarize_model(rows, model)
    ]


def percent(numerator: Any, denominator: Any) -> str:
    numerator = int(numerator)
    denominator = int(denominator)
    return f"{100 * numerator / denominator:.1f}%" if denominator else "0.0%"


def write_report(
    path: Path,
    items_path: Path,
    eval_specs: list[tuple[str, Path]],
    items_output: Path,
    summary_output: Path,
    summary: list[dict[str, Any]],
) -> None:
    headlines = [row for row in summary if row["section"] == "headline"]
    lines = [
        "# Frozen-V5 BEnQA Option-Permutation Results",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This controlled dev-only audit rotates the semantic option content across",
        "labels A/B/C/D for 36 reviewed-v5 BEnQA MCQs. It asks whether model",
        "predictions follow the option content or remain attached to label D.",
        "",
        f"- Probe items: `{repo_path(items_path)}`",
        f"- Item analysis: `{repo_path(items_output)}`",
        f"- Summary analysis: `{repo_path(summary_output)}`",
    ]
    for model, eval_path in eval_specs:
        lines.append(f"- `{model}` output: `{repo_path(eval_path)}`")
    lines.extend(
        [
            "",
            "## Headline",
            "",
            "| Model | Identity D predictions | Rotated rows from identity-D items | Remain label D | Follow original D content | Semantic match vs identity | Exact semantic-equivariant items |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in headlines:
        lines.append(
            f"| {row['model']} | {row['identity_pred_D']}/36 | "
            f"{row['identity_D_rotated_rows']} | "
            f"{row['identity_D_label_persistence']} "
            f"({percent(row['identity_D_label_persistence'], row['identity_D_rotated_rows'])}) | "
            f"{row['identity_D_semantic_persistence']} "
            f"({percent(row['identity_D_semantic_persistence'], row['identity_D_rotated_rows'])}) | "
            f"{row['semantic_match_identity']}/{row['semantic_match_identity_n']} | "
            f"{row['exact_semantic_equivariance_items']}/36 |"
        )
    lines.extend(
        [
            "",
            "Identity wrong-D subset:",
            "",
            "| Model | Identity wrong-D items | Rotated rows | Remain label D | Follow original D content |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in headlines:
        lines.append(
            f"| {row['model']} | {row['identity_wrong_D']} | "
            f"{row['identity_wrong_D_rotated_rows']} | "
            f"{row['identity_wrong_D_label_persistence']} "
            f"({percent(row['identity_wrong_D_label_persistence'], row['identity_wrong_D_rotated_rows'])}) | "
            f"{row['identity_wrong_D_semantic_persistence']} "
            f"({percent(row['identity_wrong_D_semantic_persistence'], row['identity_wrong_D_rotated_rows'])}) |"
        )
    lines.extend(
        [
            "",
            "## Rotation Breakdown",
            "",
            "| Model | Shift | Correct | Pred D | Wrong D | Selected original-D content |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary:
        if row["section"] != "rotation":
            continue
        lines.append(
            f"| {row['model']} | {row['shift']} | {row['correct']}/{row['n']} | "
            f"{row['pred_D']}/{row['n']} | {row['wrong_D']}/{row['n']} | "
            f"{row['selected_original_D']}/{row['n']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Label-D persistence after content rotation is behavioral evidence for",
            "  a positional D-attractor.",
            "- Original-D-content persistence after rotation is behavioral evidence",
            "  for semantic distractor tracking.",
            "- This is a controlled dev-only audit. It strengthens mechanism",
            "  discussion but does not prove an internal causal mechanism or support",
            "  a held-out mitigation claim.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--eval", action="append", default=[])
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEM_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    eval_specs = parse_eval_specs(args.eval)
    rows = build_rows(args.items, eval_specs)
    summary = build_summary(rows)
    write_csv(args.items_output, rows)
    write_csv(args.summary_output, summary)
    write_report(
        args.report_output,
        args.items,
        eval_specs,
        args.items_output,
        args.summary_output,
        summary,
    )
    print(f"items={len(rows)}")
    print(f"summary={len(summary)}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
