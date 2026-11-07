import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {EDL, fontCss, PhoneHold, Checklist, Orbit, RouteGrow, StopScreen, CoverStory, FrameBreak, CouchWall, UIWorld, PullBackReveal, CommentCTA} from './Fx';
type Step = {len: number; el: React.ReactNode};
const fr = (id: string) => EDL[id]?.frames ?? 24;
const HL = {hours: [0.041, 0.581, 0.393, 0.617] as [number, number, number, number], map: [0.036, 0.746, 0.964, 0.89] as [number, number, number, number], tip: [0.036, 0.639, 0.964, 0.73] as [number, number, number, number]};
export const S2: Step[] = [
  {len: fr('s2_1_hold'), el: <PhoneHold id="s2_1_hold" src="B_sunburst.png" />},
  {len: fr('s2_2_check'), el: <Checklist id="s2_2_check" items={['Save reels', 'Send them to @steven_chinapal', 'Get your trip back']} ticks={[14, 45, 68]} />},
  {len: fr('s2_3_orbit'), el: <Orbit id="s2_3_orbit" keys={['cafes']} />},
  {len: fr('s2_4_route'), el: <RouteGrow id="s2_4_route" at={[2, 17, 30, 43, 55]} tipAt={70} keys={['map', 'tips']} />},
  {len: 18, el: <StopScreen />},
  {len: fr('s2_5_cover'), el: <CoverStory id="s2_5_cover" yourAt={2} words={[{text: 'REELS', at: 16}, {text: 'TRIP', at: 48}]} />},
  {len: fr('s2_6_cta'), el: <FrameBreak id="s2_6_cta" keys={['trip']} followAt={44} />},
];
export const S3: Step[] = [
  {len: fr('s3_1_offer'), el: <FrameBreak id="s3_1_offer" keys={['saved', 'china']} />},
  {len: fr('s3_2_wall'), el: <CouchWall id="s3_2_wall" keys={['forgot']} />},
  {len: fr('s3_3_dm'), el: <UIWorld id="s3_3_dm" fly={[2, 10, 18]} replyAt={34} keys={['dms']} />},
  {len: fr('s3_4_plan'), el: <PullBackReveal id="s3_4_plan" src="A_sunburst.png" keys={['day-by-day']} />},
  {len: fr('s3_5_tips'), el: <StopScreen voice="s3_5_tips" capId="s3_5_tips" keys={['hours', 'routes', 'tips']} hl={[{at: 25, r: HL.hours}, {at: 43, r: HL.map}, {at: 71, r: HL.tip}]} />},
  {len: fr('s3_6_cta'), el: <CommentCTA id="s3_6_cta" typeAt={14} />},
];
export const total = (s: Step[]) => s.reduce((a, b) => a + b.len, 0);
export const Video: React.FC<{steps: 'S2' | 'S3'}> = ({steps}) => {
  const st = steps === 'S2' ? S2 : S3; let from = 0;
  return (<AbsoluteFill style={{background: '#000', fontFamily: 'Inter'}}><style>{fontCss}</style>
    {st.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.len}>{s.el}</Sequence>; from += s.len; return el; })}</AbsoluteFill>);
};
