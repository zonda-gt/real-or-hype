# Huzhou Giraffe Manor (湖州长颈鹿庄园): episode 1 of the China spot series (Nov 2026)

Final: **E2** (40.5 s), voice John, clips-first, comment-keyword CTA. Rebuild: put the sources below in `work/giraffe/broll/`, copy `plan_E2.py` to `<workdir>/plan.py`, `script_E2.txt` to `script.txt`, then
`vo_take.py <workdir> PXo7njgt8slUVdtKa3La` (or reuse `words_E2.json` + the original vo) → `graphics.py` → `render_cut.py` → `finish.py <workdir> giraffe_E2`.
Earlier versions A–D/D2/E (Real or Hype-era scripts and voice) live in `../../real-or-hype-video/episodes/giraffe-manor/`.

## Fact sheet (confidence: ✔✔ = 2+ sources, ✔ = single source, ✱ = guest videos)
| fact | figure | source(s) | conf |
|---|---|---|---|
| Location | 吴兴区妙西镇妙山村丁家村888号, Huzhou; ~2 h from Shanghai; 17 km from Huzhou station | Trip.com, uk.trip.com attraction page | ✔✔ |
| Opened | 20 Jan 2020 | cn.chinadaily.com.cn/a/202010/29/WS5f9a6f7da3101e7ce972c1a2.html, Trip.com | ✔✔ |
| Breakfast with giraffes | buffet 07:00–10:00; window giraffes reported 08:30–09:30 (older) to ~10:30; people queue from 6:30 | Trip.com reviews, Sohu 2021, Ctrip | ✔✔ |
| **Animal wake-up call** (小动物叫早服务) | bookable; usually a squirrel/long-tailed monkey, sometimes a raccoon; "book the 9 am slot" | Douyin guest videos 7702806207996158385, 7687950126506569713, 7687988193149901042 (promo), 7685311414965524923. The web researcher found no written source | ✱ |
| **Giraffe calves born here** | 2: "小湖鹿" b. 1 Apr 2024 (1.85 m at birth per 潮新闻 clip 7360871784494730559; ~4 m at 2 yrs), second b. 11 Jun 2026 | news.cn/ci/20260408/…, news.cn/ci/20260611/…, 163.com/dy/article/K7FVRUP40514BTAB.html | ✔✔ |
| Giraffes' journey | first 4 came 2,200 km by road from Yunnan Wildlife Park (Kunming), 13 Jun 2019; southern African subspecies | huzhou.gov.cn 2019 (snippets) | ✔ (Kenya-origin claims elsewhere are wrong) |
| Giraffe count | 6–8; names 小九 (likes head pats), 小口水 (spits if you tease it with a carrot) | Ctrip & Sina travel notes 2022 | ✔ |
| Size / cost / developer | 1,200 mu (~80 ha) bamboo forest; ¥500–650 m; Mekong Group (湄公河集团), founder 俞锦方 after visiting Kenya | mekong.cn, CRI, China Daily | ✔✔ (cost varies) |
| Rooms / demand | 141 themed rooms; May Day 2025: 99.86% full at avg ¥2,300; normal occupancy 63%; 2.1 m visitors total | China Tourism Association case study (163.com) | ✔ |
| Prices used in video | deals ¥800–1,099 for 1 night + breakfast (Douyin posts 2026); "about $140" | Douyin 7640479702965053818, 7675005795369891566 | ✔ (deal price) |
| Kenya comparison | Giraffe Manor Nairobi from ~US$1,410 per person per night (2026) | safari.com, theresortscollection.com, chaloafrica.com | ✔✔ |
| Other animals | capybaras, raccoons, ring-tailed lemurs, red-crowned cranes (national first-class protected), squirrel monkeys | case study, vlogs | ✔✔ |
| Watch-outs | giraffes stay indoors below ~10 °C (winter/rain), indoor house smells; cleanliness/AC complaints; not China's only giraffe hotel (Oleborg, Quanzhou) | Sina 2026 guide, Trip.com reviews | ✔ |

## Footage (Douyin aweme ids; credit these creators in the caption)
B2 7653507861812628772 (4K60 vlog) · G 7651132730540887336 (4K60) · R 7653362319732886150 (4K30) · V1 6819931162912509199 · WAKE 7702806207996158385 (raccoon wake-up, vertical 1080p) · CALF 7665754019054754033 · BABY 7673338456038363624 (keeper with calf).
Rejected: 7627668117356308721 (camera-app UI, location unclear), 7360871784494730559 (news text burned mid-frame; used only for the 1.85 m fact), 7582116698300386610 (labelled 虚拟演绎 staged), 7691196846156325243 (looks AI).

## Trip-guide outline (for the "Comment GIRAFFE" DM)
湖州长颈鹿庄园 + address for taxis · Shanghai → Huzhou train, then ~20 min taxi/DiDi · book a breakfast package on Trip.com (weekends/holidays sell out; May Day 2025 was 99.86% full) · deals ~¥800–1,100, list ~¥2,000+ · breakfast 7:00, queue by 6:30 for a window table · ask for carrots at check-in · book the animal wake-up call at check-in (9 am slot) · cold or rainy days: giraffes may stay indoors · apps: Alipay, DiDi, Trip.com · "Want a full China itinerary? Reply PLAN". Date-stamp it.

## E2me: creator inserted with Seedance 2.0 (creator's request)
- One clip: `doubao-seedance-2-0-260128`, 720p, 9:16, 4 s, no audio, no watermark. References: the creator's verified portrait **asset** `asset://asset-20261114110202-8gttx` (a group id like `group-…` is rejected as "asset not found": reference an asset inside the group) and a frame of B2 @22.0 (breakfast table with a giraffe at the window, cropped to 9:16) as a data URL. Prompt (Chinese): 图片1中的男人坐在图片2的早餐桌旁… 把一根胡萝卜递给长颈鹿… 竖屏，手机实拍质感，自然柔和的日光，真实感，镜头轻微手持晃动。
- Result: 87,300 tokens ≈ ¥4.0 (480p 4 s ≈ 40,600 tokens ≈ ¥1.9). Realistic first try. Saved as `broll/ai_me_breakfast.mp4` (24 fps).
- Used 3 times, ~1 s each, on the matching words: "stops at your window" (0.20–1.65), "hold out a carrot" (2.95–4.0), "here's the part nobody expects" (1.55–2.55). `plan_E2me.py`.
