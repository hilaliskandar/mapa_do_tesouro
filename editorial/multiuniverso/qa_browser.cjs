const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
const root=path.resolve('build/editorial-universes');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
const browser=await chromium.launch({headless:true});
const results=[];
try{
for(const item of manifest.editions){
  for(const vp of [{name:'desktop',width:1366,height:900},{name:'mobile',width:390,height:844}]){
   const page=await browser.newPage({viewport:{width:vp.width,height:vp.height}});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   const uri='file://'+path.join(root,item.publication_id,'index.html');
   await page.goto(uri,{waitUntil:'load'});
   assert(await page.locator('h1').count()===1,'titulo ausente');
   assert(await page.locator('a[href="#fichas"]').count()===1,'navegacao ausente');
   const links=page.locator('a[href^="municipios/"]');
   assert.equal(await links.count(),item.member_count,'fichas nao listadas');
   assert(await page.locator('section').count()>=5,'conteudo insuficiente');
   const overview=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,sections:document.querySelectorAll('section').length}));
   assert(!overview.overflow,'overflow horizontal fora de tabelas');
   const first=links.first();
   const href=await first.getAttribute('href');
   await first.click();
   assert(page.url().endsWith(href),'ficha nao aberta');
   assert(await page.getByText('Mediana do grupo',{exact:false}).count()>0,'tabela ficha ausente');
   const profile=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,details:document.querySelectorAll('details').length}));
   assert(!profile.overflow,'overflow na ficha');
   assert(profile.details>0,'serie historica da ficha ausente');
   assert.deepEqual(errors,[],'erro no navegador');
   results.push({universe:item.publication_id,viewport:vp.name,overview,profile});
   await page.close();
  }
 }
 fs.mkdirSync('build/editorial-browser-qa',{recursive:true});
 fs.writeFileSync('build/editorial-browser-qa/results.json',JSON.stringify(results,null,2));
 console.log('Browser QA aprovado: '+results.length+' cenarios desktop/mobile');
}finally{await browser.close();}
})().catch(err=>{console.error(err);process.exit(1)});
