#!/usr/bin/env python3
"""Build thesis-ready tables from current authoritative result CSVs."""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "results/tables"

MODEL_LABELS = {
    "Qwen/Qwen2.5-0.5B-Instruct": "Qwen2.5-0.5B",
    "Qwen/Qwen2.5-1.5B-Instruct": "Qwen2.5-1.5B",
    "Qwen/Qwen2.5-3B-Instruct": "Qwen2.5-3B",
    "Qwen/Qwen2.5-7B-Instruct": "Qwen2.5-7B 8-bit",
    "Qwen/Qwen3-1.7B": "Qwen3-1.7B no-thinking",
    "Qwen/Qwen3-4B-Instruct-2507": "Qwen3-4B",
    "microsoft/Phi-3.5-mini-instruct": "Phi-3.5-mini",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def truthy(value: str | bool | None) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows for {path}")
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


def pct(value: str | float) -> str:
    return f"{float(value) * 100:.1f}"


def points(value: str | float) -> str:
    value = float(value)
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def ci(low: str | float, high: str | float) -> str:
    return f"[{points(float(low) * 100)}, {points(float(high) * 100)}]"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")) for key in headers) + " |")
    return "\n".join(lines)


def script_gap_tables(out_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = read_csv(ROOT / "results/analysis/model_family_scaling_synthesis_validation200.csv")
    table: list[dict[str, Any]] = []
    for row in rows:
        table.append(
            {
                "Model": MODEL_LABELS.get(row["model"], row["model"]),
                "Family": row["model_family"],
                "Slice": row["slice"],
                "Bangla": row["bangla"],
                "Banglish": row["banglish_clean"],
                "English": row["english"],
                "Banglish-Bangla": f"{points(row['banglish_minus_bangla_points'])} pts, CI {row['banglish_minus_bangla_ci95']}",
                "Banglish-English": f"{points(row['banglish_minus_english_points'])} pts, CI {row['banglish_minus_english_ci95']}",
                "Interpretation": row["interpretation"],
            }
        )
    main_models = {"Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B"}
    main_table = [row for row in table if row["Model"] in main_models]
    write_csv(out_dir / "main_script_gap_validation200.csv", main_table)
    write_csv(out_dir / "model_family_scaling_validation200.csv", table)
    return main_table, table


def selfnorm_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "Qwen2.5-3B",
            "validation_200_v3",
            ROOT / "results/analysis/qwen25_validation200_v3_selfnorm_bootstrap.csv",
        ),
        (
            "Qwen2.5-7B 8-bit",
            "validation_200_v4",
            ROOT / "results/analysis/qwen25_7b_8bit_validation200_v4_full200_selfnorm_bootstrap.csv",
        ),
        (
            "Qwen3-4B",
            "validation_200_v3",
            ROOT / "results/analysis/qwen3_validation200_v3_selfnorm_bootstrap.csv",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for model, slice_name, path in specs:
        row = read_csv(path)[0]
        rows.append(
            {
                "Model": model,
                "Slice": slice_name,
                "Baseline": f"{row['left_correct']}/{row['n']}",
                "Self-normalized": f"{row['right_correct']}/{row['n']}",
                "Delta": f"{points(float(row['delta_right_minus_left']) * 100)} pts",
                "95% CI": ci(row["ci95_low"], row["ci95_high"]),
                "Direction p": row["bootstrap_p_opposite_direction"],
            }
        )
    write_csv(out_dir / "selfnorm_validation200.csv", rows)
    return rows


def routing_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "Qwen2.5-3B",
            ROOT / "results/analysis/qwen25_validation200_v4_devtest_selfnorm_answer_signal_bootstrap.csv",
            ROOT / "results/analysis/qwen25_validation200_v4_devtest_selfnorm_answer_signal_routed_breakdown.csv",
        ),
        (
            "Qwen3-4B",
            ROOT / "results/analysis/qwen3_validation200_v4_devtest_selfnorm_answer_signal_bootstrap.csv",
            ROOT / "results/analysis/qwen3_validation200_v4_devtest_selfnorm_answer_signal_routed_breakdown.csv",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for model, boot_path, breakdown_path in specs:
        boot = {
            row["comparison"]: row
            for row in read_csv(boot_path)
            if row["split"] == "test"
        }
        breakdown = {
            row["dataset"]: row
            for row in read_csv(breakdown_path)
            if row["group"] == "by_split_dataset" and row["split"] == "test"
        }
        baseline = boot["baseline_vs_routed"]
        selfnorm = boot["selfnorm_vs_routed"]
        rows.append(
            {
                "Model": model,
                "Rule": "selfnorm if parsed answer non-empty",
                "Baseline": f"{baseline['left_correct']}/{baseline['n']}",
                "Always selfnorm": f"{selfnorm['left_correct']}/{selfnorm['n']}",
                "Routed": f"{baseline['right_correct']}/{baseline['n']}",
                "Routed-Baseline": f"{points(float(baseline['delta_right_minus_left']) * 100)} pts, CI {ci(baseline['ci95_low'], baseline['ci95_high'])}",
                "Routed-Selfnorm": f"{points(float(selfnorm['delta_right_minus_left']) * 100)} pts, CI {ci(selfnorm['ci95_low'], selfnorm['ci95_high'])}",
                "BEnQA routed gain": f"+{breakdown['benqa']['routed_minus_baseline']}",
                "BanglaMATH routed gain": f"+{breakdown['banglamath']['routed_minus_baseline']}",
            }
        )
    write_csv(out_dir / "answer_signal_routing_test150.csv", rows)
    return rows


def real_banglish_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv")
    label_map = {
        "banglatlit:BanglaTLiT_test": "BanglaTLit test",
        "banglatlit:BanglaTLiT_val": "BanglaTLit val",
        "validation:banglish_clean:content": "Validation-200 v5 content Banglish",
        "validation:banglish_clean:raw": "Validation-200 v5 raw Banglish",
    }
    table: list[dict[str, Any]] = []
    for row in rows:
        table.append(
            {
                "Source": label_map.get(row["source"], row["source"]),
                "Rows": row["n"],
                "Mean chars": f"{float(row['mean_chars']):.1f}",
                "Mean words": f"{float(row['mean_words']):.1f}",
                "Mean Latin ratio": f"{float(row['mean_latin_ratio']):.3f}",
                "Digit row share": f"{float(row['digit_row_share']):.3f}",
                "Mixed-script share": f"{float(row['mixed_latin_bengali_share']):.3f}",
            }
        )
    write_csv(out_dir / "real_banglish_distribution.csv", table)
    return table


def auto_suggested_sensitivity_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(
        ROOT / "results/analysis/validation200_v4_auto_suggested_sensitivity_summary.csv"
    )
    table: list[dict[str, Any]] = []
    for row in rows:
        table.append(
            {
                "Model": row["model"],
                "v3 Banglish": f"{row['v3_correct']}/{row['n']}",
                "v4 Banglish": f"{row['v4_correct']}/{row['n']}",
                "Auto-suggested": f"{row['auto_correct']}/{row['n']}",
                "Auto-v4": f"{points(float(row['auto_minus_v4_delta']) * 100)} pts, CI {ci(row['auto_minus_v4_ci95_low'], row['auto_minus_v4_ci95_high'])}",
                "Gains": row["auto_vs_v4_gains"],
                "Losses": row["auto_vs_v4_losses"],
            }
        )
    write_csv(out_dir / "auto_suggested_banglish_sensitivity.csv", table)
    return table


def v5_reviewed_sensitivity_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "Qwen2.5-3B",
            ROOT / "results/analysis/qwen25_validation200_v5_vs_v4_banglish_summary.csv",
        ),
        (
            "Qwen3-4B",
            ROOT / "results/analysis/qwen3_validation200_v5_vs_v4_banglish_summary.csv",
        ),
        (
            "Qwen2.5-7B 8-bit",
            ROOT / "results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish_summary.csv",
        ),
    ]
    table: list[dict[str, Any]] = []
    for model, path in specs:
        overall = next(row for row in read_csv(path) if row["group"] == "overall")
        test = next(row for row in read_csv(path) if row["group"] == "split=test")
        table.append(
            {
                "Model": model,
                "v4 Banglish": f"{overall['baseline_correct']}/{overall['n']}",
                "v5 reviewed": f"{overall['candidate_correct']}/{overall['n']}",
                "v5-v4": f"{points(float(overall['delta_candidate_minus_baseline']) * 100)} pts, CI {ci(overall['ci95_low'], overall['ci95_high'])}",
                "Test split v5-v4": f"{points(float(test['delta_candidate_minus_baseline']) * 100)} pts, CI {ci(test['ci95_low'], test['ci95_high'])}",
                "Gains": overall["gains"],
                "Losses": overall["losses"],
                "Decision": "Use v5 for final Banglish reruns; cleanup does not erase the gap.",
            }
        )
    write_csv(out_dir / "v5_reviewed_banglish_sensitivity.csv", table)
    return table


