#!/usr/bin/env python3
"""Validate generated SVG thesis figure artifacts."""

from __future__ import annotations

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIGURES = {
    "main_script_gap.svg": "Validation-200 Frozen V5 Main Script Gap",
    "selfnorm_delta.svg": "Self-Normalization Delta vs Banglish Baseline",
    "cross_script_recovery.svg": "Cross-Script Recovery Signals",
}


def add(rows: list[dict[str, str]], figure: str, check: str, status: str, detail: str) -> None:
    rows.append({"figure": figure, "check": check, "status": status, "detail": detail})


def svg_children(root: ET.Element, suffix: str) -> list[ET.Element]:
    return [element for element in root.iter() if element.tag.endswith(suffix)]


def validate_svg(path: Path, expected_title: str, rows: list[dict[str, str]]) -> None:
    rel = str(path.relative_to(ROOT))
    if not path.exists():
        add(rows, rel, "exists", "error", "missing")
        return
    size = path.stat().st_size
    add(rows, rel, "size", "ok" if size > 1000 else "error", f"bytes={size}")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        add(rows, rel, "xml_parse", "error", str(exc))
        return
    add(rows, rel, "xml_parse", "ok", "parseable")
    add(rows, rel, "root_svg", "ok" if root.tag.endswith("svg") else "error", root.tag)
    width = root.attrib.get("width", "")
    height = root.attrib.get("height", "")
    viewbox = root.attrib.get("viewBox", "")
    geometry_ok = width.isdigit() and height.isdigit() and bool(viewbox)
    add(rows, rel, "geometry", "ok" if geometry_ok else "error", f"width={width} height={height} viewBox={viewbox}")
    texts = [element.text or "" for element in svg_children(root, "text")]
    rects = svg_children(root, "rect")
    title_ok = expected_title in texts
    add(rows, rel, "title_text", "ok" if title_ok else "error", expected_title)
    add(rows, rel, "text_count", "ok" if len(texts) >= 10 else "error", f"text_nodes={len(texts)}")
    add(rows, rel, "rect_count", "ok" if len(rects) >= 4 else "error", f"rect_nodes={len(rects)}")


def validate_readme(figure_dir: Path, rows: list[dict[str, str]]) -> None:
    path = figure_dir / "README.md"
    rel = str(path.relative_to(ROOT))
    if not path.exists():
        add(rows, rel, "exists", "error", "missing")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    add(rows, rel, "exists", "ok", "present")
    for name in EXPECTED_FIGURES:
        add(rows, rel, f"mentions_{name}", "ok" if name in text else "error", name)


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["figure", "check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, str]], output: Path, csv_path: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    issues = [row for row in rows if row["status"] != "ok"]
    lines = [
        "# Thesis Figure Integrity Check",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This report validates the generated SVG thesis figures after rebuilding",
        "them from thesis result tables.",
        "",
        f"Machine-readable check: `{csv_path.relative_to(ROOT)}`.",
        "",
        "## Summary",
        "",
        f"- Checks: {len(rows)}",
        f"- Issues: {len(issues)}",
        "",
    ]
    if issues:
        lines.extend(["## Issues", ""])
        for row in issues:
            lines.append(f"- `{row['figure']}` `{row['check']}`: {row['detail']}")
        lines.append("")
    else:
        lines.extend(["No thesis figure integrity issues found.", ""])
    lines.extend(["## Checks", "", "| Figure | Check | Status | Detail |", "| --- | --- | --- | --- |"])
    for row in rows:
        lines.append(f"| `{row['figure']}` | `{row['check']}` | `{row['status']}` | {row['detail']} |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure-dir", type=Path, default=ROOT / "reports/figures")
    parser.add_argument("--output-csv", type=Path, default=ROOT / "results/analysis/thesis_figure_integrity_check.csv")
    parser.add_argument("--output-md", type=Path, default=ROOT / "reports/thesis_figure_integrity_check.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows: list[dict[str, str]] = []
    for name, title in EXPECTED_FIGURES.items():
        validate_svg(args.figure_dir / name, title, rows)
    validate_readme(args.figure_dir, rows)
    write_csv(rows, args.output_csv)
    write_report(rows, args.output_md, args.output_csv)
    issues = [row for row in rows if row["status"] != "ok"]
    print(f"checks={len(rows)} issues={len(issues)} report={args.output_md}")
    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
