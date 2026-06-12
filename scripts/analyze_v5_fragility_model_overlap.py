#!/usr/bin/env python3
"""Analyze cross-model overlap in frozen-v5 Banglish fragility events."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_ITEM_OUTPUT = ROOT / "results/analysis/v5_banglish_fragility_model_overlap_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_banglish_fragility_model_overlap_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglish_fragility_model_overlap.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
MODEL_DISPLAY = {
    "Qwen2.5-3B": "Qwen2.5-3B",
    "Qwen2.5-7B": "Qwen2.5-7B 8-bit",
    "Qwen3-4B": "Qwen3-4B",
}
STRICT_PATTERN = "bangla_english_correct_banglish_wrong"
BUCKET_LABELS = {
    0: "no_model_fragile",
    1: "exactly_one_model",
    2: "exactly_two_models",
    3: "all_three_models",
}


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


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def build_item_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        fragile_models = [
            model for model in MODELS if truthy(row.get(f"{model}_fragility_event", ""))
        ]
        strict_models = [
            model for model in MODELS if row.get(f"{model}_pattern") == STRICT_PATTERN
        ]
        overlap_row = {
            "id": row["id"],
            "dataset": row["dataset"],
            "domain": row["domain"],
            "subject": row["subject"],
            "grade": row["grade"],
            "task_type": row["task_type"],
            "review_label": row["review_label"],
            "fragile_model_count": len(fragile_models),
            "fragility_bucket": BUCKET_LABELS[len(fragile_models)],
            "fragile_models": ";".join(fragile_models),
            "strict_model_count": len(strict_models),
            "strict_bucket": BUCKET_LABELS[len(strict_models)],
            "strict_models": ";".join(strict_models),
            "shared_fragility": len(fragile_models) >= 2,
            "shared_strict_fragility": len(strict_models) >= 2,
            "all_models_fragile": len(fragile_models) == len(MODELS),
            "all_models_strict": len(strict_models) == len(MODELS),
            "banglish_preview": row.get("banglish_preview", ""),
        }
        for model in MODELS:
            overlap_row[f"{model}_pattern"] = row.get(f"{model}_pattern", "")
            overlap_row[f"{model}_fragility_event"] = model in fragile_models
            overlap_row[f"{model}_strict_fragility_event"] = model in strict_models
        out.append(overlap_row)
    return out


def model_sets(rows: list[dict[str, Any]], strict: bool = False) -> dict[str, set[str]]:
    key = "strict_models" if strict else "fragile_models"
    out = {model: set() for model in MODELS}
    for row in rows:
        models = [model for model in str(row[key]).split(";") if model]
        for model in models:
            out[model].add(str(row["id"]))
    return out


def add_summary(
    rows: list[dict[str, Any]],
    section: str,
    key: str,
    n: int,
    denominator: int,
    detail: str = "",
    model_a: str = "",
    model_b: str = "",
) -> None:
    rows.append(
        {
            "section": section,
            "key": key,
            "model_a": model_a,
            "model_b": model_b,
            "n": n,
            "denominator": denominator,
            "rate": round(n / denominator, 4) if denominator else 0.0,
            "detail": detail,
        }
    )


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    total = len(item_rows)
    bucket_counts = Counter(int(row["fragile_model_count"]) for row in item_rows)
    strict_bucket_counts = Counter(int(row["strict_model_count"]) for row in item_rows)
    for count in range(len(MODELS) + 1):
        add_summary(
            out,
            "fragility_bucket",
            BUCKET_LABELS[count],
            bucket_counts[count],
            total,
        )
        add_summary(
            out,
            "strict_bucket",
            BUCKET_LABELS[count],
            strict_bucket_counts[count],
            total,
        )
    add_summary(
        out,
        "fragility_bucket",
        "any_model_fragile",
        sum(bucket_counts[count] for count in range(1, len(MODELS) + 1)),
        total,
    )
    add_summary(
        out,
        "fragility_bucket",
        "shared_two_or_more",
        sum(bucket_counts[count] for count in range(2, len(MODELS) + 1)),
        sum(bucket_counts[count] for count in range(1, len(MODELS) + 1)),
        "denominator is any-fragile items",
    )

    for dataset, rows in sorted(group_by(item_rows, "dataset").items()):
        dataset_counts = Counter(int(row["fragile_model_count"]) for row in rows)
        for count in range(len(MODELS) + 1):
            add_summary(
                out,
                "dataset_fragility_bucket",
                f"{dataset}:{BUCKET_LABELS[count]}",
                dataset_counts[count],
                len(rows),
            )
        add_summary(
            out,
            "dataset_fragility_bucket",
            f"{dataset}:shared_two_or_more",
            sum(dataset_counts[count] for count in range(2, len(MODELS) + 1)),
            len(rows),
        )

    fragile_sets = model_sets(item_rows)
    strict_sets = model_sets(item_rows, strict=True)
    for model in MODELS:
        unique = fragile_sets[model].copy()
        for other in MODELS:
            if other != model:
                unique -= fragile_sets[other]
        add_summary(
            out,
            "model_total",
            "fragility_items",
            len(fragile_sets[model]),
            total,
            model_a=model,
        )
        add_summary(
            out,
            "model_total",
            "strict_items",
            len(strict_sets[model]),
            total,
            model_a=model,
        )
        add_summary(
            out,
            "model_unique",
            "unique_fragility_items",
            len(unique),
            len(fragile_sets[model]),
            "denominator is model fragility items",
            model_a=model,
        )

    for model_a, model_b in combinations(MODELS, 2):
        for label, sets in (("fragility_pair_overlap", fragile_sets), ("strict_pair_overlap", strict_sets)):
            inter = sets[model_a] & sets[model_b]
            union = sets[model_a] | sets[model_b]
            add_summary(
                out,
                label,
                "intersection_over_union",
                len(inter),
                len(union),
                "rate is Jaccard overlap",
                model_a=model_a,
                model_b=model_b,
            )
        exact_two = [
            row
            for row in item_rows
            if set(str(row["fragile_models"]).split(";")) == {model_a, model_b}
        ]
        add_summary(
            out,
            "exactly_two_pair",
            "fragility_items",
            len(exact_two),
            total,
            model_a=model_a,
            model_b=model_b,
        )

    for domain, rows in sorted(group_by(item_rows, "domain").items()):
        if not domain:
            continue
        shared = sum(1 for row in rows if int(row["fragile_model_count"]) >= 2)
        all_three = sum(1 for row in rows if int(row["fragile_model_count"]) == 3)
        any_fragile = sum(1 for row in rows if int(row["fragile_model_count"]) >= 1)
        add_summary(
            out,
            "domain_shared_fragility",
            domain,
            shared,
            len(rows),
            f"any_fragile={any_fragile}; all_three={all_three}",
        )
    dataset_domain_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in item_rows:
        dataset = str(row.get("dataset", ""))
        domain = str(row.get("domain", ""))
        if dataset and domain:
            dataset_domain_rows[f"{dataset}:{domain}"].append(row)
    for key, rows in sorted(dataset_domain_rows.items()):
        shared = sum(1 for row in rows if int(row["fragile_model_count"]) >= 2)
        all_three = sum(1 for row in rows if int(row["fragile_model_count"]) == 3)
        any_fragile = sum(1 for row in rows if int(row["fragile_model_count"]) >= 1)
        add_summary(
            out,
            "dataset_domain_shared_fragility",
            key,
            shared,
            len(rows),
            f"any_fragile={any_fragile}; all_three={all_three}",
        )
    return out


def group_by(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key, ""))].append(row)
    return grouped


def summary_lookup(rows: list[dict[str, Any]], section: str, key: str) -> dict[str, Any]:
    for row in rows:
        if row["section"] == section and row["key"] == key:
            return row
    raise KeyError((section, key))


def model_summary_rows(summary_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for model in MODELS:
        total = next(
            row
            for row in summary_rows
            if row["section"] == "model_total"
            and row["key"] == "fragility_items"
            and row["model_a"] == model
        )
        strict = next(
            row
            for row in summary_rows
            if row["section"] == "model_total"
            and row["key"] == "strict_items"
            and row["model_a"] == model
        )
        unique = next(
            row
            for row in summary_rows
            if row["section"] == "model_unique"
            and row["key"] == "unique_fragility_items"
            and row["model_a"] == model
        )
        out.append({"model": model, "total": total, "strict": strict, "unique": unique})
    return out


def top_shared_domains(summary_rows: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    rows = [row for row in summary_rows if row["section"] == "domain_shared_fragility"]
    return sorted(rows, key=lambda row: (-int(row["n"]), -float(row["rate"]), row["key"]))[:limit]


def top_shared_dataset_domains(
    summary_rows: list[dict[str, Any]], limit: int = 8
) -> list[dict[str, Any]]:
    rows = [
        row
        for row in summary_rows
        if row["section"] == "dataset_domain_shared_fragility"
    ]
    return sorted(rows, key=lambda row: (-int(row["n"]), -float(row["rate"]), row["key"]))[:limit]


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    item_output: Path,
    summary_output: Path,
) -> None:
    total = len(item_rows)
    any_fragile = summary_lookup(summary_rows, "fragility_bucket", "any_model_fragile")
    shared = summary_lookup(summary_rows, "fragility_bucket", "shared_two_or_more")
    exactly_one = summary_lookup(summary_rows, "fragility_bucket", "exactly_one_model")
    exactly_two = summary_lookup(summary_rows, "fragility_bucket", "exactly_two_models")
    all_three = summary_lookup(summary_rows, "fragility_bucket", "all_three_models")
    strict_all_three = summary_lookup(summary_rows, "strict_bucket", "all_three_models")
    lines = [
        "# Frozen-V5 Fragility Model-Overlap Analysis",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend analysis separates one-model Banglish fragility from",
        "fragility shared across the three thesis-facing Qwen rows. A fragility",
        "event means reviewed Banglish is wrong while Bangla or English is correct",
        "for the same model and item.",
        "",
        f"- Item-level overlap: `{repo_path(item_output)}`",
        f"- Machine-readable summary: `{repo_path(summary_output)}`",
        "- Source: `results/analysis/v5_banglish_fragility_items.csv`",
        "",
        "## Overall Overlap",
        "",
        f"- Items with at least one fragile model: {any_fragile['n']}/{total} ({percent(int(any_fragile['n']), total)})",
        f"- Exactly one fragile model: {exactly_one['n']}/{total} ({percent(int(exactly_one['n']), total)})",
        f"- Exactly two fragile models: {exactly_two['n']}/{total} ({percent(int(exactly_two['n']), total)})",
        f"- All three models fragile: {all_three['n']}/{total} ({percent(int(all_three['n']), total)})",
        f"- Shared fragility among any-fragile items: {shared['n']}/{shared['denominator']} ({percent(int(shared['n']), int(shared['denominator']))})",
        f"- Strict all-three Bangla+English-correct/Banglish-wrong items: {strict_all_three['n']}/{total} ({percent(int(strict_all_three['n']), total)})",
        "",
        "## Model Totals",
        "",
        "| Model | Fragile items | Strict items | Unique fragile items |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in model_summary_rows(summary_rows):
        lines.append(
            f"| {MODEL_DISPLAY[row['model']]} | {row['total']['n']}/200 | "
            f"{row['strict']['n']}/200 | {row['unique']['n']}/{row['total']['n']} |"
        )

    lines.extend(
        [
            "",
            "## Pairwise Overlap",
            "",
            "| Model pair | Shared fragile items | Union | Jaccard | Shared strict items | Strict union | Strict Jaccard |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for model_a, model_b in combinations(MODELS, 2):
        frag = next(
            row
            for row in summary_rows
            if row["section"] == "fragility_pair_overlap"
            and row["model_a"] == model_a
            and row["model_b"] == model_b
        )
        strict = next(
            row
            for row in summary_rows
            if row["section"] == "strict_pair_overlap"
            and row["model_a"] == model_a
            and row["model_b"] == model_b
        )
        lines.append(
            f"| {MODEL_DISPLAY[model_a]} + {MODEL_DISPLAY[model_b]} | "
            f"{frag['n']} | {frag['denominator']} | {float(frag['rate']):.3f} | "
            f"{strict['n']} | {strict['denominator']} | {float(strict['rate']):.3f} |"
        )

    lines.extend(
        [
            "",
            "## Dataset Buckets",
            "",
            "| Dataset | No model | Exactly one | Exactly two | All three | Shared two or more |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for dataset, rows in sorted(group_by(item_rows, "dataset").items()):
        counts = Counter(int(row["fragile_model_count"]) for row in rows)
        shared_count = counts[2] + counts[3]
        lines.append(
            f"| {dataset} | {counts[0]} | {counts[1]} | {counts[2]} | "
            f"{counts[3]} | {shared_count}/{len(rows)} |"
        )

    lines.extend(
        [
            "",
            "## Highest Shared-Fragility Dataset-Domains",
            "",
            "This table separates BanglaMATH and BEnQA rows before ranking domains.",
            "",
            "| Dataset:domain | Shared-fragile items | Items | Any fragile / all three |",
            "| --- | ---: | ---: | --- |",
        ]
    )
    for row in top_shared_dataset_domains(summary_rows):
        lines.append(
            f"| {row['key']} | {row['n']} | {row['denominator']} | {row['detail']} |"
        )

    lines.extend(
        [
            "",
            "Merged-domain view for continuity:",
            "",
            "| Domain | Shared-fragile items | Items | Any fragile / all three |",
            "| --- | ---: | ---: | --- |",
        ]
    )
    for row in top_shared_domains(summary_rows):
        lines.append(
            f"| {row['key']} | {row['n']} | {row['denominator']} | {row['detail']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Shared fragility is common enough to treat Banglish fragility as more",
            "  than isolated model noise: over half of any-fragile items affect at",
            "  least two thesis-facing Qwen rows.",
            "- Model-specific fragility still matters: 52 items affect exactly one",
            "  model, so item-level examples should avoid implying every failure is",
            "  universal across the Qwen family.",
            "- Strict all-three failures are rarer, but the five such items are the",
            "  cleanest shared script-specific failures because Bangla and English",
            "  both succeed for every thesis-facing Qwen row.",
            "- The overlap analysis is descriptive failure analysis, not a causal",
            "  feature attribution or deployable routing rule.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--item-output", type=Path, default=DEFAULT_ITEM_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit(f"Missing required input: {args.input}")
    item_rows = build_item_rows(read_csv(args.input))
    summary_rows = build_summary_rows(item_rows)
    if len(item_rows) != 200:
        raise SystemExit(f"Expected 200 item rows, got {len(item_rows)}")
    fragility_events = sum(int(row["fragile_model_count"]) for row in item_rows)
    if fragility_events != 185:
        raise SystemExit(f"Expected 185 fragility events, got {fragility_events}")
    if sum(1 for row in item_rows if int(row["fragile_model_count"]) > 0) != 108:
        raise SystemExit("Expected 108 items with at least one fragile model")
    if sum(1 for row in item_rows if int(row["fragile_model_count"]) == 3) != 21:
        raise SystemExit("Expected 21 all-three fragile items")

    item_fields = [
        "id",
        "dataset",
        "domain",
        "subject",
        "grade",
        "task_type",
        "review_label",
        "fragile_model_count",
        "fragility_bucket",
        "fragile_models",
        "strict_model_count",
        "strict_bucket",
        "strict_models",
        "shared_fragility",
        "shared_strict_fragility",
        "all_models_fragile",
        "all_models_strict",
        "Qwen2.5-3B_pattern",
        "Qwen2.5-3B_fragility_event",
        "Qwen2.5-3B_strict_fragility_event",
        "Qwen2.5-7B_pattern",
        "Qwen2.5-7B_fragility_event",
        "Qwen2.5-7B_strict_fragility_event",
        "Qwen3-4B_pattern",
        "Qwen3-4B_fragility_event",
        "Qwen3-4B_strict_fragility_event",
        "banglish_preview",
    ]
    summary_fields = [
        "section",
        "key",
        "model_a",
        "model_b",
        "n",
        "denominator",
        "rate",
        "detail",
    ]
    write_csv(args.item_output, item_rows, item_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(args.report_output, item_rows, summary_rows, args.item_output, args.summary_output)
    shared = sum(1 for row in item_rows if int(row["fragile_model_count"]) >= 2)
    print(f"items={len(item_rows)}")
    print(f"fragility_events={fragility_events}")
    print(f"any_fragile=108")
    print(f"shared_two_or_more={shared}")
    print(f"all_three=21")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
