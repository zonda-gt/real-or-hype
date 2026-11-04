AT=$(tr -d '\n' < .alipan_at); ST=$(cat share_token.txt)
for n in "$@"; do
rm -f "orig/$n.MOV"
fid=$(python3 -c "import json;print([f['file_id'] for f in json.load(open('all_files.json')) if f['name'].startswith('$n')][0])")
u=$(curl -sS -m 30 -X POST https://api.alipan.com/v2/file/get_share_link_video_preview_play_info -H "Content-Type: application/json" -H "Referer: https://www.alipan.com/" -H "Authorization: Bearer $AT" -H "x-share-token: $ST" -d "{\"share_id\":\"e3FxGyLuAo8\",\"file_id\":\"$fid\",\"category\":\"live_transcoding\",\"template_id\":\"\",\"get_preview_url\":true}" | python3 -c "
import json,sys;d=json.load(sys.stdin);t=d['video_preview_play_info']['live_transcoding_task_list'];print(sorted(t,key=lambda t:-t['template_height'])[0]['preview_url'])")
ffmpeg -loglevel error -y -headers $'Referer: https://www.alipan.com/\r\n' -i "$u" -c copy -bsf:a aac_adtstoasc orig/$n.mp4 && echo "$n ok $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 orig/$n.mp4)"
done
