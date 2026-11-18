# Paid local experiences in Shanghai: 30 per method (scouted 17–18 Nov 2026)

The user's brief: find 30 unique local experiences in Shanghai that you pay for and get a service done, e.g. a photographer, a xiaolongbao workshop, a driving or test-drive experience, a robot experience, a massage.

Each method found its own 30, kept separate (120 rows, with overlaps):

| File | Method | How it searched |
|---|---|---|
| `doubao_30.md` | Doubao (Seed 2.1 Pro + web search) | 5 themed prompts that included the brief's examples. 36 results, 6 weak ones cut |
| `web_30.md` | Claude web search | Same brief and examples; English booking sites (Klook, Viator, SmartShanghai), government and press. 30 paid rows; 4 free extras listed below the line |
| `douyin_30.md` | Douyin via TikHub | 20 **open** keywords (上海 小众体验, 上海 体验课, 上海 付费体验…), no category hints: 475 videos, then 15 pin-down searches on venues already found |
| `xhs_30.md` | Xiaohongshu via TikHub | The same 20 open keywords: 318 notes, then 15 pin-down searches |
| `merged_30.md` | First merged pass | Combined list from 17 Nov. Douyin and XHS used keywords written from the brief there, so they confirmed rather than discovered |

## Each method's 30 (short names)
- **Doubao:**
  - Food: xiaolongbao class; dumpling & wonton home class; Song-dynasty whisked tea; snow-skin mooncake DIY
  - Crafts: Minhang night-school brocade and bamboo weaving; Aurora Museum cloisonné; Shanghai Museum mini-qipao
  - Driving & tech: Porsche Experience Centre; Pony.ai robotaxi; iKart indoor karts; Guma humanoid robots; Sandbox VR; F1-circuit track day; helicopter; 737 flight simulator
  - Body & style: TCM cupping/moxa; foot spa + ear cleaning; head spa; Doc's barber shave; qipao photoshoot
  - Classes: ink calligraphy; kung fu; mahjong + market
  - Outdoors & shows: Dishui Lake sailing; Suzhou Creek rowing/kayak; e-bike tour; horse riding; climbing; immersive dinner theatre
- **Web:**
  - Food: xiaolongbao class; Shanghainese home cooking; Song tea; robot-made DQ Blizzard; night food tour; hairy-crab feast
  - Classes & crafts: calligraphy + fan; seal carving; mahjong; kung fu; pottery wheel; Peking-opera costume workshop
  - Style & photos: qipao photoshoot; street-snap photographers; bespoke suit/qipao
  - Body: tuina & cupping; upscale massage; ear cleaning; head spa
  - Driving & tech: Vision Pro theatre; robotaxi; Porsche track drive; F1-track night karting; helicopter
  - Outdoors & shows: Qingpu kayaking; Huangpu yacht; indoor skiing; ERA acrobatics; English murder-mystery dinner; bike + street-food tour
- **Douyin:**
  - Body: bathhouse day pass; head spa; foot massage; oil spa massage
  - Play: rage room; trampoline/obstacle park; ice escape room; climbing + karts; full-body VR; archery tag; game/date rooms; murder mystery; paid blind-box meetup
  - Crafts & making: baking DIY; felt/anime craft; ring/perfume/bead DIY; perler beads; sewing class; night-school courses; heritage crafts; pottery; lampwork glass beads; farm "Overcooked" cooking
  - Shows & photos: maid café; palace-banquet dinner show; K-pop idol photoshoot; immersive theatre
  - Other: helicopter; Disney VIP guide; ballroom tea dance
- **Xiaohongshu:**
  - Body: bathhouse day pass; head spa; massage/spa; moxibustion
  - Crafts & making: resin "glue painting"; perler beads; paint-a-plate ceramics; cookie/chocolate decorating; sewing class; ancient-book restoration; embroidery patches; plum-wine brewing; Song tea; baking; bead bracelets; woodworking; incense-making
  - Sport: forest-park kayaking; indoor adventure park; sunset paddleboarding; skating rink; horse riding; tennis trial; boxing trial; aerial bungee/archery trials; drum-kit trial lesson
  - Shows & photos: palace-banquet dinner show; Chinese-myth escape room; qipao makeover + Bund photoshoot
  - Driving: Tianma drift/track ride

## Overlap
- **Found by all four:**
  - head spa
  - massage (tuina / foot / spa)
- **Found by three:**
  - helicopter flight (Doubao, web, Douyin)
  - kayak / paddling (Doubao, web, XHS)
  - qipao photoshoot (Doubao, web, XHS)
  - Song-dynasty tea (Doubao, web, XHS)
  - track driving (Doubao, web, XHS)
  - pottery (web, Douyin, XHS)
  - karting (Doubao, web, Douyin)
  - immersive theatre (Doubao, web, Douyin)
  - TCM / moxibustion (Doubao, web, XHS)
- **Douyin and XHS only:**
  - bathhouse day pass (the strongest signal on both)
  - palace-banquet dinner show
  - perler beads
  - indoor adventure park
  - sewing class
  - baking DIY
- **Doubao and web only:**
  - xiaolongbao class
  - calligraphy
  - kung fu
  - mahjong
  - robotaxi
  - Porsche drive
- Roughly 80–85 distinct experiences across the 120 rows.

## What this says about the methods
- **Doubao and web** reflect the brief and the tourist market. Results are English-bookable listings (Klook, Viator, GetYourGuide), with prices and addresses, close to the brief's examples. They are good for "where can a foreigner book X".
- **Douyin and XHS** reflect what locals actually pay for: bathhouses, DIY craft shops, perler beads, banquet shows, rage rooms, idol photoshoots, cheap trial classes. Prices are group-buy deal prices (美团/大众点评), often much lower.
- **On open searches, Douyin and XHS almost never surfaced the brief's own examples:**
  - Photographers came up only as a Bund qipao makeover.
  - Driving came up only as one Tianma drift ride on XHS.
  - Robots: none (the Unitree store is free; the DQ robot only makes ice cream).
  - No xiaolongbao class came up.
- **About 30% of open-search posts were relevant** (XHS ~120 of 318, Douyin ~150 of 475). The rest were free city walks, food and sightseeing.
- **Signal is thin past #20:** in both social lists, the rows below about #20 rest on 1–3 small posts.
- **Closed or not bookable:** Sleep No More closed on 30 Aug 2026. No paid robot boxing exists for the public; the URKL fights are spectator events.

Raw outputs (Doubao responses, search dumps, TikHub JSON) are in `work/shexp/` (gitignored, local to the session).
