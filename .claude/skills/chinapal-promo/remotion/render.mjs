import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
const browserExecutable='/opt/pw-browsers/chromium';
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const comp=await selectComposition({serveUrl,id:'ChinaPal',browserExecutable});
const mode=process.argv[2]||'video';
if(mode==='stills'){ for(const fr of process.argv.slice(3).map(Number)){ await renderStill({composition:comp,serveUrl,output:`stills/f${fr}.png`,frame:fr,browserExecutable}); console.log('still',fr);} }
else { await renderMedia({composition:comp,serveUrl,codec:'h264',outputLocation:'out/chinapal_demo_v2_remotion.mp4',browserExecutable,concurrency:3,crf:18,onProgress:({progress})=>{if(Math.round(progress*100)%10===0)process.stdout.write(Math.round(progress*100)+'% ');}}); console.log('done'); }
