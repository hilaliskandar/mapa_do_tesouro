#!/usr/bin/env python3
"""Audit Transferegov Obrasgov/CIPI links by municipality *proponente* in SP.

National ZIPs are transient. All joins use explicit ID_PROPOSTA, NR_CONVENIO
and id_projeto_investimento; the output has only aggregate counts and hashes.
A city of proponent is NEVER asserted as physical place of investment.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,zipfile
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from inv_sp645_transferegov_new_source_layout import acquire

DIM=Path("governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv")
SETS=("siconv_proposta","siconv_convenio","siconv_coordenadas_obra",
      "siconv_dados_obrasgov_geral","siconv_contrato_cipi")
LAYOUT={
  "siconv_proposta":{"ID_PROPOSTA","COD_MUNIC_IBGE","UF_PROPONENTE"},
  "siconv_convenio":{"ID_PROPOSTA","NR_CONVENIO"},
  "siconv_coordenadas_obra":{"ID_PROPOSTA","LATITUDE_CADASTRO_OBRA","LONGITUDE_CADASTRO_OBRA"},
  "siconv_dados_obrasgov_geral":{"id_projeto_investimento","nr_instrumento"},
  "siconv_contrato_cipi":{"ID_PROJETO_INVESTIMENTO","ID_CONTRATO"}
}

def read(path:Path,required:set[str]):
    with zipfile.ZipFile(path) as archive:
        infos=[i for i in archive.infolist() if not i.is_dir() and i.filename.lower().endswith(".csv")]
        if len(infos)!=1:raise RuntimeError("Expected 1 CSV")
        with archive.open(infos[0]) as binary:
            head=binary.readline(2_000_000)
            enc=None
            for encoding in ("utf-8-sig","latin-1"):
                try:head.decode(encoding,errors="strict");enc=encoding;break
                except UnicodeDecodeError:pass
            if enc is None:raise ValueError("Header charset invalid")
            h=head.decode(enc,errors="strict")
            sep=";" if h.count(";")>=h.count(",") else ","
            columns=next(csv.reader([h],delimiter=sep))
            if len(set(columns))!=len(columns) or not required.issubset(columns):
                raise ValueError("Source columns changed "+str(required-set(columns)))
            stream=io.TextIOWrapper(binary,encoding=enc,errors="strict",newline="")
            for row in csv.DictReader(stream,fieldnames=columns,delimiter=sep):
                if None in row:raise ValueError("CSV column width drift")
                yield row
            stream.detach()
        if archive.testzip() is not None:raise RuntimeError("ZIP CRC failure")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out-dir",required=True)
    parser.add_argument("--timeout",type=int,default=650)
    args=parser.parse_args()
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    with DIM.open(encoding="utf-8",newline="") as f:dim=list(csv.DictReader(f,delimiter=";"))
    if len(dim)!=645 or len({r["codigo_ibge"] for r in dim})!=645:
        raise RuntimeError("IBGE7 SP645 dimension not validated")
    geo={r["codigo_ibge"]:r for r in dim}
    rmrp={r["codigo_ibge"] for r in dim if r["rm_au_nome"]=="Região Metropolitana de Ribeirão Preto"}
    if len(rmrp)!=34:raise RuntimeError("RMRP roster mismatch")
    report={"time_utc":datetime.now(timezone.utc).isoformat(),
     "status":"in_progress","scope":"SP645 and RMRP34 by MUNICIPALITY OF PROPONENT",
     "not_location_of_work":True,"no_monetary_values":True,
     "dimension_sha256":hashlib.sha256(DIM.read_bytes()).hexdigest(),
     "sources":{},"counts":{},"regional_coverage":[],"warnings":[]}
    def save():
        (out/"manifest_sp645_proponent_obra_links.json").write_text(
          json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    try:
        for name in SETS:
            path,info=acquire(out,name,args.timeout)
            report["sources"][name]=info;save()
        proposals={};proposal_rows=Counter();bad_prop=0;duplicate_prop=0;allprop=0
        for r in read(out/"siconv_proposta.zip",LAYOUT["siconv_proposta"]):
            allprop+=1
            ib=(r["COD_MUNIC_IBGE"] or "").strip()
            if ib not in geo:continue
            if (r["UF_PROPONENTE"] or "").strip().upper()!="SP":
                raise RuntimeError("SP IBGE with non-SP proposer UF")
            key=(r["ID_PROPOSTA"] or "").strip()
            if not key:bad_prop+=1;continue
            if key in proposals:
                duplicate_prop+=1
                if proposals[key]!=ib:raise RuntimeError("Proposal ID with conflicting IBGE")
                continue
            proposals[key]=ib;proposal_rows[ib]+=1
        report["counts"]["proposals"]={"national_rows":allprop,"sp_proponent_unique":len(proposals),
            "rmrp_proponent_unique":sum(proposal_rows[c] for c in rmrp),
            "sp_duplicate_proposal_ids":duplicate_prop,"sp_empty_id_rows":bad_prop}
        save()
        conv_city={};conv_rows=Counter();allconv=0;conflicts=0
        for r in read(out/"siconv_convenio.zip",LAYOUT["siconv_convenio"]):
            allconv+=1
            ib=proposals.get((r["ID_PROPOSTA"] or "").strip())
            if not ib:continue
            k=(r["NR_CONVENIO"] or "").strip()
            if not k:continue
            if k in conv_city:
                if conv_city[k]!=ib:conflicts+=1
                continue
            conv_city[k]=ib;conv_rows[ib]+=1
        if conflicts:raise RuntimeError("Conflicting convênio municipality identity")
        report["counts"]["convenios"]={"national_rows":allconv,"sp_proponent_unique":len(conv_city),
            "rmrp_proponent_unique":sum(conv_rows[c] for c in rmrp)}
        save()
        coordinate_rows=Counter();coordinate_proposals=defaultdict(set)
        all_coord=0;linked_coord=0;rmrp_coord=0;nonempty_latlon=0
        for r in read(out/"siconv_coordenadas_obra.zip",LAYOUT["siconv_coordenadas_obra"]):
            all_coord+=1
            k=(r["ID_PROPOSTA"] or "").strip();ib=proposals.get(k)
            if not ib:continue
            coordinate_rows[ib]+=1;coordinate_proposals[ib].add(k)
            linked_coord+=1
            if ib in rmrp:rmrp_coord+=1
            if (r["LATITUDE_CADASTRO_OBRA"] or "").strip() and (r["LONGITUDE_CADASTRO_OBRA"] or "").strip():
                nonempty_latlon+=1
        report["counts"]["coordinates"]={"national_rows":all_coord,"sp_rows_linked_by_proposal":linked_coord,
             "rmrp_rows_linked_by_proposal":rmrp_coord,
             "sp_proposals_with_coordinates":sum(len(s) for s in coordinate_proposals.values()),
             "sp_rows_with_both_coord_strings_nonempty":nonempty_latlon}
        save()
        # An instrument may produce multiple projects. Keep project IDs as a SET
        # and never sum contract rows as project expenditure.
        project_to_city={};proj_rows=Counter();all_gen=0;matched_inst=0;conflicting_projects=set()
        for r in read(out/"siconv_dados_obrasgov_geral.zip",LAYOUT["siconv_dados_obrasgov_geral"]):
            all_gen+=1
            k=(r["nr_instrumento"] or "").strip()
            ib=conv_city.get(k)
            if not ib:continue
            matched_inst+=1
            proj=(r["id_projeto_investimento"] or "").strip()
            if not proj:continue
            if proj in project_to_city and project_to_city[proj]!=ib:
                conflicting_projects.add(proj)
                continue
            if proj not in project_to_city:proj_rows[ib]+=1
            project_to_city[proj]=ib
        if conflicting_projects:
            for p in conflicting_projects:project_to_city.pop(p,None)
            # Discard ambiguous projects: no automatic territorial attribution.
            for ib in proj_rows:proj_rows[ib]=sum(v==ib for v in project_to_city.values())
        report["counts"]["obrasgov_general"]={"national_rows":all_gen,
          "sp_rows_matched_exact_instrument_number":matched_inst,
          "sp_projects_with_unique_proponent_ibge":len(project_to_city),
          "sp_projects_with_multiple_proponent_ibge":len(conflicting_projects),
          "rmrp_projects_unique_proponent":sum(proj_rows[c] for c in rmrp)}
        save()
        contract_rows=Counter();all_contract=0;sp_contract=0;rmrp_contract=0
        for r in read(out/"siconv_contrato_cipi.zip",LAYOUT["siconv_contrato_cipi"]):
            all_contract+=1
            ib=project_to_city.get((r["ID_PROJETO_INVESTIMENTO"] or "").strip())
            if not ib:continue
            contract_rows[ib]+=1;sp_contract+=1
            if ib in rmrp:rmrp_contract+=1
        report["counts"]["contracts_cipi"]={"national_rows":all_contract,
          "sp_rows_linked_through_project_instrument":sp_contract,
          "rmrp_rows_linked_through_project_instrument":rmrp_contract}
        # region membership is defined by proponent code, not execution site.
        dimensions=[("RA","ra_codigo","ra_nome"),("RG","rg_codigo","rg_nome"),
           ("RM_AU","rm_au_codigo","rm_au_nome")]
        for kind,code_field,name_field in dimensions:
            groups=defaultdict(lambda:Counter())
            names={}
            for ib,row in geo.items():
                code=row[code_field]
                if not code:continue
                ident=(row.get("rm_au_tipo","")+"_"+code) if kind=="RM_AU" else code
                names[ident]=row[name_field]
                g=groups[ident]
                g["municipios"]+=1
                g["propostas"]+=proposal_rows[ib]
                g["convenios"]+=conv_rows[ib]
                g["coordenadas"]+=coordinate_rows[ib]
                g["projetos_obrasgov"]+=proj_rows[ib]
                g["contratos_cipi"]+=contract_rows[ib]
            for ident,counts in sorted(groups.items()):
                report["regional_coverage"].append({"dimension":kind,"code":ident,
                    "name":names[ident],**dict(counts)})
        if sum(x["municipios"] for x in report["regional_coverage"] if x["dimension"]=="RA")!=645:
            raise RuntimeError("RA region coverage is not 645")
        if sum(x["municipios"] for x in report["regional_coverage"] if x["dimension"]=="RG")!=645:
            raise RuntimeError("RG region coverage is not 645")
        if sum(x["municipios"] for x in report["regional_coverage"] if x["dimension"]=="RM_AU")!=255:
            raise RuntimeError("RM/AU region coverage not 255")
        report["warnings"]=[
           "All municipal and RA/RG/RM/AU counts refer to the MUNICIPAL PROPONENT, never geographic investment location",
           "Exact instrument number match is a candidate link; IDs and collisions audited, but it is not monetary spending",
           "Coordinates may be outside the municipality of proposal; no geospatial attribution or amounts are inferred",
           "SP and regional groups are alternative counts, not additive across different regional typologies",
           "No financial stage or nature inferred from instrument, project or contract metadata"]
        report["status"]="proponent_regional_coverage_candidate_counts_qa_pass"
        save()
        print(json.dumps({"status":report["status"],"counts":report["counts"],
          "regions":len(report["regional_coverage"])},ensure_ascii=False),flush=True)
    except Exception as e:
        report["status"]="blocked"
        report["error"]=type(e).__name__+": "+str(e)[:300]
        save();raise
    finally:
        for name in SETS:
            z=out/(name+".zip")
            if z.exists():z.unlink()

if __name__=="__main__":main()
