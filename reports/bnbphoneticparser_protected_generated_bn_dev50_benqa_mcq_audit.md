# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn_audit_summary.csv`

## Counts

- Expected prompt rows: 36
- Missing outputs: 0
- Extra output keys: 0
- Hard-fail rows: 22
- Warning rows: 0

| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benqa | generated_bn | 36 | 22 | 0 | 0 | 0 | 22 | 0 | 0 | 0 |

## First Hard Fails

- `benqa_10th-Chemistry_0280` `generated_bn` failures=formulas preview=কনতি পরথম বয়বহরিত ধাতু? A. aু B. aগ C. শন D. চু Answer with only A, B, C, or D.
- `benqa_12th-Math-II_0234` `generated_bn` failures=formulas preview=জদি এক্সঁ{২} - ৪এক্স + ৩ = ০ সমিকরনের মুলদবয় \alpha এবং \beta হয় তবে \frac{১}{\alpha} + ফরাচ{১}{\beta} এর মান- A. \frac{৪}{৩} B. \frac{৩}{৪} C. \frac-৪}{৩} D. \frac{-৩}{৪} Answer with only A, B, C, or D.
- `benqa_12th-Math-II_0230` `generated_bn` failures=formulas preview=৫ একক দুরতবে আ অ ব বিনদুতে করিয়ারত ৯ এবং ৫ একক মানের সমানতরাল বলদবয়- ই. অসঅদরিশ হলে লব্ধির মান ৪ একক ইই. সদরিশ এবং লব্ধি চ বিনদুতে করিয়ারত হলে BC = \frac{৪৫}{১৪} একক ইইই. সদরিশ হলে লব্ধির মান ১৪ একক নিছের কনতি সথিক? A. ি
- `benqa_12th-Biology-II_0119` `generated_bn` failures=formulas preview=হয়দরা-র কন ধরনের ছলনকে জঙ্কা ছলন বলে? A. গলাইদইন B. সমারসনতইং C. লুপইং D. হানতা Answer with only A, B, C, or D.
- `benqa_12th-Biology-I_0039` `generated_bn` failures=formulas preview=উদ্ভিদের অনতঅহসতিলিয় অংশ হছচ্ে- A. হাইপদারমইস B. েপইদারমইস C. মজজারশ্মই D. কারতেকস Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0202` `generated_bn` failures=formulas preview=\int \frac{চসক্স}{\sqrt{সিনক্স}} দক্স = কত? A. ২\sqrt{চসক্স} + চ B. ২\sqrt{সিনক্স} + চ C. \frac{১}{২} \sqrt{চসক্স} + চ D. \frac{১}{২} \sqrt{সিনক্স} + চ Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0088` `generated_bn` failures=formulas preview=এক্স-ের সাপেকশে লন আক্স এর অনতঅরঅজ- A. \frac{a}{এক্স} B. \frac{এক্স}{a} C. \frac{১}{এক্স} D. \frac{১}{aক্স} Answer with only A, B, C, or D.
- `benqa_12th-Physics-I_0106` `generated_bn` failures=formulas preview=নিছের কনতি শুনয় দশার সমতুলয়? A. \pi/২ B. \pi C. ৩\pi/২ D. ২\pi Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0054` `generated_bn` failures=formulas preview=আমাইদের কারয়করি মুলক হল- A. \text{-চোণহ_{২}} B. \text{-COX} C. \text{-CHO} D. \text{-ণহ_{২}} Answer with only A, B, C, or D.
- `benqa_12th-Physics-II_0088` `generated_bn` failures=formulas preview=হাইগেন‌স এর নিতির সাহাজয়ে বয়াখ্যা করা জায়- ই. পরতিসরন ইই. পরতিফলন ইইই. সমবরতন নিছের কনতি সথিক? A. ি অ ইই B. ই অ ইইই C. ইই অ ইইই D. ই, ইই অ ইইই Answer with only A, B, C, or D.
- `benqa_10th-Biology_0057` `generated_bn` failures=formulas preview=গনি সাহেব তার বাগানে এমন কিচ্ু গাচ্ লাগিয়েচ্েন জার চো_{২} বিজারনের পরথম স্থায়ি পদারথ অকসালঅ এসিতিক এসিদ. গনি সাহেব লাগিয়েচ্েন- ই. ভুততা ইই. বেগুন ইইই. আখ নিছের কনতি সথিক? A. ি অ ইই B. ইই অ ইইই C. ই অ ইইই D. ই, ইই অ ইইই A
- `benqa_12th-Chemistry-I_0140` `generated_bn` failures=formulas preview=চাফ_{২}-ের সম্প্রিকত জলিয় দরবনে ফলরাইদ আয়নের ঘনমাতরা ০.০০৬৫৫ গলঁ{-১} হলে চাফ_{২} এর দরাবয়তা গুনফল কত হবে? A. ৩.৭\times ১০ঁ{-১৩} B. ২.০৪৮\times ১০ঁ{-১০} C. ৩.৭\times ১০ঁ{-১২} D. ২.০৪৮\times ১০ঁ{-১১} Answer with only A, B,
- `benqa_12th-Chemistry-I_0190` `generated_bn` failures=formulas preview=নিছের কনতির বন্ধন কন সবছেয়ে বর? A. ছ_{৪} B. বচল_{৩} C. ণহ_{৩} D. হ_{২}ো Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0120` `generated_bn` failures=formulas preview=(৩, -৪) বিনদুগামি এবং এক্স-কশের সমানতরাল সরলরেখার সমিকরন কনতি? A. য় - ৩ = ০ B. য় + ৩ = ০ C. য় - ৪ = ০ D. য় + ৪ = ১ Answer with only A, B, C, or D.
- `benqa_10th-Math-II_0367` `generated_bn` failures=formulas preview=একতি নিরপেকশ চ্ককা একবার নিকশেপ করা হলে মউলিক সংখ্যা আসার সম্ভাবনা কত? A. \frac{১}{৬} B. \frac{১}{৩} C. \frac{১}{২} D. \frac{২}{৩} Answer with only A, B, C, or D.
- `benqa_12th-Biology-II_0179` `generated_bn` failures=formulas preview=রকত জমাত বান্ধতে কন ধাতব আয়ন সহায়তা করে? A. চাঁ{++} B. মগঁ{++} C. চুঁ{++} D. ফেঁ{++} Answer with only A, B, C, or D.
- `benqa_12th-Physics-II_0131` `generated_bn` failures=formulas preview=থারমমিতির মুল সমিকরন নিছের কনতি? A. \frac{ণ}{\theta - \theta_{িচে}} = \frac{এক্স_{\theta} - এক্স_{িচে}}{এক্স_{সতেয়াম} - এক্স_{িচে}} B. \frac{\theta - \theta_{িচে}}{ণ} = \frac{এক্স_{\theta} - এক্স_{িচে}}{এক্স_{সতেয়াম} - এ
- `benqa_12th-Biology-II_0325` `generated_bn` failures=formulas preview=রুই মাচ্ের শ্রেনি পাখনায় রকত পরিবহন করে নিছের কন ধমনি? A. িলিয়াক B. পয়ারািল C. সিলিয়াক-মেসেনতারিক D. সাবকলাভিয়ান Answer with only A, B, C, or D.
- `benqa_10th-Chemistry_0388` `generated_bn` failures=formulas preview=সকয়ানদিয়ামের সরবশেশ শকতিসতরের সথিক ইলেকতরন বিনয়াস কনতি? A. ৩সঁ{২}৩পঁ{৬}৩দঁ{৫}৪সঁ{১} B. ৩সঁ{২}৩পঁ{৬}৩দঁ{৩}৪সঁ{২} C. ৩সঁ{২}৩পঁ{৬}৩দঁ{২}৪সঁ{২} D. ৩সঁ{২}৩পঁ{৬}৩দঁ{১}৪সঁ{২} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0305` `generated_bn` failures=formulas preview=২৭ঁচ তাপমাতরায় ও_২ এর RMS মান কত? A. ৪৫৩.২৩ মসঁ{-১} B. ৪৬৩.৩৪ মসঁ{-১} C. ৪৭৩.৪৫ মসঁ{-১} D. ৪৮৩.৫৬ মসঁ{-১} Answer with only A, B, C, or D.
- `benqa_10th-Math_0032` `generated_bn` failures=formulas preview=(\sqrt{৩})ঁ{এক্স+২} = ২৭ হলে এক্স এর মান কত? A. ৬ B. ৪ C. ৩ D. ২ Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0240` `generated_bn` failures=formulas preview=ছ_{৩} - ছ_{২} - COONa + NaOH \xrightarrow[\Delta]{CaO} আ + ণা_{২}চো_{৩} উদদিপকের বিকরিয়াতি কি নামে পরিছিত? A. ুরতজ বিকরিয়া B. দি-কারবকসিলেশন বিকরিয়া C. ুরতজ ফিতিগ বিকরিয়া D. ফরিদেল করাফ‌ত বিকরিয়া Answer with only A, B, C

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
