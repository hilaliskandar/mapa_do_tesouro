"""Freeze candidate project IDs and collect missing planned values without RMRP repeat."""
import argparse,csv,json,hashlib,collections,concurrent.futures
from pathlib import Path
from pipeline.acquire.inv_sp645_proponent_obrasgov_regional_coverage import read,LAYOUT
from pipeline.acquire.inv_sp645_transferegov_new_source_layout import acquire
from pipeline.acquire.collect_rmrp_obrasgov_planned_values import fetch_one
p=argparse.ArgumentParser();p.add_argument("--out",type=Path,required=True);p.add_argument("--limit",type=int,default=100);a=p.parse_args()
root=a.out;root.mkdir(parents=True,exist_ok=True)
with open("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv",encoding="utf-8-sig") as f:geo={r["codigo_ibge"]:r for r in csv.DictReader(f,delimiter=";")}
assert len(geo)==645
with open("governance/controls/investimentos_sp645/RMRP_OBRASGOV_218_IDS_2026_11_17.csv",encoding="utf-8-sig") as f:prior={r["id_projeto_investimento"] for r in csv.DictReader(f)}
assert len(prior)==218
meta={}
for name in ("siconv_proposta","siconv_convenio","siconv_dados_obrasgov_geral"):
    path,meta[name]=acquire(root,name,650)
proposals={}
for r in read(root/"siconv_proposta.zip",LAYOUT["siconv_proposta"]):
    code=r["COD_MUNIC_IBGE"].strip();k=r["ID_PROPOSTA"].strip()
    if code not in geo or not k:continue
    assert r["UF_PROPONENTE"].strip()=="SP"
    assert k not in proposals or proposals[k]==code
    proposals[k]=code
conv={}
for r in read(root/"siconv_convenio.zip",LAYOUT["siconv_convenio"]):
    code=proposals.get(r["ID_PROPOSTA"].strip());k=r["NR_CONVENIO"].strip()
    if not code or not k:continue
    assert k not in conv or conv[k]==code
    conv[k]=code
projects=collections.defaultdict(set)
for r in read(root/"siconv_dados_obrasgov_geral.zip",LAYOUT["siconv_dados_obrasgov_geral"]):
    code=conv.get(r["nr_instrumento"].strip());pid=r["id_projeto_investimento"].strip()
    if code and pid:projects[pid].add(code)
ambiguous={k:sorted(v) for k,v in projects.items() if len(v)>1}
valid={k:next(iter(v)) for k,v in projects.items() if len(v)==1}
pending=sorted(set(valid)-prior,key=lambda k:(geo[valid[k]]["rm_au_nome"]!="Região Metropolitana de Ribeirão Preto",valid[k],k))
inventory={"sources":meta,"proposals":len(proposals),"convenios":len(conv),"projects":valid,"ambiguous":ambiguous,"previous_rmrp_ids":sorted(prior),"previous_ids_not_in_current":sorted(prior-set(valid)),"pending_ids":pending,"territorial_role":"proponent","publication_authorized":False}
(root/"inventory.json").write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
selected=pending[:a.limit]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch_one,selected))
assert [r["id_projeto_investimento"] for r in rows]==selected
for r in rows:r["codigo_ibge_proponente"]=valid[r["id_projeto_investimento"]]
(root/"values.json").write_text(json.dumps(rows,ensure_ascii=False))
summary={"municipalities_in_roster":645,"municipalities_with_linked_projects":len(set(valid.values())),"linked_projects":len(valid),"ambiguous_projects":len(ambiguous),"previous_ids_reused":len(set(valid)&prior),"pending_projects":len(pending),"pilot_requested":len(selected),"pilot_status":dict(collections.Counter(r["estado"] for r in rows)),"projects_with_planned_values":sum(bool(r.get("investimentos_previstos")) for r in rows),"publication_authorized":False}
(root/"qa.json").write_text(json.dumps(summary,indent=2))
print("OBRAS_SP645_QA",json.dumps(summary),flush=True)
for name in meta:(root/(name+".zip")).unlink()
