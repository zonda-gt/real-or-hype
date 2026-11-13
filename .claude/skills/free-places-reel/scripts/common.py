"""Shared constants for the free-places reel. The 22 cut points come from the reference reel's song and must not change."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', 'real-or-hype-video', 'scripts')
W, H, FPS = 1080, 1920, 30
# shot boundaries in seconds (22 shots): 2 opening, 9 places x 2, 2 ending
CUTS = [0, 1.4333, 2.6, 4.3, 5.6, 6.8667, 8.4667, 9.9333, 11.3667, 12.9667, 14.3, 15.8667, 17.1667,
        18.8, 20.0667, 21.6667, 22.9667, 24.5667, 25.8667, 27.4667, 28.8, 30.2333, 31.836]
SONG_URL = 'https://www.facebook.com/share/r/1DLSqdyBWE/'   # Awe China reel; its audio is the soundtrack

def load_plan(path):
    p = json.load(open(path))
    assert len(p['shots']) == 22, 'plan needs exactly 22 shots'
    p['blur'] = {int(k): v for k, v in p.get('blur', {}).items()}
    p['precrop'] = {int(k): v for k, v in p.get('precrop', {}).items()}
    p['speed'] = {int(k): float(v) for k, v in p.get('speed', {}).items()}
    return p
