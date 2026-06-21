# TakeMeter — Planning Document

---

## Community

Subnautica's Steam review community spans a wide spectrum — from players who write detailed mechanical critiques and performance benchmarks to those sharing personal playthrough stories, contributing to the game's well-known meme culture around underwater horror, or leaving content-free filler. These four types reflect genuinely different modes of engagement with the game: analytical evaluation, personal storytelling, in-group humor, and noise. The goal is to separate useful content from non-useful content so that readers can filter reviews by what they actually want to learn — whether that's how the game plays, how it feels, or what the community jokes about. With over 200,000 reviews spanning vastly different writing styles, intents, and lengths, the community produces enough natural variance across all four label types to make classification both meaningful and non-trivial.

---

## Labels

Four labels are used, each capturing the type of discourse rather than whether the review is positive or negative. Two clear examples per label and their uncertain cases are documented in [`data/taxonomy.md`](data/taxonomy.md), along with full definitions and edge case decision rules.

| Label | Definition |
|-------|------------|
| `analysis` | The review makes specific, verifiable claims about the game — its mechanics, design decisions, performance, missing features, or price. |
| `experience` | The review describes something that happened to the reviewer during their playthrough — a personal moment, emotional reaction, frustration, or story. |
| `joke` | The review is written to be funny or absurdist, and the humor references the game, its creatures, mechanics, or community culture. |
| `noise` | The review contributes nothing to a reader's decision to buy or avoid the game — gibberish, filler, or off-topic content such as bug reports and support questions. |

---

## Hard Edge Cases

The following cases sit genuinely between two labels. Decision rules for each are documented in [`data/taxonomy.md`](data/taxonomy.md) under *How to Handle Ambiguous Cases*.

- **"I LOST MY STUFF THAT IVE BEEN GRINDING FOR A WHOLE DAY BECAUSE I DIDNT PRESS A BUTTON. THERE SHOULD ALWAYS BE A AUTO-SAVE BUTTON FOR EVERYGAME NO MATTER WHAT."** — opens as a personal loss (`experience`) but pivots into a feature demand and design critique (`analysis`). Annotated as `experience` — applying the rewrite test (*Feature requests and mechanic complaints*), the core claims collapse to a single generic sentence ("please add autosave"), meaning the substance is personal and session-specific rather than a claim about the game.
- **"someone pooed my pants"** — constructed as a punchline (`joke`) but plausibly describes a genuine fear reaction to the game's underwater horror (`experience`). Annotated as `joke` — the distancing language ("someone" instead of "I") and punchline construction signal comedic intent over genuine reaction, per *Humorous lines that reference a real reaction*.
- **"Lots of things to do and find"** — references a real quality of the game (`experience`) but is too vague to meaningfully inform a buyer's decision (`noise`). Annotated as `noise` — it communicates nothing a reader couldn't already assume about an open-world survival game, per *Vague generic statements*.

---

## Data Collection Plan

Reviews are collected from Steam (Subnautica, app ID 264710) using the Steam Reviews API, filtered to English-language reviews from Steam purchasers from May 2026 onwards. 300 reviews are collected as a pool — 200 positive and 100 negative by Steam rating — to ensure content variety before annotation.

After labeling all 300 reviews, the final dataset is assembled by taking up to 25% of each label, capping at 75 examples per label. If the distribution is unequal, the cap is adjusted down to the lowest label count, with a floor of 50 examples per label (200 total minimum). If any label falls below 50 examples after labeling the full 300, an additional collection run will be made targeting reviews likely to produce more examples of that type.

---

## Evaluation Metrics

Both the fine-tuned DistilBERT model and the Groq zero-shot baseline (llama-3.3-70b-versatile) are evaluated on the same held-out test set. Results are reported as a classification table with per-label precision, recall, and F1 for each of the four labels, plus overall accuracy and macro F1 as summary rows. Macro F1 — the equal-weighted average of per-label F1 across all four labels — is the headline number used to compare the fine-tuned model against the Groq baseline, because it treats each label equally regardless of example count. The per-label rows show which specific labels each model handles well and which it confuses.

---

## Definition of Success

The fine-tuned DistilBERT model is considered good enough if it achieves a macro F1 of ≥ 0.70 on the held-out test set and outperforms the Groq zero-shot baseline on the same set. The 0.70 threshold reflects reasonable performance on a 4-class short-text problem — meaningfully above the 0.25 random chance floor — while accounting for the inherent difficulty of the `experience` / `analysis` and `joke` / `noise` boundaries.

---

## AI Tool Plan

**Review scraper generation.** Claude generated the Steam Reviews API scraper (`collect_data.py`) used to pull the review pool — including cursor-based pagination, date filtering, and random sampling logic.

**Label taxonomy design.** Each label's boundaries, ambiguous case handling, and examples were developed collaboratively with Claude — proposing definitions, testing them against real reviews, and iteratively refining the rules until the taxonomy was stable. The final definitions and decision rules are documented in `data/taxonomy.md`.

**Label stress-testing.** Claude will be given the label definitions and asked to generate one synthetic review sitting at each of the 6 pairwise boundaries — `analysis` vs `experience`, `analysis` vs `joke`, `analysis` vs `noise`, `experience` vs `joke`, `experience` vs `noise`, and `joke` vs `noise`. If any generated review cannot be cleanly classified using the current rules, the definition will be tightened before annotation begins.

**Annotation assistance.** After manual annotation is complete, Claude will be given the same reviews and asked to label them independently using the taxonomy definitions. The two sets of labels will be compared: disagreements indicate reviews where the definition is ambiguous or the rule is not specific enough. Disagreements are logged; any review where the labels diverge is re-examined and the final label is decided by the human annotator.

**Failure pattern analysis.** After evaluation, the list of wrong predictions from the fine-tuned model will be given to Claude and asked to identify patterns — which label pairs are most confused, whether there is a post type or length that the model consistently mislabels, and whether the errors cluster around the known hard boundaries. Patterns identified this way will be verified against the actual confusion matrix before being included in the evaluation report.

---