#!/usr/bin/env python3
"""Build a seed BibTeX file and citation map from official metadata sources."""

from __future__ import annotations

import argparse
import re
import textwrap
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"


ACL_BIB_URLS = [
    "https://aclanthology.org/2024.findings-acl.68.bib",
    "https://aclanthology.org/2024.findings-emnlp.859.bib",
    "https://aclanthology.org/2025.banglalp-1.27.bib",
    "https://aclanthology.org/2024.acl-long.820.bib",
]


ARXIV_KEY_BY_ID = {
    "2205.11081": "banglanlg2022",
    "2510.12836": "banglamath2025",
    "2410.10229": "banglaquad2024",
    "2505.18951": "bnmmlu2025",
    "2505.21092": "bluck2025",
    "2603.05462": "nctbqa2026",
    "2511.08813": "bnli2025",
    "2603.15949": "banglasocialbench2026",
    "2603.21165": "banglaverse2026",
    "2602.14291": "bengaliloop2026",
    "2511.04560": "banglamedqa2025",
    "2505.17102": "banglabyt52025",
    "2502.11187": "titullms2025",
    "2511.22769": "indotranslit2025",
    "2412.13161": "banglishrev2024",
    "2410.13281": "banth2024",
    "2408.08964": "bnsentmix2024",
    "2602.21608": "mixsarc2026",
    "2305.15814": "bhashaabhijnaanam2023",
    "2502.07424": "romanlens2025",
    "2502.15603": "thinkenglish2025",
    "2502.00041": "malturdu2025",
    "2512.10780": "scriptgap2025",
    "2604.14171": "romanizednepali2026",
    "2305.15425": "tokenizerfairness2023",
    "2210.03057": "mgsm2022",
    "2110.14168": "gsm8k2021",
}


@dataclass
class CitationRow:
    key: str
    title: str
    year: str
    source: str
    url: str


@dataclass(frozen=True)
class ArxivFallback:
    title: str
    author: str
    year: str
    primary_class: str


