"""Render a version spec to mp4 (video+VO+sfx, no music).
usage: render.py spec.py out.mp4 [--clean]   (--clean = footage only, no overlays/captions: for the OCR proof)
spec module defines: BEATS (list), OVERLAYS (list), VO (list of (key, t)), SFX (list of (file, t, gain_db))
BEAT = {'layout': 'single'|'split'|'tri', 'dur': s, 'shots': [ {clip,t,crop:(x,y,w,h),speed,zoom:(z0,z1),pan:(dx,dy)} ...]}
OVERLAY = (PIL RGBA image 1080x1920, t0, t1, anim)  anim in {None,'pop','fade'}"""
import sys, os, json, subprocess, importlib.util, numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx

FPS = 30; W, H = 1080, 1920
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WIN = {'single': [(0, 400, 1080, 1080)],
       'split': [(0, 300, 1080, 640), (0, 952, 1080, 640)],
       'tri': [(0, 290, 1080, 430), (0, 735, 1080, 430), (0, 1180, 1080, 430)],
       'full': [(0, 0, 1080, 1920)],
       'split2': [(0, 0, 1080, 956), (0, 964, 1080, 956)],
       'tall': [(0, 285, 1080, 1350)]}
CAP_Y = {'single': 1512, 'split': 200, 'tri': 196, 'full': 1300, 'split2': 1440, 'tall': 1380}


def load_spec(p):
    s = importlib.util.spec_from_file_location('spec', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def shot_frames(sh, dur, ww, wh):
    """returns float32 frames (n,wh,ww,3) for the shot window, with zoom/pan applied"""
    n = int(round(dur * FPS))
    speed = sh.get('speed', 1.0); z0, z1 = sh.get('zoom', (1.0, 1.0))
    zmax = max(z0, z1); ex_w, ex_h = int(ww * zmax) // 2 * 2, int(wh * zmax) // 2 * 2
    x, y, w, h = sh['crop']
    src = f"{B}/hd/{sh['clip']}.mp4"
    # decode from 2 s before the in-point so the HEVC decoder is warmed up (avoids smeared first frames), then trim
    pre = max(0.0, sh['t'] - 2.0); off = sh['t'] - pre
    head = f"trim=start={off:.4f},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y}"
    if sh.get('freeze'):
        vf = f"{head},scale={ex_w}:{ex_h}:flags=lanczos"
    elif speed < 0.95:
        # minterpolate emits a blank first frame: drop the first 2 output frames
        vf = (f"{head},scale={ex_w}:{ex_h}:flags=lanczos,setpts=PTS/{speed},"
              f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,trim=start_frame=2,setpts=PTS-STARTPTS")
    else:
        vf = f"{head},setpts=PTS/{speed},fps={FPS},scale={ex_w}:{ex_h}:flags=lanczos"
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{pre:.4f}', '-t', f'{off + dur * speed + 0.6:.4f}', '-i', src, '-an', '-vf', vf,
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, ex_h, ex_w, 3)
    if sh.get('freeze'):
        fr = np.repeat(fr[:1], n, axis=0)
    if len(fr) < n:
        raise SystemExit(f"shot {sh['clip']}@{sh['t']} too short: {len(fr)} < {n} frames")
    out = np.empty((n, wh, ww, 3), np.uint8)
    pdx, pdy = sh.get('pan', (0, 0))
    for i in range(n):
        a = i / max(1, n - 1); z = z0 + (z1 - z0) * a
        # crop size so that output = window at zoom z (relative to the extraction which is at zmax)
        cw = min(ww * zmax / z, ex_w); ch = min(wh * zmax / z, ex_h)
        cx = ex_w / 2 + pdx * a * (ex_w - cw) / 2; cy = ex_h / 2 + pdy * a * (ex_h - ch) / 2
        cwi, chi = min(int(round(cw)), ex_w), min(int(round(ch)), ex_h)
        x0 = max(0, min(int(round(cx - cwi / 2)), ex_w - cwi)); y0 = max(0, min(int(round(cy - chi / 2)), ex_h - chi))
        sub = fr[i][y0:y0 + chi, x0:x0 + cwi]
        out[i] = cv2.resize(sub, (ww, wh), interpolation=cv2.INTER_AREA if z < 1 else cv2.INTER_CUBIC)
    return out


def bg_from(win_frame):
    small = cv2.resize(win_frame, (54, 96), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), 6)
    big = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) * 0.38
    return big


