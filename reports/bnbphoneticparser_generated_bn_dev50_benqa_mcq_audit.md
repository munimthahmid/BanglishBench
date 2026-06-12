# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/bnbphoneticparser_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/bnbphoneticparser_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/bnbphoneticparser_dev50_benqa_mcq_generated_bn_audit_summary.csv`

## Counts

- Expected prompt rows: 36
- Missing outputs: 0
- Extra output keys: 0
- Hard-fail rows: 36
- Warning rows: 0

| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benqa | generated_bn | 36 | 36 | 0 | 36 | 0 | 23 | 0 | 0 | 0 |

## First Hard Fails

- `benqa_10th-Chemistry_0280` `generated_bn` failures=options,formulas preview=কনতি পরথম বয়বহরিত ধাতু? a. আউ ব. আগ চ. শন ড. চু aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Physics-I_0109` `generated_bn` failures=options preview=তরকের অপঅর নাম কি? a. ঘরশন বল ব. জরতার ভ্রামক চ. ঘুরনন বল ড. কেন্দ্রমুখি বল aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Biology-I_0218` `generated_bn` failures=options preview=গমের বইগগানইক নাম কি? a. ওরয়যা সাতিভা ব. টরিতিচুম আএসতিভুম চ. ্যেয়া মায়স ড. বামবুসা তুলদা aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Math-II_0234` `generated_bn` failures=options,formulas preview=জদি এক্সঁ{২} - ৪এক্স + ৩ = ০ সমিকরনের মুলদবয় \aলফা এবং \বেতা হয় তবে \ফরাচ{১}{\aলফা} + ফরাচ{১}{\বেতা} এর মান- a. \ফরাচ{৪}{৩} ব. \ফরাচ{৩}{৪} চ. \ফরাচ-৪}{৩} ড. \ফরাচ{-৩}{৪} aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Math-II_0230` `generated_bn` failures=options,formulas preview=৫ একক দুরতবে আ অ ব বিনদুতে করিয়ারত ৯ এবং ৫ একক মানের সমানতরাল বলদবয়- ই. অসঅদরিশ হলে লব্ধির মান ৪ একক ইই. সদরিশ এবং লব্ধি চ বিনদুতে করিয়ারত হলে বচ = \ফরাচ{৪৫}{১৪} একক ইইই. সদরিশ হলে লব্ধির মান ১৪ একক নিছের কনতি সথিক? a. ই
- `benqa_12th-Biology-II_0119` `generated_bn` failures=options,formulas preview=হয়দরা-র কন ধরনের ছলনকে জঙ্কা ছলন বলে? a. গলাইদইন ব. সমারসনতিং চ. লুপিং ড. হানতা aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Biology-I_0039` `generated_bn` failures=options,formulas preview=উদ্ভিদের অনতঅহসতিলিয় অংশ হছচ্ে- a. হাইপদারমইস ব. এপিদারমিস চ. মজজারশ্মি ড. কারতেকস aনসওের ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Math-I_0202` `generated_bn` failures=options,formulas preview=\িনত \ফরাচ{চসক্স}{\সকরত{সিনক্স}} দক্স = কত? a. ২\সকরত{চসক্স} + চ ব. ২\সকরত{সিনক্স} + চ চ. \ফরাচ{১}{২} \সকরত{চসক্স} + চ ড. \ফরাচ{১}{২} \সকরত{সিনক্স} + চ aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Math-I_0088` `generated_bn` failures=options,formulas preview=এক্স-ের সাপেকশে লন আক্স এর অনতঅরঅজ- a. \ফরাচ{a}{এক্স} ব. \ফরাচ{এক্স}{a} চ. \ফরাচ{১}{এক্স} ড. \ফরাচ{১}{aক্স} aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_8th-Math_0085` `generated_bn` failures=options preview=৪ করমের ময়াজিক বরগের কনাকুনি জগফল কত? a. ১৫ ব. ১৬ চ. ৩৪ ড. ৬৫ aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Biology-I_0265` `generated_bn` failures=options preview=মি. 'ক' বয়বহারিক কলাসে একতি নমুনার পরয়বেকশন করে দেখল মেতাজাইলেম কেন্দ্রের দিকে, ভাসকুলার বানদল ৯তি এবং কিচ্ু এককশি রম আচ্ে. পরয়বেকশিত বইশইশ্তয়গুল কিভাবে উদ্ভিদকে বাঞ্ছিয়ে রাখতে সাহাজয় করে? ই. পানি অ খনিজ লবন পরিবহন করে ই
- `benqa_12th-Chemistry-I_0303` `generated_bn` failures=options,formulas preview=নিছের কন এসিদতি সবছেয়ে শকতিশালি? a. হফ ব. হচী চ. হবর ড. হী aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_10th-Physics_0296` `generated_bn` failures=options preview=ইউরেনইয়ামের ছেইন বিকরিয়ার দওইতইয় ধাপে কততি নিউতরন নিরগত হয়? a. ২ তি ব. ৩ তি চ. ৬ তি ড. ৯ তি aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Physics-I_0106` `generated_bn` failures=options,formulas preview=নিছের কনতি শুনয় দশার সমতুলয়? a. \পি/২ ব. \পি চ. ৩\পি/২ ড. ২\পি aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Chemistry-II_0054` `generated_bn` failures=options,formulas preview=আমাইদের কারয়করি মুলক হল- a. \তেক্সত{-চোণহ_{২}} ব. \তেক্সত{-চোক্স} চ. \তেক্সত{-ছো} ড. \তেক্সত{-ণহ_{২}} aনসওের ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_10th-Biology_0197` `generated_bn` failures=options preview=কশের সকল জইবইক করিয়া নিয়ন্ত্রন করে কনতি? a. নিউকলয়াস ব. রাইবজম চ. লাইসজম ড. মাইতকন্দ্রইয়া aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Physics-II_0088` `generated_bn` failures=options,formulas preview=হাইগেন‌স এর নিতির সাহাজয়ে বয়াখ্যা করা জায়- ই. পরতিসরন ইই. পরতিফলন ইইই. সমবরতন নিছের কনতি সথিক? a. ই অ ইই ব. ই অ ইইই চ. ইই অ ইইই ড. ই, ইই অ ইইই aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_8th-Science_0153` `generated_bn` failures=options preview=পাকস্থলির এসিদিতি নিরাময়ে কনতি উপজগি? a. কয়ালসিয়াম ব. এসিতিক এসিদ চ. অজঅলুমিনিয়াম হাইদরকসাইদ ড. আমনিয়াম হাইদরকসাইদ aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_10th-Biology_0057` `generated_bn` failures=options,formulas preview=গনি সাহেব তার বাগানে এমন কিচ্ু গাচ্ লাগিয়েচ্েন জার চো_{২} বিজারনের পরথম স্থায়ি পদারথ অকসালঅ এসিতিক এসিদ. গনি সাহেব লাগিয়েচ্েন- ই. ভুততা ইই. বেগুন ইইই. আখ নিছের কনতি সথিক? a. ই অ ইই ব. ইই অ ইইই চ. ই অ ইইই ড. ই, ইই অ ইইই a
- `benqa_10th-Physics_0045` `generated_bn` failures=options preview=কন নিরদিশ্ত ভরের কন বসতুর বেগ দওইগুন করলে গতিশকতি কত গুন হবে? a. ছারগুন ব. দওইগুন চ. অরধেক ড. সমান aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Chemistry-I_0140` `generated_bn` failures=options,formulas preview=চাফ_{২}-ের সম্প্রিকত জলিয় দরবনে ফলরাইদ আয়নের ঘনমাতরা ০.০০৬৫৫ গলঁ{-১} হলে চাফ_{২} এর দরাবয়তা গুনফল কত হবে? a. ৩.৭\তিমেস ১০ঁ{-১৩} ব. ২.০৪৮\তিমেস ১০ঁ{-১০} চ. ৩.৭\তিমেস ১০ঁ{-১২} ড. ২.০৪৮\তিমেস ১০ঁ{-১১} aনসওএর ওইথ অনলয় আ, ব, 
- `benqa_12th-Chemistry-I_0190` `generated_bn` failures=options,formulas preview=নিছের কনতির বন্ধন কন সবছেয়ে বর? a. ছ_{৪} ব. বচল_{৩} চ. ণহ_{৩} ড. হ_{২}ো aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_10th-Chemistry_0374` `generated_bn` failures=options preview=ইথইলইন গলাইকল কন ধরনের জউগ? a. আলদিহািদ ব. আলকহল চ. আলকিন ড. আলকাইন aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_12th-Math-I_0120` `generated_bn` failures=options,formulas preview=(৩, -৪) বিনদুগামি এবং এক্স-কশের সমানতরাল সরলরেখার সমিকরন কনতি? a. য় - ৩ = ০ ব. য় + ৩ = ০ চ. য় - ৪ = ০ ড. য় + ৪ = ১ aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.
- `benqa_10th-Math-II_0367` `generated_bn` failures=options,formulas preview=একতি নিরপেকশ চ্ককা একবার নিকশেপ করা হলে মউলিক সংখ্যা আসার সম্ভাবনা কত? a. \ফরাচ{১}{৬} ব. \ফরাচ{১}{৩} চ. \ফরাচ{১}{২} ড. \ফরাচ{২}{৩} aনসওএর ওইথ অনলয় আ, ব, চ, অর ড.

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
