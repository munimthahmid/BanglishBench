#!/usr/bin/env python3
"""Check Markdown references to local project artifacts."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


PATH_RE = re.compile(
    r"(?P<path>(?:data|reports|results|scripts|literature|kaggle_jobs)/[A-Za-z0-9_./()\\-]+|"
    r"(?:project_index|research_log|thesis_plan|requirements-kaggle)\.md|"
    r"requirements-kaggle\.txt)"
)

IGNORE_SUFFIXES = {
    ".com",
    ".org",
}

EXPECTED_FUTURE_MARKERS = (
    "validation_200_v5",
    "validation200_v5",
    "v5_banglish_sensitivity",
    "qwen25_validation200_v5_vs_v4_banglish",
    "generated_view_output_audit",
    "results/runs/smoke.jsonl",
    "results/runs/qwen2_5_7b_pilot20.jsonl",
    "phi4_mini_validation200_v4_dev50",
    "reports/phi4_mini_dev50_probe.md",
    "qwen25_3b_benqa_ext_smoke26",
    "qwen25_3b_benqa_ext_pilot130",
    "qwen25_3b_benqa_ext_full851",
)


def iter_markdown(root: Path, output: Path) -> list[Path]:
    paths: list[Path] = []
    for base in ["reports", "literature/notes", "data/slices"]:
        start = root / base
        if start.exists():
            paths.extend(sorted(start.rglob("*.md")))
    for name in ["project_index.md", "research_log.md", "thesis_plan.md"]:
        path = root / name
        if path.exists():
            paths.append(path)
    return sorted(path for path in set(paths) if path.resolve() != output.resolve())


def normalize(raw: str) -> str:
    return raw.rstrip(".,);:]").lstrip("`(")


def should_ignore(path: str) -> bool:
    if path.startswith("literature/text/") or path.startswith("literature/papers/"):
        return False
    return any(path.endswith(suffix) for suffix in IGNORE_SUFFIXES)


def is_expected_future(path: str) -> bool:
    return any(marker in path for marker in EXPECTED_FUTURE_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--output",
        default="reports/local_artifact_reference_check.md",
        help="Markdown report to write.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = (root / args.output).resolve()
    missing: list[tuple[str, int, str]] = []
    expected_future: list[tuple[str, int, str]] = []
    checked = 0
    for md in iter_markdown(root, output):
        rel_md = md.relative_to(root)
        for line_no, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for match in PATH_RE.finditer(line):
                raw = normalize(match.group("path"))
                if should_ignore(raw):
                    continue
                checked += 1
                if not (root / raw).exists():
                    target = expected_future if is_expected_future(raw) else missing
                    target.append((str(rel_md), line_no, raw))

    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Local Artifact Reference Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        f"Checked references: {checked}",
        f"Unexpected missing references: {len(missing)}",
        f"Expected future/planned references: {len(expected_future)}",
        "",
    ]
    if missing:
        lines.extend(["## Missing", "", "| File | Line | Reference |", "| --- | ---: | --- |"])
        for source, line_no, ref in missing:
            lines.append(f"| `{source}` | {line_no} | `{ref}` |")
    else:
        lines.append("No unexpected missing local artifact references found by the heuristic checker.")
    if expected_future:
        lines.extend(
            [
                "",
                "## Expected Future Or Planned",
                "",
                "| File | Line | Reference |",
                "| --- | ---: | --- |",
            ]
        )
        for source, line_no, ref in expected_future:
            lines.append(f"| `{source}` | {line_no} | `{ref}` |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"checked={checked} unexpected_missing={len(missing)} "
        f"expected_future={len(expected_future)} report={output}"
    )
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
