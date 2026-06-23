# TakeMeter

TakeMeter classifies Steam reviews for Subnautica into four discourse types — `analysis`, `experience`, `joke`, or `noise` — so readers can filter by what they actually want to learn. Built by fine-tuning DistilBERT and comparing it against a Groq zero-shot baseline.

## Community

Subnautica (Steam app ID 264710) is a survival/exploration game with a large and humor-driven review community. It was chosen because its reviews naturally span all four label types without needing to search for specific examples.

The game's well-known community meme culture — around leviathan encounters, the no-pause mechanic, the game's underwater horror — makes the `joke` label well-defined and testable. Jokes in this community require recognizing in-game references, creating a genuine classification challenge that separates surface humor from Subnautica-specific humor. The game also produces both detailed mechanical reviews (`analysis`) and strong emotional playthrough stories (`experience`) in large volume, so all four label types are naturally common in the corpus. With over 200,000 reviews on Steam, a balanced 200-example dataset across all four labels is achievable without relaxing the English-language or purchaser-only filters.

## Labels

Four labels capture the type of discourse in each review — not whether it is positive or negative. Full edge-case decision rules are in [`data/taxonomy.md`](data/taxonomy.md).

### `analysis`

The review makes a claim about the game — its mechanics, design decisions, performance, missing features, or price. Thin claims count ("runs great", "well optimized").

> "The base building leaves a lot to be desired. Way more obtuse and annoying than it needed to be. Missing some quality of life updates I kinda expect from survival games at this point."

> "Subnautica's default VR support is unplayable without mods because the controller does not work on quest 3. Furthermore, it's terrible for anyone with neck problems."

### `experience`

The review describes something that happened to the reviewer during their playthrough — a personal moment, emotional reaction, frustration, or story. Thin reactions count ("love it", "great game").

> "I played for 4 hours, and never had any items spawn other than the fish needed for basic survival. I could not get past the first step of the story, despite trying mods, reinstalls, restarts, and new saves."

> "I found the game grindy and very frustrating. It felt like working rather than playing a game. I rage-completed it but I didn't enjoy it."

### `joke`

The review is written to be funny or absurdist, and the humor references the game, its creatures, mechanics, or community culture. The joke only lands if you know Subnautica. A bare reference with no punchline is not a joke.

> "you cant sex reaper leviathans (its been 19 hours and you cant sex reaper leviathans still, im so angry.)"

> "has to much water didnt like"

### `noise`

The review has no identifiable discourse type — gibberish, single content-free words or symbols, filler phrases, or off-topic content. A thin reaction ("great game") or vague claim ("runs great") still has a discourse type; `noise` is reserved for text with none at all.

> "gg"

> "fun its fun because its fun"

## Dataset

**Source:** Steam Reviews API (Subnautica, app ID 264710), filtered to English-language reviews from verified purchasers, collected from May 2026 onwards. 283 reviews were collected as the initial pool; a small number were removed for off-topic content before labeling.

**Labeling process:** All 282 reviews were manually labeled by a single annotator using the decision rules in [`data/taxonomy.md`](data/taxonomy.md). After manual labeling, Claude independently labeled the same reviews using the same taxonomy definitions; the two sets were compared to surface ambiguous cases. There were 16 disagreements (5.7%). Each disagreement was reviewed by the human annotator, who made the final call. No Claude label was accepted over the human label without review. The final dataset was sampled to 50 examples per label (200 total) to ensure balanced training.

**Label distribution (final dataset, 200 examples):**

| Label | Count |
|-------|-------|
| `analysis` | 50 |
| `experience` | 50 |
| `joke` | 50 |
| `noise` | 50 |
| **Total** | **200** |

**Three difficult-to-label examples:**

1. > "I LOST MY STUFF THAT IVE BEEN GRINDING FOR A WHOLE DAY BECAUSE I DIDNT PRESS A BUTTON. THERE SHOULD ALWAYS BE A AUTO-SAVE BUTTON FOR EVERYGAME NO MATTER WHAT."

   **Label: `experience`.** The review opens with a personal loss that pulls toward `experience`, but then pivots into a feature demand that looks like a design claim (`analysis`). Decision: strip the personal parts and read what literally remains without rewording — "THERE SHOULD ALWAYS BE A AUTO-SAVE BUTTON" is a *wish* ("should"), not a declarative property claim about the game ("is"). Wishes are not `analysis`.

