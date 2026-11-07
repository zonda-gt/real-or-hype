import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import places from '../src_places.json';

const W = 1080, H = 1920, BR = '#FF5A36', Y = '#FFD43B';
const P = places as [string, string, string, string][];
const fontCss = `
@font-face{font-family:MX;src:url(${staticFile('Montserrat-ExtraBold.ttf')})}
@font-face{font-family:PF;src:url(${staticFile('Playfair-Black.ttf')})}
*{box-sizing:border-box}`;
// segment lengths in frames (same cut as v1)
const SEG: [string, number][] = [['01',108],['02',95],['03',82],['04',59],['05',77],['06',114],['07',111],['08a',11],['08',49],['09',51],['10',141]];
export const TOTAL = SEG.reduce((a, s) => a + s[1], 0);
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const useSpring = (delay: number, cfg = {damping: 12, stiffness: 170, mass: 0.6}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return spring({frame: f - delay, fps, config: cfg});
};
const Base: React.FC<{n: string; style?: React.CSSProperties}> = ({n, style}) => (
  <OffthreadVideo src={staticFile(`base_${n}.mp4`)} muted style={{position: 'absolute', width: W, height: H, objectFit: 'cover', ...style}} />
);
const Cut: React.FC<{n: string; style?: React.CSSProperties}> = ({n, style}) => (
  <OffthreadVideo src={staticFile(`cut_${n}.webm`)} transparent muted style={{position: 'absolute', width: W, height: H, ...style}} />
);
const Caption: React.FC<{small: string; big: string; bigAt: number; smallAt?: number; top?: number}> = ({small, big, bigAt, smallAt = 0, top = 1330}) => {
  const f = useCurrentFrame(); const s1 = useSpring(smallAt, {damping: 14, stiffness: 220, mass: 0.5}); const s2 = useSpring(bigAt, {damping: 10, stiffness: 200, mass: 0.6});
  const txt: React.CSSProperties = {fontFamily: 'MX', color: '#fff', WebkitTextStroke: '12px #000', paintOrder: 'stroke fill', textAlign: 'center', whiteSpace: 'nowrap'};
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      {f >= smallAt && <div style={{...txt, fontSize: 56, transform: `scale(${0.7 + 0.3 * s1})`, opacity: s1}}>{small}</div>}
      {f >= bigAt && <div style={{...txt, fontSize: 108, color: Y, WebkitTextStroke: '16px #000', lineHeight: 1.05, transform: `scale(${s2}) rotate(${(1 - s2) * -4}deg)`}}>{big}</div>}
    </div>
  );
};
const Card: React.FC<{i: number; w: number; views?: boolean; style?: React.CSSProperties}> = ({i, w, views = true, style}) => (
  <div style={{position: 'absolute', width: w, height: w * 1.5, borderRadius: w * 0.12, border: `${Math.max(4, w * 0.035)}px solid #fff`, backgroundImage: `url(${staticFile(P[i][0] + '.jpg')})`, backgroundSize: 'cover', backgroundPosition: 'center', boxShadow: '0 24px 50px rgba(0,0,0,.35)', overflow: 'hidden', ...style}}>
    {views && <div style={{position: 'absolute', left: 10, bottom: 8, color: '#fff', font: `700 ${Math.round(w * 0.11)}px Inter`, textShadow: '0 2px 6px #000'}}>▶ {P[i][2]}</div>}
  </div>
);

