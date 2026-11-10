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

## 9:16 version (`china_vlog_9x16_1080x1920.mp4`)

Same cut times and sound; all-new vertical footage. Title: "CHINA" and "VLOG" split around the Chongqing tower (`title_seg_v.py`).

| # | Time (s) | Place | Douyin video | Creator | Source in (s) |
|---|---|---|---|---|---|
| 0 | 0.00–3.00 | Chongqing skyline at night (title) | https://www.douyin.com/video/7684665809965530098 | 又见默默 | 6.9 @0.75x |
| 1 | 3.00–3.47 | Monks under ginkgo, temple | https://www.douyin.com/video/7040790958220250409 | 骑水鸟的维生素 | 1.0 |
| 2 | 3.47–3.97 | Wok fire | https://www.douyin.com/video/7478536330541059385 | 郴州市北湖区同德小家常餐饮店 | 0.9 |
| 3 | 3.97–5.43 | Xijiang Miao village lights | https://www.douyin.com/video/7615586992571146387 | 是肉肉吖～ | 1.0 |
| 4 | 5.43–6.37 | Yulong River rafts, Yangshuo | https://www.douyin.com/video/7683476706813020785 | 木 子 | 0.5 |
| 5 | 6.37–7.80 | Slender West Lake, Yangzhou | https://www.douyin.com/video/7696099196599813753 | 玩转扬州 | 0.3 |
| 6 | 7.80–9.27 | Beef noodles | https://www.douyin.com/video/7292324560702115108 | 十一 | 0.5 |
| 7 | 9.27–10.23 | Potala Palace at dusk | https://www.douyin.com/video/7060985156043066655 | 過往雲煙 | 1.0 |
| 8 | 10.23–12.17 | Uncle dancing in the park | https://www.douyin.com/video/7082548581072178432 | 午夜猎人 | 1.0 |
| 9 | 12.17–14.07 | Erhai with reeds, Dali | https://www.douyin.com/video/7686344950119866234 | 蜗牛🐌 | 2.0 |
| 10 | 14.07–16.50 | Huangshan sea of clouds | https://www.douyin.com/video/7609999068706119333 | 山水又一程 | 5.0 |
| 11 | 16.50–17.43 | Xi'an city wall light trails | https://www.douyin.com/video/7682298339823874943 | 长安拍客 | 2.0 |
| 12 | 17.43–18.93 | Zigong phoenix lantern | https://www.douyin.com/video/7596962176650418875 | 渝以北 | 4.7 |
| 13 | 18.93–20.33 | Dunhuang camel caravan | https://www.douyin.com/video/7680325483075486330 | 青甘环线好先生 | 3.0 |
| 14 | 20.33–21.97 | Beijing street, cyclist | https://www.douyin.com/video/7512402819463531812 | 好摄之徒 | 1.0 |

### Place labels (`china_vlog_9x16_labels_1080x1920.mp4`)

`labels_v.py` draws each place name in white Anton (150 px, shrunk to fit 990 px) with a soft drop shadow, plus a yellow pill (Montserrat ExtraBold 54 px, #F7D02E) with the city or region. `apply_labels_v.py` burns them in for exactly their shot. Shots without a known place name (title, temple, wok, noodles, Beijing street) have no label.

## Version 3, 9:16 (`china_vlog_v3_9x16_1080x1920.mp4`)

Same cuts and sound; all-new vertical footage; single-line title behind the Tianjin tower; place labels built in.
Build: `PLAN=plan_v3 RAWDIR=v3raw SEGDIR=segs_v3 LABELDIR=labels_v3 OUTNAME=china_vlog_v3_9x16_nolabels` then render_v.py, title_seg_v.py, labels_v.py, assemble_v.sh, and `SRC=china_vlog_v3_9x16_nolabels.mp4 OUT=china_vlog_v3_9x16_1080x1920.mp4 apply_labels_v.py`.

| # | Time (s) | Place | Label | Douyin video | Creator | Source in (s) |
|---|---|---|---|---|---|---|
| 0 | 0.00–3.00 | Tianjin Haihe skyline (title) | — | https://www.douyin.com/video/7653502221975553700 | 笑傲浆糊 | 4.5 |
| 1 | 3.00–3.47 | Lingyin Temple gate | LINGYIN TEMPLE / HANGZHOU | https://www.douyin.com/video/7157901764602219780 | 江南忆 | 0.5 |
| 2 | 3.47–3.97 | Chongqing hotpot | — | https://www.douyin.com/video/7665280277241083290 | 里里不爱吃肉 | 9.3 |
| 3 | 3.97–5.43 | Zhouzhuang at night | ZHOUZHUANG / JIANGSU | https://www.douyin.com/video/7677181612211669480 | 苏州•苏灵🐱 | 5.0 |
| 4 | 5.43–6.37 | Wuzhen canal boats | WUZHEN / ZHEJIANG | https://www.douyin.com/video/7681615917277183296 | 忆江南6 | 0.5 |
| 5 | 6.37–7.80 | Hongcun reflections | HONGCUN / ANHUI | https://www.douyin.com/video/7689364074672443983 | 水云间（靓琪儿） | 0.3 |
| 6 | 7.80–9.27 | Rice rolls (cheung fun) | — | https://www.douyin.com/video/7674800814074880433 | 零糖不加冰 | 0.5 |
| 7 | 9.27–10.23 | Leshan Giant Buddha | LESHAN GIANT BUDDHA / SICHUAN | https://www.douyin.com/video/7677215030135622769 | 淡如初见 | 3.6 |
| 8 | 10.23–12.17 | Tai chi in the park | — | https://www.douyin.com/video/7700945103372760802 | 小熊饼干☯️ | 3.0 |
| 9 | 12.17–14.07 | Lushan cloud waterfall | LUSHAN / JIANGXI | https://www.douyin.com/video/7651124068234408945 | 悦悦控 | 1.0 |
| 10 | 14.07–16.50 | Hanging Temple | HANGING TEMPLE / DATONG | https://www.douyin.com/video/7498126295269051660 | 今生有你 | 2.0 |
| 11 | 16.50–17.43 | Yingwuzhou Bridge, Wuhan | YINGWUZHOU BRIDGE / WUHAN | https://www.douyin.com/video/7673808798214458283 | 悠悠的视界 | 0.5 |
| 12 | 17.43–18.93 | Datang Everbright City | DATANG EVERBRIGHT CITY / XI'AN | https://www.douyin.com/video/7598481496160946597 | 山水又一程 | 0.1 |
| 13 | 18.93–20.33 | Chaka salt lake | CHAKA SALT LAKE / QINGHAI | https://www.douyin.com/video/7662185926873634801 | 浪迹山河、 | 1.5 |
| 14 | 20.33–21.97 | Yulin Road, Chengdu | YULIN ROAD / CHENGDU | https://www.douyin.com/video/7673533308890894065 | Ww. | 0.2 |
