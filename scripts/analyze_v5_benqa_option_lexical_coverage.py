#!/usr/bin/env python3
"""Audit BEnQA stem/option lexical coverage against BanglaTLit."""

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
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_option_lexical_coverage_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_option_lexical_coverage_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_option_lexical_coverage.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B", "Qwen3-4B")
SURFACES = ("stem", "options_all", "gold_option")
TOKEN_RE = re.compile(r"[A-Za-z]+")
OPTION_RE = re.compile(r"^\s*([A-D])[\).]\s+(.*)$")
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


def latin_tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if len(token) >= 2]


def compact_preview(text: str, limit: int = 100) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def to_int(value: Any) -> int:
    return int(str(value).strip() or 0)


def rate(count: int, denominator: int) -> float:
    return round(count / denominator, 4) if denominator else 0.0


def percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def points(value: float) -> str:
    scaled = value * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(statistics.median(values), 4)


def stable_seed(label: str) -> int:
    return BOOTSTRAP_SEED + sum((index + 1) * ord(char) for index, char in enumerate(label))


def build_banglatlit_vocab(paths: list[Path]) -> tuple[Counter[str], int]:
    vocab: Counter[str] = Counter()
    rows = 0
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                rows += 1
                vocab.update(latin_tokens(str(row.get("text_transliterated", ""))))
    return vocab, rows


def parse_benqa_surfaces(text: str, answer: str) -> dict[str, Any]:
    stem_lines: list[str] = []
    option_texts: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Answer with only") or stripped.startswith("Return only"):
            continue
        match = OPTION_RE.match(stripped)
        if match:
            option_texts[match.group(1)] = match.group(2)
        else:
            stem_lines.append(stripped)
    return {
        "stem": "\n".join(stem_lines),
        "options_all": " ".join(option_texts.get(label, "") for label in ("A", "B", "C", "D")),
        "gold_option": option_texts.get(str(answer).strip(), ""),
        "options_parsed": sum(1 for label in ("A", "B", "C", "D") if option_texts.get(label)),
    }


def surface_features(text: str, vocab: Counter[str]) -> dict[str, Any]:
    tokens = latin_tokens(text)
    unique_tokens = sorted(set(tokens))
    seen_tokens = [token for token in tokens if token in vocab]
    seen_unique = [token for token in unique_tokens if token in vocab]
    unseen_unique = [token for token in unique_tokens if token not in vocab]
    return {
        "token_count": len(tokens),
        "seen_token_count": len(seen_tokens),
        "unique_token_count": len(unique_tokens),
        "seen_unique_token_count": len(seen_unique),
        "coverage": rate(len(seen_tokens), len(tokens)),
        "unique_coverage": rate(len(seen_unique), len(unique_tokens)),
        "top_unseen": "; ".join(unseen_unique[:12]),
        "preview": compact_preview(text),
    }


