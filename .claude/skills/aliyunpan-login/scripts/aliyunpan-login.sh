#!/usr/bin/env bash
# Helper for logging in to Aliyun Drive (阿里云盘 / alipan) with the tickstep/aliyunpan CLI
# from a non-interactive shell (e.g. a Claude Code cloud session).
#
# Usage:
#   aliyunpan-login.sh check    # test network access to the hosts the login and downloads need
#   aliyunpan-login.sh build    # build the CLI from source (pinned tag) if not already built
#   aliyunpan-login.sh start    # start login in the background and print the authorization link
#   aliyunpan-login.sh finish   # after the user approved in the browser + scanned the QR code
#   aliyunpan-login.sh status   # show the logged-in account, if any
#   aliyunpan-login.sh logout   # log out and remove the saved tokens
set -euo pipefail

VERSION="${ALIYUNPAN_VERSION:-v0.4.0}"
BIN_DIR="${ALIYUNPAN_BIN_DIR:-/home/user/bin}"
BIN="$BIN_DIR/aliyunpan"
SRC_DIR="${ALIYUNPAN_SRC_DIR:-/home/user/tickstep/aliyunpan-$VERSION}"
# Tokens are stored here (aliyunpan_config.json). Keep it out of any git repository.
export ALIYUNPAN_CONFIG_DIR="${ALIYUNPAN_CONFIG_DIR:-$BIN_DIR}"
STATE_DIR="${ALIYUNPAN_STATE_DIR:-${TMPDIR:-/tmp}/aliyunpan-login}"
FIFO="$STATE_DIR/stdin.fifo"
LOG="$STATE_DIR/login.log"

die() { echo "error: $*" >&2; exit 1; }

cmd_check() {
  local ok=1 h code
  for h in https://www.alipan.com https://openapi.alipan.com https://auth.alipan.com \
           https://api.aliyundrive.com https://cn-beijing-data.aliyundrive.net https://api.tickstep.com; do
    code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 15 "$h" 2>/dev/null || true)
    if [[ "$code" == "000" || -z "$code" ]]; then
      echo "BLOCKED  $h"; ok=0
    else
      echo "ok ($code) $h"
    fi
  done
  [[ $ok == 1 ]] || { echo "Some hosts are unreachable: the environment's network policy must allow them."; return 1; }
}

cmd_build() {
  if [[ -x "$BIN" ]]; then
    echo "already built: $("$BIN" --version < /dev/null)"; return 0
  fi
  command -v go >/dev/null || die "Go is not installed"
  if [[ ! -d "$SRC_DIR/.git" ]]; then
    git clone --depth 1 --branch "$VERSION" https://github.com/tickstep/aliyunpan "$SRC_DIR"
  fi
  mkdir -p "$BIN_DIR"
  (cd "$SRC_DIR" && go build -o "$BIN" .)
  "$BIN" --version < /dev/null
}

login_pid() { pgrep -f "^$BIN login$" || true; }

cmd_start() {
  [[ -x "$BIN" ]] || die "not built yet; run: $0 build"
  [[ -z "$(login_pid)" ]] || die "a login is already waiting; run '$0 finish' or kill it first"
  mkdir -p "$STATE_DIR"; chmod 700 "$STATE_DIR"
  rm -f "$FIFO" "$LOG"; mkfifo "$FIFO"
  # The CLI waits for Enter after the browser login. Its stdin is a FIFO; a sleeping writer
  # keeps the FIFO open so the CLI does not see EOF, and `finish` writes the Enter into it.
  nohup sleep 900 > "$FIFO" 2>/dev/null &
  echo $! > "$STATE_DIR/holder.pid"
  nohup "$BIN" login < "$FIFO" > "$LOG" 2>&1 &
  local i
  for i in $(seq 1 30); do
    grep -q 'https://openapi.alipan.com/oauth/authorize' "$LOG" 2>/dev/null && break
    sleep 1
  done
  local url
  url=$(grep -o 'https://openapi.alipan.com/oauth/authorize[^[:space:]]*' "$LOG" | head -1 || true)
  [[ -n "$url" ]] || { cat "$LOG"; die "no login link appeared"; }
  echo "LOGIN_URL=$url"
  echo "The link is valid for 5 minutes. The user must (1) approve access, then (2) scan the QR code with the Aliyun Drive app."
}

cmd_finish() {
  [[ -p "$FIFO" ]] || die "no login in progress; run: $0 start"
  local pid; pid=$(login_pid)
  [[ -n "$pid" ]] || { cat "$LOG"; die "the login process is no longer running"; }
  echo > "$FIFO"
  local i
  for i in $(seq 1 30); do
    [[ -z "$(login_pid)" ]] && break
    sleep 1
  done
  tail -n 2 "$LOG"
  [[ -f "$STATE_DIR/holder.pid" ]] && kill "$(cat "$STATE_DIR/holder.pid")" 2>/dev/null || true
  rm -f "$FIFO" "$STATE_DIR/holder.pid"
  cmd_status
}

cmd_status() {
  [[ -x "$BIN" ]] || die "not built yet; run: $0 build"
  local out; out=$("$BIN" who < /dev/null 2>&1)
  echo "$out"
  ! grep -q '未登录' <<<"$out"
}

cmd_logout() {
  [[ -x "$BIN" ]] || die "not built yet"
  "$BIN" logout -y < /dev/null
}

case "${1:-}" in
  check|build|start|finish|status|logout) "cmd_$1" ;;
  *) sed -n '2,13p' "$0"; exit 2 ;;
esac
