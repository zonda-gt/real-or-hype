#!/bin/bash
# download original-quality Douyin videos via TikHub; verify size
cd "$(dirname "$0")"
for id in "$@"; do
  [ -s broll/$id.mp4 ] && continue
  j=$(curl -sS -A 'Mozilla/5.0 Chrome/124' -H "Authorization: Bearer $TIKHUB_API_KEY" "https://api.tikhub.io/api/v1/douyin/app/v3/fetch_video_high_quality_play_url?aweme_id=$id")
  url=$(echo "$j" | python3 -c "import json,sys;d=json.load(sys.stdin)['data'];print(d['original_video_url'])")
  sz=$(echo "$j" | python3 -c "import json,sys;d=json.load(sys.stdin)['data'];print(d.get('file_size',0))")
  for t in 1 2 3; do curl -sSL -A 'Mozilla/5.0' -o broll/$id.part "$url" && break; sleep 3; done
  got=$(stat -c%s broll/$id.part)
  echo "$id expected=$sz got=$got"
  [ "$got" = "$sz" ] && mv broll/$id.part broll/$id.mp4 || echo "SIZE MISMATCH $id"
done
