# Script example: GATE M / West Bund Dream Center

## Final version (32 s, John v3) — the standard

Current text (`episodes/gatem/script.txt`): hook `Shanghai turned Asia's biggest cement factory into this. It's called Gate M…`, price said as `about 25 dollars per person`, CTA `Comment WOW, and we'll plan your trip for you.` (or `…for more incredible places in Shanghai.`). The table below is the Matilda cut it grew from; the beats are the same.

Every sentence carries one thing the viewer would miss if it were gone.

| Time | Line | What it gives the viewer | Shot(s) |
|---|---|---|---|
| 0–2 s | This was the biggest cement factory in Asia. | the surprise (hook) | night aerial + serif title card |
| 2–6 s | Now it's Gate M, the West Bund Dream Center, on the Huangpu River. | name + where (the only river mention until the directions) | GATE M sign → lit building → aerial |
| 6–9 s | It's super dog-friendly, so the café terraces are full of dogs. | a distinctive feature, shown | dog in stroller → dog at café table |
| 9–16 s | Inside the old silos, there's Wild Dock, where everything is grilled over apple-wood charcoal, for about 180 yuan per person. | named spot + location + what's special + price | silos → Wild Dock logo → grill → dish (label "about ¥180 / person") → cocktail |
| 16–20 s | Gentle Monster opened a store here in September, full of giant face sculptures. | famous brand + date + why it's worth seeing | storefront → sculptures wide → sculpture close |
| 20–25 s | The 800-meter riverfront looks out to Lupu Bridge, and it's best at blue hour, right after sunset. | size + view + **when to go** (Doubao-verified) | riverfront → couple facing Lupu Bridge → blue-hour skyline → sunset |
| 25–26 s | It's free to walk around. | cost | people walking past the yellow building |
| 26–31 s | Take Line 11 to 龙耀路, exit 4, then walk along the river to Tank Shanghai. | how to get there + what's next door | night aerial + metro pill → river and bridge at night |
| 31–33 s | Follow me for more Shanghai spots worth exploring. | CTA | silos with projections + follow sticker |

## The earlier 66 s version and why it felt padded

Good facts, but only ~28 of 66 s told the viewer something new.

| Line | Problem |
|---|---|
| "…now it's one of the coolest places to hang out in Shanghai." | Filler half-sentence (2.5 s). |
| "The old factory buildings are now full of indie shops and cafés, and it's super dog-friendly, so there are dogs at almost every table." | 7 s for one fact; "indie shops and cafés" names nothing. |
| "The original cement silos are still standing, and the silo rooftop looks right over the river." | Restates the hook; the rooftop wasn't confirmed open, so the line could only describe a view. |
| "…and the terrace has a view of the whole river." | Fourth river mention. |
| "Once it gets dark, the whole place lights up. Light shows get projected right onto the silos, and there's live music by the river." | Mood line + the Light Festival, which had already ended (misleading). |
| "Last winter, they even had an ice rink and a giant Christmas tree by the water." | Past event, not confirmed for this year. |
| "…so it's easy to make a whole evening out of it." | Filler. |
| Overall | "river" ×6 + "water" ×2, "silo" ×4, "whole" ×3. |

`scripts/script_audit.py` now catches every one of these automatically.

## Rules
- One idea per sentence; each sentence has a name, number, price, time or how-to.
- 4–6 named spots max; each gets its name + ONE concrete detail. Put building numbers, hours and extra tips in the Instagram caption instead.
- Say each thing once. Don't restate the hook.
- Present tense only for what's confirmed current (Doubao with dated sources). No over events.
- Every noun you say has a shot; no clean footage → cut the spot.
- Second person, plain words, no hype ("amazing", "hidden gem", "vibes") and no "here's the thing".
