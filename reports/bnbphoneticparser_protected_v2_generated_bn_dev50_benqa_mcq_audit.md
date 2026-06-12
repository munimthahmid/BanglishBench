# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn_audit_summary.csv`

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

- `benqa_12th-Math-II_0234` `generated_bn` failures=formulas preview=জদি x^{2} - 4x + 3 = 0 সমিকরনের মুলদবয় \alpha এবং \beta হয় তবে \frac{1}{\alpha} + ফরাচ{1}{\beta} এর মান- A. \frac{4}{3} B. \frac{3}{4} C. \frac-4}{3} D. \frac{-3}{4} Answer with only A, B, C, or D.
- `benqa_12th-Math-II_0230` `generated_bn` failures=formulas preview=5 একক দুরতবে আ অ ব বিনদুতে করিয়ারত 9 এবং 5 একক মানের সমানতরাল বলদবয়- ই. অসঅদরিশ হলে লব্ধির মান 4 একক ইই. সদরিশ এবং লব্ধি চ বিনদুতে করিয়ারত হলে BC = \frac{45}{14} একক ইইই. সদরিশ হলে লব্ধির মান 14 একক নিছের কনতি সথিক? A. ি
- `benqa_12th-Biology-II_0119` `generated_bn` failures=formulas preview=হয়দরা-র কন ধরনের ছলনকে জঙ্কা ছলন বলে? A. গলাইদইন B. সমারসনতইং C. লুপইং D. হানতা Answer with only A, B, C, or D.
- `benqa_12th-Biology-I_0039` `generated_bn` failures=formulas preview=উদ্ভিদের অনতঅহসতিলিয় অংশ হছচ্ে- A. হাইপদারমইস B. েপইদারমইস C. মজজারশ্মই D. কারতেকস Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0088` `generated_bn` failures=formulas preview=x-ের সাপেকশে ln ax এর অনতঅরঅজ- A. \frac{a}{x} B. \frac{x}{a} C. \frac{1}{x} D. \frac{1}{ax} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0054` `generated_bn` failures=formulas preview=আমাইদের কারয়করি মুলক হল- A. \text{-CONH_{2}} B. \text{-COX} C. \text{-CHO} D. \text{-NH_{2}} Answer with only A, B, C, or D.
- `benqa_12th-Physics-II_0088` `generated_bn` failures=formulas preview=হাইগেন‌স এর নিতির সাহাজয়ে বয়াখ্যা করা জায়- ই. পরতিসরন ইই. পরতিফলন ইইই. সমবরতন নিছের কনতি সথিক? A. ি অ ইই B. ই অ ইইই C. ইই অ ইইই D. ই, ইই অ ইইই Answer with only A, B, C, or D.
- `benqa_10th-Biology_0057` `generated_bn` failures=formulas preview=গনি সাহেব তার বাগানে এমন কিচ্ু গাচ্ লাগিয়েচ্েন জার CO_{2} বিজারনের পরথম স্থায়ি পদারথ অকসালঅ এসিতিক এসিদ. গনি সাহেব লাগিয়েচ্েন- ই. ভুততা ইই. বেগুন ইইই. আখ নিছের কনতি সথিক? A. ি অ ইই B. ইই অ ইইই C. ই অ ইইই D. ই, ইই অ ইইই A
- `benqa_12th-Chemistry-I_0140` `generated_bn` failures=formulas preview=CaF_{2}-ের সম্প্রিকত জলিয় দরবনে ফলরাইদ আয়নের ঘনমাতরা 0.00655 gL^{-1} হলে CaF_{2} এর দরাবয়তা গুনফল কত হবে? A. 3.7\times 10ঁ{-13} B. 2.048\times 10ঁ{-10} C. 3.7\times 10ঁ{-12} D. 2.048\times 10ঁ{-11} Answer with only A, B,
- `benqa_12th-Chemistry-I_0190` `generated_bn` failures=formulas preview=নিছের কনতির বন্ধন কন সবছেয়ে বর? A. CH_{4} B. BCl_{3} C. NH_{3} D. হ_{2}ো Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0120` `generated_bn` failures=formulas preview=(3, -4) বিনদুগামি এবং x-কশের সমানতরাল সরলরেখার সমিকরন কনতি? A. y - 3 = 0 B. y + 3 = 0 C. y - 4 = 0 D. y + 4 = 1 Answer with only A, B, C, or D.
- `benqa_12th-Biology-II_0325` `generated_bn` failures=formulas preview=রুই মাচ্ের শ্রেনি পাখনায় রকত পরিবহন করে নিছের কন ধমনি? A. িলিয়াক B. পয়ারািল C. সিলিয়াক-মেসেনতারিক D. সাবকলাভিয়ান Answer with only A, B, C, or D.
- `benqa_10th-Chemistry_0388` `generated_bn` failures=formulas preview=সকয়ানদিয়ামের সরবশেশ শকতিসতরের সথিক ইলেকতরন বিনয়াস কনতি? A. 3সঁ{2}3পঁ{6}3দঁ{5}4সঁ{1} B. 3সঁ{2}3পঁ{6}3দঁ{3}4সঁ{2} C. 3সঁ{2}3পঁ{6}3দঁ{2}4সঁ{2} D. 3সঁ{2}3পঁ{6}3দঁ{1}4সঁ{2} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0305` `generated_bn` failures=formulas preview=27ঁচ তাপমাতরায় ও_2 এর RMS মান কত? A. 453.23 ms^{-1} B. 463.34 ms^{-1} C. 473.45 ms^{-1} D. 483.56 ms^{-1} Answer with only A, B, C, or D.
- `benqa_10th-Math_0032` `generated_bn` failures=formulas preview=(\sqrt{3})ঁ{x+2} = 27 হলে x এর মান কত? A. 6 B. 4 C. 3 D. 2 Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0240` `generated_bn` failures=formulas preview=CH_{3} - CH_{2} - COONa + NaOH \xrightarrow[\Delta]{CaO} আ + ণা_{2}CO_{3} উদদিপকের বিকরিয়াতি কি নামে পরিছিত? A. ুরতজ বিকরিয়া B. দি-কারবকসিলেশন বিকরিয়া C. ুরতজ ফিতিগ বিকরিয়া D. ফরিদেল করাফ‌ত বিকরিয়া Answer with only A, B,

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
