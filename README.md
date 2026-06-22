# TakeMeter

A text classifier for Subnautica Steam reviews that sorts each review into one of four discourse types — `analysis`, `experience`, `joke`, or `noise` — so readers can filter reviews by what they actually want to learn. Built by fine-tuning DistilBERT and comparing it against a Groq zero-shot baseline. See [`planning.md`](planning.md) for the full plan and [`data/taxonomy.md`](data/taxonomy.md) for label definitions.

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
