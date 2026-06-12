# Frozen-V5 Subject And Grade Breakdown

Updated: 2026-06-11

This report refreshes the subject/grade spread analysis with the frozen-v5
reviewed Banglish outputs used in the release-facing main table. Bangla
and English outputs are reused because those fields did not change.

- Machine-readable summary: `results/analysis/validation200_v5_subject_breakdown.csv`
- Thesis table CSV: `results/tables/subject_breakdown_validation200_v5.csv`

## BEnQA Subject Breakdown

### Qwen2.5-3B

Reviewed Banglish is below Bangla in 7/13 BEnQA subject strata.

| Subject | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Biology | 12 | 5 | 0 | 3 | -5 |
| Biology-I | 11 | 3 | 2 | 7 | -1 |
| Biology-II | 11 | 3 | 4 | 6 | +1 |
| Chemistry | 11 | 3 | 4 | 7 | +1 |
| Chemistry-I | 11 | 4 | 2 | 5 | -2 |
| Chemistry-II | 11 | 2 | 5 | 6 | +3 |
| Math | 11 | 5 | 3 | 8 | -2 |
| Math-I | 11 | 3 | 3 | 2 | +0 |
| Math-II | 11 | 6 | 5 | 3 | -1 |
| Physics | 11 | 5 | 4 | 7 | -1 |
| Physics-I | 11 | 4 | 5 | 5 | +1 |
| Physics-II | 11 | 2 | 3 | 3 | +1 |
| Science | 11 | 4 | 1 | 4 | -3 |

### Qwen2.5-7B 8-bit

Reviewed Banglish is below Bangla in 8/13 BEnQA subject strata.

| Subject | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Biology | 12 | 5 | 6 | 9 | +1 |
| Biology-I | 11 | 6 | 2 | 8 | -4 |
| Biology-II | 11 | 6 | 5 | 6 | -1 |
| Chemistry | 11 | 3 | 1 | 6 | -2 |
| Chemistry-I | 11 | 5 | 2 | 7 | -3 |
| Chemistry-II | 11 | 5 | 4 | 9 | -1 |
| Math | 11 | 5 | 2 | 9 | -3 |
| Math-I | 11 | 5 | 6 | 6 | +1 |
| Math-II | 11 | 2 | 2 | 2 | +0 |
| Physics | 11 | 4 | 5 | 8 | +1 |
| Physics-I | 11 | 6 | 5 | 6 | -1 |
| Physics-II | 11 | 3 | 2 | 4 | -1 |
| Science | 11 | 5 | 5 | 6 | +0 |

### Qwen3-4B

Reviewed Banglish is below Bangla in 12/13 BEnQA subject strata.

| Subject | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Biology | 12 | 5 | 3 | 4 | -2 |
| Biology-I | 11 | 6 | 3 | 6 | -3 |
| Biology-II | 11 | 6 | 1 | 4 | -5 |
| Chemistry | 11 | 7 | 4 | 8 | -3 |
| Chemistry-I | 11 | 7 | 5 | 9 | -2 |
| Chemistry-II | 11 | 7 | 2 | 8 | -5 |
| Math | 11 | 5 | 2 | 6 | -3 |
| Math-I | 11 | 5 | 4 | 5 | -1 |
| Math-II | 11 | 6 | 8 | 5 | +2 |
| Physics | 11 | 8 | 6 | 9 | -2 |
| Physics-I | 11 | 6 | 4 | 6 | -2 |
| Physics-II | 11 | 3 | 2 | 4 | -1 |
| Science | 11 | 5 | 3 | 8 | -2 |

## BanglaMATH Grade Breakdown

### Qwen2.5-3B

Reviewed Banglish is below Bangla in 2/3 BanglaMATH grade strata.

| Grade | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eight | 16 | 0 | 0 | 0 | +0 |
| seven | 20 | 2 | 0 | 1 | -2 |
| six | 20 | 3 | 0 | 4 | -3 |

### Qwen2.5-7B 8-bit

Reviewed Banglish is below Bangla in 2/3 BanglaMATH grade strata.

| Grade | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eight | 16 | 0 | 0 | 1 | +0 |
| seven | 20 | 2 | 0 | 1 | -2 |
| six | 20 | 3 | 0 | 6 | -3 |

### Qwen3-4B

Reviewed Banglish is below Bangla in 1/3 BanglaMATH grade strata.

| Grade | n | Bangla | Reviewed Banglish | English | Banglish - Bangla |
| --- | ---: | ---: | ---: | ---: | ---: |
| Eight | 16 | 2 | 2 | 2 | +0 |
| seven | 20 | 0 | 0 | 1 | +0 |
| six | 20 | 2 | 0 | 3 | -2 |

## Interpretation

- Qwen3-4B reviewed Banglish remains below native Bangla in 12/13 BEnQA subject strata.
- Qwen2.5-7B 8-bit reviewed Banglish is below native Bangla in 8/13 BEnQA subject strata.
- Qwen2.5-3B is more mixed by subject, matching its weaker all-200 interval.
- BanglaMATH grade strata remain low-accuracy and are better treated as
  hard stress-test evidence than fine-grained subject evidence.
- Subject and grade strata are small, so this is descriptive support rather
  than a separate primary statistical claim.
