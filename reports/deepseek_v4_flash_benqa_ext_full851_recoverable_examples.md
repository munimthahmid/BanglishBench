# DeepSeek V4 Flash BEnQA Extension Full851 Recoverable Banglish Misses

Updated: 2026-06-05

## Summary

- Recoverable reviewed-Banglish misses exported: 380
- Bangla and English correct: 301
- English-only recovery: 51
- Bangla-only recovery: 28
- CSV: `results/analysis/deepseek_v4_flash_benqa_ext_full851_recoverable_banglish_misses.csv`

These are qualitative examples, not a separate statistical test. They are
useful for defense slides and error-analysis prose because they show the
same item becoming answerable under another script view.

## Example Rows

| ID | Gold | Correct scripts | Parsed answers | Banglish prompt snippet |
| --- | --- | --- | --- | --- |
| `benqa_ext_10th-Biology_0001` | C | Bangla, English | BN=C; BG=B; EN=C | salokosongshleshoner jony upojukt tapomatra konoti? A. 12\degree C - 25\degree C B. 17\degree C - 30\degree C C. 22\degree C - 35\degree C D. 27\degree C - 40\degree C Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0002` | D | Bangla, English | BN=D; BG=C; EN=D | konotite souroshokti sthiti shoktirupe sonchit thake? A. oksijen B. pani C. karbon dai oksaid D. shbetosar Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0018` | D | Bangla, English | BN=D; BG=B; EN=D | rokte joib ebong ojoib podarther poriman kot? A. 2-4% B. 3-5% C. 5-7% D. 8-9% Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0023` | A | Bangla | BN=A; BG=D; EN=D | nicher konoti khele kshariy mutr toiri hoy? A. apel B. katol machh C. gorur mangs D. chinabadam Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0032` | D | English | BN=C; BG=B; EN=D | kon fuler sugondh nei? A. golap B. rojonigondha C. sorisha D. patasheola Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0034` | A | Bangla, English | BN=A; BG=D; EN=A | trakiyate paoya jay- i. siudo-stryatifaid aboroni tisyu ii. siliyajukt aboroni tisyu iii. kiuboyodal aboroni tisyu nicher konoti sothik? A. i o ii B. i o iii C. ii o iii D. i, ii o iii Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0045` | D | Bangla, English | BN=D; BG=B; EN=D | kiser sahajye bhrun jorayur sathe songsthapit hoy? A. amoniyon B. roktonali C. ambilikal kord D. omora Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0049` | B | Bangla, English | BN=B; BG=C; EN=B | konoti protin songshleshon kore? A. kromoplast B. raibojom C. sentrojome D. goloji bostu Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0063` | B | Bangla, English | BN=B; BG=C; EN=B | dayatom kon rajyer jib? A. monera B. protista C. fanojai D. planoti Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0065` | A | Bangla, English | BN=A; BG=C; EN=A | nicher konoti C_{4} udbhid? A. akh B. am C. shapola D. joba Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0067` | B | Bangla, English | BN=B; BG=C; EN=B | rotoner boyos 39 bochhor. tar ojon 69 keji ebong uchchota 170 se.mi.. rotoner kshetre projojy- A. shorirer ojon kom B. susbasthyer odhikari C. shorirer ojon otirikt D. otirikt motatb Answer with only A, B, C, or D. |
| `benqa_ext_10th-Biology_0069` | A | Bangla, English | BN=A; BG=D; EN=A | jibanu bhokshon kore nicher kon konika? A. niutrofil B. iosinofil C. besofil D. thrombosait Answer with only A, B, C, or D. |
