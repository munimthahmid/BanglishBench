# Chapter 4 Main Script-Gap Results Draft

Updated: 2026-05-31

## 4.1 Chapter Goal

This chapter answers the primary empirical question: when the same Bangla
educational item is written in native Bangla script, clean Latin-script
Banglish, or English, do model answers change?

The main evidence comes from validation-200. Each comparison is paired by item
id, so script-gap estimates measure how the same questions change across script
views rather than comparing different samples.

## 4.2 Main Validation-200 Results

The primary result is that competent Qwen baselines are worse on reviewed
Banglish than on native Bangla and English. Bangla and English are unchanged
from the controlled historical slice; the Banglish column uses the completed
frozen-v5 reruns.

| Model | Bangla | Reviewed Banglish | English | Banglish - Bangla | Banglish - English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] |
| Qwen3-4B | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] |

Qwen3-4B is the strongest current open baseline and shows the largest
Banglish-below-Bangla drop: 80/200 in Bangla versus 49/200 in Banglish. The
paired interval remains far below zero, so this is not just aggregate noise.

Qwen2.5-7B 8-bit confirms that the Qwen2.5 script gap persists at a stronger
scaling point. Qwen2.5-3B retains a -6.5-point all-200 deficit, but its
reviewed-v5 interval reaches zero. Its historical v3 interval and the
strict-197 sensitivity remain negative, so the final claim should preserve
this model-specific qualification.

The English column is also important. Banglish uses Latin characters, but the
models are much stronger on English than on Banglish. Therefore, the issue is
not simply that Latin script is easy and Bengali script is hard. Bengali content
written in Latin script remains a distinct robustness condition.

Primary artifacts:

- `results/tables/main_script_gap_validation200_v5.csv`
- `reports/main_results_validation200_v5.md`
- `reports/thesis_results_dashboard.md`
- `reports/figures/main_script_gap.svg`

## 4.3 Dataset-Level Breakdown

BEnQA carries most of the frozen-v5 script-gap signal because current open
models have non-trivial task competence on BEnQA. BanglaMATH remains difficult
across all scripts, so the release-facing interpretation should keep it as a
stress test rather than as fine-grained grade evidence.

| Model | Dataset | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | BEnQA | 49/144 | 41/144 | 66/144 |
| Qwen2.5-3B | BanglaMATH | 5/56 | 0/56 | 5/56 |
| Qwen2.5-7B 8-bit | BEnQA | 60/144 | 47/144 | 86/144 |
| Qwen2.5-7B 8-bit | BanglaMATH | 5/56 | 0/56 | 8/56 |
| Qwen3-4B | BEnQA | 76/144 | 47/144 | 82/144 |
| Qwen3-4B | BanglaMATH | 4/56 | 2/56 | 6/56 |

This matters for interpretation. The thesis should not use BanglaMATH to claim
fine-grained grade-level script effects under current open models. It should use
BanglaMATH as a hard stress test and use BEnQA as the clearer source of the
orthographic robustness signal.

The paired interval view sharpens this point. On BEnQA, Qwen3-4B has a
reviewed-Banglish-minus-Bangla delta of -20.1 points with CI [-28.5, -11.8].
Qwen2.5-3B and Qwen2.5-7B 8-bit are also directionally negative on BEnQA, but
their dataset-only intervals reach zero. BanglaMATH deltas are negative or near
zero, yet the models answer so few BanglaMATH items correctly that it remains a
low-accuracy stress test rather than the clearest dataset-level proof.

Exact paired sign tests give a complementary discordant-pair view. On the
all-200 Banglish-versus-Bangla comparison, Qwen2.5-7B 8-bit has 19 Banglish
gains and 37 Banglish losses, with a two-sided exact p-value of 0.0222.
Qwen3-4B has 8 gains and 39 losses, p<0.0001. Qwen2.5-3B again remains the
weakest row, with 15 gains and 28 losses, p=0.0660, so it should keep the
CI-reaches-zero qualification.

Clustered resampling addresses a stronger dependence concern by resampling
BEnQA subjects and BanglaMATH grades rather than individual items. Under this
cluster bootstrap, the all-200 Banglish-minus-Bangla interval stays below zero
for Qwen2.5-7B 8-bit and Qwen3-4B. Qwen2.5-3B remains directionally negative
but its cluster interval reaches zero, consistent with the main qualification
for that row. BanglaMATH has only three grade clusters, so its cluster
intervals should remain descriptive.

A leave-one-BEnQA-subject stability check further shows that this support is
not a single-subject artifact. Dropping any one BEnQA subject keeps the
reviewed-Banglish-minus-Bangla delta negative for all three thesis-facing Qwen
rows. The Qwen3-4B leave-one-subject range is -23.3 to -18.0 points; the
Qwen2.5 rows remain smaller but negative under all 13 drops.

