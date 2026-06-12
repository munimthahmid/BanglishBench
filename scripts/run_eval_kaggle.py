#!/usr/bin/env python3
"""Resumable HuggingFace generation runner for Kaggle GPU notebooks."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("TRANSFORMERS_NO_TORCHVISION", "1")


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/pilot/items.jsonl"
DEFAULT_OUTPUT = ROOT / "results/runs/pilot_outputs.jsonl"
DEFAULT_EXTERNAL_NORMALIZER = "sk-community/romanized-bengali-transliterator-60M"
SENTIMENT_LABELS = ("positive", "negative", "neutral", "mixed")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_done(path: Path) -> set[tuple[str, str, str, str]]:
    done: set[tuple[str, str, str, str]] = set()
    if not path.exists():
        return done
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            done.add((row["model"], row["id"], row["variant"], row.get("prompt_mode", "baseline")))
    return done


def make_prompt_for_text(text: str, answer_type: str, prompt_mode: str) -> str:
    header = (
        "Answer the following evaluation item. Follow the requested answer format exactly.\n\n"
    )
    if prompt_mode == "neutral_terse":
        # Prompt-sensitivity template B: terser neutral wording, no Banglish hint.
        header = "Solve this question and give the answer in the exact format requested.\n\n"
    elif prompt_mode == "neutral_role":
        # Prompt-sensitivity template C: role-framed neutral wording, no Banglish hint.
        header = (
            "You are taking an exam. Read the question below and respond with only "
            "the answer in the requested format.\n\n"
        )
    elif prompt_mode == "banglish_aware":
        header = (
            "Answer the following evaluation item. If the text is Latin-script Bangla "
            "or Banglish, read it as Bengali written in Latin letters and solve the "
            "original question. Follow the requested answer format exactly.\n\n"
        )
    elif prompt_mode == "banglish_fewshot":
        if answer_type == "choice":
            header = (
                "Answer the following evaluation item. Latin-script Bangla/Banglish "
                "means Bengali written in Latin letters.\n\n"
                "Example:\n"
                "panir rashayonik sonket konti?\n"
                "A. CO2\n"
                "B. H2O\n"
                "C. O2\n"
                "D. NaCl\n"
                "Answer with only A, B, C, or D.\n"
                "Final answer: B\n\n"
                "Now answer this item. Follow the requested answer format exactly.\n\n"
            )
        else:
            header = (
                "Answer the following evaluation item. Latin-script Bangla/Banglish "
                "means Bengali written in Latin letters.\n\n"
                "Example:\n"
                "dui er sathe tin jog korle koto hoy?\n"
                "Return only the final answer.\n"
                "Final answer: 5\n\n"
                "Now answer this item. Follow the requested answer format exactly.\n\n"
            )
    elif prompt_mode == "banglish_self_normalize":
        header = (
            "Answer the following evaluation item. Follow the requested answer format exactly.\n\n"
        )
    elif prompt_mode == "banglish_self_translate_en":
        header = (
            "Answer the following evaluation item. Follow the requested answer format exactly.\n\n"
        )
    return header + text


def make_prompt(item: dict[str, Any], variant: str, prompt_mode: str) -> str:
    text = item.get(variant) or ""
    if not text:
        raise ValueError(f"Missing variant {variant} for item {item['id']}")
    return make_prompt_for_text(text, item["answer_type"], prompt_mode)


def make_rewrite_prompt(text: str) -> str:
    return (
        "Rewrite the following Latin-script Bangla/Banglish evaluation item in "
        "standard Bengali script. Preserve numbers, symbols, line breaks, and "
        "answer options exactly. Do not solve the item. Output only the rewritten "
        "item.\n\n"
        f"{text}"
    )


def make_translate_prompt(text: str) -> str:
    return (
        "Translate the following Latin-script Bangla/Banglish evaluation item "
        "into clear English. Preserve numbers, symbols, line breaks, and answer "
        "options exactly. Do not solve the item. Output only the translated item.\n\n"
        f"{text}"
    )


def load_external_normalizer(model_name: str = DEFAULT_EXTERNAL_NORMALIZER) -> tuple[Any, Any, str]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    default_device = "cuda" if torch.cuda.is_available() else "cpu"
    device = os.environ.get("EXTERNAL_NORMALIZER_DEVICE", default_device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    if device == "cuda" and torch.cuda.is_available():
        model = model.to("cuda")
    else:
        device = "cpu"
    model.eval()
    return tokenizer, model, device


def external_normalize_line(
    text: str,
    tokenizer: Any,
    model: Any,
    device: str,
    max_length: int = 192,
) -> str:
    import torch

    stripped = text.strip()
    if not stripped:
        return text

    leading = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()) :]
    core = stripped
    option_prefix = ""
    option_match = re.match(r"^([A-D])(\.\s+|\)\s+)(.*)$", core)
    if option_match:
        option_prefix = option_match.group(1) + option_match.group(2)
        core = option_match.group(3)

    inputs = tokenizer(
        core,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            num_beams=4,
            early_stopping=True,
        )
    normalized = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return f"{leading}{option_prefix}{normalized}{trailing}"


def external_normalize_text(text: str, tokenizer: Any, model: Any, device: str) -> str:
    import torch

    lines = text.splitlines()
    prepared: list[dict[str, str]] = []
    cores: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            prepared.append(
                {"kind": "blank", "leading": line, "prefix": "", "trailing": ""}
            )
            continue
        leading = line[: len(line) - len(line.lstrip())]
        trailing = line[len(line.rstrip()) :]
        core = stripped
        option_prefix = ""
        option_match = re.match(r"^([A-D])(\.\s+|\)\s+)(.*)$", core)
        if option_match:
            option_prefix = option_match.group(1) + option_match.group(2)
            core = option_match.group(3)
        prepared.append(
            {
                "kind": "text",
                "leading": leading,
                "prefix": option_prefix,
                "trailing": trailing,
            }
        )
        cores.append(core)

    if not cores:
        return text

    inputs = tokenizer(
        cores,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=192,
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=192,
            num_beams=4,
            early_stopping=True,
        )
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    decoded_iter = iter(text.strip() for text in decoded)
    normalized_lines: list[str] = []
    for meta in prepared:
        if meta["kind"] == "blank":
            normalized_lines.append(meta["leading"])
            continue
        normalized_lines.append(
            f"{meta['leading']}{meta['prefix']}{next(decoded_iter)}{meta['trailing']}"
        )
    return "\n".join(normalized_lines)


def parse_answer(text: str, answer_type: str) -> str:
    stripped = text.strip()
    if answer_type == "choice":
        upper = stripped.upper()
        lines = [line.strip().upper() for line in stripped.splitlines() if line.strip()]

        direct = re.fullmatch(r"(?:FINAL\s+ANSWER\s*[:：-]?\s*)?([ABCD])[\).。।]?", upper)
        if direct:
            return direct.group(1)

        patterns = [
            r"(?:FINAL\s+ANSWER|ANSWER)\s*(?:IS|:|：|-)?\s*([ABCD])\b",
            r"(?:CORRECT\s+ANSWER)\s*(?:IS|:|：|-)?\s*([ABCD])\b",
            r"(?:OPTION|CHOICE)\s*([ABCD])\b",
        ]
        for pattern in patterns:
            matches = list(re.finditer(pattern, upper))
            if matches:
                return matches[-1].group(1)

        for line in reversed(lines):
            line_match = re.match(r"^([ABCD])(?:[\).:：\s]|$)", line)
            if line_match and not re.search(r"\b[A-D]\s*,\s*[A-D]\b", line):
                return line_match.group(1)
        return ""

    if answer_type == "sentiment":
        lower = stripped.lower()
        direct = re.fullmatch(
            r"\s*(?:(?:final\s+)?(?:answer|label|sentiment)\s*(?:is|:|：|-)?\s*)?"
            r"[*_`]*(positive|negative|neutral|mixed)[*_`]*[.!]?\s*",
            lower,
        )
        if direct:
            return direct.group(1)

        declared_patterns = [
            r"(?:final\s+)?(?:answer|label|sentiment)\s*(?:is|:|：|-)?\s*"
            r"[*_`]*(positive|negative|neutral|mixed)\b",
            r"classification\s*(?:is|:|：|-)?\s*"
            r"[*_`]*(positive|negative|neutral|mixed)\b",
        ]
        for pattern in declared_patterns:
            matches = list(re.finditer(pattern, lower))
            if matches:
                return matches[-1].group(1)

        labels = set(re.findall(r"\b(?:positive|negative|neutral|mixed)\b", lower))
        if len(labels) == 1:
            return labels.pop()
        return ""

    answer_match = re.search(
        r"(?:final\s+answer|answer)\s*(?:is|:|：|-)?\s*(.+)",
        stripped,
        flags=re.IGNORECASE,
    )
    if answer_match:
        return answer_match.group(1).strip().splitlines()[0].strip()

    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    for line in reversed(lines):
        compact = line.strip(" -*•`")
        if len(compact) > 100:
            continue
        if re.search(r"[0-9\u09e6-\u09ef]", compact):
            return compact

    first_line = stripped.splitlines()[0] if stripped else ""
    return first_line.strip()


def normalize_answer(text: str) -> str:
    digit_map = str.maketrans(
        "\u09e6\u09e7\u09e8\u09e9\u09ea\u09eb\u09ec\u09ed\u09ee\u09ef",
        "0123456789",
    )
    superscript_map = {
        ord("\u2070"): "^0",
        ord("\u00b9"): "^1",
        ord("\u00b2"): "^2",
        ord("\u00b3"): "^3",
        ord("\u2074"): "^4",
        ord("\u2075"): "^5",
        ord("\u2076"): "^6",
        ord("\u2077"): "^7",
        ord("\u2078"): "^8",
        ord("\u2079"): "^9",
    }
    text = text.translate(digit_map)
    text = text.translate(superscript_map)
    text = text.replace("−", "-").replace("–", "-").replace("—", "-")
    text = text.strip().lower()
    unit_replacements = [
        (r"\b(days?)\b", " day "),
        (r"দিন", " day "),
        (r"\b(takas?|tk)\b", " taka "),
        (r"টাকা", " taka "),
        (r"৳", " taka "),
        (r"\bm\s*\^?\s*2\b", " m^2 "),
        (r"\bm²\b", " m^2 "),
        (r"\b(sq\.?\s*m|square\s+meters?)\b", " m^2 "),
        (r"বর্গ\s*মিটার", " m^2 "),
        (r"বর্গমিটার", " m^2 "),
    ]
    for pattern, replacement in unit_replacements:
        text = re.sub(pattern, replacement, text)
    return re.sub(r"\s+", " ", text.strip())


def compact_answer(text: str) -> str:
    text = normalize_answer(text)
    text = re.sub(r"\s+", "", text)
    return re.sub(r"[।,.;:!?\"'`]+", "", text)


def is_correct(parsed: str, gold: str, answer_type: str) -> bool:
    if answer_type == "choice":
        return parsed.upper() == gold.upper()
    if answer_type == "sentiment":
        return parsed.strip().lower() == gold.strip().lower()
    parsed_norm = normalize_answer(parsed)
    gold_norm = normalize_answer(gold)
    if not parsed_norm or not gold_norm:
        return False
    if parsed_norm == gold_norm:
        return True
    if len(gold_norm) >= 3 and gold_norm in parsed_norm:
        return True

    parsed_compact = compact_answer(parsed)
    gold_compact = compact_answer(gold)
    if parsed_compact == gold_compact:
        return True
    return len(gold_compact) >= 3 and gold_compact in parsed_compact


def load_model(model_name: str, load_in_4bit: bool, load_in_8bit: bool, adapter: str | None = None):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if load_in_4bit and load_in_8bit:
        raise ValueError("Use only one quantization mode: 4-bit or 8-bit.")

    if (load_in_4bit or load_in_8bit) and not hasattr(torch.nn.Module, "set_submodule"):
        def set_submodule(self: Any, target: str, module: Any) -> None:
            if not target:
                raise ValueError("Cannot set the root module.")
            atoms = target.split(".")
            parent = self.get_submodule(".".join(atoms[:-1])) if len(atoms) > 1 else self
            if not hasattr(parent, atoms[-1]):
                raise AttributeError(f"{parent._get_name()} has no child module {atoms[-1]}")
            setattr(parent, atoms[-1], module)

        torch.nn.Module.set_submodule = set_submodule  # type: ignore[attr-defined]

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    kwargs: dict[str, Any] = {
        "device_map": "auto",
        "trust_remote_code": True,
    }
    if load_in_4bit or load_in_8bit:
        from transformers import BitsAndBytesConfig

        if load_in_4bit:
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )
        else:
            kwargs["quantization_config"] = BitsAndBytesConfig(load_in_8bit=True)
    else:
        kwargs["torch_dtype"] = torch.float16

    model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
    if adapter:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter)
        model = model.merge_and_unload()
        print(f"Applied and merged LoRA adapter from {adapter}")
    model.eval()
    return tokenizer, model


def render_for_model(
    tokenizer: Any,
    prompt: str,
    system_message: str | None = None,
    disable_thinking: bool = False,
    prompt_wrapper: str = "auto",
) -> str:
    system_message = system_message or (
        "You are a careful evaluation model. Output only the final answer."
    )
    if prompt_wrapper == "alpaca":
        return (
            "### Instruction:\n"
            f"{system_message}\n\n"
            "### Input:\n"
            f"{prompt}\n\n"
            "### Response:\n"
        )
    if prompt_wrapper == "raw":
        if disable_thinking:
            return prompt.rstrip() + "\n/no_think"
        return prompt

    if getattr(tokenizer, "chat_template", None):
        messages = [
            {
                "role": "system",
                "content": system_message,
            },
            {"role": "user", "content": prompt},
        ]
        kwargs = {
            "tokenize": False,
            "add_generation_prompt": True,
        }
        if disable_thinking:
            kwargs["enable_thinking"] = False
        try:
            return tokenizer.apply_chat_template(messages, **kwargs)
        except TypeError:
            if disable_thinking:
                messages[-1]["content"] = messages[-1]["content"].rstrip() + "\n/no_think"
            return tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
    if disable_thinking:
        return prompt.rstrip() + "\n/no_think"
    return prompt


def generate(
    tokenizer: Any,
    model: Any,
    prompt: str,
    max_new_tokens: int,
    temperature: float,
    system_message: str | None = None,
    disable_thinking: bool = False,
    prompt_wrapper: str = "auto",
) -> str:
    import torch

    rendered = render_for_model(
        tokenizer,
        prompt,
        system_message=system_message,
        disable_thinking=disable_thinking,
        prompt_wrapper=prompt_wrapper,
    )
    inputs = tokenizer(rendered, return_tensors="pt")
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    with torch.no_grad():
        generate_kwargs = {
            "max_new_tokens": max_new_tokens,
            "do_sample": temperature > 0,
            "pad_token_id": tokenizer.eos_token_id,
        }
        if temperature > 0:
            generate_kwargs["temperature"] = temperature
        output_ids = model.generate(
            **inputs,
            **generate_kwargs,
        )
    generated_ids = output_ids[0][inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(generated_ids, skip_special_tokens=True).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--variants", nargs="+", default=["bangla", "banglish_clean", "english"]
    )
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--prompt-mode",
        choices=[
            "baseline",
            "neutral_terse",
            "neutral_role",
            "banglish_aware",
            "banglish_fewshot",
            "banglish_self_normalize",
            "banglish_self_translate_en",
            "banglish_external_normalize",
        ],
        default="baseline",
    )
    parser.add_argument("--load-in-4bit", action="store_true")
    parser.add_argument("--load-in-8bit", action="store_true")
    parser.add_argument(
        "--disable-thinking",
        action="store_true",
        help="Disable Qwen3-style thinking mode when the tokenizer chat template supports it.",
    )
    parser.add_argument(
        "--prompt-wrapper",
        choices=["auto", "raw", "alpaca"],
        default="auto",
        help="Prompt rendering wrapper. Use alpaca for instruction models without chat templates.",
    )
    parser.add_argument("--adapter", default=None, help="Path to a LoRA adapter to merge onto the base model.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.load_in_4bit and args.load_in_8bit:
        raise SystemExit("Use only one quantization flag: --load-in-4bit or --load-in-8bit.")
    items = load_jsonl(args.input)
    if args.limit:
        items = items[: args.limit]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    done = load_done(args.output)

    tokenizer = model = None
    external_normalizer_tokenizer = external_normalizer_model = None
    external_normalizer_device = "cpu"
    if not args.dry_run:
        tokenizer, model = load_model(args.model, args.load_in_4bit, args.load_in_8bit, args.adapter)
        if args.prompt_mode == "banglish_external_normalize":
            (
                external_normalizer_tokenizer,
                external_normalizer_model,
                external_normalizer_device,
            ) = load_external_normalizer()

    with args.output.open("a", encoding="utf-8") as f:
        for item in items:
            for variant in args.variants:
                if not item.get(variant):
                    continue
                key = (args.model, item["id"], variant, args.prompt_mode)
                if key in done:
                    continue

                rewrite_output = ""
                prompt = make_prompt(item, variant, args.prompt_mode)
                if args.dry_run:
                    print(f"--- {item['id']} {variant} ---")
                    print(prompt[:1200])
                    print()
                    continue

                started = time.time()
                if args.prompt_mode in {
                    "banglish_self_normalize",
                    "banglish_self_translate_en",
                } and variant.startswith("banglish"):
                    source_text = item.get(variant) or ""
                    if args.prompt_mode == "banglish_self_translate_en":
                        intermediate_prompt = make_translate_prompt(source_text)
                        system_message = (
                            "You faithfully translate Banglish into English. "
                            "Output only the translated item."
                        )
                    else:
                        intermediate_prompt = make_rewrite_prompt(source_text)
                        system_message = (
                            "You faithfully rewrite Banglish into Bengali script. "
                            "Output only the rewritten item."
                        )
                    rewrite_output = generate(
                        tokenizer,
                        model,
                        intermediate_prompt,
                        max_new_tokens=max(args.max_new_tokens, 256),
                        temperature=args.temperature,
                        system_message=system_message,
                        disable_thinking=args.disable_thinking,
                        prompt_wrapper=args.prompt_wrapper,
                    )
                    prompt = make_prompt_for_text(
                        rewrite_output, item["answer_type"], "baseline"
                    )
                elif (
                    args.prompt_mode == "banglish_external_normalize"
                    and variant.startswith("banglish")
                ):
                    source_text = item.get(variant) or ""
                    if (
                        external_normalizer_tokenizer is None
                        or external_normalizer_model is None
                    ):
                        raise RuntimeError("External normalizer was not loaded")
                    rewrite_output = external_normalize_text(
                        source_text,
                        external_normalizer_tokenizer,
                        external_normalizer_model,
                        external_normalizer_device,
                    )
                    prompt = make_prompt_for_text(
                        rewrite_output, item["answer_type"], "baseline"
                    )

                raw = generate(
                    tokenizer,
                    model,
                    prompt,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                    disable_thinking=args.disable_thinking,
                    prompt_wrapper=args.prompt_wrapper,
                )
                parsed = parse_answer(raw, item["answer_type"])
                row = {
                    "model": args.model,
                    "id": item["id"],
                    "dataset": item["dataset"],
                    "task_type": item["task_type"],
                    "variant": variant,
                    "prompt_mode": args.prompt_mode,
                    "answer_type": item["answer_type"],
                    "gold": item["answer"],
                    "raw_output": raw,
                    "rewrite_output": rewrite_output,
                    "parsed": parsed,
                    "correct": is_correct(parsed, item["answer"], item["answer_type"]),
                    "seconds": round(time.time() - started, 4),
                }
                f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
                f.flush()
                done.add(key)
                print(
                    f"{row['id']} {variant} correct={row['correct']} parsed={row['parsed']!r}"
                )


if __name__ == "__main__":
    main()
