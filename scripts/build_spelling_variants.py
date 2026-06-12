#!/usr/bin/env python3
"""Generate plausible Banglish spelling variants for a BEnQA subset.

Real romanized Bangla has heavy spelling variation (BanglaTLit). To test whether
the script gap is stable under that variation, we generate K distinct spelling
variants of each item's reviewed Banglish field by applying seeded probabilistic
phonetic substitutions, protecting digits, formulae, option labels, and the
answer-format instruction line so the task and gold answer are preserved.

Output: data/slices/spelling_variants_benqa100_v1.jsonl with fields
  spell0 (= canonical reviewed Banglish), spell1..spellK, plus bangla/english
  for reference. Each item keeps its id and gold answer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/slices/validation_200_v5.jsonl"
OUTPUT = ROOT / "data/slices/spelling_variants_benqa100_v1.jsonl"

ANSWER_LINE = "Answer with only A, B, C, or D."

# (pattern, replacement, probability) — applied left to right on a protected word.
SUBSTITUTIONS = [
    (r"sh", "s", 0.5),
    (r"bh", "v", 0.4),
    (r"ph", "f", 0.4),
    (r"kh", "k", 0.3),
    (r"chh", "ch", 0.5),
    (r"oo", "u", 0.4),
    (r"ee", "i", 0.4),
    (r"oi", "oy", 0.4),
    (r"w", "o", 0.4),
    (r"y", "i", 0.25),
    (r"z", "j", 0.4),
    (r"v", "bh", 0.2),
    (r"o\b", "", 0.18),  # drop trailing inherent vowel sometimes
    (r"ii", "i", 0.5),
]


def protected(token: str) -> bool:
    """Tokens we never alter: formulae, numbers, option labels, backslash macros."""
    if re.search(r"[0-9\\_{}^]", token):
        return True
    if re.fullmatch(r"[A-D][.)]", token):
        return True
    return False


def vary_word(word: str, rng: random.Random) -> str:
    if protected(word):
        return word
    out = word
    for pat, repl, prob in SUBSTITUTIONS:
        if rng.random() < prob:
            out = re.sub(pat, repl, out)
    return out


def vary_line(line: str, rng: random.Random) -> str:
    if line.strip() == ANSWER_LINE:
        return line
    # preserve option label prefix "A. " etc.
    m = re.match(r"^([A-D][.)]\s+)(.*)$", line)
    prefix, body = (m.group(1), m.group(2)) if m else ("", line)
    words = body.split(" ")
    return prefix + " ".join(vary_word(w, rng) for w in words)


def make_variant(text: str, seed: int) -> str:
    rng = random.Random(seed)
    return "\n".join(vary_line(ln, rng) for ln in text.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--variants", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = []
    with SOURCE.open(encoding="utf-8") as handle:
        for line in handle:
            r = json.loads(line)
            if r.get("dataset") == "benqa":
                rows.append(r)

    rng = random.Random(args.seed)
    rng.shuffle(rows)
    selected = rows[: args.count]
    selected.sort(key=lambda r: r["id"])

    out_rows = []
    for r in selected:
        canonical = r["banglish_clean"]
        item = {
            "id": r["id"],
            "dataset": "benqa",
            "task_type": r.get("task_type", "mcq"),
            "answer_type": r["answer_type"],
            "answer": r["answer"],
            "bangla": r["bangla"],
            "english": r["english"],
            "spell0": canonical,
        }
        seen = {canonical}
        made = 0
        attempt = 0
        while made < args.variants and attempt < 50:
            seed = int(hashlib.sha256(f"{r['id']}:{made}:{attempt}".encode()).hexdigest(), 16) % (2**31)
            v = make_variant(canonical, seed)
            attempt += 1
            if v in seen:
                continue
            seen.add(v)
            made += 1
            item[f"spell{made}"] = v
        # pad if fewer distinct found (rare)
        while made < args.variants:
            made += 1
            item[f"spell{made}"] = canonical
        out_rows.append(item)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as handle:
        for item in out_rows:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")

    spell_fields = ["spell0"] + [f"spell{i}" for i in range(1, args.variants + 1)]
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE.relative_to(ROOT)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "count": len(out_rows),
        "variants_per_item": args.variants,
        "spell_fields": spell_fields,
        "seed": args.seed,
        "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "notes": [
            "spell0 is the canonical reviewed Banglish; spell1..K are seeded phonetic respellings.",
            "Digits, formulae, option labels, and the answer-format line are preserved.",
        ],
    }
    OUTPUT.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # show one example
    ex = out_rows[0]
    print(f"items={len(out_rows)} variants/item={args.variants}")
    print("example id:", ex["id"])
    for f in spell_fields:
        print(f"  {f}:", ex[f].splitlines()[0][:90])


if __name__ == "__main__":
    main()
