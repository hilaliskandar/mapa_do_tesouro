#!/usr/bin/env python3
"""Triagem de itens do Plano de Aplicacao Detalhado da RMRP por ID_PROPOSTA.
Nao homologa investimento, valores ou execucao. NAO escreve no SQLite/R2.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from inv_rmrp_transferegov_join import download, rows, REFERENCE

def category(v):
    norm="".join(c for c in (v or "") if c.isdigit())
    # Nomenclatura brasileira de natureza da despesa: categoria economica 3 = corrente,
    # 4 = capital. So triagem quando estrutura de codigo identificavel.
    if len(norm)>=6 and norm[:2]=="44":
        return "candidato_investimento_gnd4"
    if len(norm)>=6 and norm[:2]=="45":
        return "capital_inversao_financeira_gnd5"
    if len(norm)>=6 and norm[:2]=="46":
        return "capital_amortizacao_divida_gnd6"
    if len(norm)>=6 and norm[0]=="4":
        return "capital_outro_ou_inconsistente"
    if len(norm)>=6 and norm[0]=="3":
        return "candidato_corrente"
    return "indeterminado"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out-dir",required=True);ap.add_argument("--reference",default=REFERENCE);ap.add_argument("--timeout",type=int,default=300)
    args=ap.parse_args();out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    names={str(r["ibge7"]):r["municipio"] for r in json.loads(Path(args.reference).read_text(encoding="utf-8"))["municipalities"]}
    if len(names)!=34:raise RuntimeError("municipios expected 34")
    manifest={"status":"in_progress","timestamp_utc":datetime.now(timezone.utc).isoformat(),"source_system":"Transferegov",
              "method":"ID_PROPOSTA -> COD_MUNIC_IBGE; COD_NATUREZA_DESPESA category candidate only",
              "files":[],"coverage":{},"errors":[]}
    def persist(): (out/"manifest_plano.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
    persist()
    try:
        for setname in ("siconv_proposta","siconv_plano_aplicacao_detalhado"):
            d=download(out,setname,args.timeout);manifest["files"].append(d);persist()
        ds={x["name"]:x for x in manifest["files"]}
        proponent={};proposals=Counter()
        for h,reader in rows(ds["siconv_proposta"]["path"],ds["siconv_proposta"]["csv_member"]):
            if not {"ID_PROPOSTA","COD_MUNIC_IBGE","UF_PROPONENTE"}.issubset(h):raise RuntimeError("proposal schema changed")
            for row in reader:
                ib=(row["COD_MUNIC_IBGE"] or "").strip()
                if ib not in names: continue
                if (row["UF_PROPONENTE"] or "").strip().upper()!="SP":raise RuntimeError("IBGE UF mismatch")
                key=(row["ID_PROPOSTA"] or "").strip()
                if not key or (key in proponent and proponent[key]!=ib): raise RuntimeError("ambiguous proposal code")
                proponent[key]=ib;proposals[ib]+=1
        assert sum(proposals.values())>=6410, "new source coverage below reference smoke"
        municipal=defaultdict(Counter); codes=Counter();categories=Counter(); loc_uf=Counter()
        count_national=count_selected=0;unique_item=set();duplicate_item=0;blank_item=0;statuses=Counter();unknown_codes=Counter();foreign_examples=[]
        with (out/"plano_rmrp_itens_nao_homologados.csv").open("w",encoding="utf-8",newline="") as dest:
            for h,reader in rows(ds["siconv_plano_aplicacao_detalhado"]["path"],ds["siconv_plano_aplicacao_detalhado"]["csv_member"]):
                required={"ID_PROPOSTA","ID_ITEM_PAD","COD_NATUREZA_DESPESA","NATUREZA_DESPESA","VALOR_TOTAL_ITEM","SIGLA","MUNICIPIO"}
                if not required.issubset(h):raise RuntimeError("plan schema changed: "+str(required-set(h)))
                writer=csv.DictWriter(dest,fieldnames=["__ibge7_proponente","__classificacao_provisoria"]+h,delimiter=";");writer.writeheader()
                for row in reader:
                    count_national+=1
                    code=(row.get("ID_PROPOSTA") or "").strip()
                    ib=proponent.get(code)
                    if not ib:continue
                    cat=category(row.get("COD_NATUREZA_DESPESA"))
                    writer.writerow({"__ibge7_proponente":ib,"__classificacao_provisoria":cat,**row})
                    count_selected+=1;categories[cat]+=1;municipal[ib][cat]+=1
                    codes[(row.get("COD_NATUREZA_DESPESA") or "").strip()]+=1
                    statuses[(row.get("SIT_ITEM") or "").strip()]+=1
                    if cat=="indeterminado":unknown_codes[(row.get("COD_NATUREZA_DESPESA") or "").strip()]+=1
                    if (row.get("SIGLA") or "").strip().upper()!="SP" and len(foreign_examples)<20:
                        foreign_examples.append({"ibge_proponente":ib,"id_proposta":code,"uf_item":row.get("SIGLA"),"municipio_item":row.get("MUNICIPIO"),"id_item":row.get("ID_ITEM_PAD")})
                    loc_uf[(row.get("SIGLA") or "").strip().upper()]+=1
                    item=(row.get("ID_ITEM_PAD") or "").strip()
                    if not item:blank_item+=1
                    elif item in unique_item:duplicate_item+=1
                    else:unique_item.add(item)
        manifest["coverage"]={
            "national_plan_items":count_national,"rmrp_proponent_proposals":len(proponent),
            "linked_plan_items":count_selected,"proponent_municipalities_with_any_item":sum(bool(x) for x in municipal.values()),
            "category_counts":dict(categories),"top_nature_codes":codes.most_common(50),
            "item_status_counts":dict(statuses),"unknown_nature_codes":dict(unknown_codes),"foreign_item_examples":foreign_examples,
            "item_location_uf_counts":dict(loc_uf),"duplicate_ID_ITEM_PAD_rows":duplicate_item,
            "blank_ID_ITEM_PAD_rows":blank_item,
            "municipalities":{ib:{"name":names[ib],"proposals":proposals[ib],"plan_items":dict(municipal[ib])} for ib in names}
        }
        manifest["cautions"]=["Classificacao provisoria por categoria economica e grupo de natureza da despesa (GND 4, 5, 6).",
            "Nao somar VALOR_TOTAL_ITEM sem auditar duplicidades, situacao e revisoes.",
            "Nao equiparar planejado a empenhado, desembolsado, aplicado ou liquidado.",
            "SIGLA/MUNICIPIO identifica local indicado no item, pode divergir do proponente.",
            "ID_ITEM_PAD pode ter relacoes de versao/linhas repetidas: revisao antes de deduplicar."]
        manifest["status"]="preliminar_plano_classificado_nao_homologado";persist()
        print(json.dumps({"status":manifest["status"],"coverage":{k:v for k,v in manifest["coverage"].items() if k!="municipalities"}},ensure_ascii=False),flush=True)
    except Exception as e:
        manifest["status"]="error";manifest["errors"].append(str(e));persist();raise
if __name__=="__main__":main()
