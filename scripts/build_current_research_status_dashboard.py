#!/usr/bin/env python3
"""Build a compact current-status dashboard from generated research checks."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date
from pathlib import Path

from build_artifact_manifest import DEFAULT_INCLUDE_ROOTS, iter_artifacts


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_int_from_report(path: Path, pattern: str) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(pattern, text)
    if not match:
        return 0
    return int(match.group(1).replace(",", ""))


def add_row(
    rows: list[dict[str, str]],
    area: str,
    status: str,
    metric: str,
    value: str | int | float,
    detail: str,
) -> None:
    rows.append(
        {
            "area": area,
            "status": status,
            "metric": metric,
            "value": str(value),
            "detail": detail,
        }
    )


def status_label(ok: bool, blocked: bool = False) -> str:
    if ok:
        return "pass"
    if blocked:
        return "blocked"
    return "fail"


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _line in handle)


def points(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}"


def summarize_v5_sensitivity(path: Path, label: str) -> str:
    rows = read_csv(path)
    overall = next(row for row in rows if row["group"] == "overall")
    delta = float(overall["delta_candidate_minus_baseline"]) * 100
    low = float(overall["ci95_low"]) * 100
    high = float(overall["ci95_high"]) * 100
    return (
        f"{label} {overall['baseline_correct']}/{overall['n']}->"
        f"{overall['candidate_correct']}/{overall['n']} "
        f"({points(delta)} pts, CI [{points(low)}, {points(high)}])"
    )


def first_pending_session(resume_rows: list[dict[str, str]]) -> dict[str, str] | None:
    for row in resume_rows:
        if int(row.get("pending_rows", "0") or 0) > 0:
            return row
    return None


def projected_manifest_count(output_paths: list[Path]) -> int:
    artifacts = iter_artifacts(ROOT, DEFAULT_INCLUDE_ROOTS)
    artifact_paths = {artifact.path for artifact in artifacts}
    missing_outputs = 0
    for output_path in output_paths:
        path = output_path if output_path.is_absolute() else ROOT / output_path
        rel = str(path.relative_to(ROOT))
        if rel not in artifact_paths:
            missing_outputs += 1
    return len(artifacts) + missing_outputs


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["area", "status", "metric", "value", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, str]], path: Path, csv_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_area: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_area.setdefault(row["area"], []).append(row)

    v5_status = next(row for row in rows if row["area"] == "v5_manual_review" and row["metric"] == "review_progress")
    rerun_status = next(
        (
            row
            for row in rows
            if row["area"] == "post_v5_reruns"
            and row["metric"] == "required_v5_sensitivity"
        ),
        next(row for row in rows if row["area"] == "post_v5_reruns" and row["metric"] == "readiness"),
    )
    qa_status = "pass" if all(row["status"] == "pass" for row in rows if row["area"] in {"qa_gates", "literature"}) else "fail"

    lines = [
        "# Current Research Status Dashboard",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "This dashboard is generated from the current local reports and CSVs. It",
        "is intended as the fastest one-file resume point before running local checks",
        "or deciding whether the next API step is replication or format-control testing.",
        "",
        f"Machine-readable dashboard: `{csv_path.relative_to(ROOT)}`.",
        "",
        "## Stoplight",
        "",
        "| Area | Status | Summary |",
        "| --- | --- | --- |",
        f"| v5 manual review | `{v5_status['status']}` | {v5_status['detail']} |",
        f"| post-v5 reruns | `{rerun_status['status']}` | {rerun_status['detail']} |",
        f"| QA/literature gates | `{qa_status}` | generated checks are green if status is `pass` |",
        "",
        "## Immediate Next Action",
        "",
    ]

    if v5_status["status"] != "pass":
        lines.extend(
            [
                "Continue manual v5 review from the next-session brief and resume card.",
                "Do not prepare or launch post-v5 Kaggle jobs while the rerun readiness",
                "status is `not_ready`.",
                "",
                "- Next-session brief: `reports/validation200_v5_next_session_brief.md`",
                "- Resume card: `reports/validation200_v5_review_resume_card.md`",
                "",
                "```bash",
                "python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run",
                "python3 scripts/review_validation200_v5_queue.py --session 1",
                "```",
                "",
            ]
        )
    elif rerun_status["status"] != "pass":
        lines.extend(
            [
                "Freeze the reviewed v5 Banglish slice, audit the frozen artifact,",
                "then rerun the local check bundle. Do not launch Kaggle jobs until",
                "`reports/post_v5_rerun_readiness.md` reports `ready`.",
                "",
                "```bash",
                "python3 scripts/validate_banglish_review_queue.py --require-complete",
                "python3 scripts/apply_banglish_review.py \\",
                "  --input data/slices/validation_200_v4.jsonl \\",
                "  --review data/slices/validation_200_v5_review_queue.csv \\",
                "  --output data/slices/validation_200_v5.jsonl \\",
                "  --audit-output results/analysis/validation200_v5_banglish_review_audit.csv \\",
                "  --quality-status human_reviewed_banglish_v5",
                "python3 scripts/audit_banglish_artifacts.py \\",
                "  data/slices/validation_200_v5.jsonl \\",
                "  --summary-output results/analysis/validation200_v5_banglish_artifact_summary.csv \\",
                "  --examples-output results/analysis/validation200_v5_banglish_artifact_examples.csv",
                "python3 scripts/run_research_checks.py",
                "```",
                "",
            ]
        )
    elif rerun_status["metric"] == "required_v5_sensitivity":
        optional_7b = next(
            (
                row
                for row in rows
                if row["area"] == "post_v5_reruns"
                and row["metric"] == "optional_7b_v5"
            ),
            None,
        )
        if optional_7b and optional_7b["status"] == "pass":
            lines.extend(
                [
                    "Required and optional post-v5 Banglish reruns are complete.",
                    "Use the frozen-v5 three-model main table in the thesis update,",
                    "then integrate the completed frontier panel and DeepSeek",
                    "full851 API replication before any broader API spend.",
                    "",
                    "- Main table: `results/tables/main_script_gap_validation200_v5.csv`",
                    "- Main report: `reports/main_results_validation200_v5.md`",
                    "- v5 sensitivity table: `results/tables/v5_reviewed_banglish_sensitivity.csv`",
                    "- v5 recoverability source decomposition: `reports/v5_recoverability_source_decomposition.md`",
                    "- v5 cross-script transfer retention: `reports/v5_cross_script_transfer.md`",
                    "- v5 review-label sensitivity: `reports/v5_review_label_sensitivity.md`",
                    "- v5 dataset gap intervals: `reports/v5_dataset_gap_intervals.md`",
                    "- v5 paired sign tests: `reports/v5_paired_sign_tests.md`",
                    "- v5 clustered gap robustness: `reports/v5_clustered_gap_robustness.md`",
                    "- v5 BEnQA subject stability: `reports/v5_benqa_subject_stability.md`",
                    "- v5 BEnQA subject-macro balance: `reports/v5_benqa_subject_balance.md`",
                    "- v5 fragility feature analysis: `reports/v5_banglish_fragility_feature_analysis.md`",
                    "- v5 Qwen scaling-transfer audit: `reports/v5_qwen_scaling_transfer.md`",
                    "- v5 fragility model-overlap analysis: `reports/v5_banglish_fragility_model_overlap.md`",
                    "- v5 item consensus audit: `reports/v5_item_consensus.md`",
                    "- v5 difficulty-conditioned gap audit: `reports/v5_difficulty_conditioned_gap.md`",
                    "- v5 consensus stability audit: `reports/v5_consensus_stability.md`",
                    "- v5 composition sensitivity audit: `reports/v5_composition_sensitivity.md`",
                    "- v5 shared-fragility examples: `reports/v5_shared_fragility_examples.md`",
                    "- v5 tokenization/failure join: `reports/tokenization_cross_script_failure_patterns.md`",
                    "- v5 subject/grade breakdown: `reports/subject_breakdown_validation200_v5.md`",
                    "- v5 answer-format audit: `reports/v5_answer_format_audit.md`",
                    "- v5 response-style drift audit: `reports/v5_response_style_drift.md`",
                    "- v5 BanglaMATH numeric sensitivity: `reports/v5_banglamath_numeric_sensitivity.md`",
                    "- v5 BanglaMATH numeric transfer audit: `reports/v5_banglamath_numeric_transfer.md`",
                    "- v5 BEnQA choice-bias audit: `reports/v5_benqa_choice_bias.md`",
                    "- v5 BEnQA subject option-bias audit: `reports/v5_benqa_subject_option_bias.md`",
                    "- v5 BEnQA prediction-diversity audit: `reports/v5_benqa_prediction_diversity.md`",
                    "- v5 BEnQA option position/content audit: `reports/v5_benqa_option_position_content.md`",
                    "- v5 BEnQA option-switching audit: `reports/v5_benqa_option_switching.md`",
                    "- v5 BEnQA cross-script option-agreement audit: `reports/v5_benqa_cross_script_option_agreement.md`",
                    "- v5 BEnQA cross-model Banglish-agreement audit: `reports/v5_benqa_cross_model_banglish_agreement.md`",
                    "- v5 BEnQA order-confound audit: `reports/v5_benqa_order_confound.md`",
                    "- v5 BEnQA review-label option-bias audit: `reports/v5_benqa_review_label_option_bias.md`",
                    "- v5 BEnQA length/token confound audit: `reports/v5_benqa_length_token_confound.md`",
                    "- v5 BEnQA option-coverage confound audit: `reports/v5_benqa_option_coverage_confound.md`",
                    "- v5 BEnQA option-switch confound audit: `reports/v5_benqa_option_switch_confound.md`",
                    "- v5 BEnQA option semantic-cue audit: `reports/v5_benqa_option_semantic_cues.md`",
                    "- v5 BEnQA multi-confound residual audit: `reports/v5_benqa_multiconfound_residual.md`",
                    "- v5 BEnQA distractor-transition audit: `reports/v5_benqa_distractor_transition.md`",
                    "- v5 BEnQA label-balance sensitivity: `reports/v5_benqa_label_balance.md`",
                    "- v5 BEnQA option-permutation dev probe: `reports/v5_benqa_option_permutation_probe_results.md`",
                    "- real-Banglish v5 distribution: `reports/real_banglish_distribution_comparison.md`",
                    "- v5 BanglaTLit lexical coverage audit: `reports/v5_banglatlit_lexical_coverage.md`",
                    "- v5 BEnQA option lexical coverage audit: `reports/v5_benqa_option_lexical_coverage.md`",
                    "- v5 BanglaTLit model-coverage sensitivity: `reports/v5_banglatlit_model_coverage_sensitivity.md`",
                    "- v5 BanglaTLit spelling-variation sensitivity: `reports/v5_banglatlit_spelling_variation_sensitivity.md`",
                    "- v5 source-variant structural parity audit: `reports/v5_source_variant_structural_parity.md`",
                    "- v5 English-warning sensitivity audit: `reports/v5_english_warning_sensitivity.md`",
                    "- v5 review edit-distance sensitivity audit: `reports/v5_review_edit_distance_sensitivity.md`",
                    "- BEnQA extension strategy: `reports/benqa_extension_publication_strategy.md`",
                    "- BEnQA extension AI-assisted review: `reports/benqa_extended_1000_v1_ai_review.md`",
                    "- BEnQA extension eval subsets: `reports/benqa_extension_eval_subsets.md`",
                    "- BEnQA extension Kaggle smoke: `reports/benqa_extension_kaggle_smoke_launch.md`",
                    "- BEnQA extension full Qwen2.5-3B result: `reports/qwen25_3b_benqa_ext_full851.md`",
                    "- BEnQA extension full paired gaps: `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`",
                    "- BEnQA extension full DeepSeek result: `reports/deepseek_v4_flash_benqa_ext_full851.md`",
                    "- BEnQA extension full DeepSeek paired gaps: `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`",
                    "- BEnQA extension pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`",
                    "- 7B sensitivity report: `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish.md`",
                    "- Gemini API audit: `reports/gemini_3_5_flash_validation200_v5_results.md`",
                    "- Gemini API summary: `results/analysis/gemini_3_5_flash_validation200_v5_summary.csv`",
                    "- GPT-5.5 full API audit: `reports/openai_gpt55_low_validation200_v5_cap1024_results.md`",
                    "- GPT-5.5 full API summary: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_summary.csv`",
                    "- Frontier API panel: `reports/frontier_api_panel_validation200_v5.md`",
                    "- Claude API audit: `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md`",
                    "- DeepSeek API full851: `reports/deepseek_v4_flash_benqa_ext_full851.md`",
                    "- Controlled frontier runbook: `reports/paid_api_audit_execution_runbook.md`",
                    "- Claude sender: `scripts/run_anthropic_api_audit.py`",
                    "- DeepSeek/OpenAI-compatible sender: `scripts/run_openai_compatible_chat_api_audit.py`",
                    "- Full validation-200 API manifest: `data/api_audit/validation200_v5_requests.jsonl`",
                    "- Full validation-200 manifest report: `reports/validation200_v5_api_audit_prompt_manifest.md`",
                    "- API audit plan/runbook: `reports/final_api_audit_cost_plan.md`",
                    "- Paid audit manifest check: `reports/api_audit_manifest_integrity_check.md`",
                    "- Paid audit import round-trip check: `reports/api_audit_import_roundtrip_check.md`",
                    "- Generated-view status: protected-v3 repairs generated-BN preservation",
                    "  and guarded EN repairs hard preservation, but the route remains",
                    "  dev-only (+1 Qwen3, -1 Qwen2.5) and strict agreement",
                    "  misses most generated-view recoveries; looser rules are volatile:",
                    "  `reports/generated_view_diagnostics_summary.md`",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    "Required post-v5 Banglish reruns are complete. Use the v5",
                    "sensitivity table in the thesis update; the optional Qwen2.5-7B",
                    "v5 rerun is only worth retrying with the known pinned 8-bit stack",
                    "if the scaling table needs a cleaner v5-only row.",
                    "",
                    "- v5 sensitivity table: `results/tables/v5_reviewed_banglish_sensitivity.csv`",
                    "- Optional 7B failure note: `reports/qwen25_7b_8bit_validation200_v5_failure.md`",
                    "",
                ]
            )
    else:
        lines.extend(
            [
                "Post-v5 rerun readiness is green. Prepare Kaggle jobs from the",
                "readiness-gated job plan, starting with the required Qwen2.5-3B",
                "and Qwen3-4B clean-Banglish reruns.",
                "",
                "- Job plan: `reports/post_v5_kaggle_job_plan.md`",
                "- Compute budget: `reports/post_v5_compute_budget.md`",
                "",
            ]
        )

    for area, area_rows in by_area.items():
        title = area.replace("_", " ").title()
        lines.extend(
            [
                f"## {title}",
                "",
                "| Status | Metric | Value | Detail |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for row in area_rows:
            lines.append(
                f"| `{row['status']}` | `{row['metric']}` | {row['value']} | {row['detail']} |"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    queue_rows = read_csv(args.review_queue)
    resume_rows = read_csv(args.review_resume)
    reviewed = sum(1 for row in queue_rows if row.get("quality_label", "").strip())
    pending = len(queue_rows) - reviewed
    next_session = first_pending_session(resume_rows)
    next_detail = (
        "all review sessions complete"
        if next_session is None
        else (
            f"next session {next_session['session']} "
            f"({next_session['substitution']}), pending "
            f"{next_session['pending_rows']} of {next_session['total_rows']}"
        )
    )
    add_row(
        rows,
        "v5_manual_review",
        status_label(pending == 0, blocked=pending > 0),
        "review_progress",
        f"{reviewed}/{len(queue_rows)}",
        next_detail,
    )

    readiness_rows = read_csv(args.rerun_readiness)
    failing_gates = [row for row in readiness_rows if row.get("status") == "fail"]
    add_row(
        rows,
        "post_v5_reruns",
        status_label(not failing_gates, blocked=bool(failing_gates)),
        "readiness",
        "ready" if not failing_gates else "not_ready",
        f"failing_gates={len(failing_gates)}",
    )

    job_rows = read_csv(args.kaggle_job_plan)
    ready_jobs = sum(1 for row in job_rows if row.get("status") == "ready_to_prepare")
    conditional_jobs = sum(1 for row in job_rows if row.get("status", "").startswith("conditional"))
    blocked_jobs = sum(1 for row in job_rows if row.get("status", "").startswith("blocked"))
    add_row(
        rows,
        "post_v5_reruns",
        status_label(blocked_jobs == 0, blocked=blocked_jobs > 0),
        "kaggle_jobs",
        len(job_rows),
        f"ready_jobs={ready_jobs}; conditional_jobs={conditional_jobs}; blocked_jobs={blocked_jobs}",
    )

    budget_rows = read_csv(args.compute_budget)
    required_hours = sum(
        float(row["conservative_gpu_hours"])
        for row in budget_rows
        if row.get("condition") == "required_after_readiness"
    )
    all_hours = sum(float(row["conservative_gpu_hours"]) for row in budget_rows)
    add_row(
        rows,
        "post_v5_reruns",
        "pass",
        "conservative_gpu_hours",
        f"{required_hours:.2f}/{all_hours:.2f}",
        "required/required_plus_conditional under 120h Kaggle assumption",
    )

    if args.qwen25_v5_summary.exists() and args.qwen3_v5_summary.exists():
        qwen25_summary = summarize_v5_sensitivity(args.qwen25_v5_summary, "Qwen2.5-3B")
        qwen3_summary = summarize_v5_sensitivity(args.qwen3_v5_summary, "Qwen3-4B")
        add_row(
            rows,
            "post_v5_reruns",
            "pass",
            "required_v5_sensitivity",
            "2/2",
            f"{qwen25_summary}; {qwen3_summary}",
        )

    if args.optional_7b_output.exists() or args.optional_7b_log.exists():
        output_rows = line_count(args.optional_7b_output) if args.optional_7b_output.exists() else 0
        log_text = (
            args.optional_7b_log.read_text(encoding="utf-8", errors="replace")
            if args.optional_7b_log.exists()
            else ""
        )
        if output_rows == 0 and "cublasLt ran into an error" in log_text:
            add_row(
                rows,
                "post_v5_reruns",
                "blocked",
                "optional_7b_v5",
                "0 rows",
                "Kaggle P100 latest-stack bitsandbytes cublasLt failure; retry only with pinned 8-bit stack",
            )
        elif output_rows > 0:
            add_row(
                rows,
                "post_v5_reruns",
                "pass",
                "optional_7b_v5",
                output_rows,
                "output rows downloaded",
            )
        else:
            add_row(
                rows,
                "post_v5_reruns",
                "blocked",
                "optional_7b_v5",
                "unknown",
                "optional kernel output missing or incomplete",
            )

    packet_rows = read_csv(args.packet_integrity)
    packet_issues = sum(1 for row in packet_rows if row.get("status") != "ok")
    add_row(
        rows,
        "qa_gates",
        status_label(packet_issues == 0),
        "v5_packet_integrity",
        len(packet_rows),
        f"issues={packet_issues}",
    )

    figure_rows = read_csv(args.figure_integrity)
    figure_issues = sum(1 for row in figure_rows if row.get("status") != "ok")
    add_row(
        rows,
        "qa_gates",
        status_label(figure_issues == 0),
        "thesis_figure_integrity",
        len(figure_rows),
        f"issues={figure_issues}",
    )

    table_rows = read_csv(args.table_integrity)
    table_issues = sum(1 for row in table_rows if row.get("status") != "ok")
    add_row(
        rows,
        "qa_gates",
        status_label(table_issues == 0),
        "thesis_table_integrity",
        len(table_rows),
        f"issues={table_issues}",
    )

    api_manifest_rows = read_csv(args.api_audit_manifest)
    api_manifest_issues = sum(1 for row in api_manifest_rows if row.get("status") != "ok")
    add_row(
        rows,
        "qa_gates",
        status_label(api_manifest_issues == 0),
        "api_audit_manifest",
        len(api_manifest_rows),
        f"issues={api_manifest_issues}",
    )

    api_import_rows = read_csv(args.api_audit_import_roundtrip)
    api_import_issues = sum(1 for row in api_import_rows if row.get("status") != "ok")
    add_row(
        rows,
        "qa_gates",
        status_label(api_import_issues == 0),
        "api_audit_import_roundtrip",
        len(api_import_rows),
        f"issues={api_import_issues}",
    )

    if args.gemini_api_summary.exists():
        gemini_rows = read_csv(args.gemini_api_summary)
        by_key = {(row["dataset"], row["variant"]): row for row in gemini_rows}
        variants = ("bangla", "banglish_clean", "english")
        strict = "/".join(by_key[("all", variant)]["strict_correct"] for variant in variants)
        secondary = "/".join(by_key[("all", variant)]["secondary_correct"] for variant in variants)
        n = by_key[("all", "bangla")]["n"]
        add_row(
            rows,
            "qa_gates",
            "pass",
            "gemini_api_audit",
            int(n) * len(variants),
            f"Gemini 3.5 Flash all-200 strict={strict}; secondary={secondary}",
        )
    else:
        add_row(
            rows,
            "qa_gates",
            "blocked",
            "gemini_api_audit",
            0,
            "Gemini API summary missing",
        )

    if args.openai_api_summary.exists():
        openai_rows = read_csv(args.openai_api_summary)
        by_key = {(row["dataset"], row["variant"]): row for row in openai_rows}
        variants = ("bangla", "banglish_clean", "english")
        strict = "/".join(by_key[("all", variant)]["strict_correct"] for variant in variants)
        secondary = "/".join(by_key[("all", variant)]["secondary_correct"] for variant in variants)
        n = by_key[("all", "bangla")]["n"]
        add_row(
            rows,
            "qa_gates",
            "pass",
            "openai_gpt55_full_api_audit",
            int(n) * len(variants),
            f"GPT-5.5 low all-200 strict={strict}; secondary={secondary}",
        )
    else:
        add_row(
            rows,
            "qa_gates",
            "blocked",
            "openai_gpt55_full_api_audit",
            0,
            "GPT-5.5 full API summary missing",
        )

    if args.frontier_api_panel.exists():
        panel_rows = read_csv(args.frontier_api_panel)
        strict_rows = [row for row in panel_rows if row.get("score_mode") == "strict"]
        model_names = {row.get("model", "") for row in strict_rows}
        panel_ok = len(panel_rows) == 10 and len(model_names) == 5 and all(
            int(row.get("raw_rows") or 0) == 600 for row in strict_rows
        )
        add_row(
            rows,
            "qa_gates",
            status_label(panel_ok),
            "frontier_api_panel_validation200_v5",
            sum(int(row.get("raw_rows") or 0) for row in strict_rows),
            "models=" + ",".join(sorted(model_names)),
        )
    else:
        add_row(
            rows,
            "qa_gates",
            "blocked",
            "frontier_api_panel_validation200_v5",
            0,
            "Frontier API panel missing",
        )

    if args.benqa_extension_review_queue.exists():
        extension_rows = read_csv(args.benqa_extension_review_queue)
        status_counts = Counter(row.get("review_status", "") for row in extension_rows)
        fail_count = status_counts.get("ai_assisted_review_fail_v1", 0)
        pass_count = status_counts.get("ai_assisted_review_pass_v1", 0)
        warn_count = status_counts.get("ai_assisted_review_warn_v1", 0)
        add_row(
            rows,
            "qa_gates",
            status_label(len(extension_rows) >= 1000 and fail_count == 0),
            "benqa_extended_ai_review",
            len(extension_rows),
            f"pass={pass_count}; warn={warn_count}; fail={fail_count}",
        )
    else:
        add_row(
            rows,
            "qa_gates",
            "blocked",
            "benqa_extended_ai_review",
            0,
            "BEnQA extension review queue missing",
        )

    if args.benqa_extension_full_summary.exists() and args.benqa_extension_full_paired.exists():
        full_rows = read_csv(args.benqa_extension_full_summary)
        by_variant = {row["variant"]: row for row in full_rows}
        paired_rows = read_csv(args.benqa_extension_full_paired)
        by_gap = {row["label"]: row for row in paired_rows if row["metric"] == "paired_gap"}
        expected_variants = ("bangla", "banglish_clean", "english")
        full_n = sum(int(by_variant[variant]["n"]) for variant in expected_variants)
        parsed_empty = sum(int(by_variant[variant]["parsed_empty"]) for variant in expected_variants)
        banglish_bangla = by_gap["banglish_minus_bangla"]
        banglish_english = by_gap["banglish_minus_english"]
        scale_ok = (
            full_n == 2553
            and parsed_empty == 0
            and float(banglish_bangla["ci95_high"]) < 0
            and float(banglish_english["ci95_high"]) < 0
        )
        detail = (
            "acc="
            f"BN:{by_variant['bangla']['correct']}/851,"
            f"BG:{by_variant['banglish_clean']['correct']}/851,"
            f"EN:{by_variant['english']['correct']}/851; "
            f"gaps=BG-BN:{float(banglish_bangla['accuracy']) * 100:.2f}pts,"
            f"BG-EN:{float(banglish_english['accuracy']) * 100:.2f}pts"
        )
        add_row(
            rows,
            "qa_gates",
            status_label(scale_ok),
            "benqa_extension_full851_qwen25_3b",
            full_n,
            detail,
        )
    else:
        add_row(
            rows,
            "qa_gates",
            "blocked",
            "benqa_extension_full851_qwen25_3b",
            0,
            "BEnQA extension full851 summary/paired gaps missing",
        )

    if args.deepseek_extension_full_summary.exists() and args.deepseek_extension_full_paired.exists():
        full_rows = read_csv(args.deepseek_extension_full_summary)
        by_variant = {row["variant"]: row for row in full_rows}
        paired_rows = read_csv(args.deepseek_extension_full_paired)
        by_gap = {row["label"]: row for row in paired_rows if row["metric"] == "paired_gap"}
        expected_variants = ("bangla", "banglish_clean", "english")
        full_n = sum(int(by_variant[variant]["n"]) for variant in expected_variants)
        parsed_empty = sum(int(by_variant[variant]["parsed_empty"]) for variant in expected_variants)
        banglish_bangla = by_gap["banglish_minus_bangla"]
        banglish_english = by_gap["banglish_minus_english"]
        scale_ok = (
            full_n == 2553
            and parsed_empty == 0
            and float(banglish_bangla["ci95_high"]) < 0
            and float(banglish_english["ci95_high"]) < 0
        )
        detail = (
            "acc="
            f"BN:{by_variant['bangla']['correct']}/851,"
            f"BG:{by_variant['banglish_clean']['correct']}/851,"
            f"EN:{by_variant['english']['correct']}/851; "
            f"gaps=BG-BN:{float(banglish_bangla['accuracy']) * 100:.2f}pts,"
            f"BG-EN:{float(banglish_english['accuracy']) * 100:.2f}pts"
        )
        add_row(
            rows,
            "qa_gates",
            status_label(scale_ok),
            "benqa_extension_full851_deepseek_v4_flash",
            full_n,
            detail,
        )
    else:
        add_row(
            rows,
            "qa_gates",
            "blocked",
            "benqa_extension_full851_deepseek_v4_flash",
            0,
            "DeepSeek BEnQA extension full851 summary/paired gaps missing",
        )

    research_log_rows = read_csv(args.research_log_compactness)
    research_log_issues = sum(1 for row in research_log_rows if row.get("status") != "ok")
    add_row(
        rows,
        "qa_gates",
        status_label(research_log_issues == 0),
        "research_log_compactness",
        len(research_log_rows),
        f"issues={research_log_issues}",
    )

    recoverability_summary = read_csv(args.recoverability_source_summary)
    recoverability_items = read_csv(args.recoverability_source_items)
    recoverability_ok = len(recoverability_summary) == 300 and len(recoverability_items) == 600
    add_row(
        rows,
        "qa_gates",
        status_label(recoverability_ok),
        "v5_recoverability_sources",
        len(recoverability_items),
        f"summary_rows={len(recoverability_summary)}",
    )

    transfer_summary = read_csv(args.cross_script_transfer_summary)
    transfer_items = read_csv(args.cross_script_transfer_items)
    transfer_ok = len(transfer_summary) == 36 and len(transfer_items) == 600
    add_row(
        rows,
        "qa_gates",
        status_label(transfer_ok),
        "v5_cross_script_transfer",
        len(transfer_items),
        f"summary_rows={len(transfer_summary)}",
    )

    token_failure_summary = read_csv(args.token_failure_summary)
    token_failure_items = read_csv(args.token_failure_items)
    token_failure_ok = len(token_failure_summary) == 78 and len(token_failure_items) == 600
    add_row(
        rows,
        "qa_gates",
        status_label(token_failure_ok),
        "v5_token_failure_join",
        len(token_failure_items),
        f"summary_rows={len(token_failure_summary)}",
    )

    review_label_rows = read_csv(args.review_label_sensitivity)
    review_label_ok = len(review_label_rows) == 39
    add_row(
        rows,
        "qa_gates",
        status_label(review_label_ok),
        "v5_review_label_sensitivity",
        len(review_label_rows),
        "expected_rows=39",
    )

    dataset_gap_rows = read_csv(args.dataset_gap_intervals)
    dataset_gap_ok = len(dataset_gap_rows) == 18
    add_row(
        rows,
        "qa_gates",
        status_label(dataset_gap_ok),
        "v5_dataset_gap_intervals",
        len(dataset_gap_rows),
        "expected_rows=18",
    )

    paired_sign_rows = read_csv(args.paired_sign_tests)
    paired_sign_ok = len(paired_sign_rows) == 18
    add_row(
        rows,
        "qa_gates",
        status_label(paired_sign_ok),
        "v5_paired_sign_tests",
        len(paired_sign_rows),
        "expected_rows=18",
    )

    clustered_gap_summary = read_csv(args.clustered_gap_summary)
    clustered_gap_clusters = read_csv(args.clustered_gap_clusters)
    clustered_gap_ok = len(clustered_gap_summary) == 18 and len(clustered_gap_clusters) == 192
    add_row(
        rows,
        "qa_gates",
        status_label(clustered_gap_ok),
        "v5_clustered_gap_robustness",
        len(clustered_gap_clusters),
        f"summary_rows={len(clustered_gap_summary)}",
    )

    benqa_subject_rows = read_csv(args.benqa_subject_stability)
    benqa_subject_ok = len(benqa_subject_rows) == 42
    add_row(
        rows,
        "qa_gates",
        status_label(benqa_subject_ok),
        "v5_benqa_subject_stability",
        len(benqa_subject_rows),
        "expected_rows=42",
    )

    benqa_subject_balance_summary = read_csv(args.benqa_subject_balance_summary)
    benqa_subject_balance_subjects = read_csv(args.benqa_subject_balance_subjects)
    benqa_subject_balance_ok = (
        len(benqa_subject_balance_summary) == 6
        and len(benqa_subject_balance_subjects) == 39
    )
    add_row(
        rows,
        "qa_gates",
        status_label(benqa_subject_balance_ok),
        "v5_benqa_subject_balance",
        len(benqa_subject_balance_subjects),
        f"summary_rows={len(benqa_subject_balance_summary)}",
    )

    scaling_transfer_summary = read_csv(args.qwen_scaling_transfer_summary)
    scaling_transfer_transitions = read_csv(args.qwen_scaling_transfer_transitions)
    same_family_bangla = next(
        row
        for row in scaling_transfer_summary
        if row["section"] == "script_transition"
        and row["dataset"] == "all"
        and row["pair_id"] == "same_family_3b_to_7b"
        and row["script"] == "bangla"
    )
    same_family_banglish = next(
        row
        for row in scaling_transfer_summary
        if row["section"] == "script_transition"
        and row["dataset"] == "all"
        and row["pair_id"] == "same_family_3b_to_7b"
        and row["script"] == "banglish"
    )
    same_family_english = next(
        row
        for row in scaling_transfer_summary
        if row["section"] == "script_transition"
        and row["dataset"] == "all"
        and row["pair_id"] == "same_family_3b_to_7b"
        and row["script"] == "english"
    )
    qwen3_gap = next(
        row
        for row in scaling_transfer_summary
        if row["section"] == "gap_change"
        and row["dataset"] == "all"
        and row["pair_id"] == "qwen25_3b_to_qwen3_4b"
    )
    scaling_transfer_ok = (
        len(scaling_transfer_summary) == 63
        and len(scaling_transfer_transitions) == 1800
        and int(same_family_bangla["net_gain"]) == 11
        and int(same_family_banglish["net_gain"]) == 6
        and int(same_family_english["net_gain"]) == 23
        and int(qwen3_gap["gap_change"]) == -18
    )
    add_row(
        rows,
        "qa_gates",
        status_label(scaling_transfer_ok),
        "v5_qwen_scaling_transfer",
        len(scaling_transfer_transitions),
        (
            f"summary_rows={len(scaling_transfer_summary)}; "
            f"qwen25_net_gains=bangla:{same_family_bangla['net_gain']},"
            f"banglish:{same_family_banglish['net_gain']},"
            f"english:{same_family_english['net_gain']}; "
            f"qwen3_gap_change={qwen3_gap['gap_change']}"
        ),
    )

    overlap_summary = read_csv(args.fragility_overlap_summary)
    overlap_items = read_csv(args.fragility_overlap_items)
    overlap_ok = len(overlap_summary) == 65 and len(overlap_items) == 200
    add_row(
        rows,
        "qa_gates",
        status_label(overlap_ok),
        "v5_fragility_overlap",
        len(overlap_items),
        f"summary_rows={len(overlap_summary)}",
    )

    item_consensus_summary = read_csv(args.item_consensus_summary)
    item_consensus_items = read_csv(args.item_consensus_items)
    item_consensus_ok = len(item_consensus_summary) == 80 and len(item_consensus_items) == 200
    add_row(
        rows,
        "qa_gates",
        status_label(item_consensus_ok),
        "v5_item_consensus",
        len(item_consensus_items),
        f"summary_rows={len(item_consensus_summary)}",
    )

    difficulty_summary = read_csv(args.difficulty_conditioned_summary)
    difficulty_items = read_csv(args.difficulty_conditioned_items)
    difficulty_ok = len(difficulty_summary) == 36 and len(difficulty_items) == 200
    add_row(
        rows,
        "qa_gates",
        status_label(difficulty_ok),
        "v5_difficulty_conditioned_gap",
        len(difficulty_items),
        f"summary_rows={len(difficulty_summary)}",
    )

    consensus_stability_summary = read_csv(args.consensus_stability_summary)
    consensus_stability_items = read_csv(args.consensus_stability_items)
    consensus_stability_ok = (
        len(consensus_stability_summary) == 21 and len(consensus_stability_items) == 1400
    )
    add_row(
        rows,
        "qa_gates",
        status_label(consensus_stability_ok),
        "v5_consensus_stability",
        len(consensus_stability_items),
        f"summary_rows={len(consensus_stability_summary)}",
    )

    composition_summary = read_csv(args.composition_sensitivity_summary)
    composition_items = read_csv(args.composition_sensitivity_items)
    composition_ok = len(composition_summary) == 27 and len(composition_items) == 200
    add_row(
        rows,
        "qa_gates",
        status_label(composition_ok),
        "v5_composition_sensitivity",
        len(composition_items),
        f"summary_rows={len(composition_summary)}",
    )

    shared_examples = read_csv(args.shared_fragility_examples)
    all_three_strict_examples = sum(
        1 for row in shared_examples if row.get("tier") == "main_all_three_strict"
    )
    shared_examples_ok = len(shared_examples) == 17 and all_three_strict_examples == 5
    add_row(
        rows,
        "qa_gates",
        status_label(shared_examples_ok),
        "v5_shared_examples",
        len(shared_examples),
        f"all_three_strict={all_three_strict_examples}",
    )

    answer_format_summary = read_csv(args.answer_format_summary)
    answer_format_items = read_csv(args.answer_format_items)
    answer_format_ok = len(answer_format_summary) == 27 and len(answer_format_items) == 1800
    add_row(
        rows,
        "qa_gates",
        status_label(answer_format_ok),
        "v5_answer_format_audit",
        len(answer_format_items),
        f"summary_rows={len(answer_format_summary)}",
    )

    response_style_summary = read_csv(args.response_style_summary)
    response_style_items = read_csv(args.response_style_items)
    qwen3_math_bangla = next(
        row
        for row in response_style_summary
        if row["model"] == "Qwen3-4B"
        and row["dataset"] == "banglamath"
        and row["variant"] == "bangla"
    )
    qwen3_math_banglish = next(
        row
        for row in response_style_summary
        if row["model"] == "Qwen3-4B"
        and row["dataset"] == "banglamath"
        and row["variant"] == "banglish_clean"
    )
    qwen3_math_english = next(
        row
        for row in response_style_summary
        if row["model"] == "Qwen3-4B"
        and row["dataset"] == "banglamath"
        and row["variant"] == "english"
    )
    response_style_ok = (
        len(response_style_summary) == 27
        and len(response_style_items) == 1800
        and int(qwen3_math_bangla["meta_uncertainty"]) == 0
        and int(qwen3_math_banglish["meta_uncertainty"]) == 15
        and int(qwen3_math_english["meta_uncertainty"]) == 1
    )
    add_row(
        rows,
        "qa_gates",
        status_label(response_style_ok),
        "v5_response_style_drift",
        len(response_style_items),
        (
            f"summary_rows={len(response_style_summary)}; "
            f"qwen3_math_meta=bangla:{qwen3_math_bangla['meta_uncertainty']},"
            f"banglish:{qwen3_math_banglish['meta_uncertainty']},"
            f"english:{qwen3_math_english['meta_uncertainty']}"
        ),
    )

    banglamath_numeric_summary = read_csv(args.banglamath_numeric_summary)
    banglamath_numeric_items = read_csv(args.banglamath_numeric_items)
    qwen3_numeric_bangla = next(
        row
        for row in banglamath_numeric_summary
        if row["model"] == "Qwen3-4B" and row["variant"] == "bangla"
    )
    qwen3_numeric_banglish = next(
        row
        for row in banglamath_numeric_summary
        if row["model"] == "Qwen3-4B" and row["variant"] == "banglish_clean"
    )
    qwen3_numeric_english = next(
        row
        for row in banglamath_numeric_summary
        if row["model"] == "Qwen3-4B" and row["variant"] == "english"
    )
    banglamath_numeric_ok = (
        len(banglamath_numeric_summary) == 9
        and len(banglamath_numeric_items) == 504
        and int(qwen3_numeric_bangla["raw_full_numeric_signature"]) == 19
        and int(qwen3_numeric_banglish["raw_full_numeric_signature"]) == 10
        and int(qwen3_numeric_english["raw_full_numeric_signature"]) == 24
    )
    add_row(
        rows,
        "qa_gates",
        status_label(banglamath_numeric_ok),
        "v5_banglamath_numeric_sensitivity",
        len(banglamath_numeric_items),
        (
            f"summary_rows={len(banglamath_numeric_summary)}; "
            f"qwen3_raw_signature=bangla:{qwen3_numeric_bangla['raw_full_numeric_signature']},"
            f"banglish:{qwen3_numeric_banglish['raw_full_numeric_signature']},"
            f"english:{qwen3_numeric_english['raw_full_numeric_signature']}"
        ),
    )

    banglamath_transfer_summary = read_csv(args.banglamath_numeric_transfer_summary)
    banglamath_transfer_items = read_csv(args.banglamath_numeric_transfer_items)
    qwen3_transfer = next(
        row for row in banglamath_transfer_summary if row["model"] == "Qwen3-4B"
    )
    qwen25_3b_transfer = next(
        row for row in banglamath_transfer_summary if row["model"] == "Qwen2.5-3B"
    )
    qwen25_7b_transfer = next(
        row for row in banglamath_transfer_summary if row["model"] == "Qwen2.5-7B 8-bit"
    )
    banglamath_transfer_ok = (
        len(banglamath_transfer_summary) == 3
        and len(banglamath_transfer_items) == 168
        and int(qwen3_transfer["alt_raw_signature_any"]) == 24
        and int(qwen3_transfer["banglish_retains_alt_raw_signature"]) == 8
        and int(qwen3_transfer["banglish_correct_given_alt_raw_signature"]) == 2
        and int(qwen3_transfer["banglish_meta_given_alt_raw_signature"]) == 9
        and int(qwen3_transfer["banglish_wrong_without_raw_number_given_alt_raw_signature"]) == 4
        and int(qwen25_3b_transfer["alt_raw_signature_any"]) == 12
        and int(qwen25_3b_transfer["banglish_retains_alt_raw_signature"]) == 1
        and int(qwen25_7b_transfer["alt_raw_signature_any"]) == 24
        and int(qwen25_7b_transfer["banglish_retains_alt_raw_signature"]) == 4
    )
    add_row(
        rows,
        "qa_gates",
        status_label(banglamath_transfer_ok),
        "v5_banglamath_numeric_transfer",
        len(banglamath_transfer_items),
        (
            f"summary_rows={len(banglamath_transfer_summary)}; "
            f"qwen3_alt_raw={qwen3_transfer['alt_raw_signature_any']}/"
            f"{qwen3_transfer['n']}; "
            f"qwen3_banglish_retains_alt_raw="
            f"{qwen3_transfer['banglish_retains_alt_raw_signature']}/"
            f"{qwen3_transfer['alt_raw_signature_any']}; "
            f"qwen3_banglish_correct_alt_raw="
            f"{qwen3_transfer['banglish_correct_given_alt_raw_signature']}/"
            f"{qwen3_transfer['alt_raw_signature_any']}; "
            f"qwen3_meta_alt_raw={qwen3_transfer['banglish_meta_given_alt_raw_signature']}/"
            f"{qwen3_transfer['alt_raw_signature_any']}; "
            f"qwen3_no_number_wrong_alt_raw="
            f"{qwen3_transfer['banglish_wrong_without_raw_number_given_alt_raw_signature']}/"
            f"{qwen3_transfer['alt_raw_signature_any']}; "
            f"qwen25_retains_alt_raw="
            f"{qwen25_3b_transfer['banglish_retains_alt_raw_signature']}/"
            f"{qwen25_3b_transfer['alt_raw_signature_any']},"
            f"{qwen25_7b_transfer['banglish_retains_alt_raw_signature']}/"
            f"{qwen25_7b_transfer['alt_raw_signature_any']}"
        ),
    )

    choice_bias_summary = read_csv(args.choice_bias_summary)
    choice_bias_items = read_csv(args.choice_bias_items)
    choice_bias_ok = len(choice_bias_summary) == 18 and len(choice_bias_items) == 432
    add_row(
        rows,
        "qa_gates",
        status_label(choice_bias_ok),
        "v5_benqa_choice_bias",
        len(choice_bias_items),
        f"summary_rows={len(choice_bias_summary)}",
    )

    subject_option_summary = read_csv(args.subject_option_summary)
    subject_option_items = read_csv(args.subject_option_items)
    qwen3_banglish_majority_d = sum(
        1
        for row in subject_option_summary
        if row["model"] == "Qwen3-4B"
        and row["variant"] == "banglish_clean"
        and row["majority_d"] == "True"
    )
    qwen25_3b_banglish_majority_d = sum(
        1
        for row in subject_option_summary
        if row["model"] == "Qwen2.5-3B"
        and row["variant"] == "banglish_clean"
        and row["majority_d"] == "True"
    )
    qwen25_7b_banglish_majority_d = sum(
        1
        for row in subject_option_summary
        if row["model"] == "Qwen2.5-7B 8-bit"
        and row["variant"] == "banglish_clean"
        and row["majority_d"] == "True"
    )
    subject_option_ok = (
        len(subject_option_summary) == 117
        and len(subject_option_items) == 1296
        and qwen3_banglish_majority_d == 12
        and qwen25_3b_banglish_majority_d == 1
        and qwen25_7b_banglish_majority_d == 0
    )
    add_row(
        rows,
        "qa_gates",
        status_label(subject_option_ok),
        "v5_benqa_subject_option_bias",
        len(subject_option_items),
        (
            f"summary_rows={len(subject_option_summary)}; "
            f"majority_d_subjects=qwen3:{qwen3_banglish_majority_d}/13,"
            f"qwen25_3b:{qwen25_3b_banglish_majority_d}/13,"
            f"qwen25_7b:{qwen25_7b_banglish_majority_d}/13"
        ),
    )

    prediction_diversity_summary = read_csv(args.prediction_diversity_summary)
    qwen3_diversity = next(
        row
        for row in prediction_diversity_summary
        if row["section"] == "variant_diversity"
        and row["model"] == "Qwen3-4B"
        and row["variant"] == "banglish_clean"
    )
    qwen25_3b_diversity = next(
        row
        for row in prediction_diversity_summary
        if row["section"] == "variant_diversity"
        and row["model"] == "Qwen2.5-3B"
        and row["variant"] == "banglish_clean"
    )
    qwen25_7b_diversity = next(
        row
        for row in prediction_diversity_summary
        if row["section"] == "variant_diversity"
        and row["model"] == "Qwen2.5-7B 8-bit"
        and row["variant"] == "banglish_clean"
    )
    qwen3_diversity_subject = next(
        row
        for row in prediction_diversity_summary
        if row["section"] == "subject_rollup"
        and row["model"] == "Qwen3-4B"
        and row["variant"] == "banglish_clean"
    )
    prediction_diversity_ok = (
        len(prediction_diversity_summary) == 25
        and int(qwen3_diversity["pred_D"]) == 111
        and float(qwen3_diversity["normalized_entropy"]) == 0.5023
        and float(qwen3_diversity["effective_options"]) == 2.01
        and float(qwen25_3b_diversity["effective_options"]) == 3.75
        and float(qwen25_7b_diversity["effective_options"]) == 3.77
        and int(qwen3_diversity_subject["majority_d_subjects"]) == 12
        and float(qwen3_diversity_subject["mean_subject_entropy"]) == 0.4021
    )
    add_row(
        rows,
        "qa_gates",
        status_label(prediction_diversity_ok),
        "v5_benqa_prediction_diversity",
        len(prediction_diversity_summary),
        (
            f"qwen3_effective_options={qwen3_diversity['effective_options']}; "
            f"qwen3_entropy={qwen3_diversity['normalized_entropy']}; "
            f"qwen3_D={qwen3_diversity['pred_D']}/144; "
            f"qwen25_effective_options={qwen25_3b_diversity['effective_options']}/"
            f"{qwen25_7b_diversity['effective_options']}; "
            f"qwen3_majorityD_subjects={qwen3_diversity_subject['majority_d_subjects']}/13"
        ),
    )

    option_position_summary = read_csv(args.option_position_summary)
    option_position_items = read_csv(args.option_position_items)
    option_position_qwen3 = next(
        row for row in option_position_summary if row["model"] == "Qwen3-4B"
    )
    option_position_features = next(
        row for row in option_position_summary if row["section"] == "item_features"
    )
    option_position_ok = (
        len(option_position_summary) == 4
        and len(option_position_items) == 432
        and int(option_position_qwen3["pred_D_when_D_not_longest"]) == 30
        and int(option_position_qwen3["D_not_longest_n"]) == 46
        and int(option_position_features["D_longest_n"]) == 98
    )
    add_row(
        rows,
        "qa_gates",
        status_label(option_position_ok),
        "v5_benqa_option_position_content",
        len(option_position_items),
        (
            f"summary_rows={len(option_position_summary)}; "
            f"D_longest_items={option_position_features['D_longest_n']}/144; "
            f"qwen3_D_when_not_longest={option_position_qwen3['pred_D_when_D_not_longest']}/"
            f"{option_position_qwen3['D_not_longest_n']}"
        ),
    )

    option_switching_summary = read_csv(args.option_switching_summary)
    option_switching_items = read_csv(args.option_switching_items)
    qwen3_switch_bangla = next(
        row
        for row in option_switching_summary
        if row["section"] == "headline"
        and row["model"] == "Qwen3-4B"
        and row["baseline_variant"] == "bangla"
    )
    qwen3_switch_english = next(
        row
        for row in option_switching_summary
        if row["section"] == "headline"
        and row["model"] == "Qwen3-4B"
        and row["baseline_variant"] == "english"
    )
    option_switching_ok = (
        len(option_switching_summary) == 36
        and len(option_switching_items) == 864
        and int(qwen3_switch_bangla["non_d_to_D"]) == 47
        and int(qwen3_switch_bangla["baseline_non_d_n"]) == 73
        and int(qwen3_switch_english["non_d_to_D"]) == 55
        and int(qwen3_switch_english["baseline_non_d_n"]) == 78
    )
    add_row(
        rows,
        "qa_gates",
        status_label(option_switching_ok),
        "v5_benqa_option_switching",
        len(option_switching_items),
        (
            f"summary_rows={len(option_switching_summary)}; "
            f"qwen3_nonD_to_D=bangla:{qwen3_switch_bangla['non_d_to_D']}/"
            f"{qwen3_switch_bangla['baseline_non_d_n']},"
            f"english:{qwen3_switch_english['non_d_to_D']}/"
            f"{qwen3_switch_english['baseline_non_d_n']}"
        ),
    )

    cross_script_option_agreement_summary = read_csv(args.cross_script_option_agreement_summary)
    cross_script_option_agreement_items = read_csv(args.cross_script_option_agreement_items)
    qwen3_agreement_correct_non_d = next(
        row
        for row in cross_script_option_agreement_summary
        if row["model"] == "Qwen3-4B"
        and row["scope"] == "be_correct_agree_non_d"
    )
    qwen25_3b_agreement_correct_non_d = next(
        row
        for row in cross_script_option_agreement_summary
        if row["model"] == "Qwen2.5-3B"
        and row["scope"] == "be_correct_agree_non_d"
    )
    qwen25_7b_agreement_correct_non_d = next(
        row
        for row in cross_script_option_agreement_summary
        if row["model"] == "Qwen2.5-7B 8-bit"
        and row["scope"] == "be_correct_agree_non_d"
    )
    qwen3_agreement_non_d = next(
        row
        for row in cross_script_option_agreement_summary
        if row["model"] == "Qwen3-4B"
        and row["scope"] == "be_agree_non_d"
    )
    qwen3_agreement_all = next(
        row
        for row in cross_script_option_agreement_summary
        if row["model"] == "Qwen3-4B"
        and row["scope"] == "be_agree"
    )
    cross_script_option_agreement_ok = (
        len(cross_script_option_agreement_summary) == 21
        and len(cross_script_option_agreement_items) == 432
        and int(qwen3_agreement_correct_non_d["banglish_wrong_D"]) == 23
        and int(qwen3_agreement_correct_non_d["n"]) == 36
        and int(qwen25_3b_agreement_correct_non_d["banglish_wrong_D"]) == 2
        and int(qwen25_3b_agreement_correct_non_d["n"]) == 23
        and int(qwen25_7b_agreement_correct_non_d["banglish_wrong_D"]) == 7
        and int(qwen25_7b_agreement_correct_non_d["n"]) == 44
        and int(qwen3_agreement_non_d["banglish_D"]) == 30
        and int(qwen3_agreement_non_d["n"]) == 47
        and int(qwen3_agreement_all["banglish_D"]) == 72
        and int(qwen3_agreement_all["n"]) == 92
    )
    add_row(
        rows,
        "qa_gates",
        status_label(cross_script_option_agreement_ok),
        "v5_benqa_cross_script_option_agreement",
        len(cross_script_option_agreement_items),
        (
            f"summary_rows={len(cross_script_option_agreement_summary)}; "
            f"qwen3_correct_BE_agree_nonD_wrongD="
            f"{qwen3_agreement_correct_non_d['banglish_wrong_D']}/"
            f"{qwen3_agreement_correct_non_d['n']}; "
            f"qwen25_wrongD={qwen25_3b_agreement_correct_non_d['banglish_wrong_D']}/"
            f"{qwen25_3b_agreement_correct_non_d['n']},"
            f"{qwen25_7b_agreement_correct_non_d['banglish_wrong_D']}/"
            f"{qwen25_7b_agreement_correct_non_d['n']}; "
            f"qwen3_BE_agree_nonD_D={qwen3_agreement_non_d['banglish_D']}/"
            f"{qwen3_agreement_non_d['n']}; "
            f"qwen3_BE_agree_D={qwen3_agreement_all['banglish_D']}/"
            f"{qwen3_agreement_all['n']}"
        ),
    )

    cross_model_banglish_agreement_summary = read_csv(args.cross_model_banglish_agreement_summary)
    cross_model_banglish_agreement_items = read_csv(args.cross_model_banglish_agreement_items)
    q25_agree_non_d = next(
        row
        for row in cross_model_banglish_agreement_summary
        if row["scope"] == "q25_agree_non_d"
    )
    q25_correct_agree_non_d = next(
        row
        for row in cross_model_banglish_agreement_summary
        if row["scope"] == "q25_correct_agree_non_d"
    )
    q25_correct_agree_d = next(
        row
        for row in cross_model_banglish_agreement_summary
        if row["scope"] == "q25_correct_agree_d"
    )
    cross_model_banglish_agreement_ok = (
        len(cross_model_banglish_agreement_summary) == 8
        and len(cross_model_banglish_agreement_items) == 144
        and int(q25_agree_non_d["n"]) == 42
        and int(q25_agree_non_d["qwen3_D"]) == 26
        and int(q25_agree_non_d["qwen3_wrong_D"]) == 18
        and int(q25_correct_agree_non_d["n"]) == 15
        and int(q25_correct_agree_non_d["qwen3_wrong_D"]) == 8
        and int(q25_correct_agree_non_d["qwen3_same_as_q25_agreement"]) == 4
        and int(q25_correct_agree_d["n"]) == 7
        and int(q25_correct_agree_d["qwen3_D"]) == 7
    )
    add_row(
        rows,
        "qa_gates",
        status_label(cross_model_banglish_agreement_ok),
        "v5_benqa_cross_model_banglish_agreement",
        len(cross_model_banglish_agreement_items),
        (
            f"summary_rows={len(cross_model_banglish_agreement_summary)}; "
            f"q25_agree_nonD_qwen3_D={q25_agree_non_d['qwen3_D']}/"
            f"{q25_agree_non_d['n']}; "
            f"q25_agree_nonD_qwen3_wrongD={q25_agree_non_d['qwen3_wrong_D']}/"
            f"{q25_agree_non_d['n']}; "
            f"q25_correct_nonD_qwen3_wrongD="
            f"{q25_correct_agree_non_d['qwen3_wrong_D']}/"
            f"{q25_correct_agree_non_d['n']}; "
            f"q25_correct_nonD_qwen3_same="
            f"{q25_correct_agree_non_d['qwen3_same_as_q25_agreement']}/"
            f"{q25_correct_agree_non_d['n']}; "
            f"q25_correct_D_qwen3_D={q25_correct_agree_d['qwen3_D']}/"
            f"{q25_correct_agree_d['n']}"
        ),
    )

    order_confound_summary = read_csv(args.order_confound_summary)
    order_confound_items = read_csv(args.order_confound_items)
    qwen3_run_q1 = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["section"] == "order_quartile"
        and row["axis"] == "run_line"
        and row["bucket"] == "q1"
    )
    qwen3_run_q2 = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["section"] == "order_quartile"
        and row["axis"] == "run_line"
        and row["bucket"] == "q2"
    )
    qwen3_run_q3 = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["section"] == "order_quartile"
        and row["axis"] == "run_line"
        and row["bucket"] == "q3"
    )
    qwen3_run_q4 = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["section"] == "order_quartile"
        and row["axis"] == "run_line"
        and row["bucket"] == "q4"
    )
    qwen3_order_sequence = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["section"] == "run_sequence"
        and row["axis"] == "run_line"
    )
    qwen25_3b_order_sequence = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen2.5-3B"
        and row["section"] == "run_sequence"
        and row["axis"] == "run_line"
    )
    qwen25_7b_order_sequence = next(
        row
        for row in order_confound_summary
        if row["model"] == "Qwen2.5-7B 8-bit"
        and row["section"] == "run_sequence"
        and row["axis"] == "run_line"
    )
    order_confound_ok = (
        len(order_confound_summary) == 39
        and len(order_confound_items) == 432
        and int(qwen3_run_q1["banglish_D"]) == 26
        and int(qwen3_run_q1["banglish_wrong_D"]) == 20
        and int(qwen3_run_q2["banglish_D"]) == 31
        and int(qwen3_run_q3["banglish_D"]) == 28
        and int(qwen3_run_q4["banglish_D"]) == 26
        and int(qwen3_run_q4["banglish_wrong_D"]) == 19
        and int(qwen3_order_sequence["banglish_D"]) == 111
        and int(qwen3_order_sequence["d_run_count"]) == 23
        and int(qwen3_order_sequence["longest_d_run"]) == 13
        and int(qwen25_3b_order_sequence["banglish_D"]) == 39
        and int(qwen25_3b_order_sequence["longest_d_run"]) == 3
        and int(qwen25_7b_order_sequence["banglish_D"]) == 25
        and int(qwen25_7b_order_sequence["longest_d_run"]) == 2
    )
    add_row(
        rows,
        "qa_gates",
        status_label(order_confound_ok),
        "v5_benqa_order_confound",
        len(order_confound_items),
        (
            f"summary_rows={len(order_confound_summary)}; "
            f"qwen3_run_quartile_D={qwen3_run_q1['banglish_D']}/"
            f"{qwen3_run_q1['n']},{qwen3_run_q2['banglish_D']}/"
            f"{qwen3_run_q2['n']},{qwen3_run_q3['banglish_D']}/"
            f"{qwen3_run_q3['n']},{qwen3_run_q4['banglish_D']}/"
            f"{qwen3_run_q4['n']}; "
            f"qwen3_wrongD_q1_q4={qwen3_run_q1['banglish_wrong_D']}/"
            f"{qwen3_run_q1['n']},{qwen3_run_q4['banglish_wrong_D']}/"
            f"{qwen3_run_q4['n']}; "
            f"qwen3_D_runs={qwen3_order_sequence['d_run_count']}; "
            f"qwen3_longest_D_run={qwen3_order_sequence['longest_d_run']}; "
            f"qwen25_longest_D_run={qwen25_3b_order_sequence['longest_d_run']},"
            f"{qwen25_7b_order_sequence['longest_d_run']}"
        ),
    )

    review_label_option_summary = read_csv(args.review_label_option_summary)
    review_label_option_items = read_csv(args.review_label_option_items)
    qwen3_review_label_unreviewed = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen3-4B" and row["bucket"] == "unreviewed"
    )
    qwen3_review_label_minor = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen3-4B" and row["bucket"] == "minor_edit"
    )
    qwen3_review_label_nonbad = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen3-4B" and row["bucket"] == "reviewed_nonbad"
    )
    qwen25_3b_review_label_unreviewed = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen2.5-3B" and row["bucket"] == "unreviewed"
    )
    qwen25_7b_review_label_unreviewed = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen2.5-7B 8-bit" and row["bucket"] == "unreviewed"
    )
    qwen25_3b_review_label_nonbad = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen2.5-3B" and row["bucket"] == "reviewed_nonbad"
    )
    qwen25_7b_review_label_nonbad = next(
        row
        for row in review_label_option_summary
        if row["model"] == "Qwen2.5-7B 8-bit" and row["bucket"] == "reviewed_nonbad"
    )
    review_label_option_ok = (
        len(review_label_option_summary) == 24
        and len(review_label_option_items) == 432
        and int(qwen3_review_label_unreviewed["n"]) == 51
        and int(qwen3_review_label_unreviewed["gold_D"]) == 13
        and int(qwen3_review_label_unreviewed["banglish_D"]) == 39
        and int(qwen3_review_label_unreviewed["banglish_wrong_D"]) == 28
        and int(qwen3_review_label_minor["n"]) == 88
        and int(qwen3_review_label_minor["banglish_D"]) == 67
        and int(qwen3_review_label_minor["banglish_wrong_D"]) == 45
        and int(qwen3_review_label_nonbad["n"]) == 90
        and int(qwen3_review_label_nonbad["banglish_D"]) == 69
        and int(qwen3_review_label_nonbad["banglish_wrong_D"]) == 47
        and int(qwen25_3b_review_label_unreviewed["banglish_D"]) == 10
        and int(qwen25_7b_review_label_unreviewed["banglish_D"]) == 7
        and int(qwen25_3b_review_label_nonbad["banglish_D"]) == 28
        and int(qwen25_7b_review_label_nonbad["banglish_D"]) == 17
    )
    add_row(
        rows,
        "qa_gates",
        status_label(review_label_option_ok),
        "v5_benqa_review_label_option_bias",
        len(review_label_option_items),
        (
            f"summary_rows={len(review_label_option_summary)}; "
            f"qwen3_unreviewed_D={qwen3_review_label_unreviewed['banglish_D']}/"
            f"{qwen3_review_label_unreviewed['n']}; "
            f"qwen3_unreviewed_wrongD={qwen3_review_label_unreviewed['banglish_wrong_D']}/"
            f"{qwen3_review_label_unreviewed['n']}; "
            f"qwen3_minor_D={qwen3_review_label_minor['banglish_D']}/"
            f"{qwen3_review_label_minor['n']}; "
            f"qwen3_reviewed_nonbad_D={qwen3_review_label_nonbad['banglish_D']}/"
            f"{qwen3_review_label_nonbad['n']}; "
            f"qwen25_unreviewed_D={qwen25_3b_review_label_unreviewed['banglish_D']}/"
            f"{qwen25_3b_review_label_unreviewed['n']},"
            f"{qwen25_7b_review_label_unreviewed['banglish_D']}/"
            f"{qwen25_7b_review_label_unreviewed['n']}; "
            f"qwen25_reviewed_nonbad_D={qwen25_3b_review_label_nonbad['banglish_D']}/"
            f"{qwen25_3b_review_label_nonbad['n']},"
            f"{qwen25_7b_review_label_nonbad['banglish_D']}/"
            f"{qwen25_7b_review_label_nonbad['n']}"
        ),
    )

    length_token_summary = read_csv(args.length_token_confound_summary)
    length_token_items = read_csv(args.length_token_confound_items)

    def length_token_row(model: str, metric: str, quartile: str) -> dict[str, str]:
        return next(
            row
            for row in length_token_summary
            if row["model"] == model and row["metric"] == metric and row["quartile"] == quartile
        )

    qwen3_token_q1 = length_token_row("Qwen3-4B", "banglish_hf_tokens", "q1")
    qwen3_token_q2 = length_token_row("Qwen3-4B", "banglish_hf_tokens", "q2")
    qwen3_token_q3 = length_token_row("Qwen3-4B", "banglish_hf_tokens", "q3")
    qwen3_token_q4 = length_token_row("Qwen3-4B", "banglish_hf_tokens", "q4")
    qwen3_char_q1 = length_token_row("Qwen3-4B", "banglish_chars", "q1")
    qwen3_char_q4 = length_token_row("Qwen3-4B", "banglish_chars", "q4")
    qwen3_density_q1 = length_token_row(
        "Qwen3-4B", "banglish_hf_tokens_per_word", "q1"
    )
    qwen3_density_q4 = length_token_row(
        "Qwen3-4B", "banglish_hf_tokens_per_word", "q4"
    )
    qwen25_3b_token_q1 = length_token_row("Qwen2.5-3B", "banglish_hf_tokens", "q1")
    qwen25_3b_token_q4 = length_token_row("Qwen2.5-3B", "banglish_hf_tokens", "q4")
    qwen25_7b_token_q1 = length_token_row(
        "Qwen2.5-7B 8-bit", "banglish_hf_tokens", "q1"
    )
    qwen25_7b_token_q4 = length_token_row(
        "Qwen2.5-7B 8-bit", "banglish_hf_tokens", "q4"
    )
    length_token_ok = (
        len(length_token_summary) == 48
        and len(length_token_items) == 432
        and int(qwen3_token_q1["n"]) == 36
        and int(qwen3_token_q1["banglish_D"]) == 32
        and int(qwen3_token_q1["banglish_wrong_D"]) == 26
        and int(qwen3_token_q2["n"]) == 36
        and int(qwen3_token_q2["banglish_D"]) == 26
        and int(qwen3_token_q2["banglish_wrong_D"]) == 17
        and int(qwen3_token_q3["n"]) == 36
        and int(qwen3_token_q3["banglish_D"]) == 27
        and int(qwen3_token_q3["banglish_wrong_D"]) == 15
        and int(qwen3_token_q4["n"]) == 36
        and int(qwen3_token_q4["banglish_D"]) == 26
        and int(qwen3_token_q4["banglish_wrong_D"]) == 19
        and int(qwen3_char_q1["banglish_D"]) == 31
        and int(qwen3_char_q4["banglish_D"]) == 29
        and int(qwen3_density_q1["banglish_D"]) == 33
        and int(qwen3_density_q4["banglish_D"]) == 22
        and int(qwen25_3b_token_q1["banglish_D"]) == 5
        and int(qwen25_3b_token_q4["banglish_D"]) == 14
        and int(qwen25_7b_token_q1["banglish_D"]) == 1
        and int(qwen25_7b_token_q4["banglish_D"]) == 9
    )
    add_row(
        rows,
        "qa_gates",
        status_label(length_token_ok),
        "v5_benqa_length_token_confound",
        len(length_token_items),
        (
            f"summary_rows={len(length_token_summary)}; "
            f"qwen3_token_quartile_D={qwen3_token_q1['banglish_D']}/"
            f"{qwen3_token_q1['n']},{qwen3_token_q2['banglish_D']}/"
            f"{qwen3_token_q2['n']},{qwen3_token_q3['banglish_D']}/"
            f"{qwen3_token_q3['n']},{qwen3_token_q4['banglish_D']}/"
            f"{qwen3_token_q4['n']}; "
            f"qwen3_token_wrongD={qwen3_token_q1['banglish_wrong_D']}/"
            f"{qwen3_token_q1['n']},{qwen3_token_q2['banglish_wrong_D']}/"
            f"{qwen3_token_q2['n']},{qwen3_token_q3['banglish_wrong_D']}/"
            f"{qwen3_token_q3['n']},{qwen3_token_q4['banglish_wrong_D']}/"
            f"{qwen3_token_q4['n']}; "
            f"qwen3_char_q1_q4_D={qwen3_char_q1['banglish_D']}/"
            f"{qwen3_char_q1['n']},{qwen3_char_q4['banglish_D']}/"
            f"{qwen3_char_q4['n']}; "
            f"qwen3_density_q1_q4_D={qwen3_density_q1['banglish_D']}/"
            f"{qwen3_density_q1['n']},{qwen3_density_q4['banglish_D']}/"
            f"{qwen3_density_q4['n']}; "
            f"qwen25_token_q1_q4_D={qwen25_3b_token_q1['banglish_D']}/"
            f"{qwen25_3b_token_q1['n']},{qwen25_3b_token_q4['banglish_D']}/"
            f"{qwen25_3b_token_q4['n']};"
            f"{qwen25_7b_token_q1['banglish_D']}/"
            f"{qwen25_7b_token_q1['n']},{qwen25_7b_token_q4['banglish_D']}/"
            f"{qwen25_7b_token_q4['n']}"
        ),
    )

    option_coverage_summary = read_csv(args.option_coverage_confound_summary)
    option_coverage_items = read_csv(args.option_coverage_confound_items)

    def option_coverage_row(model: str, bucket: str) -> dict[str, str]:
        return next(
            row
            for row in option_coverage_summary
            if row["model"] == model and row["bucket"] == bucket
        )

    qwen3_coverage_tie = option_coverage_row("Qwen3-4B", "all_options_same_coverage")
    qwen25_3b_coverage_tie = option_coverage_row(
        "Qwen2.5-3B", "all_options_same_coverage"
    )
    qwen25_7b_coverage_tie = option_coverage_row(
        "Qwen2.5-7B 8-bit", "all_options_same_coverage"
    )
    qwen3_coverage_not_highest = option_coverage_row(
        "Qwen3-4B", "d_not_highest_coverage"
    )
    qwen25_3b_coverage_not_highest = option_coverage_row(
        "Qwen2.5-3B", "d_not_highest_coverage"
    )
    qwen25_7b_coverage_not_highest = option_coverage_row(
        "Qwen2.5-7B 8-bit", "d_not_highest_coverage"
    )
    qwen3_coverage_strict_highest = option_coverage_row(
        "Qwen3-4B", "d_strict_highest_coverage"
    )
    option_coverage_ok = (
        len(option_coverage_summary) == 21
        and len(option_coverage_items) == 432
        and int(qwen3_coverage_tie["n"]) == 101
        and int(qwen3_coverage_tie["banglish_D"]) == 76
        and int(qwen3_coverage_tie["banglish_wrong_D"]) == 52
        and int(qwen25_3b_coverage_tie["banglish_D"]) == 14
        and int(qwen25_7b_coverage_tie["banglish_D"]) == 8
        and int(qwen3_coverage_not_highest["n"]) == 35
        and int(qwen3_coverage_not_highest["banglish_D"]) == 31
        and int(qwen3_coverage_not_highest["banglish_wrong_D"]) == 23
        and int(qwen25_3b_coverage_not_highest["banglish_D"]) == 22
        and int(qwen25_7b_coverage_not_highest["banglish_D"]) == 15
        and int(qwen3_coverage_strict_highest["n"]) == 3
        and int(qwen3_coverage_strict_highest["banglish_D"]) == 1
    )
    add_row(
        rows,
        "qa_gates",
        status_label(option_coverage_ok),
        "v5_benqa_option_coverage_confound",
        len(option_coverage_items),
        (
            f"summary_rows={len(option_coverage_summary)}; "
            f"qwen3_tied_coverage_D={qwen3_coverage_tie['banglish_D']}/"
            f"{qwen3_coverage_tie['n']}; "
            f"qwen3_tied_coverage_wrongD={qwen3_coverage_tie['banglish_wrong_D']}/"
            f"{qwen3_coverage_tie['n']}; "
            f"qwen25_tied_coverage_D={qwen25_3b_coverage_tie['banglish_D']}/"
            f"{qwen25_3b_coverage_tie['n']},"
            f"{qwen25_7b_coverage_tie['banglish_D']}/"
            f"{qwen25_7b_coverage_tie['n']}; "
            f"qwen3_D_not_highest_coverage={qwen3_coverage_not_highest['banglish_D']}/"
            f"{qwen3_coverage_not_highest['n']}; "
            f"qwen3_wrongD_not_highest_coverage="
            f"{qwen3_coverage_not_highest['banglish_wrong_D']}/"
            f"{qwen3_coverage_not_highest['n']}; "
            f"qwen25_D_not_highest_coverage="
            f"{qwen25_3b_coverage_not_highest['banglish_D']}/"
            f"{qwen25_3b_coverage_not_highest['n']},"
            f"{qwen25_7b_coverage_not_highest['banglish_D']}/"
            f"{qwen25_7b_coverage_not_highest['n']}; "
            f"qwen3_D_strict_highest_coverage="
            f"{qwen3_coverage_strict_highest['banglish_D']}/"
            f"{qwen3_coverage_strict_highest['n']}"
        ),
    )

    switch_confound_summary = read_csv(args.switch_confound_summary)
    switch_confound_items = read_csv(args.switch_confound_items)
    qwen3_confound_bangla = next(
        row
        for row in switch_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["baseline_variant"] == "bangla"
        and row["scope"] == "correct_non_d_d_not_longest"
    )
    qwen3_confound_english = next(
        row
        for row in switch_confound_summary
        if row["model"] == "Qwen3-4B"
        and row["baseline_variant"] == "english"
        and row["scope"] == "correct_non_d_d_not_longest"
    )
    switch_confound_ok = (
        len(switch_confound_summary) == 36
        and len(switch_confound_items) == 864
        and int(qwen3_confound_bangla["correct_non_d_to_wrong_D"]) == 11
        and int(qwen3_confound_bangla["n"]) == 19
        and int(qwen3_confound_english["correct_non_d_to_wrong_D"]) == 12
        and int(qwen3_confound_english["n"]) == 21
    )
    add_row(
        rows,
        "qa_gates",
        status_label(switch_confound_ok),
        "v5_benqa_option_switch_confound",
        len(switch_confound_items),
        (
            f"summary_rows={len(switch_confound_summary)}; "
            f"qwen3_correct_nonD_D_not_longest_wrongD=bangla:"
            f"{qwen3_confound_bangla['correct_non_d_to_wrong_D']}/"
            f"{qwen3_confound_bangla['n']},english:"
            f"{qwen3_confound_english['correct_non_d_to_wrong_D']}/"
            f"{qwen3_confound_english['n']}"
        ),
    )

    semantic_cue_summary = read_csv(args.semantic_cue_summary)
    semantic_cue_items = read_csv(args.semantic_cue_items)
    semantic_features = next(
        row for row in semantic_cue_summary if row["section"] == "item_features"
    )
    qwen3_semantic_no_cue = next(
        row
        for row in semantic_cue_summary
        if row["section"] == "model_cue_bucket"
        and row["model"] == "Qwen3-4B"
        and row["scope"] == "D_no_semantic_cue"
    )
    qwen3_semantic_bangla = next(
        row
        for row in semantic_cue_summary
        if row["section"] == "switch_cue_bucket"
        and row["model"] == "Qwen3-4B"
        and row["baseline_variant"] == "bangla"
        and row["scope"] == "correct_non_d_D_no_semantic_cue"
    )
    qwen3_semantic_english = next(
        row
        for row in semantic_cue_summary
        if row["section"] == "switch_cue_bucket"
        and row["model"] == "Qwen3-4B"
        and row["baseline_variant"] == "english"
        and row["scope"] == "correct_non_d_D_no_semantic_cue"
    )
    semantic_cue_ok = (
        len(semantic_cue_summary) == 25
        and len(semantic_cue_items) == 432
        and int(semantic_features["D_no_semantic_cue"]) == 47
        and int(qwen3_semantic_no_cue["pred_D"]) == 38
        and int(qwen3_semantic_no_cue["n"]) == 47
        and int(qwen3_semantic_bangla["correct_non_d_to_wrong_D"]) == 15
        and int(qwen3_semantic_bangla["n"]) == 18
        and int(qwen3_semantic_english["correct_non_d_to_wrong_D"]) == 18
        and int(qwen3_semantic_english["n"]) == 23
    )
    add_row(
        rows,
        "qa_gates",
        status_label(semantic_cue_ok),
        "v5_benqa_option_semantic_cues",
        len(semantic_cue_items),
        (
            f"summary_rows={len(semantic_cue_summary)}; "
            f"D_no_cue={semantic_features['D_no_semantic_cue']}/144; "
            f"qwen3_D_no_cue={qwen3_semantic_no_cue['pred_D']}/"
            f"{qwen3_semantic_no_cue['n']}; "
            f"qwen3_correct_nonD_no_cue_wrongD=bangla:"
            f"{qwen3_semantic_bangla['correct_non_d_to_wrong_D']}/"
            f"{qwen3_semantic_bangla['n']},english:"
            f"{qwen3_semantic_english['correct_non_d_to_wrong_D']}/"
            f"{qwen3_semantic_english['n']}"
        ),
    )

    multiconfound_summary = read_csv(args.multiconfound_residual_summary)
    multiconfound_items = read_csv(args.multiconfound_residual_items)

    def multiconfound_row(
        section: str,
        model: str,
        scope: str,
        baseline: str = "",
    ) -> dict[str, str]:
        return next(
            row
            for row in multiconfound_summary
            if row["section"] == section
            and row["model"] == model
            and row["scope"] == scope
            and row["baseline_variant"] == baseline
        )

    qwen3_multi_primary = multiconfound_row(
        "choice_scope", "Qwen3-4B", "residual_primary"
    )
    qwen25_3b_multi_primary = multiconfound_row(
        "choice_scope", "Qwen2.5-3B", "residual_primary"
    )
    qwen25_7b_multi_primary = multiconfound_row(
        "choice_scope", "Qwen2.5-7B 8-bit", "residual_primary"
    )
    qwen3_multi_tied = multiconfound_row(
        "choice_scope", "Qwen3-4B", "residual_tied_coverage"
    )
    qwen3_multi_bangla_switch = multiconfound_row(
        "switch_scope",
        "Qwen3-4B",
        "baseline_correct_non_D_residual_primary",
        "bangla",
    )
    qwen3_multi_english_switch = multiconfound_row(
        "switch_scope",
        "Qwen3-4B",
        "baseline_correct_non_D_residual_primary",
        "english",
    )
    qwen25_3b_multi_bangla_switch = multiconfound_row(
        "switch_scope",
        "Qwen2.5-3B",
        "baseline_correct_non_D_residual_primary",
        "bangla",
    )
    qwen25_7b_multi_bangla_switch = multiconfound_row(
        "switch_scope",
        "Qwen2.5-7B 8-bit",
        "baseline_correct_non_D_residual_primary",
        "bangla",
    )
    qwen25_3b_multi_english_switch = multiconfound_row(
        "switch_scope",
        "Qwen2.5-3B",
        "baseline_correct_non_D_residual_primary",
        "english",
    )
    qwen25_7b_multi_english_switch = multiconfound_row(
        "switch_scope",
        "Qwen2.5-7B 8-bit",
        "baseline_correct_non_D_residual_primary",
        "english",
    )
    multiconfound_ok = (
        len(multiconfound_summary) == 36
        and len(multiconfound_items) == 432
        and int(qwen3_multi_primary["n"]) == 24
        and int(qwen3_multi_primary["banglish_wrong_D"]) == 19
        and int(qwen25_3b_multi_primary["banglish_wrong_D"]) == 4
        and int(qwen25_7b_multi_primary["banglish_wrong_D"]) == 1
        and int(qwen3_multi_tied["n"]) == 20
        and int(qwen3_multi_tied["banglish_wrong_D"]) == 16
        and int(qwen3_multi_bangla_switch["n"]) == 13
        and int(qwen3_multi_bangla_switch["correct_non_D_to_wrong_D"]) == 11
        and int(qwen3_multi_english_switch["n"]) == 14
        and int(qwen3_multi_english_switch["correct_non_D_to_wrong_D"]) == 11
        and int(qwen25_3b_multi_bangla_switch["correct_non_D_to_wrong_D"]) == 1
        and int(qwen25_7b_multi_bangla_switch["correct_non_D_to_wrong_D"]) == 1
        and int(qwen25_3b_multi_english_switch["correct_non_D_to_wrong_D"]) == 1
        and int(qwen25_7b_multi_english_switch["correct_non_D_to_wrong_D"]) == 0
    )
    add_row(
        rows,
        "qa_gates",
        status_label(multiconfound_ok),
        "v5_benqa_multiconfound_residual",
        len(multiconfound_items),
        (
            f"summary_rows={len(multiconfound_summary)}; "
            f"qwen3_primary_wrongD={qwen3_multi_primary['banglish_wrong_D']}/"
            f"{qwen3_multi_primary['n']}; "
            f"qwen25_primary_wrongD={qwen25_3b_multi_primary['banglish_wrong_D']}/"
            f"{qwen25_3b_multi_primary['n']},"
            f"{qwen25_7b_multi_primary['banglish_wrong_D']}/"
            f"{qwen25_7b_multi_primary['n']}; "
            f"qwen3_tied_wrongD={qwen3_multi_tied['banglish_wrong_D']}/"
            f"{qwen3_multi_tied['n']}; "
            f"qwen3_correct_nonD_residual_wrongD=bangla:"
            f"{qwen3_multi_bangla_switch['correct_non_D_to_wrong_D']}/"
            f"{qwen3_multi_bangla_switch['n']},english:"
            f"{qwen3_multi_english_switch['correct_non_D_to_wrong_D']}/"
            f"{qwen3_multi_english_switch['n']}; "
            f"qwen25_correct_nonD_residual_wrongD=bangla:"
            f"{qwen25_3b_multi_bangla_switch['correct_non_D_to_wrong_D']}/"
            f"{qwen25_3b_multi_bangla_switch['n']},"
            f"{qwen25_7b_multi_bangla_switch['correct_non_D_to_wrong_D']}/"
            f"{qwen25_7b_multi_bangla_switch['n']};english:"
            f"{qwen25_3b_multi_english_switch['correct_non_D_to_wrong_D']}/"
            f"{qwen25_3b_multi_english_switch['n']},"
            f"{qwen25_7b_multi_english_switch['correct_non_D_to_wrong_D']}/"
            f"{qwen25_7b_multi_english_switch['n']}"
        ),
    )

    option_permutation_summary = read_csv(args.option_permutation_summary)
    option_permutation_items = read_csv(args.option_permutation_items)
    qwen3_permutation = next(
        row
        for row in option_permutation_summary
        if row["section"] == "headline" and row["model"] == "Qwen3-4B"
    )
    qwen25_permutation = next(
        row
        for row in option_permutation_summary
        if row["section"] == "headline" and row["model"] == "Qwen2.5-3B"
    )
    option_permutation_ok = (
        len(option_permutation_summary) == 10
        and len(option_permutation_items) == 288
        and int(qwen3_permutation["valid_options"]) == 139
        and int(qwen3_permutation["identity_pred_D"]) == 26
        and int(qwen3_permutation["identity_wrong_D"]) == 15
        and int(qwen3_permutation["identity_D_label_persistence"]) == 60
        and int(qwen3_permutation["identity_D_rotated_rows"]) == 78
        and int(qwen3_permutation["identity_D_semantic_persistence"]) == 9
        and int(qwen3_permutation["identity_wrong_D_label_persistence"]) == 35
        and int(qwen3_permutation["identity_wrong_D_rotated_rows"]) == 45
        and int(qwen3_permutation["identity_wrong_D_semantic_persistence"]) == 6
        and int(qwen25_permutation["identity_wrong_D_label_persistence"]) == 5
        and int(qwen25_permutation["identity_wrong_D_rotated_rows"]) == 21
        and int(qwen25_permutation["identity_wrong_D_semantic_persistence"]) == 12
    )
    add_row(
        rows,
        "qa_gates",
        status_label(option_permutation_ok),
        "v5_benqa_option_permutation_probe",
        len(option_permutation_items),
        (
            f"summary_rows={len(option_permutation_summary)}; "
            f"qwen3_wrongD_rotated=labelD:"
            f"{qwen3_permutation['identity_wrong_D_label_persistence']}/"
            f"{qwen3_permutation['identity_wrong_D_rotated_rows']},"
            f"semanticD:{qwen3_permutation['identity_wrong_D_semantic_persistence']}/"
            f"{qwen3_permutation['identity_wrong_D_rotated_rows']}; "
            f"qwen25_wrongD_rotated=labelD:"
            f"{qwen25_permutation['identity_wrong_D_label_persistence']}/"
            f"{qwen25_permutation['identity_wrong_D_rotated_rows']},"
            f"semanticD:{qwen25_permutation['identity_wrong_D_semantic_persistence']}/"
            f"{qwen25_permutation['identity_wrong_D_rotated_rows']}"
        ),
    )

    bnsentmix_summary = read_csv(args.bnsentmix_summary)
    bnsentmix_items = read_csv(args.bnsentmix_items)
    qwen3_bnsentmix = next(
        row
        for row in bnsentmix_summary
        if row["section"] == "headline" and row["model"] == "Qwen3-4B"
    )
    qwen25_bnsentmix = next(
        row
        for row in bnsentmix_summary
        if row["section"] == "headline" and row["model"] == "Qwen2.5-3B"
    )
    qwen25_7b_bnsentmix = next(
        row
        for row in bnsentmix_summary
        if row["section"] == "headline" and row["model"] == "Qwen2.5-7B 8-bit"
    )
    bnsentmix_ok = (
        len(bnsentmix_summary) == 75
        and len(bnsentmix_items) == 600
        and int(qwen25_bnsentmix["n"]) == 200
        and int(qwen25_bnsentmix["valid_outputs"]) == 200
        and int(qwen25_bnsentmix["correct"]) == 89
        and int(qwen25_7b_bnsentmix["n"]) == 200
        and int(qwen25_7b_bnsentmix["valid_outputs"]) == 200
        and int(qwen25_7b_bnsentmix["correct"]) == 98
        and int(qwen3_bnsentmix["n"]) == 200
        and int(qwen3_bnsentmix["valid_outputs"]) == 200
        and int(qwen3_bnsentmix["correct"]) == 99
    )
    add_row(
        rows,
        "qa_gates",
        status_label(bnsentmix_ok),
        "bnsentmix_external_validation",
        len(bnsentmix_items),
        (
            f"summary_rows={len(bnsentmix_summary)}; "
            f"qwen25={qwen25_bnsentmix['correct']}/{qwen25_bnsentmix['n']},"
            f"macro_f1={float(qwen25_bnsentmix['macro_f1']):.3f}; "
            f"qwen25_7b={qwen25_7b_bnsentmix['correct']}/{qwen25_7b_bnsentmix['n']},"
            f"macro_f1={float(qwen25_7b_bnsentmix['macro_f1']):.3f}; "
            f"qwen3={qwen3_bnsentmix['correct']}/{qwen3_bnsentmix['n']},"
            f"macro_f1={float(qwen3_bnsentmix['macro_f1']):.3f}; "
            "valid_outputs=600/600"
        ),
    )

    bnsentmix_complementarity_items = read_csv(args.bnsentmix_complementarity_items)
    bnsentmix_complementarity_summary = read_csv(args.bnsentmix_complementarity_summary)
    bnsentmix_oracle = next(
        row
        for row in bnsentmix_complementarity_summary
        if row["section"] == "triad_oracle" and row["metric"] == "any_model_oracle"
    )
    bnsentmix_oracle_delta = next(
        row
        for row in bnsentmix_complementarity_summary
        if row["section"] == "triad_oracle" and row["metric"] == "oracle_minus_best_single"
    )
    bnsentmix_majority_7b = next(
        row
        for row in bnsentmix_complementarity_summary
        if row["section"] == "majority_vote"
        and row["metric"] == "majority_with_Qwen2.5-7B 8-bit_fallback"
    )
    bnsentmix_complementarity_ok = (
        len(bnsentmix_complementarity_items) == 200
        and len(bnsentmix_complementarity_summary) == 23
        and int(bnsentmix_oracle["correct"]) == 154
        and int(bnsentmix_oracle["n"]) == 200
        and int(bnsentmix_oracle_delta["best_single_correct"]) == 99
        and int(bnsentmix_oracle_delta["oracle_correct"]) == 154
        and round(float(bnsentmix_oracle_delta["delta_oracle_minus_best_single"]), 3) == 0.275
        and int(bnsentmix_majority_7b["correct"]) == 106
    )
    add_row(
        rows,
        "qa_gates",
        status_label(bnsentmix_complementarity_ok),
        "bnsentmix_model_complementarity",
        len(bnsentmix_complementarity_items),
        (
            f"summary_rows={len(bnsentmix_complementarity_summary)}; "
            f"any_model_oracle={bnsentmix_oracle['correct']}/{bnsentmix_oracle['n']}; "
            f"oracle_minus_best={float(bnsentmix_oracle_delta['delta_oracle_minus_best_single']) * 100:+.1f}pts; "
            f"majority_7b_fallback={bnsentmix_majority_7b['correct']}/{bnsentmix_majority_7b['n']}"
        ),
    )

    bnsentmix_routing_candidates = read_csv(args.bnsentmix_routing_candidates)
    bnsentmix_routing_summary = read_csv(args.bnsentmix_routing_summary)
    bnsentmix_routing_pilot = next(
        row
        for row in bnsentmix_routing_summary
        if row["section"] == "pilot_devtest" and row["metric"] == "pilot40_selected_rule"
    )
    bnsentmix_routing_hash5 = next(
        row
        for row in bnsentmix_routing_summary
        if row["section"] == "cv_overall" and row["metric"] == "hash5"
    )
    bnsentmix_routing_block40 = next(
        row
        for row in bnsentmix_routing_summary
        if row["section"] == "cv_overall" and row["metric"] == "block40"
    )
    bnsentmix_routing_ok = (
        len(bnsentmix_routing_candidates) == 15
        and len(bnsentmix_routing_summary) == 14
        and bnsentmix_routing_pilot["selected_rule"] == "single|Qwen2.5-3B"
        and int(bnsentmix_routing_pilot["dev_correct"]) == 17
        and int(bnsentmix_routing_pilot["test_correct"]) == 72
        and int(bnsentmix_routing_pilot["best_single_test_correct"]) == 87
        and int(bnsentmix_routing_pilot["posthoc_best_correct"]) == 95
        and int(bnsentmix_routing_hash5["selected_correct"]) == 106
        and bnsentmix_routing_hash5["selected_rule_counts"] == "majority_fallback|Qwen2.5-7B 8-bit=5"
        and int(bnsentmix_routing_block40["selected_correct"]) == 84
    )
    add_row(
        rows,
        "qa_gates",
        status_label(bnsentmix_routing_ok),
        "bnsentmix_routing_devtest",
        len(bnsentmix_routing_candidates),
        (
            f"summary_rows={len(bnsentmix_routing_summary)}; "
            f"pilot40_holdout={bnsentmix_routing_pilot['test_correct']}/{bnsentmix_routing_pilot['test_n']}; "
            f"hash5_cv={bnsentmix_routing_hash5['selected_correct']}/{bnsentmix_routing_hash5['n']}; "
            f"block40_cv={bnsentmix_routing_block40['selected_correct']}/{bnsentmix_routing_block40['n']}"
        ),
    )

    distractor_summary = read_csv(args.distractor_transition_summary)
    distractor_items = read_csv(args.distractor_transition_items)
    distractor_consensus = read_csv(args.distractor_transition_consensus)
    distractor_overall_rows = [
        row for row in distractor_summary if row["section"] == "model_overall"
    ]
    total_recoverable = sum(int(row["recoverable_misses"]) for row in distractor_overall_rows)
    total_valid = sum(int(row["valid_recoverable_misses"]) for row in distractor_overall_rows)
    qwen3_d_mode = next(
        row
        for row in distractor_overall_rows
        if row["model"] == "Qwen3-4B"
    )
    two_plus_convergence = next(
        row
        for row in distractor_summary
        if row["section"] == "cross_model_convergence"
        and row["bucket"] == "two_plus_models_recoverable_valid"
    )
    distractor_ok = (
        len(distractor_summary) == 20
        and len(distractor_items) == 432
        and len(distractor_consensus) == 144
        and len(distractor_overall_rows) == 3
        and total_valid == 162
        and total_recoverable == 164
        and qwen3_d_mode["top_wrong_option"] == "D"
        and int(qwen3_d_mode["pred_D"]) == 44
        and int(two_plus_convergence["n"]) == 50
        and int(two_plus_convergence["repeated_wrong_option_items"]) == 27
    )
    add_row(
        rows,
        "qa_gates",
        status_label(distractor_ok),
        "v5_benqa_distractor_transition",
        len(distractor_items),
        (
            f"summary_rows={len(distractor_summary)}; "
            f"consensus_rows={len(distractor_consensus)}; "
            f"valid_recoverable={total_valid}/{total_recoverable}; "
            f"two_plus_same_wrong={two_plus_convergence['repeated_wrong_option_items']}/"
            f"{two_plus_convergence['n']}"
        ),
    )

    label_balance_summary = read_csv(args.label_balance_summary)
    label_balance_by_label = read_csv(args.label_balance_by_label)
    label_balance_ok = len(label_balance_summary) == 24 and len(label_balance_by_label) == 36
    add_row(
        rows,
        "qa_gates",
        status_label(label_balance_ok),
        "v5_benqa_label_balance",
        len(label_balance_summary),
        f"by_label_rows={len(label_balance_by_label)}",
    )

    real_distribution_summary = read_csv(args.real_banglish_distribution_summary)
    real_distribution_items = read_csv(args.real_banglish_distribution_items)
    real_distribution_ok = len(real_distribution_summary) == 4 and len(real_distribution_items) == 4400
    add_row(
        rows,
        "qa_gates",
        status_label(real_distribution_ok),
        "real_banglish_v5_distribution",
        len(real_distribution_items),
        f"summary_rows={len(real_distribution_summary)}",
    )

    lexical_coverage_summary = read_csv(args.banglatlit_lexical_coverage_summary)
    lexical_coverage_items = read_csv(args.banglatlit_lexical_coverage_items)
    lexical_coverage_ok = len(lexical_coverage_summary) == 15 and len(lexical_coverage_items) == 200
    add_row(
        rows,
        "qa_gates",
        status_label(lexical_coverage_ok),
        "v5_banglatlit_lexical_coverage",
        len(lexical_coverage_items),
        f"summary_rows={len(lexical_coverage_summary)}",
    )

    option_lexical_summary = read_csv(args.benqa_option_lexical_coverage_summary)
    option_lexical_items = read_csv(args.benqa_option_lexical_coverage_items)
    options_all_q4 = next(
        row
        for row in option_lexical_summary
        if row["section"] == "coverage_quartile"
        and row["surface"] == "options_all"
        and row["bucket"] == "q4"
    )
    gold_option_q4 = next(
        row
        for row in option_lexical_summary
        if row["section"] == "coverage_quartile"
        and row["surface"] == "gold_option"
        and row["bucket"] == "q4"
    )
    parsed_options = sum(1 for row in option_lexical_items if int(row["options_parsed"]) == 4)
    option_lexical_ok = (
        len(option_lexical_summary) == 15
        and len(option_lexical_items) == 144
        and parsed_options == 144
        and int(options_all_q4["banglish_correct"]) < int(options_all_q4["bangla_correct"])
        and int(gold_option_q4["banglish_correct"]) < int(gold_option_q4["bangla_correct"])
    )
    add_row(
        rows,
        "qa_gates",
        status_label(option_lexical_ok),
        "v5_benqa_option_lexical_coverage",
        len(option_lexical_items),
        (
            f"summary_rows={len(option_lexical_summary)}; "
            f"options_parsed={parsed_options}/144; "
            f"options_q4={options_all_q4['banglish_correct']}/{options_all_q4['model_item_slots']} "
            f"vs {options_all_q4['bangla_correct']}/{options_all_q4['model_item_slots']}; "
            f"gold_q4={gold_option_q4['banglish_correct']}/{gold_option_q4['model_item_slots']} "
            f"vs {gold_option_q4['bangla_correct']}/{gold_option_q4['model_item_slots']}"
        ),
    )

    model_coverage_summary = read_csv(args.banglatlit_model_coverage_sensitivity_summary)
    model_coverage_items = read_csv(args.banglatlit_model_coverage_sensitivity_items)
    q4_rows = [
        row
        for row in model_coverage_summary
        if row["section"] == "coverage_quartile_all"
        and row["dataset"] == "all"
        and row["bucket"] == "q4"
    ]
    all_quartile_rows = [
        row
        for row in model_coverage_summary
        if row["section"] == "coverage_quartile_all"
        and row["dataset"] == "all"
    ]
    q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in q4_rows
    )
    all_quartile_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in all_quartile_rows
    )
    model_coverage_ok = (
        len(model_coverage_summary) == 45
        and len(model_coverage_items) == 600
        and len(q4_rows) == 3
        and len(all_quartile_rows) == 12
        and q4_direction_ok
        and all_quartile_direction_ok
    )
    add_row(
        rows,
        "qa_gates",
        status_label(model_coverage_ok),
        "v5_banglatlit_model_coverage_sensitivity",
        len(model_coverage_items),
        (
            f"summary_rows={len(model_coverage_summary)}; "
            f"all_q4_direction_ok={q4_direction_ok}; "
            f"all_quartile_direction_ok={all_quartile_direction_ok}"
        ),
    )

    spelling_variation_summary = read_csv(args.banglatlit_spelling_variation_sensitivity_summary)
    spelling_variation_items = read_csv(args.banglatlit_spelling_variation_sensitivity_items)
    spelling_q4_rows = [
        row
        for row in spelling_variation_summary
        if row["section"] == "variation_quartile_all"
        and row["dataset"] == "all"
        and row["bucket"] == "q4"
    ]
    spelling_all_quartile_rows = [
        row
        for row in spelling_variation_summary
        if row["section"] == "variation_quartile_all"
        and row["dataset"] == "all"
    ]
    spelling_q2_to_q4_rows = [
        row
        for row in spelling_all_quartile_rows
        if row["bucket"] in {"q2", "q3", "q4"}
    ]
    spelling_q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in spelling_q4_rows
    )
    spelling_q2_to_q4_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in spelling_q2_to_q4_rows
    )
    spelling_variation_ok = (
        len(spelling_variation_summary) == 45
        and len(spelling_variation_items) == 600
        and len(spelling_q4_rows) == 3
        and len(spelling_all_quartile_rows) == 12
        and len(spelling_q2_to_q4_rows) == 9
        and spelling_q4_direction_ok
        and spelling_q2_to_q4_direction_ok
    )
    add_row(
        rows,
        "qa_gates",
        status_label(spelling_variation_ok),
        "v5_banglatlit_spelling_variation_sensitivity",
        len(spelling_variation_items),
        (
            f"summary_rows={len(spelling_variation_summary)}; "
            f"all_q4_direction_ok={spelling_q4_direction_ok}; "
            f"q2_to_q4_direction_ok={spelling_q2_to_q4_direction_ok}"
        ),
    )

    source_parity_summary = read_csv(args.source_variant_parity_summary)
    source_parity_items = read_csv(args.source_variant_parity_items)
    primary_all = next(
        row
        for row in source_parity_summary
        if row["comparison"] == "bangla_vs_banglish"
        and row["dataset"] == "all"
        and row["task_type"] == "all"
    )
    source_parity_ok = (
        len(source_parity_summary) == 15
        and len(source_parity_items) == 600
        and int(primary_all["primary_pair_hard_fail"]) == 0
    )
    add_row(
        rows,
        "qa_gates",
        status_label(source_parity_ok),
        "v5_source_variant_structural_parity",
        len(source_parity_items),
        f"summary_rows={len(source_parity_summary)}; primary_hard_fails={primary_all['primary_pair_hard_fail']}",
    )

    english_warning_summary = read_csv(args.english_warning_sensitivity_summary)
    english_warning_items = read_csv(args.english_warning_sensitivity_items)
    clean_all_rows = [
        row
        for row in english_warning_summary
        if row["structural_group"] == "english_structural_clean"
        and row["dataset"] == "all"
    ]
    clean_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in clean_all_rows
    )
    warning_item_count = len(
        {
            row["id"]
            for row in english_warning_items
            if row["english_structural_warning"] == "True"
        }
    )
    english_warning_ok = (
        len(english_warning_summary) == 27
        and len(english_warning_items) == 600
        and len(clean_all_rows) == 3
        and clean_direction_ok
        and warning_item_count == 39
    )
    add_row(
        rows,
        "qa_gates",
        status_label(english_warning_ok),
        "v5_english_warning_sensitivity",
        len(english_warning_items),
        f"summary_rows={len(english_warning_summary)}; warning_items={warning_item_count}; clean_direction_ok={clean_direction_ok}",
    )

    edit_distance_summary = read_csv(args.review_edit_distance_sensitivity_summary)
    edit_distance_items = read_csv(args.review_edit_distance_sensitivity_items)
    no_change_rows = [
        row
        for row in edit_distance_summary
        if row["edit_bucket"] == "no_applied_change"
        and row["dataset"] == "all"
    ]
    no_change_direction_ok = all(
        int(row["banglish_correct"]) < int(row["bangla_correct"])
        and int(row["banglish_correct"]) < int(row["english_correct"])
        for row in no_change_rows
    )
    edit_bucket_counts = {
        row["edit_bucket"]
        for row in edit_distance_items
    }
    edit_distance_ok = (
        len(edit_distance_summary) == 45
        and len(edit_distance_items) == 600
        and len(no_change_rows) == 3
        and no_change_direction_ok
        and len(edit_bucket_counts) == 4
    )
    add_row(
        rows,
        "qa_gates",
        status_label(edit_distance_ok),
        "v5_review_edit_distance_sensitivity",
        len(edit_distance_items),
        f"summary_rows={len(edit_distance_summary)}; no_change_direction_ok={no_change_direction_ok}",
    )

    lit_rows = read_csv(args.literature_corpus)
    lit_issues = sum(1 for row in lit_rows if row.get("status") != "ok")
    add_row(
        rows,
        "literature",
        status_label(lit_issues == 0),
        "literature_corpus",
        len(lit_rows),
        f"issues={lit_issues}",
    )

    citation_rows = read_csv(args.citation_readiness)
    citation_issues = sum(1 for row in citation_rows if row.get("status") != "ok")
    add_row(
        rows,
        "literature",
        status_label(citation_issues == 0),
        "citation_readiness",
        len(citation_rows),
        f"issues={citation_issues}",
    )

    secret_findings = len(read_csv(args.secret_hygiene))
    files_checked = parse_int_from_report(args.secret_hygiene_report, r"Files checked: ([0-9,]+)")
    add_row(
        rows,
        "qa_gates",
        status_label(secret_findings == 0),
        "secret_hygiene",
        files_checked,
        f"suspicious_findings={secret_findings}",
    )

    refs_checked = parse_int_from_report(args.local_refs_report, r"Checked references: ([0-9,]+)")
    unexpected_missing = parse_int_from_report(args.local_refs_report, r"Unexpected missing references: ([0-9,]+)")
    expected_future = parse_int_from_report(args.local_refs_report, r"Expected future/planned references: ([0-9,]+)")
    add_row(
        rows,
        "qa_gates",
        status_label(unexpected_missing == 0),
        "local_artifact_refs",
        refs_checked,
        f"unexpected_missing={unexpected_missing}; expected_future={expected_future}",
    )

    manifest_count = projected_manifest_count([args.output_csv, args.output_md])
    add_row(
        rows,
        "qa_gates",
        "pass",
        "reproducibility_manifest",
        manifest_count,
        "non-secret artifacts tracked",
    )

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-queue", type=Path, default=ROOT / "data/slices/validation_200_v5_review_queue.csv")
    parser.add_argument("--review-resume", type=Path, default=ROOT / "results/analysis/validation200_v5_review_resume_card.csv")
    parser.add_argument("--rerun-readiness", type=Path, default=ROOT / "results/analysis/post_v5_rerun_readiness.csv")
    parser.add_argument("--kaggle-job-plan", type=Path, default=ROOT / "results/analysis/post_v5_kaggle_job_plan.csv")
    parser.add_argument("--compute-budget", type=Path, default=ROOT / "results/analysis/post_v5_compute_budget.csv")
    parser.add_argument("--qwen25-v5-summary", type=Path, default=ROOT / "results/analysis/qwen25_validation200_v5_vs_v4_banglish_summary.csv")
    parser.add_argument("--qwen3-v5-summary", type=Path, default=ROOT / "results/analysis/qwen3_validation200_v5_vs_v4_banglish_summary.csv")
    parser.add_argument("--optional-7b-output", type=Path, default=ROOT / "results/runs/qwen25_7b_8bit_validation200_v5_banglish_pinned/results/runs/qwen2_5_7b_8bit_validation200_v5_banglish_pinned.jsonl")
    parser.add_argument("--optional-7b-log", type=Path, default=ROOT / "results/runs/qwen25_7b_8bit_validation200_v5_banglish_pinned/qwen2-5-7b-8-bit-validation-200-v5-banglish-pinned.log")
    parser.add_argument("--packet-integrity", type=Path, default=ROOT / "results/analysis/validation200_v5_review_packet_integrity.csv")
    parser.add_argument("--figure-integrity", type=Path, default=ROOT / "results/analysis/thesis_figure_integrity_check.csv")
    parser.add_argument("--table-integrity", type=Path, default=ROOT / "results/analysis/thesis_table_integrity_check.csv")
    parser.add_argument("--api-audit-manifest", type=Path, default=ROOT / "results/analysis/api_audit_manifest_integrity_check.csv")
    parser.add_argument("--api-audit-import-roundtrip", type=Path, default=ROOT / "results/analysis/api_audit_import_roundtrip_check.csv")
    parser.add_argument("--gemini-api-summary", type=Path, default=ROOT / "results/analysis/gemini_3_5_flash_validation200_v5_summary.csv")
    parser.add_argument("--openai-api-summary", type=Path, default=ROOT / "results/analysis/openai_gpt55_low_validation200_v5_cap1024_summary.csv")
    parser.add_argument("--frontier-api-panel", type=Path, default=ROOT / "results/analysis/frontier_api_panel_validation200_v5.csv")
    parser.add_argument("--benqa-extension-review-queue", type=Path, default=ROOT / "results/analysis/benqa_extended_1000_v1_ai_review_queue.csv")
    parser.add_argument("--benqa-extension-full-summary", type=Path, default=ROOT / "results/analysis/qwen25_3b_benqa_ext_full851_summary.csv")
    parser.add_argument("--benqa-extension-full-paired", type=Path, default=ROOT / "results/analysis/qwen25_3b_benqa_ext_full851_paired_gaps.csv")
    parser.add_argument("--deepseek-extension-full-summary", type=Path, default=ROOT / "results/analysis/deepseek_v4_flash_benqa_ext_full851_summary.csv")
    parser.add_argument("--deepseek-extension-full-paired", type=Path, default=ROOT / "results/analysis/deepseek_v4_flash_benqa_ext_full851_paired_gaps.csv")
    parser.add_argument("--research-log-compactness", type=Path, default=ROOT / "results/analysis/research_log_compactness_check.csv")
    parser.add_argument("--recoverability-source-items", type=Path, default=ROOT / "results/analysis/v5_recoverability_source_items.csv")
    parser.add_argument("--recoverability-source-summary", type=Path, default=ROOT / "results/analysis/v5_recoverability_source_summary.csv")
    parser.add_argument("--cross-script-transfer-items", type=Path, default=ROOT / "results/analysis/v5_cross_script_transfer_items.csv")
    parser.add_argument("--cross-script-transfer-summary", type=Path, default=ROOT / "results/analysis/v5_cross_script_transfer_summary.csv")
    parser.add_argument("--token-failure-items", type=Path, default=ROOT / "results/analysis/validation200_v5_cross_script_token_patterns_items.csv")
    parser.add_argument("--token-failure-summary", type=Path, default=ROOT / "results/analysis/validation200_v5_cross_script_token_patterns_summary.csv")
    parser.add_argument("--review-label-sensitivity", type=Path, default=ROOT / "results/analysis/v5_review_label_sensitivity_summary.csv")
    parser.add_argument("--dataset-gap-intervals", type=Path, default=ROOT / "results/analysis/v5_dataset_gap_intervals.csv")
    parser.add_argument("--paired-sign-tests", type=Path, default=ROOT / "results/analysis/v5_paired_sign_tests.csv")
    parser.add_argument("--clustered-gap-clusters", type=Path, default=ROOT / "results/analysis/v5_clustered_gap_clusters.csv")
    parser.add_argument("--clustered-gap-summary", type=Path, default=ROOT / "results/analysis/v5_clustered_gap_summary.csv")
    parser.add_argument("--benqa-subject-stability", type=Path, default=ROOT / "results/analysis/v5_benqa_subject_stability.csv")
    parser.add_argument("--benqa-subject-balance-subjects", type=Path, default=ROOT / "results/analysis/v5_benqa_subject_balance_subjects.csv")
    parser.add_argument("--benqa-subject-balance-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_subject_balance_summary.csv")
    parser.add_argument("--qwen-scaling-transfer-transitions", type=Path, default=ROOT / "results/analysis/v5_qwen_scaling_transfer_transitions.csv")
    parser.add_argument("--qwen-scaling-transfer-summary", type=Path, default=ROOT / "results/analysis/v5_qwen_scaling_transfer_summary.csv")
    parser.add_argument("--fragility-overlap-items", type=Path, default=ROOT / "results/analysis/v5_banglish_fragility_model_overlap_items.csv")
    parser.add_argument("--fragility-overlap-summary", type=Path, default=ROOT / "results/analysis/v5_banglish_fragility_model_overlap_summary.csv")
    parser.add_argument("--item-consensus-items", type=Path, default=ROOT / "results/analysis/v5_item_consensus_items.csv")
    parser.add_argument("--item-consensus-summary", type=Path, default=ROOT / "results/analysis/v5_item_consensus_summary.csv")
    parser.add_argument("--difficulty-conditioned-items", type=Path, default=ROOT / "results/analysis/v5_difficulty_conditioned_gap_items.csv")
    parser.add_argument("--difficulty-conditioned-summary", type=Path, default=ROOT / "results/analysis/v5_difficulty_conditioned_gap_summary.csv")
    parser.add_argument("--consensus-stability-items", type=Path, default=ROOT / "results/analysis/v5_consensus_stability_items.csv")
    parser.add_argument("--consensus-stability-summary", type=Path, default=ROOT / "results/analysis/v5_consensus_stability_summary.csv")
    parser.add_argument("--composition-sensitivity-items", type=Path, default=ROOT / "results/analysis/v5_composition_sensitivity_items.csv")
    parser.add_argument("--composition-sensitivity-summary", type=Path, default=ROOT / "results/analysis/v5_composition_sensitivity_summary.csv")
    parser.add_argument("--shared-fragility-examples", type=Path, default=ROOT / "results/analysis/v5_shared_fragility_examples.csv")
    parser.add_argument("--answer-format-items", type=Path, default=ROOT / "results/analysis/v5_answer_format_audit_items.csv")
    parser.add_argument("--answer-format-summary", type=Path, default=ROOT / "results/analysis/v5_answer_format_audit_summary.csv")
    parser.add_argument("--response-style-items", type=Path, default=ROOT / "results/analysis/v5_response_style_drift_items.csv")
    parser.add_argument("--response-style-summary", type=Path, default=ROOT / "results/analysis/v5_response_style_drift_summary.csv")
    parser.add_argument("--banglamath-numeric-items", type=Path, default=ROOT / "results/analysis/v5_banglamath_numeric_sensitivity_items.csv")
    parser.add_argument("--banglamath-numeric-summary", type=Path, default=ROOT / "results/analysis/v5_banglamath_numeric_sensitivity_summary.csv")
    parser.add_argument("--banglamath-numeric-transfer-items", type=Path, default=ROOT / "results/analysis/v5_banglamath_numeric_transfer_items.csv")
    parser.add_argument("--banglamath-numeric-transfer-summary", type=Path, default=ROOT / "results/analysis/v5_banglamath_numeric_transfer_summary.csv")
    parser.add_argument("--choice-bias-items", type=Path, default=ROOT / "results/analysis/v5_benqa_choice_bias_items.csv")
    parser.add_argument("--choice-bias-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_choice_bias_summary.csv")
    parser.add_argument("--subject-option-items", type=Path, default=ROOT / "results/analysis/v5_benqa_subject_option_bias_items.csv")
    parser.add_argument("--subject-option-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_subject_option_bias_summary.csv")
    parser.add_argument("--prediction-diversity-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_prediction_diversity_summary.csv")
    parser.add_argument("--option-position-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_position_content_items.csv")
    parser.add_argument("--option-position-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_position_content_summary.csv")
    parser.add_argument("--option-switching-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_switching_items.csv")
    parser.add_argument("--option-switching-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_switching_summary.csv")
    parser.add_argument("--cross-script-option-agreement-items", type=Path, default=ROOT / "results/analysis/v5_benqa_cross_script_option_agreement_items.csv")
    parser.add_argument("--cross-script-option-agreement-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_cross_script_option_agreement_summary.csv")
    parser.add_argument("--cross-model-banglish-agreement-items", type=Path, default=ROOT / "results/analysis/v5_benqa_cross_model_banglish_agreement_items.csv")
    parser.add_argument("--cross-model-banglish-agreement-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_cross_model_banglish_agreement_summary.csv")
    parser.add_argument("--order-confound-items", type=Path, default=ROOT / "results/analysis/v5_benqa_order_confound_items.csv")
    parser.add_argument("--order-confound-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_order_confound_summary.csv")
    parser.add_argument("--review-label-option-items", type=Path, default=ROOT / "results/analysis/v5_benqa_review_label_option_bias_items.csv")
    parser.add_argument("--review-label-option-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_review_label_option_bias_summary.csv")
    parser.add_argument("--length-token-confound-items", type=Path, default=ROOT / "results/analysis/v5_benqa_length_token_confound_items.csv")
    parser.add_argument("--length-token-confound-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_length_token_confound_summary.csv")
    parser.add_argument("--option-coverage-confound-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_coverage_confound_items.csv")
    parser.add_argument("--option-coverage-confound-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_coverage_confound_summary.csv")
    parser.add_argument("--switch-confound-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_switch_confound_items.csv")
    parser.add_argument("--switch-confound-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_switch_confound_summary.csv")
    parser.add_argument("--semantic-cue-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_semantic_cues_items.csv")
    parser.add_argument("--semantic-cue-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_semantic_cues_summary.csv")
    parser.add_argument("--multiconfound-residual-items", type=Path, default=ROOT / "results/analysis/v5_benqa_multiconfound_residual_items.csv")
    parser.add_argument("--multiconfound-residual-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_multiconfound_residual_summary.csv")
    parser.add_argument("--distractor-transition-items", type=Path, default=ROOT / "results/analysis/v5_benqa_distractor_transition_items.csv")
    parser.add_argument("--distractor-transition-consensus", type=Path, default=ROOT / "results/analysis/v5_benqa_distractor_transition_item_consensus.csv")
    parser.add_argument("--distractor-transition-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_distractor_transition_summary.csv")
    parser.add_argument("--label-balance-by-label", type=Path, default=ROOT / "results/analysis/v5_benqa_label_balance_by_label.csv")
    parser.add_argument("--label-balance-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_label_balance_summary.csv")
    parser.add_argument("--option-permutation-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_permutation_probe_items.csv")
    parser.add_argument("--option-permutation-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_permutation_probe_summary.csv")
    parser.add_argument("--bnsentmix-items", type=Path, default=ROOT / "results/analysis/bnsentmix_external_validation_items.csv")
    parser.add_argument("--bnsentmix-summary", type=Path, default=ROOT / "results/analysis/bnsentmix_external_validation_summary.csv")
    parser.add_argument("--bnsentmix-complementarity-items", type=Path, default=ROOT / "results/analysis/bnsentmix_model_complementarity_items.csv")
    parser.add_argument("--bnsentmix-complementarity-summary", type=Path, default=ROOT / "results/analysis/bnsentmix_model_complementarity_summary.csv")
    parser.add_argument("--bnsentmix-routing-candidates", type=Path, default=ROOT / "results/analysis/bnsentmix_routing_devtest_candidates.csv")
    parser.add_argument("--bnsentmix-routing-summary", type=Path, default=ROOT / "results/analysis/bnsentmix_routing_devtest_summary.csv")
    parser.add_argument("--real-banglish-distribution-items", type=Path, default=ROOT / "results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_items.csv")
    parser.add_argument("--real-banglish-distribution-summary", type=Path, default=ROOT / "results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv")
    parser.add_argument("--banglatlit-lexical-coverage-items", type=Path, default=ROOT / "results/analysis/v5_banglatlit_lexical_coverage_items.csv")
    parser.add_argument("--banglatlit-lexical-coverage-summary", type=Path, default=ROOT / "results/analysis/v5_banglatlit_lexical_coverage_summary.csv")
    parser.add_argument("--benqa-option-lexical-coverage-items", type=Path, default=ROOT / "results/analysis/v5_benqa_option_lexical_coverage_items.csv")
    parser.add_argument("--benqa-option-lexical-coverage-summary", type=Path, default=ROOT / "results/analysis/v5_benqa_option_lexical_coverage_summary.csv")
    parser.add_argument("--banglatlit-model-coverage-sensitivity-items", type=Path, default=ROOT / "results/analysis/v5_banglatlit_model_coverage_sensitivity_items.csv")
    parser.add_argument("--banglatlit-model-coverage-sensitivity-summary", type=Path, default=ROOT / "results/analysis/v5_banglatlit_model_coverage_sensitivity_summary.csv")
    parser.add_argument("--banglatlit-spelling-variation-sensitivity-items", type=Path, default=ROOT / "results/analysis/v5_banglatlit_spelling_variation_sensitivity_items.csv")
    parser.add_argument("--banglatlit-spelling-variation-sensitivity-summary", type=Path, default=ROOT / "results/analysis/v5_banglatlit_spelling_variation_sensitivity_summary.csv")
    parser.add_argument("--source-variant-parity-items", type=Path, default=ROOT / "results/analysis/v5_source_variant_structural_parity_items.csv")
    parser.add_argument("--source-variant-parity-summary", type=Path, default=ROOT / "results/analysis/v5_source_variant_structural_parity_summary.csv")
    parser.add_argument("--english-warning-sensitivity-items", type=Path, default=ROOT / "results/analysis/v5_english_warning_sensitivity_items.csv")
    parser.add_argument("--english-warning-sensitivity-summary", type=Path, default=ROOT / "results/analysis/v5_english_warning_sensitivity_summary.csv")
    parser.add_argument("--review-edit-distance-sensitivity-items", type=Path, default=ROOT / "results/analysis/v5_review_edit_distance_sensitivity_items.csv")
    parser.add_argument("--review-edit-distance-sensitivity-summary", type=Path, default=ROOT / "results/analysis/v5_review_edit_distance_sensitivity_summary.csv")
    parser.add_argument("--literature-corpus", type=Path, default=ROOT / "results/analysis/literature_corpus_check.csv")
    parser.add_argument("--citation-readiness", type=Path, default=ROOT / "results/analysis/citation_readiness_check.csv")
    parser.add_argument("--secret-hygiene", type=Path, default=ROOT / "results/analysis/secret_hygiene_check.csv")
    parser.add_argument("--secret-hygiene-report", type=Path, default=ROOT / "reports/secret_hygiene_check.md")
    parser.add_argument("--local-refs-report", type=Path, default=ROOT / "reports/local_artifact_reference_check.md")
    parser.add_argument("--output-csv", type=Path, default=ROOT / "results/analysis/current_research_status_dashboard.csv")
    parser.add_argument("--output-md", type=Path, default=ROOT / "reports/current_research_status_dashboard.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(args)
    write_csv(rows, args.output_csv)
    write_report(rows, args.output_md, args.output_csv)
    failing = sum(1 for row in rows if row["status"] == "fail")
    blocked = sum(1 for row in rows if row["status"] == "blocked")
    print(
        f"rows={len(rows)} blocked={blocked} failing={failing} "
        f"report={args.output_md}"
    )


if __name__ == "__main__":
    main()