Subject-macro balancing addresses a related weighting question. Equal-weighting
the 13 BEnQA subjects keeps reviewed Banglish below Bangla for all three
thesis-facing Qwen rows. Qwen3-4B is -20.2 points with a subject-bootstrap CI
[-28.6, -11.2], and Qwen2.5-7B 8-bit is -9.2 points with CI [-16.8, -1.6].
Qwen2.5-3B remains the qualified row at -5.3 points with CI [-15.2, +4.2].

An answer-format audit checks a different validity concern. Qwen2.5-3B has no
format failures across the 600 thesis-facing outputs. Qwen2.5-7B 8-bit has two
reviewed-Banglish BEnQA MCQ format failures; even crediting both as correct
leaves an all-200 Banglish-Bangla gap of -8.0 points. Qwen3-4B has more BEnQA
format failures in English and Bangla than in reviewed Banglish, so parser
failure does not explain the Qwen3 gap.

A BEnQA choice-bias audit separates malformed choices from systematic option
preferences. Qwen2.5-3B and Qwen2.5-7B do not collapse to a single
reviewed-Banglish option label: their largest Banglish option shares are 38.9%
and 39.6%. Qwen3-4B does show a script-conditioned failure mode, predicting D
on 111/144 reviewed-Banglish BEnQA rows even though the gold distribution has
D on only 39/144 rows. This should be reported as an important failure pattern
for Qwen3, not as a parser artifact or as an explanation for the Qwen2.5 gaps.

A distractor-transition audit strengthens that point. Among BEnQA misses where
Bangla or English is correct, reviewed Banglish emits a valid wrong option in
162/164 model-item cases. The Qwen2.5 wrong choices remain distributed, while
Qwen3 selects D on 44/55 recoverable reviewed-Banglish misses. Across items,
27/50 cases with at least two valid recoverable Banglish misses share the same
wrong option across models.

A gold-label balance sensitivity check makes the MCQ interpretation sharper.
After averaging accuracy across A/B/C/D gold-label strata, reviewed Banglish
remains below Bangla and English for all three thesis-facing Qwen rows.
Qwen3-4B is -21.7 points below Bangla on the balanced metric and -29.5 points
on the non-D slice, where option-D over-selection cannot help. Qwen2.5-3B and
Qwen2.5-7B 8-bit remain directionally negative under balancing; keep their
interval qualifications and use the result as sensitivity support.

A cross-model item-consensus audit summarizes the same paired result across the
three thesis-facing Qwen rows. Over 600 model-item slots, reviewed Banglish is
correct 137 times, compared with 199 for Bangla and 253 for English. Resampling
items as paired clusters gives a -10.3-point Banglish-minus-Bangla consensus
delta with CI [-14.7, -6.3], and a -19.3-point Banglish-minus-English delta
with CI [-25.0, -13.7].

The recoverability source decomposition adds one more guardrail for
interpretation. Of 463 reviewed-Banglish misses across the 600 model-item
slots, 185 are recoverable by Bangla or English and 278 are all-script hard.
Native Bangla participates in 104 recoverable misses, English in 157, and both
alternate scripts recover 76. Thus the recoverability evidence is not merely an
English-only effect, although English is the stronger alternate view overall.

The consensus result is not carried by a single Qwen row. In a leave-one-model
stability audit, every two-model subset keeps reviewed Banglish below both
Bangla and English on the all-200 slice and on BEnQA. On all-200, the
Banglish-minus-Bangla pairwise range is -7.8 to -12.2 points, with all
item-bootstrap intervals below zero.

A composition-sensitivity audit checks whether the gap is only a consequence
of number-heavy or formula-heavy educational rows. In the 61 no-digit rows, all
three Qwen rows keep reviewed Banglish below both Bangla and English; the
Banglish-minus-Bangla range is -13.1 to -32.8 points. The 107-row
no-formula/operator subset is also negative for all three Qwen rows. These are
not natural-Banglish samples, but they show that the release-facing result is
not solely a numeric/formula artifact.

Primary artifacts:

- `reports/main_results_validation200_v5.md`
- `reports/subject_breakdown_validation200_v5.md`
- `reports/v5_dataset_gap_intervals.md`
- `reports/v5_paired_sign_tests.md`
- `reports/v5_clustered_gap_robustness.md`
- `reports/v5_benqa_subject_stability.md`
- `reports/v5_benqa_subject_balance.md`
- `reports/v5_answer_format_audit.md`
- `reports/v5_benqa_choice_bias.md`
- `reports/v5_benqa_label_balance.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_item_consensus.md`
- `reports/v5_consensus_stability.md`
- `reports/v5_composition_sensitivity.md`

## 4.4 Model Scaling And Breadth

The script gap becomes most interpretable once a model has enough task
competence. The weakest model, Qwen2.5-0.5B, is noisy and does not provide a
useful anchor. Qwen2.5-1.5B shows a clear Banglish-vs-English gap but weaker
Banglish-vs-Bangla separation. Qwen2.5-3B and Qwen2.5-7B show reliable
Banglish-below-Bangla drops.