2. > "someone pooed my pants"

   **Label: `joke`.** Constructed as a punchline about being scared by the game's underwater horror, but plausibly a genuine (if hyperbolic) fear reaction, which would be `experience`. Decision: the distancing language ("someone" instead of "I") and punchline structure signal comedic construction over a genuine personal account.

3. > "Lots of things to do and find"

   **Label: `analysis`.** Generic enough to describe almost any open-world survival game, which pulls toward `noise`. Decision: the review still asserts something about the game's properties — that it has content — even if thinly. A thin claim about the game is `analysis`, not `noise`.

## Results

### Zero-shot baseline (Milestone 4)

The Groq API (`llama-3.3-70b-versatile`) was used as a zero-shot baseline on the 30-review test split. The system prompt:

```
You are classifying Steam reviews for the video game Subnautica.
Assign each review to exactly one of the following categories.

analysis: The review makes a claim about the game — its mechanics, design, performance, or features. Thin claims like "runs great" or "good graphics" count.
Example: "The base building leaves a lot to be desired. Missing some quality of life updates I expect from survival games."

experience: The review describes the reviewer's personal reaction or playthrough story. Thin reactions like "great game" or "love it" count.
Example: "I got lost so many times and shat my pants (8) times."

joke: Written to be funny in a way that only lands if you know Subnautica. A bare reference with no punchline is not a joke.
Example: "you cant sex reaper leviathans (its been 19 hours and you cant im so angry.)"

noise: Has no identifiable discourse type at all — not even a thin reaction or claim about the game.
Example: "gg"

Respond with ONLY the label name.
Do not explain your reasoning.

Valid labels:
analysis
experience
joke
noise
```

**Results (30/30 parseable responses):**

| Label | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| analysis | 0.67 | 1.00 | 0.80 | 8 |
| experience | 0.86 | 0.86 | 0.86 | 7 |
| joke | 1.00 | 0.50 | 0.67 | 8 |
| noise | 0.86 | 0.86 | 0.86 | 7 |
| **macro avg** | **0.85** | **0.80** | **0.80** | **30** |

Accuracy: 0.800

**Reflection:** The weakest label was `joke` (recall = 0.50) — the model missed 4 in 8 jokes. `analysis` had the lowest precision (0.67), meaning it over-fired on non-analysis reviews. Both issues point to the same failure: Subnautica-specific deadpan humor reads as a sincere reaction or claim to a model with no community context. The model never falsely labels something as `joke` (precision = 1.00), but it cannot recognize a joke when it sees one without prior exposure to the community's style.

**Hypothesis:** Fine-tuned DistilBERT will recover `joke` recall most, because it will learn from labeled examples that short, punchy Subnautica-referencing phrases signal `joke` even without obvious comedic markers. The `analysis`/`experience` boundary — where the baseline already performs well — should stay stable or improve slightly.

### Fine-tuned DistilBERT (Milestone 5)

**Base model:** `distilbert-base-uncased` | **Platform:** Google Colab (T4 GPU) | **Split:** 70/15/15 → 140 train / 30 validation / 30 test

`distilbert-base-uncased` was fine-tuned on the 140-review training split. Several hyperparameter combinations were explored; the key findings were:

- The original course-provided settings (`warmup_steps=50`, `batch=16`, `lr=2e-5`, 3 epochs) failed silently — `warmup_steps` exceeded the total training steps (~27), so the learning rate never reached its target and `joke` recall was 0.00.
- Fixing warmup and reducing batch size to 8 (doubling gradient updates per epoch) recovered `joke` recall.
- Lower learning rates (`2e-5`, `3e-5`) with more epochs generalized better than `5e-5`, which overfit by epoch 4–5.

**Final hyperparameters:**

```python
num_train_epochs=15,
per_device_train_batch_size=8,
learning_rate=2e-5,
warmup_steps=10,
metric_for_best_model="accuracy",  # best checkpoint: epoch 10, val acc 0.700
```

**Training (best run):**

| Epoch | Training Loss | Val Loss | Val Accuracy |
|-------|--------------|----------|-------------|
| 1 | 1.3756 | 1.3229 | 0.233 |
| 5 | 0.6390 | 0.9474 | 0.667 |
| 10 | 0.1394 | 0.8290 | 0.700 |
| 15 | 0.0750 | 0.8948 | 0.700 |

**Results (30 test examples):**

