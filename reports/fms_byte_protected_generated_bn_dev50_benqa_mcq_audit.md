# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/fms_byte_protected_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/fms_byte_protected_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/fms_byte_protected_dev50_benqa_mcq_generated_bn_audit_summary.csv`

## Counts

- Expected prompt rows: 36
- Missing outputs: 0
- Extra output keys: 0
- Hard-fail rows: 15
- Warning rows: 7

| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benqa | generated_bn | 36 | 15 | 7 | 0 | 0 | 15 | 0 | 0 | 7 |

## First Hard Fails

- `benqa_12th-Math-II_0234` `generated_bn` failures=formulas preview=যদি x^{2}  -  4x  +  3  =  0 সমস্যার মূলবাদ \alpha এসব \beta হয় তবে \frac{1}{\alpha}  + ফার্ক{1}{\beta} এর মান- A. \frac{4}{3} B. \frac{3}{4} C. \frac-4}{3} D. \frac{-3}{4} Answer with only A, B, C, or D.
- `benqa_12th-Math-II_0230` `generated_bn` failures=formulas preview=5 একই রকম এ ও বি বিন্ডুট হওয়ারত 9 এসব 5 একক মানের সমস্যার বলোবয়-  i. অস্থির হ হলে লবিডিহার মান 4 একক ii. সদরিশ এখন লব্য সি বনিত করারত হলে BC  =  \frac{45}{14} একক iii. সমস্যা হলে লবিডিহার মান 14 একই নিচের কোনটা সঠিক? A
- `benqa_12th-Biology-II_0119` `generated_bn` failures=formulas preview=হির্ডা-আর কোন ধরণের চলোনোকে যেন চলোনো বলে? A. গালিডীন B. সমস্যারকমিং C. ল্যাপিং D. হ্যানতা Answer with only A, B, C, or D.
- `benqa_12th-Biology-I_0039` `generated_bn` failures=formulas preview=উল্লেখের অন্টিস্টলিয় বিবশ হচ্ছে- A. হাইপোডারমিস B. এপিডারমিস C. মানদারুচ্ছি D. কারটেক্স Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0088` `generated_bn` failures=formulas preview=x-এর সাপেক্সে ln  ax এর অন্তরয়- A. \frac{a}{x} B. \frac{x}{a} C. \frac{1}{x} D. \frac{1}{ax} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0054` `generated_bn` failures=formulas preview=এমআইসেডার কারোরি মূল কথা হলো- A. \text{-CONH_{2}} B. \text{-COX} C. \text{-CHO} D. \text{-NH_{2}} Answer with only A, B, C, or D.
- `benqa_12th-Physics-II_0088` `generated_bn` failures=formulas preview=হেইগেন স এর নিজের সাজাযে খাওয়া করা যায়-  i. প্রতিসোর ii. প্রোটিফলন iii। সম্পর্কে নিচের কোনটা সঠিক? A. i ও ii B. i ও iii C. ii ও iii D. i,  ii ও iii Answer with only A, B, C, or D.
- `benqa_10th-Biology_0057` `generated_bn` failures=formulas preview=গনি সাহব টার ব্যালানে এমন কিছু উপায় লাগিয়েছেন যার CO_{2} আইভরিনের প্রথম সথেই পর্যন্ত অসুজা সবকিছু ইসিদ। গনি সাহব লাগিয়েছেন-  i. বন্ধু ii. ব্যাগন iii। এখন নিচের কোনটা সঠিক? A. i ও ii B. ii ও iii C. i ও iii D. i,  ii ও 
- `benqa_12th-Chemistry-I_0140` `generated_bn` failures=formulas preview=CaF_{2}-এর সম্পর্কে যদিই drobোন ফুলেল এইনের হচ্ছে 0.00655  gL^{-1} হলে CaF_{2} এর ড্রাবিটা গুনোফাল কতো হবে? A. 3.7\times  10^{-13} B. 2.048\times  10^{-10} C. 3.7\times  10^{-12} D. 2.048\times  10^{-11} Answer with only
- `benqa_12th-Chemistry-I_0190` `generated_bn` failures=formulas preview=নিচের কোনোটার বন্ধন কোন সমস্যায় বের? A. CH_{4} B. BCl_{3} C. NH_{3} D. হা_{2}ও Answer with only A, B, C, or D.
- `benqa_12th-Math-I_0120` `generated_bn` failures=formulas preview=(3,  -4) বিনোদনাপ্যামি এখন x-ওকেসের সমস্যার সমাধানের সমস্যার কোনটা? A. y  -  3  =  0 B. y  +  3  =  0 C. y  -  4  =  0 D. y  +  4  =  1 Answer with only A, B, C, or D.
- `benqa_12th-Biology-II_0325` `generated_bn` failures=formulas preview=রুআই মেশির এসেনি পেলামি রকেট পরিবেশন করে নিচ্ছের কোন ধন্যবাদ? A. ইলিয়াকা B. হাহাইয়েল C. শিখাইনা-মেসেন্সটারিক D. সবকিছুবানান Answer with only A, B, C, or D.
- `benqa_10th-Chemistry_0388` `generated_bn` failures=formulas preview=স্কাইন্ডিয়মার সমস্যা শিখিটর সঠিক ইলেটরন চালাইনাস কোনো? A. 3এস^{2}3পি^{6}3ডি^{5}4এস^{1} B. 3এস^{2}3পি^{6}3ডি^{3}4এস^{2} C. 3এস^{2}3পি^{6}3ডি^{2}4এস^{2} D. 3এস^{2}3পি^{6}3ডি^{1}4এস^{2} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0305` `generated_bn` failures=formulas preview=27^ঐ টিতোমেটারি ও_2 এর RMS মান কট? A. 453.23  ms^{-1} B. 463.34  ms^{-1} C. 473.45  ms^{-1} D. 483.56  ms^{-1} Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-II_0240` `generated_bn` failures=formulas preview=CH_{3}  -  CH_{2}  -  COONa  +  NaOH  \xrightarrow[\Delta]{CaO} এ + না_{2}CO_{3} ইউডিপোকার বিক্রয়তি কি নাম পর্যন্ত? A. উঠতাও শিখিয়া B. দি-কারবক্সেশোনা বিক্রিয়া C. উঠতাও ফিটিচ বিস্তারিত D. ফ্রাইডেল রাখ ট শিখিয়া Answer

