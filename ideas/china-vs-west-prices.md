# China vs West prices: ideas and scripts

Draft, Nov 2026. Every price below is a **ballpark to replace with what you film** (receipt, menu, price tag, app screen). Prices marked `¥__` / `$__` must be filled on the day.

## The angle

"Everything in China is cheap" is already a crowded genre. What makes it ours is the **Real or Hype? verdict**: take one viral price claim, test it with a receipt, and be honest when China is *not* cheaper. The episodes where China loses (Starbucks, imported food, sneakers) are the ones people argue about in the comments.

Recommendation: run it as a **price edition of Real or Hype?**, not a new series. It keeps the sting, the REAL/HYPE bar, the ticks and the audience you're building. The claim becomes "X is cheaper in China".

### Rules for this edition

- **One West reference per video, the US in $** (matches the $ already used in the series). Use one exchange rate per video, rounded, taken on shoot day (around ¥7.1 = $1, check it), and put it small on screen once: `¥7.1 = $1`.
- **Show both prices as proof**: China = your own shot of the tag or receipt. US = a dated screenshot from the official app or site (Starbucks app, Apple.com, a US friend's receipt). Never a number you can't show.
- **Same item, same size** (grande latte vs grande latte). Say when a deal is a coupon price.
- Price said once, as big yellow text (like "$20,000"), not read out and shown at the same time.
- Plain voice: name the thing, give the number, one flat opinion. No "China wins / America loses" tone; it's a price check, not politics.
- Skip fake/"replica" markets and anything that needs filming where it isn't allowed.

### What we reuse from the pipeline

| Existing piece | Price edition |
| --- | --- |
| Hook: viral card + context line | Same, context line is the claim: `"Coffee in China costs $1"` / `Shanghai` |
| Sting + REAL OR HYPE bar | Same |
| ONLINE / REAL LIFE panel | **CHINA / USA panel**: his price-tag shot left, US screenshot right, both prices in yellow |
| Yellow "$20,000" punch + typewriter ding | Same, for each price |
| Verdict ticks (green REAL / red HYPE + buzzer) | Same, two claims per episode |

New graphic needed: the CHINA / USA dual price card (one PIL overlay in `v9_overlays_extra.py` style).

## Ideas (ranked by how well they test + how much they'll be argued about)

| # | Claim to test | Where in Shanghai | Likely verdict | Why it works |
| --- | --- | --- | --- | --- |
| 1 | "Coffee in China costs $1" | Luckin + Starbucks on the same street | Luckin real, Starbucks hype | Twist built in; everyone knows Starbucks prices |
| 2 | "Glasses in China cost $20 and are ready in an hour" | A glasses market / optical mall (name to confirm) | Price real, 1 hour: test it | Two checkable claims, big price gap, useful to tourists |
| 3 | "You can buy a new electric car in China for $10,000" | BYD showroom (Seagull) | Real, but you can't buy it in the US | Huge number, showroom looks good on camera |
| 4 | "The metro costs 50 cents" | Any line, longest ride vs shortest | Real | Easy shoot, pairs with the how-to style of variant C |
| 5 | "Groceries are cheaper in China" | Hema / Sam's Club, 5-item basket | Local food real, imported food hype | Mixed verdict = comments |
| 6 | "Costco in China is the same as the US" | Costco Shanghai | Test the hot dog, the rotisserie chicken, the membership | Known US reference prices |
| 7 | "iPhones are cheaper in China" | Apple Store Nanjing Rd | Likely hype on sticker (US prices exclude tax) | Tax/subsidy twist |
| 8 | "Nike is cheaper in China" | Nike store, same shoe | Probably hype | Same shoe, two tags |
| 9 | "A haircut in China costs $5" | Neighbourhood barber vs mall salon | Real at the barber | Him in the chair = good visuals |
| 10 | "Taxis in China are almost free" | Didi from Pudong airport to the Bund | Real vs JFK–Manhattan | Long ride, clear number |
| 11 | "Street breakfast costs $1" | Jianbing / shengjian stall | Real | Food close-ups, cheapest shoot |

Start with 1, 2 and 3: they have the best visuals and the clearest verdicts.

## Script 1: Coffee (Luckin vs Starbucks), ~38 s

Viral clip to find: someone saying coffee in China is "like a dollar" (Luckin 9.9 deal). Context line: `"Coffee in China costs $1"` / `Shanghai`.

| Time | Picture | Audio |
| --- | --- | --- |
| 0–5 | Him deadpan, viral card left, context line top | Viral clip audio (A0) or VO: "People say coffee in China costs one dollar." |
| 5–7 | Sting | "Is it real or hype?" |
| 7–9 | Luckin storefront, him walking in | VO: "First, Luckin. This is the one everyone talks about." |
| 9–12 | Phone screen ordering in the app, price `¥9.9` | VO: "Iced latte, nine point nine on the app." |
| 12–13 | Yellow punch `$1.40` + ding | — |
| 13–15 | Cup in hand, sip | His line: "Honestly, it's good." |
| 15–17 | Menu board / app without coupon `¥__` | VO: "Without the deal, it's about ¥__." (only if it's notably higher) |
| 17–19 | Walk to Starbucks, same street | VO: "Now Starbucks, same street." |
| 19–22 | Menu board, grande latte `¥__` | — |
| 22–25 | CHINA / USA panel: his tag left, US app screenshot right, `$__` vs `$__` + ding | VO: "Grande latte. Almost the same price as in the US." |
| 25–27 | Him holding both cups | His line: "Same coffee money as back home." |
| 27–38 | Interior b-roll, then ticks | VO: "Overall: cheap coffee is real, but only at the Chinese chains. Starbucks costs the same." Ticks: LUCKIN ✓ REAL / STARBUCKS ✗ HYPE 💩 |

VO word count ~55.

Hook variants for trial reels:
- **A (claim)**: "People say coffee in China costs one dollar."
- **B (price shock)**: open on the `¥9.9` screen + `$1.40` punch, then "This is a latte in Shanghai. But there's a catch."
- **C (two cups)**: open on him holding both cups: "One of these was a dollar forty. The other one wasn't."

## Script 2: Glasses, ~39 s

Viral clip to find: "I got prescription glasses in China for $20 in one hour". Context line: `"Glasses for $20 in 1 hour"` / `Shanghai`.

Before filming: confirm the market's name and address, write it in Chinese characters in the script so the v3 voice says it in Mandarin (pinyin in the subtitles).

| Time | Picture | Audio |
| --- | --- | --- |
| 0–5 | Hook, viral card | VO: "People say you can get glasses in China for twenty dollars, in one hour." |
| 5–7 | Sting | — |
| 7–10 | Station exit, him walking to the building | VO: "First you get to this station, [name in Chinese]." |
| 10–13 | Entrance piece to camera | His line: "We're at the glasses market. The whole building is glasses." |
| 13–16 | Corridors of shops, walls of frames | VO: "Floor after floor, just glasses shops." |
| 16–19 | Eye test machine, him in the chair | VO: "Eye test is free." (only if it was) |
| 19–22 | Picking frames, mirror | — |
| 22–24 | Receipt / calculator `¥__` + yellow `$__` + ding | — |
| 24–26 | Phone clock / timer: start time | VO: "Frames and lenses. Now we wait." |
| 26–28 | Timer jump cut, glasses handed over | His line: "[x] minutes. Done." |
| 28–31 | CHINA / USA panel: his receipt vs US price `$__` (dated source) | VO: "In the US, about $__ without insurance." |
| 31–39 | Him wearing them on the street, ticks | VO: "Overall: the price is real. The one hour is [real / hype]." Ticks: PRICE ✓ REAL / ONE HOUR ✓ or ✗ |

Film the clock honestly: if it takes 3 hours, the HYPE tick is the better video.

## Script 3: Electric car, ~37 s

Viral clip to find: "In China you can buy a new electric car for $10,000". Context line: `"A new EV for $10,000"` / `Shanghai`. Ask the showroom before filming inside.

| Time | Picture | Audio |
| --- | --- | --- |
| 0–5 | Hook, viral card | VO: "People say in China you can buy a new electric car for ten thousand dollars." |
| 5–7 | Sting | — |
| 7–10 | BYD showroom exterior, him walking in | VO: "So we went to a BYD showroom." |
| 10–13 | The car, wide; him opening the door | His line: "This is the cheapest one they have." |
| 13–16 | Interior: screen, seats, him in the driver's seat | VO: "Big screen, four doors, about 300 km of range." (use the real spec on the stand) |
| 16–18 | Price stand `¥__` | — |
| 18–19 | Yellow punch `$__` + ding | — |
| 19–23 | CHINA / USA panel: price stand vs cheapest new US EV `$__` (dated) | VO: "The cheapest new EV in the US is about $__." |
| 23–26 | Him getting out, looking at the car | His line: "[his honest reaction]" |
| 26–37 | Street shots of cars, ticks | VO: "Overall: the price is real. But you can't buy one in the US." Ticks: $10,000 ✓ REAL / IN THE US ✗ HYPE |

Keep the US line factual (not sold there), no opinion on why.

## Next steps

1. Pick the first episode (my vote: coffee, cheapest and fastest to film).
2. Find the viral reaction clip: Bright Data TikTok keyword discover, e.g. "china cheap coffee", "luckin 9.9", "glasses china cheap", "byd seagull price".
3. Shot list for filming: every price shot steady for 3+ s, both the tag and his hand/face in one frame, the receipt flat, and a to-camera line at each location.
4. Build the CHINA / USA dual price card overlay.
