# Reference breakdown

Both reels were fetched with TikHub (`instagram/v1/fetch_post_by_url`, `tiktok/app/v3/fetch_one_video_by_share_url`). They were analysed with ffmpeg scene detection (`select='gt(scene,0.3)'`), 2 fps / 1 fps contact sheets, and Whisper. Neither reel has a spoken voice: Whisper returned only noise tokens. Both run on music and natural sound, and all the information is on-screen text.

---

## 1. "$1 vs $100 food": @sushi.monsters (Instagram reel Dd6UpSGo4Rk)

- **Plays:** 2,682,509 (TikHub `video_play_count`)
- **Length:** 27.04 s, 720x1280
- **Format:** one creator at a table, with two foods side by side on a round wooden board. He tastes the cheap one, then the expensive one. A score pops up after each bite. There are 3 rounds, then a cat-meme punchline.

### Shots (scene cuts at threshold 0.3)

| # | Start–end (s) | Shot |
|---|---|---|
| 1 | 0.00–2.40 | Wide: both burgers on the board, creator gestures at each. "1$" pops at 0.5 s, "100$" at 1.0 s |
| 2 | 2.40–4.96 | Punch-in: bites the $1 burger → "7/10"; bites the $100 cheese burger → green "10/10" |
| 3 | 4.96–6.48 | Round 2 wide: octopus. "1$" and "100$" pop in again |
| 4 | 6.48–8.52 | Bite of the $1 octopus |
| 5 | 8.52–11.16 | Bite of the $100 octopus → "3/10", green "4/10" |
| 6 | 11.16–14.16 | Round 3 wide: sausage vs giant ham, "1$" and "100$" |
| 7 | 14.16–18.60 | Bites → green "10/10" for $1, "9/10" for $100 (**the twist: cheap wins**) |
| 8 | 18.60–19.40 | Cut-away: black cat standing (meme) |
| 9 | 19.40–20.84 | Creator turns to the cat and hands it ham |
| 10 | 20.84–21.92 | Cat eats |
| 11 | 21.92–24.88 | Creator side-eye reaction |
| 12 | 24.88–26.44 | Cat "shrug" meme |
| 13 | 26.44–27.04 | Back to creator. The last frame matches the first for a loop |

- **Average shot length:** 27.04 / 13 = **2.1 s**. Each round is about 5–7 s.
- **Hook (0–2 s):** no words are spoken. On screen there are only the two price tags: "1$" at 0.5 s, then "100$" at 1.0 s, over both products side by side. The comparison is understood in under a second.
- **Price labels:** very large (about 7–8 % of frame height), heavy italic sans-serif, white digits with a thick black outline and a **green "$"**. They sit in the bottom fifth of the frame, under each item (cheap on the left, expensive on the right), and stay up for the whole wide shot.
- **Score / verdict labels:** same font. The winning score turns green. They appear right after each bite, so every round has its own mini-verdict.
- **Captions:** none. The price tags and scores carry everything.
- **Reveal timing:** the first round's verdict lands at 3.5 s (13 %). The twist verdict lands at 16.5 s (**61 %**), followed by the meme ending (31 % of the runtime).
- **Audio:** music and eating sounds. No voice.
- **Ending:** a meme pay-off, with no call to action. The last frame matches the opening wide shot so the reel loops.

## 2. "Cheap shammy vs premium microfiber": @flashdetaileurope (TikTok 7641213524924042498)

- **Plays:** 23,695,710 (TikHub `play_count`), 659,357 likes
- **Length:** 69.59 s, 1080x1920
- **Format:** a fixed camera on a wet car bonnet, filmed as one continuous test. There is only **one** hard cut, at 14.8 s, when the towel changes.

### Shots

| # | Start–end (s) | Shot |
|---|---|---|
| 1 | 0.00–14.83 | Cheap towel: "9€ shammy" label, then 3 wipe passes counted on screen as 1✅ 2❌ 3❌. It soaks up water and is wrung out |
| 2 | 14.83–69.59 | Premium towel: "26€ FLASH towel" label, then wipe passes counted 1✅ … 11✅ |

- **Average shot length:** 34.8 s. The pace comes from the action itself, with a new wipe every 2–3 s, not from edits.
- **Hook (0–2 s):** "9€ shammy" in small white text in the lower centre, and the cheap towel is already on the car. Nothing is spoken.
- **Price labels:** small (about 2.5 % of frame height), plain white sans-serif with a soft shadow, centred at about 78 % of frame height. The label shows for about 2 s when each product is introduced.
- **Captions:** only a running pass counter (number + ✅/❌ emoji) in the same spot.
- **Reveal / verdict:** the cheap towel fails at about 10 s (14 %). The premium towel's count keeps climbing, and the verdict is the final "11✅" at about 66 s (**95 %**).
- **Audio:** music bed and towel sounds. No voice.
- **Ending:** the premium towel is held up to the camera, with no end card and no CTA.

---

## Editing recipe (what I copied)

Open on **both extremes at once**: a split screen of the cheapest room and the most expensive room. Each half gets a huge price tag that pops in on beat, cheap one first and expensive one 0.5 s later (from the $1/$100 reel). The comparison has to be readable in under one second, before the first sentence ends. Then run one **tier per beat, cheapest first**, about 7–8 s each. Each beat is cut into **4 shots of about 2 s** (room → view → bathroom → standout detail), which matches the food reel's 2.1 s average. The tier's price tag (¥ big, then ≈ $, then hotel name and area smaller) slams in on the first frame of the beat and stays at least 2 s. Price tags use a heavy outlined sans-serif with a coloured currency symbol, low in the frame, at roughly 7 % of frame height. Keep a running "score" feel by giving each tier one honest trade-off line. Save the strongest visual (the skyline view) for the last tier, just before the verdict. Land the **verdict at about 75–80 %** of the runtime, as one line, where the cheaper-than-expected option can win (the food reel's twist at 61 % is what made it shareable). Then a 3-second CTA card. Our reel needs a voice for trust (a planner talking), so I add a voiceover the references don't have. I keep their "text tells the whole story with the sound off" rule: captions of 1–3 words, plus price tags that make sense without audio.
