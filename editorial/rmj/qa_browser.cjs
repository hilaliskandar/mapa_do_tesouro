const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const base = process.env.RMJ_QA_URL;
  assert(base && /^https:\/\//.test(base), 'RMJ_QA_URL precisa ser HTTPS');
  const out = 'build/rmj-qa';
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const viewport of [{width:1366,height:900,name:'desktop'},{width:390,height:844,name:'mobile'}]) {
      const page = await browser.newPage({viewport:{width:viewport.width,height:viewport.height},deviceScaleFactor:1});
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      const response = await page.goto(base, {waitUntil:'networkidle',timeout:45000});
      assert.equal(response.status(),200);
      await page.locator('#tr-cidade').selectOption('3525904');
      await page.locator('#tr-cidade').selectOption('REGIAO');
      await page.locator('#editorial-cidade').selectOption('3525904');
      await page.locator('#editorial-highlights [data-id="3524006"]').click();
      await page.locator('#editorial-cidade').selectOption('3525904');
      await page.locator('#sintese-cidade').selectOption('3525904');
      await page.locator('#legal-cidade').selectOption('3525904');
      await page.locator('#funcoes-cidade').selectOption('3525904');
      await page.locator('#conta-municipio').selectOption('3525904');
      await page.locator('#serie').selectOption('3525904');
      await page.locator('#sintese-cidade').selectOption('3508405');
      await page.locator('#constantes').click();
      await page.locator('#nominais').click();
      const observations = await page.evaluate(() => ({
        version: document.body.innerText.match(/Versão editorial 0\.\d+/)?.[0] || '',
        sections:document.querySelectorAll('section').length,
        jsContent:document.querySelector('#sintese-texto')?.textContent?.length || 0,
        historyRows:document.querySelectorAll('#historical-table tbody tr').length,
        editorialProfiles:document.querySelectorAll('#editorial-highlights [data-id]').length,
        trendRows:document.querySelectorAll('#tr-table tbody tr').length,
        trendText:document.querySelector('#tr-analysis')?.textContent?.length || 0,
        editorialText:document.querySelector('#editorial-story')?.textContent?.length || 0,
        annualRows:document.querySelectorAll('#real-table tbody tr').length,
        legalRows:document.querySelectorAll('#legal-table tbody tr').length,
        overflow:document.documentElement.scrollWidth>window.innerWidth,
        width:window.innerWidth,
        scrollWidth:document.documentElement.scrollWidth
      }));
      assert.equal(observations.historyRows,5);
      assert.equal(observations.editorialProfiles,7);
      assert.equal(observations.trendRows,5);
      assert(observations.trendText>150);
      assert(observations.editorialText>250);
      assert.equal(observations.annualRows,5);
      assert.equal(observations.legalRows,4);
      assert(observations.jsContent>100);
      assert(!observations.overflow, 'overflow horizontal na largura '+viewport.width);
      assert.deepEqual(errors,[]);
      await page.screenshot({path:path.join(out,'rmj-'+viewport.name+'.png'),fullPage:true});
      results.push({...viewport,...observations,errors});
      await page.close();
    }
    fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));
    console.log(JSON.stringify(results,null,2));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
