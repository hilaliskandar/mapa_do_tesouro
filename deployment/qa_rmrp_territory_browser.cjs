"use strict";
const { chromium } = require("playwright");
(async () => {
  const base = process.env.RMRP_PREVIEW_URL || "https://sp645-rmrp-release.finbra-tic-tim-referencia.pages.dev";
  const browser = await chromium.launch({headless:true});
  try {
    for (const viewport of [{width:1280,height:800},{width:375,height:812}]) {
      const page=await browser.newPage({viewport});
      const errors=[];
      page.on("pageerror",err=>errors.push(err.message));
      const resp=await page.goto(base+"/territorio-rmrp-validado.html",{waitUntil:"domcontentloaded",timeout:45000});
      if (resp.status()!==200) throw Error("HTML HTTP "+resp.status());
      await page.waitForFunction(()=>document.querySelector("#status")?.textContent?.includes("34 municípios"),{timeout:35000});
      const rows=await page.locator("#rows tr").count();
      if(rows!==34)throw Error("Expected 34 rows, got "+rows);
      if(await page.locator("#sub option").count()!==5)throw Error("Expected 4 subregions");
      await page.locator("#sub").selectOption({label:"Sub-região de Batatais (7)"});
      if(await page.locator("#rows tr").count()!==7)throw Error("Batatais filter expected 7 municipalities");
      await page.locator("#sub").selectOption("");
      await page.locator("#q").fill("Ribeirão Preto");
      if(await page.locator("#rows tr").count()!==1)throw Error("Name search expected one match");
      const metrics=await page.evaluate(()=>({width:window.innerWidth,documentWidth:document.documentElement.scrollWidth}));
      if(metrics.documentWidth>metrics.width+2)throw Error("Unexpected horizontal page overflow "+JSON.stringify(metrics));
      if(errors.length)throw Error("Browser errors: "+errors.join("; "));
      console.log(JSON.stringify({status:"pass",viewport,rows:34,filtered:7,search:1}));
      await page.close();
    }
    const page=await browser.newPage();
    const jsonResp=await page.goto(base+"/data/api/v3/investimentos/rmrp/territorio-validado.json");
    if(jsonResp.status()!==200)throw Error("JSON HTTP "+jsonResp.status());
    const json=JSON.parse(await jsonResp.text());
    if(json.municipios?.length!==34||json.metadata?.qa_status!=="validado_dimensao_territorial_sem_homologacao_financeira")throw Error("JSON contract mismatch");
    console.log("RMRP_BROWSER_QA_PASS");
    await page.close();
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