def v5_bad_row_policy_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/v5_bad_row_policy_sensitivity.csv")
    table: list[dict[str, Any]] = []
    for row in rows:
        if row["policy"] != "strict197":
            continue
        table.append(
            {
                "Model": row["model"],
                "Comparison": row["comparison"],
                "Policy": row["policy"],
                "Left": f"{row['left_correct']}/{row['n']}",
                "Right": f"{row['right_correct']}/{row['n']}",
                "Delta": f"{points(float(row['delta_right_minus_left']) * 100)} pts, CI {ci(row['ci95_low'], row['ci95_high'])}",
                "Gains": row["gains"],
                "Losses": row["losses"],
            }
        )
    write_csv(out_dir / "v5_bad_row_policy_sensitivity.csv", table)
    return table


def frozen_v5_main_script_gap_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/v5_bad_row_policy_sensitivity.csv")
    by_key = {
        (row["model"], row["comparison"]): row
        for row in rows
        if row["policy"] == "all200"
    }
    interpretations = {
        "Qwen2.5-3B": "Point deficit remains; all-200 CI reaches zero. Historical v3 and strict-197 checks remain negative.",
        "Qwen2.5-7B 8-bit": "Reviewed gap remains reliable at the stronger Qwen2.5 scaling point.",
        "Qwen3-4B": "Strongest reviewed open-model gap.",
    }
    table: list[dict[str, Any]] = []
    for model in ["Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B"]:
        vs_bangla = by_key[(model, "v5_banglish_minus_bangla")]
        vs_english = by_key[(model, "v5_banglish_minus_english")]
        table.append(
            {
                "Model": model,
                "Slice": "validation_200_v5",
                "Bangla": f"{vs_bangla['left_correct']}/{vs_bangla['n']}",
                "Reviewed Banglish": f"{vs_bangla['right_correct']}/{vs_bangla['n']}",
                "English": f"{vs_english['left_correct']}/{vs_english['n']}",
                "Banglish-Bangla": f"{points(float(vs_bangla['delta_right_minus_left']) * 100)} pts, CI {ci(vs_bangla['ci95_low'], vs_bangla['ci95_high'])}",
                "Banglish-English": f"{points(float(vs_english['delta_right_minus_left']) * 100)} pts, CI {ci(vs_english['ci95_low'], vs_english['ci95_high'])}",
                "Interpretation": interpretations[model],
            }
        )
    write_csv(out_dir / "main_script_gap_validation200_v5.csv", table)
    return table


