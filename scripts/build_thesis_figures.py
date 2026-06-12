#!/usr/bin/env python3
"""Build lightweight SVG thesis figures from generated CSV tables."""

from __future__ import annotations

import argparse
import csv
import html
import math
import re
from pathlib import Path


COLORS = {
    "bangla": "#2a9d8f",
    "banglish": "#e76f51",
    "english": "#457b9d",
    "agreement": "#6d597a",
    "oracle": "#8ab17d",
    "positive": "#2a9d8f",
    "negative": "#d1495b",
    "neutral": "#6c757d",
    "grid": "#d8dee4",
    "axis": "#30363d",
    "text": "#24292f",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct_from_fraction(value: str) -> float:
    num, den = value.split("/", 1)
    return 100.0 * float(num) / float(den)


def float_from_delta(value: str) -> float:
    match = re.search(r"([+-]?\d+(?:\.\d+)?)", value)
    if not match:
        raise ValueError(f"Could not parse delta from {value!r}")
    return float(match.group(1))


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def svg_text(x: float, y: float, text: str, size: int = 12, anchor: str = "middle", weight: str = "400") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="Arial, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS["text"]}">{esc(text)}</text>'
    )


def write_grouped_bar_chart(
    output: Path,
    title: str,
    rows: list[dict[str, str]],
    series: list[tuple[str, str, str]],
    ylabel: str,
) -> None:
    width, height = 980, 560
    left, right, top, bottom = 80, 40, 70, 120
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_value = max(pct_from_fraction(row[col]) for row in rows for _, col, _ in series)
    ymax = max(10, int(math.ceil(max_value / 10.0) * 10))
    group_w = plot_w / len(rows)
    bar_w = min(34, group_w / (len(series) + 2))

    def y(value: float) -> float:
        return top + plot_h - (value / ymax) * plot_h

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(width / 2, 32, title, size=18, weight="700"),
        svg_text(20, top + plot_h / 2, ylabel, size=12, anchor="middle"),
    ]

    for tick in range(0, ymax + 1, 10):
        yy = y(tick)
        lines.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="{COLORS["grid"]}" stroke-width="1"/>')
        lines.append(svg_text(left - 12, yy + 4, str(tick), size=11, anchor="end"))

    lines.append(f'<line x1="{left}" y1="{top+plot_h:.1f}" x2="{width-right}" y2="{top+plot_h:.1f}" stroke="{COLORS["axis"]}" stroke-width="1.4"/>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="{COLORS["axis"]}" stroke-width="1.4"/>')

    for i, row in enumerate(rows):
        center = left + group_w * (i + 0.5)
        start = center - (len(series) * bar_w) / 2
        for j, (label, col, color) in enumerate(series):
            value = pct_from_fraction(row[col])
            x = start + j * bar_w
            yy = y(value)
            h = top + plot_h - yy
            lines.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{bar_w-3:.1f}" height="{h:.1f}" fill="{color}" rx="2"/>')
            lines.append(svg_text(x + (bar_w - 3) / 2, yy - 6, f"{value:.1f}", size=10))
        lines.append(svg_text(center, top + plot_h + 28, row["Model"], size=12))
        lines.append(svg_text(center, top + plot_h + 46, row.get("Slice", ""), size=10))

    legend_x = left
    legend_y = height - 35
    for label, _, color in series:
        lines.append(f'<rect x="{legend_x}" y="{legend_y-11}" width="14" height="14" fill="{color}" rx="2"/>')
        lines.append(svg_text(legend_x + 20, legend_y, label, size=12, anchor="start"))
        legend_x += 155

    lines.append("</svg>")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_delta_chart(output: Path, rows: list[dict[str, str]]) -> None:
    width, height = 880, 500
    left, right, top, bottom = 90, 50, 70, 100
    plot_w = width - left - right
    plot_h = height - top - bottom
    values = [float_from_delta(row["Delta"]) for row in rows]
    limit = max(abs(min(values)), abs(max(values)), 5)
    ymax = int(math.ceil(limit / 5.0) * 5)
    group_w = plot_w / len(rows)
    bar_w = min(70, group_w * 0.42)

    def y(value: float) -> float:
        return top + plot_h / 2 - (value / ymax) * (plot_h / 2)

    zero_y = y(0)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(width / 2, 32, "Self-Normalization Delta vs Banglish Baseline", size=18, weight="700"),
        svg_text(26, top + plot_h / 2, "Accuracy delta (pts)", size=12),
    ]

    for tick in range(-ymax, ymax + 1, 5):
        yy = y(tick)
        stroke = COLORS["axis"] if tick == 0 else COLORS["grid"]
        sw = "1.5" if tick == 0 else "1"
        lines.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="{stroke}" stroke-width="{sw}"/>')
        lines.append(svg_text(left - 12, yy + 4, str(tick), size=11, anchor="end"))

    for i, row in enumerate(rows):
        value = float_from_delta(row["Delta"])
        center = left + group_w * (i + 0.5)
        x = center - bar_w / 2
        yy = min(y(value), zero_y)
        h = abs(y(value) - zero_y)
        color = COLORS["positive"] if value > 0 else COLORS["negative"] if value < 0 else COLORS["neutral"]
        lines.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}" rx="2"/>')
        label_y = yy - 8 if value >= 0 else yy + h + 18
        lines.append(svg_text(center, label_y, f"{value:+.1f}", size=12, weight="700"))
        lines.append(svg_text(center, top + plot_h + 30, row["Model"], size=12))
        lines.append(svg_text(center, top + plot_h + 48, row["95% CI"], size=10))

    lines.append("</svg>")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(output: Path) -> None:
    lines = [
        "# Draft Thesis Figures",
        "",
        "Generated from `results/tables/*.csv` by:",
        "",
        "```bash",
        "python3 scripts/build_thesis_figures.py",
        "```",
        "",
        "Files:",
        "",
        "- `main_script_gap.svg`: Bangla/reviewed-Banglish/English accuracy for the frozen-v5 main Qwen table.",
        "- `selfnorm_delta.svg`: self-normalization delta vs Banglish baseline.",
        "- `cross_script_recovery.svg`: frozen-v5 reviewed Banglish, privileged agreement route, and oracle.",
        "",
        "Regenerate after `scripts/build_thesis_tables.py` changes the source CSVs.",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tables-dir", default="results/tables")
    parser.add_argument("--output-dir", default="reports/figures")
    args = parser.parse_args()

    tables = Path(args.tables_dir)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    main_rows = read_csv(tables / "main_script_gap_validation200_v5.csv")
    write_grouped_bar_chart(
        output / "main_script_gap.svg",
        "Validation-200 Frozen V5 Main Script Gap",
        main_rows,
        [
            ("Bangla", "Bangla", COLORS["bangla"]),
            ("Reviewed Banglish", "Reviewed Banglish", COLORS["banglish"]),
            ("English", "English", COLORS["english"]),
        ],
        "Accuracy (%)",
    )

    selfnorm_rows = read_csv(tables / "selfnorm_validation200.csv")
    write_delta_chart(output / "selfnorm_delta.svg", selfnorm_rows)

    recovery_rows = read_csv(tables / "cross_script_answer_agreement.csv")
    write_grouped_bar_chart(
        output / "cross_script_recovery.svg",
        "Cross-Script Recovery Signals",
        recovery_rows,
        [
            ("Banglish", "Banglish", COLORS["banglish"]),
            ("Agreement route", "Agreement route", COLORS["agreement"]),
            ("Oracle", "Oracle", COLORS["oracle"]),
        ],
        "Accuracy (%)",
    )
    write_readme(output / "README.md")
    print(f"wrote SVG figures to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
