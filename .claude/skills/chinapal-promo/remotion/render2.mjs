import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
const browserExecutable='/opt/pw-browsers/chromium';
const [id,mode,...fr]=process.argv.slice(2);
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const comp=await selectComposition({serveUrl,id,browserExecutable});
console.log(id,'frames',comp.durationInFrames,(comp.durationInFrames/24).toFixed(2)+'s');
if(mode==='stills'){for(const f of fr.map(Number)){await renderStill({composition:comp,serveUrl,output:`stills/${id}_${f}.png`,frame:f,browserExecutable});}console.log('stills done');}
else{await renderMedia({composition:comp,serveUrl,codec:'h264',outputLocation:`out/${id}.mp4`,browserExecutable,concurrency:3,crf:18});console.log('done');}
