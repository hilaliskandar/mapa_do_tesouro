"use strict";
const el=id=>document.getElementById(id);
const brl=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});
let current=null;
function clearNode(node){while(node.firstChild)node.removeChild(node.firstChild)}
function status(message,error=false){el("status").textContent=message;el("status").className=error?"error":""}
function stages(data){return Array.from(new Set([...data.programas,...data.acoes].map(r=>r.estagio))).sort()}
function aggregate(data,stage,level,filter){
 const out=new Map(),words=filter.toLocaleLowerCase("pt-BR");
 for(const r of data[level]){
  if(r.estagio!==stage)continue;
  if(![r.ds_programa,r.ds_acao||""].join(" ").toLocaleLowerCase("pt-BR").includes(words))continue;
  const label=[r.orgao,r.cd_programa,r.ds_programa,level==="acoes"?r.cd_acao:"",level==="acoes"?r.ds_acao:""];
  const key=JSON.stringify(label);const current=out.get(key);
  if(!Number.isSafeInteger(r.valor_centavos))throw Error("Valor fora do intervalo seguro");
  const cents=(current?.cents||0)+r.valor_centavos;
  if(!Number.isSafeInteger(cents))throw Error("Total excede precisão segura");
  out.set(key,{label,cents});
 }
 return [...out.values()].sort((a,b)=>b.cents-a.cents);
}
function render(){
 if(!current)return;
 const selected=el("estagio").value;
 const rows=aggregate(current,selected,el("nivel").value,el("filtro").value.trim());
 const body=el("resultado");clearNode(body);
 let total=0;
 for(const entry of rows){
  const tr=document.createElement("tr");
  const texts=[entry.label[0],entry.label[1]+" — "+entry.label[2],entry.label[4]?entry.label[3]+" — "+entry.label[4]:"—",brl.format(entry.cents/100)];
  for(const txt of texts){const td=document.createElement("td");td.textContent=txt;tr.appendChild(td)}
  body.appendChild(tr);total+=entry.cents;
 }
 el("total").textContent=`${rows.length} registros agregados • R$ ${brl.format(total/100)} • ${selected}`;
 status("Consulta concluída.");
}
async function load(){
 const code=el("municipio").value.trim(),year=el("ano").value;
 if(!/^35\d{5}$/.test(code)){status("Informe um código IBGE válido de município paulista.",true);return}
 status("Consultando dados auditados...");current=null;clearNode(el("resultado"));
 const path=`./data/api/v2/tcesp/${year}/municipios/${code}.json`;
 try{
  const response=await fetch(path,{cache:"no-store"});
  if(!response.ok)throw Error(`HTTP ${response.status}`);
  const data=await response.json();
  if(data.codigo_ibge!==code||data.ano!==Number(year)||!Array.isArray(data.programas)||!Array.isArray(data.acoes))throw Error("Contrato de dados incompatível");
  current=data;
  const names=stages(data);clearNode(el("estagio"));
  for(const name of names){const option=document.createElement("option");option.value=name;option.textContent=name;el("estagio").appendChild(option)}
  el("estagio").value=names.includes("valor liquidado")?"valor liquidado":names[0];
  render();
 }catch(err){status(`Dados não disponíveis ou inválidos: ${err.message}`,true)}
}
el("consultar").addEventListener("click",load);
for(const key of ["estagio","nivel"])el(key).addEventListener("change",render);
el("filtro").addEventListener("input",render);
load();
