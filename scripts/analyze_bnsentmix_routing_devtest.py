#!/usr/bin/env python3
"""Audit whether BnSentMix model complementarity yields a deployable route."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from bootstrap_accuracy_delta import bootstrap_delta


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/analysis/bnsentmix_model_complementarity_items.csv"
DEFAULT_CANDIDATES_OUTPUT = ROOT / "results/analysis/bnsentmix_routing_devtest_candidates.csv"
DEFAULT_SUMMARY_OUTPUT = ROOT / "results/analysis/bnsentmix_routing_devtest_summary.csv"
DEFAULT_REPORT = ROOT / "reports/bnsentmix_routing_devtest.md"
MODELS = ("Qwen2.5-3B", "Qwen2.5-7B 8-bit", "Qwen3-4B")
BOOTSTRAP_ITERATIONS = 5000
BOOTSTRAP_SEED = 20260603


@dataclass(frozen=True)
class Rule:
    kind: str
    left: str
    right: str = ""
    fallback: str = ""

    @property
    def rule_id(self) -> str:
        parts = [self.kind, self.left]
        if self.right:
            parts.append(self.right)
        if self.fallback:
            parts.append(self.fallback)
        return "|".join(parts)

    @property
    def complexity(self) -> int:
        return {"single": 0, "majority_fallback": 1, "pair_agree_fallback": 2}[self.kind]


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def model_key(model: str) -> str:
    return model.lower().replace(".", "").replace("-", "_").replace(" ", "_")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"No rows to write for {path}")
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


def percent(correct: int, n: int) -> str:
    return f"{100 * correct / n:.1f}%" if n else "0.0%"


def points(value: Any) -> str:
    scaled = float(value) * 100
    sign = "+" if scaled > 0 else ""
    return f"{sign}{scaled:.1f}"


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|")


def load_items(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    if len(rows) != 200:
        raise SystemExit(f"Expected 200 BnSentMix complementarity rows, found {len(rows)}")
    required = {"id", "gold", "majority_prediction"}
    for model in MODELS:
        required.add(f"{model_key(model)}_parsed")
        required.add(f"{model_key(model)}_correct")
    missing = sorted(required - set(rows[0]))
    if missing:
        raise SystemExit(f"{path} is missing required columns: {missing}")
    return rows


def build_rules() -> list[Rule]:
    rules = [Rule("single", model) for model in MODELS]
    rules.extend(Rule("majority_fallback", model) for model in MODELS)
    for idx, left in enumerate(MODELS):
        for right in MODELS[idx + 1 :]:
            for fallback in MODELS:
                rules.append(Rule("pair_agree_fallback", left, right, fallback))
    return rules


def predict(row: dict[str, str], rule: Rule) -> str:
    if rule.kind == "single":
        return row[f"{model_key(rule.left)}_parsed"]
    if rule.kind == "majority_fallback":
        return row["majority_prediction"] or row[f"{model_key(rule.left)}_parsed"]
    if rule.kind == "pair_agree_fallback":
        left_prediction = row[f"{model_key(rule.left)}_parsed"]
        right_prediction = row[f"{model_key(rule.right)}_parsed"]
        if left_prediction == right_prediction:
            return left_prediction
        return row[f"{model_key(rule.fallback)}_parsed"]
    raise ValueError(f"Unsupported rule: {rule}")


def correct(row: dict[str, str], rule: Rule) -> bool:
    return predict(row, rule) == row["gold"]


def score(rows: list[dict[str, str]], rule: Rule) -> int:
    return sum(correct(row, rule) for row in rows)


def choose_rule(rows: list[dict[str, str]], rules: list[Rule]) -> Rule:
    return max(
        rules,
        key=lambda rule: (
            score(rows, rule),
            -rule.complexity,
            tuple(-ord(char) for char in rule.rule_id),
        ),
    )


def best_rule(rows: list[dict[str, str]], rules: list[Rule]) -> Rule:
    return max(rules, key=lambda rule: (score(rows, rule), -rule.complexity, rule.rule_id))


def single_correct(rows: list[dict[str, str]], model: str) -> int:
    key = model_key(model)
    return sum(truthy(row[f"{key}_correct"]) for row in rows)


def best_single_correct(rows: list[dict[str, str]]) -> int:
    return max(single_correct(rows, model) for model in MODELS)


def hash_folds(rows: list[dict[str, str]], k: int = 5) -> list[list[dict[str, str]]]:
    folds: list[list[dict[str, str]]] = [[] for _ in range(k)]
    for row in rows:
        digest = hashlib.sha256(row["id"].encode("utf-8")).hexdigest()
        folds[int(digest, 16) % k].append(row)
    return folds


def block_folds(rows: list[dict[str, str]], size: int = 40) -> list[list[dict[str, str]]]:
    return [rows[start : start + size] for start in range(0, len(rows), size)]


def bootstrap_delta_for_flags(left_flags: list[bool], right_flags: list[bool], seed: int) -> tuple[float, float, float, float]:
    return bootstrap_delta(list(zip(left_flags, right_flags)), BOOTSTRAP_ITERATIONS, seed)


def cv_select(
    rows: list[dict[str, str]],
    folds: list[list[dict[str, str]]],
    rules: list[Rule],
    split_strategy: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[bool]]:
    fold_rows: list[dict[str, Any]] = []
    selected_correct_flags_by_id: dict[str, bool] = {}
    for fold_index, test_rows in enumerate(folds):
        test_ids = {row["id"] for row in test_rows}
        train_rows = [row for row in rows if row["id"] not in test_ids]
        selected = choose_rule(train_rows, rules)
        train_correct = score(train_rows, selected)
        test_correct = score(test_rows, selected)
        fold_rows.append(
            {
                "section": "cv_fold",
                "metric": f"{split_strategy}_fold_{fold_index}",
                "split_strategy": split_strategy,
                "fold": fold_index,
                "selected_rule": selected.rule_id,
                "train_correct": train_correct,
                "train_n": len(train_rows),
                "eval_correct": test_correct,
                "eval_n": len(test_rows),
                "qwen3_correct": single_correct(test_rows, "Qwen3-4B"),
                "qwen25_7b_correct": single_correct(test_rows, "Qwen2.5-7B 8-bit"),
                "best_single_correct": best_single_correct(test_rows),
            }
        )
        for row in test_rows:
            selected_correct_flags_by_id[row["id"]] = correct(row, selected)
    if set(selected_correct_flags_by_id) != {row["id"] for row in rows}:
        raise SystemExit(f"{split_strategy} CV did not score every item exactly once")

    selected_flags = [selected_correct_flags_by_id[row["id"]] for row in rows]
    qwen3_flags = [truthy(row[f"{model_key('Qwen3-4B')}_correct"]) for row in rows]
    qwen25_7b_flags = [truthy(row[f"{model_key('Qwen2.5-7B 8-bit')}_correct"]) for row in rows]
    selected_correct = sum(selected_flags)
    qwen3_delta = bootstrap_delta_for_flags(qwen3_flags, selected_flags, BOOTSTRAP_SEED + 211)
    qwen25_7b_delta = bootstrap_delta_for_flags(qwen25_7b_flags, selected_flags, BOOTSTRAP_SEED + 223)
    selected_rule_counts = Counter(str(row["selected_rule"]) for row in fold_rows)
    overall = {
        "section": "cv_overall",
        "metric": split_strategy,
        "split_strategy": split_strategy,
        "selected_correct": selected_correct,
        "n": len(rows),
        "selected_accuracy": f"{selected_correct / len(rows):.6f}",
        "qwen3_correct": single_correct(rows, "Qwen3-4B"),
        "qwen25_7b_correct": single_correct(rows, "Qwen2.5-7B 8-bit"),
        "best_single_oracle_by_fold_correct": sum(int(row["best_single_correct"]) for row in fold_rows),
        "selected_minus_qwen3": f"{qwen3_delta[0]:.6f}",
        "selected_minus_qwen3_ci95_low": f"{qwen3_delta[1]:.6f}",
        "selected_minus_qwen3_ci95_high": f"{qwen3_delta[2]:.6f}",
        "selected_minus_qwen25_7b": f"{qwen25_7b_delta[0]:.6f}",
        "selected_minus_qwen25_7b_ci95_low": f"{qwen25_7b_delta[1]:.6f}",
        "selected_minus_qwen25_7b_ci95_high": f"{qwen25_7b_delta[2]:.6f}",
        "selected_rule_counts": ";".join(
            f"{rule_id}={count}" for rule_id, count in sorted(selected_rule_counts.items())
        ),
    }
    return overall, fold_rows, selected_flags


def candidate_rows(rows: list[dict[str, str]], rules: list[Rule]) -> list[dict[str, Any]]:
    dev_rows = rows[:40]
    holdout_rows = rows[40:]
    out: list[dict[str, Any]] = []
    for rule in rules:
        full_correct = score(rows, rule)
        dev_correct = score(dev_rows, rule)
        holdout_correct = score(holdout_rows, rule)
        out.append(
            {
                "rule": rule.rule_id,
                "kind": rule.kind,
                "left": rule.left,
                "right": rule.right,
                "fallback": rule.fallback,
                "full_correct": full_correct,
                "full_n": len(rows),
                "full_accuracy": f"{full_correct / len(rows):.6f}",
                "dev40_correct": dev_correct,
                "dev40_n": len(dev_rows),
                "dev40_accuracy": f"{dev_correct / len(dev_rows):.6f}",
                "holdout160_correct": holdout_correct,
                "holdout160_n": len(holdout_rows),
                "holdout160_accuracy": f"{holdout_correct / len(holdout_rows):.6f}",
            }
        )
    return out


def build_summary(rows: list[dict[str, str]], rules: list[Rule]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    dev_rows = rows[:40]
    holdout_rows = rows[40:]
    selected = choose_rule(dev_rows, rules)
    posthoc_best = best_rule(holdout_rows, rules)
    selected_test_correct = score(holdout_rows, selected)
    selected_flags = [correct(row, selected) for row in holdout_rows]
    qwen3_flags = [truthy(row[f"{model_key('Qwen3-4B')}_correct"]) for row in holdout_rows]
    qwen3_delta = bootstrap_delta_for_flags(qwen3_flags, selected_flags, BOOTSTRAP_SEED + 101)
    summary.append(
        {
            "section": "pilot_devtest",
            "metric": "pilot40_selected_rule",
            "selected_rule": selected.rule_id,
            "dev_correct": score(dev_rows, selected),
            "dev_n": len(dev_rows),
            "test_correct": selected_test_correct,
            "test_n": len(holdout_rows),
            "qwen3_test_correct": single_correct(holdout_rows, "Qwen3-4B"),
            "qwen25_7b_test_correct": single_correct(holdout_rows, "Qwen2.5-7B 8-bit"),
            "best_single_test_correct": best_single_correct(holdout_rows),
            "posthoc_best_rule": posthoc_best.rule_id,
            "posthoc_best_correct": score(holdout_rows, posthoc_best),
            "selected_minus_qwen3": f"{qwen3_delta[0]:.6f}",
            "selected_minus_qwen3_ci95_low": f"{qwen3_delta[1]:.6f}",
            "selected_minus_qwen3_ci95_high": f"{qwen3_delta[2]:.6f}",
            "note": "Pilot-prefix selection is unstable and underperforms stronger single models on the remaining rows.",
        }
    )

    hash_overall, hash_fold_rows, _hash_flags = cv_select(rows, hash_folds(rows), rules, "hash5")
    block_overall, block_fold_rows, _block_flags = cv_select(rows, block_folds(rows), rules, "block40")
    summary.append(hash_overall)
    summary.extend(hash_fold_rows)
    summary.append(block_overall)
    summary.extend(block_fold_rows)
    summary.append(
        {
            "section": "input",
            "metric": "candidate_rules",
            "candidate_rules": len(rules),
            "items": len(rows),
            "models": len(MODELS),
        }
    )
    return summary


def find(summary: list[dict[str, Any]], section: str, metric: str) -> dict[str, Any]:
    return next(row for row in summary if row["section"] == section and row["metric"] == metric)


def write_report(
    path: Path,
    input_path: Path,
    candidates_output: Path,
    summary_output: Path,
    summary: list[dict[str, Any]],
) -> None:
    pilot = find(summary, "pilot_devtest", "pilot40_selected_rule")
    hash5 = find(summary, "cv_overall", "hash5")
    block40 = find(summary, "cv_overall", "block40")
    lines = [
        "# BnSentMix Routing Dev-Test Audit",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        "This no-spend audit tests whether the BnSentMix three-model",
        "complementarity signal can be converted into a simple deployable route.",
        "It deliberately separates post-hoc oracle evidence from rules selected",
        "without seeing the evaluation fold labels.",
        "",
        f"- Source complementarity items: `{repo_path(input_path)}`",
        f"- Candidate table: `{repo_path(candidates_output)}`",
        f"- Routing summary: `{repo_path(summary_output)}`",
        "",
        "## Headline",
        "",
        "| Selection protocol | Selected result | Baseline context | Interpretation |",
        "| --- | ---: | --- | --- |",
        (
            f"| Pilot40 -> holdout160 | {pilot['test_correct']}/{pilot['test_n']} | "
            f"Qwen3 and Qwen2.5-7B each reach {pilot['best_single_test_correct']}/{pilot['test_n']} "
            f"as the best single held-out rows; post-hoc best route reaches "
            f"{pilot['posthoc_best_correct']}/{pilot['test_n']}. | "
            "The 40-row ordered pilot is too small/misleading for route selection. |"
        ),
        (
            f"| Hash5 cross-validation | {hash5['selected_correct']}/{hash5['n']} | "
            f"Qwen3 {hash5['qwen3_correct']}/{hash5['n']}; Qwen2.5-7B "
            f"{hash5['qwen25_7b_correct']}/{hash5['n']}. | "
            "All hash folds select majority vote with Qwen2.5-7B fallback; "
            "this is a weak deployable candidate, not a locked mitigation. |"
        ),
        (
            f"| Block40 cross-validation | {block40['selected_correct']}/{block40['n']} | "
            f"Qwen3 {block40['qwen3_correct']}/{block40['n']}; Qwen2.5-7B "
            f"{block40['qwen25_7b_correct']}/{block40['n']}. | "
            "Ordered blocks expose route-selection instability. |"
        ),
        "",
        "## What This Means",
        "",
        "- The complementarity result remains meaningful: the same natural",
        "  code-mixed items are not failed by all models in the same way.",
        "- A simple majority route with Qwen2.5-7B fallback is the only practical",
        "  candidate that survives hash-fold selection, reaching 106/200.",
        "- The candidate is not strong enough to claim a deployed solution because",
        "  block folds and the pilot-prefix split underperform single-model baselines.",
        "",
        "## Fold Details",
        "",
        "| Split | Fold | Selected rule | Train | Eval | Qwen3 eval | Qwen2.5-7B eval |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in [row for row in summary if row["section"] == "cv_fold"]:
        lines.append(
            f"| {row['split_strategy']} | {row['fold']} | {md_cell(row['selected_rule'])} | "
            f"{row['train_correct']}/{row['train_n']} | "
            f"{row['eval_correct']}/{row['eval_n']} | "
            f"{row['qwen3_correct']}/{row['eval_n']} | "
            f"{row['qwen25_7b_correct']}/{row['eval_n']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- Report this as a deployability stress test for the complementarity",
            "  finding, not as a final routing method.",
            "- The thesis-safe result is: large natural-task complementarity exists,",
            "  but simple label-only routing needs a larger preregistered external",
            "  development set before it can be claimed as mitigation.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def assert_expected(summary: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> None:
    pilot = find(summary, "pilot_devtest", "pilot40_selected_rule")
    hash5 = find(summary, "cv_overall", "hash5")
    block40 = find(summary, "cv_overall", "block40")
    expected = [
        (len(candidates) == 15, "expected 15 candidate rules"),
        (len(summary) == 14, "expected 14 summary rows"),
        (pilot["selected_rule"] == "single|Qwen2.5-3B", "unexpected pilot-selected rule"),
        (int(pilot["dev_correct"]) == 17, "unexpected pilot dev score"),
        (int(pilot["test_correct"]) == 72, "unexpected pilot holdout score"),
        (int(pilot["best_single_test_correct"]) == 87, "unexpected holdout best-single score"),
        (int(pilot["posthoc_best_correct"]) == 95, "unexpected posthoc holdout best route"),
        (int(hash5["selected_correct"]) == 106, "unexpected hash5 CV score"),
        (
            hash5["selected_rule_counts"] == "majority_fallback|Qwen2.5-7B 8-bit=5",
            "unexpected hash5 selected-rule counts",
        ),
        (int(block40["selected_correct"]) == 84, "unexpected block40 CV score"),
    ]
    failures = [message for ok, message in expected if not ok]
    if failures:
        raise SystemExit("; ".join(failures))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--candidates-output", type=Path, default=DEFAULT_CANDIDATES_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_items(args.input)
    rules = build_rules()
    candidates = candidate_rows(rows, rules)
    summary = build_summary(rows, rules)
    assert_expected(summary, candidates)
    write_csv(args.candidates_output, candidates)
    write_csv(args.summary_output, summary)
    write_report(args.report_output, args.input, args.candidates_output, args.summary_output, summary)
    print(f"candidate_rules={len(candidates)}")
    print(f"summary_rows={len(summary)}")
    print(f"report={args.report_output}")


if __name__ == "__main__":
    main()
