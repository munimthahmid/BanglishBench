# Qwen2.5-3B BEnQA Extension Pilot130 Recoverable Banglish Misses

Updated: 2026-06-05

## Summary

- Recoverable reviewed-Banglish misses exported: 49
- Bangla and English correct: 17
- English-only recovery: 26
- Bangla-only recovery: 6
- CSV: `results/analysis/qwen25_3b_benqa_ext_pilot130_recoverable_banglish_misses.csv`

These are qualitative examples, not a separate statistical test. They are
useful for defense slides and error-analysis prose because they show the
same item becoming answerable under another script view.

## Example Rows

| ID | Gold | Correct scripts | Parsed answers | Banglish prompt snippet |
| --- | --- | --- | --- | --- |
| `benqa_ext_10th-Biology_0002` | D | English | BN=B; BG=A; EN=D | konotite souroshokti sthiti shoktirupe sonchit thake? A. oksijen B. pani C. karbon dai oksaid D. shbetosar Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0091` | C | Bangla | BN=C; BG=D; EN=D | sugarobit er mul ebong kander briddhir jony kon pushti upadan proyojon? A. boron B. ayoron C. klorin D. potashiyam Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0100` | C | Bangla, English | BN=C; BG=D; EN=C | akotin o mayosin protin kon ongganute thake? A. sentrojom B. raibojom C. koshokongkal D. kloroplast Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0196` | C | English | BN=D; BG=D; EN=C | chalota kon dhoroner fol? A. jougik B. guchchh C. oprokrit D. prokrit Answer with only A, B, C, or D. |
| `benqa_ext_10th-Chemistry_0095` | D | English | BN=B; BG=B; EN=D | CH_{3} - C \equiv CH jougotir IUPAC nam ki? A. propail B. propen C. propin D. propain Answer with only A, B, C, or D. |
| `benqa_ext_10th-Chemistry_0232` | A | Bangla, English | BN=A; BG=D; EN=A | kon mouler poromanute niutron nei? A. H B. He C. Li D. Be Answer with only A, B, C, or D. |
| `benqa_ext_10th-Chemistry_0285` | B | English | BN=D; BG=D; EN=B | ghonibhoboner kshetre- i. podarth taposhokti nirgot kore ii. konar gotishokti briddhi pay iii. ayoton hras pay nicher konoti sothik? A. i o ii B. i o iii C. ii o iii D. i, ii o iii Answer with only A, B, C, or D. |
| `benqa_ext_10th-Chemistry_0376` | B | English | BN=A; BG=D; EN=B | konoti prakritik polimar? A. polithin B. rabar C. pibhisi D. polipropin Answer with only A, B, C, or D. |
| `benqa_ext_10th-Math-II_0119` | B | English | BN=D; BG=D; EN=B | 8^{a} = 64^{b) hole a:b er man nicher konoti? A. 1:02 B. 2:01 C. 2:03 D. 3:02 Answer with only A, B, C, or D. |
| `benqa_ext_10th-Math_0258` | A | English | BN=B; BG=B; EN=A | 0.0625 songkhyati sadharon loger purnok kot? A. \bar{2} B. \bar{1} C. 1 D. 2 Answer with only A, B, C, or D. |
| `benqa_ext_10th-Physics_0180` | B | Bangla, English | BN=B; BG=D; EN=B | apekshik truti- i. ek dhoroner onupat ii. sotyikarer trutir porimap iii. sadharon skeler tulonay bharniyar skele kom hoy nicher konoti sothik? A. i and ii B. i and iii C. ii and iii D. i, ii and iii Answer with only A... |
| `benqa_ext_10th-Physics_0227` | A | Bangla, English | BN=A; BG=B; EN=A | obotol dorpone fokas tol o prodhan oksher modhyoborti koner man kot? A. 90\degree B. 180\degree C. 270\degree D. 360\degree Answer with only A, B, C, or D. |
