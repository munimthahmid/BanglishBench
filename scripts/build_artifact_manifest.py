#!/usr/bin/env python3
"""Build a non-secret reproducibility manifest for thesis artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_INCLUDE_ROOTS = [
    "project_index.md",
    "thesis_plan.md",
    "research_log.md",
    "requirements-kaggle.txt",
    "data/slices",
    "data/generated_views",
    "literature/notes",
    "reports",
    "results/analysis",
    "results/experiment_log.md",
    "results/tables",
    "scripts",
]

SECRET_PATTERNS = [
    "kaggle.json",
    "kaggle (1).json",
    "kaggle_api",
    ".pem",
    ".env",
]

SKIP_PARTS = {
    "__pycache__",
    ".ipynb_checkpoints",
}

SELF_OUTPUTS = {
    "reports/reproducibility_artifact_manifest.md",
    "results/analysis/reproducibility_artifact_manifest.csv",
}


@dataclass(frozen=True)
class Artifact:
    path: str
    bytes: int
    sha256: str
    category: str


def is_secret_or_generated_noise(path: Path) -> bool:
    path_text = str(path)
    lower_name = path.name.lower()
    if path_text in SELF_OUTPUTS:
        return True
    if any(part in SKIP_PARTS for part in path.parts):
        return True
    return any(pattern in path_text or pattern in lower_name for pattern in SECRET_PATTERNS)


def categorize(path: Path) -> str:
    text = str(path)
    if text.startswith("data/slices/"):
        return "dataset_slice"
    if text.startswith("data/generated_views/"):
        return "generated_view"
    if text.startswith("literature/notes/"):
        return "literature_note"
    if text in {"project_index.md", "thesis_plan.md", "research_log.md", "requirements-kaggle.txt"}:
        return "project_log"
    if text.startswith("reports/"):
        return "report"
    if text == "results/experiment_log.md":
        return "project_log"
    if text.startswith("results/analysis/"):
        return "analysis_table"
    if text.startswith("results/tables/"):
        return "thesis_table"
    if text.startswith("scripts/"):
        return "script"
    return "other"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def iter_artifacts(root: Path, include_roots: list[str]) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for include_root in include_roots:
        start = root / include_root
        if not start.exists():
            continue
        files = [start] if start.is_file() else sorted(p for p in start.rglob("*") if p.is_file())
        for path in files:
            rel = path.relative_to(root)
            if is_secret_or_generated_noise(rel):
                continue
            artifacts.append(
                Artifact(
                    path=str(rel),
                    bytes=path.stat().st_size,
                    sha256=sha256_file(path),
                    category=categorize(rel),
                )
            )
    return sorted(artifacts, key=lambda item: (item.category, item.path))


def write_csv(artifacts: list[Artifact], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "category", "bytes", "sha256"])
        writer.writeheader()
        for artifact in artifacts:
            writer.writerow(
                {
                    "path": artifact.path,
                    "category": artifact.category,
                    "bytes": artifact.bytes,
                    "sha256": artifact.sha256,
                }
            )


def write_markdown(artifacts: list[Artifact], output: Path, csv_path: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    by_category: dict[str, list[Artifact]] = {}
    for artifact in artifacts:
        by_category.setdefault(artifact.category, []).append(artifact)

    lines: list[str] = [
        "# Reproducibility Artifact Manifest",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This manifest records non-secret local artifacts needed to reproduce the",
        "current Script Matters thesis state. It intentionally excludes Kaggle API",
        "keys, PEM files, virtual environments, raw credential files, and its own",
        "generated manifest outputs.",
        "",
        f"Machine-readable manifest: `{csv_path}`.",
        "",
        "## Summary",
        "",
        "| Category | Files | Total bytes |",
        "| --- | ---: | ---: |",
    ]

    for category in sorted(by_category):
        group = by_category[category]
        lines.append(f"| {category} | {len(group)} | {sum(item.bytes for item in group)} |")

    lines.extend(
        [
            "",
            "## Core Thesis Artifacts",
            "",
            "| Path | Category | Bytes | SHA-256 prefix |",
            "| --- | --- | ---: | --- |",
        ]
    )

    core_prefixes = (
        "data/slices/validation_200",
        "reports/thesis_",
        "reports/evidence_matrix",
        "reports/current_research_state",
        "reports/post_v5",
        "reports/final_api",
        "reports/dataset_card",
        "results/tables/",
        "project_index.md",
        "thesis_plan.md",
        "research_log.md",
        "results/experiment_log.md",
        "requirements-kaggle.txt",
        "scripts/run_eval_kaggle.py",
        "scripts/validate_banglish_review_queue.py",
        "scripts/apply_banglish_review.py",
    )
    core = [item for item in artifacts if item.path.startswith(core_prefixes)]
    for item in core:
        lines.append(f"| `{item.path}` | {item.category} | {item.bytes} | `{item.sha256[:12]}` |")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Rebuild this manifest after freezing v5 or regenerating thesis tables.",
            "- Treat changes in dataset slices, parser/evaluator scripts, or thesis",
            "  tables as versioned thesis events and log them in `research_log.md`.",
            "- The full CSV contains every included artifact and complete SHA-256 hash.",
        ]
    )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root.")
    parser.add_argument(
        "--csv-output",
        default="results/analysis/reproducibility_artifact_manifest.csv",
        help="Path for the machine-readable manifest.",
    )
    parser.add_argument(
        "--md-output",
        default="reports/reproducibility_artifact_manifest.md",
        help="Path for the Markdown summary.",
    )
    parser.add_argument(
        "--include-root",
        action="append",
        dest="include_roots",
        help="Root path to include. May be repeated. Defaults cover thesis artifacts.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    include_roots = args.include_roots or DEFAULT_INCLUDE_ROOTS
    artifacts = iter_artifacts(root, include_roots)
    csv_path = Path(args.csv_output)
    md_path = Path(args.md_output)
    write_csv(artifacts, root / csv_path)
    write_markdown(artifacts, root / md_path, csv_path)
    print(
        f"wrote {len(artifacts)} artifacts | csv={root / csv_path} | md={root / md_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