ARXIV_FALLBACKS = {
    "2205.11081": ArxivFallback(
        title=(
            "BanglaNLG and BanglaT5: Benchmarks and Resources for Evaluating "
            "Low-Resource Natural Language Generation in Bangla"
        ),
        author="Abhik Bhattacharjee and Tahmid Hasan and Wasi Uddin Ahmad and Rifat Shahriyar",
        year="2022",
        primary_class="cs.CL",
    ),
    "2603.21165": ArxivFallback(
        title=(
            "Many Dialects, Many Languages, One Cultural Lens: Evaluating "
            "Multilingual VLMs for Bengali Culture Understanding Across "
            "Historically Linked Languages and Regional Dialects"
        ),
        author=(
            "Nurul Labib Sayeedi and Md. Faiyaz Abdullah Sayeedi and "
            "Shubhashis Roy Dipta and Rubaya Tabassum and Ariful Ekraj Hridoy "
            "and Mehraj Mahmood and Mahbub E Sobhani and Md. Tarek Hasan and "
            "Swakkhar Shatabda"
        ),
        year="2026",
        primary_class="cs.CL",
    ),
    "2602.14291": ArxivFallback(
        title="Bengali-Loop: Community Benchmarks for Long-Form Bangla ASR and Speaker Diarization",
        author=(
            "H.M. Shadman Tabib and Istiak Ahmmed Rifti and "
            "Abdullah Muhammed Amimul Ehsan and Somik Dasgupta and "
            "Md Zim Mim Siddiqee Sowdha and Abrar Jahin Sarker and "
            "Md. Rafiul Islam Nijamy and Tanvir Hossain and Mst. Metaly Khatun "
            "and Munzer Mahmood and Rakesh Debnath and Gourab Biswas and "
            "Asif Karim and Wahid Al Azad Navid and Masnoon Muztahid and "
            "Fuad Ahmed Udoy and Shahad Shahriar Rahman and "
            "Md. Tashdiqur Rahman Shifat and Most. Sonia Khatun and "
            "Mushfiqur Rahman and Md. Miraj Hasan and Anik Saha and "
            "Mohammad Ninad Mahmud Nobo and Soumik Bhattacharjee and "
            "Tusher Bhomik and Ahmmad Nur Swapnil and Shahriar Kabir"
        ),
        year="2026",
        primary_class="cs.SD",
    ),
    "2511.04560": ArxivFallback(
        title=(
            "BanglaMedQA and BanglaMMedBench: Evaluating Retrieval-Augmented "
            "Generation Strategies for Bangla Biomedical Question Answering"
        ),
        author=(
            "Sadia Sultana and Saiyma Sittul Muna and "
            "Mosammat Zannatul Samarukh and Ajwad Abrar and "
            "Tareque Mohmud Chowdhury"
        ),
        year="2025",
        primary_class="cs.CL",
    ),
    "2505.17102": ArxivFallback(
        title="BanglaByT5: Byte-Level Modelling for Bangla",
        author="Pramit Bhattacharyya and Arnab Bhattacharya",
        year="2025",
        primary_class="cs.CL",
    ),
    "2502.11187": ArxivFallback(
        title="TituLLMs: A Family of Bangla LLMs with Comprehensive Benchmarking",
        author=(
            "Shahriar Kabir Nahin and Rabindra Nath Nandi and Sagor Sarker and "
            "Quazi Sarwar Muhtaseem and Md Kowsher and Apu Chandraw Shill and "
            "Md Ibrahim and Mehadi Hasan Menon and Tareq Al Muntasir and Firoj Alam"
        ),
        year="2025",
        primary_class="cs.CL",
    ),
    "2604.14171": ArxivFallback(
        title=(
            "Benchmarking Linguistic Adaptation in Comparable-Sized LLMs: "
            "A Study of Llama-3.1-8B, Mistral-7B-v0.1, and Qwen3-8B on "
            "Romanized Nepali"
        ),
        author="Ananda Rimal and Adarsha Rimal",
        year="2026",
        primary_class="cs.CL",
    ),
}


MANUAL_BIBS = [
    (
        "\n".join(
            [
                "@misc{banglaguard2026,",
                "  title = {BanglaGuard: Benchmarking and Defending Large Language Models for Safety in Low-Resource Languages},",
                "  author = {{Anonymous}},",
                "  year = {2026},",
                "  howpublished = {OpenReview},",
                "  note = {Under double-blind review as an ICLR 2026 conference paper},",
                "  url = {https://openreview.net/forum?id=KTsGJzaEPg}",
                "}",
            ]
        ),
        CitationRow(
            key="banglaguard2026",
            title="BanglaGuard: Benchmarking and Defending Large Language Models for Safety in Low-Resource Languages",
            year="2026",
            source="OpenReview",
            url="https://openreview.net/forum?id=KTsGJzaEPg",
        ),
    ),
    (
        "\n".join(
            [
                "@inproceedings{raihan-zampieri-2025-tigerllm,",
                "  title = {TigerLLM - A Family of Bangla Large Language Models},",
                "  author = {Raihan, Nishat and Zampieri, Marcos},",
                "  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},",
                "  year = {2025},",
                "  address = {Vienna, Austria},",
                "  publisher = {Association for Computational Linguistics},",
                "  pages = {887--896},",
                "  doi = {10.18653/v1/2025.acl-short.69},",
                "  url = {https://aclanthology.org/2025.acl-short.69/}",
                "}",
            ]
        ),
        CitationRow(
            key="raihan-zampieri-2025-tigerllm",
            title="TigerLLM - A Family of Bangla Large Language Models",
            year="2025",
            source="ACL Anthology",
            url="https://aclanthology.org/2025.acl-short.69/",
        ),
    ),
]


