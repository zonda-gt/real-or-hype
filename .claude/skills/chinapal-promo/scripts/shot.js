const {chromium}=require('playwright');
(async()=>{const jobs=JSON.parse(require('fs').readFileSync(process.argv[2]));
const b=await chromium.launch();
for(const j of jobs){const p=await b.newPage({viewport:{width:j.w,height:j.h},deviceScaleFactor:j.s||1});
await p.goto('file://'+j.html);await p.waitForTimeout(900);await p.screenshot({path:j.out,omitBackground:!!j.alpha});await p.close();console.log('shot',j.out);}
await b.close();})();
