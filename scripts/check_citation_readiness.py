#!/usr/bin/env python3
"""Check citation-key readiness across bibliography and writing artifacts."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")
BACKTICK_RE = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class ExpectedCitation:
    citation_key: str
    name: str
    group: str


def load_expected_citations() -> list[ExpectedCitation]:
    corpus_script = ROOT / "scripts/check_literature_corpus.py"
    spec = importlib.util.spec_from_file_location("check_literature_corpus", corpus_script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {corpus_script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return [
        ExpectedCitation(source.citation_key, source.name, source.group)
        for source in module.EXPECTED_SOURCES
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bib_keys(text: str) -> tuple[set[str], set[str]]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for match in BIB_KEY_RE.finditer(text):
        key = match.group(1).strip()
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    return seen, duplicates


def citation_map_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        if line.startswith("| `"):
            parts = line.split("`")
            if len(parts) >= 3:
                keys.add(parts[1])
    return keys


def inline_citation_keys(text: str, known_keys: set[str]) -> set[str]:
    return {token for token in BACKTICK_RE.findall(text) if token in known_keys}


def build_rows(
    expected: list[ExpectedCitation],
    bib_key_set: set[str],
    map_key_set: set[str],
    chapter_key_set: set[str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for citation in expected:
        checks = {
            "bib_key_present": citation.citation_key in bib_key_set,
            "citation_map_present": citation.citation_key in map_key_set,
            "chapter2_checklist_present": citation.citation_key in chapter_key_set,
        }
        missing = [name for name, present in checks.items() if not present]
        rows.append(
            {
                "group": citation.group,
                "source": citation.name,
                "citation_key": citation.citation_key,
                **{name: str(present).lower() for name, present in checks.items()},
                "status": "ok" if not missing else "missing:" + ",".join(missing),
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "group",
        "source",
        "citation_key",
        "bib_key_present",
        "citation_map_present",
        "chapter2_checklist_present",
        "status",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    rows: list[dict[str, str]],
    duplicate_bib_keys: set[str],
    extra_map_keys: set[str],
    extra_chapter_keys: set[str],
    output_path: Path,
    csv_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    issues = [row for row in rows if row["status"] != "ok"]
    complete = len(rows) - len(issues)
    lines = [
        "# Citation Readiness Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report checks that the thesis literature corpus has stable citation",
        "keys in the seed bibliography, citation-key map, and Chapter 2 citation",
        "checklist.",
        "",
        f"Machine-readable check: `{csv_path.relative_to(ROOT)}`.",
        "",
        "## Summary",
        "",
        f"- Expected citation keys: {len(rows)}",
        f"- Complete keys: {complete}",
        f"- Keys with issues: {len(issues)}",
        f"- Duplicate BibTeX keys: {len(duplicate_bib_keys)}",
        f"- Citation-map extras not in expected corpus: {len(extra_map_keys)}",
        f"- Chapter 2 checklist extras not in expected corpus: {len(extra_chapter_keys)}",
        "",
    ]
    if issues or duplicate_bib_keys or extra_map_keys or extra_chapter_keys:
        lines.extend(["## Issues", ""])
        if duplicate_bib_keys:
            lines.append(
                "- Duplicate BibTeX keys: "
                + ", ".join(f"`{key}`" for key in sorted(duplicate_bib_keys))
            )
        for row in issues:
            lines.append(
                f"- `{row['citation_key']}` ({row['source']}): `{row['status']}`"
            )
        if extra_map_keys:
            lines.append(
                "- Citation-map extras: "
                + ", ".join(f"`{key}`" for key in sorted(extra_map_keys))
            )
        if extra_chapter_keys:
            lines.append(
                "- Chapter 2 checklist extras: "
                + ", ".join(f"`{key}`" for key in sorted(extra_chapter_keys))
            )
        lines.append("")
    else:
        lines.extend(
            [
                "No citation readiness issues found.",
                "",
            ]
        )
    lines.extend(
        [
            "## Expected Keys",
            "",
            "| Group | Source | Citation key | BibTeX | Map | Chapter 2 | Status |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(rows, key=lambda item: (item["group"], item["source"])):
        lines.append(
            "| {group} | {source} | `{key}` | `{bib}` | `{cmap}` | `{chapter}` | `{status}` |".format(
                group=row["group"],
                source=row["source"],
                key=row["citation_key"],
                bib=row["bib_key_present"],
                cmap=row["citation_map_present"],
                chapter=row["chapter2_checklist_present"],
                status=row["status"],
            )
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", type=Path, default=ROOT / "literature/references_seed.bib")
    parser.add_argument(
        "--citation-map",
        type=Path,
        default=ROOT / "literature/notes/citation_key_map.md",
    )
    parser.add_argument(
        "--chapter-2",
        type=Path,
        default=ROOT / "reports/chapter_2_related_work_draft.md",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "results/analysis/citation_readiness_check.csv",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=ROOT / "reports/citation_readiness_check.md",
    )
    args = parser.parse_args()

    expected = load_expected_citations()
    expected_keys = {citation.citation_key for citation in expected}
    bib_key_set, duplicate_bib_keys = bib_keys(read_text(args.bib))
    map_key_set = citation_map_keys(read_text(args.citation_map))
    chapter_key_set = inline_citation_keys(read_text(args.chapter_2), bib_key_set | expected_keys)

    rows = build_rows(expected, bib_key_set, map_key_set, chapter_key_set)
    extra_map_keys = map_key_set - expected_keys
    extra_chapter_keys = chapter_key_set - expected_keys

    write_csv(rows, args.output_csv)
    write_report(
        rows,
        duplicate_bib_keys,
        extra_map_keys,
        extra_chapter_keys,
        args.output_md,
        args.output_csv,
    )

    issue_count = sum(1 for row in rows if row["status"] != "ok")
    print(
        "expected={expected} complete={complete} issues={issues} "
        "duplicate_bib_keys={dupes} report={report}".format(
            expected=len(rows),
            complete=len(rows) - issue_count,
            issues=issue_count,
            dupes=len(duplicate_bib_keys),
            report=args.output_md,
        )
    )
    if issue_count or duplicate_bib_keys or extra_map_keys or extra_chapter_keys:
        sys.exit(1)


if __name__ == "__main__":
    main()
