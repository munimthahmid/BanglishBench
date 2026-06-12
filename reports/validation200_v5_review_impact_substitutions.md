# Validation-200 v5 Review Impact Substitutions

Updated: 2026-05-28

## Inputs

- Impact ranking: `results/analysis/validation200_v5_review_impact_ranking.csv`
- Substitution CSV: `results/analysis/validation200_v5_review_impact_substitutions.csv`

This report helps batch review repeated suggested substitutions. It is
not an auto-accept list; every row still needs source-context review.

## Top Substitutions By Impact

| Substitution | Rows | Occurrences | Tier-1 rows | Test rows | Max score | Mean score | Example IDs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `konoti` -> `konti` | 56 | 57 | 23 | 45 | 177 | 110.9 | benqa_12th-Chemistry-II_0228; benqa_12th-Physics-II_0046; benqa_10th-Physics_0021; benqa_8th-Science_0202; benqa_12th-Biology-II_0287 |
| `kot` -> `koto` | 72 | 72 | 17 | 55 | 173 | 115.3 | benqa_8th-Math_0167; banglamath_0526; banglamath_0230; banglamath_0231; benqa_8th-Math_0085 |
| `ekoti` -> `ekti` | 37 | 40 | 13 | 26 | 177 | 133.9 | benqa_10th-Math_0044; benqa_12th-Chemistry-II_0228; benqa_8th-Math_0167; banglamath_0526; benqa_12th-Biology-I_0265 |
| `kshetrofol` -> `khetrofol` | 13 | 14 | 6 | 10 | 170 | 137.8 | banglamath_0526; banglamath_0552; banglamath_0538; banglamath_0541; banglamath_0549 |
| `doirghy` -> `doirgho` | 11 | 13 | 5 | 8 | 173 | 136.9 | benqa_8th-Math_0167; banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0540 |
| `prosth` -> `prostho` | 9 | 9 | 4 | 7 | 173 | 138 | benqa_8th-Math_0167; banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0519 |
| `ayotakar` -> `ayotokar` | 7 | 7 | 3 | 5 | 173 | 138.9 | benqa_8th-Math_0167; banglamath_0538; banglamath_0541; banglamath_0519; banglamath_0558 |
| `achhe` -> `ache` | 6 | 6 | 3 | 5 | 177 | 145.5 | benqa_10th-Math_0044; benqa_12th-Biology-I_0265; benqa_8th-Science_0127; banglamath_1691; banglamath_0183 |
| `thakole` -> `thakle` | 5 | 5 | 3 | 4 | 144 | 135.8 | banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0522; banglamath_0181 |
| `choora` -> `chowra` | 4 | 4 | 3 | 3 | 144 | 139.5 | banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0522 |
| `kshetre` -> `khetre` | 5 | 5 | 2 | 5 | 171 | 120.8 | benqa_12th-Physics-II_0046; benqa_12th-Physics-I_0254; benqa_12th-Math-I_0218; benqa_12th-Chemistry-I_0227; benqa_12th-Physics-II_0085 |
| `uchchota` -> `ucchota` | 2 | 2 | 2 | 2 | 170 | 159 | banglamath_0526; banglamath_0552 |
| `korote` -> `korte` | 7 | 10 | 1 | 5 | 142 | 118.7 | banglamath_1688; benqa_10th-Physics_0106; banglamath_1691; banglamath_0184; banglamath_0189 |
| `penyaj` -> `peyaj` | 1 | 5 | 1 | 1 | 142 | 142 | banglamath_1688 |

## Review Use

Start with high tier-1/test-row substitutions, but verify each item
against Bangla and English because the same spelling edit can be correct
in one context and too aggressive in another.
