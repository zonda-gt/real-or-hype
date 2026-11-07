import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import edlRaw from '../edl.json';
import places from '../src_places.json';
export const W = 1080, H = 1920, BR = '#FF5A36', Y = '#FFD43B';
const P = places as [string, string, string, string][];
export type Word = {w: string; f: number; e: number};
export type Seg = {id: string; frames: number; words: Word[]};
export const EDL: Record<string, Seg> = Object.fromEntries((edlRaw as Seg[]).map(s => [s.id, s]));
export const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
export const useSpr = (delay: number, cfg = {damping: 12, stiffness: 170, mass: 0.6}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); return spring({frame: f - delay, fps, config: cfg});
};
export const wf = (id: string, word: string, nth = 0) => { const ws = EDL[id]?.words.filter(x => x.w.toLowerCase().replace(/[^a-z0-9']/g, '').startsWith(word.toLowerCase())) || []; return ws[nth]?.f ?? 0; };
export const fontCss = `@font-face{font-family:MX;src:url(${staticFile('Montserrat-ExtraBold.ttf')})}@font-face{font-family:PF;src:url(${staticFile('Playfair-Black.ttf')})}*{box-sizing:border-box}`;
export const Base: React.FC<{id: string; style?: React.CSSProperties}> = ({id, style}) => <OffthreadVideo src={staticFile(`${id}_base.mp4`)} muted style={{position: 'absolute', left: 0, top: 0, width: W, height: H, objectFit: 'cover', ...style}} />;
export const Cut: React.FC<{id: string; style?: React.CSSProperties}> = ({id, style}) => <OffthreadVideo src={staticFile(`${id}_cut.webm`)} transparent muted style={{position: 'absolute', left: 0, top: 0, width: W, height: H, ...style}} />;
export const Voice: React.FC<{id: string}> = ({id}) => <Audio src={staticFile(`${id}_a.wav`)} />;
export const Sfx: React.FC<{at: number; name: 'whoosh_es' | 'pop_es' | 'ding' | 'click'; vol?: number}> = ({at, name, vol = 0.3}) => <Sequence from={Math.max(0, at)} durationInFrames={24}><Audio src={staticFile(`${name}.wav`)} volume={vol} /></Sequence>;
// word-synced captions: chunks of <=3 words, active word yellow
export const Captions: React.FC<{id: string; top?: number; keys?: string[]; size?: number; hideFrom?: number}> = ({id, top = 1330, keys = [], size = 76, hideFrom = 1e9}) => {
  const f = useCurrentFrame(); const ws = EDL[id]?.words || []; const chunks: Word[][] = [];
  let cur: Word[] = [];
  ws.forEach(w => { cur.push(w); if (cur.length >= 3 || /[.,!?]$/.test(w.w)) { chunks.push(cur); cur = []; } });
  if (cur.length) chunks.push(cur);
  const idx = chunks.findIndex((c, i) => f >= c[0].f - 2 && (i === chunks.length - 1 || f < chunks[i + 1][0].f - 2));
  if (idx < 0 || f >= hideFrom) return null;
  const c = chunks[idx]; const s = spring({frame: f - (c[0].f - 2), fps: 24, config: {damping: 13, stiffness: 260, mass: 0.5}});
  return (<div style={{position: 'absolute', left: 30, right: 30, top, textAlign: 'center', transform: `scale(${0.85 + 0.15 * s})`}}>
    {c.map((w, k) => { const act = c.reduce((a, x, j) => (f >= x.f - 2 ? j : a), 0); const on = f >= w.f - 2; const key = keys.some(kk => w.w.toLowerCase().includes(kk)); return (
      <span key={k} style={{fontFamily: 'MX', fontSize: key ? size * 1.25 : size, color: (on && key) || k === act ? Y : '#fff', WebkitTextStroke: `${key ? 16 : 13}px #000`, paintOrder: 'stroke fill', margin: '0 10px', display: 'inline-block', textTransform: 'lowercase'}}>{w.w.replace(/[.,]$/, '')}</span>); })}
  </div>);
};
export const Card: React.FC<{i: number; w: number; views?: boolean; style?: React.CSSProperties}> = ({i, w, views = true, style}) => (
  <div style={{position: 'absolute', width: w, height: w * 1.5, borderRadius: w * 0.12, border: `${Math.max(4, w * 0.035)}px solid #fff`, backgroundImage: `url(${staticFile(P[i][0] + '.jpg')})`, backgroundSize: 'cover', backgroundPosition: 'center', boxShadow: '0 24px 50px rgba(0,0,0,.35)', overflow: 'hidden', ...style}}>
    {views && <div style={{position: 'absolute', left: 10, bottom: 8, color: '#fff', font: `700 ${Math.round(w * 0.11)}px Inter`, textShadow: '0 2px 6px #000'}}>▶ {P[i][2]}</div>}
  </div>);
// phone with a screen image; children are positioned in screen fractions
export const Phone: React.FC<{src: string; w: number; style?: React.CSSProperties; children?: React.ReactNode}> = ({src, w, style, children}) => {
  const b = w * 0.032, sw = w - 2 * b, sh = sw / 0.4615;
  return (<div style={{position: 'absolute', width: w, height: sh + 2 * b, borderRadius: w * 0.15, background: '#1c1c1e', boxShadow: '0 40px 100px rgba(0,0,0,.45), inset 0 0 0 3px #46464a', ...style}}>
    <div style={{position: 'absolute', left: b, top: b, width: sw, height: sh, borderRadius: w * 0.12, overflow: 'hidden'}}>
      <Img src={staticFile(src)} style={{width: sw, height: sh}} />
      {children}
      <div style={{position: 'absolute', left: sw / 2 - sw * 0.12, top: sh * 0.012, width: sw * 0.24, height: sw * 0.065, borderRadius: sw * 0.04, background: '#000'}} />
    </div></div>);
};

// ---- effects ----
export const PhoneHold: React.FC<{id: string; src: string}> = ({id, src}) => {
  const f = useCurrentFrame(); const s = useSpr(2, {damping: 14, stiffness: 120, mass: 0.8});
  return (<AbsoluteFill><Base id={id} />
    <Phone src={src} w={430} style={{left: 610, top: interpolate(s, [0, 1], [1950, 330]) + Math.sin(f / 10) * 8, transform: `perspective(1600px) rotateY(-18deg) rotateZ(${4 + (1 - s) * 10}deg)`}} />
    <Sfx at={2} name="whoosh_es" /><Voice id={id} /><Captions id={id} keys={['10', 'ten', 'reels']} /></AbsoluteFill>);
};
export const Checklist: React.FC<{id: string; items: string[]; ticks: number[]}> = ({id, items, ticks}) => {
  const f = useCurrentFrame(); const e = useSpr(0, {damping: 15, stiffness: 140, mass: 0.7}); const st = ticks.filter(t => f >= t).length;
  const sp = ticks.map(t => useSpr(t, {damping: 9, stiffness: 260, mass: 0.5}));
  return (<AbsoluteFill><Base id={id} />
    <div style={{position: 'absolute', left: 80, top: interpolate(e, [0, 1], [-500, 140]), width: 920, padding: '40px 52px', borderRadius: 44, background: 'rgba(22,22,26,.62)', backdropFilter: 'blur(28px)', border: '2px solid rgba(255,255,255,.18)', boxShadow: '0 30px 80px rgba(0,0,0,.45)'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', font: '700 30px Inter', letterSpacing: '.12em', color: 'rgba(255,255,255,.65)', marginBottom: 12}}><span>ALL YOU NEED TO DO</span><span>{st} of {items.length}</span></div>
      {items.map((t, j) => { const on = f >= ticks[j]; return (<div key={j} style={{display: 'flex', alignItems: 'center', gap: 26, padding: '18px 0', font: '700 46px Inter', color: on ? '#fff' : 'rgba(255,255,255,.45)'}}>
        <div style={{width: 58, height: 58, borderRadius: 29, border: on ? 'none' : '4px solid rgba(255,255,255,.4)', background: on ? BR : 'transparent', display: 'grid', placeItems: 'center', color: '#fff', fontSize: 36, transform: `scale(${on ? 0.6 + 0.4 * sp[j] : 1})`}}>{on ? '✓' : ''}</div>{t}</div>); })}
    </div>
    {ticks.map((t, k) => <Sfx key={k} at={t} name="ding" vol={0.25} />)}<Sfx at={0} name="whoosh_es" />
    <Voice id={id} /><Captions id={id} keys={['send', 'this']} /></AbsoluteFill>);
};
export const Orbit: React.FC<{id: string; keys?: string[]}> = ({id, keys = []}) => {
  const f = useCurrentFrame(); const g = useSpr(0, {damping: 16, stiffness: 90, mass: 0.8});
  const items = P.map((_, i) => { const a = (2 * Math.PI * i) / 10 + 0.2 + f * 0.06; return {i, a, x: 540 + 500 * g * Math.cos(a), y: 1020 + 120 * g * Math.sin(a), d: (Math.sin(a) + 1) / 2}; });
  const r = (it: typeof items[0]) => { const w = 150; return <div key={it.i} style={{position: 'absolute', left: it.x - w / 2, top: it.y - w * 0.75, width: w, height: w * 1.5, transform: `perspective(900px) rotateY(${-Math.cos(it.a) * 55}deg) scale(${(0.55 + 0.6 * it.d) * g})`, filter: `blur(${(1 - it.d) * 2.5}px) brightness(${0.75 + 0.25 * it.d})`}}><Card i={it.i} w={w} views={false} /></div>; };
  return (<AbsoluteFill><Base id={id} />{items.filter(t => Math.sin(t.a) <= 0).map(r)}<Cut id={id} />{items.filter(t => Math.sin(t.a) > 0).sort((a, b) => a.d - b.d).map(r)}
    <Sfx at={0} name="whoosh_es" /><Voice id={id} /><Captions id={id} keys={keys} /></AbsoluteFill>);
};
export const CouchWall: React.FC<{id: string; keys?: string[]}> = ({id, keys = []}) => {
  const f = useCurrentFrame();
  const pos = [[150,190,190,-6],[360,120,170,4],[780,130,180,-3],[960,300,160,7],[110,620,170,5],[975,640,170,-5],[270,400,150,-2],[850,430,150,3],[560,70,150,-4]];
  const sp = pos.map((_, i) => useSpr(2 + i * 3));
  return (<AbsoluteFill><Base id={id} />
    {pos.map(([x, y, w, r], i) => <div key={i} style={{position: 'absolute', left: x - w / 2, top: y - w * 0.75 + Math.sin((f + i * 9) / 18) * 6, transform: `scale(${sp[i]}) rotate(${r + (1 - sp[i]) * 20}deg)`, width: w, height: w * 1.5}}><Card i={i} w={w} /></div>)}
    <Cut id={id} />{pos.map((_, i) => i % 2 === 0 ? <Sfx key={i} at={2 + i * 3} name="pop_es" vol={0.18} /> : null)}
    <Voice id={id} /><Captions id={id} keys={keys} /></AbsoluteFill>);
};
export const UIWorld: React.FC<{id: string; fly: number[]; replyAt: number; keys?: string[]}> = ({id, fly, replyAt, keys = []}) => {
  const f = useCurrentFrame(); const e = useSpr(0, {damping: 14, stiffness: 120, mass: 0.8}); const cards = [4, 6, 1, 3];
  return (<AbsoluteFill><Base id={id} />
    <div style={{position: 'absolute', left: 610, top: interpolate(e, [0, 1], [-1100, 150]), transform: `perspective(1600px) rotateY(-20deg) rotateZ(${4 + (1 - e) * 8}deg)`, width: 430, height: 930}}>
      <div style={{width: 430, height: 930, borderRadius: 56, border: '10px solid #111', overflow: 'hidden', boxShadow: '0 40px 90px rgba(0,0,0,.5)'}}><Img src={staticFile(f >= replyAt ? 'screen_dm.png' : 'screen_dm_sending.png')} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div></div>
    {fly.map((t0, k) => { const q = interpolate(f, [t0, t0 + 10], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)}); if (q <= 0 || q >= 1) return null;
      const x = interpolate(q, [0, 1], [-60, 820]), y = interpolate(q, [0, 1], [1150, 650]) - 260 * Math.sin(Math.PI * q);
      return <div key={k} style={{position: 'absolute', left: x - 90, top: y - 135, transform: `scale(${1.1 - 0.75 * q}) rotate(${-20 * (1 - q)}deg)`, opacity: q > 0.8 ? (1 - q) * 5 : 1}}><Card i={cards[k % 4]} w={180} /></div>; })}
    <Sfx at={0} name="whoosh_es" />{fly.map((t, k) => <Sfx key={k} at={t} name="whoosh_es" vol={0.15} />)}<Sfx at={replyAt} name="ding" />
    <Voice id={id} /><Captions id={id} keys={keys} /></AbsoluteFill>);
};
// his shot shrinks into a facecam tile while the itinerary phone rises
export const PullBackReveal: React.FC<{id: string; src: string; keys?: string[]}> = ({id, src, keys = []}) => {
  const f = useCurrentFrame(); const p = useSpr(3, {damping: 18, stiffness: 110, mass: 0.8}); const ph = useSpr(8, {damping: 15, stiffness: 100, mass: 0.8});
  const t = {x: 50, y: 110, w: 320, h: 430};
  const r = {x: interpolate(p, [0, 1], [0, t.x]), y: interpolate(p, [0, 1], [0, t.y]), w: interpolate(p, [0, 1], [W, t.w]), h: interpolate(p, [0, 1], [H, t.h])};
  return (<AbsoluteFill style={{background: 'linear-gradient(160deg,#F3EEE6,#E6DED2)'}}>
    <Phone src={src} w={640} style={{left: 400, top: interpolate(ph, [0, 1], [2000, 150]), transform: `rotate(${(1 - ph) * 8}deg)`}} />
    <div style={{position: 'absolute', left: r.x, top: r.y, width: r.w, height: r.h, borderRadius: 36 * p, overflow: 'hidden', boxShadow: `0 20px 60px rgba(0,0,0,${0.35 * p})`, border: `${6 * p}px solid #fff`}}>
      <Base id={id} style={{width: W, height: H, transform: `scale(${interpolate(p, [0, 1], [1, 0.42])})`, transformOrigin: '540px 760px', left: (r.w - W) / 2, top: (r.h - H) / 2}} /></div>
    <Sfx at={3} name="whoosh_es" /><Sfx at={8} name="pop_es" vol={0.25} />
    <Voice id={id} /><Captions id={id} keys={keys} top={1755} size={64} /></AbsoluteFill>);
};
// the stop page, zooming in; optional highlights at word frames (rects in screen fractions)
export const StopScreen: React.FC<{voice?: string; capId?: string; hl?: {at: number; r: [number, number, number, number]}[]; keys?: string[]}> = ({voice, capId, hl = [], keys = []}) => {
  const f = useCurrentFrame(); const z = interpolate(f, [0, 8], [3.2, 1], {...clamp, easing: Easing.out(Easing.cubic)}); const sw = 740 * (1 - 0.064), sh = sw / 0.4615;
  const sp = hl.map(h => useSpr(h.at, {damping: 11, stiffness: 220, mass: 0.5}));
  return (<AbsoluteFill style={{background: '#111'}}>
    <Img src={staticFile('p06_catcafe.jpg')} style={{position: 'absolute', width: W, height: H, objectFit: 'cover', filter: 'blur(40px) brightness(.55)', transform: 'scale(1.2)'}} />
    <div style={{position: 'absolute', left: 170, top: 100, transform: `scale(${z})`, transformOrigin: '370px 500px', filter: `blur(${(z - 1) * 4}px)`}}>
      <Phone src="C_sunburst.png" w={740}>
        {hl.map((h, k) => f >= h.at ? <div key={k} style={{position: 'absolute', left: h.r[0] * sw - 8, top: h.r[1] * sh - 8, width: (h.r[2] - h.r[0]) * sw + 16, height: (h.r[3] - h.r[1]) * sh + 16, borderRadius: 26, border: `6px solid ${BR}`, boxShadow: `0 0 0 ${10 * (1 - sp[k])}px rgba(255,90,54,.35)`, transform: `scale(${0.8 + 0.2 * sp[k]})`}} /> : null)}
      </Phone></div>
    <Sfx at={0} name="whoosh_es" vol={0.35} />{hl.map((h, k) => <Sfx key={k} at={h.at} name="pop_es" vol={0.22} />)}
    {voice && <Voice id={voice} />}{capId && <Captions id={capId} keys={keys} top={1730} size={64} />}</AbsoluteFill>);
};
export const RouteGrow: React.FC<{id: string; at: number[]; tipAt?: number; keys?: string[]}> = ({id, at, tipAt, keys = []}) => {
  const f = useCurrentFrame();
  const pts = [[120, 700], [345, 500], [570, 380], [795, 450], [975, 660]];
  const pins: [number | null, string][] = [[null, 'Start'], [5, 'Cat café'], [null, ''], [3, 'Yu Garden'], [2, 'Rooftop bar']];
  const segL = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1])); const total = segL.reduce((a, b) => a + b, 0);
  let len = 0; for (let k = 0; k < at.length - 1; k++) len += segL[k] * interpolate(f, [at[k], at[k + 1]], [0, 1], clamp);
  const d = 'M' + pts.map(p => p.join(',')).join(' L'); const sp = at.map(a => useSpr(a, {damping: 9, stiffness: 220, mass: 0.5})); const day = useSpr(0); const tp = useSpr(tipAt ?? 1e6, {damping: 11, stiffness: 200, mass: 0.6});
  return (<AbsoluteFill><Base id={id} />
    <svg width={W} height={H} style={{position: 'absolute'}}><defs><mask id={`rv${id}`}><path d={d} stroke="#fff" strokeWidth={20} fill="none" strokeDasharray={`${len} ${total}`} strokeLinecap="round" /></mask></defs>
      <path d={d} stroke={BR} strokeWidth={11} fill="none" strokeDasharray="26 18" strokeLinecap="round" mask={`url(#rv${id})`} /></svg>
    {pins.map(([ci, lab], k) => { const s = sp[k]; const [x, y] = pts[k]; return (<React.Fragment key={k}>
      {ci !== null && <div style={{position: 'absolute', left: x - 70, top: y - 250, transform: `scale(${s})`, transformOrigin: '70px 230px'}}><Card i={ci} w={140} views={false} /></div>}
      {lab && ci !== null && <div style={{position: 'absolute', left: x - 110, top: y + 42, width: 220, textAlign: 'center', transform: `scale(${s})`}}><span style={{background: 'rgba(29,29,31,.9)', color: '#fff', font: '700 30px Inter', padding: '8px 18px', borderRadius: 24}}>{lab}</span></div>}
      <div style={{position: 'absolute', left: x - 34, top: y - 34, width: 68, height: 68, borderRadius: 34, background: BR, border: '6px solid #fff', display: 'grid', placeItems: 'center', color: '#fff', font: '800 32px Inter', transform: `scale(${s})`}}>{k + 1}</div></React.Fragment>); })}
    <div style={{position: 'absolute', left: 60, top: 80, font: '800 48px Inter', color: '#fff', background: '#1d1d1f', padding: '14px 34px', borderRadius: 44, transform: `scale(${day})`}}>DAY 1</div>
    <Cut id={id} />
    {tipAt !== undefined && <div style={{position: 'absolute', left: 560, top: 900, width: 460, padding: '22px 26px', borderRadius: 28, background: '#FFF4EF', boxShadow: '0 20px 50px rgba(0,0,0,.3)', transform: `scale(${tp}) rotate(${(1 - tp) * 8 + 2}deg)`, transformOrigin: '0 0'}}>
      <div style={{font: '800 30px Inter', color: BR}}>Steven's tip</div><div style={{font: '600 30px Inter', color: '#1d1d1f', marginTop: 6}}>Go before 10 to beat the crowds</div></div>}
    {at.map((a, k) => <Sfx key={k} at={a} name="pop_es" vol={0.22} />)}{tipAt !== undefined && <Sfx at={tipAt} name="ding" vol={0.25} />}
    <Voice id={id} /><Captions id={id} keys={keys} /></AbsoluteFill>);
};
export const CoverStory: React.FC<{id: string; words: {text: string; at: number}[]; yourAt?: number}> = ({id, words, yourAt}) => {
  const ya = yourAt ?? words[0].at;
  const f = useCurrentFrame(); const cur = [...words].reverse().find(w => f >= w.at); const sc = interpolate(f, [0, 60], [1, 1.06], clamp);
  const sp = useSpr(cur?.at ?? 0, {damping: 12, stiffness: 180, mass: 0.6}); const yr = useSpr(ya, {damping: 12, stiffness: 180, mass: 0.6});
  return (<AbsoluteFill><Base id={id} style={{transform: `scale(${sc})`}} />
    {f >= ya && <div style={{position: 'absolute', left: 0, right: 0, top: 360, textAlign: 'center', font: '900 260px PF', color: '#fff', lineHeight: 1, textShadow: '0 12px 40px rgba(0,0,0,.25)', transform: `translateY(${(1 - yr) * 100}px)`, opacity: Math.min(1, yr * 1.5)}}>YOUR</div>}
    {cur && <div key={cur.text} style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', font: '900 260px PF', color: cur === words[words.length - 1] ? Y : '#fff', lineHeight: 1, textShadow: '0 12px 40px rgba(0,0,0,.25)', transform: `translateY(${(1 - sp) * 120}px)`, opacity: Math.min(1, sp * 1.5)}}>{cur.text}</div>}
    <Cut id={id} style={{transform: `scale(${sc})`}} />{words.map((w, k) => <Sfx key={k} at={w.at} name="whoosh_es" vol={0.2} />)}<Voice id={id} /></AbsoluteFill>);
};
export const FrameBreak: React.FC<{id: string; keys?: string[]; capTop?: number; followAt?: number}> = ({id, keys = [], capTop = 1600, followAt = 1e6}) => {
  const f = useCurrentFrame(); const p = useSpr(0, {damping: 16, stiffness: 110, mass: 0.8}); const fs = useSpr(followAt);
  const r = {x0: 142 * p, y0: 210 * p, x1: W - 142 * p, y1: H - 360 * p}; const follow = f >= followAt;
  return (<AbsoluteFill style={{background: '#000'}}>
    <Base id={id} style={{filter: 'blur(26px) brightness(.4)', transform: 'scale(1.1)'}} />
    <div style={{position: 'absolute', left: r.x0, top: r.y0, width: r.x1 - r.x0, height: r.y1 - r.y0, borderRadius: 44 * p, overflow: 'hidden', border: `${6 * p}px solid #fff`}}>
      <Base id={id} style={{left: -r.x0, top: -r.y0}} />
      <div style={{position: 'absolute', right: 26, bottom: 170, opacity: p, display: 'flex', flexDirection: 'column', gap: 34, alignItems: 'center', color: '#fff', font: '600 26px Inter', textShadow: '0 2px 8px #000'}}>
        {[['♥', '12.4K'], ['💬', '1,024'], ['➤', '']].map(([i, l]) => <div key={i} style={{textAlign: 'center'}}><div style={{fontSize: 60}}>{i}</div>{l}</div>)}</div>
      <div style={{position: 'absolute', left: 30, bottom: 40, display: 'flex', alignItems: 'center', gap: 16, font: '700 34px Inter', color: '#fff', textShadow: '0 2px 8px #000', opacity: p}}>
        <span style={{width: 62, height: 62, borderRadius: 31, background: BR, display: 'grid', placeItems: 'center'}}>C</span>steven_chinapal
        <span style={{border: '3px solid #fff', borderRadius: 14, padding: '4px 18px', fontSize: 28, background: follow ? 'rgba(255,255,255,.25)' : 'transparent', transform: `scale(${follow ? 1 + 0.15 * (1 - fs) : 1})`}}>{follow ? 'Following' : 'Follow'}</span></div></div>
    <Cut id={id} style={{clipPath: `inset(0 0 ${H - r.y1}px 0)`}} />
    {followAt < 1e6 && <Sfx at={followAt} name="click" vol={0.4} />}
    <Voice id={id} /><Captions id={id} keys={keys} top={capTop} /></AbsoluteFill>);
};
// Instagram comment sheet slides up, "TRIP" gets typed and posted, auto-DM reply appears
export const CommentCTA: React.FC<{id: string; typeAt: number}> = ({id, typeAt}) => {
  const f = useCurrentFrame(); const sh = useSpr(0, {damping: 16, stiffness: 120, mass: 0.8}); const word = 'TRIP'; const n = Math.max(0, Math.min(4, Math.floor((f - typeAt) / 2) + 1));
  const posted = typeAt + 12; const ps = useSpr(posted, {damping: 12, stiffness: 200, mass: 0.6}); const rs = useSpr(posted + 10, {damping: 12, stiffness: 200, mass: 0.6});
  return (<AbsoluteFill><Base id={id} />
    <div style={{position: 'absolute', left: 0, right: 0, top: interpolate(sh, [0, 1], [H, 1180]), height: 800, background: '#1c1c1e', borderRadius: '48px 48px 0 0', boxShadow: '0 -20px 60px rgba(0,0,0,.4)', padding: '22px 40px', color: '#fff'}}>
      <div style={{width: 90, height: 10, borderRadius: 5, background: '#555', margin: '0 auto 22px'}} />
      <div style={{textAlign: 'center', font: '700 34px Inter', marginBottom: 30}}>Comments</div>
      {f >= posted && <div style={{display: 'flex', gap: 20, alignItems: 'center', transform: `translateY(${(1 - ps) * 40}px)`, opacity: ps, marginBottom: 26}}>
        <div style={{width: 72, height: 72, borderRadius: 36, background: 'linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7)'}} /><div><div style={{font: '600 26px Inter', color: '#aaa'}}>you · now</div><div style={{font: '700 40px Inter'}}>TRIP</div></div></div>}
      {f >= posted + 10 && <div style={{display: 'flex', gap: 20, alignItems: 'center', marginLeft: 70, transform: `translateY(${(1 - rs) * 40}px)`, opacity: rs}}>
        <div style={{width: 60, height: 60, borderRadius: 30, background: BR, display: 'grid', placeItems: 'center', font: '800 28px Inter'}}>C</div><div><div style={{font: '600 24px Inter', color: '#aaa'}}>steven_chinapal · author</div><div style={{font: '600 34px Inter'}}>Sent you a DM 📩</div></div></div>}
      <div style={{position: 'absolute', left: 40, right: 40, top: 520, height: 96, borderRadius: 48, border: '2px solid #444', display: 'flex', alignItems: 'center', padding: '0 34px', font: '600 38px Inter', color: f >= typeAt && f < posted ? '#fff' : '#888'}}>
        {f >= typeAt && f < posted ? word.slice(0, n) + (f % 12 < 6 ? '|' : '') : 'Add a comment…'}<span style={{marginLeft: 'auto', color: '#4c9aff', fontWeight: 700}}>{f >= typeAt + 8 && f < posted ? 'Post' : ''}</span></div></div>
    <Sfx at={0} name="whoosh_es" />{[0, 1, 2, 3].map(k => <Sfx key={k} at={typeAt + k * 2} name="click" vol={0.15} />)}<Sfx at={posted} name="pop_es" vol={0.3} /><Sfx at={posted + 10} name="ding" vol={0.3} />
    <Voice id={id} /><Captions id={id} keys={['trip']} top={300} /></AbsoluteFill>);
};
