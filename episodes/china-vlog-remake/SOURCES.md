# China Vlog remake: shot list and Douyin sources

Reference: https://www.tiktok.com/@tutiimaccio/video/7631383112307461396 (structure, cut timing and original sound).

Footage belongs to the Douyin creators below. Credit them, or ask permission, before posting.

| # | Time (s) | Place | Douyin video | Creator | Source in (s) |
|---|---|---|---|---|---|
| 0 | 0.00–3.00 | Guangzhou Canton Tower (title) | https://www.douyin.com/video/7536157470457695531 | 奕梦星海 | 5.0 |
| 1 | 3.00–3.47 | Temple gate | https://www.douyin.com/video/7665079382855191854 | 繆思 | 7.18 |
| 2 | 3.47–3.97 | Teppanyaki flame | https://www.douyin.com/video/7243240214632680743 | 兴美城市广场 | 8.3 |
| 3 | 3.97–5.43 | Xitang lantern boats | https://www.douyin.com/video/7244825772140105016 | 西塘古镇景区 | 14.0 |
| 4 | 5.43–6.37 | Guilin Li River raft | https://www.douyin.com/video/7572870227614518735 | ^Xjoker | 3.0 |
| 5 | 6.37–7.80 | Lizhuang ancient town sunset | https://www.douyin.com/video/7695357803590686646 | Z | 3.0 |
| 6 | 7.80–9.27 | Steaming pot kitchen | https://www.douyin.com/video/7449403524397485339 | wakaka1pin | 0.0 |
| 7 | 9.27–10.23 | Potala Palace, Lhasa | https://www.douyin.com/video/7701334294639540297 | KangbaLadho | 0.5 |
| 8 | 10.23–12.17 | Park circle dance | https://www.douyin.com/video/7703784750254877878 | 是胖胖呀 | 8.0 |
| 9 | 12.17–14.07 | Jiuzhaigou autumn | https://www.douyin.com/video/7685403242537289802 | 李先生 | 0.0 |
| 10 | 14.07–16.50 | Zhangjiajie in mist | https://www.douyin.com/video/7690080863061851310 | mojito228 | 10.0 |
| 11 | 16.50–17.43 | Chongqing skyline | https://www.douyin.com/video/7661513526356788462 | 🐟刘钰儿Yuer⁹²¹² | 5.0 |
| 12 | 17.43–18.93 | Fish lanterns + fireworks | https://www.douyin.com/video/7622310743648183110 | 千千层 | 2.0 |
| 13 | 18.93–20.33 | Yangshuo golden hour | https://www.douyin.com/video/7694273741970340721 | 颜途小院(咖啡)☕ | 3.4 |
| 14 | 20.33–21.97 | Street life | https://www.douyin.com/video/7290578707402476837 | 青墨-张运良 | 0.2 |

## How it was made

- Reference cuts are all on the beat (~123 BPM); the remake reuses the exact same cut times and the reference's own audio track.
- Clips found with `dysearch.py` (TikHub Douyin video search, landscape `横屏` / `空镜` queries) and downloaded at original quality with `dydl.py`.
- `render.py`: each shot trimmed to an exact frame count, HLG clips tone-mapped to BT.709, scaled to 1920x1080@30 and graded (lifted blacks, rolled-off highlights, warm highlights / teal shadows, saturation 0.92, soft vignette).
- `title_seg.py` + `title.py` + `skymask.py`: "CHINA VLOG" (Anton, squashed tall, #F2DB11) drawn behind the skyline using a SegFormer-B4 ADE20K sky mask (ONNX), guided-filter refined and smoothed over 3 frames; pops in at 0.567 s like the reference.
- `assemble.sh`: concat + original sound. The reference's "filmed and edited by @…" credit and studio logo were left out on purpose.
