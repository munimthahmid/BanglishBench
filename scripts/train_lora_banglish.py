#!/usr/bin/env python3
"""LoRA training kernel for the Banglish mitigation experiment (Kaggle P100).

Self-contained: avoids trl API drift by using transformers.Trainer with manual
completion-only masking. Each training row is a chat example
{"messages": [user, assistant]}; the assistant content (a single A-D letter) is
the only supervised target. Prompt tokens are masked to -100.

P100 has no bf16, so fp16 is used throughout (next_steps.md Step 2).
Run as a Kaggle script kernel; reads ARM from the ARM env or a hardcoded default.
"""

from __future__ import annotations

import json
import os
import shutil
import zipfile
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

INPUT_BASE = Path("/kaggle/input")
WORKING = Path("/kaggle/working")

BASE_MODEL = os.environ.get("LORA_BASE_MODEL", "Qwen/Qwen2.5-3B-Instruct")
ARM = os.environ.get("LORA_ARM", "armA")  # armA | armB
TRAIN_FILE = {
    "armA": "lora_train_banglish.jsonl",
    "armB": "lora_train_mixed.jsonl",
}[ARM]
OUTPUT_NAME = {"armA": "lora_armA_banglish", "armB": "lora_armB_mixed"}[ARM]
MAX_LEN = 1024
SEED = 42


def find_input_file(name: str) -> Path:
    matches = [p for p in INPUT_BASE.rglob(name) if p.is_file()]
    if not matches:
        raise FileNotFoundError(f"{name} not found under {INPUT_BASE}")
    return matches[0]


def load_chat_rows(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> None:
    print(f"ARM={ARM} BASE={BASE_MODEL} TRAIN_FILE={TRAIN_FILE}")
    gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
    print("GPU:", gpu)

    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    train_path = find_input_file(TRAIN_FILE)
    raw = load_chat_rows(train_path)
    print(f"loaded {len(raw)} training rows from {train_path}")

    def encode(example: dict) -> dict:
        messages = example["messages"]
        user_msg, asst_msg = messages[0], messages[1]
        prompt_ids = tok.apply_chat_template(
            [user_msg], add_generation_prompt=True, tokenize=True
        )
        full_ids = tok.apply_chat_template(messages, add_generation_prompt=False, tokenize=True)
        if len(full_ids) > MAX_LEN:
            full_ids = full_ids[:MAX_LEN]
        labels = list(full_ids)
        mask_len = min(len(prompt_ids), len(labels))
        for i in range(mask_len):
            labels[i] = -100
        return {"input_ids": full_ids, "labels": labels, "attention_mask": [1] * len(full_ids)}

    ds = Dataset.from_list(raw).map(encode, remove_columns=["messages"])

    def collate(batch: list[dict]) -> dict:
        maxlen = max(len(b["input_ids"]) for b in batch)
        pad_id = tok.pad_token_id
        input_ids, labels, attn = [], [], []
        for b in batch:
            n = maxlen - len(b["input_ids"])
            input_ids.append(b["input_ids"] + [pad_id] * n)
            labels.append(b["labels"] + [-100] * n)
            attn.append(b["attention_mask"] + [0] * n)
        return {
            "input_ids": torch.tensor(input_ids),
            "labels": torch.tensor(labels),
            "attention_mask": torch.tensor(attn),
        }

    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float16)
    model.config.use_cache = False
    model.enable_input_require_grads()

    peft_cfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, peft_cfg)
    model.print_trainable_parameters()

    out_dir = WORKING / OUTPUT_NAME
    targs = TrainingArguments(
        output_dir=str(out_dir),
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=2,
        learning_rate=1e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=20,
        save_steps=100,
        save_total_limit=1,
        fp16=True,
        bf16=False,
        seed=SEED,
        report_to=[],
        gradient_checkpointing=True,
    )
    trainer = Trainer(model=model, args=targs, train_dataset=ds, data_collator=collate)
    trainer.train()

    adapter_dir = out_dir / "adapter"
    model.save_pretrained(str(adapter_dir))
    tok.save_pretrained(str(adapter_dir))

    manifest = {
        "arm": ARM,
        "base_model": BASE_MODEL,
        "train_file": TRAIN_FILE,
        "train_rows": len(raw),
        "gpu": gpu,
        "lora": {"r": 16, "alpha": 32, "dropout": 0.05},
        "hparams": {
            "epochs": 2, "lr": 1e-4, "schedule": "cosine", "warmup_ratio": 0.03,
            "per_device_batch": 4, "grad_accum": 4, "effective_batch": 16,
            "max_len": MAX_LEN, "precision": "fp16", "seed": SEED,
        },
    }
    (adapter_dir / "train_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    zip_path = WORKING / f"{OUTPUT_NAME}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in adapter_dir.rglob("*"):
            if p.is_file():
                zf.write(p, p.relative_to(WORKING))
    print("saved adapter zip:", zip_path)
    # keep only the zip to stay under output limits
    if (out_dir / "adapter").exists():
        for sub in out_dir.iterdir():
            if sub.name != "adapter":
                if sub.is_dir():
                    shutil.rmtree(sub, ignore_errors=True)


if __name__ == "__main__":
    main()
