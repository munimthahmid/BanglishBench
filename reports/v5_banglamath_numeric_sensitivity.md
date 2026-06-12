# Frozen-V5 BanglaMATH Numeric Sensitivity

Updated: 2026-06-11

## Scope

This no-spend audit asks whether BanglaMATH short-answer losses are mainly
caused by conservative answer normalization. It extracts numeric signatures
from the gold answer, parsed answer, and raw model output for the same
thesis-facing frozen-v5 Qwen rows.

- Item-level output: `results/analysis/v5_banglamath_numeric_sensitivity_items.csv`
- Summary table: `results/analysis/v5_banglamath_numeric_sensitivity_summary.csv`

A row has a full numeric-signature hit when all numeric values in the gold
answer appear in the parsed answer or raw output after Bengali digit,
fraction, and percent normalization. This is intentionally generous:
a raw hit can occur inside reasoning rather than the final answer, so it is
an upper bound on parser/unit sensitivity, not a replacement accuracy metric.

## Headline

- A generous raw numeric-signature credit does not erase the BanglaMATH
  reviewed-Banglish deficit for any thesis-facing Qwen row.
- Qwen3-4B raw numeric-signature hits are 10/56 for reviewed Banglish, 19/56 for Bangla, and 24/56 for English.
- Qwen2.5-7B 8-bit has 5/56 reviewed-Banglish raw hits versus 16/56 Bangla and 20/56 English; Qwen2.5-3B has 1/56 versus 10/56 and 10/56.
- Conservative unit and fraction normalization misses exist, especially in
  Bangla and English outputs, so BanglaMATH absolute accuracy should stay
  caveated. The cross-script Banglish gap is not explained by those misses.

## BanglaMATH Numeric Signature Summary

| Model | Variant | Correct | Parsed numeric signature | Raw numeric signature | Wrong raw signature hits | Wrong no-number outputs |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 5/56 | 10/56 | 10/56 | 5/51 | 1/51 |
| Qwen2.5-3B | Reviewed Banglish | 0/56 | 1/56 | 1/56 | 1/56 | 4/56 |
| Qwen2.5-3B | English | 5/56 | 9/56 | 10/56 | 5/51 | 3/51 |
| Qwen2.5-7B 8-bit | Bangla | 5/56 | 16/56 | 16/56 | 11/51 | 2/51 |
| Qwen2.5-7B 8-bit | Reviewed Banglish | 0/56 | 5/56 | 5/56 | 5/56 | 2/56 |
| Qwen2.5-7B 8-bit | English | 8/56 | 20/56 | 20/56 | 12/48 | 3/48 |
| Qwen3-4B | Bangla | 4/56 | 16/56 | 19/56 | 15/52 | 2/52 |
| Qwen3-4B | Reviewed Banglish | 2/56 | 5/56 | 10/56 | 8/54 | 10/54 |
| Qwen3-4B | English | 6/56 | 18/56 | 24/56 | 18/50 | 2/50 |

## Interpretation

- `Parsed numeric signature` is closest to a parser/unit-normalization
  sensitivity check. It credits answers such as a Latin-unit number when
  the exact evaluator keeps the row wrong.
- `Raw numeric signature` is more optimistic because it may credit numbers
  that appear during reasoning even when the final answer is absent or
  malformed.
- Reviewed Banglish remains the lowest row under both views for Qwen2.5-3B,
  Qwen2.5-7B 8-bit, and Qwen3-4B. This supports using BanglaMATH as a
  low-accuracy stress test with conservative scoring caveats, not as a
  parser-artifact explanation of the main gap.

## Wrong Rows With Parsed Numeric Signature Hits

| Model | Variant | Item | Gold | Parsed | Raw excerpt |
| --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | Bangla | `banglamath_0227` | `৭.৫ কিমি` | `7.5` | 7.5 |
| Qwen2.5-3B | English | `banglamath_0227` | `৭.৫ কিমি` | `7.5km` | 7.5km |
| Qwen2.5-3B | Bangla | `banglamath_0228` | `২/৫` | `40% একটি সাধারণ ভগ্নাংশে প্রকাশ করলে 4/10 হয়.` | 40% একটি সাধারণ ভগ্নাংশে প্রকাশ করলে 4/10 হয়. |
| Qwen2.5-3B | Bangla | `banglamath_0521` | `৭০ মিটার` | `70 meters` | 70 meters |
| Qwen2.5-3B | Bangla | `banglamath_0540` | `২১ মিটার` | `21 meters` | 21 meters |
| Qwen2.5-3B | English | `banglamath_0540` | `২১ মিটার` | `21 meters` | 21 meters |