def cross_script_answer_agreement_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/validation200_v5_cross_script_answer_agreement_routes.csv")
    by_key = {
        (row["model"], row["dataset"], row["route"]): row
        for row in rows
        if row["dataset"] == "all"
    }
    table: list[dict[str, Any]] = []
    for model in [
        "Qwen/Qwen2.5-3B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen3-4B-Instruct-2507",
    ]:
        route = by_key[(model, "all", "bangla_english_agreement_route")]
        oracle = by_key[(model, "all", "oracle")]
        table.append(
            {
                "Model": MODEL_LABELS.get(model, model),
                "Banglish": f"{route['banglish_correct']}/{route['n']}",
                "Agreement route": f"{route['route_correct']}/{route['n']}",
                "Route-Banglish": f"{points(float(route['delta_route_minus_banglish']) * 100)} pts, CI {ci(route['ci95_low'], route['ci95_high'])}",
                "Oracle": f"{oracle['route_correct']}/{oracle['n']}",
                "Oracle-Banglish": f"{points(float(oracle['delta_route_minus_banglish']) * 100)} pts, CI {ci(oracle['ci95_low'], oracle['ci95_high'])}",
            }
        )
    write_csv(out_dir / "cross_script_answer_agreement.csv", table)
    return table


def generated_view_preservation_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "Qwen2.5-7B 8-bit",
            ROOT / "results/analysis/qwen25_7b_8bit_validation200_v4_selfnorm_preservation_v2_summary.csv",
        ),
        (
            "Qwen3-4B",
            ROOT / "results/analysis/qwen3_validation200_v3_selfnorm_preservation_v2_summary.csv",
        ),
    ]
    table: list[dict[str, Any]] = []
    for model, path in specs:
        for row in read_csv(path):
            table.append(
                {
                    "Model": model,
                    "Dataset": row["dataset"],
                    "n": row["n"],
                    "Options changed": row["options_not_preserved"],
                    "Digit sequence changed": row["digit_sequence_not_preserved"],
                    "Formulas changed": row["formulas_not_preserved"],
                    "Line count changed": row["line_count_not_preserved"],
                    "Extra answer markers": row["extra_answer_marker_count"],
                    "Gate implication": "Reject generated view on option/digit/formula/answer-marker failures.",
                }
            )
    write_csv(out_dir / "generated_view_preservation_v2.csv", table)
    return table


def diagnostic_pilot_table(out_dir: Path) -> list[dict[str, Any]]:
    table = [
        {
            "Model": "Qwen3-8B",
            "Mode": "8-bit",
            "Bangla": "blocked",
            "Banglish": "blocked",
            "English": "blocked",
            "Decision": "Do not retry on P100; bitsandbytes backend blocked.",
        },
        {
            "Model": "Mistral-7B-Instruct-v0.3",
            "Mode": "8-bit pilot20",
            "Bangla": "3/20",
            "Banglish": "4/20",
            "English": "4/20",
            "Decision": "Diagnostic only; weak and slow.",
        },
        {
            "Model": "Indic-Gemma-2B Navarasa",
            "Mode": "fp16 pilot20, Alpaca wrapper",
            "Bangla": "4/20",
            "Banglish": "3/20",
            "English": "5/20",
            "Decision": "Diagnostic only; parseable but around chance.",
        },
    ]
    write_csv(out_dir / "diagnostic_model_pilots.csv", table)
    return table


def deterministic_generated_view_smoke_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "phonetic-bangla 1.0.0",
            "raw",
            ROOT
            / "results/analysis/phonetic_bangla_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "bnbphoneticparser 0.1.5",
            "raw",
            ROOT
            / "results/analysis/bnbphoneticparser_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "phonetic-bangla 1.0.0",
            "legacy protected v1; historical answer-audit input",
            ROOT
            / "results/analysis/phonetic_bangla_protected_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "bnbphoneticparser 0.1.5",
            "legacy protected v1; historical answer-audit input",
            ROOT
            / "results/analysis/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "phonetic-bangla 1.0.0",
            "expanded protected v2",
            ROOT
            / "results/analysis/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "bnbphoneticparser 0.1.5",
            "expanded protected v2",
            ROOT
            / "results/analysis/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "phonetic-bangla 1.0.0",
            "reviewed-v5 expanded protected v2",
            ROOT
            / "results/analysis/phonetic_bangla_protected_v2_v5_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "bnbphoneticparser 0.1.5",
            "reviewed-v5 expanded protected v2",
            ROOT
            / "results/analysis/bnbphoneticparser_protected_v2_v5_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "phonetic-bangla 1.0.0",
            "reviewed-v5 formulaish protected v3",
            ROOT
            / "results/analysis/phonetic_bangla_protected_v3_v5_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
        (
            "bnbphoneticparser 0.1.5",
            "reviewed-v5 formulaish protected v3",
            ROOT
            / "results/analysis/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn_audit_summary.csv",
        ),
    ]
    table: list[dict[str, Any]] = []
    for generator, protection, path in specs:
        row = read_csv(path)[0]
        hard_fail = int(row["hard_fail"])
        n = int(row["n"])
        decision = "Reject for routing" if hard_fail else "Eligible for answer audit"
        if "formulaish protected v3" in protection:
            decision = "Gate-passing; answer audit complete"
        table.append(
            {
                "Generator": generator,
                "Protection": protection,
                "Dataset": row["dataset"],
                "Target view": row["target_view"],
                "n": n,
                "Hard fails": hard_fail,
                "Option failures": row["options_not_preserved"],
                "Digit failures": row["digit_sequence_not_preserved"],
                "Formula failures": row["formulas_not_preserved"],
                "Extra answer markers": row["extra_answer_marker"],
                "Latin fragment warnings": row.get("unexpected_latin_fragment", "0"),
                "Decision": decision,
            }
        )
    write_csv(out_dir / "deterministic_generated_view_smokes.csv", table)
    return table


