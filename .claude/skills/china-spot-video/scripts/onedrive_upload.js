// Upload files into a OneDrive shared-folder link (edit link), optionally into a sub-folder it creates if missing.
// Same-name files are replaced.
// usage: node onedrive_upload.js <share_link> [--folder <name>] <file> [<file>...]
const { chromium } = require('playwright');
(async () => {
  const args = process.argv.slice(2); const link = args.shift();
  let folder = null; if (args[0] === '--folder') { args.shift(); folder = args.shift(); }
  const files = args;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const body = () => p.evaluate(() => document.body.innerText);
  await p.goto(link, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(10000);
  if (folder) {
    const row = p.locator(`[role="row"] :text-is("${folder}"), button:text-is("${folder}")`).first();
    if (!(await row.count())) {
      await p.getByText('Create or upload').first().click(); await p.waitForTimeout(1200);
      await p.getByText(/^Folder$/).first().click(); await p.waitForTimeout(1500);
      const input = p.locator('input[type="text"]').last();
      await input.fill(folder); await p.waitForTimeout(500);
      await p.getByRole('button', { name: /^Create$/ }).first().click();
      await p.waitForTimeout(6000);
      console.log('created folder', folder);
    }
    await p.locator(`:text-is("${folder}")`).first().click();
    await p.waitForTimeout(8000);
    const crumbs = await body();
    if (!crumbs.includes(folder)) throw new Error('could not open folder ' + folder);
  }
  if (!files.length) { console.log('no files'); await b.close(); return; }
  await p.getByText('Create or upload').first().click(); await p.waitForTimeout(1500);
  const [chooser] = await Promise.all([p.waitForEvent('filechooser', { timeout: 20000 }), p.getByText(/^Files? upload$/i).first().click()]);
  await chooser.setFiles(files);
  // same-name files: OneDrive asks whether to replace; always replace
  for (let i = 0; i < 20; i++) {
    await p.waitForTimeout(1500);
    const rep = p.getByRole('button', { name: /^Replace( all)?$/i }).first();
    if (await rep.count()) { await rep.click(); console.log('replacing existing file(s)'); }
    else if (i > 3) break;
  }
  const names = files.map(f => f.split('/').pop()); const t0 = Date.now(); let ok = false;
  while (Date.now() - t0 < 60*60*1000) {
    await p.waitForTimeout(5000);
    const txt = await body();
    if (/upload(ed)? failed|couldn't upload|can't upload/i.test(txt)) { console.log('FAILED'); break; }
    if (names.every(n => txt.includes(n)) && !/Uploading|remaining|Preparing/i.test(txt)) { ok = true; break; }
  }
  await p.screenshot({ path: process.env.SHOT || '/tmp/onedrive_after.png' });
  console.log(ok ? 'UPLOADED ' + names.join(', ') + (folder ? ' -> ' + folder : '') : 'NOT CONFIRMED');
  await b.close();
})().catch(e => { console.error('ERROR', e.message); process.exit(1); });
