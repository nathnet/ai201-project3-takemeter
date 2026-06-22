# Subnautica Review Type Taxonomy

Each label captures the **type of discourse** in the review — not whether it is positive or negative, long or short, or well-written.

---

## Labels

### `analysis`
The review makes claims about the game — its mechanics, design decisions, performance, missing features, or price. Specific, verifiable claims are the clearest examples, but thin claims about the game's properties also count.

**Key signal:** Is the reviewer saying something about what the game *is*, rather than how it made them feel? "The oxygen tank lasts 45 seconds", "there is no multiplayer", "it runs at 110fps on a 2080 Ti" are analysis. So are thin claims like "runs great" or "well optimized" — they describe the game's properties, not the reviewer's reaction. "It felt grindy", "it was confusing", "it was fun" are not — those are personal reactions.

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
The review has no identifiable discourse type — it contributes no claim, personal account, or joke about the game. This includes gibberish, single content-free words or symbols, filler phrases, and off-topic content such as bug reports, support questions, or requests that belong in a forum rather than a review.

**Key signal:** Does this text say anything about the game or the reviewer's experience with it — even briefly? If no → `noise`. A thin reaction ("great game", "love it") or a vague claim ("runs great") still has a discourse type; reserve `noise` for text that has none at all.

**Clear examples:**
- "gg"
- "fun its fun because its fun"

**Uncertain case:**
- "Lots of things to do and find" — names a real quality of the game, but is generic enough to describe almost any open-world or survival game. Sits between `noise` and `analysis`.

---

## How to Handle Ambiguous Cases

**Feature requests, mechanic complaints, and claims wrapped in a personal story:**
Delete the personal parts — the story, the loss, the feelings — and read what literally remains, *without rewording it*. If a **declarative statement about the game** is left ("there *is* no leveling", "combat is pointless"), it's `analysis`. If only a **wish or demand** remains ("there *should* be autosave", "they need to add X"), it's `experience` — do not reword a wish into a claim. The deciding signal is grammatical mood, "should" vs "is", and it lives in the text, so two annotators reading the same words land in the same place.

- *`experience`:* "I LOST MY STUFF... THERE SHOULD ALWAYS BE AN AUTO-SAVE BUTTON" — strip the personal loss and only a wish remains.
- *`analysis`:* "combat is basically pointless, you're better off just avoiding everything. took me a good 10 hours to accept i wasnt supposed to win fights... theres no leveling. you just run" — strip the personal framing and the reviewer's own declarative claims remain: combat is basically pointless, theres no leveling, you just run.

**Short reviews that make a specific claim:**
Length alone does not determine the label. "Too much grinding for a story game" is one sentence, but it asserts something specific about the game's design balance. Short reviews that name a real quality or flaw of the game lean toward `analysis` or `experience`, not `noise`.

**Humorous lines that reference a real reaction:**
Some joke reviews are also plausibly describing how the game made the reviewer feel. Prefer `joke` when the review is clearly constructed for comedic effect (punchline structure, distancing language like "someone" instead of "I"). Prefer `experience` when the humor feels incidental to a genuine description of their reaction.

**Jokes built around a real fact, or deliberate false advice:**
A review can state something true and verifiable and still be a `joke` if the fact is the setup or vehicle for the humor rather than the point. The inverse also applies: a review can sound like `analysis` — specific numbers, step-by-step advice — but be deliberately false, written as a trap to send new players to their death. Both are `joke`. Strip the comedy away — if what remains is a genuine claim presented to inform a buyer, it's `analysis`; if the fact or false advice only exists to enable the bit, it's `joke`. When a specific claim seems suspicious, verify it — if it doesn't hold up in the game, treat it as `joke`.

**References without a punchline:**
Merely naming a creature, mechanic, or community meme does not make a review a `joke`. A joke needs comedic construction — a punchline, incongruity, or built bit. A bare reference with no construction and no discourse type (e.g. "peeper 🐟") is `noise`.

**Vague generic statements:**
"Great game", "fun", "love it", "too scared" — these are thin `experience` (a personal reaction), not `noise`. "Runs great", "well optimized", "good graphics" — these are thin `analysis` (a claim about the game's properties), not `noise`. Reserve `noise` for text with no discourse type at all: "gg", "e", random characters, phrases that say nothing about the game whatsoever, **gameplay tips or guides** written as if the review were a wiki entry or walkthrough (no evaluative stance, belongs in a forum), and **incoherent or garbled writing** that cannot be parsed into any discourse type.

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
