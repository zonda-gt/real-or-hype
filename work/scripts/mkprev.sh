# small review previews (autorotated, 360 px wide, mono audio) + stats line per clip
cd "$1"; for f in orig/*.MOV orig/*.mp4 other/*.mp4; do
  [ -f "$f" ] || continue; n=$(basename "${f%.*}"); [ -f "prev/$n.mp4" ] && continue
  ffmpeg -loglevel error -y -i "$f" -vf "scale=360:-2,fps=15" -c:v libx264 -preset ultrafast -crf 28 -c:a aac -b:a 64k -ac 1 "prev/$n.mp4" || continue
  info=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,color_transfer:stream_side_data=rotation:format=duration -of csv=p=0:nk=1 "$f" | tr '\n' ' ')
  vol=$(ffmpeg -hide_banner -i "$f" -af volumedetect -vn -f null - 2>&1 | grep -oE "(mean|max)_volume: [-0-9.]+" | awk '{print $2}' | tr '\n' ' ')
  echo "$n | $info | vol(mean max) $vol" >> prev/stats.txt
done
