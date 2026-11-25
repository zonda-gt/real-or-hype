---
name: instagram-trial-reel
description: Post videos to Instagram as TRIAL reels (shown to non-followers first) for @steven_chinapal or another account whose token is set up. Use when the user says "post this as a trial reel", "post it on Instagram", "publish these reels", or similar. Trial reels only; never normal posts, stories or feed posts. Works with local video files (desktop app or cloud) and public video URLs.
---

# Post Instagram trial reels

This skill only posts **trial reels**: they go to non-followers first. Never post a normal reel, feed post or story with it.

**Captions never mention AI-generated clips or where footage came from** (Douyin, Xiaohongshu, other creators): the user's standing rule (Nov 2026). Don't add AI labels, "credit:" lines or source tags to captions, and don't suggest them.

**Graduation is always `MANUAL` (the user's standing rule).** The reel is shown to non-followers only, and the user shares it to their followers themselves from the Instagram app. Never use `SS_PERFORMANCE` (Instagram auto-sharing it to followers), and don't ask the user which to use: the script has no option for it.

Script: `scripts/post_trial_reel.py` in this skill's folder (Python 3 + `requests` + `git`; `ffprobe` optional for the video checks).

**A caption or video with a "Comment KEYWORD" call to action needs its auto-reply live first.** Check that `src/lib/inbox/code-rules.ts` in the ChinaPal repo (`zonda-gt/ChinaPal`) has that keyword, and that its guide link answers 200 on www.chinapal.co. If either is missing, set it up first, following the china-spot-video skill ("The DM side of the CTA"). Never send the user to the /comment page for it.

## How posting works (and why)

Instagram takes a reel **only from a public video URL** with our Instagram Login token. A direct file upload (`upload_type=resumable`) is rejected with `The parameter video_url is required`. That comes from Instagram's server, so it is the same from the cloud or a local computer. Every trial reel so far was posted from a public URL.

So for a **local file** the script hosts it in this repo first, which is public:
1. finds an identical file already tracked in the repo (by git blob hash) and reuses it, or copies it to `media/trial-reels/<name>.mp4`;
2. commits it and pushes the **current branch** (retries with backoff);
3. waits until `https://raw.githubusercontent.com/<owner>/<repo>/refs/heads/<branch>/<path>` answers 200 with the right size;
4. gives Instagram that URL as `video_url` with `media_type=REELS` and `trial_params={"graduation_strategy": "MANUAL"}`, polls `status_code` until `FINISHED`, then calls `media_publish`.

A **public URL** given by the user is used as it is, with no hosting.

Consequences to tell the user once: hosted videos stay downloadable from the repo; GitHub takes files up to ~95 MB (re-encode bigger ones); the repo must stay public.

`--direct-upload` keeps the resumable upload for a **Facebook Login** token with `instagram_content_publish`. It has not been tested yet: try it only when the user has such a token, and fall back to hosting if it fails.

## Steps

1. **Collect**: the video file(s) or public URL(s), the caption, the account (default `steven_chinapal`). Graduation is not a choice: it is always `MANUAL`.
   - No caption given: draft one (hook line, what to do, CTA keyword if any, 3–5 hashtags) and treat it as a proposal, not a decision. Check every claim in it (e.g. don't call a paid thing free).
   - Several videos for one A/B test: use the **same caption on all of them** unless told otherwise.
   - Save the caption to a text file and pass `--caption-file`, so emoji and line breaks survive.
   - Write the hosting commit message (with this session's attribution lines) to a file and pass `--commit-message-file`.
2. **Dry run** (checks token, account, files, caption, and shows where each file would be hosted; pushes and publishes nothing):
   ```bash
   python3 -I <skill>/scripts/post_trial_reel.py VIDEO1.mp4 VIDEO2.mp4 --account steven_chinapal --caption-file caption.txt --dry-run
   ```
   Fix any `PROBLEM` (re-encode with `ffmpeg -i in.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 -movflags +faststart out.mp4`). Show warnings (e.g. not 9:16) to the user.
3. **Confirm with the user before publishing**: show the account, the file names, the exact caption and "trial reel, graduation MANUAL (you share it to followers yourself)", and ask "Post these?". Publishing is public and can't be undone from here. If the user's request already named the files, the caption and trial settings explicitly ("post X and Y as trial reels with this caption: ..."), that is the confirmation.
4. **Publish**: the same command with `--yes` instead of `--dry-run` (plus `--commit-message-file`). It hosts local files, waits for processing, publishes, and prints each permalink.
   - It writes `<video>.ig.json` (container, media id, permalink, video URL) next to the repo copy and next to the local file, and skips anything already published, so re-running after a partial failure is safe. Never delete those logs to "retry" a published video.
   - Then **commit and push the new `.ig.json` logs** so later sessions know these videos are posted.
   - If one video fails, report Instagram's error; re-run once at most. Don't improvise other hosts (temporary file sites are blocked and not approved).
5. **Report**: the permalink of each trial reel, plus a reminder that trial reels appear in the Trial reels section of the professional dashboard, and the user shares the winner to followers from there (nothing is auto-shared).

## Token setup

The token is never printed or pasted in chat. The script reads, in order:
- `INSTAGRAM_ACCESS_TOKEN` (+ `INSTAGRAM_USER_ID`, optional): Instagram Login token, uses graph.instagram.com
- `INSTAGRAM_FB_TOKEN` + `INSTAGRAM_USER_ID`: Facebook Login token, uses graph.facebook.com (fallback)

Where they come from:
- **Claude Code on the web (cloud)**: the environment's variables or network secrets (environments "Video editing" or "AI Chat generation env" have them). Variables load when a session starts, so a session that was running before they were added won't see them: start a new chat.
- **Desktop app / local terminal**: put them in `~/.config/instagram-trial-reel/.env` (`chmod 600`), or export them in the shell profile, or pass `--env-file path`:
  ```
  INSTAGRAM_ACCESS_TOKEN=...
  INSTAGRAM_USER_ID=...
  ```
- If the user pastes a token in chat anyway: write it to a `umask 077` file in the scratchpad, pass `--env-file`, use it for this task only, and tell them to rotate it afterwards.
- The token needs `instagram_business_content_publish` (Instagram Login) or `instagram_content_publish` (Facebook Login), and the account must be a professional account eligible for trial reels. The current Facebook token lacks the publish permission.

If no token is found, tell the user where to put it; never ask them to paste it into the chat.

## Scheduling

The Instagram API has no "publish at" option. To post later, schedule a task (a scheduled task in this cloud session, or cron locally) that runs this script with `--yes` at the chosen time. The token must be in the environment's settings, not in chat.

## Using it in other projects

The skill lives in the `zonda-gt/real-or-hype` repo (`.claude/skills/instagram-trial-reel/`). Hosting needs a checkout of that repo, which the script finds from its own location; pass `--repo` if the script was copied elsewhere (e.g. `~/.claude/skills/`).

## Notes

- Formats: H.264 (or HEVC) + AAC ≤ 48 kHz, 23–60 fps, 3 s to 15 min, 9:16 (1080×1920) recommended; ≤ ~95 MB for GitHub hosting. Caption ≤ 2200 characters, ≤ 30 hashtags.
- Set `GRAPH_VERSION` to change the Graph API version (default v24.0).

## Posted so far

| Video | Permalink | Date |
| --- | --- | --- |
| ChinaPal v1_fast, s2_result, s3_offer | see `media/chinapal-trial/*.ig.json` (branch `claude/fervent-sagan-20nx4z`) | 2026-11-08 |
| Shenzhen free places v2 | https://www.instagram.com/reel/DffNyDVAo4w/ | 2026-11-08 |
| Alipay: 3 ways to pay (no music) | https://www.instagram.com/reel/DfjI8D4jvlo/ | 2026-11-10 |
| China Vlog remake (16:9) | https://www.instagram.com/reel/DfjXsxGHJnG/ | 2026-11-10 |
| Baixiangju 8D building recreation | https://www.instagram.com/reel/DfkWXqVH3D-/ | 2026-11-10 |
| China Vlog remake (9:16, new footage) | https://www.instagram.com/reel/DfkY2QznPtZ/ | 2026-11-10 |
| Giraffe Manor E2me (full tour) | https://www.instagram.com/reel/DfwVcgvFL6b/ | 2026-11-15 |
| Giraffe Manor F (Kenya vs China) | https://www.instagram.com/reel/DfwVlUTDETB/ | 2026-11-15 |
| Giraffe Manor G (4 things nobody tells you) | https://www.instagram.com/reel/DfwVrTRjjJK/ | 2026-11-15 |
| Helicopter A (the full flight), music: Momentum Rising (Audio API) | https://www.instagram.com/reel/DgA5IhQmX8O/ | 2026-11-21 |
| Helicopter B (New York vs Shanghai), same music | https://www.instagram.com/reel/DgA5T6hiV_a/ | 2026-11-21 |
| Helicopter C (4 things before you book), same music | https://www.instagram.com/reel/DgA5cIniIUA/ | 2026-11-21 |
| Bathhouse A, music: Lofi Street | https://www.instagram.com/reel/DgC5qUHFdI8/ | 2026-11-22 |
| Bathhouse B, same music | https://www.instagram.com/reel/DgC50dRCCzy/ | 2026-11-22 |
| Bathhouse C, same music | https://www.instagram.com/reel/DgC588lApUt/ | 2026-11-22 |
| Idol studio A, music: Seoul Vibes (Instrumental) | https://www.instagram.com/reel/DgGF_A_ks7o/ | 2026-11-23 |
| Idol studio B, same music | https://www.instagram.com/reel/DgGGHUclLUs/ | 2026-11-23 |
| Idol studio C, same music | https://www.instagram.com/reel/DgGGOaZjpki/ | 2026-11-23 |
| Palace banquet A, music: Colorful Clouds Chasing The Moon | https://www.instagram.com/reel/DgIq3sDjcqy/ | 2026-11-24 |
| Palace banquet B, same music | https://www.instagram.com/reel/DgIrDMYjOtC/ | 2026-11-24 |
| Palace banquet C, same music | https://www.instagram.com/reel/DgIrPOviWgJ/ | 2026-11-24 |
| Paramount A, music: Swing String Fling | https://www.instagram.com/reel/DgLPh5cFIIx/ | 2026-11-25 |
| Paramount B, same music | https://www.instagram.com/reel/DgLPom2gWNw/ | 2026-11-25 |
| Paramount C, same music | https://www.instagram.com/reel/DgLPxAGilpy/ | 2026-11-25 |

Facebook (normal reel on the ChinaPal Page 1320731184454757, Page token with `pages_manage_posts`): Giraffe Manor E2me, https://www.facebook.com/reel/2196029041327397/ (2026-11-15), log `media/trial-reels/giraffe_E2me_1080.mp4.fb.json`.
Recipe: `POST /{page}/video_reels upload_phase=start` → `POST rupload.facebook.com/video-upload/v24.0/{video_id}` with headers `Authorization: OAuth <token>` + `file_url: <public raw URL>` → `POST /{page}/video_reels upload_phase=finish video_state=PUBLISHED description=…` → poll `GET /{video_id}?fields=status,permalink_url`. Took ~1 min.

## Music from Instagram's licensed library (Audio API, from Nov 2026)
- `--audio-id <id> [--audio-volume 25] [--video-volume 100]` attaches a licensed track when the reel is created (`audio_configuration`), so the reel links to the sound's page. Use it with a **voice-only** export (china-spot-video: `NO_MUSIC=1 finish.py`); otherwise two music tracks play at once.
- It needs the **Facebook Login / Unified Login token** (`INSTAGRAM_FB_TOKEN` + `INSTAGRAM_USER_ID`, graph.facebook.com) with `instagram_content_publish`. The Instagram Login token can't attach music. A never-expiring system-user token comes from Meta app → Instagram API → "API setup with Unified login" → Create new configuration → Generate access tokens ("ChinaPal Concierge System User", Nov 2026).
- An env file only fills variables that aren't already set (setdefault). If the environment holds an older `INSTAGRAM_FB_TOKEN`, run `env -u INSTAGRAM_FB_TOKEN python3 scripts/post_trial_reel.py --env-file <file> ...`.
- Find tracks: `GET graph.facebook.com/v22.0/ig_audio?audio_type=music&user_id=<ig id>&search_query=<words>` (with no query it returns trending tracks); `GET /<audio_id>?user_id=...` gives a `download_url` preview (about 1.5 days). The catalogue is only music cleared for third-party apps, so there are no big-label hits (searching BLACKPINK returns unrelated tracks). Search by mood or genre instead.
- There's no preview of the final mix before publishing. 25/100 was chosen without hearing it: check the first post, then adjust.
- From 23 Nov 2026 the environment's own `INSTAGRAM_FB_TOKEN` is the Unified Login token (it can publish), so `env -u` and `--env-file` are no longer needed.
- First use: the 3 helicopter reels (21 Nov 2026), published fine; `GET /<media_id>?fields=media_audio_type` returns `MUSIC` when the track is attached.
- Never bake in songs downloaded from YouTube or elsewhere (copyright; Instagram mutes or limits matched audio).
