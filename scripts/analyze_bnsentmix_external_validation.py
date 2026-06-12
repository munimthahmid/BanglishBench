#!/usr/bin/env python3
"""Analyze zero-shot BnSentMix external-validation sentiment outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = ROOT / "data/slices/bnsentmix_balanced200_v1.jsonl"
DEFAULT_ITEMS_OUTPUT = (
    ROOT / "results/analysis/bnsentmix_external_validation_items.csv"
)
DEFAULT_SUMMARY_OUTPUT = (
    ROOT / "results/analysis/bnsentmix_external_validation_summary.csv"
)
DEFAULT_REPORT = ROOT / "reports/bnsentmix_external_validation_results.md"
DEFAULT_EVALS = (
    (
        "Qwen2.5-3B",
        ROOT
        / "results/runs/qwen25_3b_bnsentmix_full200/results/runs/qwen25_3b_bnsentmix_full200.jsonl",
    ),
    (
        "Qwen2.5-7B 8-bit",
        ROOT
        / "results/runs/qwen25_7b_8bit_bnsentmix_full200/results/runs/qwen25_7b_8bit_bnsentmix_full200.jsonl",
    ),
    (
        "Qwen3-4B",
        ROOT
        / "results/runs/qwen3_4b_bnsentmix_full200/results/runs/qwen3_4b_bnsentmix_full200.jsonl",
    ),
)
LABELS = ("positive", "negative", "neutral", "mixed")


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


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def percent(value: float) -> str:
    return f"{100 * value:.1f}%"


def build_rows(
    items_path: Path, eval_specs: list[tuple[str, Path]]
) -> list[dict[str, Any]]:
    items = {str(row["id"]): row for row in load_jsonl(items_path)}
    if not items:
        raise SystemExit(f"No BnSentMix items in {items_path}")

    output: list[dict[str, Any]] = []
    for model_label, eval_path in eval_specs:
        results = load_jsonl(eval_path)
        if not results:
            raise SystemExit(f"No evaluation rows in {eval_path}")
        seen: set[str] = set()
        for result in results:
            item_id = str(result["id"])
            if item_id not in items:
                raise SystemExit(f"Unknown BnSentMix id in {eval_path}: {item_id}")
            if item_id in seen:
                raise SystemExit(f"Duplicate BnSentMix id in {eval_path}: {item_id}")
            seen.add(item_id)
            item = items[item_id]
            gold = str(item["answer"]).strip().lower()
            parsed = parse_answer(
                str(result.get("raw_output", "")), str(result["answer_type"])
            ).strip().lower()
            valid = parsed in LABELS
            output.append(
                {
                    "model": model_label,
                    "id": item_id,
                    "source_row": item["source_row"],
                    "gold": gold,
                    "parsed": parsed if valid else "invalid",
                    "valid_output": valid,
                    "correct": is_correct(parsed, gold, "sentiment"),
                    "raw_output": str(result.get("raw_output", ""))[:240].replace(
                        "\n", " "
                    ),
                    "seconds": result.get("seconds", ""),
                }
            )
    return sorted(output, key=lambda row: (str(row["model"]), str(row["id"])))


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for model in sorted({str(row["model"]) for row in rows}):
        selected = [row for row in rows if row["model"] == model]
        support = Counter(str(row["gold"]) for row in selected)
        predicted = Counter(str(row["parsed"]) for row in selected)
        per_label: list[dict[str, Any]] = []
        for label in LABELS:
            tp = sum(
                row["gold"] == label and row["parsed"] == label for row in selected
            )
            precision = ratio(tp, predicted[label])
            recall = ratio(tp, support[label])
            f1 = ratio(2 * precision * recall, precision + recall)
            per_label.append(
                {
                    "section": "per_label",
                    "model": model,
                    "label": label,
                    "support": support[label],
                    "predicted": predicted[label],
                    "tp": tp,
                    "precision": f"{precision:.6f}",
                    "recall": f"{recall:.6f}",
                    "f1": f"{f1:.6f}",
                }
            )
        correct = sum(bool(row["correct"]) for row in selected)
        valid = sum(bool(row["valid_output"]) for row in selected)
        macro_f1 = sum(float(row["f1"]) for row in per_label) / len(LABELS)
        balanced_accuracy = sum(float(row["recall"]) for row in per_label) / len(
            LABELS
        )
        summary.append(
            {
                "section": "headline",
                "model": model,
                "n": len(selected),
                "valid_outputs": valid,
                "invalid_outputs": len(selected) - valid,
                "correct": correct,
                "accuracy": f"{ratio(correct, len(selected)):.6f}",
                "macro_f1": f"{macro_f1:.6f}",
                "balanced_accuracy": f"{balanced_accuracy:.6f}",
                "majority_baseline": f"{ratio(max(support.values()), len(selected)):.6f}",
            }
        )
        summary.extend(per_label)
        for gold in LABELS:
            for parsed in (*LABELS, "invalid"):
                summary.append(
                    {
                        "section": "confusion",
                        "model": model,
                        "gold": gold,
                        "parsed": parsed,
                        "count": sum(
                            row["gold"] == gold and row["parsed"] == parsed
                            for row in selected
                        ),
                    }
                )
    return summary


def write_report(
    path: Path,
    items_path: Path,
    eval_specs: list[tuple[str, Path]],
    items_output: Path,
    summary_output: Path,
    summary: list[dict[str, Any]],
) -> None:
    headlines = [row for row in summary if row["section"] == "headline"]
    per_labels = [row for row in summary if row["section"] == "per_label"]
    lines = [
        "# BnSentMix External-Validation Results",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This ecological-validity layer measures zero-shot four-way sentiment",
        "classification on naturally occurring Bengali-English code-mixed text.",
        "It is separate from the paired cross-script knowledge benchmark.",
        "",
        f"- Slice: `{repo_path(items_path)}`",
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
            "| Model | Rows | Valid outputs | Accuracy | Macro-F1 | Balanced accuracy | Majority baseline |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in headlines:
        lines.append(
            f"| {row['model']} | {row['n']} | {row['valid_outputs']}/{row['n']} | "
            f"{percent(float(row['accuracy']))} | "
            f"{float(row['macro_f1']):.3f} | "
            f"{percent(float(row['balanced_accuracy']))} | "
            f"{percent(float(row['majority_baseline']))} |"
        )
    lines.extend(
        [
            "",
            "## Per-Label Recall",
            "",
            "| Model | Label | Support | Predicted | Recall | F1 |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in per_labels:
        lines.append(
            f"| {row['model']} | {row['label']} | {row['support']} | "
            f"{row['predicted']} | {percent(float(row['recall']))} | "
            f"{float(row['f1']):.3f} |"
        )
    headline_by_model = {str(row["model"]): row for row in headlines}
    per_label_by_model = {
        str(row["model"]): [label_row for label_row in per_labels if label_row["model"] == row["model"]]
        for row in headlines
    }
    if "Qwen2.5-3B" in headline_by_model and "Qwen2.5-7B 8-bit" in headline_by_model:
        qwen25_3b = headline_by_model["Qwen2.5-3B"]
        qwen25_7b = headline_by_model["Qwen2.5-7B 8-bit"]
        acc_delta = (
            float(qwen25_7b["accuracy"]) - float(qwen25_3b["accuracy"])
        ) * 100
        macro_delta = float(qwen25_7b["macro_f1"]) - float(qwen25_3b["macro_f1"])
        lines.extend(
            [
                "",
                "## Scaling Note",
                "",
                f"- Qwen2.5 scaling improves this natural code-mixed sentiment slice from "
                f"{qwen25_3b['correct']}/{qwen25_3b['n']} to "
                f"{qwen25_7b['correct']}/{qwen25_7b['n']} "
                f"({acc_delta:+.1f} points) and macro-F1 from "
                f"{float(qwen25_3b['macro_f1']):.3f} to "
                f"{float(qwen25_7b['macro_f1']):.3f} ({macro_delta:+.3f}).",
            ]
        )
        if "Qwen3-4B" in headline_by_model:
            qwen3 = headline_by_model["Qwen3-4B"]
            lines.append(
                f"- Qwen2.5-7B nearly matches Qwen3-4B on the headline score "
                f"({qwen25_7b['correct']}/{qwen25_7b['n']} vs "
                f"{qwen3['correct']}/{qwen3['n']}), but their label priors differ."
            )
        qwen25_7b_pred = {
            str(row["label"]): int(row["predicted"])
            for row in per_label_by_model["Qwen2.5-7B 8-bit"]
        }
        lines.append(
            f"- Qwen2.5-7B overpredicts neutral labels "
            f"({qwen25_7b_pred.get('neutral', 0)}/200 predictions), while Qwen3-4B "
            f"overpredicts positive labels "
            f"({{qwen3_positive}}/200 predictions)."
        )
        if "Qwen3-4B" in per_label_by_model:
            qwen3_pred = {
                str(row["label"]): int(row["predicted"])
                for row in per_label_by_model["Qwen3-4B"]
            }
            lines[-1] = lines[-1].format(
                qwen3_positive=qwen3_pred.get("positive", 0)
            )
    lines.extend(
        [
            "",
            "## Interpretation Contract",
            "",
            "- This layer broadens ecological validity with natural code-mixed text.",
            "- It does not estimate the paired script penalty because there is no",
            "  matched Bangla-script or English translation for each item.",
            "- Compare model behavior within this task. Do not directly compare",
            "  absolute accuracy against the core knowledge benchmark.",
            "- Public-dataset contamination remains an open threat.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--eval", action="append", default=[])
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    eval_specs = parse_eval_specs(args.eval)
    rows = build_rows(args.items, eval_specs)
    summary = summarize(rows)
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
    print(f"item_rows={len(rows)}")
    print(f"summary_rows={len(summary)}")
    print(f"items_output={args.items_output}")
    print(f"summary_output={args.summary_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
