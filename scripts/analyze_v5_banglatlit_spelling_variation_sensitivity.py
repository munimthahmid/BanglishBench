#!/usr/bin/env python3
"""Sensitivity of frozen-v5 gaps to BanglaTLit spelling-variation exposure."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_FRAGILITY_ITEMS = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_VARIATION_TOKENS = ROOT / "results/analysis/banglatlit_spelling_variation_tokens.csv"
DEFAULT_VARIATION_SUMMARY = ROOT / "results/analysis/banglatlit_spelling_variation_summary.csv"
DEFAULT_DATASET_INTERVALS = ROOT / "results/analysis/v5_dataset_gap_intervals.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_banglatlit_spelling_variation_sensitivity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_banglatlit_spelling_variation_sensitivity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglatlit_spelling_variation_sensitivity.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
DATASETS = ("all", "benqa", "banglamath")
LATIN_TOKEN_RE = re.compile(r"[A-Za-z]+")
OPTION_LINE_RE = re.compile(r"^\s*[A-D][\).]\s+")
BOOTSTRAPS = 5000
SEED = 20260531


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def to_int(value: Any) -> int:
    return int(str(value).strip() or 0)


def to_float(value: Any) -> float:
    return float(str(value).strip() or 0)


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def pct(value: Any) -> str:
    return f"{float(value) * 100:.1f}"


def stable_seed(label: str) -> int:
    return SEED + sum((idx + 1) * ord(ch) for idx, ch in enumerate(label))


def strip_eval_scaffold(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Answer with only") or stripped.startswith("Return only"):
            continue
        if OPTION_LINE_RE.match(stripped):
            continue
        kept.append(stripped)
    return "\n".join(kept)


def latin_tokens(text: str) -> list[str]:
    return [token.lower() for token in LATIN_TOKEN_RE.findall(text) if len(token) >= 2]


def parse_variant_list(raw: str) -> list[tuple[str, int]]:
    variants: list[tuple[str, int]] = []
    for part in str(raw).split(";"):
        part = part.strip()
        if not part or ":" not in part:
            continue
        token, count = part.rsplit(":", 1)
        token = token.strip().lower()
        if token:
            variants.append((token, to_int(count)))
    return variants


def build_variation_lexicon(rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    lexicon: dict[str, dict[str, Any]] = {}
    for row in rows:
        repeated_variants = to_int(row["repeated_latin_variants"])
        unique_variants = to_int(row["unique_latin_variants"])
        total_count = to_int(row["total_count"])
        for token, count in parse_variant_list(row["top_repeated_latin_variants"]):
            entry = lexicon.setdefault(
                token,
                {
                    "max_repeated_variants": 0,
                    "max_unique_variants": 0,
                    "total_variant_token_count": 0,
                    "source_bangla_tokens": set(),
                },
            )
            entry["max_repeated_variants"] = max(
                int(entry["max_repeated_variants"]), repeated_variants
            )
            entry["max_unique_variants"] = max(int(entry["max_unique_variants"]), unique_variants)
            entry["total_variant_token_count"] = int(entry["total_variant_token_count"]) + count
            if total_count >= 3:
                entry["source_bangla_tokens"].add(row["bangla_token"])
    return lexicon


def load_validation_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
            review = item.get("banglish_review") if isinstance(item.get("banglish_review"), dict) else {}
            rows.append(
                {
                    "id": item["id"],
                    "dataset": item.get("dataset", ""),
                    "domain": item.get("domain", ""),
                    "subject": metadata.get("subject", ""),
                    "grade": metadata.get("grade", ""),
                    "task_type": item.get("task_type", ""),
                    "quality_status": item.get("quality_status", ""),
                    "review_label": review.get("label", "unreviewed"),
                    "banglish": item.get("banglish_clean", ""),
                }
            )
    return rows


def item_variation_features(
    item: dict[str, Any], lexicon: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    tokens = latin_tokens(strip_eval_scaffold(str(item["banglish"])))
    n = len(tokens)
    matched = [lexicon[token] for token in tokens if token in lexicon]
    high_variation = [
        entry for entry in matched if int(entry["max_repeated_variants"]) >= 4
    ]
    exposure = sum(max(int(entry["max_repeated_variants"]) - 1, 0) for entry in matched)
    return {
        "content_token_count": n,
        "variation_seen_token_count": len(matched),
        "high_variation_token_count": len(high_variation),
        "variation_seen_share": rate(len(matched), n),
        "high_variation_share": rate(len(high_variation), n),
        "spelling_variation_exposure": round(exposure / n, 4) if n else 0.0,
        "mean_repeated_variants_seen": round(
            sum(int(entry["max_repeated_variants"]) for entry in matched) / len(matched), 4
        )
        if matched
        else 0.0,
    }


def quartile_labels(
    base_rows: list[dict[str, Any]], dataset: str, metric: str
) -> dict[str, str]:
    selected = base_rows if dataset == "all" else [row for row in base_rows if row["dataset"] == dataset]
    sorted_rows = sorted(selected, key=lambda row: (float(row[metric]), row["id"]))
    labels: dict[str, str] = {}
    n = len(sorted_rows)
    for index in range(4):
        start = index * n // 4
        end = (index + 1) * n // 4
        for row in sorted_rows[start:end]:
            labels[row["id"]] = f"q{index + 1}"
    return labels


def build_item_rows(
    validation_rows: list[dict[str, Any]],
    fragility_rows: list[dict[str, str]],
    lexicon: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    fragility_by_id = {row["id"]: row for row in fragility_rows}
    base_rows: list[dict[str, Any]] = []
    for item in validation_rows:
        base = {key: value for key, value in item.items() if key != "banglish"}
        base.update(item_variation_features(item, lexicon))
        base_rows.append(base)

    all_quartiles = quartile_labels(base_rows, "all", "spelling_variation_exposure")
    dataset_quartiles = {
        dataset: quartile_labels(base_rows, dataset, "spelling_variation_exposure")
        for dataset in ("benqa", "banglamath")
    }

    out: list[dict[str, Any]] = []
    for base in base_rows:
        fragility = fragility_by_id[base["id"]]
        for model in MODELS:
            bangla = truthy(fragility.get(f"{model}_bangla_correct", ""))
            banglish = truthy(fragility.get(f"{model}_banglish_correct", ""))
            english = truthy(fragility.get(f"{model}_english_correct", ""))
            out.append(
                {
                    **base,
                    "variation_exposure_quartile_all": all_quartiles[base["id"]],
                    "variation_exposure_quartile_dataset": dataset_quartiles[base["dataset"]][
                        base["id"]
                    ],
                    "model": model,
                    "bangla_correct": bangla,
                    "banglish_correct": banglish,
                    "english_correct": english,
                    "banglish_fragile": (not banglish) and (bangla or english),
                    "strict_bangla_english_fragile": (not banglish) and bangla and english,
                    "all_script_hard": (not bangla) and (not banglish) and (not english),
                }
            )
    return out


def select_rows(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    model: str,
) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["model"] == model]
    if dataset != "all":
        selected = [row for row in selected if row["dataset"] == dataset]
    if section == "variation_quartile_all":
        selected = [row for row in selected if row["variation_exposure_quartile_all"] == bucket]
    elif section == "variation_quartile_by_dataset":
        selected = [
            row for row in selected if row["variation_exposure_quartile_dataset"] == bucket
        ]
    elif section != "dataset_overall":
        raise SystemExit(f"Unknown section: {section}")
    return selected


def interval(
    rows: list[dict[str, Any]], left_key: str, right_key: str, seed_label: str
) -> tuple[float, float, float]:
    pairs = [(bool(row[left_key]), bool(row[right_key])) for row in rows]
    observed, low, high, _p = bootstrap_delta(
        pairs,
        samples=BOOTSTRAPS,
        seed=stable_seed(seed_label),
    )
    return observed, low, high


def summarize_selected(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    model: str,
    detail: str,
) -> dict[str, Any]:
    if not rows:
        raise SystemExit(f"Empty summary bucket: {section} {dataset} {bucket} {model}")
    n = len(rows)
    bangla = sum(int(row["bangla_correct"]) for row in rows)
    banglish = sum(int(row["banglish_correct"]) for row in rows)
    english = sum(int(row["english_correct"]) for row in rows)
    bangla_delta = interval(rows, "bangla_correct", "banglish_correct", f"{section}:{dataset}:{bucket}:{model}:bn")
    english_delta = interval(
        rows, "english_correct", "banglish_correct", f"{section}:{dataset}:{bucket}:{model}:en"
    )
    return {
        "section": section,
        "dataset": dataset,
        "bucket": bucket,
        "model": model,
        "n_items": n,
        "mean_spelling_variation_exposure": round(
            sum(float(row["spelling_variation_exposure"]) for row in rows) / n, 4
        ),
        "mean_variation_seen_share": round(
            sum(float(row["variation_seen_share"]) for row in rows) / n, 4
        ),
        "mean_high_variation_share": round(
            sum(float(row["high_variation_share"]) for row in rows) / n, 4
        ),
        "bangla_correct": bangla,
        "banglish_correct": banglish,
        "english_correct": english,
        "bangla_accuracy": rate(bangla, n),
        "banglish_accuracy": rate(banglish, n),
        "english_accuracy": rate(english, n),
        "banglish_minus_bangla": round(bangla_delta[0], 4),
        "banglish_minus_bangla_ci95_low": round(bangla_delta[1], 4),
        "banglish_minus_bangla_ci95_high": round(bangla_delta[2], 4),
        "banglish_minus_english": round(english_delta[0], 4),
        "banglish_minus_english_ci95_low": round(english_delta[1], 4),
        "banglish_minus_english_ci95_high": round(english_delta[2], 4),
        "banglish_fragile_items": sum(int(row["banglish_fragile"]) for row in rows),
        "strict_bangla_english_fragile_items": sum(
            int(row["strict_bangla_english_fragile"]) for row in rows
        ),
        "all_script_hard_items": sum(int(row["all_script_hard"]) for row in rows),
        "detail": detail,
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for dataset in DATASETS:
        for model in MODELS:
            summary.append(
                summarize_selected(
                    select_rows(item_rows, "dataset_overall", dataset, "all", model),
                    "dataset_overall",
                    dataset,
                    "all",
                    model,
                    "all rows",
                )
            )
    for bucket in ("q1", "q2", "q3", "q4"):
        for model in MODELS:
            summary.append(
                summarize_selected(
                    select_rows(item_rows, "variation_quartile_all", "all", bucket, model),
                    "variation_quartile_all",
                    "all",
                    bucket,
                    model,
                    "quartiles over all validation-200 items by BanglaTLit spelling-variation exposure",
                )
            )
    for dataset in ("benqa", "banglamath"):
        for bucket in ("q1", "q2", "q3", "q4"):
            for model in MODELS:
                summary.append(
                    summarize_selected(
                        select_rows(
                            item_rows, "variation_quartile_by_dataset", dataset, bucket, model
                        ),
                        "variation_quartile_by_dataset",
                        dataset,
                        bucket,
                        model,
                        f"quartiles within {dataset} by BanglaTLit spelling-variation exposure",
                    )
                )
    return summary


def apply_main_interval_overrides(
    summary_rows: list[dict[str, Any]], interval_rows: list[dict[str, str]]
) -> None:
    intervals = {
        (row["model"], row["dataset"], row["comparison"]): row for row in interval_rows
    }
    for row in summary_rows:
        if row["section"] != "dataset_overall":
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


def row_for(
    rows: list[dict[str, Any]], section: str, dataset: str, bucket: str, model: str
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == section
        and row["dataset"] == dataset
        and row["bucket"] == bucket
        and row["model"] == model
    )


def ci_cell(row: dict[str, Any], prefix: str) -> str:
    return (
        f"{points(row[prefix])} pts "
        f"[{points(row[prefix + '_ci95_low'])}, {points(row[prefix + '_ci95_high'])}]"
    )


def summary_metric(summary_rows: list[dict[str, str]], metric: str) -> str:
    return next((row["value"] for row in summary_rows if row["metric"] == metric), "")


def add_model_table(
    lines: list[str],
    summary_rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    title: str,
) -> None:
    lines.extend(
        [
            f"### {title}",
            "",
            "| Model | n | Mean exposure | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |",
        ]
    )
    for model in MODELS:
        row = row_for(summary_rows, section, dataset, bucket, model)
        lines.append(
            f"| {model} | {row['n_items']} | {row['mean_spelling_variation_exposure']} | "
            f"{row['bangla_correct']}/{row['n_items']} | "
            f"{row['banglish_correct']}/{row['n_items']} | "
            f"{row['english_correct']}/{row['n_items']} | "
            f"{ci_cell(row, 'banglish_minus_bangla')} | "
            f"{ci_cell(row, 'banglish_minus_english')} | "
            f"{row['banglish_fragile_items']} |"
        )
    lines.append("")


def add_quartile_direction_table(
    lines: list[str], summary_rows: list[dict[str, Any]]
) -> None:
    lines.extend(
        [
            "## All-200 Variation-Exposure Direction Check",
            "",
            "| Exposure bucket | Model | n | Mean exposure | Bangla | Banglish | English | Direction |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for bucket in ("q1", "q2", "q3", "q4"):
        for model in MODELS:
            row = row_for(summary_rows, "variation_quartile_all", "all", bucket, model)
            direction = (
                "below Bangla and English"
                if int(row["banglish_correct"]) < int(row["bangla_correct"])
                and int(row["banglish_correct"]) < int(row["english_correct"])
                else "mixed"
            )
            lines.append(
                f"| `{bucket}` | {model} | {row['n_items']} | "
                f"{row['mean_spelling_variation_exposure']} | "
                f"{row['bangla_correct']} | {row['banglish_correct']} | "
                f"{row['english_correct']} | {direction} |"
            )
    lines.append("")


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    variation_summary_rows: list[dict[str, str]],
    validation_path: Path,
    fragility_path: Path,
    variation_tokens_path: Path,
    variation_summary_path: Path,
    interval_path: Path,
    items_output: Path,
    summary_output: Path,
) -> None:
    q4_rows = [
        row_for(summary_rows, "variation_quartile_all", "all", "q4", model) for model in MODELS
    ]
    q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in q4_rows
    )
    all_quartile_rows = [
        row
        for row in summary_rows
        if row["section"] == "variation_quartile_all" and row["dataset"] == "all"
    ]
    all_quartile_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in all_quartile_rows
    )
    aligned = summary_metric(variation_summary_rows, "aligned_token_pairs")
    repeated = summary_metric(
        variation_summary_rows, "bangla_tokens_with_2plus_repeated_latin_variants_min3"
    )
    rows_aligned = summary_metric(variation_summary_rows, "rows_token_aligned")
    lines = [
        "# V5 BanglaTLit Spelling-Variation Sensitivity",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Inputs And Outputs",
        "",
        f"- Frozen-v5 slice: `{repo_path(validation_path)}`",
        f"- Fragility/correctness items: `{repo_path(fragility_path)}`",
        f"- BanglaTLit spelling-variation tokens: `{repo_path(variation_tokens_path)}`",
        f"- BanglaTLit spelling-variation summary: `{repo_path(variation_summary_path)}`",
        f"- Main dataset intervals for all-item rows: `{repo_path(interval_path)}`",
        f"- Per-model item output: `{repo_path(items_output)}`",
        f"- Per-model summary output: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        (
            f"- The BanglaTLit alignment contributes {aligned} aligned token pairs "
            f"from {rows_aligned} token-aligned rows and identifies {repeated} "
            "Bangla tokens with at least two repeated Latin variants."
        ),
        "- This audit scores each frozen-v5 content Banglish item by exposure to",
        "  those repeated-variant Latin spellings.",
        (
            "- In the highest spelling-variation-exposure all-200 quartile, reviewed "
            "Banglish remains below both Bangla and English for every thesis-facing "
            "Qwen row."
            if q4_direction_ok
            else "- The highest spelling-variation-exposure quartile has mixed direction."
        ),
        (
            "- The below-Bangla-and-English direction holds in all but the lowest "
            "all-200 exposure quartile, where Qwen2.5-3B ties Bangla at 16/50."
            if not all_quartile_direction_ok
            else "- The below-Bangla-and-English direction holds in every all-200 exposure quartile."
        ),
        "- This is descriptive naturalness evidence, not a causal spelling-variation",
        "  mechanism.",
        "",
    ]
    add_model_table(
        lines,
        summary_rows,
        "dataset_overall",
        "all",
        "all",
        "All Frozen-V5 Items",
    )
    add_model_table(
        lines,
        summary_rows,
        "variation_quartile_all",
        "all",
        "q4",
        "Highest Spelling-Variation Exposure Quartile",
    )
    add_model_table(
        lines,
        summary_rows,
        "variation_quartile_by_dataset",
        "benqa",
        "q4",
        "Highest BEnQA Spelling-Variation Exposure Quartile",
    )
    add_quartile_direction_table(lines, summary_rows)
    lines.extend(
        [
            "## Interpretation",
            "",
            "BanglaTLit shows that natural Romanized Bangla has many repeated spelling",
            "variants. The frozen-v5 benchmark is still controlled educational",
            "Banglish, but high exposure to BanglaTLit repeated-variant spellings",
            "does not remove the reviewed-Banglish deficit. The lowest-exposure",
            "bucket is mixed for Qwen2.5-3B, so this audit should be cited as",
            "limitations/robustness evidence rather than a monotonic feature effect.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_banglatlit_spelling_variation_sensitivity.py`",
            f"- Per-model item rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "- Exposure metric: for each content token that appears as a repeated",
            "  BanglaTLit Latin variant, add `max_repeated_variants - 1`, divided by",
            "  content token count.",
            "- Bootstrap: paired item resampling within each model/bucket, 5,000 samples.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--fragility-items", type=Path, default=DEFAULT_FRAGILITY_ITEMS)
    parser.add_argument("--variation-tokens", type=Path, default=DEFAULT_VARIATION_TOKENS)
    parser.add_argument("--variation-summary", type=Path, default=DEFAULT_VARIATION_SUMMARY)
    parser.add_argument("--dataset-intervals", type=Path, default=DEFAULT_DATASET_INTERVALS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(
        load_validation_rows(args.validation),
        read_csv(args.fragility_items),
        build_variation_lexicon(read_csv(args.variation_tokens)),
    )
    summary_rows = build_summary_rows(item_rows)
    apply_main_interval_overrides(summary_rows, read_csv(args.dataset_intervals))
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(
        args.report_output,
        item_rows,
        summary_rows,
        read_csv(args.variation_summary),
        args.validation,
        args.fragility_items,
        args.variation_tokens,
        args.variation_summary,
        args.dataset_intervals,
        args.items_output,
        args.summary_output,
    )
    q4_rows = [
        row_for(summary_rows, "variation_quartile_all", "all", "q4", model) for model in MODELS
    ]
    q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in q4_rows
    )
    print(
        " | ".join(
            [
                f"items={len(item_rows)}",
                f"summary_rows={len(summary_rows)}",
                f"all_q4_direction_ok={q4_direction_ok}",
                f"report={args.report_output}",
            ]
        )
    )


if __name__ == "__main__":
    main()