| Label | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| analysis | 0.55 | 0.75 | 0.63 | 8 |
| experience | 0.60 | 0.43 | 0.50 | 7 |
| joke | 0.88 | 0.88 | 0.88 | 8 |
| noise | 1.00 | 0.86 | 0.92 | 7 |
| **macro avg** | **0.76** | **0.73** | **0.73** | **30** |

Accuracy: 0.733

**Hypothesis check:** The M4 hypothesis held — fine-tuning recovered `joke` recall most (0.50 → 0.88), confirming that labeled examples taught the model Subnautica-specific humor patterns. Contrary to the hypothesis, the `analysis`/`experience` boundary did not stay stable: both labels underperformed the baseline, suggesting that distinguishing personal reactions from game claims requires broader language understanding that a 66M-parameter model cannot match from 140 training examples.

**Confusion matrix** (see also [`confusion_matrix.png`](confusion_matrix.png)):

|  | Pred: analysis | Pred: experience | Pred: joke | Pred: noise |
|--|:--------------:|:----------------:|:----------:|:-----------:|
| **True: analysis** | 6 | 2 | 0 | 0 |
| **True: experience** | 4 | 3 | 0 | 0 |
| **True: joke** | 1 | 0 | 7 | 0 |
| **True: noise** | 0 | 0 | 1 | 6 |

The dominant error pattern is the `analysis`/`experience` boundary — 4 experience reviews were called `analysis` and 2 analysis reviews were called `experience`. These 6 errors account for all but 2 of the model's mistakes. `joke` and `noise` were nearly clean (1 error each).

**AI-assisted failure pattern analysis:**

All 8 wrong predictions were pasted into Claude to identify common themes. The dominant pattern: 6 of 8 errors fall on the `analysis`/`experience` boundary. Within that boundary, the consistent driver is surface word choice — reviews that name game mechanics (story, crafting, exploration) get predicted as `analysis` even when the reviewer is clearly describing a personal reaction, not making a claim about the game. High prediction confidence does not reliably signal correctness: 5 of the 8 errors had confidence ≥ 0.89, including the highest-confidence wrong prediction in the test set (0.96). What had to be corrected during training: the initial epoch count was too low (3 epochs with the course defaults), which gave the model too few passes over the already-small 140-example training set. Increasing to 15 epochs allowed the model to learn more of the label boundaries before overfitting, recovering `joke` recall from 0.00 to 0.88.

**Error analysis — 3 misclassified examples:**

1. > "its a very fun exploration type game, totally not scary at all"

   Actual label: `joke` | Predicted label: `analysis` (confidence: 0.96)

   Analysis: "Totally not scary at all" is obvious sarcasm to anyone who knows Subnautica is notorious for being terrifying. The model read it as a literal claim about the game's genre and tone and predicted `analysis` with near-certainty — the highest-confidence misfire in the test set. Sarcasm detection requires cultural context the fine-tuned model doesn't have.

2. > "Enjoyed, and actually got some jump scares. A little crafting and exploration, atmosphere really submerges you"

   Actual label: `experience` | Predicted label: `analysis` (confidence: 0.89)

   Analysis: The reviewer is describing their personal reaction, but the review names game mechanics (crafting, exploration, atmosphere) along the way. The model weighted those mechanic-referencing words heavily and called it `analysis`. This was also borderline in the original annotation — "mentions of mechanics pull towards analysis, but nothing specific is claimed against the mechanics."

3. > "bad endgame"

   Actual label: `analysis` | Predicted label: `experience` (confidence: 0.78)

   Analysis: A two-word property claim — exactly what `analysis` is for. The model likely read "bad" as an emotional reaction word and predicted `experience`. The lowest-confidence error of the three, and a clear sign that very short text gives the model too little signal to override its prior toward emotional language meaning `experience`.

**Sample classifications:**

| Text | True label | Predicted | Confidence |
|------|------------|-----------|------------|
| "Some QOL features are missing like building from your storage, but overall a very good experience even today." | `analysis` | `analysis` ✓ | 0.91 |
| "Genuinely the greatest game of all time." | `experience` | `experience` ✓ | 0.69 |
| "7.8/10 Too much water" | `joke` | `joke` ✓ | 0.87 |
| "gg" | `noise` | `noise` ✓ | 0.94 |
| "its a very fun exploration type game, totally not scary at all" | `joke` | `analysis` ✗ | 0.96 |

