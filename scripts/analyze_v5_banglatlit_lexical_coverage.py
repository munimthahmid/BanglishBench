#!/usr/bin/env python3
"""Join frozen-v5 Banglish items with BanglaTLit lexical coverage."""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import statistics
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALIDATION = ROOT / "data/slices/validation_200_v5.jsonl"
DEFAULT_FRAGILITY_ITEMS = ROOT / "results/analysis/v5_banglish_fragility_items.csv"
DEFAULT_BANGLATLIT = [
    ROOT / "literature/code/BanglaTLit/data/BanglaTLiT_val.csv",
    ROOT / "literature/code/BanglaTLit/data/BanglaTLiT_test.csv",
]
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_banglatlit_lexical_coverage_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_banglatlit_lexical_coverage_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_banglatlit_lexical_coverage.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
DATASETS = ("all", "benqa", "banglamath")
LATIN_TOKEN_RE = re.compile(r"[A-Za-z]+")
OPTION_LINE_RE = re.compile(r"^\s*[A-D][\).]\s+")
BOOTSTRAP_ITERATIONS = 5000
BOOTSTRAP_SEED = 20260531


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
    # Length-1 tokens are often roman numerals, option labels, or particles.
    return [token.lower() for token in LATIN_TOKEN_RE.findall(text) if len(token) >= 2]


def build_banglatlit_vocab(paths: list[Path]) -> tuple[Counter[str], int]:
    vocab: Counter[str] = Counter()
    rows = 0
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                rows += 1
                vocab.update(latin_tokens(str(row.get("text_transliterated", ""))))
    return vocab, rows


def load_validation_items(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            rows.append(
                {
                    "id": str(row["id"]),
                    "dataset": str(row.get("dataset", "")),
                    "domain": str(row.get("domain", "")),
                    "subject": str(metadata.get("subject", "")),
                    "grade": str(metadata.get("grade", "")),
                    "task_type": str(row.get("task_type", "")),
                    "quality_status": str(row.get("quality_status", "")),
                    "review_label": str(row.get("banglish_review", {}).get("label", "unreviewed"))
                    if isinstance(row.get("banglish_review"), dict)
                    else "unreviewed",
                    "banglish": str(row.get("banglish_clean", "")),
                }
            )
    return rows


def to_int(value: Any) -> int:
    return int(str(value).strip() or 0)


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def percent(count: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * count / denominator:.1f}%"


def points(value: float) -> str:
    pct = value * 100
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.1f}"


def stable_seed(label: str) -> int:
    return BOOTSTRAP_SEED + sum((index + 1) * ord(char) for index, char in enumerate(label))


def bootstrap_delta(rows: list[dict[str, Any]], seed_label: str) -> tuple[float, float, float]:
    denominator = len(rows) * len(MODELS)
    if not rows or denominator == 0:
        return 0.0, 0.0, 0.0
    observed = (
        sum(to_int(row["banglish_correct_models"]) - to_int(row["bangla_correct_models"]) for row in rows)
        / denominator
    )
    rng = random.Random(stable_seed(seed_label))
    draws: list[float] = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        total = 0
        for _i in range(len(rows)):
            row = rng.choice(rows)
            total += to_int(row["banglish_correct_models"]) - to_int(row["bangla_correct_models"])
        draws.append(total / denominator)
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    return observed, low, high


def build_item_rows(
    validation_rows: list[dict[str, Any]],
    fragility_rows: list[dict[str, str]],
    banglatlit_vocab: Counter[str],
) -> list[dict[str, Any]]:
    fragility_by_id = {row["id"]: row for row in fragility_rows}
    item_rows: list[dict[str, Any]] = []
    for row in validation_rows:
        fragility = fragility_by_id[row["id"]]
        content = strip_eval_scaffold(row["banglish"])
        tokens = latin_tokens(content)
        unique_tokens = sorted(set(tokens))
        seen_tokens = [token for token in tokens if token in banglatlit_vocab]
        frequent_tokens = [token for token in tokens if banglatlit_vocab.get(token, 0) >= 5]
        seen_unique = [token for token in unique_tokens if token in banglatlit_vocab]
        unseen_unique = [token for token in unique_tokens if token not in banglatlit_vocab]
        token_count = len(tokens)
        unique_count = len(unique_tokens)
        item_rows.append(
            {
                "id": row["id"],
                "dataset": row["dataset"],
                "domain": row["domain"],
                "subject": row["subject"],
                "grade": row["grade"],
                "task_type": row["task_type"],
                "quality_status": row["quality_status"],
                "review_label": row["review_label"],
                "content_token_count": token_count,
                "unique_content_token_count": unique_count,
                "banglatlit_seen_token_count": len(seen_tokens),
                "banglatlit_seen_unique_token_count": len(seen_unique),
                "banglatlit_frequent_token_count": len(frequent_tokens),
                "token_coverage": rate(len(seen_tokens), token_count),
                "unique_token_coverage": rate(len(seen_unique), unique_count),
                "frequent_token_coverage": rate(len(frequent_tokens), token_count),
                "top_unseen_tokens": "; ".join(unseen_unique[:12]),
                "bangla_correct_models": to_int(fragility["bangla_correct_models"]),
                "banglish_correct_models": to_int(fragility["banglish_correct_models"]),
                "english_correct_models": to_int(fragility["english_correct_models"]),
                "banglish_fragility_events": to_int(fragility["banglish_fragility_events"]),
                "strict_bangla_english_fragility_events": to_int(
                    fragility["strict_bangla_english_fragility_events"]
                ),
                "banglish_preview": str(fragility.get("banglish_preview", "")),
            }
        )
    return item_rows


