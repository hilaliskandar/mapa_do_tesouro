#!/usr/bin/env python3
"""Read-only verification of TCESP R2 objects for RMSJRP. No external re-collection."""
from __future__ import annotations
import collections
import csv
import hashlib
import json
import os
from pathlib import Path
from deployment.download_r2_source import download_r2_object

ROOT=Path("build/rmsjrp-r2-qa")
ROOT.mkdir(parents=True,exist_ok=True)
ids={}
with Path("editorial/rmsjrp/MUNICIPIOS_SUBREGIOES_2025.csv").open(encoding="utf-8",newline="") as f:
    for r in csv.DictReader(f,delimiter=";"):
        ids[r["cod_ibge"]]=r
assert len(ids)==37
prefixes={2023:"tcesp/estadual/despesas/2023/run_40263996213",2024:"tcesp/estadual/despesas/2024/run_40263996213",2025:"tcesp/estadual/despesas/2025/run_40262193781"}
account=os.environ["CLOUDFLARE_ACCOUNT_ID"]
token=os.environ["CLOUDFLARE_API_TOKEN"]
bucket=os.environ["CLOUDFLARE_R2_BUCKET"]
def fetch(key,path):
    download_r2_object(account_id=account,api_token=token,bucket=bucket,object_key=key,output=path)
    return hashlib.sha256(path.read_bytes()).hexdigest()
results=[]
manifest_evidence=[]
for year,prefix in prefixes.items():
    folder=ROOT/str(year)
    folder.mkdir(exist_ok=True)
    manifest_path=folder/"r2_manifest.json"
    manifest_sha=fetch(prefix+"/r2_manifest.json",manifest_path)
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["source_year"]==year
    assert manifest["qa_status"]=="pass"
    object_map={obj["name"]:obj for obj in manifest["objects"]}
    details=[]
    for name in ("investimentos_grupo44_por_municipio_mes_estagio.csv","investimentos_grupo44_por_programa.csv","investimentos_grupo44_por_acao.csv"):
        path=folder/name
        sha=fetch(prefix+"/"+name,path)
        assert sha==object_map[name]["sha256"],(year,name,sha,object_map[name]["sha256"])
        details.append({"object":name,"sha256":sha,"bytes":path.stat().st_size})
    aggregates=[]
    for name in ("investimentos_grupo44_por_municipio_mes_estagio.csv","investimentos_grupo44_por_programa.csv","investimentos_grupo44_por_acao.csv"):
        totals=collections.Counter()
        counts=collections.Counter()
        with (folder/name).open(encoding="utf-8",newline="") as f:
            reader=csv.DictReader(f)
            for row in reader:
                code=row["codigo_ibge"]
                if code not in ids:continue
                key=(code,row["estagio"])
                totals[key]+=int(row["centavos"])
                counts[key]+=1
        aggregates.append((totals,counts))
    assert aggregates[0][0]==aggregates[1][0]==aggregates[2][0],f"{year}: divergência entre níveis"
    for code in ids:
        for stage in ("valor empenhado","valor liquidado","valor pago"):
            key=(code,stage)
            observed=key in aggregates[0][0]
            results.append({"ano":year,"cod_ibge":code,"municipio":ids[code]["municipio"],"subregiao":ids[code]["subregiao_pdui"],"estagio":stage,"observado":int(observed),
            "linhas_mensais":aggregates[0][1][key],"linhas_programas":aggregates[1][1][key],"linhas_acoes":aggregates[2][1][key],
            "centavos":aggregates[0][0][key] if observed else ""})
    manifest_evidence.append({"year":year,"prefix":prefix,"manifest_sha256":manifest_sha,"objects":details})
with (ROOT/"MATRIZ_TCESP_RMSJRP_2023_2025.csv").open("w",encoding="utf-8",newline="") as f:
    wr=csv.DictWriter(f,fieldnames=results[0].keys(),delimiter=";")
    wr.writeheader()
    wr.writerows(results)
# Crosscheck against the immutable statewide DCA snapshot; never alter either source.
dca_key="sp_645/dca/2013_2025/normalized.csv"
dca_path=ROOT/"dca_sp645_canonical.csv"
dca_sha=fetch(dca_key,dca_path)
assert dca_sha=="67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5",dca_sha
dca_values={}
with dca_path.open(encoding="utf-8",newline="") as f:
    for row in csv.DictReader(f):
        if row["cod_ibge"] in ids and int(row["ano"]) in prefixes:
            value=row["dca_investimentos_liquidada"]
            dca_values[(int(row["ano"]),row["cod_ibge"])]=round(float(value)*100) if value else None
comparisons=[]
for row in results:
    if row["estagio"]!="valor liquidado":continue
    k=(row["ano"],row["cod_ibge"])
    dca=dca_values.get(k)
    tcesp=int(row["centavos"]) if row["observado"] else None
    comparisons.append({"ano":row["ano"],"cod_ibge":row["cod_ibge"],"dca_centavos":dca if dca is not None else "",
        "tcesp_centavos":tcesp if tcesp is not None else "",
        "diferenca_centavos":tcesp-dca if dca is not None and tcesp is not None else ""})
assert len(comparisons)==111
with (ROOT/"CONFRONTO_TCESP_DCA_2023_2025.csv").open("w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=comparisons[0].keys(),delimiter=";")
    writer.writeheader();writer.writerows(comparisons)
nonzero=[x for x in comparisons if x["diferenca_centavos"] not in ("",0)]
summary={"status":"pass","source":"TCESP_R2_approved","municipalities":37,"years":[2023,2024,2025],
 "pairs_expected":111,
 "liquidated_pairs_observed":sum(x["observado"] for x in results if x["estagio"]=="valor liquidado"),
 "rows":len(results),"manifest_evidence":manifest_evidence,"dca_r2_sha256":dca_sha,"dca_comparison_pairs":len(comparisons),"dca_discrepancies":len(nonzero),"dca_discrepancy_examples":nonzero[:20]}
(ROOT/"RESULTADO_TCESP_R2.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":summary["status"],"pairs_expected":111,"liquidated_pairs_observed":summary["liquidated_pairs_observed"],"years":summary["years"],"dca_comparison_pairs":summary["dca_comparison_pairs"],"dca_discrepancies":summary["dca_discrepancies"]}))
