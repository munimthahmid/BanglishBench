#!/usr/bin/env python3
"""Validate citation-backed local literature artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class LiteratureSource:
    citation_key: str
    name: str
    group: str
    paper_path: str
    text_path: str


EXPECTED_SOURCES = [
    LiteratureSource(
        "shafayat-etal-2024-benqa",
        "BEnQA",
        "Core QA/math benchmark",
        "literature/papers/benqa_2024_findings_acl.pdf",
        "literature/text/benqa_2024_findings_acl.txt",
    ),
    LiteratureSource(
        "banglamath2025",
        "BanglaMATH",
        "Core QA/math benchmark",
        "literature/papers/banglamath_2510.12836.pdf",
        "literature/text/banglamath_2510.12836.txt",
    ),
    LiteratureSource(
        "mgsm2022",
        "MGSM",
        "Core QA/math benchmark",
        "literature/papers/mgsm_multilingual_cot_2210.03057.pdf",
        "literature/text/mgsm_multilingual_cot_2210.03057.txt",
    ),
    LiteratureSource(
        "gsm8k2021",
        "GSM8K",
        "Core QA/math benchmark",
        "literature/papers/gsm8k_2110.14168.pdf",
        "literature/text/gsm8k_2110.14168.txt",
    ),
    LiteratureSource(
        "banglaquad2024",
        "BanglaQuAD",
        "Bengali benchmark landscape",
        "literature/papers/banglaquad_2410.10229.pdf",
        "literature/text/banglaquad_2410.10229.txt",
    ),
    LiteratureSource(
        "bnmmlu2025",
        "BnMMLU",
        "Bengali benchmark landscape",
        "literature/papers/bnmmlu_2505.18951.pdf",
        "literature/text/bnmmlu_2505.18951.txt",
    ),
    LiteratureSource(
        "bluck2025",
        "BLUCK",
        "Bengali benchmark landscape",
        "literature/papers/bluck_2505.21092.pdf",
        "literature/text/bluck_2505.21092.txt",
    ),
    LiteratureSource(
        "nctbqa2026",
        "NCTB-QA",
        "Bengali benchmark landscape",
        "literature/papers/nctb_qa_2603.05462.pdf",
        "literature/text/nctb_qa_2603.05462.txt",
    ),
    LiteratureSource(
        "bnli2025",
        "BNLI",
        "Bengali benchmark landscape",
        "literature/papers/bnli_2511.08813.pdf",
        "literature/text/bnli_2511.08813.txt",
    ),
    LiteratureSource(
        "banglasocialbench2026",
        "BanglaSocialBench",
        "Bengali benchmark landscape",
        "literature/papers/bangla_social_bench_2603.15949.pdf",
        "literature/text/bangla_social_bench_2603.15949.txt",
    ),
    LiteratureSource(
        "banglaverse2026",
        "BanglaVerse",
        "Bengali benchmark landscape",
        "literature/papers/banglaverse_2603.21165.pdf",
        "literature/text/banglaverse_2603.21165.txt",
    ),
    LiteratureSource(
        "bengaliloop2026",
        "Bengali-Loop",
        "Bengali benchmark landscape",
        "literature/papers/bengali_loop_2602.14291.pdf",
        "literature/text/bengali_loop_2602.14291.txt",
    ),
    LiteratureSource(
        "banglaguard2026",
        "BanglaGuard",
        "Bengali benchmark landscape",
        "literature/papers/banglaguard_openreview_KTsGJzaEPg.pdf",
        "literature/text/banglaguard_openreview_KTsGJzaEPg.txt",
    ),
    LiteratureSource(
        "banglamedqa2025",
        "BanglaMedQA",
        "Bengali benchmark landscape",
        "literature/papers/banglamedqa_2511.04560.pdf",
        "literature/text/banglamedqa_2511.04560.txt",
    ),
    LiteratureSource(
        "fahim-etal-2024-banglatlit",
        "BanglaTLit",
        "Banglish/script robustness",
        "literature/papers/banglatlit_2024_findings_emnlp.pdf",
        "literature/text/banglatlit_2024_findings_emnlp.txt",
    ),
    LiteratureSource(
        "haider-etal-2025-robustness",
        "Bangla transliteration robustness",
        "Banglish/script robustness",
        "literature/papers/bangla_transliteration_robustness_2025_banglalp.pdf",
        "literature/text/bangla_transliteration_robustness_2025_banglalp.txt",
    ),
    LiteratureSource(
        "banglishrev2024",
        "BanglishRev",
        "Banglish/script robustness",
        "literature/papers/banglishrev_2412.13161.pdf",
        "literature/text/banglishrev_2412.13161.txt",
    ),
    LiteratureSource(
        "banth2024",
        "BAN-TH",
        "Banglish/script robustness",
        "literature/papers/banth_2410.13281.pdf",
        "literature/text/banth_2410.13281.txt",
    ),
    LiteratureSource(
        "bnsentmix2024",
        "BnSentMix",
        "Banglish/script robustness",
        "literature/papers/bnsentmix_2408.08964.pdf",
        "literature/text/bnsentmix_2408.08964.txt",
    ),
    LiteratureSource(
        "mixsarc2026",
        "MixSarc",
        "Banglish/script robustness",
        "literature/papers/mixsarc_2602.21608.pdf",
        "literature/text/mixsarc_2602.21608.txt",
    ),
    LiteratureSource(
        "bhashaabhijnaanam2023",
        "Bhasha-Abhijnaanam",
        "Banglish/script robustness",
        "literature/papers/bhasha_abhijnaanam_2305.15814.pdf",
        "literature/text/bhasha_abhijnaanam_2305.15814.txt",
    ),
    LiteratureSource(
        "indotranslit2025",
        "IndoTranslit",
        "Banglish/script robustness",
        "literature/papers/indotranslit_2511.22769.pdf",
        "literature/text/indotranslit_2511.22769.txt",
    ),
    LiteratureSource(
        "scriptgap2025",
        "Script Gap",
        "Banglish/script robustness",
        "literature/papers/script_gap_2512.10780.pdf",
        "literature/text/script_gap_2512.10780.txt",
    ),
    LiteratureSource(
        "romanizednepali2026",
        "Romanized Nepali LLM Benchmark",
        "Banglish/script robustness",
        "literature/papers/romanized_nepali_llm_benchmark_2604.14171.pdf",
        "literature/text/romanized_nepali_llm_benchmark_2604.14171.txt",
    ),
    LiteratureSource(
        "tokenizerfairness2023",
        "Do All Languages Cost The Same?",
        "Mechanism/tokenization",
        "literature/papers/do_all_languages_cost_same_2305.15425.pdf",
        "literature/text/do_all_languages_cost_same_2305.15425.txt",
    ),
    LiteratureSource(
        "romanlens2025",
        "RomanLens",
        "Mechanism/tokenization",
        "literature/papers/romanlens_2502.07424.pdf",
        "literature/text/romanlens_2502.07424.txt",
    ),
    LiteratureSource(
        "wendler-etal-2024-llamas",
        "Do Llamas Work in English?",
        "Mechanism/tokenization",
        "literature/papers/do_llamas_work_in_english_2024_acl.pdf",
        "literature/text/do_llamas_work_in_english_2024_acl.txt",
    ),
    LiteratureSource(
        "thinkenglish2025",
        "Do Multilingual LLMs Think in English?",
        "Mechanism/tokenization",
        "literature/papers/do_multilingual_llms_think_in_english_2502.15603.pdf",
        "literature/text/do_multilingual_llms_think_in_english_2502.15603.txt",
    ),
    LiteratureSource(
        "malturdu2025",
        "MALT Urdu",
        "Mechanism/tokenization",
        "literature/papers/malt_urdu_2502.00041.pdf",
        "literature/text/malt_urdu_2502.00041.txt",
    ),
    LiteratureSource(
        "banglanlg2022",
        "BanglaNLG/BanglaT5",
        "Bangla model ecosystem",
        "literature/papers/bangla_nlg_banglat5_2205.11081.pdf",
        "literature/text/bangla_nlg_banglat5_2205.11081.txt",
    ),
    LiteratureSource(
        "banglabyt52025",
        "BanglaByT5",
        "Bangla model ecosystem",
        "literature/papers/banglabyt5_2505.17102.pdf",
        "literature/text/banglabyt5_2505.17102.txt",
    ),
    LiteratureSource(
        "titullms2025",
        "TituLLMs",
        "Bangla model ecosystem",
        "literature/papers/titullms_2502.11187.pdf",
        "literature/text/titullms_2502.11187.txt",
    ),
    LiteratureSource(
        "raihan-zampieri-2025-tigerllm",
        "TigerLLM",
        "Bangla model ecosystem",
        "literature/papers/tigerllm_2025_acl_short.pdf",
        "literature/text/tigerllm_2025_acl_short.txt",
    ),
]


def has_bib_key(bib_text: str, key: str) -> bool:
    return bool(re.search(rf"@\w+\{{{re.escape(key)},", bib_text))


def source_status(row: dict[str, str | bool]) -> str:
    missing = [
        label
        for label in ["bib_key_present", "citation_map_present", "paper_exists", "text_exists"]
        if not row[label]
    ]
    return "ok" if not missing else "missing_" + ",".join(missing)


def write_csv(rows: list[dict[str, str | bool]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "citation_key",
        "name",
        "group",
        "paper_path",
        "text_path",
        "bib_key_present",
        "citation_map_present",
        "paper_exists",
        "text_exists",
        "status",
    ]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str | bool]], output: Path, csv_path: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    problems = [row for row in rows if row["status"] != "ok"]
    lines = [
        "# Literature Corpus Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report validates the citation-backed local literature corpus used for",
        "the Script Matters thesis argument. It checks that each selected source has",
        "a bibliography key, a citation-map row, a local paper, and extracted text.",
        "",
        f"Machine-readable check: `{csv_path}`.",
        "",
        "## Summary",
        "",
        f"- Expected citation-backed sources: {len(rows)}",
        f"- Complete sources: {len(rows) - len(problems)}",
        f"- Sources with issues: {len(problems)}",
        "",
    ]
    if problems:
        lines.extend(["## Issues", "", "| Source | Citation key | Status |", "| --- | --- | --- |"])
        for row in problems:
            lines.append(f"| {row['name']} | `{row['citation_key']}` | `{row['status']}` |")
            lines.append("")

    lines.extend(
        [
            "## Sources",
            "",
            "| Group | Source | Citation key | Paper | Text | Status |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(rows, key=lambda item: (str(item["group"]), str(item["name"]))):
        lines.append(
            "| {group} | {name} | `{key}` | `{paper}` | `{text}` | `{status}` |".format(
                group=row["group"],
                name=row["name"],
                key=row["citation_key"],
                paper=row["paper_path"],
                text=row["text_path"],
                status=row["status"],
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--bib",
        type=Path,
        default=ROOT / "literature/references_seed.bib",
    )
    parser.add_argument(
        "--citation-map",
        type=Path,
        default=ROOT / "literature/notes/citation_key_map.md",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/literature_corpus_check.csv",
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=ROOT / "reports/literature_corpus_check.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    bib_text = args.bib.read_text(encoding="utf-8", errors="replace")
    citation_map_text = args.citation_map.read_text(encoding="utf-8", errors="replace")

    rows: list[dict[str, str | bool]] = []
    for source in EXPECTED_SOURCES:
        row: dict[str, str | bool] = {
            "citation_key": source.citation_key,
            "name": source.name,
            "group": source.group,
            "paper_path": source.paper_path,
            "text_path": source.text_path,
            "bib_key_present": has_bib_key(bib_text, source.citation_key),
            "citation_map_present": f"`{source.citation_key}`" in citation_map_text,
            "paper_exists": (root / source.paper_path).exists(),
            "text_exists": (root / source.text_path).exists(),
        }
        row["status"] = source_status(row)
        rows.append(row)

    write_csv(rows, args.csv_output)
    write_markdown(rows, args.md_output, args.csv_output.relative_to(root))
    problems = [row for row in rows if row["status"] != "ok"]
    print(
        f"sources={len(rows)} complete={len(rows) - len(problems)} "
        f"issues={len(problems)} report={args.md_output}"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
