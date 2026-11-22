# Nicole in China top 10: 3 videos per place

Request (22 Nov 2026): take @nicole.inchina's 10 most-viewed posts from the last 3 months (22 Aug to 22 Nov 2026),
make 3 videos per place and post them as trial reels, 3 every 12 hours, without asking first.
- **A**: like Nicole's reel: no narration, music + one small meme-style text line, long POV takes (~4-6 s), aesthetic Douyin footage.
- **B, C**: china-spot-video skill (research, narration, labels), two different angles.
- Account: @steven_chinapal, trial reels, graduation MANUAL.
- CTA: "Follow for more". No comment keyword, because the ChinaPal repo (DM auto-replies) was not available in this session.
- Cadence: one video every ~4 h (= 3 per 12 h), made just before it posts, so usage is spread out. Order: Nicole's ranking, A then B then C.

## Ranking (reels, views as of 22 Nov 2026; duplicates of one place merged under its best reel)
| rank | place | Nicole's best reel | views | other reels of it |
|---|---|---|---|---|
| 1 | Harbin Ice-Snow World (哈尔滨冰雪大世界) | [De1USPhyy1_](https://www.instagram.com/reel/De1USPhyy1_/) | 968,399 | Df95gc3SDt9 329k, DewUVcZIhl8 317k, DerIZlkyrfQ 267k |
| 2 | Aurora village, Altay, Xinjiang | [DeRSANzFOKU](https://www.instagram.com/reel/DeRSANzFOKU/) | 962,678 | |
| 3 | Go-kart boats on water (location to identify) | [DeG9FEiD5pt](https://www.instagram.com/reel/DeG9FEiD5pt/) | 491,510 | |
| 4 | Guangzhou kart racing (venue to identify) | [DclH6T0yABG](https://www.instagram.com/reel/DclH6T0yABG/) | 345,224 | |
| 5 | Shanghai 4,000 m² indoor playground, 100+ activities (venue to identify) | [Dfo59N0ya_R](https://www.instagram.com/reel/Dfo59N0ya_R/) | 259,521 | DfzJKi6yyqy 171k |
| 6 | Dunhuang (old city, desert sunset concert) | [DegqVrMSVKZ](https://www.instagram.com/reel/DegqVrMSVKZ/) | 221,255 | DdQ_hfXyr4R 125k |
| 7 | Zhangjiajie Grand Canyon slide | [DfExn_gSOM8](https://www.instagram.com/reel/DfExn_gSOM8/) | 145,682 | |
| 8 | Zhangjiajie 72 Qilou (72奇楼) | [DdoFhxHyg4-](https://www.instagram.com/reel/DdoFhxHyg4-/) | 140,133 | |
| 9 | Sea-view hotel, Yunnan (Fuxian Lake? to identify) | [Dcio0kPS2bP](https://www.instagram.com/reel/Dcio0kPS2bP/) | 116,549 | |
| 10 | Suichang Center of the Earth, Lishui (遂昌地心世界) | [DfhOuJsyfuJ](https://www.instagram.com/reel/DfhOuJsyfuJ/) | 99,306 | |

Left out: pinned older reels (DcTC8i0S_-X 21 Aug, 3.69M, one day outside the window; DXwCE7IyAX0 Apr; DS--vqEikGD Jan).

## Queue (status: todo / made / posted)
| # | place | version | status | file | permalink |
|---|---|---|---|---|---|
| 1 | 1 | A | posted 22 Nov | harbin_A_1080.mp4 | https://www.instagram.com/reel/DgDEi6pIet3/ |
| 2 | 1 | B | todo | | |
| 3 | 1 | C | todo | | |
| 4 | 2 | A | todo | | |
| 5 | 2 | B | todo | | |
| 6 | 2 | C | todo | | |
| 7 | 3 | A | todo | | |
| 8 | 3 | B | todo | | |
| 9 | 3 | C | todo | | |
| 10 | 4 | A | todo | | |
| 11 | 4 | B | todo | | |
| 12 | 4 | C | todo | | |
| 13 | 5 | A | todo | | |
| 14 | 5 | B | todo | | |
| 15 | 5 | C | todo | | |
| 16 | 6 | A | todo | | |
| 17 | 6 | B | todo | | |
| 18 | 6 | C | todo | | |
| 19 | 7 | A | todo | | |
| 20 | 7 | B | todo | | |
| 21 | 7 | C | todo | | |
| 22 | 8 | A | todo | | |
| 23 | 8 | B | todo | | |
| 24 | 8 | C | todo | | |
| 25 | 9 | A | todo | | |
| 26 | 9 | B | todo | | |
| 27 | 9 | C | todo | | |
| 28 | 10 | A | todo | | |
| 29 | 10 | B | todo | | |
| 30 | 10 | C | todo | | |

## How each run works (scheduled every 4 h, one video per run)
1. Take the first `todo` row. Work dir: `work/<slug>/` (gitignored); committed files go in `episodes/nicole-top10/<slug>/`.
2. First run for a place (version A): watch Nicole's best reel for it (`scripts/ig_fetch.py` + `sheet.py`), identify the exact place (Chinese name), search Douyin, download the most **aesthetic** clips. Looks are the only filter: camera watermarks (DJI etc.) and 720p are fine if the shot is beautiful; skip TikTok/Douyin watermarks, staged/AI labels and other branches.
3. Version A: `scripts/nicole_style.py <workdir> <slug>_A` (plan_A.py: long POV takes ~3-6 s, one small meme-style text line in the first ~8 s, a "save this" line at the end, music bed). Check the contact sheet for scene changes inside a shot (`cuts.sh` misses some).
4. Versions B/C: china-spot-video skill, sections 1-8 (fact sheet in `<slug>/README.md`, John voice, ~35-45 s), two different angles. CTA "Follow for more China" (no keyword). Write B's fact sheet before B.
5. One caption per place (same for A/B/C), no AI/source mentions. Post with the instagram-trial-reel skill, `--yes` (pre-approved by the creator on 22 Nov 2026).
6. Mark the row posted with its permalink, commit plan/caption/README + `.ig.json`, push.
