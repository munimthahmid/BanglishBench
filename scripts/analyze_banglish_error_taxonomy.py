#!/usr/bin/env python3
"""Rule-assisted error taxonomy for recoverable reviewed-Banglish misses.

Codes the recoverable BEnQA Banglish misses (items the model gets wrong under
reviewed Banglish but right under Bangla or English, same item) into four
categories defined for the failure analysis:

  option_format_failure   - the Banglish answer is not a parseable A-D letter
  number_unit_misread     - the item turns on digits, formulae, or units that
                            the romanization renders ambiguously
  technical_term_corruption - the decisive options are romanized scientific or
                            named-entity terms (the named-entity channel)
  romanized_word_ambiguity - residual: ordinary-word romanization ambiguity

The coder is deterministic and documented so the assignment is reproducible;
representative examples per category are emitted for the write-up.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLICE = ROOT / "data/slices/validation_200_v5.jsonl"
FAILURES = ROOT / "results/analysis/validation200_v5_cross_script_failure_patterns_items.csv"
DEFAULT_OUTPUT = ROOT / "results/analysis/banglish_error_taxonomy.csv"
DEFAULT_REPORT = ROOT / "reports/banglish_error_taxonomy.md"

VALID = {"A", "B", "C", "D"}

# Romanized scientific / technical term signatures (chemistry, biology, units).
TECH_SUFFIXES = (
    "esid", "asitik", "oksaid", "oksid", "kosh", "koshe", "kondriya", "plast",
    "jom", "soma", "iyam", "iyum", "oti", "enjaim", "hormon", "protin", "glukoj",
    "glisar", "laktik", "lyakotik", "niukloya", "raibo", "laiso", "kloro",
    "metajailem", "bhaskular", "kromosom", "jaigot", "siniukloya",
)


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def has_formula_or_number(text: str) -> bool:
    if re.search(r"[A-Za-z]_\{?\d", text):  # CO_{2}, H_2
        return True
    if re.search(r"\d", text):
        return True
    units = (" cm", " mm", " kg", " gram", " mol", " joule", " watt", " ohm", " volt", " meter", "%")
    return any(u in text.lower() for u in units)


def option_block(banglish: str) -> list[str]:
    opts = re.findall(r"(?m)^([A-D])\.\s*(.+)$", banglish)
    return [body.strip() for _label, body in opts]


def looks_technical(options: list[str]) -> bool:
    hits = 0
    for opt in options:
        low = opt.lower()
        if any(sig in low for sig in TECH_SUFFIXES):
            hits += 1
        else:
            # single long romanized token with no spaces is usually a term
            tokens = low.split()
            if len(tokens) == 1 and len(tokens[0]) >= 7:
                hits += 1
    return hits >= 2


def classify(row: dict[str, str], banglish: str) -> str:
    parsed = row["banglish_clean_parsed"].strip()
    if parsed not in VALID:
        return "option_format_failure"
    options = option_block(banglish)
    # question stem is everything before the first option
    stem = banglish.split("\nA.")[0]
    if has_formula_or_number(stem) or any(has_formula_or_number(o) for o in options):
        # only if the numeric content is plausibly decisive (short numeric options
        # or formula in stem), otherwise fall through
        if re.search(r"[A-Za-z]_\{?\d", banglish) or any(re.fullmatch(r"[\d.\s%a-z/]+", o.lower()) for o in options):
            return "number_unit_misread"
    if looks_technical(options):
        return "technical_term_corruption"
    return "romanized_word_ambiguity"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    slice_rows = {}
    with SLICE.open(encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            slice_rows[rec["id"]] = rec

    with FAILURES.open(encoding="utf-8", newline="") as handle:
        failures = list(csv.DictReader(handle))

    coded = []
    for row in failures:
        if row["dataset"] != "benqa":
            continue
        if truthy(row["banglish_clean_correct"]):
            continue
        if not (truthy(row["bangla_correct"]) or truthy(row["english_correct"])):
            continue
        banglish = slice_rows[row["id"]]["banglish_clean"]
        category = classify(row, banglish)
        recovered = []
        if truthy(row["bangla_correct"]):
            recovered.append("Bangla")
        if truthy(row["english_correct"]):
            recovered.append("English")
        coded.append(
            {
                "model": row["model"].split("/")[-1],
                "id": row["id"],
                "subject": row["subject"],
                "gold": row["gold"],
                "banglish_parsed": row["banglish_clean_parsed"].strip(),
                "bangla_parsed": row["bangla_parsed"].strip(),
                "english_parsed": row["english_parsed"].strip(),
                "recovered_by": "+".join(recovered),
                "category": category,
                "banglish_excerpt": " | ".join(
                    banglish.replace("\nAnswer with only A, B, C, or D.", "").splitlines()
                )[:240],
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(coded[0]))
        writer.writeheader()
        writer.writerows(coded)

    counts = Counter(c["category"] for c in coded)
    order = [
        "technical_term_corruption",
        "romanized_word_ambiguity",
        "number_unit_misread",
        "option_format_failure",
    ]
    titles = {
        "technical_term_corruption": "Named-entity / technical-term corruption",
        "romanized_word_ambiguity": "Romanized-word ambiguity",
        "number_unit_misread": "Number / unit / formula misread",
        "option_format_failure": "Option-format failure",
    }
    total = len(coded)
    lines = [
        "# Reviewed-Banglish Recoverable-Miss Error Taxonomy",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        f"Rule-assisted coding of all {total} recoverable BEnQA reviewed-Banglish",
        "misses across the three Qwen models (items wrong under Banglish but",
        "correct under Bangla or English on the same item). Categories are assigned",
        "by the deterministic rules in `scripts/analyze_banglish_error_taxonomy.py`.",
        "",
        f"- Coding sheet: `{args.output.relative_to(ROOT)}`",
        "",
        "| Category | Count | Share |",
        "| --- | ---: | ---: |",
    ]
    for key in order:
        lines.append(f"| {titles[key]} | {counts.get(key, 0)} | {100*counts.get(key,0)/total:.1f}% |")
    lines += [f"| **Total** | **{total}** | **100%** |", ""]

    for key in order:
        examples = [c for c in coded if c["category"] == key][:2]
        lines += [f"## {titles[key]}", ""]
        for ex in examples:
            lines += [
                f"- **{ex['model']}** `{ex['id']}` (gold {ex['gold']}, "
                f"Banglish parsed {ex['banglish_parsed']}, recovered by {ex['recovered_by']}):",
                f"  > {ex['banglish_excerpt']}",
            ]
        lines.append("")
    args.report_output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"coded={total} {dict(counts)} report={args.report_output}")


if __name__ == "__main__":
    main()