def rows_for_dataset(rows: list[dict[str, Any]], dataset: str) -> list[dict[str, Any]]:
    if dataset == "all":
        return rows
    return [row for row in rows if row["dataset"] == dataset]


def quartile_chunks(rows: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    sorted_rows = sorted(rows, key=lambda row: (float(row["token_coverage"]), str(row["id"])))
    chunks: list[tuple[str, list[dict[str, Any]]]] = []
    n = len(sorted_rows)
    for index in range(4):
        start = index * n // 4
        end = (index + 1) * n // 4
        chunks.append((f"q{index + 1}", sorted_rows[start:end]))
    return chunks


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(statistics.median(values), 4)


def summarize_rows(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
    detail: str,
) -> dict[str, Any]:
    denominator = len(rows) * len(MODELS)
    bangla = sum(to_int(row["bangla_correct_models"]) for row in rows)
    banglish = sum(to_int(row["banglish_correct_models"]) for row in rows)
    english = sum(to_int(row["english_correct_models"]) for row in rows)
    delta = bootstrap_delta(rows, f"{section}:{dataset}:{bucket}")
    token_coverages = [float(row["token_coverage"]) for row in rows]
    unique_coverages = [float(row["unique_token_coverage"]) for row in rows]
    total_tokens = sum(to_int(row["content_token_count"]) for row in rows)
    seen_tokens = sum(to_int(row["banglatlit_seen_token_count"]) for row in rows)
    return {
        "section": section,
        "dataset": dataset,
        "bucket": bucket,
        "n_items": len(rows),
        "model_item_slots": denominator,
        "mean_token_coverage": round(sum(token_coverages) / len(rows), 4) if rows else 0.0,
        "median_token_coverage": median(token_coverages),
        "mean_unique_token_coverage": round(sum(unique_coverages) / len(rows), 4) if rows else 0.0,
        "total_content_tokens": total_tokens,
        "banglatlit_seen_tokens": seen_tokens,
        "pooled_token_coverage": rate(seen_tokens, total_tokens),
        "bangla_correct": bangla,
        "banglish_correct": banglish,
        "english_correct": english,
        "bangla_accuracy": rate(bangla, denominator),
        "banglish_accuracy": rate(banglish, denominator),
        "english_accuracy": rate(english, denominator),
        "banglish_minus_bangla": round(delta[0], 4),
        "banglish_minus_bangla_ci95_low": round(delta[1], 4),
        "banglish_minus_bangla_ci95_high": round(delta[2], 4),
        "banglish_fragility_events": sum(to_int(row["banglish_fragility_events"]) for row in rows),
        "strict_bangla_english_fragility_events": sum(
            to_int(row["strict_bangla_english_fragility_events"]) for row in rows
        ),
        "detail": detail,
    }


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for dataset in DATASETS:
        rows = rows_for_dataset(item_rows, dataset)
        summary.append(
            summarize_rows(rows, "dataset_overall", dataset, "all", "all rows")
        )
    for bucket, rows in quartile_chunks(item_rows):
        summary.append(
            summarize_rows(
                rows,
                "coverage_quartile_all",
                "all",
                bucket,
                "quartiles over all validation-200 items by exact BanglaTLit token coverage",
            )
        )
    for dataset in ("benqa", "banglamath"):
        for bucket, rows in quartile_chunks(rows_for_dataset(item_rows, dataset)):
            summary.append(
                summarize_rows(
                    rows,
                    "coverage_quartile_by_dataset",
                    dataset,
                    bucket,
                    f"quartiles within {dataset} by exact BanglaTLit token coverage",
                )
            )
    return summary


def row_for(
    rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    bucket: str,
) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == section and row["dataset"] == dataset and row["bucket"] == bucket
    )


