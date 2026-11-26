# ep3 copy: extra -8 dB music dip under segment H (20.217-24.617 s), where the fast line was masked
# mix_music.py <video_without_music.mp4> <bed.wav> <out.mp4> [dB_under_voice=6]
# Music under a talking head the way the reference does it: bed levelled to ~7 dB under the voice (-22 vs -15 LUFS),
# sidechain-ducked ~3 dB while he speaks so the beat lifts in the gaps, then the mix to -14 LUFS / TP -1.5 (two-pass),
# video stream copied. Prints the bed's level under speech and in the gaps.
import sys, json, subprocess, re
vid, bed, out = sys.argv[1:4]; under = float(sys.argv[4]) if len(sys.argv) > 4 else 6.0   # dB under the voice before ducking
def lufs(f):
    r = subprocess.run(['ffmpeg', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid], capture_output=True, text=True).stdout)
voice = lufs(vid); g = (voice - under) - lufs(bed)
fc = (f"[1:a]equalizer=f=2500:t=q:w=0.9:g=-4,volume={g:.2f}dB,volume='1-0.6*clip(min((t-20.217)/0.3\,(24.617-t)/0.3)\,0\,1)':eval=frame,atrim=0:{dur:.3f},apad=whole_dur={dur:.3f},afade=t=out:st={dur-0.8:.3f}:d=0.8[m];"
      f"[0:a]asplit=2[v][sc];"
      f"[m][sc]sidechaincompress=threshold=0.1:ratio=2:attack=30:release=350:makeup=1[md];"
      f"[v][md]amix=inputs=2:duration=first:normalize=0[mix]")
tmp = out.replace('.mp4', '_pre.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', bed, '-filter_complex', fc, '-map', '[mix]', '-ar', '48000', tmp], check=True)
j = subprocess.run(['ffmpeg', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(j[j.rindex('{'):j.rindex('}') + 1])
ln = f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', tmp, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', ln + ',aresample=48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
r = subprocess.run(['ffmpeg', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print(out.split('/')[-1], 'bed gain %+.1f dB' % g, '| final', re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1], 'LUFS, peak', re.findall(r'Peak:\s+(-?[\d.]+)', r)[-1], 'dBFS')
