#!/usr/bin/env bash
# usage: get_song.sh WORKDIR  -> WORKDIR/song.mp4 (the reference reel; only its audio is used)
set -e; D="$1"; mkdir -p "$D"
[ -s "$D/song.mp4" ] && exit 0
pip install -q -U yt-dlp >/dev/null 2>&1 || true
yt-dlp -q -o "$D/song.%(ext)s" "https://www.facebook.com/share/r/1DLSqdyBWE/"
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$D/song.mp4")
python3 -c "import sys; d=float('$d'); sys.exit(0 if abs(d-31.836)<0.2 else 'song length %.2f, expected 31.84' % d)"
echo "song OK ($d s)"
