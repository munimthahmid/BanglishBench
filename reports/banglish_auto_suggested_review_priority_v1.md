# Auto-Suggested Banglish Human-Review Priority v1

Updated: 2026-05-28

## Purpose

This queue prioritizes automatic Banglish spelling suggestions for manual review. It is not a reviewed dataset; blank review fields are included so accepted edits can later be copied into the v5 workflow.

## Artifacts

- Review CSV: `data/slices/banglish_auto_suggested_review_priority_v1.csv`

## Counts

- Candidate rows: 140
- `banglamath`: 47
- `benqa`: 93

| Priority bucket | Items |
| --- | ---: |
| `both_wrong_single_edit` | 55 |
| `both_wrong_multi_edit` | 40 |
| `lower_priority` | 39 |
| `qwen25_wrong_multi_edit` | 4 |
| `qwen3_wrong_multi_edit` | 2 |

## Review Guidance

- Review `current_banglish_clean` against the Bangla/English source before accepting `auto_suggested_banglish_clean`.
- Fill `reviewed_banglish` only when the reviewed text should replace the current clean Banglish.
- Use `quality_label` values from the v5 workflow: `ok`, `minor_edit`, `major_edit`, or `bad`.

## Top Examples

### 1. banglamath_0538

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

Auto-suggested:

```text
ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto
Return only the final answer.
```

### 2. banglamath_0541

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

Auto-suggested:

```text
ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto
Return only the final answer.
```

### 3. banglamath_0549

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti baganer baire 2.5 mitar choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 mi o prosth 35 mi hoy
Return only the final answer.
```

Auto-suggested:

```text
ekti baganer baire 2.5 mitar chowra rasta thakle rastar khetrofol koto jodi baganer doirgho 50 mi o prostho 35 mi hoy
Return only the final answer.
```

### 4. banglamath_1688

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ekoti->ekti (1); korote->korte (1); penyaj->peyaj (5)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
kon ekoti biyer onushthane ranna korote baburchi o tar sohokormi mot 400ti penyaj katen. baburchi proti minite ontot 3ti penyaj ebong tar sohokormi proti minite ontot 2ti penyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age penyaj kata bondh, tobe ke kototi penyaj ketechhil ar kar kotokshon somoy legechhil?
Return only the final answer.
```

Auto-suggested:

```text
kon ekti biyer onushthane ranna korte baburchi o tar sohokormi mot 400ti peyaj katen. baburchi proti minite ontot 3ti peyaj ebong tar sohokormi proti minite ontot 2ti peyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age peyaj kata bondh, tobe ke kototi peyaj ketechhil ar kar kotokshon somoy legechhil?
Return only the final answer.
```

### 5. banglamath_0519

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti ayotakar baganer doirghy 150 mitar o prosth 50 mitar hole kshetrofol kot
Return only the final answer.
```

Auto-suggested:

```text
ekti ayotokar baganer doirgho 150 mitar o prostho 50 mitar hole khetrofol koto
Return only the final answer.
```

### 6. banglamath_0518

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ayotakar->ayotokar (1); doirghy->doirgho (2); ekoti->ekti (1); kot->koto (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti ayotakar baganer doirghy prosther tinogun ebong porisima 400 mitar hole baganer doirghy kot
Return only the final answer.
```

Auto-suggested:

```text
ekti ayotokar baganer doirgho prosther tinogun ebong porisima 400 mitar hole baganer doirgho koto
Return only the final answer.
```

### 7. banglamath_0540

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: doirghy->doirgho (2); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti ghorer doirghy prosther tinogun ebong kshetrofol 147 borgomitar hole ghorotir doirghy kot
Return only the final answer.
```

Auto-suggested:

```text
ekti ghorer doirgho prosther tinogun ebong khetrofol 147 borgomitar hole ghorotir doirgho koto
Return only the final answer.
```

### 8. benqa_8th-Math_0167

- Dataset: `benqa`
- Priority: `both_wrong_multi_edit`
- Suggestions: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Auto-suggested:

```text
ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

### 9. banglamath_0521

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti jomir doirghy 20 mitar o prosth 15 mitar hole tar porisima kot
Return only the final answer.
```

Auto-suggested:

```text
ekti jomir doirgho 20 mitar o prostho 15 mitar hole tar porisima koto
Return only the final answer.
```

### 10. banglamath_0522

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: choora->chowra (1); kot->koto (1); kshetrofol->khetrofol (1); thakole->thakle (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
jomir bhitore 2 mitar choora rasta thakole rastabade jomir kshetrofol kot
Return only the final answer.
```

Auto-suggested:

```text
jomir bhitore 2 mitar chowra rasta thakle rastabade jomir khetrofol koto
Return only the final answer.
```

### 11. banglamath_0526

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

Auto-suggested:

```text
ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto
Return only the final answer.
```

### 12. banglamath_0552

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrofol kot
Return only the final answer.
```

Auto-suggested:

```text
ekti samantoriker bhumi 90 goj o ucchota 50 goj hole tar khetrofol koto
Return only the final answer.
```

### 13. banglamath_0558

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: ayotakar->ayotokar (1); doirghy->doirgho (1); kot->koto (1); prosth->prostho (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
60 mitar dirgh ayotakar baganer doirghy prosther 3 gun hole prosth kot
Return only the final answer.
```

Auto-suggested:

```text
60 mitar dirgh ayotokar baganer doirgho prosther 3 gun hole prostho koto
Return only the final answer.
```

### 14. banglamath_1691

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: achhe->ache (1); ekoti->ekti (2); korote->korte (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
beru goyalar kachhe ekoti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekoti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korote chay. goyalar kachhe jedojesob patr achhe shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob?
Return only the final answer.
```

Auto-suggested:

```text
beru goyalar kachhe ekti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korte chay. goyalar kachhe jedojesob patr ache shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob?
Return only the final answer.
```

### 15. banglamath_0183

- Dataset: `banglamath`
- Priority: `both_wrong_multi_edit`
- Suggestions: achhe->ache (1); ekoti->ekti (1); kot->koto (1)
- v4 correctness: Qwen2.5=False, Qwen3=False

Current:

```text
ekoti chhatrabase 50 joner 15 diner khaddo mojud achhe. oi khadde 25 joner kot din cholobe
Return only the final answer.
```

Auto-suggested:

```text
ekti chhatrabase 50 joner 15 diner khaddo mojud ache. oi khadde 25 joner koto din cholobe
Return only the final answer.
```