def generated_bn_candidate_preservation_table(
    out_dir: Path, deterministic_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    fms_row = read_csv(
        ROOT
        / "results/analysis/fms_byte_protected_dev50_benqa_mcq_generated_bn_audit_summary.csv"
    )[0]
    hard_fail = int(fms_row["hard_fail"])
    table = [
        *deterministic_rows,
        {
            "Generator": "fms-byte/banglish_to_bangla MBART",
            "Protection": "expanded protected line segments",
            "Dataset": fms_row["dataset"],
            "Target view": fms_row["target_view"],
            "n": fms_row["n"],
            "Hard fails": fms_row["hard_fail"],
            "Option failures": fms_row["options_not_preserved"],
            "Digit failures": fms_row["digit_sequence_not_preserved"],
            "Formula failures": fms_row["formulas_not_preserved"],
            "Extra answer markers": fms_row["extra_answer_marker"],
            "Latin fragment warnings": fms_row.get("unexpected_latin_fragment", "0"),
            "Decision": (
                "Reject for routing"
                if hard_fail
                else "Pass formal gates; inspect lexical quality"
            ),
        },
    ]
    write_csv(out_dir / "generated_bn_candidate_preservation.csv", table)
    return table


def generated_bn_reference_similarity_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(
        ROOT / "results/analysis/generated_bn_reference_similarity_summary.csv"
    )
    table: list[dict[str, Any]] = []
    for rank, row in enumerate(rows, start=1):
        table.append(
            {
                "Rank": rank,
                "Generator": row["generator"],
                "n": row["n"],
                "Mean CER": row["mean_cer"],
                "Median CER": row["median_cer"],
                "Mean sequence similarity": row["mean_sequence_similarity"],
                "Mean Bengali ratio": row["mean_bengali_ratio"],
                "Exact matches": row["exact_match"],
                "Decision": (
                    "Closest native-reference match among audited candidates"
                    if rank == 1
                    else "Privileged dev-only lexical diagnostic"
                ),
            }
        )
    write_csv(out_dir / "generated_bn_reference_similarity_dev50.csv", table)
    return table


def gate_stats(compare_path: Path, variant: str) -> dict[str, Any]:
    if not compare_path.exists():
        return {
            "gate_hard_fails": "",
            "eligible_n": "",
            "eligible_baseline_correct": "",
            "eligible_generated_correct": "",
        }
    rows = [row for row in read_csv(compare_path) if row.get("variant") == variant]
    if not rows:
        return {
            "gate_hard_fails": "",
            "eligible_n": "",
            "eligible_baseline_correct": "",
            "eligible_generated_correct": "",
        }
    eligible = [row for row in rows if not truthy(row.get("gate_hard_fail"))]
    return {
        "gate_hard_fails": len(rows) - len(eligible),
        "eligible_n": len(eligible),
        "eligible_baseline_correct": sum(
            1 for row in eligible if truthy(row.get("baseline_correct"))
        ),
        "eligible_generated_correct": sum(
            1 for row in eligible if truthy(row.get("generated_correct"))
        ),
    }


def generated_bn_answer_audit_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "Qwen3-4B",
            ROOT / "results/analysis/qwen3_4b_generated_bn_answer_audit_dev50_summary.csv",
        ),
        (
            "Qwen2.5-3B",
            ROOT / "results/analysis/qwen25_3b_generated_bn_answer_audit_dev50_summary.csv",
        ),
    ]
    bootstrap_paths = {
        ("Qwen3-4B", "generated_bn_phonetic_protected"): ROOT
        / "results/analysis/qwen3_4b_generated_bn_answer_audit_phonetic_vs_banglish_bootstrap.csv",
        ("Qwen3-4B", "generated_bn_bnb_protected"): ROOT
        / "results/analysis/qwen3_4b_generated_bn_answer_audit_bnb_vs_banglish_bootstrap.csv",
        ("Qwen2.5-3B", "generated_bn_phonetic_protected"): ROOT
        / "results/analysis/qwen25_3b_generated_bn_answer_audit_phonetic_vs_banglish_bootstrap.csv",
        ("Qwen2.5-3B", "generated_bn_bnb_protected"): ROOT
        / "results/analysis/qwen25_3b_generated_bn_answer_audit_bnb_vs_banglish_bootstrap.csv",
        ("Qwen3-4B", "generated_bn_phonetic_protected_v3"): ROOT
        / "results/analysis/qwen3_4b_generated_bn_v5_pv3_phonetic_vs_banglish_bootstrap.csv",
        ("Qwen3-4B", "generated_bn_bnb_protected_v3"): ROOT
        / "results/analysis/qwen3_4b_generated_bn_v5_pv3_bnb_vs_banglish_bootstrap.csv",
        ("Qwen2.5-3B", "generated_bn_phonetic_protected_v3"): ROOT
        / "results/analysis/qwen25_3b_generated_bn_v5_pv3_phonetic_vs_banglish_bootstrap.csv",
        ("Qwen2.5-3B", "generated_bn_bnb_protected_v3"): ROOT
        / "results/analysis/qwen25_3b_generated_bn_v5_pv3_bnb_vs_banglish_bootstrap.csv",
    }
    label_map = {
        "banglish_clean": "Banglish baseline",
        "generated_bn_phonetic_protected": "Historical protected-v1 phonetic-bangla generated-BN",
        "generated_bn_bnb_protected": "Historical protected-v1 bnbphoneticparser generated-BN",
        "generated_bn_phonetic_protected_v2": "Reviewed-v5 protected-v2 phonetic-bangla generated-BN",
        "generated_bn_bnb_protected_v2": "Reviewed-v5 protected-v2 bnbphoneticparser generated-BN",
        "generated_bn_phonetic_protected_v3": "Reviewed-v5 protected-v3 phonetic-bangla generated-BN",
        "generated_bn_bnb_protected_v3": "Reviewed-v5 protected-v3 bnbphoneticparser generated-BN",
    }
    table: list[dict[str, Any]] = []
    for model, path in specs:
        rows = read_csv(path)
        baseline_correct = next(
            int(row["correct"]) for row in rows if row["variant"] == "banglish_clean"
        )
        best_generated = max(
            (row for row in rows if row["variant"] != "banglish_clean"),
            key=lambda row: int(row["correct"]),
        )
        for row in rows:
            correct = int(row["correct"])
            is_best = row["variant"] == best_generated["variant"]
            boot_path = bootstrap_paths.get((model, row["variant"]))
            boot = read_csv(boot_path)[0] if boot_path and boot_path.exists() else None
            table.append(
                {
                    "Model": model,
                    "Variant": label_map.get(row["variant"], row["variant"]),
                    "n": row["n"],
                    "Correct": correct,
                    "Accuracy": f"{float(row['accuracy']):.3f}",
                    "Delta vs Banglish": correct - baseline_correct,
                    "Delta 95% CI (pts)": (
                        ci(boot["ci95_low"], boot["ci95_high"]) if boot else ""
                    ),
                    "Direction p": boot["bootstrap_p_opposite_direction"] if boot else "",
                    "Parsed empty": row["parsed_empty"],
                    "Gate hard fails": "",
                    "Eligible n": "",
                    "Eligible baseline": "",
                    "Eligible generated": "",
                    "Decision": (
                        "Model-specific dev lead"
                        if is_best and correct > baseline_correct
                        else "Drop for this model"
                        if row["variant"] != "banglish_clean" and correct <= baseline_correct
                        else "Baseline"
                    ),
                }
            )

    reviewed_specs = [
        (
            "Qwen3-4B",
            ROOT / "results/analysis/qwen3_4b_generated_bn_v5_pv2_dev50_summary.csv",
            ROOT / "results/analysis/qwen3_4b_generated_bn_v5_pv2_dev50_item_compare.csv",
        ),
        (
            "Qwen2.5-3B",
            ROOT / "results/analysis/qwen25_3b_generated_bn_v5_pv2_dev50_summary.csv",
            ROOT / "results/analysis/qwen25_3b_generated_bn_v5_pv2_dev50_item_compare.csv",
        ),
        (
            "Qwen3-4B",
            ROOT / "results/analysis/qwen3_4b_generated_bn_v5_pv3_dev50_summary.csv",
            ROOT / "results/analysis/qwen3_4b_generated_bn_v5_pv3_dev50_item_compare.csv",
        ),
        (
            "Qwen2.5-3B",
            ROOT / "results/analysis/qwen25_3b_generated_bn_v5_pv3_dev50_summary.csv",
            ROOT / "results/analysis/qwen25_3b_generated_bn_v5_pv3_dev50_item_compare.csv",
        ),
    ]
    for model, summary_path, compare_path in reviewed_specs:
        if not summary_path.exists():
            continue
        rows = read_csv(summary_path)
        baseline_correct = next(
            int(row["correct"]) for row in rows if row["variant"] == "banglish_clean"
        )
        best_generated = max(
            (row for row in rows if row["variant"] != "banglish_clean"),
            key=lambda row: int(row["correct"]),
        )
        for row in rows:
            correct = int(row["correct"])
            boot_path = bootstrap_paths.get((model, row["variant"]))
            boot = read_csv(boot_path)[0] if boot_path and boot_path.exists() else None
            stats = (
                gate_stats(compare_path, row["variant"])
                if row["variant"] != "banglish_clean"
                else {
                    "gate_hard_fails": "",
                    "eligible_n": "",
                    "eligible_baseline_correct": "",
                    "eligible_generated_correct": "",
                }
            )
            is_best = row["variant"] == best_generated["variant"]
            if row["variant"] == "banglish_clean":
                decision = "Baseline"
            elif stats["gate_hard_fails"] not in {"", 0}:
                decision = "Gate-blocked diagnostic"
            elif is_best and correct > baseline_correct:
                decision = "Gate-passing dev lead; needs generated-English before test150"
            elif correct > baseline_correct:
                decision = "Gate-passing weak dev lead"
            else:
                decision = "Gate-passing but no lead"
            table.append(
                {
                    "Model": model,
                    "Variant": label_map.get(row["variant"], row["variant"]),
                    "n": row["n"],
                    "Correct": correct,
                    "Accuracy": f"{float(row['accuracy']):.3f}",
                    "Delta vs Banglish": correct - baseline_correct,
                    "Delta 95% CI (pts)": (
                        ci(boot["ci95_low"], boot["ci95_high"]) if boot else ""
                    ),
                    "Direction p": boot["bootstrap_p_opposite_direction"] if boot else "",
                    "Parsed empty": row["parsed_empty"],
                    "Gate hard fails": stats["gate_hard_fails"],
                    "Eligible n": stats["eligible_n"],
                    "Eligible baseline": stats["eligible_baseline_correct"],
                    "Eligible generated": stats["eligible_generated_correct"],
                    "Decision": decision,
                }
            )
    write_csv(out_dir / "generated_bn_answer_audit_dev50.csv", table)
    return table


