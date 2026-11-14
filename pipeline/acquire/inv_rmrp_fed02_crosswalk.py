#!/usr/bin/env python3
"""INV-FED02: instrument-level overlap between PAD GND4 approved and disbursements.

All joins use explicit IDs. This does NOT allocate any financial amount to investment
nor assert a municipality is the physical site of expenditure. Read-only official ZIPs.
"""
from __future__ import annotations
import argparse,csv,json,hashlib,unicodedata
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
from inv_rmrp_transferegov_join import download,rows,REFERENCE

SETS=("siconv_proposta","siconv_convenio","siconv_desembolso","siconv_plano_aplicacao_detalhado")
def canon(value):
    s=unicodedata.normalize("NFKD",(value or "").strip().upper())
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).split())
def approved_gnd4(row):
    code="".join(c for c in (row.get("COD_NATUREZA_DESPESA") or "") if c.isdigit())
    return len(code)>=6 and code.startswith("44") and (row.get("SIT_ITEM") or "").strip().upper()=="APROVADO"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--timeout",type=int,default=300)
    ap.add_argument("--reference",default=REFERENCE)
    args=ap.parse_args()
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    ref=json.loads(Path(args.reference).read_text(encoding="utf-8"))
    names={str(v["ibge7"]):v["municipio"] for v in ref["municipalities"]}
    if len(names)!=34:raise RuntimeError("expected 34 IBGE municipalities")
    name_to_ib={canon(n):k for k,n in names.items()}
    if len(name_to_ib)!=34:raise RuntimeError("ambiguous municipal names")
    manifest={"created_at_utc":datetime.now(timezone.utc).isoformat(),"status":"in_progress",
              "sources":[],"qa":{},"errors":[]}
    def persist(): (out/"manifest_fed02.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    persist()
    try:
        for dataset in SETS:
            source=download(out,dataset,args.timeout)
            manifest["sources"].append(source);persist()
        files={x["name"]:x for x in manifest["sources"]}
        proposals={};conflict=set();proposal_rows=0;all_proposals=0
        for headers,reader in rows(files["siconv_proposta"]["path"],files["siconv_proposta"]["csv_member"]):
            if not {"ID_PROPOSTA","COD_MUNIC_IBGE","UF_PROPONENTE"}.issubset(headers):
                raise RuntimeError("proposal layout changed")
            for row in reader:
                all_proposals+=1
                ib=(row["COD_MUNIC_IBGE"] or "").strip()
                if ib not in names:continue
                if (row["UF_PROPONENTE"] or "").strip().upper()!="SP":raise RuntimeError("UF mismatch")
                prop=(row["ID_PROPOSTA"] or "").strip()
                if not prop:raise RuntimeError("missing RMRP proposal id")
                proposal_rows+=1
                if prop in proposals and proposals[prop]!=ib:conflict.add(prop)
                else:proposals[prop]=ib
        if conflict:raise RuntimeError(f"ambiguous proposals: {len(conflict)}")
        conv_to_proposal={};proposal_convs=defaultdict(set);conv_conflict=set()
        national_convs=linked_convs=0
        for headers,reader in rows(files["siconv_convenio"]["path"],files["siconv_convenio"]["csv_member"]):
            if not {"ID_PROPOSTA","NR_CONVENIO"}.issubset(headers):raise RuntimeError("convenio layout changed")
            for row in reader:
                national_convs+=1;prop=(row["ID_PROPOSTA"] or "").strip()
                if prop not in proposals:continue
                conv=(row["NR_CONVENIO"] or "").strip()
                if not conv:raise RuntimeError("missing matched NR_CONVENIO")
                linked_convs+=1
                if conv in conv_to_proposal and conv_to_proposal[conv]!=prop:conv_conflict.add(conv)
                conv_to_proposal[conv]=prop;proposal_convs[prop].add(conv)
        if conv_conflict:raise RuntimeError(f"conflicting convenio IDs: {len(conv_conflict)}")
        items_by_proposal=Counter();dest_by_proposal=defaultdict(Counter)
        national_pad=linked_pad=approved_items=0;seen_items=set()
        for headers,reader in rows(files["siconv_plano_aplicacao_detalhado"]["path"],files["siconv_plano_aplicacao_detalhado"]["csv_member"]):
            needed={"ID_PROPOSTA","ID_ITEM_PAD","COD_NATUREZA_DESPESA","SIT_ITEM","SIGLA","MUNICIPIO"}
            if not needed.issubset(headers):raise RuntimeError("PAD layout changed")
            for row in reader:
                national_pad+=1;prop=(row["ID_PROPOSTA"] or "").strip()
                if prop not in proposals:continue
                linked_pad+=1
                item=(row["ID_ITEM_PAD"] or "").strip()
                if not item or item in seen_items:raise RuntimeError("missing/duplicate item ID")
                seen_items.add(item)
                if not approved_gnd4(row):continue
                approved_items+=1;items_by_proposal[prop]+=1
                uf=(row["SIGLA"] or "").strip().upper()
                dst=name_to_ib.get(canon(row["MUNICIPIO"])) if uf=="SP" else None
                if dst:typ="rmrp_named";key=dst
                elif uf=="SP":typ="sp_not_rmrp";key=None
                else:typ="out_of_sp";key=None
                dest_by_proposal[prop][typ]+=1
                if dst and dst!=proposals[prop]:dest_by_proposal[prop]["cross_municipal_rmrp"]+=1
        national_dis=linked_dis=0;dis_by_conv=Counter();orphan_by_prop=Counter()
        for headers,reader in rows(files["siconv_desembolso"]["path"],files["siconv_desembolso"]["csv_member"]):
            if not {"NR_CONVENIO","ID_DESEMBOLSO"}.issubset(headers):raise RuntimeError("desembolso layout changed")
            seen_events=set()
            for row in reader:
                national_dis+=1;conv=(row["NR_CONVENIO"] or "").strip()
                if conv not in conv_to_proposal:continue
                eid=(row["ID_DESEMBOLSO"] or "").strip()
                if not eid or eid in seen_events:raise RuntimeError("duplicate or missing event ID")
                seen_events.add(eid);linked_dis+=1;dis_by_conv[conv]+=1
        table=[]
        categories=Counter()
        for prop,ib in sorted(proposals.items()):
            convs=proposal_convs.get(prop,set())
            events=sum(dis_by_conv[c] for c in convs)
            gnd4=items_by_proposal[prop]
            classification=("ambos_pad_gnd4_aprovado_e_desembolso" if gnd4 and events else
               "pad_gnd4_aprovado_sem_desembolso_encontrado" if gnd4 else
               "desembolso_sem_pad_gnd4_aprovado" if events else "nenhum_dos_dois")
            categories[classification]+=1
            table.append({"id_proposta":prop,"ibge7_proponente":ib,"municipio_proponente":names[ib],
              "n_convenios":len(convs),"n_desembolsos_vinculados":events,
              "n_itens_gnd4_aprovados":gnd4,
              "n_itens_gnd4_rmrp_nome":dest_by_proposal[prop]["rmrp_named"],
              "n_itens_gnd4_sp_fora_rmrp":dest_by_proposal[prop]["sp_not_rmrp"],
              "n_itens_gnd4_fora_sp":dest_by_proposal[prop]["out_of_sp"],
              "n_itens_gnd4_destino_rmrp_outro_municipio":dest_by_proposal[prop]["cross_municipal_rmrp"],
              "classificacao_cruzamento":classification,
              "aviso":"Desembolso integral do instrumento NAO atribuido aos itens GND4"})
        dest=out/"matriz_proposta_conv_pad_desembolso_nao_monetaria.csv"
        with dest.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(table[0]),delimiter=";");writer.writeheader();writer.writerows(table)
        qa={"national_proposals":all_proposals,"linked_rmrp_proposals":proposal_rows,
            "national_convenio_rows":national_convs,"linked_convenio_rows":linked_convs,
            "national_pad_items":national_pad,"rmrp_pad_items":linked_pad,"gnd4_approved_items":approved_items,
            "national_disbursement_rows":national_dis,"linked_disbursement_rows":linked_dis,
            "proposals_by_class":dict(categories),
            "sum_gnd4_approved_items":sum(r["n_itens_gnd4_aprovados"] for r in table),
            "sum_disbursements":sum(r["n_desembolsos_vinculados"] for r in table),
            "sum_named_rmrp_items":sum(r["n_itens_gnd4_rmrp_nome"] for r in table),
            "sum_cross_municipal_items":sum(r["n_itens_gnd4_destino_rmrp_outro_municipio"] for r in table)}
        if qa["linked_rmrp_proposals"]!=6410 or qa["gnd4_approved_items"]!=7917:
            raise RuntimeError("source drift from audited baseline; inspect before promotion: "+str(qa))
        if qa["linked_disbursement_rows"]!=qa["sum_disbursements"]:raise RuntimeError("non-conserved disbursements")
        if qa["gnd4_approved_items"]!=qa["sum_gnd4_approved_items"]:raise RuntimeError("non-conserved items")
        manifest["qa"]=qa
        manifest["output"]={"file":str(dest),"sha256":hashlib.sha256(dest.read_bytes()).hexdigest()}
        manifest["status"]="joined_pilot_non_monetary_not_homologated"
        manifest["restrictions"]=["Proponent municipality is not necessarily municipality of execution",
            "A disbursement from a mixed GND convenio is NOT entirely investment",
            "A planned approved PAD item is NOT evidence of actual execution or payment",
            "No money amounts are allocated; no R2/SQLite production changes"]
        persist()
        print(json.dumps({"status":manifest["status"],"qa":qa},ensure_ascii=False),flush=True)
    except Exception as exc:
        manifest["status"]="error";manifest["errors"].append(repr(exc));persist();raise
if __name__=="__main__":main()
