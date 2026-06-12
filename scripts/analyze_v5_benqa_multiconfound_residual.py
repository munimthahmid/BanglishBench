#!/usr/bin/env python3
"""Join BEnQA option confounds and test the residual Qwen3 D-attractor."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHOICE_ITEMS = ROOT / "results/analysis/v5_benqa_choice_bias_items.csv"
DEFAULT_POSITION_ITEMS = ROOT / "results/analysis/v5_benqa_option_position_content_items.csv"
DEFAULT_COVERAGE_ITEMS = ROOT / "results/analysis/v5_benqa_option_coverage_confound_items.csv"
DEFAULT_SEMANTIC_ITEMS = ROOT / "results/analysis/v5_benqa_option_semantic_cues_items.csv"
DEFAULT_SWITCH_ITEMS = ROOT / "results/analysis/v5_benqa_option_switching_items.csv"
DEFAULT_ITEMS_OUTPUT = ROOT / "results/analysis/v5_benqa_multiconfound_residual_items.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/v5_benqa_multiconfound_residual_summary.csv"
DEFAULT_REPORT = ROOT / "reports/v5_benqa_multiconfound_residual.md"

MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
BASELINES = ("bangla", "english")
BASELINE_LABELS = {"bangla": "Bangla", "english": "English"}


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{numerator / denominator:.4f}"


def percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100 * numerator / denominator:.1f}%"


def index_by_model_id(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["model"], row["id"]): row for row in read_csv(path)}


def build_item_rows(
    choice_items: Path,
    position_items: Path,
    coverage_items: Path,
    semantic_items: Path,
    switch_items: Path,
) -> list[dict[str, Any]]:
    position = index_by_model_id(position_items)
    coverage = index_by_model_id(coverage_items)
    semantic = index_by_model_id(semantic_items)
    switch = {
        (row["model"], row["baseline_variant"], row["id"]): row
        for row in read_csv(switch_items)
    }

    rows: list[dict[str, Any]] = []
    for choice in read_csv(choice_items):
        key = (choice["model"], choice["id"])
        if key not in position or key not in coverage or key not in semantic:
            raise SystemExit(f"Missing joined confound features for {key}")
        pos = position[key]
        cov = coverage[key]
        sem = semantic[key]
        gold_not_d = choice["gold"] != "D"
        d_not_longest = not truthy(pos["d_is_longest"])
        d_no_semantic_cue = truthy(sem["D_no_semantic_cue"])
        all_options_same_coverage = truthy(cov["all_options_same_coverage"])
        d_not_highest_coverage = truthy(cov["d_not_highest_coverage"])
        residual_primary = gold_not_d and d_not_longest and d_no_semantic_cue
        residual_tied_coverage = residual_primary and all_options_same_coverage
        residual_not_highest_coverage = residual_primary and d_not_highest_coverage
        banglish_d = choice["banglish_clean_parsed_option"] == "D"
        wrong_d = banglish_d and gold_not_d

        row: dict[str, Any] = {
            "model": choice["model"],
            "id": choice["id"],
            "subject": pos["subject"],
            "gold": choice["gold"],
            "bangla_option": choice["bangla_parsed_option"],
            "bangla_correct": truthy(choice["bangla_correct"]),
            "banglish_option": choice["banglish_clean_parsed_option"],
            "banglish_correct": truthy(choice["banglish_clean_correct"]),
            "english_option": choice["english_parsed_option"],
            "english_correct": truthy(choice["english_correct"]),
            "banglish_D": banglish_d,
            "banglish_wrong_D": wrong_d,
            "gold_not_D": gold_not_d,
            "D_not_longest": d_not_longest,
            "D_no_semantic_cue": d_no_semantic_cue,
            "D_not_highest_coverage": d_not_highest_coverage,
            "all_options_same_coverage": all_options_same_coverage,
            "D_char_len": pos["d_char_len"],
            "D_token_len": pos["d_token_len"],
            "D_coverage": cov["d_coverage"],
            "longest_options": pos["longest_options"],
            "highest_coverage_options": cov["highest_coverage_options"],
            "D_text": sem["D_text"],
            "residual_primary": residual_primary,
            "residual_tied_coverage": residual_tied_coverage,
            "residual_not_highest_coverage": residual_not_highest_coverage,
        }
        for baseline in BASELINES:
            switch_key = (choice["model"], baseline, choice["id"])
            if switch_key not in switch:
                raise SystemExit(f"Missing switch features for {switch_key}")
            sw = switch[switch_key]
            row[f"{baseline}_baseline_correct_non_D"] = truthy(
                sw["baseline_correct_non_d"]
            )
            row[f"{baseline}_correct_non_D_to_wrong_D"] = truthy(
                sw["baseline_correct_non_d_to_d_wrong"]
            )
            row[f"{baseline}_baseline_option"] = sw["baseline_option"]
        rows.append(row)

    expected = len(MODELS) * 144
    if len(rows) != expected:
        raise SystemExit(f"Expected {expected} joined choice rows, got {len(rows)}")
    return rows


def choice_scopes() -> list[tuple[str, str, Callable[[dict[str, Any]], bool]]]:
    return [
        ("non_gold_D", "Gold is not D", lambda row: truthy(row["gold_not_D"])),
        (
            "non_gold_D_D_not_longest",
            "Gold is not D and D is not longest",
            lambda row: truthy(row["gold_not_D"]) and truthy(row["D_not_longest"]),
        ),
        (
            "non_gold_D_D_no_semantic_cue",
            "Gold is not D and D has no simple semantic cue",
            lambda row: truthy(row["gold_not_D"]) and truthy(row["D_no_semantic_cue"]),
        ),
        (
            "residual_primary",
            "Gold not D, D not longest, D has no simple cue",
            lambda row: truthy(row["residual_primary"]),
        ),
        (
            "residual_tied_coverage",
            "Primary residual and all options have tied exact coverage",
            lambda row: truthy(row["residual_tied_coverage"]),
        ),
        (
            "residual_D_not_highest_coverage",
            "Primary residual and D is not highest exact coverage",
            lambda row: truthy(row["residual_not_highest_coverage"]),
        ),
    ]


def switch_scopes() -> list[tuple[str, str, Callable[[dict[str, Any]], bool]]]:
    return [
        (
            "baseline_correct_non_D",
            "Baseline is correct non-D",
            lambda row: True,
        ),
        (
            "baseline_correct_non_D_residual_primary",
            "Baseline correct non-D in primary residual",
            lambda row: truthy(row["residual_primary"]),
        ),
        (
            "baseline_correct_non_D_residual_tied_coverage",
            "Baseline correct non-D in tied-coverage residual",
            lambda row: truthy(row["residual_tied_coverage"]),
        ),
    ]


def summarize(item_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for model in MODELS:
        model_rows = [row for row in item_rows if row["model"] == model]
        for scope, label, predicate in choice_scopes():
            scoped = [row for row in model_rows if predicate(row)]
            d_count = sum(truthy(row["banglish_D"]) for row in scoped)
            wrong_d = sum(truthy(row["banglish_wrong_D"]) for row in scoped)
            subjects = sorted({row["subject"] for row in scoped})
            summary.append(
                {
                    "section": "choice_scope",
                    "model": model,
                    "baseline_variant": "",
                    "baseline_label": "",
                    "scope": scope,
                    "scope_label": label,
                    "n": len(scoped),
                    "banglish_D": d_count,
                    "banglish_D_rate": rate(d_count, len(scoped)),
                    "banglish_wrong_D": wrong_d,
                    "banglish_wrong_D_rate": rate(wrong_d, len(scoped)),
                    "correct_non_D_to_wrong_D": "",
                    "correct_non_D_to_wrong_D_rate": "",
                    "subject_count": len(subjects),
                    "subjects": ";".join(subjects),
                }
            )
        for baseline in BASELINES:
            baseline_ok_key = f"{baseline}_baseline_correct_non_D"
            wrong_key = f"{baseline}_correct_non_D_to_wrong_D"
            correct_non_d = [row for row in model_rows if truthy(row[baseline_ok_key])]
            for scope, label, predicate in switch_scopes():
                scoped = [row for row in correct_non_d if predicate(row)]
                wrong = sum(truthy(row[wrong_key]) for row in scoped)
                subjects = sorted({row["subject"] for row in scoped})
                summary.append(
                    {
                        "section": "switch_scope",
                        "model": model,
                        "baseline_variant": baseline,
                        "baseline_label": BASELINE_LABELS[baseline],
                        "scope": scope,
                        "scope_label": label,
                        "n": len(scoped),
                        "banglish_D": "",
                        "banglish_D_rate": "",
                        "banglish_wrong_D": "",
                        "banglish_wrong_D_rate": "",
                        "correct_non_D_to_wrong_D": wrong,
                        "correct_non_D_to_wrong_D_rate": rate(wrong, len(scoped)),
                        "subject_count": len(subjects),
                        "subjects": ";".join(subjects),
                    }
                )
    return summary


def row_for(
    summary_rows: list[dict[str, Any]],
    section: str,
    model: str,
    scope: str,
    baseline: str = "",
) -> dict[str, Any]:
    return next(
        row
        for row in summary_rows
        if row["section"] == section
        and row["model"] == model
        and row["scope"] == scope
        and row["baseline_variant"] == baseline
    )


def count_text(row: dict[str, Any], numerator_key: str) -> str:
    return f"{row[numerator_key]}/{row['n']}"


def write_report(
    path: Path,
    item_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    items_output: Path,
    summary_output: Path,
) -> None:
    q3_primary = row_for(summary_rows, "choice_scope", "Qwen3-4B", "residual_primary")
    q25_3b_primary = row_for(
        summary_rows, "choice_scope", "Qwen2.5-3B", "residual_primary"
    )
    q25_7b_primary = row_for(
        summary_rows, "choice_scope", "Qwen2.5-7B 8-bit", "residual_primary"
    )
    q3_tied = row_for(summary_rows, "choice_scope", "Qwen3-4B", "residual_tied_coverage")
    q25_3b_tied = row_for(
        summary_rows, "choice_scope", "Qwen2.5-3B", "residual_tied_coverage"
    )
    q25_7b_tied = row_for(
        summary_rows, "choice_scope", "Qwen2.5-7B 8-bit", "residual_tied_coverage"
    )
    q3_not_highest = row_for(
        summary_rows, "choice_scope", "Qwen3-4B", "residual_D_not_highest_coverage"
    )
    q3_bangla_switch = row_for(
        summary_rows,
        "switch_scope",
        "Qwen3-4B",
        "baseline_correct_non_D_residual_primary",
        "bangla",
    )
    q3_english_switch = row_for(
        summary_rows,
        "switch_scope",
        "Qwen3-4B",
        "baseline_correct_non_D_residual_primary",
        "english",
    )
    q25_3b_bangla_switch = row_for(
        summary_rows,
        "switch_scope",
        "Qwen2.5-3B",
        "baseline_correct_non_D_residual_primary",
        "bangla",
    )
    q25_7b_bangla_switch = row_for(
        summary_rows,
        "switch_scope",
        "Qwen2.5-7B 8-bit",
        "baseline_correct_non_D_residual_primary",
        "bangla",
    )
    q25_3b_english_switch = row_for(
        summary_rows,
        "switch_scope",
        "Qwen2.5-3B",
        "baseline_correct_non_D_residual_primary",
        "english",
    )
    q25_7b_english_switch = row_for(
        summary_rows,
        "switch_scope",
        "Qwen2.5-7B 8-bit",
        "baseline_correct_non_D_residual_primary",
        "english",
    )

    lines = [
        "# Frozen-v5 BEnQA Multi-Confound Residual Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This audit joins the frozen-v5 BEnQA choice-bias rows with option",
        "position/length, exact BanglaTLit option coverage, simple semantic-cue",
        "flags, and alternate-script option-switch rows. It asks whether the Qwen3",
        "reviewed-Banglish D-attractor remains after several local explanations",
        "are removed at the same time.",
        "",
        "Machine-readable outputs:",
        "",
        f"- Item rows: `{repo_path(items_output)}`",
        f"- Summary rows: `{repo_path(summary_output)}`",
        "",
        "## Key Result",
        "",
        "- Primary residual scope: gold is not D, D is not the longest option, and",
        "  D has no simple composite/numeric/all-none-both cue.",
        f"- In that 24-item scope, Qwen3 predicts wrong D on "
        f"{count_text(q3_primary, 'banglish_wrong_D')} rows "
        f"({percent(int(q3_primary['banglish_wrong_D']), int(q3_primary['n']))}).",
        f"- The two Qwen2.5 rows are much lower: "
        f"{count_text(q25_3b_primary, 'banglish_wrong_D')} and "
        f"{count_text(q25_7b_primary, 'banglish_wrong_D')}.",
        f"- In the stricter tied-coverage residual scope, Qwen3 is wrong-D on "
        f"{count_text(q3_tied, 'banglish_wrong_D')} rows, while Qwen2.5 rows are "
        f"{count_text(q25_3b_tied, 'banglish_wrong_D')} and "
        f"{count_text(q25_7b_tied, 'banglish_wrong_D')}.",
        f"- The D-not-highest-coverage residual is tiny at n={q3_not_highest['n']}; "
        f"Qwen3 is wrong-D on {q3_not_highest['banglish_wrong_D']}/{q3_not_highest['n']},",
        "  so use it only as a stress slice, not as a standalone estimate.",
        "",
        "## Alternate-Script Support",
        "",
        "Restricting to rows where the same model's Bangla or English answer is",
        "already correct and non-D preserves the residual failure mode:",
        "",
        "| Model | Bangla correct non-D -> wrong D | English correct non-D -> wrong D |",
        "| --- | ---: | ---: |",
        (
            f"| Qwen2.5-3B | "
            f"{count_text(q25_3b_bangla_switch, 'correct_non_D_to_wrong_D')} | "
            f"{count_text(q25_3b_english_switch, 'correct_non_D_to_wrong_D')} |"
        ),
        (
            f"| Qwen2.5-7B 8-bit | "
            f"{count_text(q25_7b_bangla_switch, 'correct_non_D_to_wrong_D')} | "
            f"{count_text(q25_7b_english_switch, 'correct_non_D_to_wrong_D')} |"
        ),
        (
            f"| Qwen3-4B | "
            f"{count_text(q3_bangla_switch, 'correct_non_D_to_wrong_D')} | "
            f"{count_text(q3_english_switch, 'correct_non_D_to_wrong_D')} |"
        ),
        "",
        "## Interpretation",
        "",
        "The Qwen3 D-attractor is not just a single local confound such as gold-label",
        "imbalance, a long D option, a simple semantic cue, or exact option-coverage",
        "ties considered separately. The residual scope is smaller than the full",
        "BEnQA set, so it should be used as a targeted failure-mode audit rather than",
        "a replacement for the main all-200 paired result.",
        "",
        "## Summary Table",
        "",
        "| Section | Scope | Model | Baseline | n | D/wrong-D or switch count | Subjects |",
        "| --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        if row["section"] == "choice_scope":
            count = f"{row['banglish_wrong_D']}/{row['n']}"
            baseline = ""
        else:
            count = f"{row['correct_non_D_to_wrong_D']}/{row['n']}"
            baseline = row["baseline_label"]
        lines.append(
            f"| {row['section']} | {row['scope']} | {row['model']} | {baseline} | "
            f"{row['n']} | {count} | {row['subject_count']} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--choice-items", type=Path, default=DEFAULT_CHOICE_ITEMS)
    parser.add_argument("--position-items", type=Path, default=DEFAULT_POSITION_ITEMS)
    parser.add_argument("--coverage-items", type=Path, default=DEFAULT_COVERAGE_ITEMS)
    parser.add_argument("--semantic-items", type=Path, default=DEFAULT_SEMANTIC_ITEMS)
    parser.add_argument("--switch-items", type=Path, default=DEFAULT_SWITCH_ITEMS)
    parser.add_argument("--items-output", type=Path, default=DEFAULT_ITEMS_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item_rows = build_item_rows(
        args.choice_items,
        args.position_items,
        args.coverage_items,
        args.semantic_items,
        args.switch_items,
    )
    summary_rows = summarize(item_rows)
    write_csv(args.items_output, item_rows)
    write_csv(args.summary_output, summary_rows)
    write_report(args.report_output, item_rows, summary_rows, args.items_output, args.summary_output)

    q3_primary = row_for(summary_rows, "choice_scope", "Qwen3-4B", "residual_primary")
    q3_tied = row_for(summary_rows, "choice_scope", "Qwen3-4B", "residual_tied_coverage")
    print(
        "items={items} summary_rows={summary} "
        "qwen3_primary_wrongD={primary}/{primary_n} "
        "qwen3_tied_wrongD={tied}/{tied_n} report={report}".format(
            items=len(item_rows),
            summary=len(summary_rows),
            primary=q3_primary["banglish_wrong_D"],
            primary_n=q3_primary["n"],
            tied=q3_tied["banglish_wrong_D"],
            tied_n=q3_tied["n"],
            report=args.report_output,
        )
    )


if __name__ == "__main__":
    main()
