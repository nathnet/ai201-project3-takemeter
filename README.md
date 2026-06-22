# TakeMeter

A text classifier for Subnautica Steam reviews that sorts each review into one of four discourse types — `analysis`, `experience`, `joke`, or `noise` — so readers can filter reviews by what they actually want to learn. Built by fine-tuning DistilBERT and comparing it against a Groq zero-shot baseline. See [`planning.md`](planning.md) for the full plan and [`data/taxonomy.md`](data/taxonomy.md) for label definitions.

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

**Results (30/30):**

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

## AI Usage Transparency

This section documents where AI tools were used in the project. More usages will be added as the project progresses.

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
