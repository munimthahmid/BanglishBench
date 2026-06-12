#!/usr/bin/env python3
"""Analyze how stronger Qwen rows transfer competence across scripts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_TRANSITIONS_OUTPUT = ROOT / "results/analysis/v5_qwen_scaling_transfer_transitions.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_qwen_scaling_transfer_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_qwen_scaling_transfer.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
MODEL_LABELS = {
    "Qwen2.5-3B": "Qwen2.5-3B",
    "Qwen2.5-7B": "Qwen2.5-7B 8-bit",
    "Qwen3-4B": "Qwen3-4B",
}
MODEL_PAIRS = (
    ("Qwen2.5-3B", "Qwen2.5-7B", "same_family_3b_to_7b"),
    ("Qwen2.5-3B", "Qwen3-4B", "qwen25_3b_to_qwen3_4b"),
    ("Qwen2.5-7B", "Qwen3-4B", "qwen25_7b_to_qwen3_4b"),
)
SCRIPTS = ("bangla", "banglish", "english")
SCRIPT_LABELS = {
    "bangla": "Bangla",
    "banglish": "Reviewed Banglish",
    "english": "English",
}
DATASETS = ("all", "benqa", "banglamath")


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def select_dataset(rows: list[dict[str, str]], dataset: str) -> list[dict[str, str]]:
    if dataset == "all":
        return rows
    return [row for row in rows if row["dataset"] == dataset]


def correct(row: dict[str, str], model: str, script: str) -> bool:
    return truthy(row.get(f"{model}_{script}_correct", ""))


def build_transition_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        for source, target, pair_id in MODEL_PAIRS:
            for script in SCRIPTS:
                source_correct = correct(row, source, script)
                target_correct = correct(row, target, script)
                if source_correct and target_correct:
                    transition = "both_correct"
                elif source_correct and not target_correct:
                    transition = "loss"
                elif not source_correct and target_correct:
                    transition = "gain"
                else:
                    transition = "both_wrong"
                out.append(
                    {
                        "id": row["id"],
                        "dataset": row["dataset"],
                        "domain": row.get("domain", ""),
                        "task_type": row.get("task_type", ""),
                        "pair_id": pair_id,
                        "source_model": MODEL_LABELS[source],
                        "target_model": MODEL_LABELS[target],
                        "script": script,
                        "script_label": SCRIPT_LABELS[script],
                        "source_correct": source_correct,
                        "target_correct": target_correct,
                        "transition": transition,
                    }
                )
    return out


def add_summary(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    pair_id: str = "",
    source_model: str = "",
    target_model: str = "",
    script: str = "",
    source_correct: int = 0,
    target_correct: int = 0,
    gains: int = 0,
    losses: int = 0,
    both_correct: int = 0,
    both_wrong: int = 0,
    denominator: int = 0,
    banglish_minus_bangla_source: int | str = "",
    banglish_minus_bangla_target: int | str = "",
    gap_change: int | str = "",
    detail: str = "",
) -> None:
    net_gain = gains - losses
    rows.append(
        {
            "section": section,
            "dataset": dataset,
            "pair_id": pair_id,
            "source_model": source_model,
            "target_model": target_model,
            "script": script,
            "source_correct": source_correct,
            "target_correct": target_correct,
            "gains": gains,
            "losses": losses,
            "net_gain": net_gain,
            "both_correct": both_correct,
            "both_wrong": both_wrong,
            "denominator": denominator,
            "source_accuracy": round(source_correct / denominator, 4) if denominator else "",
            "target_accuracy": round(target_correct / denominator, 4) if denominator else "",
            "net_gain_rate": round(net_gain / denominator, 4) if denominator else "",
            "banglish_minus_bangla_source": banglish_minus_bangla_source,
            "banglish_minus_bangla_target": banglish_minus_bangla_target,
            "gap_change": gap_change,
            "detail": detail,
        }
    )


def build_summary_rows(rows: list[dict[str, str]], transition_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for dataset in DATASETS:
        dataset_rows = select_dataset(rows, dataset)
        n = len(dataset_rows)
        for model in MODELS:
            for script in SCRIPTS:
                count = sum(correct(row, model, script) for row in dataset_rows)
                add_summary(
                    summary,
                    section="model_accuracy",
                    dataset=dataset,
                    target_model=MODEL_LABELS[model],
                    script=script,
                    target_correct=count,
                    denominator=n,
                    detail=f"{SCRIPT_LABELS[script]} correct count for {MODEL_LABELS[model]}",
                )

        for source, target, pair_id in MODEL_PAIRS:
            source_bangla = sum(correct(row, source, "bangla") for row in dataset_rows)
            source_banglish = sum(correct(row, source, "banglish") for row in dataset_rows)
            target_bangla = sum(correct(row, target, "bangla") for row in dataset_rows)
            target_banglish = sum(correct(row, target, "banglish") for row in dataset_rows)
            source_gap = source_banglish - source_bangla
            target_gap = target_banglish - target_bangla
            add_summary(
                summary,
                section="gap_change",
                dataset=dataset,
                pair_id=pair_id,
                source_model=MODEL_LABELS[source],
                target_model=MODEL_LABELS[target],
                denominator=n,
                banglish_minus_bangla_source=source_gap,
                banglish_minus_bangla_target=target_gap,
                gap_change=target_gap - source_gap,
                detail="Change in reviewed-Banglish-minus-Bangla count gap",
            )

            for script in SCRIPTS:
                selected = [
                    row
                    for row in transition_rows
                    if row["dataset"] == dataset or dataset == "all"
                    if row["pair_id"] == pair_id and row["script"] == script
                ]
                counts = Counter(row["transition"] for row in selected)
                source_count = sum(row["source_correct"] for row in selected)
                target_count = sum(row["target_correct"] for row in selected)
                add_summary(
                    summary,
                    section="script_transition",
                    dataset=dataset,
                    pair_id=pair_id,
                    source_model=MODEL_LABELS[source],
                    target_model=MODEL_LABELS[target],
                    script=script,
                    source_correct=source_count,
                    target_correct=target_count,
                    gains=counts["gain"],
                    losses=counts["loss"],
                    both_correct=counts["both_correct"],
                    both_wrong=counts["both_wrong"],
                    denominator=len(selected),
                    detail="Item-level transition from source model to target model",
                )
    return summary


def find_row(rows: list[dict[str, Any]], section: str, **criteria: str) -> dict[str, Any]:
    for row in rows:
        if row["section"] != section:
            continue
        if all(str(row.get(key, "")) == value for key, value in criteria.items()):
            return row
    raise KeyError((section, criteria))


def write_report(
    path: Path,
    transition_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    transitions_output: Path,
    summary_output: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    same_bangla = find_row(
        summary_rows,
        "script_transition",
        dataset="all",
        pair_id="same_family_3b_to_7b",
        script="bangla",
    )
    same_banglish = find_row(
        summary_rows,
        "script_transition",
        dataset="all",
        pair_id="same_family_3b_to_7b",
        script="banglish",
    )
    same_english = find_row(
        summary_rows,
        "script_transition",
        dataset="all",
        pair_id="same_family_3b_to_7b",
        script="english",
    )
    qwen3_bangla = find_row(
        summary_rows,
        "script_transition",
        dataset="all",
        pair_id="qwen25_3b_to_qwen3_4b",
        script="bangla",
    )
    qwen3_banglish = find_row(
        summary_rows,
        "script_transition",
        dataset="all",
        pair_id="qwen25_3b_to_qwen3_4b",
        script="banglish",
    )
    qwen3_english = find_row(
        summary_rows,
        "script_transition",
        dataset="all",
        pair_id="qwen25_3b_to_qwen3_4b",
        script="english",
    )
    same_gap = find_row(
        summary_rows, "gap_change", dataset="all", pair_id="same_family_3b_to_7b"
    )
    qwen3_gap = find_row(
        summary_rows, "gap_change", dataset="all", pair_id="qwen25_3b_to_qwen3_4b"
    )

    lines = [
        "# Frozen-V5 Qwen Scaling-Transfer Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit asks whether stronger Qwen rows transfer added",
        "task competence equally across Bangla, reviewed Banglish, and English.",
        "It uses the frozen-v5 thesis-facing Qwen correctness table; no new",
        "model inference is involved.",
        "",
        f"- Transition table: `{repo_path(transitions_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            "- Same-family Qwen2.5 3B->7B scaling improves all-200 Bangla by "
            f"{same_bangla['net_gain']} items and English by {same_english['net_gain']} "
            f"items, but reviewed Banglish by only {same_banglish['net_gain']} items."
        ),
        (
            "- The reviewed-Banglish-minus-Bangla count gap widens from "
            f"{same_gap['banglish_minus_bangla_source']} to "
            f"{same_gap['banglish_minus_bangla_target']} under Qwen2.5 3B->7B "
            f"(change {same_gap['gap_change']})."
        ),
        (
            "- Comparing Qwen2.5-3B to Qwen3-4B, Bangla gains "
            f"{qwen3_bangla['net_gain']} items and English gains "
            f"{qwen3_english['net_gain']} items, while reviewed Banglish gains "
            f"{qwen3_banglish['net_gain']} items."
        ),
        (
            "- The Qwen2.5-3B->Qwen3-4B reviewed-Banglish-minus-Bangla count gap "
            f"widens from {qwen3_gap['banglish_minus_bangla_source']} to "
            f"{qwen3_gap['banglish_minus_bangla_target']} "
            f"(change {qwen3_gap['gap_change']})."
        ),
        "- Treat this as behavioral scaling-transfer evidence, not a causal model-size mechanism.",
        "",
        "## All-200 Script Transitions",
        "",
        "| Pair | Script | Source correct | Target correct | Gains | Losses | Net | Both correct | Both wrong |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for pair_id in [pair[2] for pair in MODEL_PAIRS]:
        for script in SCRIPTS:
            row = find_row(
                summary_rows,
                "script_transition",
                dataset="all",
                pair_id=pair_id,
                script=script,
            )
            pair_label = f"{row['source_model']} -> {row['target_model']}"
            lines.append(
                "| {pair} | {script_label} | {source_correct}/200 | {target_correct}/200 | "
                "{gains} | {losses} | {net_gain} | {both_correct} | {both_wrong} |".format(
                    pair=pair_label,
                    script_label=SCRIPT_LABELS[script],
                    **row,
                )
            )

    lines.extend(
        [
            "",
            "## Banglish-Minus-Bangla Gap Change",
            "",
            "| Dataset | Pair | Source gap | Target gap | Change |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for dataset in DATASETS:
        for pair_id in [pair[2] for pair in MODEL_PAIRS]:
            row = find_row(summary_rows, "gap_change", dataset=dataset, pair_id=pair_id)
            pair_label = f"{row['source_model']} -> {row['target_model']}"
            lines.append(
                "| {dataset_label} | {pair} | {banglish_minus_bangla_source} | "
                "{banglish_minus_bangla_target} | {gap_change} |".format(
                    dataset_label=dataset,
                    pair=pair_label,
                    **row,
                )
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The frozen-v5 scaling pattern is not just that stronger models get more",
            "items correct. Their added competence transfers unevenly across scripts.",
            "For the same-family Qwen2.5 comparison, the 7B row gains many more",
            "English items and somewhat more Bangla items than Banglish items. For the",
            "Qwen2.5-3B to Qwen3-4B comparison, Bangla improves sharply while",
            "reviewed Banglish improves only modestly.",
            "",
            "This supports the thesis framing that script is a robustness variable:",
            "more model competence does not automatically close the Latin-script",
            "Banglish gap. The Qwen3 comparison crosses model families/generations,",
            "so cite it as descriptive scaling-transfer evidence rather than as a",
            "controlled parameter-count claim.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_qwen_scaling_transfer.py`",
            f"- Transition rows: {len(transition_rows)}",
            f"- Summary rows: {len(summary_rows)}",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--transitions-output", type=Path, default=DEFAULT_TRANSITIONS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_csv(args.input)
    if len(rows) != 200:
        raise SystemExit(f"Expected 200 frozen-v5 item rows, got {len(rows)}")
    transition_rows = build_transition_rows(rows)
    summary_rows = build_summary_rows(rows, transition_rows)
    transition_fields = [
        "id",
        "dataset",
        "domain",
        "task_type",
        "pair_id",
        "source_model",
        "target_model",
        "script",
        "script_label",
        "source_correct",
        "target_correct",
        "transition",
    ]
    summary_fields = [
        "section",
        "dataset",
        "pair_id",
        "source_model",
        "target_model",
        "script",
        "source_correct",
        "target_correct",
        "gains",
        "losses",
        "net_gain",
        "both_correct",
        "both_wrong",
        "denominator",
        "source_accuracy",
        "target_accuracy",
        "net_gain_rate",
        "banglish_minus_bangla_source",
        "banglish_minus_bangla_target",
        "gap_change",
        "detail",
    ]
    write_csv(args.transitions_output, transition_rows, transition_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(args.report_output, transition_rows, summary_rows, args.transitions_output, args.summary_output)
    print(
        f"transitions={len(transition_rows)} | summary_rows={len(summary_rows)} | "
        f"report={args.report_output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
