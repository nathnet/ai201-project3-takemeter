# Subnautica Review Type Taxonomy

Each label captures the **type of discourse** in the review — not whether it is positive or negative, long or short, or well-written.

---

## Labels

### `analysis`
The review makes specific, verifiable claims about the game — its mechanics, design decisions, performance, missing features, or price — that a prospective buyer could independently confirm.

**Key signal:** The claims could be fact-checked. "The oxygen tank lasts 45 seconds", "there is no multiplayer", "it runs at 110fps on a 2080 Ti" are analysis. "It felt grindy", "it was confusing", "it was fun" are not — those are reactions, not verifiable facts about the game.

**Clear examples:**
- "The base building leaves a lot to be desired. Way more obtuse and annoying than it needed to be. Missing some quality of life updates I kinda expect from survival games at this point."
- "Subnautica's default VR support is unplayable without mods because the controller does not work on quest 3. Furthermore, it's terrible for anyone with neck problems."

**Uncertain case:**
- "Too much grinding for a story game" — asserts a design critique, but could also be read as a personal frustration from their playthrough rather than an evaluation of the game's structure. Sits between `analysis` and `experience`.

---

### `experience`
The review describes something that happened to the reviewer during their playthrough — a personal moment, emotional reaction, frustration, or story. The focus is on the reviewer's journey, not an evaluation of the game's design.

**Key signal:** The reviewer is telling you what happened to them, not arguing about what the game is. Often uses past tense, first-person narrative, or describes a specific in-game event.

**Clear examples:**
- "I played for 4 hours, and never had any items spawn other than the fish needed for basic survival. I could not get past the first step of the story, despite trying mods, reinstalls, restarts, and new saves."
- "I found the game grindy and very frustrating. It felt like working rather than playing a game. I rage-completed it but I didn't enjoy it."

**Uncertain case:**
- "I LOST MY STUFF THAT IVE BEEN GRINDING FOR A WHOLE DAY BECAUSE I DIDNT PRESS A BUTTON. THERE SHOULD ALWAYS BE A AUTO-SAVE BUTTON FOR EVERYGAME NO MATTER WHAT." — opens as a personal loss (experience) but pivots into a feature demand and design critique, which pulls toward `analysis`.

---

### `joke`
The review is written to be funny or absurdist, and the humor references the game, its creatures, mechanics, or community culture. The joke only lands if you know Subnautica.

**Key signal:** The review is constructed as a punchline or comedic bit rather than a genuine description of the game or the reviewer's time with it.

**Clear examples:**
- "you cant sex reaper leviathans (its been 19 hours and you cant sex reaper leviathans still, im so angry.)"
- "has to much water didnt like"

**Uncertain case:**
- "someone pooed my pants" — constructed as a punchline, but could also be read as a genuine (if hyperbolic) description of being frightened by the game. Sits between `joke` and `experience`.

---

### `noise`
The review contributes nothing to a reader's decision to buy or avoid the game. This includes gibberish, single content-free words, filler phrases, and off-topic content such as bug reports, support questions, or requests that belong in a forum rather than a review.

**Key signal:** Does this tell a reader anything — positive, negative, or neutral — that would inform their decision about the game? If no → `noise`.

**Clear examples:**
- "gg"
- "fun its fun because its fun"

**Uncertain case:**
- "Lots of things to do and find" — names a real quality of the game, but is generic enough to describe almost any open-world or survival game. Sits between `noise` and `experience`.

---

## How to Handle Ambiguous Cases

**Feature requests and mechanic complaints:**
Rewrite the review's core claims as "this game does X." If the rewrite preserves most of the review's meaning, the original is making claims about the game → `analysis`. If the rewrite collapses the review into one generic sentence (e.g. "please add autosave"), the substance was personal and session-specific → `experience`.

**Short reviews that make a specific claim:**
Length alone does not determine the label. "Too much grinding for a story game" is one sentence, but it asserts something specific about the game's design balance. Short reviews that name a real quality or flaw of the game lean toward `analysis` or `experience`, not `noise`.

**Humorous lines that reference a real reaction:**
Some joke reviews are also plausibly describing how the game made the reviewer feel. Prefer `joke` when the review is clearly constructed for comedic effect (punchline structure, distancing language like "someone" instead of "I"). Prefer `experience` when the humor feels incidental to a genuine description of their reaction.

**Vague generic statements:**
"Great game", "Lots of things to do and find", "fun", "too scared" — ask whether the statement gives a reader any real signal about the game. If it names something specific enough to inform a buying decision, lean toward `experience` or `analysis`. If it communicates nothing a reader couldn't already assume about the game or its genre, lean toward `noise`.

**Off-topic reviews (delete, do not label):**
Reviews that discuss the developer, company ethics, EULA, or Steam refund policy without meaningfully discussing the game itself are off-topic. Delete these rows before annotating.

---

## Valid Labels

```
analysis
experience
joke
noise
```
