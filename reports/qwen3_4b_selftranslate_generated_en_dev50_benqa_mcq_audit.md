# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq.jsonl`
- Item audit CSV: `results/analysis/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq_audit_items.csv`
- Summary CSV: `results/analysis/qwen3_4b_selftranslate_generated_en_dev50_benqa_mcq_audit_summary.csv`

## Counts

- Expected prompt rows: 36
- Missing outputs: 0
- Extra output keys: 0
- Hard-fail rows: 16
- Warning rows: 18

| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benqa | generated_en | 36 | 16 | 18 | 0 | 5 | 16 | 0 | 0 | 0 |

## First Hard Fails

- `benqa_12th-Math-II_0234` `generated_en` failures=digits,formulas preview=If x² - 4x + 3 = 0 has roots α and β, then what is the value of 1/α + 1/β?   A. 4/3   B. 3/4   C. -4/3   D. -3/4
- `benqa_12th-Biology-II_0119` `generated_en` failures=formulas preview=Which of the following is a type of water channel?   A. glaidin   B. somarosonting   C. luping   D. hanta
- `benqa_12th-Math-I_0202` `generated_en` failures=formulas preview=∫ (cosx / √(sinx)) dx = kot?   A. 2√(cosx) + c   B. 2√(sinx) + c   C. (1/2) √(cosx) + c   D. (1/2) √(sinx) + c
- `benqa_12th-Math-I_0088` `generated_en` failures=formulas preview=x minus a divided by x times a minus x   A. \frac{a}{x}   B. \frac{x}{a}   C. \frac{1}{x}   D. \frac{1}{ax}   Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-I_0303` `generated_en` failures=formulas preview=Which of the following is the strongest acid?   A. HF   B. HCl   C. HBr   D. HI   Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0054` `generated_en` failures=formulas preview=The functional group in the compound is- A. \text{-CONH_{2}} B. \text{-COX} C. \text{-CHO} D. \text{-NH_{2}} Answer with only A, B, C, or D.
- `benqa_12th-Physics-II_0088` `generated_en` failures=formulas preview=Which of the following can be easily understood? i. Protisoron ii. Protifolon iii. Somoborton?   A. i and ii   B. i and iii   C. ii and iii   D. i, ii and iii
- `benqa_12th-Chemistry-I_0140` `generated_en` failures=digits,formulas preview=CaF₂-solubility is given as 0.00655 g/L. What is the solubility product (Ksp) of CaF₂?   A. 3.7×10⁻¹³   B. 2.048×10⁻¹⁰   C. 3.7×10⁻¹²   D. 2.048×10⁻¹¹   Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0120` `generated_en` failures=formulas preview=What is the equation of the line passing through the point (3, -4) and parallel to the x-axis?   A. y - 3 = 0   B. y + 3 = 0   C. y - 4 = 0   D. y + 4 = 1   Answer with only A, B, C, or D.
- `benqa_10th-Math-II_0367` `generated_en` failures=formulas preview=If a single independent event is performed once, what is the probability of a simple event occurring?   A. \frac{1}{6}   B. \frac{1}{3}   C. \frac{1}{2}   D. \frac{2}{3}
- `benqa_10th-Chemistry_0388` `generated_en` failures=digits,formulas preview=What is the electron configuration of chromium in the +3 oxidation state?   A. 3s²3p⁶3d⁵4s¹   B. 3s²3p⁶3d³4s²   C. 3s²3p⁶3d²4s²   D. 3s²3p⁶3d¹4s²   Answer with only A, B, C, or D.
- `benqa_10th-Physics_0055` `generated_en` failures=formulas preview=In which type of situation is an abortion performed?   A. sthiti ghorshon   B. goti ghorshon   C. abort ghorshon   D. probahi ghorshon
- `benqa_12th-Chemistry-II_0305` `generated_en` failures=digits,formulas preview=What is the RMS speed of O₂ at 27°C?   A. 453.23 ms^{-1}   B. 463.34 ms^{-1}   C. 473.45 ms^{-1}   D. 483.56 ms^{-1}
- `benqa_8th-Science_0024` `generated_en` failures=formulas preview=In which phase of mitosis do chromosomes become visible and get aligned at the equator of the cell?   A. prophase   B. metaphase   C. anaphase   D. telophase
- `benqa_10th-Math_0032` `generated_en` failures=formulas preview=(√3)^(x+2) = 27, what is the value of x?   A. 6   B. 4   C. 3   D. 2   Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0240` `generated_en` failures=digits,formulas preview=CH₃ - CH₂ - COONa + NaOH →[CaO, Δ] A + Na₂CO₃. What is the name of this reaction?   A. Decarboxylation reaction   B. Double carboxylation reaction   C. Decarboxylation fusion reaction   D. Friedel-Crafts reaction   Answe

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