Qwen3 shows a similar competence threshold. Qwen3-1.7B no-thinking shows a
large Banglish-vs-English gap but no reliable Banglish-below-Bangla gap.
Qwen3-4B shows the strongest script-gap result.

Phi-3.5-mini is an important non-Qwen contrast. It scores 38/200 in Bangla,
40/200 in Banglish, and 80/200 in English. It does not replicate the
Banglish-below-Bangla ordering, but it does show that Banglish is much harder
than English. This constrains the thesis claim: the Banglish-below-Bangla result
is strongest for competent Qwen baselines, while the broader pattern is that
script/language choice strongly changes model behavior.

Primary artifacts:

- `results/tables/model_family_scaling_validation200.csv`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/figures/main_script_gap.svg`

## 4.5 Robustness To Banglish Cleanup

The script-gap result is not removed by cleaning known romanization artifacts.
Validation-200 v4 changes 38/200 Banglish fields and removes targeted artifact
classes. Qwen2.5-3B moves from 38/200 to 39/200, and Qwen3-4B moves from
46/200 to 47/200. A broader automatic suggestion candidate changes each model
by only one additional item.

This does not prove the rule-based Banglish is fully natural. It does show that
the main validation-200 script-gap conclusion is not driven by the specific v3
artifact classes targeted by v4 or by the broader automatic suggestions tested
so far.

The frozen v5 review provides a stronger final sensitivity check. After 140
queued Banglish rows were reviewed, Qwen2.5-3B moves from 39/200 on v4 to
41/200 on v5, a +1.0-point change with CI [-1.0, +3.0]. Qwen3-4B moves from
47/200 to 49/200, a +1.0-point change with CI [0.0, +2.5]. Human-reviewed
cleanup slightly improves both required models. The pinned-stack Qwen2.5-7B
8-bit rerun
moves from 48/200 to 47/200, a -0.5-point change with CI [-3.5, +2.5]. Across
all three reruns, reviewed cleanup does not erase the main gap.

The separate strict-197 denominator sensitivity excludes the three flagged
source-quality rows without replacing the preregistered all-200 main policy.
Reviewed Banglish remains below native Bangla for Qwen2.5-3B (-7.1 points,
CI [-13.2, -1.0]), Qwen3-4B (-15.7 points, CI [-22.3, -9.6]), and
Qwen2.5-7B 8-bit (-9.6 points, CI [-16.8, -2.5]). The denominator choice
therefore does not drive the core conclusion.

Primary artifacts:

- `reports/v4_banglish_sensitivity_validation200.md`
- `reports/validation200_v4_auto_suggested_sensitivity.md`
- `results/tables/auto_suggested_banglish_sensitivity.csv`
- `results/tables/v5_reviewed_banglish_sensitivity.csv`
- `results/analysis/qwen25_validation200_v5_vs_v4_banglish.md`
- `results/analysis/qwen3_validation200_v5_vs_v4_banglish.md`
- `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish.md`
- `reports/v5_bad_row_policy_sensitivity.md`

## 4.6 Robustness To Deterministic Noise

The deterministic noisy-Banglish condition does not explain the main clean
Banglish gap. On validation-200, Qwen2.5-3B scores 38/200 on clean Banglish and
41/200 on noisy Banglish. Qwen3-4B scores 46/200 on both clean and noisy
Banglish. The current noise generator is therefore not the source of the
observed gap.

This should not be overclaimed. Natural Banglish spelling variation is broader
than the deterministic noise generator. The result only says that this
particular synthetic noise condition does not create the main deficit.

Primary artifact:

- `reports/noisy_banglish_validation200.md`

## 4.7 Subject Spread

Qwen3's BEnQA Banglish deficit is broad across subject strata under the
reviewed-v5 Banglish slice. Qwen3 reviewed Banglish is below Bangla in 12 of
13 BEnQA subject strata, with only Math-II slightly positive. Qwen2.5-7B 8-bit
is below Bangla in 8 of 13 BEnQA strata, and Qwen2.5-3B is more mixed at 7 of
13. The strata are small, so this should be treated as descriptive support
rather than a separate statistical claim.

Primary artifact:

- `reports/subject_breakdown_validation200_v5.md`

## 4.8 Chapter Conclusion

The main result is a paired orthographic robustness gap. Competent Qwen models
answer substantially fewer validation-200 items correctly when the same Bangla
content is written in reviewed Latin-script Banglish rather than native Bangla
script or English. The effect survives targeted Banglish cleanup, broader
automatic spelling suggestions, and the current deterministic noisy-Banglish
stress test.

The claim remains bounded. Banglish is not universally below Bangla for every
model tested, and the reviewed slice is still controlled educational Banglish
rather than a natural user corpus. The strongest thesis-safe statement is that
controlled Latin-script Banglish exposes a robust weakness in the competent
open Qwen baselines, and that this weakness is undermeasured by standard
Bangla-vs-English evaluation.