def delta_cell(row: dict[str, Any]) -> str:
    return (
        f"{points(float(row['banglish_minus_bangla']))} pts, CI "
        f"[{points(float(row['banglish_minus_bangla_ci95_low']))},"
        f"{points(float(row['banglish_minus_bangla_ci95_high']))}]"
    )


def success_cell(row: dict[str, Any], key: str) -> str:
    return f"{row[key]}/{row['model_item_slots']} ({percent(to_int(row[key]), to_int(row['model_item_slots']))})"


def add_quartile_table(
    lines: list[str],
    summary_rows: list[dict[str, Any]],
    section: str,
    dataset: str,
    title: str,
) -> None:
    lines.extend(
        [
            f"### {title}",
            "",
            "| Bucket | Items | Mean coverage | Bangla slots | Reviewed Banglish slots | English slots | Fragility events | Banglish - Bangla |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for bucket in ("q1", "q2", "q3", "q4"):
        row = row_for(summary_rows, section, dataset, bucket)
        lines.append(
            "| "
            f"`{bucket}` | {row['n_items']} | {float(row['mean_token_coverage']) * 100:.1f}% | "
            f"{success_cell(row, 'bangla_correct')} | "
            f"{success_cell(row, 'banglish_correct')} | "
            f"{success_cell(row, 'english_correct')} | "
            f"{row['banglish_fragility_events']} | {delta_cell(row)} |"
        )
    lines.append("")


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
    validation_path: Path,
    banglatlit_paths: list[Path],
    vocab: Counter[str],
    banglatlit_rows: int,
) -> None:
    all_overall = row_for(summary_rows, "dataset_overall", "all", "all")
    benqa_overall = row_for(summary_rows, "dataset_overall", "benqa", "all")
    math_overall = row_for(summary_rows, "dataset_overall", "banglamath", "all")
    all_q1 = row_for(summary_rows, "coverage_quartile_all", "all", "q1")
    all_q4 = row_for(summary_rows, "coverage_quartile_all", "all", "q4")
    benqa_q4 = row_for(summary_rows, "coverage_quartile_by_dataset", "benqa", "q4")

    lines = [
        "# V5 BanglaTLit Lexical Coverage Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This no-spend audit compares frozen-v5 controlled Banglish prompts with",
        "BanglaTLit's naturally written Romanized Bangla. It is a conservative",
        "exact-token overlap check, not a semantic naturalness score.",
        "",
        "## Inputs And Outputs",
        "",
        f"- Frozen-v5 slice: `{repo_path(validation_path)}`",
        f"- BanglaTLit files: {', '.join(f'`{repo_path(path)}`' for path in banglatlit_paths)}",
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        f"- BanglaTLit rows used: {banglatlit_rows}",
        f"- BanglaTLit exact Latin vocabulary size: {len(vocab)} token types",
        "",
        "## Headline",
        "",
        f"- Frozen-v5 content Banglish has low exact overlap with BanglaTLit: mean",
        f"  token coverage is {float(all_overall['mean_token_coverage']) * 100:.1f}% overall,",
        f"  {float(benqa_overall['mean_token_coverage']) * 100:.1f}% for BEnQA, and",
        f"  {float(math_overall['mean_token_coverage']) * 100:.1f}% for BanglaMATH.",
        "- This reinforces the current limitation: the benchmark is controlled",
        "  educational Banglish, not a sample of naturally occurring chat Banglish.",
        "- The script gap is not confined to the least-attested lexical items.",
        f"  In the highest-coverage all-200 quartile, reviewed Banglish has",
        f"  {all_q4['banglish_correct']}/{all_q4['model_item_slots']} correct slots",
        f"  versus Bangla {all_q4['bangla_correct']}/{all_q4['model_item_slots']}",
        f"  ({delta_cell(all_q4)}).",
        f"- The lowest-coverage all-200 quartile has reviewed Banglish",
        f"  {all_q1['banglish_correct']}/{all_q1['model_item_slots']} versus Bangla",
        f"  {all_q1['bangla_correct']}/{all_q1['model_item_slots']} ({delta_cell(all_q1)}).",
        f"- In the highest-coverage BEnQA quartile, reviewed Banglish has",
        f"  {benqa_q4['banglish_correct']}/{benqa_q4['model_item_slots']} correct slots",
        f"  versus Bangla {benqa_q4['bangla_correct']}/{benqa_q4['model_item_slots']}",
        f"  ({delta_cell(benqa_q4)}).",
        "",
        "## Coverage By Dataset",
        "",
        "| Dataset | Items | Mean exact token coverage | Pooled token coverage | Bangla slots | Reviewed Banglish slots | Banglish - Bangla |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in (all_overall, benqa_overall, math_overall):
        lines.append(
            "| "
            f"{row['dataset']} | {row['n_items']} | "
            f"{float(row['mean_token_coverage']) * 100:.1f}% | "
            f"{float(row['pooled_token_coverage']) * 100:.1f}% | "
            f"{success_cell(row, 'bangla_correct')} | "
            f"{success_cell(row, 'banglish_correct')} | "
            f"{delta_cell(row)} |"
        )
    lines.append("")

    lines.extend(
        [
            "## Coverage Quartiles",
            "",
            "Quartiles are sorted by exact token coverage against BanglaTLit. The",
            "all-200 quartiles have 50 items each; BEnQA quartiles have 36 items",
            "each. The confidence intervals resample validation items within the",
            "bucket.",
            "",
        ]
    )
    add_quartile_table(lines, summary_rows, "coverage_quartile_all", "all", "All 200 Items")
    add_quartile_table(lines, summary_rows, "coverage_quartile_by_dataset", "benqa", "BEnQA")
    add_quartile_table(lines, summary_rows, "coverage_quartile_by_dataset", "banglamath", "BanglaMATH")

    lines.extend(
        [
            "## Interpretation",
            "",
            "- The low exact overlap is useful limitations evidence. Controlled",
            "  curriculum Banglish contains technical vocabulary, formulas, and",
            "  romanization choices that are not frequent in BanglaTLit.",
            "- The high-coverage quartiles remaining negative weakens a simple",
            "  explanation that the Banglish deficit is only out-of-vocabulary",
            "  conversational-naturalness mismatch.",
            "- Exact token matching is deliberately conservative. It misses related",
            "  spellings and morphology, and BanglaTLit is conversational rather than",
            "  educational. Use this audit as a bridge between benchmark naturalness",
            "  and failure analysis, not as a causal lexical mechanism.",
            "",
            "## Reproducibility",
            "",
            "- Builder: `scripts/analyze_v5_banglatlit_lexical_coverage.py`",
            f"- Input items: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "- Token rule: Latin alphabetic tokens of length at least 2 after removing",
            "  answer instructions and MCQ option lines.",
            "- Bootstrap: item-cluster resampling within each bucket, 5,000 samples.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--fragility-items", type=Path, default=DEFAULT_FRAGILITY_ITEMS)
    parser.add_argument("--banglatlit", type=Path, nargs="+", default=DEFAULT_BANGLATLIT)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vocab, banglatlit_rows = build_banglatlit_vocab(args.banglatlit)
    item_rows = build_item_rows(
        load_validation_items(args.validation),
        read_csv(args.fragility_items),
        vocab,
    )
    summary_rows = build_summary_rows(item_rows)
    item_fields = [
        "id",
        "dataset",
        "domain",
        "subject",
        "grade",
        "task_type",
        "quality_status",
        "review_label",
        "content_token_count",
        "unique_content_token_count",
        "banglatlit_seen_token_count",
        "banglatlit_seen_unique_token_count",
        "banglatlit_frequent_token_count",
        "token_coverage",
        "unique_token_coverage",
        "frequent_token_coverage",
        "top_unseen_tokens",
        "bangla_correct_models",
        "banglish_correct_models",
        "english_correct_models",
        "banglish_fragility_events",
        "strict_bangla_english_fragility_events",
        "banglish_preview",
    ]
    summary_fields = [
        "section",
        "dataset",
        "bucket",
        "n_items",
        "model_item_slots",
        "mean_token_coverage",
        "median_token_coverage",
        "mean_unique_token_coverage",
        "total_content_tokens",
        "banglatlit_seen_tokens",
        "pooled_token_coverage",
        "bangla_correct",
        "banglish_correct",
        "english_correct",
        "bangla_accuracy",
        "banglish_accuracy",
        "english_accuracy",
        "banglish_minus_bangla",
        "banglish_minus_bangla_ci95_low",
        "banglish_minus_bangla_ci95_high",
        "banglish_fragility_events",
        "strict_bangla_english_fragility_events",
        "detail",
    ]
    write_csv(args.items_output, item_rows, item_fields)
    write_csv(args.summary_output, summary_rows, summary_fields)
    write_report(
        args.report_output,
        item_rows,
        summary_rows,
        args.items_output,
        args.summary_output,
        args.validation,
        args.banglatlit,
        vocab,
        banglatlit_rows,
    )
    print(
        f"items={len(item_rows)} summary_rows={len(summary_rows)} "
        f"vocab={len(vocab)} report={args.report_output}"
    )


if __name__ == "__main__":
    main()