def generated_view_route_dev_table(out_dir: Path) -> list[dict[str, Any]]:
    specs = [
        (
            "Historical protected-v1 BNB generated-BN + Qwen3 generated-EN agreement",
            ROOT / "results/analysis/qwen3_4b_generated_view_agreement_route_dev_summary.csv",
            "generated_bn_bnb_correct",
            "Do not test150; generated-EN bottleneck.",
        ),
        (
            "Qwen3 protected-v3 BNB generated-BN + guarded generated-EN agreement",
            ROOT / "results/analysis/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev_summary.csv",
            "generated_bn_correct",
            "Weak dev-only +1 item; no held-out launch.",
        ),
        (
            "Qwen2.5 protected-v3 phonetic generated-BN + guarded generated-EN agreement",
            ROOT / "results/analysis/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev_summary.csv",
            "generated_bn_correct",
            "Negative dev route; drop for this model.",
        ),
    ]
    table: list[dict[str, Any]] = []
    for route, path, bn_field, decision in specs:
        if not path.exists():
            continue
        row = read_csv(path)[0]
        table.append(
            {
                "Route": route,
                "n": row["n"],
                "Banglish": row["banglish_correct"],
                "Generated-BN": row.get(bn_field, row["generated_bn_correct"]),
                "Generated-EN": row["generated_en_correct"],
                "Routed": row["routed_correct"],
                "Routed-Banglish": row["routed_minus_banglish"],
                "Routed items": row["route_to_generated_agreement"],
                "EN gate fallbacks": row["fallback_generated_en_gate"],
                "Decision": decision,
            }
        )
    write_csv(out_dir / "generated_view_agreement_route_dev.csv", table)
    return table


