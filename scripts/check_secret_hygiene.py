#!/usr/bin/env python3
"""Scan non-secret thesis artifacts for accidental credential leaks."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

INCLUDE_ROOTS = [
    "project_index.md",
    "thesis_plan.md",
    "research_log.md",
    "requirements-kaggle.txt",
    "kaggle_api_workflow.md",
    "data/slices",
    "data/generated_views",
    "literature/notes",
    "reports",
    "results/analysis",
    "results/experiment_log.md",
    "results/tables",
    "scripts",
]

SECRET_FILENAME_MARKERS = (
    "kaggle.json",
    "kaggle_api",
    ".pem",
    ".env",
)

SKIP_PARTS = {
    "__pycache__",
    ".ipynb_checkpoints",
}

PATTERNS = [
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b")),
    ("hf_token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    ("kaggle_env_key", re.compile(r"\bKAGGLE_KEY\s*=\s*['\"]?([A-Za-z0-9_-]{16,})")),
    ("kaggle_json_key", re.compile(r'"key"\s*:\s*"([A-Za-z0-9_-]{16,})"')),
]

ALLOW_MARKERS = (
    "YOUR_KEY",
    "your_api_key",
    "your_key",
    "<key>",
    "<api_key>",
    "REDACTED",
    "redacted",
    "placeholder",
    "example",
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    pattern: str
    excerpt: str


def is_secret_filename(path: Path) -> bool:
    text = str(path)
    lower_name = path.name.lower()
    return any(marker in text or marker in lower_name for marker in SECRET_FILENAME_MARKERS)


def iter_files(root: Path, include_roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for include_root in include_roots:
        start = root / include_root
        if not start.exists():
            continue
        candidates = [start] if start.is_file() else sorted(path for path in start.rglob("*") if path.is_file())
        for path in candidates:
            rel = path.relative_to(root)
            if any(part in SKIP_PARTS for part in rel.parts):
                continue
            if is_secret_filename(rel):
                continue
            files.append(path)
    return sorted(set(files))


def allowed_placeholder(line: str) -> bool:
    return any(marker in line for marker in ALLOW_MARKERS)


def safe_excerpt(line: str) -> str:
    text = line.strip()
    if len(text) > 120:
        text = text[:117] + "..."
    return text.replace("|", r"\|")


def scan_file(root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_no, line in enumerate(text.splitlines(), 1):
        if allowed_placeholder(line):
            continue
        for name, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        path=str(path.relative_to(root)),
                        line=line_no,
                        pattern=name,
                        excerpt=safe_excerpt(line),
                    )
                )
    return findings


def write_csv(findings: list[Finding], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "line", "pattern", "excerpt"])
        writer.writeheader()
        for finding in findings:
            writer.writerow(
                {
                    "path": finding.path,
                    "line": finding.line,
                    "pattern": finding.pattern,
                    "excerpt": finding.excerpt,
                }
            )


def write_markdown(findings: list[Finding], output: Path, csv_path: Path, checked_files: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Secret Hygiene Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This scan checks non-secret thesis artifacts for common credential patterns.",
        "It intentionally skips credential filenames such as Kaggle JSON/API files,",
        "PEM keys, and `.env` files; those files must never be added to reports or",
        "release manifests.",
        "",
        f"Machine-readable findings: `{csv_path}`.",
        "",
        "## Summary",
        "",
        f"- Files checked: {checked_files}",
        f"- Suspicious findings: {len(findings)}",
        "",
    ]
    if findings:
        lines.extend(["## Findings", "", "| File | Line | Pattern | Excerpt |", "| --- | ---: | --- | --- |"])
        for finding in findings:
            lines.append(
                f"| `{finding.path}` | {finding.line} | `{finding.pattern}` | `{finding.excerpt}` |"
            )
    else:
        lines.append("No suspicious credential patterns found in non-secret thesis artifacts.")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=ROOT / "results/analysis/secret_hygiene_check.csv",
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=ROOT / "reports/secret_hygiene_check.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    files = iter_files(root, INCLUDE_ROOTS)
    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(root, path))
    write_csv(findings, args.csv_output)
    write_markdown(findings, args.md_output, args.csv_output.relative_to(root), len(files))
    print(f"files={len(files)} suspicious={len(findings)} report={args.md_output}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
