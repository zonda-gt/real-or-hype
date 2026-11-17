#!/bin/bash
# Download ORIGINAL-quality Douyin uploads via TikHub (often 4K60) into <workdir>/broll/<id>.mp4, size-checked.
# usage: dl_douyin.sh <workdir> <aweme_id> [...]      Safe to run several copies in parallel on disjoint id lists.
# ~$0.005 per id. Files can be 300-600 MB; ~1.5 MB/s, so run it in the background.
W=$1; shift; mkdir -p "$W/broll"; cd "$W"
for id in "$@"; do
  [ -s broll/$id.mp4 ] && continue; [ -e broll/$id.part ] && continue
  j=$(curl -sS -A 'Mozilla/5.0 Chrome/124' -H "Authorization: Bearer $TIKHUB_API_KEY" "https://api.tikhub.io/api/v1/douyin/app/v3/fetch_video_high_quality_play_url?aweme_id=$id")
  url=$(echo "$j" | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['original_video_url'])" 2>/dev/null)
  sz=$(echo "$j" | python3 -c "import json,sys;print(json.load(sys.stdin)['data'].get('file_size',0))" 2>/dev/null)
  [ -z "$url" ] && { echo "NO URL $id: $(echo $j | head -c 200)"; continue; }
  for t in 1 2 3; do curl -sSL -A 'Mozilla/5.0' -o broll/$id.part "$url" && break; sleep 3; done
  got=$(stat -c%s broll/$id.part); echo "$id expected=$sz got=$got"
  [ "$got" = "$sz" ] && mv broll/$id.part broll/$id.mp4 || echo "SIZE MISMATCH $id"
done