def v5_benqa_option_permutation_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(
        ROOT / "results/analysis/v5_benqa_option_permutation_probe_summary.csv"
    )
    headlines = [row for row in rows if row["section"] == "headline"]
    table: list[dict[str, Any]] = []
    for row in headlines:
        rotated_n = int(row["identity_D_rotated_rows"])
        label_d = int(row["identity_D_label_persistence"])
        semantic_d = int(row["identity_D_semantic_persistence"])
        if label_d > semantic_d:
            decision = "Label-position attraction dominates semantic D-content tracking"
        elif semantic_d > label_d:
            decision = "Semantic D-content tracking dominates label-position attraction"
        else:
            decision = "Mixed label-position and semantic tracking"
        table.append(
            {
                "Model": row["model"],
                "Source items": row["source_items"],
                "Identity pred D": f"{row['identity_pred_D']}/36",
                "Identity wrong D": row["identity_wrong_D"],
                "Rotated identity-D rows": rotated_n,
                "Remain label D": f"{label_d}/{rotated_n}",
                "Follow original D content": f"{semantic_d}/{rotated_n}",
                "Semantic match vs identity": (
                    f"{row['semantic_match_identity']}/"
                    f"{row['semantic_match_identity_n']}"
                ),
                "Exact semantic-equivariant items": (
                    f"{row['exact_semantic_equivariance_items']}/36"
                ),
                "Decision": decision,
            }
        )
    write_csv(out_dir / "v5_benqa_option_permutation_dev50.csv", table)
    return table


def bnsentmix_external_validation_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/bnsentmix_external_validation_summary.csv")
    headlines = [row for row in rows if row["section"] == "headline"]
    per_label = {
        (row["model"], row["label"]): row
        for row in rows
        if row["section"] == "per_label"
    }
    table: list[dict[str, Any]] = []
    for row in headlines:
        model = row["model"]
        table.append(
            {
                "Model": model,
                "Rows": row["n"],
                "Valid outputs": f"{row['valid_outputs']}/{row['n']}",
                "Correct": f"{row['correct']}/{row['n']}",
                "Accuracy": f"{pct(row['accuracy'])}%",
                "Macro-F1": f"{float(row['macro_f1']):.3f}",
                "Positive recall": f"{pct(per_label[(model, 'positive')]['recall'])}%",
                "Negative recall": f"{pct(per_label[(model, 'negative')]['recall'])}%",
                "Neutral recall": f"{pct(per_label[(model, 'neutral')]['recall'])}%",
                "Mixed recall": f"{pct(per_label[(model, 'mixed')]['recall'])}%",
                "Interpretation": (
                    "Zero-shot natural code-mixed sentiment external-validity layer"
                ),
            }
        )
    write_csv(out_dir / "bnsentmix_external_validation.csv", table)
    return table


