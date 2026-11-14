#!/usr/bin/env python3
"""INV-FED02 preliminary cross-tab. Reads existing PAD territorial CSV only.

Never equates planned values to payments; refuses to make monetary totals.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

def category(value):
    code="".join(c for c in (value or "") if c.isdigit())
    if len(code)<6:return "indeterminado"
    if code.startswith("44"):return "gnd4_investimento_planejado"
    if code.startswith("45"):return "gnd5_inversao"
    if code.startswith("46"):return "gnd6_amortizacao"
    if code.startswith("3"):return "corrente"
    if code.startswith("4"):return "capital_outro"
    return "indeterminado"

def status(value):
    norm=(value or "").strip().upper()
    if norm=="APROVADO":return "aprovado"
    if norm=="EM_COMPLEMENTACAO":return "em_complementacao"
    if not norm:return "vazio_nao_homologado"
    return "outro:"+norm

def canonical_name(value):
    s=unicodedata.normalize("NFKD", (value or "").strip().upper())
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).split())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--manifest",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--roster",default="governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv")
    args=p.parse_args()
    input_path=Path(args.input); raw=input_path.read_bytes()
    prior=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if prior.get("status")!="preliminar_plano_classificado_nao_homologado":
        raise RuntimeError("source manifest not qualified for preliminary audit")
    with Path(args.roster).open(encoding="utf-8-sig",newline="") as roster_file:
        roster=list(csv.DictReader(roster_file,delimiter=";"))
    if len(roster)!=34:raise RuntimeError("RMRP roster expected 34")
    roster_by_name={}
    for municipality in roster:
        name=canonical_name(municipality["municipio"])
        code=municipality["codigo_ibge"]
        if name in roster_by_name or len(code)!=7:raise RuntimeError("ambiguous roster")
        roster_by_name[name]=code
    required={"__ibge7_proponente","ID_PROPOSTA","ID_ITEM_PAD","COD_NATUREZA_DESPESA","SIT_ITEM","SIGLA","MUNICIPIO"}
    cross=Counter(); municipalities=defaultdict(Counter); unknown=Counter()
    locations=Counter(); destination=Counter(); destination_by_proponent=Counter(); destination_exception_rows=[]; cross_municipal=Counter(); exceptional=[]; ids=set(); n=0; missing_id=0; duplicate=0
    with input_path.open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f,delimiter=";")
        assert required.issubset(set(reader.fieldnames or [])),str(required-set(reader.fieldnames or []))
        for row in reader:
            n+=1
            ib=(row["__ibge7_proponente"] or "").strip()
            if len(ib)!=7 or not ib.isdigit():raise RuntimeError("invalid proponent IBGE")
            ident=(row["ID_ITEM_PAD"] or "").strip()
            if not ident:missing_id+=1
            elif ident in ids:duplicate+=1
            else:ids.add(ident)
            cat=category(row["COD_NATUREZA_DESPESA"])
            st=status(row["SIT_ITEM"])
            uf=(row["SIGLA"] or "").strip().upper()
            loc="item_uf_sp_municipio_nao_validado" if uf=="SP" else ("item_uf_ausente" if not uf else "item_uf_fora_sp")
            destination_code=roster_by_name.get(canonical_name(row["MUNICIPIO"])) if uf=="SP" else None
            if uf!="SP":dest_type="fora_sp"
            elif destination_code:dest_type="municipio_item_corresponde_rmrp_por_nome"
            elif (row["MUNICIPIO"] or "").strip():dest_type="municipio_item_sp_sem_correspondencia_rmrp"
            else:dest_type="municipio_item_nao_informado"
            if cat=="gnd4_investimento_planejado" and st=="aprovado":
                destination[dest_type]+=1
                if destination_code:
                    destination_by_proponent[(ib,destination_code)]+=1
                    if destination_code!=ib:cross_municipal[(ib,destination_code)]+=1
                else:
                    destination_exception_rows.append({"ibge7_proponente":ib,"id_proposta":row["ID_PROPOSTA"],"id_item_pad":ident,"natureza":row["COD_NATUREZA_DESPESA"],"situacao":row["SIT_ITEM"],"uf_item":uf,"municipio_item":row["MUNICIPIO"],"motivo":dest_type})
            cross[(cat,st,loc)]+=1
            municipalities[ib][(cat,st,loc)]+=1
            locations[(uf or "(vazio)")]+=1
            if cat=="indeterminado":unknown[row["COD_NATUREZA_DESPESA"]]+=1
            if (cat=="indeterminado" or loc!="item_uf_sp_municipio_nao_validado") and len(exceptional)<100:
                exceptional.append({"ibge7_proponente":ib,"id_proposta":row["ID_PROPOSTA"],"id_item_pad":ident,
                    "natureza":row["COD_NATUREZA_DESPESA"],"situacao":row["SIT_ITEM"],"uf_item":uf,"municipio_item":row["MUNICIPIO"],
                    "motivo":"natureza_indeterminada" if cat=="indeterminado" else loc})
    count_expected=prior.get("coverage",{}).get("linked_plan_items")
    if count_expected!=n:raise RuntimeError(f"plan count mismatch {n} != {count_expected}")
    if missing_id or duplicate:raise RuntimeError(f"invalid item ids: missing={missing_id} duplicated={duplicate}")
    if len(municipalities)!=34:raise RuntimeError("expected 34 proponent municipalities")
    if sum(cross.values())!=n:raise RuntimeError("cross total mismatch")
    candidate=sum(v for (cat,st,loc),v in cross.items() if cat=="gnd4_investimento_planejado" and st=="aprovado")
    approved_in_sp=sum(v for (cat,st,loc),v in cross.items() if cat=="gnd4_investimento_planejado" and st=="aprovado" and loc=="item_uf_sp_municipio_nao_validado")
    if sum(destination.values()) != candidate:
        raise RuntimeError("destination reconciliation mismatch")
    if sum(destination_by_proponent.values()) != destination.get("municipio_item_corresponde_rmrp_por_nome", 0):
        raise RuntimeError("municipal candidate crosswalk mismatch")
    if len(destination_exception_rows)!=candidate-destination.get("municipio_item_corresponde_rmrp_por_nome",0):
        raise RuntimeError("exception count mismatch")
    report={"generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "qa_status":"preliminary_cross_tab_not_homologated",
      "source_file":str(input_path),"source_sha256":hashlib.sha256(raw).hexdigest(),
      "source_manifest":str(args.manifest),"rows_checked":n,"unique_item_ids":len(ids),
      "proponent_municipalities":len(municipalities),
      "gnd4_approved_items_candidate":candidate,
      "gnd4_approved_and_item_uf_sp_not_geocoded":approved_in_sp,
      "cross_tab":[{"natureza":a,"situacao":b,"localizacao":c,"itens":v} for (a,b,c),v in sorted(cross.items())],
      "item_uf_counts":dict(sorted(locations.items())),
      "gnd4_approved_destination_match":dict(sorted(destination.items())),
      "gnd4_approved_territorial_exceptions_all":destination_exception_rows,
      "gnd4_approved_other_rmrp_destination_count":sum(cross_municipal.values()),
      "gnd4_approved_other_rmrp_destination_pairs":[{"ibge7_proponente":p,"ibge7_municipio_item":d,"itens":q} for (p,d),q in sorted(cross_municipal.items())],
      "gnd4_approved_proponent_to_named_destination":[{"ibge7_proponente":p,"ibge7_municipio_item":d,"itens":q} for (p,d),q in sorted(destination_by_proponent.items())],
      "territorial_method":"Exact normalized municipality name match with the 34 IBGE-coded roster, after requiring item UF=SP; this is a candidate linkage, not a confirmed execution geocode.",
      "unknown_nature_codes":dict(sorted(unknown.items())),
      "by_proponent":[{"ibge7":ib,"cross_tab":[{"natureza":a,"situacao":b,"localizacao":c,"itens":v} for (a,b,c),v in sorted(counter.items())]} for ib,counter in sorted(municipalities.items())],
      "exception_samples":exceptional,
      "restrictions":["This is a cross-tab of planned PAD items, NOT verified investment execution.",
        "SIT_ITEM approved is administrative status, not proof of payment.",
        "UF=SP does not establish an investment within the 34 RMRP municipalities.",
        "Municipality name matches are provisional until matched to official source identifiers and territorial evidence.",
        "No totals of planned, committed, disbursed or executed monetary values.",
        "Proponent territory does not establish implementation territory."]}
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({**{k:report[k] for k in ("qa_status","rows_checked","unique_item_ids","proponent_municipalities","gnd4_approved_items_candidate","gnd4_approved_and_item_uf_sp_not_geocoded")},"gnd4_approved_destination_match":report["gnd4_approved_destination_match"],"gnd4_approved_other_rmrp_destination_count":report["gnd4_approved_other_rmrp_destination_count"],"gnd4_approved_territorial_exceptions_all":report["gnd4_approved_territorial_exceptions_all"],"gnd4_approved_top_crosswalk":sorted(report["gnd4_approved_proponent_to_named_destination"],key=lambda r:-r["itens"])[:15]},ensure_ascii=False))

if __name__=="__main__":main()
