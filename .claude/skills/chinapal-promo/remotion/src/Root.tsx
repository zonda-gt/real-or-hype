import React from 'react';
import {Composition} from 'remotion';
import {Demo, TOTAL} from './Demo';
import {Video, S1, S2, S3, R1, R2, R3, total} from './Scripts';
export const Root: React.FC = () => (<>
  <Composition id="ChinaPal" component={Demo} durationInFrames={TOTAL} fps={24} width={1080} height={1920} />
  <Composition id="Script1" component={Video} defaultProps={{steps: 'S1' as const}} durationInFrames={total(S1)} fps={24} width={1080} height={1920} />
  <Composition id="Script2" component={Video} defaultProps={{steps: 'S2' as const}} durationInFrames={total(S2)} fps={24} width={1080} height={1920} />
  <Composition id="Script3" component={Video} defaultProps={{steps: 'S3' as const}} durationInFrames={total(S3)} fps={24} width={1080} height={1920} />
  <Composition id="Real1" component={Video} defaultProps={{steps: 'R1' as const}} durationInFrames={total(R1)} fps={24} width={1080} height={1920} />
  <Composition id="Real2" component={Video} defaultProps={{steps: 'R2' as const}} durationInFrames={total(R2)} fps={24} width={1080} height={1920} />
  <Composition id="Real3" component={Video} defaultProps={{steps: 'R3' as const}} durationInFrames={total(R3)} fps={24} width={1080} height={1920} />
</>);
