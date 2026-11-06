---
name: aliyunpan-login
description: Log in to Aliyun Drive (阿里云盘 / alipan.com / aliyundrive) from this environment with the tickstep/aliyunpan CLI, then list and download files of any size. Use when the user wants files from their Aliyun Drive, alipan, or 阿里云盘 in the session, or asks to log in to it.
---

# Aliyun Drive login (aliyunpan CLI)

The helper script `scripts/aliyunpan-login.sh` (next to this file) builds the CLI and runs
its two-step browser login from a non-interactive shell. Run every step through it.

```bash
S=.claude/skills/aliyunpan-login/scripts/aliyunpan-login.sh   # path relative to the repository root
```

Use this to get **original files of any size**, including files over 100 MB, which the
web API (`get_download_url`) refuses to link. It works on the logged-in user's own drive.
For someone's share link, ask the drive owner to tap "保存到我的网盘" (save to my drive) in
the Aliyun Drive app first; the CLI cannot save another account's share.

## Steps

1. **Check network.** Run `bash $S check`. Any `BLOCKED` host means the environment's
   network policy denies it. Stop and ask the user to allow these domains in the
   environment's Network access settings: `alipan.com`, `aliyundrive.com`,
   `aliyundrive.net`, `api.tickstep.com`. Do not try to work around the block.

2. **Build.** Run `bash $S build`. This shallow-clones tag `v0.4.0` of
   `github.com/tickstep/aliyunpan` and builds it with Go to `/home/user/bin/aliyunpan`.
   It does nothing if the binary already exists. Run `bash $S status` too: if an account is
   already logged in, skip to step 5.

3. **Tell the user how the login works before starting it.** The CLI's OAuth redirect
   goes to its author's server, `api.tickstep.com`, which hands the tokens back to the CLI.
   Those tokens can read, write, and share the whole drive. Never ask for the user's
   password or a refresh token in chat; the QR login does not need them.

4. **Log in.**
   - Run `bash $S start`. It prints `LOGIN_URL=...`. Give the user that link in full.
     It is valid for 5 minutes, and the user must do two things: approve access in the
     browser, then scan the QR code with the Aliyun Drive phone app.
   - Wait for the user to say they are done. Then run `bash $S finish`. Success prints
     `阿里云盘登录成功` and the account (`当前帐号UID ... 昵称 ...`).
   - If the link expired or `finish` fails, run `start` again and give the user the new link.

5. **Use the drive.** Always pass `< /dev/null` so prompts never hang the shell. Paths
   contain spaces and Chinese names, so always quote them.
   - List files: `/home/user/bin/aliyunpan ls "/folder" < /dev/null`
   - Download: `/home/user/bin/aliyunpan download --saveto /home/user/videos "/folder/file.mp4" < /dev/null`
     Add `--np` to hide the progress bar in logs. A whole folder path downloads recursively.
     The CLI checks each file after download (`检验文件有效性成功` = file check passed).
   - The account has two drives: 备份盘 (backup) and 资源库 (resource library).
     `aliyunpan who` shows which drive is in use; switch with `aliyunpan drive <DRIVE ID>`
     (run `aliyunpan drive < /dev/null` to list the IDs).
   - `who` also shows `三方权益包` (third-party app pack, paid). Downloads work without it
     (`未开通` = not active); the pack adds things like WebDAV and faster download quota.
   - Before downloading a lot, compare total size with free disk space (`df -h /home/user`).
     Download with `-p 3 --sp 3` (3 files at once, 3 slices each): one file at a time ran at
     ~2.5 MB/s, while `-p 3 --sp 3` averaged ~30 MB/s (19.6 GB in 12 minutes) without the paid
     三方权益包, which therefore isn't needed for downloads. The CLI warns that this is above Alipan's
     recommended concurrency; lower it if downloads start failing. Run long downloads with
     `run_in_background`, and if a download is stopped, delete the half-written file (and its
     `.aliyunpan-downloading` marker) before restarting, because the CLI skips files that already exist.

6. **Log out when done** if the user wants: `bash $S logout`. The user can also remove the
   app's access in their Aliyun Drive account settings.

## Notes

- Tokens are saved in `/home/user/bin/aliyunpan_config.json` (set by
  `ALIYUNPAN_CONFIG_DIR`). Never commit or print that file.
- The container is temporary. The binary, the login, and downloaded files are gone when the
  session ends, so rerun `build` and the login in a new session.
- GitHub release binaries are not reachable from this environment; that is why the
  script builds from source.