def bnsentmix_model_complementarity_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/bnsentmix_model_complementarity_summary.csv")

    def find(section: str, metric: str) -> dict[str, str]:
        return next(row for row in rows if row["section"] == section and row["metric"] == metric)

    oracle = find("triad_oracle", "any_model_oracle")
    oracle_delta = find("triad_oracle", "oracle_minus_best_single")
    exactly_one = find("correct_count_distribution", "1")
    all_wrong = find("correct_count_distribution", "0")
    majority_7b = find("majority_vote", "majority_with_Qwen2.5-7B 8-bit_fallback")
    pair_rows = [row for row in rows if row["section"] == "pairwise"]
    best_pair = max(pair_rows, key=lambda row: int(row["pair_oracle_correct"]))

    table = [
        {
            "Result": "Best single model",
            "Count": f"{oracle_delta['best_single_correct']}/{oracle_delta['n']}",
            "Delta": "",
            "Interpretation": f"{oracle_delta['best_single_model']} is the strongest single BnSentMix row.",
        },
        {
            "Result": "Any-model diagnostic oracle",
            "Count": f"{oracle['correct']}/{oracle['n']}",
            "Delta": (
                f"{points(float(oracle_delta['delta_oracle_minus_best_single']) * 100)} pts, "
                f"CI [{points(float(oracle_delta['ci95_low']) * 100)}, "
                f"{points(float(oracle_delta['ci95_high']) * 100)}]"
            ),
            "Interpretation": "Upper bound showing cross-model error complementarity, not deployable accuracy.",
        },
        {
            "Result": "Exactly one model correct",
            "Count": f"{exactly_one['n']}/{exactly_one['denominator']}",
            "Delta": "",
            "Interpretation": "Rows where the answer is recoverable by only one of the three models.",
        },
        {
            "Result": "All models wrong",
            "Count": f"{all_wrong['n']}/{all_wrong['denominator']}",
            "Delta": "",
            "Interpretation": "Residual hard natural code-mixed sentiment rows for this model set.",
        },
        {
            "Result": "Best pair oracle",
            "Count": f"{best_pair['pair_oracle_correct']}/{best_pair['n']}",
            "Delta": "",
            "Interpretation": f"{best_pair['metric']} has the largest pairwise oracle coverage.",
        },
        {
            "Result": "Majority + 7B fallback",
            "Count": f"{majority_7b['correct']}/{majority_7b['n']}",
            "Delta": (
                f"{points(float(majority_7b['delta_vs_fallback_model']) * 100)} pts, "
                f"CI [{points(float(majority_7b['ci95_low']) * 100)}, "
                f"{points(float(majority_7b['ci95_high']) * 100)}]"
            ),
            "Interpretation": "Simple behavioral route; promising but not a locked deployment claim.",
        },
    ]
    write_csv(out_dir / "bnsentmix_model_complementarity.csv", table)
    return table


def bnsentmix_routing_devtest_table(out_dir: Path) -> list[dict[str, Any]]:
    rows = read_csv(ROOT / "results/analysis/bnsentmix_routing_devtest_summary.csv")

    def find(section: str, metric: str) -> dict[str, str]:
        return next(row for row in rows if row["section"] == section and row["metric"] == metric)

    def readable_rule_counts(value: str) -> str:
        return (
            value.replace("majority_fallback|Qwen2.5-7B 8-bit", "majority + Qwen2.5-7B fallback")
            .replace("majority_fallback|Qwen3-4B", "majority + Qwen3 fallback")
            .replace("single|Qwen3-4B", "single Qwen3")
        )

    pilot = find("pilot_devtest", "pilot40_selected_rule")
    hash5 = find("cv_overall", "hash5")
    block40 = find("cv_overall", "block40")
    table = [
        {
            "Protocol": "Pilot40-selected rule",
            "Selected result": f"{pilot['test_correct']}/{pilot['test_n']}",
            "Baseline context": (
                f"best single heldout {pilot['best_single_test_correct']}/{pilot['test_n']}"
            ),
            "Post-hoc context": (
                f"best heldout route {pilot['posthoc_best_correct']}/{pilot['test_n']}"
            ),
            "Interpretation": "Ordered 40-row pilot underperforms; not a reliable route selector.",
        },
        {
            "Protocol": "Hash5 cross-validation",
            "Selected result": f"{hash5['selected_correct']}/{hash5['n']}",
            "Baseline context": (
                f"Qwen3 {hash5['qwen3_correct']}/{hash5['n']}; "
                f"Qwen2.5-7B {hash5['qwen25_7b_correct']}/{hash5['n']}"
            ),
            "Post-hoc context": readable_rule_counts(hash5["selected_rule_counts"]),
            "Interpretation": "Majority + Qwen2.5-7B fallback is a weak deployable candidate.",
        },
        {
            "Protocol": "Block40 cross-validation",
            "Selected result": f"{block40['selected_correct']}/{block40['n']}",
            "Baseline context": (
                f"Qwen3 {block40['qwen3_correct']}/{block40['n']}; "
                f"Qwen2.5-7B {block40['qwen25_7b_correct']}/{block40['n']}"
            ),
            "Post-hoc context": readable_rule_counts(block40["selected_rule_counts"]),
            "Interpretation": "Ordered blocks expose split sensitivity; do not claim deployed mitigation.",
        },
    ]
    write_csv(out_dir / "bnsentmix_routing_devtest.csv", table)
    return table


