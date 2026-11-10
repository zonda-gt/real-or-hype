import os, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.environ.get('WORK', '.') + '/tools')
from skymask import sky_prob
FONT = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Anton-Regular.ttf'
MODEL = os.environ.get('WORK', '.') + '/models/segformer_b4.onnx'
def text_layer(W=1920, H=1080, text='CHINA VLOG', box=(358, 185, 1562, 625), color=(250, 222, 22)):
    # render big, then squash horizontally into box (tall condensed look like the reference)
    f = ImageFont.truetype(FONT, 600)
    l, t, r, b = f.getbbox(text)
    im = Image.new('L', (r - l + 20, b - t + 20), 0)
    ImageDraw.Draw(im).text((10 - l, 10 - t), text, font=f, fill=255)
    bw, bh = box[2] - box[0], box[3] - box[1]
    im = im.resize((bw, bh), Image.LANCZOS)
    a = np.zeros((H, W), np.float32); a[box[1]:box[3], box[0]:box[2]] = np.asarray(im, np.float32) / 255
    return a, np.array(color, np.float32)
def guided(I, p, r=8, eps=1e-3):
    mI = cv2.boxFilter(I, -1, (r, r)); mp = cv2.boxFilter(p, -1, (r, r))
    cIp = cv2.boxFilter(I * p, -1, (r, r)) - mI * mp; vI = cv2.boxFilter(I * I, -1, (r, r)) - mI * mI
    a = cIp / (vI + eps); b = mp - a * mI
    return cv2.boxFilter(a, -1, (r, r)) * I + cv2.boxFilter(b, -1, (r, r))
def composite(frame_rgb, alpha, color, sky=None):
    if sky is None:
        sky = np.asarray(sky_prob(Image.fromarray(frame_rgb), MODEL), np.float32) / 255
    g = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    sky = np.clip(guided(g, sky, 6, 1e-3), 0, 1)
    sky = np.clip((sky - 0.35) / 0.3, 0, 1)  # tighten
    a = (alpha * sky)[..., None]
    out = frame_rgb.astype(np.float32) * (1 - a) + color * a
    return out.astype(np.uint8), sky
if __name__ == '__main__':
    fr = np.asarray(Image.open(sys.argv[1]).convert('RGB').resize((1920, 1080)))
    al, col = text_layer()
    out, sky = composite(fr, al, col)
    Image.fromarray(out).save(sys.argv[2], quality=92)

def words_layer(W, H, words, y0, y1, xs, squash, color=(242, 219, 17)):
    """Render words at a common height (y0..y1) and horizontal squash; xs = left x of each word."""
    f = ImageFont.truetype(FONT, 600)
    a = np.zeros((H, W), np.float32)
    for text, x in zip(words, xs):
        l, t, r, b = f.getbbox(text)
        im = Image.new('L', (r - l + 20, b - t + 20), 0)
        ImageDraw.Draw(im).text((10 - l, 10 - t), text, font=f, fill=255)
        h = y1 - y0; w = int(im.width * h / im.height * squash)
        im = np.asarray(im.resize((w, h), Image.LANCZOS), np.float32) / 255
        xe = min(W, x + w); a[y0:y1, x:xe] = np.maximum(a[y0:y1, x:xe], im[:, :xe - x])
    return a, np.array(color, np.float32)

def word_width(text, h, squash):
    f = ImageFont.truetype(FONT, 600); l, t, r, b = f.getbbox(text)
    return int((r - l + 20) * h / (b - t + 20) * squash)
