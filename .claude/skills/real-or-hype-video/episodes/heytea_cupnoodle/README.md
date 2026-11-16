# Heytea × Cup Noodle "Fresh Coconut Ramen" (生打椰拉面), Instagram reel, Nov 2026

Not a Real or Hype episode: a straight product-review reel modelled on @jennaisblonde's Heytea × Cup Noodle reel
(hook with the cup + big title → storefront/menu → ordering → unboxing → tasting → verdict → follow CTA, ~31 s).

- Footage: 18 clips, OneDrive folder from the creator (20261115_HHMMSS.mp4, HLG → tone-mapped to BT.709).
- Narration: ElevenLabs library voice **Dev, English-speaking Korean male streamer** (`5J8HNhWkTAhN2YWsd9Ta`),
  `eleven_multilingual_v2`, stability 0.35 / similarity 0.8 / style 0.45 / speaker boost, trimmed, `atempo=1.1`.
  Other lively Korean-accent voices auditioned: John `PXo7njgt8slUVdtKa3La`, Jeongki `fwH9jZjJVWYg6qwyWr01`,
  Minho `LoXeQQJXcdhPF6vk2Phy`, The student `Ih5c9jfzl0g5jmK1Z2Nq`, Minzy (female) `y3J9lm4KG5NLFtSFEB5A`.
  Shared-library voices work directly by id with this key. Write "Hey Tea" in TTS text (subtitles say "Heytea").
- Facts used: launched 13 Nov 2026, coconut base + mango "noodles" + corn, ¥22, some shops sold out in minutes (21jingji, Sohu).

Pipeline (workdir has raw/, vo/L*.wav, title.png):
1. `python3 title.py <wd>/title.png`
2. `python3 render.py <wd>`  shots from `segs.py`, gap check against his measured speech spans
3. `python3 finish.py <wd>`  subtitles, title card, narration, whoosh/pop, loudnorm -15 LUFS, limiter