"7.8/10 Too much water" is a reasonable `joke` prediction: it references the IGN "7.8/10 too much water" review meme, which Subnautica players adopted ironically because the game is set almost entirely underwater. The humor only lands with community context — exactly the pattern the model learned to recognize. The incorrect prediction ("totally not scary at all") shows the opposite failure: sarcasm that requires the same kind of community context, but the model read it as a literal genre claim.

### Summary

| | Groq zero-shot (llama-3.3-70b) | DistilBERT fine-tuned |
|--|:---:|:---:|
| Accuracy | 0.800 | 0.733 |
| Macro F1 | 0.80 | 0.73 |
| `analysis` F1 | 0.80 | 0.63 |
| `experience` F1 | 0.86 | 0.50 |
| `joke` F1 | 0.67 | **0.88** |
| `noise` F1 | 0.86 | **0.92** |

The zero-shot baseline outperforms the fine-tuned model overall (macro F1 0.80 vs 0.73), but the fine-tuned model wins on `joke` and `noise` — the two labels that most depend on Subnautica-specific patterns. The fine-tuned model's weakness is `experience` (0.50), where its limited training data and smaller capacity compared to the 70B baseline make the `analysis`/`experience` boundary harder to learn. Both models meet the project's success criterion of macro F1 ≥ 0.70.

## Reflection

The taxonomy defined `analysis` and `experience` by discourse structure — what is the reviewer *doing*? Are they making a claim about the game, or describing what happened to them? The intended decision boundary is about communicative intent, not word choice. The model learned a surface approximation instead: reviews that name game mechanics (story, crafting, exploration, atmosphere) get classified as `analysis`; reviews with emotional or reaction language get classified as `experience`. This works for unambiguous cases but breaks exactly at the boundary the taxonomy anticipated — reviews where both word types co-occur, because a reviewer describes their personal experience *through* game mechanics. The model never learned to look past the vocabulary to the structure around it.

For `joke` and `noise`, the model learned the right signal. Subnautica-specific references are a reliable surface marker for `joke` because the label itself is surface-accessible — a joke requires community context, and community context lives in specific words. `noise` is similarly learnable: content-free text has no vocabulary to latch onto. The labels the taxonomy treats as conceptually simpler (`analysis` and `experience`) turned out harder for a small model to learn, because their boundary is about intent rather than lexicon. This is a data distribution problem, not a labeling problem. The labels were applied consistently — the human vs. Claude comparison produced only 5.7% disagreement, and the taxonomy decision rules are specific enough that two annotators land in the same place on most cases. The taxonomy correctly captures the distinction; the training set just doesn't provide enough boundary-case examples for the model to learn the intent-based signal. What the model overfit to was the most frequent co-occurring features per label across 140 training examples — never enough boundary cases to learn that mechanic words in an experience-framed sentence are still `experience`. More training examples specifically at the `analysis`/`experience` boundary would be the most direct fix.

## Spec Reflection

**One way the spec helped:** The spec required defining a concrete success criterion — macro F1 ≥ 0.70 — before training began. This grounded the hyperparameter search. When the first fine-tuning run returned `joke` recall of 0.00 and macro F1 of 0.47, the criterion made it clear the failure was catastrophic rather than marginal, which justified making substantial changes (fixing the warmup bug, halving the batch size, increasing epochs) rather than small adjustments. Without a stated threshold, it would have been easy to rationalize small improvements as progress.

**One way implementation diverged:** The Data Collection Plan specified up to 75 examples per label, adjusted down to the lowest label count with a floor of 50. The final dataset landed at exactly 50 per label. `joke` and `noise` reviews were sparse in the initial pool, and supplemental collection brought them to 50, but reaching 75 would have required expanding the date range or relaxing the English/purchaser filters — changing the review population in ways that felt worse than a smaller balanced dataset. 50-per-label balanced was chosen over 75-per-label unbalanced.

## AI Usage Transparency

### Review scraper generation (Milestone 1)

Claude was asked to generate a Steam Reviews API scraper including cursor-based pagination, date filtering (May 2026 onwards), English-language and verified-purchaser filters, and random sampling across positive and negative reviews. It produced `collect_data.py`, which was used without major revision to collect the initial 283-review pool. The only override was the sampling ratio — the spec called for 200 positive and 100 negative reviews, which was adjusted during collection based on actual availability.

### Label taxonomy design (Milestones 1–2)

