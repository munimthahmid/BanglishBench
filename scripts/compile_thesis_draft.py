#!/usr/bin/env python3
"""Compile chapter draft Markdown files into a single thesis draft."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


DEFAULT_CHAPTERS = [
    "reports/chapter_1_introduction_draft.md",
    "reports/chapter_2_related_work_draft.md",
    "reports/chapter_3_benchmark_construction_draft.md",
    "reports/chapter_4_main_results_draft.md",
    "reports/chapter_5_robustness_and_model_breadth_draft.md",
    "reports/chapter_6_failure_analysis_draft.md",
    "reports/chapter_7_tokenization_mechanism_draft.md",
    "reports/chapter_8_mitigation_draft.md",
    "reports/chapter_9_limitations_draft.md",
    "reports/chapter_10_conclusion_draft.md",
]


def strip_title(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip()
    return text.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="reports/thesis_draft_compiled.md")
    parser.add_argument("--chapter", action="append", dest="chapters")
    args = parser.parse_args()

    chapter_paths = [Path(path) for path in (args.chapters or DEFAULT_CHAPTERS)]
    missing = [str(path) for path in chapter_paths if not path.exists()]
    if missing:
        raise SystemExit(f"Missing chapter draft(s): {', '.join(missing)}")

    lines = [
        "# Script Matters Thesis Draft",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This compiled draft is generated from chapter drafts. Regenerate with:",
        "",
        "```bash",
        "python3 scripts/compile_thesis_draft.py",
        "```",
        "",
        "Source chapters:",
        "",
    ]
    for path in chapter_paths:
        lines.append(f"- `{path}`")
    lines.append("")

    for idx, path in enumerate(chapter_paths, 1):
        text = path.read_text(encoding="utf-8")
        lines.extend(["", "---", "", f"<!-- Source: {path} -->", ""])
        lines.append(strip_title(text))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"compiled {len(chapter_paths)} chapters to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