def prep_overlays(ovs):
    out = []
    for img, t0, t1, anim in ovs:
        a = np.asarray(img)
        ys, xs = np.where(a[..., 3] > 0)
        if not len(xs):
            continue
        pad = 40 if anim == 'pop' else 0
        x0, y0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
        x1, y1 = min(W, xs.max() + 1 + pad), min(H, ys.max() + 1 + pad)
        crop = a[y0:y1, x0:x1].astype(np.float32)
        out.append(dict(rgb=crop[..., :3], a=crop[..., 3:4] / 255.0, t0=t0, t1=t1, anim=anim, box=(x0, y0, x1, y1)))
    return out


def comp_overlay(frame, o, t):
    if not (o['t0'] <= t < o['t1']):
        return
    dt = t - o['t0']
    rgb, a = o['rgb'], o['a']
    x0, y0, x1, y1 = o['box']
    if o['anim'] == 'pop' and dt < 0.2:
        s = [0.6, 0.85, 1.08, 1.12, 1.06, 1.0][min(5, int(dt * FPS))]
        h, w = rgb.shape[:2]; cx, cy = w / 2, h / 2
        M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy]])
        rgba = cv2.warpAffine(np.dstack([rgb, a]), M, (w, h), flags=cv2.INTER_LINEAR)
        rgb, a = rgba[..., :3], rgba[..., 3:4]
    if o['anim'] in ('pop', 'fade'):
        fade = min(1.0, dt / 0.12, (o['t1'] - t) / 0.08)
    else:
        fade = min(1.0, (o['t1'] - t) / 0.05)
    aa = a * max(0.0, fade)
    region = frame[y0:y1, x0:x1]
    region[:] = region * (1 - aa) + rgb * aa


def main():
    spec = load_spec(sys.argv[1]); out = sys.argv[2]; clean = '--clean' in sys.argv
    beats = spec.BEATS
    total = sum(b['dur'] for b in beats)
    nT = int(round(total * FPS))
    ovs = [] if clean else prep_overlays(spec.OVERLAYS + spec.caption_overlays(CAP_Y))
    tmpv = out + '.v.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
                            '-color_trc', 'bt709', '-colorspace', 'bt709', tmpv], stdin=subprocess.PIPE)
    fi = 0; t_beat = 0.0; log = []
    for bi, b in enumerate(beats):
        n = int(round((t_beat + b['dur']) * FPS)) - int(round(t_beat * FPS))
        wins = WIN[b['layout']]
        frs = [shot_frames(sh, n / FPS, w_[2], w_[3]) for sh, w_ in zip(b['shots'], wins)]
        log.append(dict(beat=bi, t0=round(t_beat, 3), dur=round(n / FPS, 3), layout=b['layout'], shots=b['shots']))
        for i in range(n):
            if b['layout'] == 'full':
                frame = frs[0][i].astype(np.float32)
            elif b['layout'] == 'split2':
                frame = np.full((H, W, 3), 12.0, np.float32)
                for f_, (x, y, w, h) in zip(frs, wins):
                    frame[y:y + h, x:x + w] = f_[i]
            else:
                frame = bg_from(frs[0][i])
                for f_, (x, y, w, h) in zip(frs, wins):
                    frame[y:y + h, x:x + w] = f_[i]
            t = fi / FPS
            for o in ovs:
                comp_overlay(frame, o, t)
            enc.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
            fi += 1
        t_beat += b['dur']
    enc.stdin.close(); enc.wait()
    json.dump(log, open(out + '.beats.json', 'w'), indent=1)
    # audio: VO lines + sfx
    inputs = []; filt = []; k = 0
    for key, t in spec.VO:
        inputs += ['-i', f'{B}/vo/p/{key}.wav']
        filt.append(f'[{k+1}:a]aresample=48000,aformat=channel_layouts=mono,volume=1.0,adelay={int(t*1000)}:all=1[a{k}]'); k += 1
    for f, t, g in ([] if clean else spec.SFX):
        inputs += ['-i', f]
        filt.append(f'[{k+1}:a]aresample=48000,aformat=channel_layouts=mono,volume={g}dB,adelay={int(t*1000)}:all=1[a{k}]'); k += 1
    mix = ''.join(f'[a{i}]' for i in range(k)) + f'amix=inputs={k}:normalize=0:duration=longest,apad,atrim=0:{nT/FPS},loudnorm=I=-15:TP=-2:LRA=9,alimiter=limit=0.78:level=0,aresample=48000[aout]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmpv] + inputs + ['-filter_complex', ';'.join(filt) + ';' + mix,
                    '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
    os.remove(tmpv)
    print('wrote', out, round(nT / FPS, 2), 's')


if __name__ == '__main__':
    main()