def write_markdown(
    out_dir: Path,
    frozen_v5_main_gap: list[dict[str, Any]],
    main_gap: list[dict[str, Any]],
    scaling: list[dict[str, Any]],
    selfnorm: list[dict[str, Any]],
    routing: list[dict[str, Any]],
    real_banglish: list[dict[str, Any]],
    auto_suggested: list[dict[str, Any]],
    v5_reviewed: list[dict[str, Any]],
    v5_bad_row_policy: list[dict[str, Any]],
    cross_script_agreement: list[dict[str, Any]],
    generated_view_preservation: list[dict[str, Any]],
    diagnostic_pilots: list[dict[str, Any]],
    deterministic_generated_view_smokes: list[dict[str, Any]],
    generated_bn_candidate_preservation: list[dict[str, Any]],
    generated_bn_reference_similarity: list[dict[str, Any]],
    generated_bn_answer_audit: list[dict[str, Any]],
    generated_view_route_dev: list[dict[str, Any]],
    v5_benqa_option_permutation: list[dict[str, Any]],
    bnsentmix_external_validation: list[dict[str, Any]],
    bnsentmix_model_complementarity: list[dict[str, Any]],
    bnsentmix_routing_devtest: list[dict[str, Any]],
) -> None:
    sections = [
        ("Frozen V5 Main Script Gap", frozen_v5_main_gap),
        ("Main Script Gap", main_gap),
        ("Model Family And Scaling", scaling),
        ("Self-Normalization", selfnorm),
        ("Answer-Signal Routing", routing),
        ("Cross-Script Answer Agreement", cross_script_agreement),
        ("Generated-View Preservation Gates", generated_view_preservation),
        ("Deterministic Generated-View Smokes", deterministic_generated_view_smokes),
        ("Generated-BN Candidate Preservation", generated_bn_candidate_preservation),
        ("Generated-BN Reference Similarity Dev50", generated_bn_reference_similarity),
        ("Generated-BN Answer Audit Dev50", generated_bn_answer_audit),
        ("Generated-View Agreement Route Dev", generated_view_route_dev),
        ("V5 BEnQA Option Permutation Dev50", v5_benqa_option_permutation),
        ("BnSentMix External Validation", bnsentmix_external_validation),
        ("BnSentMix Model Complementarity", bnsentmix_model_complementarity),
        ("BnSentMix Routing Dev-Test", bnsentmix_routing_devtest),
        ("Diagnostic Model Pilots", diagnostic_pilots),
        ("Real Banglish Distribution", real_banglish),
        ("Auto-Suggested Banglish Sensitivity", auto_suggested),
        ("V5 Reviewed Banglish Sensitivity", v5_reviewed),
        ("V5 Flagged-Bad Policy Sensitivity", v5_bad_row_policy),
    ]
    path = out_dir / "thesis_tables.md"
    lines = [
        "# Generated Thesis Tables",
        "",
        "Generated from authoritative CSV artifacts. Re-run:",
        "",
        "```bash",
        "python3 scripts/build_thesis_tables.py",
        "```",
        "",
    ]
    for title, rows in sections:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(markdown_table(rows))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out_dir
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    main_gap, scaling = script_gap_tables(out_dir)
    frozen_v5_main_gap = frozen_v5_main_script_gap_table(out_dir)
    selfnorm = selfnorm_table(out_dir)
    routing = routing_table(out_dir)
    real_banglish = real_banglish_table(out_dir)
    auto_suggested = auto_suggested_sensitivity_table(out_dir)
    v5_reviewed = v5_reviewed_sensitivity_table(out_dir)
    v5_bad_row_policy = v5_bad_row_policy_table(out_dir)
    cross_script_agreement = cross_script_answer_agreement_table(out_dir)
    generated_view_preservation = generated_view_preservation_table(out_dir)
    diagnostic_pilots = diagnostic_pilot_table(out_dir)
    deterministic_generated_view_smokes = deterministic_generated_view_smoke_table(out_dir)
    generated_bn_candidate_preservation = generated_bn_candidate_preservation_table(
        out_dir, deterministic_generated_view_smokes
    )
    generated_bn_reference_similarity = generated_bn_reference_similarity_table(out_dir)
    generated_bn_answer_audit = generated_bn_answer_audit_table(out_dir)
    generated_view_route_dev = generated_view_route_dev_table(out_dir)
    v5_benqa_option_permutation = v5_benqa_option_permutation_table(out_dir)
    bnsentmix_external_validation = bnsentmix_external_validation_table(out_dir)
    bnsentmix_model_complementarity = bnsentmix_model_complementarity_table(out_dir)
    bnsentmix_routing_devtest = bnsentmix_routing_devtest_table(out_dir)
    write_markdown(
        out_dir,
        frozen_v5_main_gap,
        main_gap,
        scaling,
        selfnorm,
        routing,
        real_banglish,
        auto_suggested,
        v5_reviewed,
        v5_bad_row_policy,
        cross_script_agreement,
        generated_view_preservation,
        diagnostic_pilots,
        deterministic_generated_view_smokes,
        generated_bn_candidate_preservation,
        generated_bn_reference_similarity,
        generated_bn_answer_audit,
        generated_view_route_dev,
        v5_benqa_option_permutation,
        bnsentmix_external_validation,
        bnsentmix_model_complementarity,
        bnsentmix_routing_devtest,
    )
    print(f"wrote={out_dir}")


if __name__ == "__main__":
    main()
