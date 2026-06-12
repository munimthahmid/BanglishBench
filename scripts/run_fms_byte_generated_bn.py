#!/usr/bin/env python3
"""Run the fms-byte MBART Banglish-to-Bengali model with structural protection."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl"
)
DEFAULT_OUTPUT = (
    ROOT / "results/generated_views/fms_byte_protected_dev50_benqa_mcq_generated_bn.jsonl"
)
DEFAULT_MODEL = "fms-byte/banglish_to_bangla"
DEFAULT_REVISION = "c14b1cf0fe575b9b9f9429142fdd2265a9b39920"

ANSWER_LINE_RE = re.compile(r"^Answer with only .*$")
OPTION_PREFIX_RE = re.compile(r"^(\s*[A-D][.)]\s+)(.*)$")
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
ROMAN_ENUM_RE = re.compile(r"(?<![A-Za-z])(?:i|ii|iii)(?![A-Za-z])")
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
MATH_PUNCT_RE = re.compile(r"[{}^_=+\-*/(),]")


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


def scientific_spans(text: str) -> list[tuple[int, int]]:
    return [
        match.span()
        for match in SCIENTIFIC_TOKEN_RE.finditer(text)
        if len(match.group()) >= 2 or "_" in match.group() or "^" in match.group()
    ]


def protected_spans(text: str) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for pattern in [
        LATEX_COMMAND_RE,
        ANNOTATED_TOKEN_RE,
        NUMBER_RE,
        ROMAN_ENUM_RE,
        MATH_TOKEN_RE,
        FORMULAISH_TOKEN_RE,
        ISOLATED_UPPER_MATH_TOKEN_RE,
        MATH_PUNCT_RE,
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


def split_body(text: str) -> tuple[list[tuple[str, str]], int]:
    spans = protected_spans(text)
    if not spans:
        return [("generate", text)], 0

    pieces: list[tuple[str, str]] = []
    cursor = 0
    for start, end in spans:
        if cursor < start:
            pieces.append(("generate", text[cursor:start]))
        pieces.append(("preserve", text[start:end]))
        cursor = end
    if cursor < len(text):
        pieces.append(("generate", text[cursor:]))
    return pieces, len(spans)


def plan_text(text: str) -> tuple[list[tuple[str, str]], int]:
    pieces: list[tuple[str, str]] = []
    protected_count = 0
    for index, line in enumerate(text.splitlines()):
        if index:
            pieces.append(("preserve", "\n"))
        if ANSWER_LINE_RE.fullmatch(line):
            pieces.append(("preserve", line))
            protected_count += 1
            continue
        option_match = OPTION_PREFIX_RE.match(line)
        body = line
        if option_match:
            pieces.append(("preserve", option_match.group(1)))
            body = option_match.group(2)
            protected_count += 1
        body_pieces, body_count = split_body(body)
        pieces.extend(body_pieces)
        protected_count += body_count
    return pieces, protected_count


def generation_core(text: str) -> tuple[str, str, str]:
    leading = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()) :]
    return leading, text.strip(), trailing


def generate_segments(
    segments: list[str],
    model_name: str,
    revision: str,
    batch_size: int,
    max_new_tokens: int,
) -> tuple[dict[str, str], str]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else None
    tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        revision=revision,
        torch_dtype=dtype,
    ).to(device)
    model.eval()

    unique = sorted({segment for segment in segments if segment})
    generated: dict[str, str] = {}
    for start in range(0, len(unique), batch_size):
        batch = unique[start : start + batch_size]
        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
        )
        inputs = {key: value.to(device) for key, value in inputs.items()}
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                num_beams=5,
                early_stopping=True,
            )
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        generated.update(zip(batch, (text.strip() for text in decoded), strict=True))
        print(f"generated_segments={min(start + len(batch), len(unique))}/{len(unique)}")
    return generated, device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=192)
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prompts = [
        row
        for row in load_jsonl(args.input)
        if row.get("target_view") == "generated_bn"
    ]
    if args.limit is not None:
        prompts = prompts[: args.limit]

    planned: list[tuple[dict[str, Any], list[tuple[str, str]], int]] = []
    generation_segments: list[str] = []
    for prompt in prompts:
        pieces, protected_count = plan_text(str(prompt.get("source_text", "")))
        planned.append((prompt, pieces, protected_count))
        for kind, text in pieces:
            if kind != "generate":
                continue
            _, core, _ = generation_core(text)
            if core:
                generation_segments.append(core)

    generated, device = generate_segments(
        generation_segments,
        args.model,
        args.revision,
        args.batch_size,
        args.max_new_tokens,
    )

    rows: list[dict[str, Any]] = []
    created_at = datetime.now(timezone.utc).isoformat()
    for prompt, pieces, protected_count in planned:
        output_parts: list[str] = []
        for kind, text in pieces:
            if kind == "preserve":
                output_parts.append(text)
                continue
            leading, core, trailing = generation_core(text)
            output_parts.append(f"{leading}{generated.get(core, core)}{trailing}")
        rows.append(
            {
                "id": prompt["id"],
                "target_view": prompt["target_view"],
                "generator": args.model,
                "model_revision": args.revision,
                "protection": "line_segment_option_answer_latex_scientific_token_number_math",
                "protected_spans": protected_count,
                "device": device,
                "created_at_utc": created_at,
                "source_text": prompt.get("source_text", ""),
                "generated_text": "".join(output_parts),
            }
        )

    write_jsonl(args.output, rows)
    print(f"rows={len(rows)}")
    print(f"device={device}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
