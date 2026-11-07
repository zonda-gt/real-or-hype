import React from 'react';
import {Composition} from 'remotion';
import {Demo, TOTAL} from './Demo';
import {Video, S2, S3, total} from './Scripts';
export const Root: React.FC = () => (<>
  <Composition id="ChinaPal" component={Demo} durationInFrames={TOTAL} fps={24} width={1080} height={1920} />
  <Composition id="Script2" component={Video} defaultProps={{steps: 'S2' as const}} durationInFrames={total(S2)} fps={24} width={1080} height={1920} />
  <Composition id="Script3" component={Video} defaultProps={{steps: 'S3' as const}} durationInFrames={total(S3)} fps={24} width={1080} height={1920} />
</>);
