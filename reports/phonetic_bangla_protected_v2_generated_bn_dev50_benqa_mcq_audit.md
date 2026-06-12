# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn_audit_summary.csv`

## Counts

- Expected prompt rows: 36
- Missing outputs: 0
- Extra output keys: 0
- Hard-fail rows: 16
- Warning rows: 0

| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benqa | generated_bn | 36 | 16 | 0 | 0 | 0 | 16 | 0 | 0 | 0 |

## First Hard Fails

- `benqa_12th-Math-II_0234` `generated_bn` failures=formulas preview=জদি x^{2} - 4x ্ 3 = 0 সমিকরনের মুলদ্বয় \alpha এবং \beta হয় তবে \frac{1}{\alpha} ্ ফ্রাচ{1}{\beta} এর মান- A. \frac{4}{3} B. \frac{3}{4} C. \frac-4}{3} D. \frac{-3}{4} Answer with only A, B, C, or D.
- `benqa_12th-Math-II_0230` `generated_bn` failures=formulas preview=5 একক দুরত্বে আ অ B বিন্দুতে ক্রিয়ারত 9 এবং 5 একক মানের সমান্তরাল বলদ্বয়- ই। অসদ্রিশ হলে লব্ধির মান 4 একক ইই। সদ্রিশ এবং লব্ধি ঁ বিন্দুতে ক্রিয়ারত হলে BC = \frac{45}{14} একক ইইই। সদ্রিশ হলে লব্ধির মান 14 একক নিছের কনতি স
- `benqa_12th-Biology-II_0119` `generated_bn` failures=formulas preview=ঃয্দ্রা-র কন ধরনের ছলনকে জন্কা ছলন বলে? A. গ্লাইদিন B. সমারসন্তিং C. লুপিং D. হান্তা Answer with only A, B, C, or D.
- `benqa_12th-Biology-I_0039` `generated_bn` failures=formulas preview=উদ্ভিদের অন্তহ্স্তিলিয় অংশ হছ্ছ্হে- A. হাইপদার্মিস B. এপিদার্মিস C. মজ্জারশ্মি D. কার্তেক্স Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0088` `generated_bn` failures=formulas preview=x-এর সাপেক্শে ln ax এর অন্তরজ- A. \frac{a}{x} B. \frac{x}{a} C. \frac{1}{x} D. \frac{1}{ax} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0054` `generated_bn` failures=formulas preview=আমাইদের কার্যকরি মুলক হল- A. \text{-CONH_{2}} B. \text{-COX} C. \text{-CHO} D. \text{-NH_{2}} Answer with only A, B, C, or D.
- `benqa_12th-Physics-II_0088` `generated_bn` failures=formulas preview=হাইগেন‌স এর নিতির সাহাজ্যে ব্যাখ্যা করা জায়- ই। প্রতিসরন ইই। প্রতিফলন ইইই। সমবর্তন নিছের কনতি সথিক? A. ই অ ইই B. ই অ ইইই C. ইই অ ইইই D. ই, ইই অ ইইই Answer with only A, B, C, or D.
- `benqa_10th-Biology_0057` `generated_bn` failures=formulas preview=গনি সাহেব তার বাগানে এমন কিছ্হু গাছ্হ লাগিয়েছ্হেন জার CO_{2} বিজারনের প্রথম স্থায়ি পদার্থ অক্সালো এসিতিক এসিদ। গনি সাহেব লাগিয়েছ্হেন- ই। ভুত্তা ইই। বেগুন ইইই। আখ নিছের কনতি সথিক? A. ই অ ইই B. ইই অ ইইই C. ই অ ইইই D. ই, ইই
- `benqa_12th-Chemistry-I_0140` `generated_bn` failures=formulas preview=CaF_{2}-এর সম্প্রিক্ত জলিয় দ্রবনে ফ্লরাইদ আয়নের ঘনমাত্রা 0.00655 gL^{-1} হলে CaF_{2} এর দ্রাব্যতা গুনফল কত হবে? A. 3.7\times 10^{-13} B. 2.048\times 10^{-10} C. 3.7\times 10^{-12} D. 2.048\times 10^{-11} Answer with only
- `benqa_12th-Chemistry-I_0190` `generated_bn` failures=formulas preview=নিছের কনতির বন্ধন কন সবছেয়ে বর? A. CH_{4} B. BCl_{3} C. NH_{3} D. ঃ_{2}ও Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0120` `generated_bn` failures=formulas preview=(3, -4) বিন্দুগামি এবং x-অক্শের সমান্তরাল সরলরেখার সমিকরন কনতি? A. y - 3 = 0 B. y ্ 3 = 0 C. y - 4 = 0 D. y ্ 4 = 1 Answer with only A, B, C, or D.
- `benqa_12th-Biology-II_0325` `generated_bn` failures=formulas preview=রুই মাছ্হের শ্রেনি পাখনায় রক্ত পরিবহন করে নিছের কন ধমনি? A. ইলিয়াক B. প্যারাইল C. সিলিয়াক-মেসেন্তারিক D. সাবক্লাভিয়ান Answer with only A, B, C, or D.
- `benqa_10th-Chemistry_0388` `generated_bn` failures=formulas preview=স্ক্যান্দিয়ামের সর্বশেশ শক্তিস্তরের সথিক ইলেকত্রন বিন্যাস কনতি? A. 3স^{2}3প^{6}3দ^{5}4স^{1} B. 3স^{2}3প^{6}3দ^{3}4স^{2} C. 3স^{2}3প^{6}3দ^{2}4স^{2} D. 3স^{2}3প^{6}3দ^{1}4স^{2} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0305` `generated_bn` failures=formulas preview=27^অঁ তাপমাত্রায় ও_2 এর RMS মান কত? A. 453.23 ms^{-1} B. 463.34 ms^{-1} C. 473.45 ms^{-1} D. 483.56 ms^{-1} Answer with only A, B, C, or D.
- `benqa_10th-Math_0032` `generated_bn` failures=formulas preview=(\sqrt{3})^{x্2} = 27 হলে x এর মান কত? A. 6 B. 4 C. 3 D. 2 Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0240` `generated_bn` failures=formulas preview=CH_{3} - CH_{2} - COONa ্ NaOH \xrightarrow[\Delta]{CaO} আ ্ ণা_{2}CO_{3} উদ্দিপকের বিক্রিয়াতি কি নামে পরিছিত? A. উর্তজ বিক্রিয়া B. দি-কার্বক্সিলেশন বিক্রিয়া C. উর্তজ ফিতিগ বিক্রিয়া D. ফ্রিদেল ক্রাফ‌ত বিক্রিয়া Answer wit

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
