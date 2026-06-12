#!/usr/bin/env python3
"""Compare generated Bengali views with native-Bangla references on the dev slice."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import unicodedata
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = ROOT / "data/slices/validation_200_v4_dev50.jsonl"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/generated_bn_reference_similarity_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/generated_bn_reference_similarity_summary.csv"
DEFAULT_REPORT = ROOT / "reports/generated_bn_reference_similarity_dev50.md"
DEFAULT_GENERATED = [
    (
        "protected_phonetic_bangla",
        ROOT
        / "results/generated_views/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn.jsonl",
    ),
    (
        "protected_bnbphoneticparser",
        ROOT
        / "results/generated_views/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn.jsonl",
    ),
    (
        "protected_fms_byte_mbart",
        ROOT
        / "results/generated_views/fms_byte_protected_dev50_benqa_mcq_generated_bn.jsonl",
    ),
]

WHITESPACE_RE = re.compile(r"\s+")
BN_RE = re.compile(r"[\u0980-\u09ff]")
OUTPUT_FIELDS = [
    "generated_text",
    "generation_output",
    "rewritten_text",
    "output_text",
    "output",
    "text",
    "raw_output",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def output_text(row: dict[str, Any]) -> str:
    for field in OUTPUT_FIELDS:
        value = row.get(field)
        if value is not None:
            return str(value)
    return ""


def normalize(text: str) -> str:
    return WHITESPACE_RE.sub(" ", unicodedata.normalize("NFC", text)).strip()


def edit_distance(left: str, right: str) -> int:
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for left_index, left_char in enumerate(left, start=1):
        current = [left_index]
        for right_index, right_char in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1] + int(left_char != right_char),
                )
            )
        previous = current
    return previous[-1]


def mean(values: list[float]) -> float:
    return round(statistics.mean(values), 4) if values else 0.0


def median(values: list[float]) -> float:
    return round(statistics.median(values), 4) if values else 0.0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_generated_specs(values: list[str] | None) -> list[tuple[str, Path]]:
    if not values:
        return DEFAULT_GENERATED
    specs: list[tuple[str, Path]] = []
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Expected --generated LABEL=PATH, got: {value}")
        label, raw_path = value.split("=", 1)
        path = Path(raw_path)
        if not path.is_absolute():
            path = ROOT / path
        specs.append((label, path))
    return specs


def relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def write_report(
    path: Path,
    reference_path: Path,
    specs: list[tuple[str, Path]],
    items_path: Path,
    summary_path: Path,
    summary: list[dict[str, Any]],
) -> None:
    lines = [
        "# Generated-BN Reference Similarity: Dev50 BEnQA MCQ",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This report compares generated Bengali views with benchmark-provided",
        "native-Bangla references on the locked dev50 BEnQA MCQ subset. It is a",
        "privileged dev-only generator-selection diagnostic, not deployed",
        "accuracy and not a held-out mitigation result.",
        "",
        f"- Native reference slice: `{relative(reference_path)}`",
        f"- Item metrics: `{relative(items_path)}`",
        f"- Summary metrics: `{relative(summary_path)}`",
        "",
        "Generated inputs:",
        "",
    ]
    for label, generated_path in specs:
        lines.append(f"- `{label}`: `{relative(generated_path)}`")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Generator | n | Mean CER | Median CER | Mean sequence similarity | Mean Bengali ratio | Exact matches |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary:
        lines.append(
            "| {generator} | {n} | {mean_cer:.4f} | {median_cer:.4f} | "
            "{mean_sequence_similarity:.4f} | {mean_bengali_ratio:.4f} | "
            "{exact_match} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- Lower character error rate (CER) and higher sequence similarity mean",
            "  the generated view is textually closer to the native-Bangla reference.",
            "- Similarity does not prove semantic equivalence or downstream answer",
            "  improvement.",
            "- Generator selection remains dev-only until a routing rule is locked",
            "  and evaluated unchanged on held-out test items.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument(
        "--generated",
        action="append",
        help="Generated candidate as LABEL=PATH. Repeat for multiple candidates.",
    )
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    specs = parse_generated_specs(args.generated)
    references = {
        str(row["id"]): str(row["bangla"])
        for row in load_jsonl(args.reference)
        if row.get("dataset") == "benqa" and row.get("answer_type") == "choice"
    }

    items: list[dict[str, Any]] = []
    for generator, generated_path in specs:
        if not generated_path.is_file():
            raise SystemExit(f"Missing generated input: {generated_path}")
        generated_rows = {
            str(row["id"]): output_text(row) for row in load_jsonl(generated_path)
        }
        if set(generated_rows) != set(references):
            missing = sorted(set(references) - set(generated_rows))
            extra = sorted(set(generated_rows) - set(references))
            raise SystemExit(
                f"{generator}: key mismatch missing={missing[:5]} extra={extra[:5]}"
            )
        for item_id, reference in sorted(references.items()):
            generated = generated_rows[item_id]
            normalized_reference = normalize(reference)
            normalized_generated = normalize(generated)
            distance = edit_distance(normalized_reference, normalized_generated)
            reference_chars = len(normalized_reference)
            generated_chars = len(normalized_generated)
            items.append(
                {
                    "generator": generator,
                    "id": item_id,
                    "reference_chars": reference_chars,
                    "generated_chars": generated_chars,
                    "edit_distance": distance,
                    "cer": round(distance / max(reference_chars, 1), 4),
                    "sequence_similarity": round(
                        SequenceMatcher(
                            None, normalized_reference, normalized_generated
                        ).ratio(),
                        4,
                    ),
                    "bengali_ratio": round(
                        len(BN_RE.findall(normalized_generated))
                        / max(generated_chars, 1),
                        4,
                    ),
                    "exact_match": normalized_reference == normalized_generated,
                    "generated_preview": normalized_generated[:220],
                }
            )

    summary: list[dict[str, Any]] = []
    for generator, _ in specs:
        rows = [row for row in items if row["generator"] == generator]
        summary.append(
            {
                "generator": generator,
                "n": len(rows),
                "mean_cer": mean([float(row["cer"]) for row in rows]),
                "median_cer": median([float(row["cer"]) for row in rows]),
                "mean_sequence_similarity": mean(
                    [float(row["sequence_similarity"]) for row in rows]
                ),
                "mean_bengali_ratio": mean(
                    [float(row["bengali_ratio"]) for row in rows]
                ),
                "exact_match": sum(int(row["exact_match"]) for row in rows),
            }
        )
    summary.sort(key=lambda row: (float(row["mean_cer"]), str(row["generator"])))

    write_csv(args.items_output, items)
    write_csv(args.summary_output, summary)
    write_report(
        args.report_output,
        args.reference,
        specs,
        args.items_output,
        args.summary_output,
        summary,
    )
    print(f"items={len(items)}")
    print(f"summary={args.summary_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