## First Generated-BN Latin-Fragment Warnings

- `benqa_12th-Physics-I_0109` fragments=shon preview=তরকার ওপর নাম কি? A. ধরshon বল B. এরকম ভুরামক C. ঘুরনোন বল D. কিন্তুমুখি বল Answer with only A, B, C, or D.
- `benqa_10th-Biology_0197` fragments=kond preview=কষ্টের সকল জৈবিক ক্রিয়ে হিরোনটরন করে কোনো? A. নিুয়াযাস B. রানাবৈম C. লাগলোম D. মেথkondরিয়া Answer with only A, B, C, or D.
- `benqa_8th-Science_0153` fragments=dro preview=প্যাকোস্টল এর এসব টি নরমায়ে কোন উপযোগি? A. চালুসিয়াম B. ইসিটিক ইসিদ C. অভুমিনিয়াম হাইধরসাইদ D. এমনামাইয়া হইdroক্সাইড Answer with only A, B, C, or D.
- `benqa_12th-Chemistry-I_0140` fragments=drob preview=CaF_{2}-এর সম্পর্কে যদিই drobোন ফুলেল এইনের হচ্ছে 0.00655  gL^{-1} হলে CaF_{2} এর ড্রাবিটা গুনোফাল কতো হবে? A. 3.7\times  10^{-13} B. 2.048\times  10^{-10} C. 3.7\times  10^{-12} D. 2.048\times  10^{-11} Answer with only
- `benqa_10th-Chemistry_0374` fragments=kol preview=ইতিলিন গ্রেইkol কোন ধরণের যুগ? A. আলডাহিইড B. অলকোহল C. আলাকিন D. আলকাইন Answer with only A, B, C, or D.
- `benqa_10th-Physics_0055` fragments=shon preview=পেনিতে সুন্দর কাটার সময় কোন বন্ধ ঐক্রিম করতে হয়? A. সত্যি গরশন B. গতুই ধরshon C. অ্যাব্ট গরশন D. প্রেমি ধরshon Answer with only A, B, C, or D.
- `benqa_10th-Biology_0143` fragments=daya preview=একসামিক কিছুনি ওকেয হতে পারে কোন কারনে? A. dayaবেটিস B. নেটফ্রাইটিস C. মারামক দিয়া D. উচিত রকতোকাপ Answer with only A, B, C, or D.

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