def cached_bib_entries(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks = re.findall(r"(?ms)^@\w+\{.*?(?=^@\w+\{|\Z)", text)
    return {extract_bib_key(chunk): chunk.strip() for chunk in chunks}


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "script-matters-citation-seed"})
    last_error: Exception | None = None
    for _ in range(2):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8")
        except (TimeoutError, urllib.error.URLError) as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def normalize_space(text: str) -> str:
    return " ".join((text or "").split())


def bib_field(text: str) -> str:
    return normalize_space(text).replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def extract_bib_key(bib: str) -> str:
    match = re.search(r"@\w+\{([^,]+),", bib)
    return match.group(1) if match else "unknown"


def extract_bib_field(bib: str, field: str) -> str:
    pattern = re.compile(rf"\b{field}\s*=\s*[{{\"](.+?)[}}\"],", re.IGNORECASE | re.DOTALL)
    match = pattern.search(bib)
    return normalize_space(match.group(1)) if match else ""


def year_from_date(date: str) -> str:
    return (date or "")[:4]


def arxiv_id_from_entry(entry: ET.Element) -> str:
    raw = entry.findtext(f"{ATOM}id", default="")
    match = re.search(r"/abs/(\d{4}\.\d+)", raw)
    if not match:
        raise ValueError(f"Could not parse arXiv id from {raw!r}")
    return match.group(1)


def arxiv_bib(entry: ET.Element, key: str) -> tuple[str, CitationRow]:
    title = normalize_space(entry.findtext(f"{ATOM}title", default=""))
    published = entry.findtext(f"{ATOM}published", default="")
    year = year_from_date(published)
    authors = [
        normalize_space(author.findtext(f"{ATOM}name", default=""))
        for author in entry.findall(f"{ATOM}author")
    ]
    primary = entry.find(f"{ARXIV}primary_category")
    primary_class = primary.attrib.get("term", "") if primary is not None else ""
    arxiv_id = arxiv_id_from_entry(entry)
    url = f"https://arxiv.org/abs/{arxiv_id}"
    doi = entry.findtext(f"{ARXIV}doi", default="")
    author_field = " and ".join(authors)
    lines = [
        f"@misc{{{key},",
        f"  title = {{{bib_field(title)}}},",
        f"  author = {{{bib_field(author_field)}}},",
        f"  year = {{{year}}},",
        f"  eprint = {{{arxiv_id}}},",
        "  archivePrefix = {arXiv},",
    ]
    if primary_class:
        lines.append(f"  primaryClass = {{{primary_class}}},")
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    lines.append(f"  url = {{{url}}}")
    lines.append("}")
    return "\n".join(lines), CitationRow(key, title, year, "arXiv", url)


def fallback_arxiv_bib(arxiv_id: str, key: str, fallback: ArxivFallback) -> tuple[str, CitationRow]:
    url = f"https://arxiv.org/abs/{arxiv_id}"
    lines = [
        f"@misc{{{key},",
        f"  title = {{{bib_field(fallback.title)}}},",
        f"  author = {{{bib_field(fallback.author)}}},",
        f"  year = {{{fallback.year}}},",
        f"  eprint = {{{arxiv_id}}},",
        "  archivePrefix = {arXiv},",
        f"  primaryClass = {{{fallback.primary_class}}},",
        f"  url = {{{url}}}",
        "}",
    ]
    return "\n".join(lines), CitationRow(key, fallback.title, fallback.year, "arXiv", url)


def row_from_cached_bib(key: str, bib: str) -> CitationRow:
    eprint = extract_bib_field(bib, "eprint")
    url = extract_bib_field(bib, "url") or (f"https://arxiv.org/abs/{eprint}" if eprint else "")
    return CitationRow(
        key=key,
        title=extract_bib_field(bib, "title"),
        year=extract_bib_field(bib, "year"),
        source="arXiv",
        url=url,
    )