// 01 couch wall: saved reels pin to the wall behind him
const S01 = () => {
  const f = useCurrentFrame();
  const pos = [[150,190,190,-6],[360,120,170,4],[780,130,180,-3],[960,300,160,7],[110,620,170,5],[975,640,170,-5],[270,400,150,-2],[850,430,150,3],[560,70,150,-4]];
  return (<AbsoluteFill>
    <Base n="01" />
    {pos.map(([x, y, w, r], i) => { const s = useSpring(3 + i * 6); return (
      <div key={i} style={{position: 'absolute', left: x - w / 2, top: y - w * 0.75 + Math.sin((f + i * 9) / 18) * 6, transform: `scale(${s}) rotate(${r + (1 - s) * 20}deg)`, width: w, height: w * 1.5}}><Card i={i} w={w} /></div>); })}
    <Cut n="01" />
    <Caption small="you've saved" big="hundreds of reels" bigAt={32} />
  </AbsoluteFill>);
};
// 02 orbit: the reels circle him in 3D
const S02 = () => {
  const f = useCurrentFrame(); const g = useSpring(0, {damping: 16, stiffness: 90, mass: 0.8});
  const items = P.map((_, i) => { const a = (2 * Math.PI * i) / 10 + 0.2 + f * 0.045; return {i, a, x: 540 + 500 * g * Math.cos(a), y: 1020 + 120 * g * Math.sin(a), d: (Math.sin(a) + 1) / 2}; });
  const render = (it: typeof items[0]) => { const w = 150; const s = (0.55 + 0.6 * it.d) * g; return (
    <div key={it.i} style={{position: 'absolute', left: it.x - w / 2, top: it.y - w * 0.75, width: w, height: w * 1.5, transform: `perspective(900px) rotateY(${-Math.cos(it.a) * 55}deg) scale(${s})`, filter: `blur(${(1 - it.d) * 2.5}px) brightness(${0.75 + 0.25 * it.d})`}}><Card i={it.i} w={w} views={false} /></div>); };
  return (<AbsoluteFill>
    <Base n="02" />
    {items.filter(t => Math.sin(t.a) <= 0).map(render)}
    <Cut n="02" />
    {items.filter(t => Math.sin(t.a) > 0).sort((a, b) => a.d - b.d).map(render)}
    <Caption small="rooftop bars, dumpling spots," big="that café…" smallAt={9} bigAt={79} />
  </AbsoluteFill>);
};
// 03 vertigo: dolly zoom on the empty room, he stays the same size
const S03 = () => {
  const f = useCurrentFrame(); const s = interpolate(f, [0, 82], [1, 1.75], {...clamp, easing: Easing.inOut(Easing.cubic)});
  return (<AbsoluteFill style={{background: '#000'}}>
    <Img src={staticFile('plate_03.jpg')} style={{position: 'absolute', width: W, height: H, transform: `scale(${s})`, transformOrigin: '540px 840px', filter: `blur(${(s - 1) * 4}px)`}} />
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, transparent 45%, rgba(0,0,0,${(s - 1) * 0.8}) 100%)`}} />
    <Cut n="03" />
    <Caption small="and you've been to" big="none of them." bigAt={31} />
  </AbsoluteFill>);
};
// 04 UI world: the DM with ChinaPal floats in, reels fly into it
const S04 = () => {
  const f = useCurrentFrame(); const e = useSpring(0, {damping: 14, stiffness: 120, mass: 0.8});
  const fly = [[4, 9], [6, 18], [1, 27]];
  return (<AbsoluteFill>
    <Base n="04" />
    <div style={{position: 'absolute', left: 610, top: interpolate(e, [0, 1], [-1100, 150]), width: 430, height: 930, borderRadius: 56, border: '10px solid #111', overflow: 'hidden', boxShadow: '0 40px 90px rgba(0,0,0,.5)', transform: `perspective(1600px) rotateY(-20deg) rotateZ(${4 + (1 - e) * 8}deg)`}}>
      <Img src={staticFile(f >= 47 ? 'screen_dm.png' : 'screen_dm_sending.png')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </div>
    {fly.map(([ci, t0], k) => { const q = interpolate(f, [t0, t0 + 11], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)}); if (q <= 0 || q >= 1) return null;
      const x = interpolate(q, [0, 1], [-60, 820]), y = interpolate(q, [0, 1], [1150, 650]) - 260 * Math.sin(Math.PI * q);
      return <div key={k} style={{position: 'absolute', left: x - 90, top: y - 135, transform: `scale(${1.1 - 0.75 * q}) rotate(${-20 * (1 - q)}deg)`, opacity: q > 0.8 ? (1 - q) * 5 : 1}}><Card i={ci} w={180} /></div>; })}
    <Caption small="so just send them" big="all to us" smallAt={20} bigAt={39} />
  </AbsoluteFill>);
};
// 05 checklist: glass panel ticks off as he counts
const S05 = () => {
  const f = useCurrentFrame(); const e = useSpring(0, {damping: 15, stiffness: 140, mass: 0.7});
  const ticks = [27, 49, 55]; const st = ticks.filter(t => f >= t).length;
  const items = ['Save the reel', 'Send it to @steven_chinapal', 'Get your trip'];
  return (<AbsoluteFill>
    <Base n="05" />
    <div style={{position: 'absolute', left: 80, top: interpolate(e, [0, 1], [-500, 150]), width: 920, padding: '40px 52px', borderRadius: 44, background: 'rgba(22,22,26,.62)', backdropFilter: 'blur(28px)', border: '2px solid rgba(255,255,255,.18)', boxShadow: '0 30px 80px rgba(0,0,0,.45)'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', font: '700 30px Inter', letterSpacing: '.12em', color: 'rgba(255,255,255,.65)', marginBottom: 12}}><span>ALL YOU NEED TO DO</span><span>{st} of 3</span></div>
      {items.map((t, j) => { const s = useSpring(ticks[j], {damping: 9, stiffness: 260, mass: 0.5}); const on = f >= ticks[j]; return (
        <div key={j} style={{display: 'flex', alignItems: 'center', gap: 26, padding: '20px 0', font: '700 46px Inter', color: on ? '#fff' : 'rgba(255,255,255,.45)'}}>
          <div style={{width: 58, height: 58, borderRadius: 29, border: on ? 'none' : '4px solid rgba(255,255,255,.4)', background: on ? BR : 'transparent', display: 'grid', placeItems: 'center', color: '#fff', fontSize: 36, transform: `scale(${on ? 0.6 + 0.4 * s : 1})`}}>{on ? '✓' : ''}</div>
          <span style={{textDecoration: 'none'}}>{t}</span></div>); })}
    </div>
  </AbsoluteFill>);
};
// 06 pull-back reveal: his shot shrinks into the trip being built
const S06 = () => {
  const f = useCurrentFrame(); const p = useSpring(11, {damping: 18, stiffness: 90, mass: 0.9});
  const win = {x: 70, y: 285, w: 940, h: 1570}; const vid = {x: win.x + 30, y: win.y + 108, w: win.w - 60, h: 720};
  const r = {x: interpolate(p, [0, 1], [0, vid.x]), y: interpolate(p, [0, 1], [0, vid.y]), w: interpolate(p, [0, 1], [W, vid.w]), h: interpolate(p, [0, 1], [H, vid.h])};
  const pct = Math.round(interpolate(f, [29, 108], [0, 100], {...clamp, easing: Easing.inOut(Easing.quad)}));
  const steps = ['Watched your 10 reels', 'Found 10 places', 'Grouped them by area', 'Checked opening hours', 'Built 3 days'];
  return (<AbsoluteFill style={{background: '#E9E4DA'}}>
    <div style={{opacity: p}}>
      <div style={{position: 'absolute', left: 60, top: 40, font: '900 180px Inter', letterSpacing: '-.05em', color: '#1d1d1f'}}>{pct}%</div>
      <div style={{position: 'absolute', left: win.x, top: win.y, width: win.w, height: win.h, borderRadius: 42, background: '#FAF8F4', boxShadow: '0 40px 100px rgba(0,0,0,.18)'}}>
        <div style={{height: 78, display: 'flex', alignItems: 'center', gap: 14, padding: '0 32px', borderBottom: '2px solid #eee'}}>
          {['#ff5f57', '#febc2e', '#28c840'].map(c => <i key={c} style={{width: 20, height: 20, borderRadius: 10, background: c}} />)}
          <span style={{marginLeft: 20, font: '600 28px Inter', color: '#888'}}>ChinaPal · building your trip</span></div>
        <div style={{position: 'absolute', left: 50, top: 850}}>
          {steps.map((s, i) => { const t0 = 34 + i * 15; const on = f >= t0; const k = useSpring(t0, {damping: 9, stiffness: 260, mass: 0.5}); return (
            <div key={i} style={{display: 'flex', gap: 22, alignItems: 'center', font: '700 40px Inter', color: on ? '#1d1d1f' : '#a5a5aa', padding: '10px 0'}}>
              <div style={{width: 46, height: 46, borderRadius: 23, display: 'grid', placeItems: 'center', color: '#fff', fontSize: 26, background: on ? BR : 'transparent', border: on ? 'none' : '4px solid #cfcac1', transform: `scale(${on ? 0.6 + 0.4 * k : 1})`}}>{on ? '✓' : ''}</div>{s}</div>); })}
          <div style={{marginTop: 30, width: 840, height: 22, borderRadius: 11, background: '#e6e1d8', overflow: 'hidden'}}><div style={{width: `${pct}%`, height: '100%', background: BR}} /></div>
          <div style={{display: 'flex', gap: 18, marginTop: 34}}>{P.slice(0, 5).map((q, i) => <div key={i} style={{width: 153, height: 200, borderRadius: 20, backgroundImage: `url(${staticFile(q[0] + '.jpg')})`, backgroundSize: 'cover', transform: `scale(${useSpring(34 + i * 12)})`}} />)}</div>
        </div>
      </div>
    </div>
    <div style={{position: 'absolute', left: r.x, top: r.y, width: r.w, height: r.h, borderRadius: 30 * p, overflow: 'hidden'}}>
      <Base n="06" style={{width: W, height: H, left: (r.w - W) / 2, top: (r.h - H) / 2 + interpolate(p, [0, 1], [0, -150])}} />
    </div>
  </AbsoluteFill>);
};
// 07 route grow: Day 1 route draws across the wall behind him
const S07 = () => {
  const f = useCurrentFrame();
  const pts = [[120, 700], [345, 500], [570, 380], [795, 450], [975, 660]]; const at = [7, 34, 50, 67, 91];
  const pins: [number, number | null, string][] = [[0, null, 'Start'], [1, 5, 'Cat café'], [2, null, ''], [3, 3, 'Yu Garden'], [4, 2, 'Rooftop bar']];
  let len = 0; const segL = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1])); const total = segL.reduce((a, b) => a + b, 0);
  for (let k = 0; k < at.length - 1; k++) { const q = interpolate(f, [at[k], at[k + 1]], [0, 1], clamp); len += segL[k] * q; }
  const d = 'M' + pts.map(p => p.join(',')).join(' L');
  return (<AbsoluteFill>
    <Base n="07" />
    <svg width={W} height={H} style={{position: 'absolute'}}>
      <defs><mask id="rv"><path d={d} stroke="#fff" strokeWidth={20} fill="none" strokeDasharray={`${len} ${total}`} strokeLinecap="round" /></mask></defs>
      <path d={d} stroke={BR} strokeWidth={11} fill="none" strokeDasharray="26 18" strokeLinecap="round" mask="url(#rv)" />
    </svg>
    {pins.map(([pi, ci, lab], k) => { const s = useSpring(at[k], {damping: 9, stiffness: 220, mass: 0.5}); const [x, y] = pts[pi]; return (
      <React.Fragment key={k}>
        {ci !== null && <div style={{position: 'absolute', left: x - 70, top: y - 250, transform: `scale(${s})`, transformOrigin: '70px 230px'}}><Card i={ci} w={140} views={false} /></div>}
        {lab && ci !== null && <div style={{position: 'absolute', left: x - 110, top: y + 42, width: 220, textAlign: 'center', transform: `scale(${s})`}}><span style={{background: 'rgba(29,29,31,.9)', color: '#fff', font: '700 30px Inter', padding: '8px 18px', borderRadius: 24}}>{lab}</span></div>}
        <div style={{position: 'absolute', left: x - 34, top: y - 34, width: 68, height: 68, borderRadius: 34, background: BR, border: '6px solid #fff', display: 'grid', placeItems: 'center', color: '#fff', font: '800 32px Inter', transform: `scale(${s})`, boxShadow: '0 8px 20px rgba(0,0,0,.3)'}}>{k + 1}</div>
      </React.Fragment>); })}
    <div style={{position: 'absolute', left: 60, top: 80, font: '800 48px Inter', color: '#fff', background: '#1d1d1f', padding: '14px 34px', borderRadius: 44, transform: `scale(${useSpring(0)})`}}>DAY 1</div>
    <Cut n="07" />
  </AbsoluteFill>);
};
// 08a zoom-through: dive into the café reel
const S08a = () => {
  const f = useCurrentFrame(); const s = interpolate(f, [0, 11], [0.55, 4.2], {...clamp, easing: Easing.in(Easing.cubic)});
  return (<AbsoluteFill style={{background: '#111'}}>
    {[0, 1, 2, 3, 4, 5].map(k => <Img key={k} src={staticFile('p06_catcafe.jpg')} style={{position: 'absolute', left: 0, top: (H - W * 1.5) / 2, width: W, height: W * 1.5, borderRadius: 40 / s, transform: `scale(${s * (1 + k * 0.05 * (f / 11))})`, opacity: k === 0 ? 1 : 0.22}} />)}
  </AbsoluteFill>);
};
const S08 = () => {
  const f = useCurrentFrame(); const q = interpolate(f, [0, 7], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return (<AbsoluteFill><Base n="08" style={{transform: `scale(${1.35 - 0.35 * q})`, filter: `blur(${(1 - q) * 10}px)`}} /></AbsoluteFill>);
};
// 09 cover story: magazine title behind his head
const S09 = () => {
  const f = useCurrentFrame();
  const word = (w: string, t0: number, top: number) => (
    <div style={{position: 'absolute', left: 0, right: 0, top, textAlign: 'center', font: '900 300px PF', color: '#fff', letterSpacing: '.02em', lineHeight: 1, textShadow: '0 12px 40px rgba(0,0,0,.25)'}}>
      {w.split('').map((c, i) => { const s = useSpring(t0 + i * 2, {damping: 12, stiffness: 180, mass: 0.6}); return <span key={i} style={{display: 'inline-block', transform: `translateY(${(1 - s) * 120}px)`, opacity: Math.min(1, s * 1.5)}}>{c}</span>; })}
    </div>);
  return (<AbsoluteFill>
    <Base n="09" style={{transform: `scale(${interpolate(f, [0, 51], [1, 1.06])})`}} />
    {word('YOUR', 5, 380)}{word('TRIP', 33, 660)}
    <Cut n="09" style={{transform: `scale(${interpolate(f, [0, 51], [1, 1.06])})`}} />
  </AbsoluteFill>);
};
// 10 frame break: he reaches out of the reel frame
const S10 = () => {
  const f = useCurrentFrame(); const p = useSpring(0, {damping: 16, stiffness: 110, mass: 0.8});
  const r = {x0: 142 * p, y0: 225 * p, x1: W - 142 * p, y1: H - 330 * p};
  const follow = f >= 110; const fs = useSpring(110);
  return (<AbsoluteFill style={{background: '#000'}}>
    <Base n="10" style={{filter: 'blur(26px) brightness(.4)', transform: 'scale(1.1)'}} />
    <div style={{position: 'absolute', left: r.x0, top: r.y0, width: r.x1 - r.x0, height: r.y1 - r.y0, borderRadius: 44 * p, overflow: 'hidden', border: `${6 * p}px solid #fff`, boxShadow: '0 30px 90px rgba(0,0,0,.6)'}}>
      <Base n="10" style={{left: -r.x0, top: -r.y0}} />
      <div style={{position: 'absolute', right: 26, bottom: 170, opacity: p, display: 'flex', flexDirection: 'column', gap: 34, alignItems: 'center', color: '#fff', font: '600 26px Inter', textShadow: '0 2px 8px #000'}}>
        {[['♥', '12.4K'], ['💬', '1,024'], ['➤', '']].map(([i, l]) => <div key={i} style={{textAlign: 'center'}}><div style={{fontSize: 60}}>{i}</div>{l}</div>)}</div>
      <div style={{position: 'absolute', left: 30, bottom: 40, display: 'flex', alignItems: 'center', gap: 16, font: '700 34px Inter', color: '#fff', textShadow: '0 2px 8px #000', opacity: p}}>
        <span style={{width: 62, height: 62, borderRadius: 31, background: BR, display: 'grid', placeItems: 'center'}}>C</span>steven_chinapal
        <span style={{border: '3px solid #fff', borderRadius: 14, padding: '4px 18px', fontSize: 28, background: follow ? 'rgba(255,255,255,.25)' : 'transparent', transform: `scale(${follow ? 1 + 0.15 * (1 - fs) : 1})`}}>{follow ? 'Following' : 'Follow'}</span></div>
    </div>
    <Cut n="10" style={{clipPath: `inset(0 0 ${H - r.y1}px 0)`}} />
    <Caption small="comment" big="TRIP" smallAt={54} bigAt={73} top={1610} />
  </AbsoluteFill>);
};
const MAP: Record<string, React.FC> = {'01': S01, '02': S02, '03': S03, '04': S04, '05': S05, '06': S06, '07': S07, '08a': S08a, '08': S08, '09': S09, '10': S10};
export const Demo: React.FC = () => {
  let from = 0;
  return (<AbsoluteFill style={{background: '#000', fontFamily: 'Inter'}}>
    <style>{fontCss}</style>
    {SEG.map(([n, d]) => { const C = MAP[n]; const el = <Sequence key={n} from={from} durationInFrames={d}><C /></Sequence>; from += d; return el; })}
    <Audio src={staticFile('mix.wav')} />
  </AbsoluteFill>);
};
