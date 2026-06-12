# Reviewed-Banglish Recoverable-Miss Error Taxonomy

Updated: 2026-06-11

Rule-assisted coding of all 164 recoverable BEnQA reviewed-Banglish
misses across the three Qwen models (items wrong under Banglish but
correct under Bangla or English on the same item). Categories are assigned
by the deterministic rules in `scripts/analyze_banglish_error_taxonomy.py`.

- Coding sheet: `results/analysis/banglish_error_taxonomy.csv`

| Category | Count | Share |
| --- | ---: | ---: |
| Named-entity / technical-term corruption | 58 | 35.4% |
| Romanized-word ambiguity | 51 | 31.1% |
| Number / unit / formula misread | 53 | 32.3% |
| Option-format failure | 2 | 1.2% |
| **Total** | **164** | **100%** |

## Named-entity / technical-term corruption

- **Qwen2.5-3B-Instruct** `benqa_10th-Biology_0128` (gold A, Banglish parsed C, recovered by Bangla+English):
  > ister shboson prokriyay konti utoponn hoy? | A. lyakotik esid | B. glukoj | C. oksalo asitik esid | D. glisarik esid
- **Qwen2.5-3B-Instruct** `benqa_10th-Biology_0149` (gold B, Banglish parsed A, recovered by Bangla):
  > konotir prantiy prachir gole noler srishti hoy? | A. sibhokosh | B. bhesel | C. trakid | D. songgikosh

## Romanized-word ambiguity

- **Qwen2.5-3B-Instruct** `benqa_10th-Chemistry_0194` (gold D, Banglish parsed C, recovered by English):
  > nicher kon mouloti odhik sokriy? | A. O | B. P | C. N | D. F
- **Qwen2.5-3B-Instruct** `benqa_10th-Physics_0280` (gold B, Banglish parsed A, recovered by English):
  > tamar rodhokotto konti? | A. 1.6 \times 10^{-8}\Omega m | B. 1.68 \times 10^{-8}\Omega m | C. 2.44 \times 10^{-8}\Omega m | D. 5.5 \times 10^{-8}\Omega m

## Number / unit / formula misread

- **Qwen2.5-3B-Instruct** `benqa_10th-Biology_0057` (gold C, Banglish parsed D, recovered by Bangla):
  > goni saheb tar bagane emon kichhu gachh lagiyechhen jar CO_{2} bijaroner prothom sthayi podarth oksalo esitik esid. goni saheb lagiyechhen- i. bhutta ii. begun iii. akh nicher konti sothik? | A. i o ii | B. ii o iii | C. i o iii | D. i, ii 
- **Qwen2.5-3B-Instruct** `benqa_10th-Biology_0215` (gold B, Banglish parsed D, recovered by English):
  > C_{6}H_{12}O_{6}\xarrowright{enojaim}C_{3}H_{4}O_{3} uddipoker prokriyati- i. sobat o obat shbosoner prothom dhap ii. kosher maitokondriyay ghote thake iii. ete nit onu ATP utoponn hoy nicher konti sothik? | A. i o ii | B. i o iii | C. ii o

## Option-format failure

- **Qwen2.5-7B-Instruct** `benqa_10th-Chemistry_0110` (gold C, Banglish parsed , recovered by Bangla+English):
  > chuner panir songket konti? | A. CaCO_{3} | B. CaO | C. Ca(OH)_{2} | D. Ca(HCO_{3})_{2}
- **Qwen2.5-7B-Instruct** `benqa_12th-Physics-I_0133` (gold C, Banglish parsed , recovered by Bangla+English):
  > \frac{3}{2} mol gyaser jony adorsh gyas somikoron hobe konti? | A. 3PV = 2RT | B. 2PV = \frac{1}{3} RT | C. 2PV = 3RT | D. \frac{PV}{RT}=\frac{2}{3}
