import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {EDL, wf, Vertigo, CafeClip, fontCss, PhoneHold, Checklist, Orbit, RouteGrow, StopScreen, CoverStory, FrameBreak, CouchWall, UIWorld, PullBackReveal, CommentCTA} from './Fx';
type Step = {len: number; el: React.ReactNode};
const fr = (id: string) => EDL[id]?.frames ?? 24;
const HL = {hours: [0.041, 0.581, 0.393, 0.617] as [number, number, number, number], map: [0.036, 0.746, 0.964, 0.89] as [number, number, number, number], tip: [0.036, 0.639, 0.964, 0.73] as [number, number, number, number]};
export const S2: Step[] = [
  {len: fr('s2_1_hold'), el: <PhoneHold id="s2_1_hold" src="B_sunburst.png" />},
  {len: fr('s2_2_check'), el: <Checklist id="s2_2_check" items={['Save reels', 'Send them to @steven_chinapal', 'Get your trip back']} ticks={[wf('s2_2_check', 'reels') + 4, wf('s2_2_check', 'me') + 3, wf('s2_2_check', 'back') + 2]} />},
  {len: fr('s2_3_orbit'), el: <Orbit id="s2_3_orbit" keys={['cafes']} />},
  {len: fr('s2_4_route'), el: <RouteGrow id="s2_4_route" at={[1, wf('s2_4_route', 'map'), wf('s2_4_route', 'right'), wf('s2_4_route', 'order'), wf('s2_4_route', 'with')]} tipAt={wf('s2_4_route', 'tips')} keys={['map', 'tips']} />},
  {len: 18, el: <StopScreen />},
  {len: fr('s2_5_cover'), el: <CoverStory id="s2_5_cover" yourAt={wf('s2_5_cover', 'your')} words={[{text: 'REELS', at: wf('s2_5_cover', 'reels')}, {text: 'TRIP', at: wf('s2_5_cover', 'trip')}]} />},
  {len: fr('s2_6_cta'), el: <FrameBreak id="s2_6_cta" keys={['reel']} followAt={Math.max(10, fr('s2_6_cta') - 8)} />},
];
export const S3: Step[] = [
  {len: fr('s3_1_offer'), el: <FrameBreak id="s3_1_offer" keys={['saved', 'china']} />},
  {len: fr('s3_2_wall'), el: <CouchWall id="s3_2_wall" keys={['forgot']} />},
  {len: fr('s3_3_dm'), el: <UIWorld id="s3_3_dm" fly={[1, 6, 11]} replyAt={Math.max(18, fr('s3_3_dm') - 12)} keys={['dm']} />},
  {len: fr('s3_4_plan'), el: <PullBackReveal id="s3_4_plan" src="A_sunburst.png" keys={['daily']} />},
  {len: fr('s3_5_tips'), el: <StopScreen voice="s3_5_tips" capId="s3_5_tips" keys={['hours', 'routes', 'tips']} hl={[{at: wf('s3_5_tips', 'hours'), r: HL.hours}, {at: wf('s3_5_tips', 'routes'), r: HL.map}, {at: wf('s3_5_tips', 'tips'), r: HL.tip}]} />},
  {len: fr('s3_6_cta'), el: <CommentCTA id="s3_6_cta" word="REEL" typeAt={Math.max(2, wf('s3_6_cta', 'reel') - 2)} />},
];
export const S1: Step[] = [
  {len: fr('v1_01_wall'), el: <CouchWall id="v1_01_wall" keys={['hundreds']} />},
  {len: fr('v1_02_orbit'), el: <Orbit id="v1_02_orbit" keys={['cafe']} />},
  {len: fr('v1_03_vertigo'), el: <Vertigo id="v1_03_vertigo" keys={['none']} />},
  {len: fr('v1_04_dm'), el: <UIWorld id="v1_04_dm" fly={[1, 7, 13]} replyAt={Math.max(20, fr('v1_04_dm') - 14)} keys={['all']} />},
  {len: fr('v1_05_check'), el: <Checklist id="v1_05_check" items={['Save the reel', 'Send it to @steven_chinapal', 'Get your trip']} ticks={[wf('v1_05_check', 'reel') + 4, wf('v1_05_check', 'me') + 3, wf('v1_05_check', 'that') + 2]} />},
  {len: fr('v1_06_plan'), el: <PullBackReveal id="v1_06_plan" src="A_sunburst.png" keys={['day-by-day']} />},
  {len: fr('v1_07_route'), el: <RouteGrow id="v1_07_route" at={[1, wf('v1_07_route', 'cafe'), wf('v1_07_route', 'then'), wf('v1_07_route', 'garden'), wf('v1_07_route', 'dinner')]} keys={['cafe', 'garden', 'dinner']} />},
  {len: 12, el: <StopScreen />},
  {len: Math.min(30, fr('v1_08_cafe')), el: <CafeClip id="v1_08_cafe" />},
  {len: fr('v1_09_cover'), el: <CoverStory id="v1_09_cover" yourAt={wf('v1_09_cover', 'that')} words={[{text: 'TRIP', at: wf('v1_09_cover', 'trip')}]} />},
  {len: fr('v1_10_cta'), el: <FrameBreak id="v1_10_cta" keys={['saved', 'reel']} followAt={Math.max(10, fr('v1_10_cta') - 10)} />},
];
export const total = (s: Step[]) => s.reduce((a, b) => a + b.len, 0);
export const Video: React.FC<{steps: 'S1' | 'S2' | 'S3'}> = ({steps}) => {
  const st = steps === 'S1' ? S1 : steps === 'S2' ? S2 : S3; let from = 0;
  return (<AbsoluteFill style={{background: '#000', fontFamily: 'Inter'}}><style>{fontCss}</style>
    {st.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.len}>{s.el}</Sequence>; from += s.len; return el; })}</AbsoluteFill>);
};
