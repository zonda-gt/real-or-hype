// usage: node up.js <share_link> <file> [<file>...]   Uploads files into the shared OneDrive folder via its web UI.
const { chromium } = require('playwright');
(async () => {
  const [link, ...files] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.goto(link, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(10000);
  await p.getByText('Create or upload', { exact: false }).first().click();
  await p.waitForTimeout(1500);
  const [chooser] = await Promise.all([
    p.waitForEvent('filechooser', { timeout: 20000 }),
    p.getByText(/^Files? upload$/i).first().click(),
  ]);
  await chooser.setFiles(files);
  // wait until each file name shows up in the list (or timeout)
  const names = files.map(f => f.split('/').pop());
  const t0 = Date.now(); let ok = false;
  while (Date.now() - t0 < 30*60*1000) {
    await p.waitForTimeout(5000);
    const txt = await p.evaluate(() => document.body.innerText);
    if (/upload(ed)? failed|couldn't upload|can't upload/i.test(txt)) { console.log('FAILED:', txt.match(/.{0,80}(failed|couldn't|can't).{0,80}/i)?.[0]); break; }
    if (names.every(n => txt.includes(n)) && !/Uploading|remaining/i.test(txt)) { ok = true; break; }
  }
  await p.screenshot({ path: 'after_upload.png' });
  console.log(ok ? 'UPLOADED ' + names.join(', ') : 'NOT CONFIRMED');
  await b.close();
})();