def fetch_arxiv_entries(ids: list[str]) -> list[ET.Element]:
    entries: list[ET.Element] = []
    for start in range(0, len(ids), 8):
        batch = ids[start : start + 8]
        params = urllib.parse.urlencode({"max_results": len(batch), "id_list": ",".join(batch)})
        xml_text = fetch_text(f"https://export.arxiv.org/api/query?{params}")
        root = ET.fromstring(xml_text)
        entries.extend(root.findall(f"{ATOM}entry"))
    return entries


def build_outputs() -> tuple[str, str]:
    bib_chunks: list[str] = []
    rows: list[CitationRow] = []
    cached_arxiv_bibs = cached_bib_entries(ROOT / "literature/references_seed.bib")

    for url in ACL_BIB_URLS:
        bib = fetch_text(url).strip()
        bib_chunks.append(bib)
        rows.append(
            CitationRow(
                key=extract_bib_key(bib),
                title=extract_bib_field(bib, "title"),
                year=extract_bib_field(bib, "year"),
                source="ACL Anthology",
                url=extract_bib_field(bib, "url"),
            )
        )

    try:
        entries = fetch_arxiv_entries(list(ARXIV_KEY_BY_ID))
    except Exception as exc:
        print(f"warning: arXiv API fetch failed, using cached/manual metadata where possible: {exc}")
        entries = []
    by_id = {arxiv_id_from_entry(entry): entry for entry in entries}
    unavailable: list[str] = []

    for arxiv_id, key in ARXIV_KEY_BY_ID.items():
        if arxiv_id in by_id:
            bib, row = arxiv_bib(by_id[arxiv_id], key)
        elif key in cached_arxiv_bibs:
            bib = cached_arxiv_bibs[key]
            row = row_from_cached_bib(key, bib)
        elif arxiv_id in ARXIV_FALLBACKS:
            bib, row = fallback_arxiv_bib(arxiv_id, key, ARXIV_FALLBACKS[arxiv_id])
        else:
            unavailable.append(arxiv_id)
            continue
        bib_chunks.append(bib)
        rows.append(row)
    if unavailable:
        raise RuntimeError(f"Missing arXiv metadata for: {', '.join(unavailable)}")

    for bib, row in MANUAL_BIBS:
        bib_chunks.append(bib)
        rows.append(row)

    bib_text = "\n\n".join(bib_chunks) + "\n"
    md_lines = [
        "# Citation Key Map",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "Generated from official ACL Anthology BibTeX exports, the arXiv API,",
        "and manually recorded venue metadata.",
        "Use `literature/references_seed.bib` as a starting bibliography, then",
        "adjust formatting for the final thesis template.",
        "",
        "| Citation key | Year | Source | Title | URL |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in sorted(rows, key=lambda item: (item.year, item.key)):
        title = row.title.replace("|", r"\|")
        md_lines.append(f"| `{row.key}` | {row.year} | {row.source} | {title} | {row.url} |")
    md_lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is a seed file, not a final thesis bibliography.",
            "- Prefer venue BibTeX over arXiv BibTeX when a final proceedings version exists.",
            "- Keep citation keys stable once chapters start using them.",
            "",
        ]
    )
    return bib_text, "\n".join(md_lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bib-output",
        type=Path,
        default=ROOT / "literature/references_seed.bib",
    )
    parser.add_argument(
        "--map-output",
        type=Path,
        default=ROOT / "literature/notes/citation_key_map.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bib_text, map_text = build_outputs()
    args.bib_output.parent.mkdir(parents=True, exist_ok=True)
    args.map_output.parent.mkdir(parents=True, exist_ok=True)
    args.bib_output.write_text(bib_text, encoding="utf-8")
    args.map_output.write_text(textwrap.dedent(map_text), encoding="utf-8")
    print(f"wrote={args.bib_output}")
    print(f"wrote={args.map_output}")


if __name__ == "__main__":
    main()
