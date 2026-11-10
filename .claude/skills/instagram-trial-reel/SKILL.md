---
name: instagram-trial-reel
description: Post videos to Instagram as TRIAL reels (shown to non-followers first) for @steven_chinapal or another account whose token is set up. Use when the user says "post this as a trial reel", "post it on Instagram", "publish these reels", or similar. Trial reels only; never normal posts, stories or feed posts. Works with local video files (desktop app or cloud) and public video URLs.
---

# Post Instagram trial reels

This skill only posts **trial reels**: they go to non-followers first. Never post a normal reel, feed post or story with it.

**Graduation is always `MANUAL` (the user's standing rule).** The reel is shown to non-followers only, and the user shares it to their followers themselves from the Instagram app. Never use `SS_PERFORMANCE` (Instagram auto-sharing it to followers), and don't ask the user which to use: the script has no option for it.

Script: `scripts/post_trial_reel.py` in this skill's folder (Python 3 + `requests` + `git`; `ffprobe` optional for the video checks).

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
