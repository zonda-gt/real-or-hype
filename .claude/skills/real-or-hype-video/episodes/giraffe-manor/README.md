# Giraffe Manor (湖州长颈鹿庄园, Huzhou): B-roll-only explainer (Nov 2026)

Not the Real or Hype? format: the creator hasn't visited, so there's no reaction, sting or verdict. Douyin B-roll + his cloned voice.
Three angles (same music): **A** "breakfast with giraffes" (29.3 s), **B** Kenya $1,400+/night vs China ¥1,000 (~$140) (26.3 s), **C** how-to (22.5 s).

- Place: Giraffe Manor Hotel, 妙西镇, 吴兴区, Huzhou (not Changxing). Opened Jan 2020. Breakfast 07:00–10:00; reviewers say be there ~6:30 for a window table. ~2 h from Shanghai; 17 km from Huzhou station. Trip.com 9.3/10 (7.5k reviews). Deal prices on Douyin: ¥800–1,099 for 1 night + breakfast; list price ~¥2,000. Kenya's Giraffe Manor: from ~US$1,410 per person per night (2026).
- Footage: TikHub `douyin/search/fetch_video_search_v2` (needs a browser User-Agent, else Cloudflare 1010), then `douyin/app/v3/fetch_video_high_quality_play_url` for the original upload (4K for the best vlogs; size-checked in `dl.sh`). Main sources: 7653507861812628772 (4K60), 7651132730540887336 (4K60), 7653362319732886150 (4K30), 6819931162912509199 (vertical). Their burned-in Chinese subtitles are cropped off (`cut` in `plan.py`). Credit/tag the original creators in the post caption.
- `gen_vo.py`: creator clone, Whisper-checked. "a thousand yuan" was often heard as "a thousand when"; B6 says "RMB". "Huzhou" mispronounced in C3, so that line avoids it.
- `render.py <V>` (shots → segments, gap check), `finish.py <V>` (cards, word subs, ElevenLabs Music marimba track ducked under VO, whoosh/pop, -15 LUFS, TP ≤ -1). Lines with a big on-screen card have no subtitles.

## Update: variant D and new captions
- **D** (30.8 s): cold open on a real shocked reaction at the venue (vlogger 7651132730540887336 at 51.40 s, hands up, mouth open), then all of A. **D2** (31.3 s): same, but opens on 7582116698300386610 (a giraffe licks a woman's face). It's wilder, but Douyin labels it 虚拟演绎 仅供娱乐 (staged, for entertainment only) and it's at a zoo, not Giraffe Manor. The label is left visible. 7691196846156325243 (kid's hair licked up) looks AI-made too. Many viral "reaction" clips are staged or AI, so check for the label before using one.
- Reaction sound: ElevenLabs "crowd gasping then laughing" (`sfx/react1.mp3`, earshot: strong). Music starts on the cut out of the reaction, with a whoosh.
- Captions (creator's request): **centred on screen**, lighter and cleaner. Poppins SemiBold 66 px (fontsource woff2 → ttf in `fonts/`), white, 2.2 px dark outline at 70% opacity, soft shadow, current word in soft yellow `#FFE27A`.
