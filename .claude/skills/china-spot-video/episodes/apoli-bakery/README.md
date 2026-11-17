# APOLI ITABAKERY (AP意大利料理面包坊), Shanghai: "the Hogwarts bakery" (Nov 2026)

The creator asked for "Apollo Cafe, the Harry Potter / Hogwarts cafe in Shanghai". No wizard-themed "Apollo" cafe exists. The place people mean is **APOLI ITABAKERY**, an Italian bakery across from Wukang Mansion that visitors and media call "Shanghai's Harry Potter bakery" for its castle interior. The only Shanghai "Apollo" is a Latin-American bar on Anfu Lu with no theme. The one real Harry Potter-themed café, Wonder Palazzo (歪歪宫殿) in Hongkou, is likely closed (its listing hasn't been updated since 2020).

**It is NOT licensed and NOT themed:** no wands, robes, butterbeer or sorting hat. Every version says "not official" or "Italian bakery". Never call it a Harry Potter café.

Keyword **CASTLE** (unused in ChinaPal `code-rules.ts` as of 17 Nov 2026). Voice: John. Previews: A 32.8 s, B 36.0 s, C 34.0 s, all at -15 LUFS.

## Three angles
- **A "the walkthrough"**: "There's a bakery in Shanghai that looks like Hogwarts." Door → stone walls → branches → chandeliers → counters → the price pivot. Relaxed pace (1.56 s/shot), 2×2 collage + serif title "SHANGHAI'S / Hogwarts Bakery", handwritten labels.
- **B "London vs Shanghai"**: "The Harry Potter studio tour in London costs about $77…" Then: a castle you walk into for free, and $2 pastries. Fast (0.97 s/shot), opens full screen on a $77 card with no collage, plus a "Shanghai, not London" label at once (so the London card is never read as this footage), and price cards.
- **C "4 things to know"**: not official / no booking + queues / self-service / cheap + mentaiko pick. Medium pace (1.21 s/shot), one full-screen hero shot under "4 THINGS / to know before you go", #1–#4 stickers.
`compare_cuts.py`: all pairs ok (order 0.42–0.50; openings all different).

## Fact sheet (✔✔ = 2+ sources, ✔ = single, ⚠ = conflicting)
| fact | figure | source(s) | conf |
|---|---|---|---|
| Name | APOLI ITABAKERY·AP意大利料理面包坊(上海首店) | Apple Maps (Dianping data) maps.apple.com/place?auid=1118732206030370; hedonisthk.blogspot.com 2026/04 | ✔✔ |
| Address | 长宁区兴国路380号, diagonally across from Wukang Mansion (武康大楼) | Apple Maps; thirdeyetraveller.com/apoli-itabakery-shanghai; eatbook.sg/best-shanghai-cafes; citynewsservice.cn/articles/okwvxbyn | ✔✔ |
| Metro | Jiaotong University (Lines 10/11), Exit 7, ~430–500 m | Apple Maps; Third Eye | ✔✔ |
| Opened | mid-Sept 2024 | news.qq.com/rain/a/20240923A07OJN00; sohu.com/a/811018659_113612 | ✔✔ |
| Hours | 9:00–21:00 (newer listings) vs 10:00–20:00 (older) | Apple Maps, Third Eye vs Eatbook, Lemon8 | ⚠ (videos never state hours) |
| Booking | none; walk in, queue to pay, then find a table | Third Eye; trip.com/moments/detail/shanghai-2-156767326 | ✔✔ |
| Entry fee / min spend | none | Third Eye; Eatbook | ✔✔ |
| Per person | ~¥43–50 ($6–7) | Apple Maps; 21jingji.com/article/20260914/… | ✔✔ |
| Item prices | most ¥12–25 ($2–3.50), list prices | Apple Maps; Eatbook; Tencent 2024 | ✔✔ |
| Mentaiko bread | ¥15, most-recommended item on Dianping (285 recs) | Apple Maps (Dianping data) | ✔ |
| Full tray + coffee | ~¥110 ($15) | Third Eye 2026; Lemon8 2025 (6 pastries ¥111) | ✔✔ |
| Range | 100+ rotating items | HK blog; Taiwanese article | ✔✔ |
| Queues | 1 h+ daily in the opening weeks (2024); shorter now, weekends busy | Tencent ×2 2024; Lemon8; Third Eye | ✔✔ |
| London studio tour | adult from ~£56–58.50 ≈ $75–78 → "about $77" | several 2026 guides; wbstudiotour.co.uk | ✔✔ |
| Licence | none; "Harry Potter bakery" is a nickname | Third Eye; Eatbook; Tencent | ✔✔ |
| Criticisms (not in video) | called a copycat of Japan's AMAM DACOTAN; food "so-so" to some; open display / hygiene; limited seating | Tencent 23 Sep + 17 Oct 2024 | ✔✔ |
| Branches | Jing'an Joy City (166 Xizang Bei Lu, 10–22), Wujiaochang Hopson One, Aranya. **Footage is the flagship only** (Joy City / Aranya clips rejected) | SmartShanghai; Apple Maps | ✔ |

## Footage (Douyin aweme ids; internal only)
P 7662654833274632698 (2026, clean, wide) · L 7417095420498726144 (clean) · G 7413386842168397107 (1080p 120 fps) · S 7556148391236128058 · Q 7414326013427060009 · R 7426794630210981178 · T 7418168285440593179 · H 7413297549991218486 (horizontal). Cuts and time ranges are in `srcs.py`.
- Burned subtitles sit at ~0.77 of the frame height in most clips (cut 0.26), ~0.66 in Q (cut 0.36) and ~0.85 in the horizontal H (cut 0.18).
- Rejected: 7700918950213647331 (Joy City branch), 7682258951262964870 and 7645496901541956900 (Aranya), 7567559588343279202 (an American creator's face and captions throughout), 7684892900367237371 (4K but with doodle overlays), 7413651957170048319 / 7599999408725602724 (collage and overlay edits).

## Notes
- TTS / Whisper: "Apoli" is heard as Apoly / Apolli / "a Polly", and "Wukang" as Wukong, so the captions use CAPTION_FIX. B hears "candle" as "handle" (fixed in the captions). A's "Then come the counters" lost "Then" when gaps were squeezed, so it became "And then, the counters." C's "Comment castle" was heard as "Common/Pommen castle", so it became "So, comment castle" (the leading word fixed it).
- After re-voicing, `scripts/remap_cues.py <workdir> <old words.json>` moves the plan's word indices. Check its output: reworded words map to the next matched word.
- "Cinnamon swirls": G 70.9–75.6 is labelled *Earl Grey snail rolls*, so A uses Q 43.4 (brioche cinnamon rolls).

## Trip-guide outline (for the "Comment CASTLE" DM)
APOLI ITABAKERY · AP意大利料理面包坊, 长宁区兴国路380号 (show to taxi / DiDi) · Metro 10/11 Jiaotong University Exit 7, ~7 min walk · walk-in only, no booking · go on a weekday morning; weekends and noon are busiest · take a tray and tongs, pick, pay at the till; drinks are collected by number · ~¥45–110 ($6–15) per person, Alipay / WeChat Pay · get the mentaiko bread (¥15) and the truffle chicken bread · one person holds a table · Wukang Mansion photo across the street, then walk Anfu Lu · busy? Joy City branch (10:00–22:00) · it's an Italian bakery with a castle look, not an official Harry Potter venue · footer "Want a full China itinerary? Reply PLAN". Date-stamp it (checked 17 Nov 2026).