## Qwen3 Reviewed-Banglish Raw Signature Hits

| Model | Variant | Item | Gold | Parsed | Raw excerpt |
| --- | --- | --- | --- | --- | --- |
| Qwen3-4B | Reviewed Banglish | `banglamath_0228` | `২/৫` | `40% ke sadharon bhognangshe prokash korole ki hoy` | 40% ke sadharon bhognangshe prokash korole ki hoy → 40% ke sadharon bhognangshe prokash korole ki hoy, ta holo 40% ke sadharon bhognangshe prokash korole ki hoy, jekhane "sadhar... |
| Qwen3-4B | Reviewed Banglish | `banglamath_0229` | `1.5` | `150` | 150% ke doshomik bhognangshe prokash korole ki hoy, tai 150% = 150/100 = 1.5 Doshomik bhognangshe prokash korle, 1.5 = 1.5 × 100 = 150 Teh, 150% ke doshomik bhognangshe prokash... |
| Qwen3-4B | Reviewed Banglish | `banglamath_0231` | `২০ টাকা` | `19.2` | 20% labhe 24 takay bikroy korle kroyomullo koto 24 er 20% = (20/100) × 24 = 4.8 Tehabe kroyomullo = 24 - 4.8 = 19.2 Final answer: 19.2 |
| Qwen3-4B | Reviewed Banglish | `banglamath_0233` | `৭ দিন` | `168 কাজ করা হয় 24 জনের মধ্যে → প্রতি জনের কাজ = 168 / 24 = 7` | 6 jon lok 28 dine kaj kore, 24 jon lok koto dine kore? 1. 6 jon lok 28 dine kaj kore → 6 × 28 = 168 কাজ 2. 24 jon lok er kaj kore? 168 কাজ করা হয় 24 জনের মধ্যে → প্রতি জনের কাজ... |
| Qwen3-4B | Reviewed Banglish | `banglamath_0519` | `৭৫০০ বর্গমিটার` | `75` | The question appears to be in a mix of Bengali and possibly a typo or miscommunication. However, interpreting it in a logical context: "ekti ayotokar baganer doirgho 150 mitar o... |

## Qwen3 Reviewed-Banglish Wrong Rows Without Numbers

| Model | Variant | Item | Gold | Parsed | Raw excerpt |
| --- | --- | --- | --- | --- | --- |
| Qwen3-4B | Reviewed Banglish | `banglamath_0181` | `সময় কমে যায়` | `{kajer poriman oporibortit thakle lok songkhya barale somoy ki hoy}` | {kajer poriman oporibortit thakle lok songkhya barale somoy ki hoy} |
| Qwen3-4B | Reviewed Banglish | `banglamath_0182` | `৬০০ টাকা` | `cannot be derived.` | The given text appears to be in a mix of Bengali and possibly a typo or miscommunication. It seems to be trying to express a calculation or comparison involving "keji chaler" (p... |
| Qwen3-4B | Reviewed Banglish | `banglamath_0227` | `৭.৫ কিমি` | `.` | The question appears to be in a mix of Bengali and English, and it seems to be asking about a sequence or pattern involving "bondhur durotto" (likely meaning "bondhur" or "pair"... |
| Qwen3-4B | Reviewed Banglish | `banglamath_0236` | `১২ টাকা` | `Unable to evaluate due to unclear or malformed input.` | The given text appears to be in a mix of Bengali and possibly a typo or miscommunication. It seems to describe a product (bolopener dam) with pricing and quantity details, but t... |
| Qwen3-4B | Reviewed Banglish | `banglamath_0518` | `১৫০ মিটার` | `Unable to evaluate due to nonsensical or corrupted input.` | The given text appears to be in a corrupted or nonsensical form, possibly due to a language or encoding issue. It does not form a coherent sentence in any known language, and th... |

