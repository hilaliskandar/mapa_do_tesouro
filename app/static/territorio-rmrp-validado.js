"use strict";
const source="./data/api/v3/investimentos/rmrp/territorio-validado.json";
const select=document.getElementById("sub"),input=document.getElementById("q"),rows=document.getElementById("rows"),status=document.getElementById("status");
let catalog;
function render(){
 if(!catalog)return;
 const s=select.value,q=input.value.toLocaleLowerCase("pt-BR").trim();
 const items=catalog.municipios.filter(v=>(!s||v.sub_regiao===s)&&(!q||(v.municipio+" "+v.codigo_ibge).toLocaleLowerCase("pt-BR").includes(q)));
 rows.replaceChildren();
 for(const v of items){
  const tr=document.createElement("tr");
  for(const value of [v.municipio,v.codigo_ibge,v.sub_regiao]){const td=document.createElement("td");td.textContent=value;tr.appendChild(td)}
  rows.appendChild(tr);
 }
 status.textContent=items.length+" de "+catalog.total_municipios+" municípios encontrados.";
}
fetch(source,{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(data=>{
 if(data.metadata.qa_status!=="validado_dimensao_territorial_sem_homologacao_financeira"||data.total_municipios!==34||data.municipios.length!==34||data.sub_regioes.length!==4)throw Error("Contrato territorial inválido");
 catalog=data;
 for(const v of data.sub_regioes){const option=document.createElement("option");option.value=v.nome;option.textContent=v.nome+" ("+v.municipios+")";select.appendChild(option)}
 select.addEventListener("change",render);input.addEventListener("input",render);render();
}).catch(error=>{status.textContent="Falha na consulta ao catálogo territorial: "+error.message});
