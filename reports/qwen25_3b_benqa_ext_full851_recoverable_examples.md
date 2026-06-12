# Qwen2.5-3B BEnQA Extension Full851 Recoverable Banglish Misses

Updated: 2026-06-05

## Summary

- Recoverable reviewed-Banglish misses exported: 311
- Bangla and English correct: 96
- English-only recovery: 175
- Bangla-only recovery: 40
- CSV: `results/analysis/qwen25_3b_benqa_ext_full851_recoverable_banglish_misses.csv`

These are qualitative examples, not a separate statistical test. They are
useful for defense slides and error-analysis prose because they show the
same item becoming answerable under another script view.

## Example Rows

| ID | Gold | Correct scripts | Parsed answers | Banglish prompt snippet |
| --- | --- | --- | --- | --- |
| `benqa_ext_10th-Biology_0002` | D | English | BN=B; BG=A; EN=D | konotite souroshokti sthiti shoktirupe sonchit thake? A. oksijen B. pani C. karbon dai oksaid D. shbetosar Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0034` | A | English | BN=D; BG=D; EN=A | trakiyate paoya jay- i. siudo-stryatifaid aboroni tisyu ii. siliyajukt aboroni tisyu iii. kiuboyodal aboroni tisyu nicher konoti sothik? A. i o ii B. i o iii C. ii o iii D. i, ii o iii Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0045` | D | English | BN=B; BG=A; EN=D | kiser sahajye bhrun jorayur sathe songsthapit hoy? A. amoniyon B. roktonali C. ambilikal kord D. omora Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0065` | A | English | BN=C; BG=B; EN=A | nicher konoti C_{4} udbhid? A. akh B. am C. shapola D. joba Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0067` | B | English | BN=C; BG=C; EN=B | rotoner boyos 39 bochhor. tar ojon 69 keji ebong uchchota 170 se.mi.. rotoner kshetre projojy- A. shorirer ojon kom B. susbasthyer odhikari C. shorirer ojon otirikt D. otirikt motatb Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0069` | A | English | BN=C; BG=B; EN=A | jibanu bhokshon kore nicher kon konika? A. niutrofil B. iosinofil C. besofil D. thrombosait Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0084` | C | English | BN=B; BG=B; EN=C | jyanthofil thakole udbhid ki born dharon kore? A. lal B. nil C. holud D. komola Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0085` | D | English | BN=A; BG=C; EN=D | laisojomer kaj konoti? A. amish songshleshon B. khaddo sonchoy C. probah pother nirdeshona D. jibanu dhbongs Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0091` | C | Bangla | BN=C; BG=D; EN=D | sugarobit er mul ebong kander briddhir jony kon pushti upadan proyojon? A. boron B. ayoron C. klorin D. potashiyam Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0100` | C | Bangla, English | BN=C; BG=D; EN=C | akotin o mayosin protin kon ongganute thake? A. sentrojom B. raibojom C. koshokongkal D. kloroplast Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0102` | A | Bangla, English | BN=A; BG=B; EN=A | jibodeher shboson, rechon ityadi somporkit bijnan konoti? A. sharirobidya B. chikitosabijnan C. farmesi D. pranorosayon Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0120` | D | Bangla, English | BN=D; BG=B; EN=D | byakoteriyate kon ongganuti uposthit? A. maitokondriya B. plastid C. endoplajomik retikulam D. raibojom Answer with only A, B, C, or D. |
