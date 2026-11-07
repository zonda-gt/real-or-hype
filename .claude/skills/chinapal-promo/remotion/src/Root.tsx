import React from 'react';
import {Composition} from 'remotion';
import {Demo, TOTAL} from './Demo';
export const Root: React.FC = () => (
  <Composition id="ChinaPal" component={Demo} durationInFrames={TOTAL} fps={24} width={1080} height={1920} />
);
