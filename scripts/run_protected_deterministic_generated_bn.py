#!/usr/bin/env python3
"""Run deterministic Banglish-to-Bengali generators with preservation masks."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "results/generated_views"

ANSWER_LINE_RE = re.compile(r"^Answer with only .*$", flags=re.MULTILINE)
OPTION_PREFIX_RE = re.compile(r"^\s*[A-D][.)]\s+", flags=re.MULTILINE)
LATEX_COMMAND_RE = re.compile(
    r"\\[A-Za-z]+(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})*"
)
SCIENTIFIC_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Z][a-z]?)+(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})*"
    r"(?![A-Za-z0-9_])"
)
ANNOTATED_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])[A-Za-z]+(?:_\{[^{}\n]+\}|\^\{[^{}\n]+\})+"
    r"(?![A-Za-z0-9_])"
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
MATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z])(?:cosx|sinx|ln|dx|ax|x|y|a|c|N|X|BC|RMS|gL|ms)(?![A-Za-z])"
)
FORMULAISH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9\\])"
    r"(?=[A-Za-z0-9\\_{}^+\-*/=().]*[\\_{}^+\-*/=()])"
    r"([A-Za-z0-9\\_{}^+\-*/=().]+)"
    r"(?![A-Za-z0-9])"
)
ISOLATED_UPPER_MATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:N|X)(?![A-Za-z0-9_])"
)


def scientific_spans(text: str) -> list[tuple[int, int]]:
    return [
        match.span()
        for match in SCIENTIFIC_TOKEN_RE.finditer(text)
        if len(match.group()) >= 2 or "_" in match.group() or "^" in match.group()
    ]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def non_overlapping_spans(text: str) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for pattern in [
        ANSWER_LINE_RE,
        OPTION_PREFIX_RE,
        LATEX_COMMAND_RE,
        ANNOTATED_TOKEN_RE,
        NUMBER_RE,
        MATH_TOKEN_RE,
        FORMULAISH_TOKEN_RE,
        ISOLATED_UPPER_MATH_TOKEN_RE,
    ]:
        candidates.extend(match.span() for match in pattern.finditer(text))
    candidates.extend(scientific_spans(text))
    candidates.sort(key=lambda span: (span[0], -(span[1] - span[0])))

    spans: list[tuple[int, int]] = []
    occupied_until = -1
    for start, end in candidates:
        if start < occupied_until:
            continue
        spans.append((start, end))
        occupied_until = end
    return spans


def protected_transliterate(text: str, transliterate: Callable[[str], str]) -> tuple[str, int]:
    spans = non_overlapping_spans(text)
    if not spans:
        return transliterate(text), 0

    masked_parts: list[str] = []
    replacements: dict[str, str] = {}
    cursor = 0
    for idx, (start, end) in enumerate(spans):
        placeholder = chr(0xE000 + idx)
        masked_parts.append(text[cursor:start])
        masked_parts.append(placeholder)
        replacements[placeholder] = text[start:end]
        cursor = end
    masked_parts.append(text[cursor:])

    generated = transliterate("".join(masked_parts))
    for placeholder, original in replacements.items():
        generated = generated.replace(placeholder, original)
    return generated, len(replacements)


def load_generator(name: str) -> Callable[[str], str]:
    if name == "phonetic-bangla":
        try:
            from phoneticbn import transliterate
        except ImportError as exc:
            raise SystemExit(
                "Install phonetic-bangla==1.0.0 or put its wheel on PYTHONPATH."
            ) from exc
        return lambda text: transliterate(text)

    if name == "bnbphoneticparser":
        try:
            from bnbphoneticparser import BanglishToBengali
        except ImportError as exc:
            raise SystemExit(
                "Install bnbphoneticparser==0.1.5 or put its source package on PYTHONPATH."
            ) from exc
        parser = BanglishToBengali()
        return lambda text: parser.parse(text)

    raise SystemExit(f"Unknown generator: {name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--generator",
        choices=["phonetic-bangla", "bnbphoneticparser"],
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    transliterate = load_generator(args.generator)
    output = args.output or (
        DEFAULT_OUTPUT_DIR
        / f"{args.generator.replace('-', '_')}_protected_dev50_benqa_mcq_generated_bn.jsonl"
    )

    rows = []
    for prompt in load_jsonl(args.input):
        if prompt.get("target_view") != "generated_bn":
            continue
        generated, protected_spans = protected_transliterate(
            str(prompt.get("source_text", "")),
            transliterate,
        )
        rows.append(
            {
                "id": prompt["id"],
                "target_view": prompt["target_view"],
                "generator": args.generator,
                "protection": "option_prefix_answer_line_latex_scientific_formulaish_number_v3",
                "protected_spans": protected_spans,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "source_text": prompt.get("source_text", ""),
                "generated_text": generated,
            }
        )
    write_jsonl(output, rows)
    print(f"rows={len(rows)}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