def load_validation_items(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("dataset") != "benqa":
                continue
            metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            review = row.get("banglish_review") if isinstance(row.get("banglish_review"), dict) else {}
            rows.append(
                {
                    "id": str(row["id"]),
                    "dataset": str(row.get("dataset", "")),
                    "domain": str(row.get("domain", "")),
                    "subject": str(metadata.get("subject", "")),
                    "grade": str(metadata.get("grade", "")),
                    "task_type": str(row.get("task_type", "")),
                    "quality_status": str(row.get("quality_status", "")),
                    "review_label": str(review.get("label", "unreviewed")),
                    "answer": str(row.get("answer", "")),
                    "banglish": str(row.get("banglish_clean", "")),
                }
            )
    return rows


def build_item_rows(
    validation_rows: list[dict[str, Any]],
    fragility_rows: list[dict[str, str]],
    banglatlit_vocab: Counter[str],
) -> list[dict[str, Any]]:
    fragility_by_id = {row["id"]: row for row in fragility_rows}
    item_rows: list[dict[str, Any]] = []
    for row in validation_rows:
        fragility = fragility_by_id[row["id"]]
        surfaces = parse_benqa_surfaces(row["banglish"], row["answer"])
        out = {
            "id": row["id"],
            "dataset": row["dataset"],
            "domain": row["domain"],
            "subject": row["subject"],
            "grade": row["grade"],
            "task_type": row["task_type"],
            "quality_status": row["quality_status"],
            "review_label": row["review_label"],
            "answer": row["answer"],
            "options_parsed": surfaces["options_parsed"],
            "bangla_correct_models": to_int(fragility["bangla_correct_models"]),
            "banglish_correct_models": to_int(fragility["banglish_correct_models"]),
            "english_correct_models": to_int(fragility["english_correct_models"]),
            "banglish_fragility_events": to_int(fragility["banglish_fragility_events"]),
            "strict_bangla_english_fragility_events": to_int(
                fragility["strict_bangla_english_fragility_events"]
            ),
            "banglish_preview": str(fragility.get("banglish_preview", "")),
        }
        for surface in SURFACES:
            features = surface_features(str(surfaces[surface]), banglatlit_vocab)
            for key, value in features.items():
                out[f"{surface}_{key}"] = value
        item_rows.append(out)
    return item_rows


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
        for _index in range(len(rows)):
            row = rng.choice(rows)
            total += to_int(row["banglish_correct_models"]) - to_int(row["bangla_correct_models"])
        draws.append(total / denominator)
    draws.sort()
    low = draws[int(0.025 * (len(draws) - 1))]
    high = draws[int(0.975 * (len(draws) - 1))]
    return observed, low, high


def summarize_rows(
    rows: list[dict[str, Any]],
    section: str,
    surface: str,
    bucket: str,
    detail: str,
) -> dict[str, Any]:
    denominator = len(rows) * len(MODELS)
    token_counts = [to_int(row[f"{surface}_token_count"]) for row in rows]
    coverage_values = [float(row[f"{surface}_coverage"]) for row in rows]
    unique_coverage_values = [float(row[f"{surface}_unique_coverage"]) for row in rows]
    total_tokens = sum(token_counts)
    seen_tokens = sum(to_int(row[f"{surface}_seen_token_count"]) for row in rows)
    bangla = sum(to_int(row["bangla_correct_models"]) for row in rows)
    banglish = sum(to_int(row["banglish_correct_models"]) for row in rows)
    english = sum(to_int(row["english_correct_models"]) for row in rows)
    delta, ci_low, ci_high = bootstrap_delta(rows, f"{section}:{surface}:{bucket}")
    return {
        "section": section,
        "surface": surface,
        "bucket": bucket,
        "n_items": len(rows),
        "model_item_slots": denominator,
        "mean_token_count": round(sum(token_counts) / len(rows), 4) if rows else 0.0,
        "mean_coverage": round(sum(coverage_values) / len(rows), 4) if rows else 0.0,
        "median_coverage": median(coverage_values),
        "mean_unique_coverage": round(sum(unique_coverage_values) / len(rows), 4) if rows else 0.0,
        "total_tokens": total_tokens,
        "seen_tokens": seen_tokens,
        "pooled_coverage": rate(seen_tokens, total_tokens),
        "bangla_correct": bangla,
        "banglish_correct": banglish,
        "english_correct": english,
        "bangla_accuracy": rate(bangla, denominator),
        "banglish_accuracy": rate(banglish, denominator),
        "english_accuracy": rate(english, denominator),
        "banglish_minus_bangla": round(delta, 4),
        "banglish_minus_bangla_ci95_low": round(ci_low, 4),
        "banglish_minus_bangla_ci95_high": round(ci_high, 4),
        "banglish_fragility_events": sum(to_int(row["banglish_fragility_events"]) for row in rows),
        "strict_bangla_english_fragility_events": sum(
            to_int(row["strict_bangla_english_fragility_events"]) for row in rows
        ),
        "detail": detail,
    }


def quartile_chunks(rows: list[dict[str, Any]], surface: str) -> list[tuple[str, list[dict[str, Any]]]]:
    sorted_rows = sorted(rows, key=lambda row: (float(row[f"{surface}_coverage"]), str(row["id"])))
    chunks: list[tuple[str, list[dict[str, Any]]]] = []
    n = len(sorted_rows)
    for index in range(4):
        start = index * n // 4
        end = (index + 1) * n // 4
        chunks.append((f"q{index + 1}", sorted_rows[start:end]))
    return chunks


def build_summary_rows(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for surface in SURFACES:
        summary.append(
            summarize_rows(
                item_rows,
                "surface_overall",
                surface,
                "all",
                "all BEnQA rows",
            )
        )
        for bucket, bucket_rows in quartile_chunks(item_rows, surface):
            summary.append(
                summarize_rows(
                    bucket_rows,
                    "coverage_quartile",
                    surface,
                    bucket,
                    f"BEnQA quartiles sorted by {surface} exact BanglaTLit token coverage",
                )
            )
    return summary


def find_row(rows: list[dict[str, Any]], section: str, surface: str, bucket: str) -> dict[str, Any]:
    return next(
        row
        for row in rows
        if row["section"] == section and row["surface"] == surface and row["bucket"] == bucket
    )


def row_line(row: dict[str, Any]) -> str:
    return (
        f"| `{row['surface']}` | `{row['bucket']}` | {row['n_items']} | "
        f"{percent(float(row['mean_coverage']))} | {percent(float(row['pooled_coverage']))} | "
        f"{row['bangla_correct']}/{row['model_item_slots']} | "
        f"{row['banglish_correct']}/{row['model_item_slots']} | "
        f"{row['english_correct']}/{row['model_item_slots']} | "
        f"{points(float(row['banglish_minus_bangla']))} pts, CI "
        f"[{points(float(row['banglish_minus_bangla_ci95_low']))},"
        f"{points(float(row['banglish_minus_bangla_ci95_high']))}] | "
        f"{row['banglish_fragility_events']} |"
    )


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation: Path,
    fragility_items: Path,
    banglatlit_paths: list[Path],
    items_output: Path,
    summary_output: Path,
    banglatlit_vocab_size: int,
    banglatlit_rows: int,
) -> None:
    stem_overall = find_row(summary_rows, "surface_overall", "stem", "all")
    option_overall = find_row(summary_rows, "surface_overall", "options_all", "all")
    gold_overall = find_row(summary_rows, "surface_overall", "gold_option", "all")
    option_q4 = find_row(summary_rows, "coverage_quartile", "options_all", "q4")
    gold_q4 = find_row(summary_rows, "coverage_quartile", "gold_option", "q4")
    stem_q4 = find_row(summary_rows, "coverage_quartile", "stem", "q4")
    option_parse_issues = sum(1 for row in item_rows if to_int(row["options_parsed"]) != 4)

    lines = [
        "# V5 BEnQA Option Lexical Coverage Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit separates BEnQA reviewed-Banglish prompt text into",
        "question stem, all answer options, and the gold answer option. It compares",
        "each surface with BanglaTLit exact Latin-token coverage and then checks the",
        "frozen-v5 three-Qwen correctness gap inside coverage quartiles.",
        "",
        f"- Frozen-v5 slice: `{repo_path(validation)}`",
        f"- Fragility items: `{repo_path(fragility_items)}`",
        "- BanglaTLit files: "
        + ", ".join(f"`{repo_path(path)}`" for path in banglatlit_paths),
        f"- Item-level output: `{repo_path(items_output)}`",
        f"- Summary table: `{repo_path(summary_output)}`",
        f"- BanglaTLit rows used: {banglatlit_rows}",
        f"- BanglaTLit exact Latin vocabulary size: {banglatlit_vocab_size}",
        "",
        "## Headline",
        "",
        f"- BEnQA reviewed-Banglish stem coverage is {percent(float(stem_overall['mean_coverage']))}; "
        f"all-option coverage is lower at {percent(float(option_overall['mean_coverage']))}, "
        f"and gold-option coverage is {percent(float(gold_overall['mean_coverage']))}.",
        f"- Even in the highest all-option coverage quartile, reviewed Banglish is "
        f"{option_q4['banglish_correct']}/{option_q4['model_item_slots']} correct slots versus "
        f"Bangla {option_q4['bangla_correct']}/{option_q4['model_item_slots']} "
        f"({points(float(option_q4['banglish_minus_bangla']))} pts, CI "
        f"[{points(float(option_q4['banglish_minus_bangla_ci95_low']))},"
        f"{points(float(option_q4['banglish_minus_bangla_ci95_high']))}]).",
        f"- The highest gold-option coverage quartile is also negative: reviewed Banglish "
        f"{gold_q4['banglish_correct']}/{gold_q4['model_item_slots']} versus Bangla "
        f"{gold_q4['bangla_correct']}/{gold_q4['model_item_slots']} "
        f"({points(float(gold_q4['banglish_minus_bangla']))} pts).",
        f"- Option parsing is complete for {len(item_rows) - option_parse_issues}/{len(item_rows)} BEnQA rows.",
        "- Treat this as descriptive evidence about answer-choice lexical exposure, not",
        "  as a causal option-token mechanism.",
        "",
        "## Surface-Level Coverage",
        "",
        "| Surface | Bucket | Items | Mean coverage | Pooled coverage | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla | Fragility events |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for surface in SURFACES:
        lines.append(row_line(find_row(summary_rows, "surface_overall", surface, "all")))

    lines.extend(
        [
            "",
            "## Coverage Quartiles",
            "",
            "Quartiles are sorted separately for each surface. Each BEnQA quartile has",
            "36 items and 108 model-item slots.",
            "",
        ]
    )
    for surface, title in (
        ("stem", "Question Stem"),
        ("options_all", "All Answer Options"),
        ("gold_option", "Gold Answer Option"),
    ):
        lines.extend(
            [
                f"### {title}",
                "",
                "| Surface | Bucket | Items | Mean coverage | Pooled coverage | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla | Fragility events |",
                "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for bucket in ("q1", "q2", "q3", "q4"):
            lines.append(row_line(find_row(summary_rows, "coverage_quartile", surface, bucket)))
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "- BEnQA answer options have substantially lower exact overlap with",
            "  BanglaTLit than the stems, which is an important naturalness limitation:",
            "  many answer choices are curriculum terms rather than chat-style Banglish.",
        "- The highest option-coverage and gold-option-coverage quartile point",
        "  estimates are still negative, although their intervals cross zero.",
        "  This weakens a simple explanation that the main BEnQA gap is only",
        "  caused by completely unattested answer-choice strings.",
            "- The stem quartiles reproduce the existing lexical-coverage pattern; the",
            f"  highest stem quartile is {stem_q4['banglish_correct']}/{stem_q4['model_item_slots']}",
            f"  reviewed-Banglish slots versus {stem_q4['bangla_correct']}/{stem_q4['model_item_slots']}",
            "  Bangla slots.",
            "- Use this audit in the limitations and failure-analysis chapters: it",
            "  acknowledges option lexical exposure while preserving the controlled",
            "  paired-script result.",
            "",
            "## Reproducibility",
            "",
            f"- Builder: `{repo_path(Path(__file__))}`",
            f"- Item rows: {len(item_rows)}",
            f"- Summary rows: {len(summary_rows)}",
            "- Token rule: Latin alphabetic tokens of length at least 2.",
            "- Bootstrap: item-cluster resampling within each bucket, 5,000 samples.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    validation_rows = load_validation_items(args.validation)
    fragility_rows = read_csv(args.fragility_items)
    item_rows = build_item_rows(validation_rows, fragility_rows, vocab)
    summary_rows = build_summary_rows(item_rows)

    item_fieldnames = [
        "id",
        "dataset",
        "domain",
        "subject",
        "grade",
        "task_type",
        "quality_status",
        "review_label",
        "answer",
        "options_parsed",
        "stem_token_count",
        "stem_seen_token_count",
        "stem_unique_token_count",
        "stem_seen_unique_token_count",
        "stem_coverage",
        "stem_unique_coverage",
        "stem_top_unseen",
        "stem_preview",
        "options_all_token_count",
        "options_all_seen_token_count",
        "options_all_unique_token_count",
        "options_all_seen_unique_token_count",
        "options_all_coverage",
        "options_all_unique_coverage",
        "options_all_top_unseen",
        "options_all_preview",
        "gold_option_token_count",
        "gold_option_seen_token_count",
        "gold_option_unique_token_count",
        "gold_option_seen_unique_token_count",
        "gold_option_coverage",
        "gold_option_unique_coverage",
        "gold_option_top_unseen",
        "gold_option_preview",
        "bangla_correct_models",
        "banglish_correct_models",
        "english_correct_models",
        "banglish_fragility_events",
        "strict_bangla_english_fragility_events",
        "banglish_preview",
    ]
    summary_fieldnames = [
        "section",
        "surface",
        "bucket",
        "n_items",
        "model_item_slots",
        "mean_token_count",
        "mean_coverage",
        "median_coverage",
        "mean_unique_coverage",
        "total_tokens",
        "seen_tokens",
        "pooled_coverage",
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
    write_csv(args.items_output, item_rows, item_fieldnames)
    write_csv(args.summary_output, summary_rows, summary_fieldnames)
    write_report(
        args.report_output,
        item_rows,
        summary_rows,
        args.validation,
        args.fragility_items,
        args.banglatlit,
        args.items_output,
        args.summary_output,
        len(vocab),
        banglatlit_rows,
    )
    print(
        f"items={len(item_rows)} | summary_rows={len(summary_rows)} | "
        f"report={repo_path(args.report_output)}"
    )


if __name__ == "__main__":
    main()
