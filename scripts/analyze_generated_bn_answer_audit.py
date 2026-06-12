#!/usr/bin/env python3
"""Analyze generated-Bengali answer-audit outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from run_eval_kaggle import is_correct, parse_answer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS = (
    ROOT
    / "data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl"
)
DEFAULT_SUMMARY = (
    ROOT / "results/analysis/qwen3_4b_generated_bn_answer_audit_dev50_summary.csv"
)
DEFAULT_COMPARE = (
    ROOT / "results/analysis/qwen3_4b_generated_bn_answer_audit_dev50_item_compare.csv"
)
DEFAULT_REPORT = ROOT / "reports/qwen3_4b_generated_bn_answer_audit_dev50.md"
BASELINE_VARIANT = "banglish_clean"
GENERATED_VARIANTS = [
    "generated_bn_phonetic_protected",
    "generated_bn_bnb_protected",
]


def jsonl_paths(inputs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.jsonl")))
        else:
            paths.append(path)
    return paths


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_eval_rows(inputs: list[Path], rescore: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in jsonl_paths(inputs):
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not {"id", "variant", "model"}.issubset(row):
                    continue
                if rescore:
                    if row.get("raw_output"):
                        row["parsed"] = parse_answer(
                            str(row.get("raw_output", "")),
                            str(row.get("answer_type", "")),
                        )
                    row["correct"] = is_correct(
                        str(row.get("parsed", "")),
                        str(row.get("gold", "")),
                        str(row.get("answer_type", "")),
                    )
                rows.append(row)
    return rows


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_gate_specs(raw_specs: list[str] | None) -> dict[str, Path]:
    specs: dict[str, Path] = {}
    for raw in raw_specs or []:
        if "=" not in raw:
            raise SystemExit("--gate-audit must use VARIANT=CSV")
        variant, path_text = raw.split("=", 1)
        variant = variant.strip()
        if not variant:
            raise SystemExit("--gate-audit VARIANT cannot be empty")
        path = Path(path_text.strip())
        if not path.is_absolute():
            path = ROOT / path
        specs[variant] = path
    return specs


def load_gate_lookup(specs: dict[str, Path]) -> dict[tuple[str, str], bool]:
    lookup: dict[tuple[str, str], bool] = {}
    for variant, path in specs.items():
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lookup[(variant, str(row.get("id", "")))] = parse_bool(
                    row.get("hard_fail", "")
                )
    return lookup


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(str(row.get("model", "")), str(row.get("variant", "")))].append(row)
    out: list[dict[str, Any]] = []
    for (model, variant), items in sorted(groups.items()):
        correct = sum(int(bool(row.get("correct"))) for row in items)
        parsed_empty = sum(int(not str(row.get("parsed", "")).strip()) for row in items)
        seconds = [float(row.get("seconds", 0.0) or 0.0) for row in items]
        out.append(
            {
                "model": model,
                "variant": variant,
                "n": len(items),
                "correct": correct,
                "accuracy": round(correct / len(items), 4) if items else 0.0,
                "parsed_empty": parsed_empty,
                "mean_seconds": round(sum(seconds) / len(seconds), 4) if seconds else 0.0,
                "total_seconds": round(sum(seconds), 4),
            }
        )
    return out


def change_label(before: bool, after: bool) -> str:
    if before and after:
        return "same_correct"
    if not before and not after:
        return "same_wrong"
    if not before and after:
        return "gain"
    return "loss"


def compare_rows(
    eval_rows: list[dict[str, Any]],
    items: dict[str, dict[str, Any]],
    baseline_variant: str,
    generated_variants: list[str],
    gate_lookup: dict[tuple[str, str], bool] | None = None,
) -> list[dict[str, Any]]:
    by_id_variant = {
        (str(row.get("id", "")), str(row.get("variant", ""))): row for row in eval_rows
    }
    out: list[dict[str, Any]] = []
    for item_id in sorted(items):
        baseline = by_id_variant.get((item_id, baseline_variant))
        if baseline is None:
            continue
        for variant in generated_variants:
            generated = by_id_variant.get((item_id, variant))
            if generated is None:
                continue
            base_correct = bool(baseline.get("correct"))
            gen_correct = bool(generated.get("correct"))
            out.append(
                {
                    "id": item_id,
                    "variant": variant,
                    "gold": baseline.get("gold", ""),
                    "baseline_correct": base_correct,
                    "generated_correct": gen_correct,
                    "gate_hard_fail": (gate_lookup or {}).get((variant, item_id), False),
                    "change": change_label(base_correct, gen_correct),
                    "baseline_parsed": baseline.get("parsed", ""),
                    "generated_parsed": generated.get("parsed", ""),
                    "baseline_raw": str(baseline.get("raw_output", ""))[:240].replace("\n", " "),
                    "generated_raw": str(generated.get("raw_output", ""))[:240].replace("\n", " "),
                    "generated_text": str(items[item_id].get(variant, ""))[:260].replace("\n", " "),
                }
            )
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def write_report(
    path: Path,
    inputs: list[Path],
    items_path: Path,
    summary_path: Path,
    compare_path: Path,
    summary: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    baseline_variant: str,
    generated_variants: list[str],
    provenance_note: str,
    report_title: str | None = None,
) -> None:
    changes = Counter((row["variant"], row["change"]) for row in comparisons)
    model_label = summary[0]["model"] if summary else "Model"
    title = report_title or f"{model_label} Generated-BN Answer Audit: Dev50 BEnQA MCQ"
    lines = [
        f"# {title}",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Eval inputs: {', '.join(f'`{repo_path(path)}`' for path in inputs)}",
        f"- Item slice: `{repo_path(items_path)}`",
        f"- Summary CSV: `{repo_path(summary_path)}`",
        f"- Item compare CSV: `{repo_path(compare_path)}`",
        "",
        "## Provenance",
        "",
        provenance_note,
        "",
        "## Accuracy",
        "",
        "| Variant | n | Correct | Accuracy | Parsed empty |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            f"| `{row['variant']}` | {row['n']} | {row['correct']} | "
            f"{float(row['accuracy']):.3f} | {row['parsed_empty']} |"
        )

    lines.extend(["", f"## Pairwise Changes vs `{baseline_variant}`", ""])
    lines.append("| Generated variant | Gains | Losses | Same correct | Same wrong |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for variant in generated_variants:
        lines.append(
            f"| `{variant}` | {changes[(variant, 'gain')]} | "
            f"{changes[(variant, 'loss')]} | {changes[(variant, 'same_correct')]} | "
            f"{changes[(variant, 'same_wrong')]} |"
        )

    if any("gate_hard_fail" in row for row in comparisons):
        lines.extend(["", "## Gate-Eligible Pairwise Changes", ""])
        lines.append(
            "| Generated variant | Gate hard fails | Eligible n | Baseline correct | "
            "Generated correct | Gains | Losses | Same correct | Same wrong |"
        )
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for variant in generated_variants:
            variant_rows = [row for row in comparisons if row["variant"] == variant]
            eligible = [row for row in variant_rows if not row.get("gate_hard_fail")]
            eligible_changes = Counter(row["change"] for row in eligible)
            lines.append(
                f"| `{variant}` | {sum(int(row.get('gate_hard_fail', False)) for row in variant_rows)} | "
                f"{len(eligible)} | {sum(int(row['baseline_correct']) for row in eligible)} | "
                f"{sum(int(row['generated_correct']) for row in eligible)} | "
                f"{eligible_changes['gain']} | {eligible_changes['loss']} | "
                f"{eligible_changes['same_correct']} | {eligible_changes['same_wrong']} |"
            )

    gains = [row for row in comparisons if row["change"] == "gain"]
    losses = [row for row in comparisons if row["change"] == "loss"]
    if gains:
        lines.extend(["", "## Example Gains", ""])
        for row in gains[:8]:
            lines.append(
                f"- `{row['id']}` `{row['variant']}` gold={row['gold']} "
                f"baseline={row['baseline_parsed']} generated={row['generated_parsed']}"
            )
    if losses:
        lines.extend(["", "## Example Losses", ""])
        for row in losses[:8]:
            lines.append(
                f"- `{row['id']}` `{row['variant']}` gold={row['gold']} "
                f"baseline={row['baseline_parsed']} generated={row['generated_parsed']}"
            )

    lines.extend(
        [
            "",
            "## Decision Rule",
            "",
            "This is a dev-only diagnostic. It can justify dropping or inspecting",
            "a generated-view path, but it must not be promoted to a held-out",
            "mitigation claim. A deployable route requires preservation-gate",
            "eligibility, a locked agreement route, and a held-out test",
            "protocol.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--items", type=Path, default=DEFAULT_ITEMS)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--compare-output", type=Path, default=DEFAULT_COMPARE)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--report-title")
    parser.add_argument("--baseline-variant", default=BASELINE_VARIANT)
    parser.add_argument(
        "--generated-variants",
        nargs="+",
        default=GENERATED_VARIANTS,
    )
    parser.add_argument(
        "--provenance-note",
        default=(
            "This report analyzes a generated-BN dev answer audit. It is "
            "dev-only evidence and must not be presented as a held-out "
            "mitigation claim."
        ),
    )
    parser.add_argument(
        "--gate-audit",
        action="append",
        help="Optional preservation gate CSV as VARIANT=CSV. Repeat per generated variant.",
    )
    parser.add_argument("--rescore", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    items = {str(row["id"]): row for row in load_jsonl(args.items)}
    eval_rows = load_eval_rows(args.inputs, args.rescore)
    if not eval_rows:
        raise SystemExit("No evaluation rows found.")
    summary = summarize(eval_rows)
    gate_lookup = load_gate_lookup(parse_gate_specs(args.gate_audit))
    comparisons = compare_rows(
        eval_rows,
        items,
        args.baseline_variant,
        args.generated_variants,
        gate_lookup,
    )
    write_csv(args.summary_output, summary)
    write_csv(args.compare_output, comparisons)
    write_report(
        args.report_output,
        args.inputs,
        args.items,
        args.summary_output,
        args.compare_output,
        summary,
        comparisons,
        args.baseline_variant,
        args.generated_variants,
        args.provenance_note,
        args.report_title,
    )
    print(f"rows={len(eval_rows)}")
    print(f"summary={args.summary_output}")
    print(f"compare={args.compare_output}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
