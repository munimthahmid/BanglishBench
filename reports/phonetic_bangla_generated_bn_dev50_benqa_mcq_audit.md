# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/phonetic_bangla_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/phonetic_bangla_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/phonetic_bangla_dev50_benqa_mcq_generated_bn_audit_summary.csv`

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

- `benqa_10th-Chemistry_0280` `generated_bn` failures=options,formulas preview=কনতি প্রথম ব্যবহ্রিত ধাতু? আ। আউ B। আগ ঁ। শ্ন ড। ঁউ আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Physics-I_0109` `generated_bn` failures=options preview=তর্কের অপর নাম কি? আ। ঘর্শন বল B। জরতার ভ্রামক ঁ। ঘুর্নন বল ড। কেন্দ্রমুখি বল আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Biology-I_0218` `generated_bn` failures=options preview=গমের বইগ্গানিক নাম কি? আ। ওর্য্যা সাতিভা B। ট্রিতিচুম আএস্তিভুম ঁ। যেআ মায়্স ড। Bআম্বুসা তুল্দা আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Math-II_0234` `generated_bn` failures=options,formulas preview=জদি x^{2} - 4x ্ 3 = 0 সমিকরনের মুলদ্বয় \আল্ফা এবং \বেতা হয় তবে \ফ্রাচ{1}{\আল্ফা} ্ ফ্রাচ{1}{\বেতা} এর মান- আ। \ফ্রাচ{4}{3} B। \ফ্রাচ{3}{4} ঁ। \ফ্রাচ-4}{3} ড। \ফ্রাচ{-3}{4} আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Math-II_0230` `generated_bn` failures=options,formulas preview=5 একক দুরত্বে আ অ B বিন্দুতে ক্রিয়ারত 9 এবং 5 একক মানের সমান্তরাল বলদ্বয়- ই। অসদ্রিশ হলে লব্ধির মান 4 একক ইই। সদ্রিশ এবং লব্ধি ঁ বিন্দুতে ক্রিয়ারত হলে Bঁ = \ফ্রাচ{45}{14} একক ইইই। সদ্রিশ হলে লব্ধির মান 14 একক নিছের কনতি 
- `benqa_12th-Biology-II_0119` `generated_bn` failures=options,formulas preview=ঃয্দ্রা-র কন ধরনের ছলনকে জন্কা ছলন বলে? আ। গ্লাইদিন B। সমারসন্তিং ঁ। লুপিং ড। হান্তা আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Biology-I_0039` `generated_bn` failures=options,formulas preview=উদ্ভিদের অন্তহ্স্তিলিয় অংশ হছ্ছ্হে- আ। হাইপদার্মিস B। এপিদার্মিস ঁ। মজ্জারশ্মি ড। কার্তেক্স আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Math-I_0202` `generated_bn` failures=options,formulas preview=\ইন্ত \ফ্রাচ{চসx}{\সqর্ত{সিনx}} দx = কত? আ। 2\সqর্ত{চসx} ্ চ B। 2\সqর্ত{সিনx} ্ চ ঁ। \ফ্রাচ{1}{2} \সqর্ত{চসx} ্ চ ড। \ফ্রাচ{1}{2} \সqর্ত{সিনx} ্ চ আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Math-I_0088` `generated_bn` failures=options,formulas preview=x-এর সাপেক্শে ল্ন আx এর অন্তরজ- আ। \ফ্রাচ{আ}{x} B। \ফ্রাচ{x}{আ} ঁ। \ফ্রাচ{1}{x} ড। \ফ্রাচ{1}{আx} আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_8th-Math_0085` `generated_bn` failures=options preview=4 ক্রমের ম্যাজিক বর্গের কনাকুনি জগফল কত? আ। 15 B। 16 ঁ। 34 ড। 65 আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Biology-I_0265` `generated_bn` failures=options preview=মি। 'ক' ব্যবহারিক ক্লাসে একতি নমুনার পর্যবেক্শন করে দেখলো মেতাজাইলেম কেন্দ্রের দিকে, ভাস্কুলার বান্দল 9তি এবং কিছ্হু এককশি রম আছ্হে। পর্যবেক্শিত বইশিশ্ত্যগুলো কিভাবে উদ্ভিদকে বান্ছিয়ে রাখতে সাহাজ্য করে? ই। পানি অ খনিজ লব
- `benqa_12th-Chemistry-I_0303` `generated_bn` failures=options,formulas preview=নিছের কন এসিদতি সবছেয়ে শক্তিশালি? আ। ঃF B। ঃঁঈ ঁ। ঃBর ড। ঃঈ আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_10th-Physics_0296` `generated_bn` failures=options preview=ইউরেনিয়ামের ছেইন বিক্রিয়ার দ্বিতিয় ধাপে কততি নিউত্রন নির্গত হয়? আ। 2 তি B। 3 তি ঁ। 6 তি ড। 9 তি আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Physics-I_0106` `generated_bn` failures=options,formulas preview=নিছের কনতি শুন্য দশার সমতুল্য? আ। \পি/2 B। \পি ঁ। 3\পি/2 ড। 2\পি আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Chemistry-II_0054` `generated_bn` failures=options,formulas preview=আমাইদের কার্যকরি মুলক হল- আ। \তেxত{-ঁওণঃ_{2}} B। \তেxত{-ঁওX} ঁ। \তেxত{-ঁঃও} ড। \তেxত{-ণঃ_{2}} আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_10th-Biology_0197` `generated_bn` failures=options preview=কশের সকল জইবিক ক্রিয়া নিয়ন্ত্রন করে কনতি? আ। নিউক্লয়াস B। রাইবজম ঁ। লাইসজম ড। মাইতকন্দ্রিয়া আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Physics-II_0088` `generated_bn` failures=options,formulas preview=হাইগেন‌স এর নিতির সাহাজ্যে ব্যাখ্যা করা জায়- ই। প্রতিসরন ইই। প্রতিফলন ইইই। সমবর্তন নিছের কনতি সথিক? আ। ই অ ইই B। ই অ ইইই ঁ। ইই অ ইইই ড। ই, ইই অ ইইই আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_8th-Science_0153` `generated_bn` failures=options preview=পাকস্থলির এসিদিতি নিরাময়ে কনতি উপজগি? আ। ক্যালসিয়াম B। এসিতিক এসিদ ঁ। অজলুমিনিয়াম হাইদ্রক্সাইদ ড। আমনিয়াম হাইদ্রক্সাইদ আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_10th-Biology_0057` `generated_bn` failures=options,formulas preview=গনি সাহেব তার বাগানে এমন কিছ্হু গাছ্হ লাগিয়েছ্হেন জার ঁও_{2} বিজারনের প্রথম স্থায়ি পদার্থ অক্সালো এসিতিক এসিদ। গনি সাহেব লাগিয়েছ্হেন- ই। ভুত্তা ইই। বেগুন ইইই। আখ নিছের কনতি সথিক? আ। ই অ ইই B। ইই অ ইইই ঁ। ই অ ইইই ড। ই, ইই
- `benqa_10th-Physics_0045` `generated_bn` failures=options preview=কন নির্দিশ্ত ভরের কনো বস্তুর বেগ দ্বিগুন করলে গতিশক্তি কত গুন হবে? আ। ছারগুন B। দ্বিগুন ঁ। অর্ধেক ড। সমান আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Chemistry-I_0140` `generated_bn` failures=options,formulas preview=ঁআF_{2}-এর সম্প্রিক্ত জলিয় দ্রবনে ফ্লরাইদ আয়নের ঘনমাত্রা 0।00655 গL^{-1} হলে ঁআF_{2} এর দ্রাব্যতা গুনফল কত হবে? আ। 3।7\তিমেস 10^{-13} B। 2।048\তিমেস 10^{-10} ঁ। 3।7\তিমেস 10^{-12} ড। 2।048\তিমেস 10^{-11} আন্স্বের বিথ অন্
- `benqa_12th-Chemistry-I_0190` `generated_bn` failures=options,formulas preview=নিছের কনতির বন্ধন কন সবছেয়ে বর? আ। ঁঃ_{4} B। Bঁল_{3} ঁ। ণঃ_{3} ড। ঃ_{2}ও আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_10th-Chemistry_0374` `generated_bn` failures=options preview=ইথিলিন গ্লাইকল কন ধরনের জউগ? আ। আলদিহাইদ B। আলকহল ঁ। আলকিন ড। আলকাইন আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_12th-Math-I_0120` `generated_bn` failures=options,formulas preview=(3, -4) বিন্দুগামি এবং x-অক্শের সমান্তরাল সরলরেখার সমিকরন কনতি? আ। য - 3 = 0 B। য ্ 3 = 0 ঁ। য - 4 = 0 ড। য ্ 4 = 1 আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।
- `benqa_10th-Math-II_0367` `generated_bn` failures=options,formulas preview=একতি নিরপেক্শ ছ্হক্কা একবার নিক্শেপ করা হলে মউলিক সংখ্যা আসার সম্ভাবনা কত? আ। \ফ্রাচ{1}{6} B। \ফ্রাচ{1}{3} ঁ। \ফ্রাচ{1}{2} ড। \ফ্রাচ{2}{3} আন্স্বের বিথ অন্ল্য আ, B, ঁ, অর ড।

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
