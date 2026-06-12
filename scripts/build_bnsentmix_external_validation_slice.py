#!/usr/bin/env python3
"""Build a balanced natural-code-mixed BnSentMix sentiment evaluation slice."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "literature/data/bnsentmix/dataset.csv"
DEFAULT_OUTPUT = ROOT / "data/slices/bnsentmix_balanced200_v1.jsonl"
DEFAULT_REPORT = ROOT / "reports/bnsentmix_external_validation_slice.md"
SOURCE_URL = "https://huggingface.co/datasets/aplycaebous/BnSentMix"
PAPER_URL = "https://aclanthology.org/2025.loreslm-1.4/"
EXPECTED_SOURCE_SHA256 = (
    "148f23eb3dc40c1012a973efec920eaccc39700a74e5bcfb56806b0bf389029d"
)
LABEL_MAP = {
    "0": "positive",
    "1": "negative",
    "2": "neutral",
    "3": "mixed",
}
LABELS = tuple(LABEL_MAP.values())


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_source(path: Path) -> tuple[list[dict[str, Any]], int]:
    if not path.exists():
        raise SystemExit(
            f"Missing {path}. Run: python3 scripts/fetch_bnsentmix.py"
        )
    actual_sha256 = sha256_file(path)
    if actual_sha256 != EXPECTED_SOURCE_SHA256:
        raise SystemExit(
            f"BnSentMix CSV hash mismatch: expected {EXPECTED_SOURCE_SHA256}, "
            f"got {actual_sha256}"
        )

    rows: list[dict[str, Any]] = []
    duplicates = 0
    seen_sentences: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["Sentence", "Label"]:
            raise SystemExit(f"Unexpected BnSentMix columns: {reader.fieldnames}")
        for source_row, row in enumerate(reader, start=2):
            sentence = str(row["Sentence"]).strip()
            raw_label = str(row["Label"]).strip()
            if not sentence:
                raise SystemExit(f"Empty sentence at source row {source_row}")
            if raw_label not in LABEL_MAP:
                raise SystemExit(
                    f"Unexpected label {raw_label!r} at source row {source_row}"
                )
            if sentence in seen_sentences:
                duplicates += 1
                continue
            seen_sentences.add(sentence)
            rows.append(
                {
                    "sentence": sentence,
                    "raw_label": raw_label,
                    "label": LABEL_MAP[raw_label],
                    "source_row": source_row,
                }
            )
    return rows, duplicates


def build_prompt(sentence: str) -> str:
    return (
        "Classify the sentiment of this naturally occurring Bengali-English "
        "code-mixed text.\n"
        "Return exactly one lowercase label: positive, negative, neutral, or mixed.\n\n"
        "Text:\n"
        f"{sentence}"
    )


def sample_rows(
    source_rows: list[dict[str, Any]],
    per_label: int,
    seed: int,
    source_file: Path,
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in source_rows:
        grouped[str(row["label"])].append(row)

    rng = random.Random(seed)
    selected: dict[str, list[dict[str, Any]]] = {}
    for label in LABELS:
        candidates = sorted(grouped[label], key=lambda row: int(row["source_row"]))
        if len(candidates) < per_label:
            raise SystemExit(
                f"Need {per_label} rows for {label}, got {len(candidates)}"
            )
        rng.shuffle(candidates)
        selected[label] = candidates[:per_label]

    output: list[dict[str, Any]] = []
    for index in range(per_label):
        for label in LABELS:
            source = selected[label][index]
            source_row = int(source["source_row"])
            output.append(
                {
                    "answer": label,
                    "answer_type": "sentiment",
                    "dataset": "bnsentmix",
                    "difficulty": "unknown",
                    "domain": "real_code_mixed_sentiment",
                    "id": f"bnsentmix_{source_row:05d}",
                    "license_notes": (
                        "Upstream paper states CC BY 4.0; current Hugging Face "
                        "dataset card states MIT. Use locally for research "
                        "evaluation and reconcile before public redistribution."
                    ),
                    "metadata": {
                        "original_numeric_label": str(source["raw_label"]),
                        "sampling_seed": seed,
                        "sentiment_label": label,
                    },
                    "quality_status": "upstream_human_annotated",
                    "real_banglish": build_prompt(str(source["sentence"])),
                    "source_file": repo_path(source_file),
                    "source_row": source_row,
                    "source_url": SOURCE_URL,
                    "task_type": "sentiment_classification",
                }
            )
    return output


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(
    path: Path,
    input_path: Path,
    output_path: Path,
    source_rows: list[dict[str, Any]],
    duplicates: int,
    selected: list[dict[str, Any]],
    per_label: int,
    pilot_per_label: int,
    seed: int,
) -> None:
    source_counts = Counter(str(row["label"]) for row in source_rows)
    selected_counts = Counter(str(row["answer"]) for row in selected)
    pilot = selected[: pilot_per_label * len(LABELS)]
    pilot_counts = Counter(str(row["answer"]) for row in pilot)
    lines = [
        "# BnSentMix External-Validation Slice",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Purpose",
        "",
        "This layer evaluates zero-shot sentiment classification on naturally",
        "occurring Bengali-English code-mixed text. It broadens the thesis beyond",
        "controlled romanized benchmark variants. It is an ecological-validity",
        "layer, not a paired causal estimate of script effects.",
        "",
        "## Upstream Source",
        "",
        f"- Dataset card: {SOURCE_URL}",
        f"- Paper: {PAPER_URL}",
        f"- Local pinned CSV: `{repo_path(input_path)}`",
        f"- Source SHA-256: `{EXPECTED_SOURCE_SHA256}`",
        "- The paper and card describe 20,000 samples. The current pinned CSV",
        f"  contains {len(source_rows) + duplicates:,} rows; exact duplicate text",
        f"  rows removed before sampling: {duplicates:,}.",
        "- License metadata needs reconciliation before public redistribution:",
        "  the paper states CC BY 4.0 while the current Hugging Face card states MIT.",
        "",
        "## Slice Design",
        "",
        f"- Output: `{repo_path(output_path)}`",
        f"- Sampling seed: `{seed}`",
        f"- Balanced external slice: {len(selected)} rows ({per_label} per label).",
        f"- Pilot prefix: {len(pilot)} rows ({pilot_per_label} per label).",
        "- Prompt output is a sentiment word, not an A/B/C/D option, so the",
        "  external layer does not reuse the core MCQ label-position behavior.",
        "",
        "| Label | Unique source rows | Slice rows | Pilot rows |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label in LABELS:
        lines.append(
            f"| {label} | {source_counts[label]} | {selected_counts[label]} | "
            f"{pilot_counts[label]} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Contract",
            "",
            "- Report accuracy, macro-F1, per-label recall, and invalid output rate.",
            "- Compare models within this independently sampled external layer.",
            "- Do not compare its absolute accuracy directly with the paired",
            "  knowledge benchmark as if the tasks had equal difficulty.",
            "- Treat data contamination as an open threat because the public",
            "  dataset predates the evaluated instruction checkpoints.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--per-label", type=int, default=50)
    parser.add_argument("--pilot-per-label", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260603)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.per_label <= 0 or args.pilot_per_label <= 0:
        raise SystemExit("Sampling counts must be positive.")
    if args.pilot_per_label > args.per_label:
        raise SystemExit("--pilot-per-label cannot exceed --per-label.")

    source_rows, duplicates = load_source(args.input)
    selected = sample_rows(source_rows, args.per_label, args.seed, args.input)
    write_jsonl(args.output, selected)
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": repo_path(args.input),
        "notes": [
            "Independent balanced real-code-mixed sentiment evaluation layer.",
            "Local research use only until upstream license metadata mismatch is reconciled.",
            "The first pilot_per_label * 4 rows form a balanced pilot prefix.",
        ],
        "output": repo_path(args.output),
        "paper_url": PAPER_URL,
        "pilot_items": args.pilot_per_label * len(LABELS),
        "sampling_seed": args.seed,
        "source_dataset_url": SOURCE_URL,
        "source_rows": len(source_rows) + duplicates,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_unique_rows": len(source_rows),
        "source_exact_duplicate_rows": duplicates,
        "summary": {
            "counts_by_label": dict(
                sorted(Counter(str(row["answer"]) for row in selected).items())
            ),
            "total_items": len(selected),
        },
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(
        args.report_output,
        args.input,
        args.output,
        source_rows,
        duplicates,
        selected,
        args.per_label,
        args.pilot_per_label,
        args.seed,
    )
    print(f"source_rows={len(source_rows) + duplicates}")
    print(f"source_unique_rows={len(source_rows)}")
    print(f"source_exact_duplicate_rows={duplicates}")
    print(f"slice_rows={len(selected)}")
    print(f"pilot_rows={args.pilot_per_label * len(LABELS)}")
    print(f"output={args.output}")
    print(f"manifest={manifest_path}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
