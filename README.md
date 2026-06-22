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
| analysis | 0.73 | 1.00 | 0.84 | 8 |
| experience | 0.86 | 0.86 | 0.86 | 7 |
| joke | 1.00 | 0.62 | 0.77 | 8 |
| noise | 0.86 | 0.86 | 0.86 | 7 |
| **macro avg** | **0.86** | **0.83** | **0.83** | **30** |

Accuracy: 0.833

**Reflection:** The weakest label was `joke` (recall = 0.62) — the model missed roughly 3 in 8 jokes. `analysis` had the lowest precision (0.73), meaning it over-fired on non-analysis reviews. Both issues point to the same failure: Subnautica-specific deadpan humor reads as a sincere reaction or claim to a model with no community context. The model never falsely labels something as `joke` (precision = 1.00), but it cannot recognize a joke when it sees one without prior exposure to the community's style.

**Hypothesis:** Fine-tuned DistilBERT will recover `joke` recall most, because it will learn from labeled examples that short, punchy Subnautica-referencing phrases signal `joke` even without obvious comedic markers. The `analysis`/`experience` boundary — where the baseline already performs well — should stay stable or improve slightly.

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
