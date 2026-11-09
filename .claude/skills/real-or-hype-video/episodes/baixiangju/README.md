# Baixiangju (白象居, Chongqing): straight recreation (Nov 2026)

This episode is a straight recreation of 于锡明's Douyin vlog 7633751862790313829 ("重庆这小区建的也太梦幻了", 4 min), cut to 61 s.
It is not in the Real or Hype? format: there's no sting and no verdict, and his own on-camera lines tell the story (10F → 15F → 14F → 12F → "ground floor again").

- Footage: Alipan 资源库 `/chongqing、/重庆系列/白象居（惊讶）` (19 files, 3.4 GB). Douyin drone B-roll: 7416732680286489856 (F11, needs `play_addr_h264`; the default stream is ByteVC2, which ffmpeg can't decode).
- Work dir layout: `src/` (the Alipan folder), `broll/<aweme_id>_hq.mp4`, `ov/`, and `words.json` (faster-whisper medium word stamps).
- `python3 bxj_check.py` runs the noise-relative energy check on every in/out point of his voice (must print ALL OK).
- `python3 bxj_render.py` writes `out/bxj_1080.mp4` (HLG tone-map, his lines at 1.3× with loudnorm -16, elevator floor badge 2 frames before each floor word, hook title, end card, word subtitles).
- `python3 bxj_sfx.py sfx/ding_el.wav sfx/whoosh_tonal.wav 0.30 0.35` writes `out/bxj_final_1080.mp4`.
  The ding is ElevenLabs "Hotel lift arrival chime" (earshot: strong as a bell ding, top match for a lift chime). Its **peak sits 0.30 s before the floor word at 0.35 volume**: on the word itself it masked "14th floor" (Whisper heard "424").
- `vruns.py <file> <a> <b>` prints voiced runs, to pick cut points that land in silence.