The label definitions, boundary rules, and ambiguous case handling in `data/taxonomy.md` were developed iteratively with Claude — proposing definitions, testing them against real reviews, and identifying where two labels could apply. Claude produced draft definitions and a first set of edge cases. Several rules were revised after human review: the `noise` definition was rewritten to focus on "no identifiable discourse type" rather than content quality, and the `analysis`/`experience` boundary rule was changed from a "rewrite test" (too loose — rewording could flip any wish into a claim) to a "delete the personal parts" rule judged on grammatical mood ("should" vs "is"). All final definitions and decision rules were written by the human annotator.

### Label stress-testing (Milestone 3)

Before annotating the dataset, I asked Claude to generate synthetic Subnautica reviews positioned at each of the six pairwise boundaries between the four labels, then to rewrite them to be as borderline as possible. I classified each one by hand using `data/taxonomy.md`; the cases that couldn't be resolved cleanly exposed gaps in the taxonomy, which I then fixed. These reviews are **synthetic (AI-generated)** and are **not** part of the labeled dataset.

The six synthetic reviews (verbatim) and what each surfaced:

1. **`analysis` ↔ `experience`**
   > "combat is basically pointless, you're better off just avoiding everything. took me a good 10 hours to accept i wasnt supposed to win fights — i kept dying to the same reaper thinking i was underleveled or something. theres no leveling. you just run."

   Resolved as `analysis`. Exposed that the old "rewrite test" was loose — rewording could turn any wish into a claim — so it was replaced with a delete-the-personal-parts rule judged on grammatical mood ("should" vs "is").

2. **`analysis` ↔ `joke`**
   > "public service announcement: you cannot pause this game. the world does not stop for your doorbell, your dinner, or the reaper currently using your submarine as a chew toy. there is no pause. bring a catheter. 9/10"

   Resolved as `joke`. No analysis-vs-joke rule existed, so *Jokes built around a real fact* was added.

3. **`analysis` ↔ `noise`**
   > "solid game honestly, no real complaints. looks great, runs smooth even on my potato, lots to do. devs clearly put work into optimizing it. would recommend"

   Resolved as `analysis`. Thin claims about the game's properties — "runs smooth", "looks great", "lots to do" — are `analysis` even without specs or numbers. *Vague generic statements* was updated to make this explicit.

4. **`experience` ↔ `joke`**
   > "i live alone and last night i screamed loud enough that my neighbor knocked to check if i was okay. a leviathan came out of the dark and i threw my headset across the room. had to sit on my porch for ten minutes. this game is a menace and i have already reinstalled it"

   Resolved as `experience`. No gap — the existing *Humorous lines that reference a real reaction* rule already handled it.

5. **`experience` ↔ `noise`**
   > "finished it last week and honestly i still kind of miss it? hard to put into words. it just stuck with me in a way most games dont. anyway. good stuff"

   Resolved as `experience`. A sincere personal reaction — "I still kind of miss it", "it stuck with me" — is `experience` regardless of specificity. No gap — the `experience` definition already covered it.

6. **`joke` ↔ `noise`**
   > "peeper 🐟"

   Resolved as `noise`. No joke-vs-noise rule existed; a bare reference isn't a joke without comedic construction, so *References without a punchline* was added.

### Annotation assistance (Milestone 3)

After manual labeling was complete, Claude was given the same 283 reviews and the full taxonomy definitions and asked to label them independently. It produced a label and a short note for each review. The two sets were compared: there were 16 disagreements (5.7%). Each disagreement was reviewed by the human annotator, who made the final call — no Claude label was accepted without review. Notable overrides: Claude labeled "has to much water didnt like" as `noise` (missing the joke), and labeled "hell yea" as `experience` where the human called it `noise` (too thin to have any discourse type). All final labels in the dataset are the human annotator's.

### Failure pattern analysis (Milestone 6)

All 8 wrong predictions from the fine-tuned model were pasted into Claude and it was asked to identify common themes across them. Claude identified the `analysis`/`experience` boundary as the dominant failure (6 of 8 errors), surface word choice (mechanic nouns → `analysis`, emotional words → `experience`) as the consistent driver, and high prediction confidence as an unreliable correctness signal. Post length was also flagged as a potential pattern but was discarded after reviewing the examples — errors span from 2-word reviews to multi-sentence ones, so length is not the driver. The lexical-cue pattern was verified against the full confusion matrix before being included in the evaluation report.
