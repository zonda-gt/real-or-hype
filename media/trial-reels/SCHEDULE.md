# Trial-reel schedule (set 21 Nov 2026): one Shanghai place a day, 3 reels each, at about 19:05 UTC

| Date (UTC) | Place | Files (this folder) | Caption | Music (Instagram audio_id) | Comment keyword |
|---|---|---|---|---|---|
| 2026-11-21 | helicopter | helicopter_{A,B,C}_voice_1080.mp4 | (posted) | 2569981020089689 Momentum Rising | HELICOPTER |
| 2026-11-22 (posted 13:2x UTC) | bathhouse | bathhouse_{A,B,C}_voice_1080.mp4 | captions/bathhouse.txt (posted) | 544713431841568 Lofi Street | BATHHOUSE |
| 2026-11-23 | idol-studio | idol-studio_{A,B,C}_voice_1080.mp4 | captions/idol-studio.txt (posted) | 1105478964958211 Seoul Vibes (Instrumental) | IDOL |
| 2026-11-24 | palace-banquet | palace-banquet_{A,B,C}_voice_1080.mp4 | captions/palace-banquet.txt | 1516724508945302 Colorful Clouds Chasing The Moon | BANQUET |
| 2026-11-25 | paramount | paramount_{A,B,C}_voice_1080.mp4 | captions/paramount.txt | 977536832781184 Swing String Fling | PARAMOUNT |

All comment replies are live in ChinaPal `src/lib/inbox/code-rules.ts` (PRs #275, #277).

Post command (from the repo root; the videos are already tracked here, so nothing new is uploaded):
```bash
P=<place>; ID=<audio_id>
env -u INSTAGRAM_FB_TOKEN python3 -I .claude/skills/instagram-trial-reel/scripts/post_trial_reel.py \
  media/trial-reels/${P}_A_voice_1080.mp4 media/trial-reels/${P}_B_voice_1080.mp4 media/trial-reels/${P}_C_voice_1080.mp4 \
  --account steven_chinapal --caption-file media/trial-reels/captions/$P.txt --audio-id $ID \
  --env-file <file with INSTAGRAM_FB_TOKEN=<unified-login token> and INSTAGRAM_USER_ID=17841434818373119> \
  --commit-message-file <msg> --yes
```
If the environment's own `INSTAGRAM_FB_TOKEN` already has `instagram_content_publish`, drop `env -u` and `--env-file`.
Then commit the new `.ig.json` logs, and check `GET /<media_id>?fields=media_audio_type` = MUSIC.
