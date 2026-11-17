#!/usr/bin/env python3
"""INV-FED03: nonmonetary municipality/proposal crosswalk for Transferegov payments.

Only counts rows from the official siconv_pagamento dataset joined by NR_CONVENIO.
No personal, beneficiary or bank microdata are retained in published outputs.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from inv_rmrp_transferegov_join import download,rows,REFERENCE

SOURCES=("siconv_proposta","siconv_convenio","siconv_pagamento")
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out-dir",required=True)
    a.add_argument("--timeout",type=int,default=650)
    a.add_argument("--reference",default=REFERENCE)
    args=a.parse_args()
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    reference=json.loads(Path(args.reference).read_text(encoding="utf-8"))
    municipalities={str(x["ibge7"]):x["municipio"] for x in reference["municipalities"]}
    if len(municipalities)!=34:raise RuntimeError("Expected 34 municipalities")
    manifest={"status":"in_progress","captured_at_utc":datetime.now(timezone.utc).isoformat(),
      "scope":"RMRP proponent, not necessarily expenditure site","sources":[],"qa":{},"errors":[]}
    def persist(): (out/"manifest_fed03_payment_join.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    persist()
    try:
        for name in SOURCES:
            item=download(out,name,args.timeout);manifest["sources"].append(item);persist()
        sources={x["name"]:x for x in manifest["sources"]}
        prop_city={};prop_count=0;all_prop=0
        for h,reader in rows(sources["siconv_proposta"]["path"],sources["siconv_proposta"]["csv_member"]):
            if not {"ID_PROPOSTA","COD_MUNIC_IBGE","UF_PROPONENTE"}.issubset(h):raise RuntimeError("proposal headers changed")
            for row in reader:
                all_prop+=1;ib=(row["COD_MUNIC_IBGE"] or "").strip()
                if ib not in municipalities:continue
                if (row["UF_PROPONENTE"] or "").strip().upper()!="SP":raise RuntimeError("non-SP roster")
                p=(row["ID_PROPOSTA"] or "").strip()
                if not p or (p in prop_city and prop_city[p]!=ib):raise RuntimeError("ambiguous proposal")
                if p in prop_city:raise RuntimeError("duplicate proposal")
                prop_city[p]=ib;prop_count+=1
        conv_prop={};all_conv=selected_conv=0
        for h,reader in rows(sources["siconv_convenio"]["path"],sources["siconv_convenio"]["csv_member"]):
            if not {"ID_PROPOSTA","NR_CONVENIO"}.issubset(h):raise RuntimeError("convenio headers changed")
            for row in reader:
                all_conv+=1;p=(row["ID_PROPOSTA"] or "").strip()
                if p not in prop_city:continue
                conv=(row["NR_CONVENIO"] or "").strip()
                if not conv or (conv in conv_prop and conv_prop[conv]!=p):raise RuntimeError("ambiguous convenio")
                if conv in conv_prop:raise RuntimeError("duplicate convenio row")
                conv_prop[conv]=p;selected_conv+=1
        payments_by_convenio=Counter();payment_count=linked_payment=empty_convenio=0
        for h,reader in rows(sources["siconv_pagamento"]["path"],sources["siconv_pagamento"]["csv_member"]):
            if "NR_CONVENIO" not in h:raise RuntimeError("payment NR_CONVENIO not found in official schema")
            for row in reader:
                payment_count+=1;conv=(row["NR_CONVENIO"] or "").strip()
                if not conv:empty_convenio+=1
                if conv in conv_prop:
                    payments_by_convenio[conv]+=1;linked_payment+=1
        per_proposal=Counter();per_city=Counter();per_city_convenios=Counter()
        for conv,count in payments_by_convenio.items():
            p=conv_prop[conv];ib=prop_city[p]
            per_proposal[p]+=count;per_city[ib]+=count;per_city_convenios[ib]+=1
        classes=Counter()
        for prop in prop_city:
            classes["proposal_with_payment_rows" if per_proposal[prop] else "proposal_without_payment_rows_in_source"]+=1
        matrix=out/"pagamentos_contagem_municipio_proponente.csv"
        with matrix.open("w",encoding="utf-8",newline="") as f:
            fields=["ibge7_proponente","municipio_proponente","eventos_pagamento_linhas","convenios_com_pagamento_linhas"]
            writer=csv.DictWriter(f,delimiter=";",fieldnames=fields);writer.writeheader()
            for ib,name in sorted(municipalities.items()):
                writer.writerow(dict(zip(fields,[ib,name,per_city[ib],per_city_convenios[ib]])))
        qa={"national_proposal_rows":all_prop,"rmrp_proposals":prop_count,
            "national_convenio_rows":all_conv,"rmrp_convenio_rows":selected_conv,
            "national_payment_rows":payment_count,"rmrp_linked_payment_rows":linked_payment,
            "national_payment_rows_missing_NR_CONVENIO":empty_convenio,
            "rmrp_convenios_with_payment_rows":len(payments_by_convenio),
            "proposals":dict(classes),"covered_municipalities":sum(per_city[k]>0 for k in municipalities),
            "reconciled_payment_rows":sum(per_city.values())}
        if qa["rmrp_proposals"]!=6410 or qa["rmrp_convenio_rows"]!=1793:
            raise RuntimeError("Audited baseline drift; inspect before promotion")
        if qa["reconciled_payment_rows"]!=qa["rmrp_linked_payment_rows"]:raise RuntimeError("payment rows not conserved")
        manifest["qa"]=qa
        manifest["municipal_aggregates_csv"]={"path":str(matrix),"sha256":hashlib.sha256(matrix.read_bytes()).hexdigest()}
        manifest["status"]="proponent_payment_rows_linked_nonmonetary"
        manifest["restrictions"]=["One payment row is not necessarily one final payment, nor net paid amount.",
            "No payment cancellation, amount, OBTV or status classification was assessed.",
            "No inference about GND4 eligibility or physical execution from an instrument payment.",
            "Municipality is proponent only; no personal payment details persisted in outputs.",
            "No R2 or SQLite production writes."];persist()
        print(json.dumps({"status":manifest["status"],"qa":qa},ensure_ascii=False),flush=True)
    except Exception as exc:
        manifest["status"]="error";manifest["errors"].append(repr(exc));persist();raise
if __name__=="__main__":main()
