#!/usr/bin/env python3
"""Vincula registros Transferegov de propostas, convenios e eventos ao IBGE.
Usa apenas chaves administrativas explicitas. Nao classifica nem soma investimento.
Dados nacionais sao baixados em ZIP; resultados territoriais nao substituem as fontes.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import zipfile
from urllib.request import Request, urlopen

URL = "https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/"
REFERENCE = "governance/INV_RMRP_SIAFEM_CROSSWALK_COBERTURA_34_MUNICIPIOS_2026_11_12.json"
SETS = ("siconv_proposta", "siconv_convenio", "siconv_desembolso", "siconv_emenda")
DEFAULT_TIMEOUT = 240

def download(out: Path, name: str, timeout: int) -> dict:
    dest=out / (name + ".zip")
    sha=hashlib.sha256()
    req=Request(URL+name+".zip", headers={"User-Agent":"financas-rmrp-transferegov/0.2"})
    with urlopen(req,timeout=timeout) as response, dest.open("wb") as handle:
        for block in iter(lambda:response.read(1024*1024),b""):
            sha.update(block);handle.write(block)
    with zipfile.ZipFile(dest) as z:
        members=[x for x in z.infolist() if x.filename.lower().endswith(".csv")]
        if len(members)!=1:raise RuntimeError(f"{name}: CSV members={len(members)}")
        member=members[0]
        return {"name":name,"path":str(dest),"url":URL+name+".zip","sha256":sha.hexdigest(),"bytes_zip":dest.stat().st_size,
                "csv_member":member.filename,"csv_uncompressed_bytes":member.file_size}

def rows(path: str, member: str):
    """Yields (headers, row iterator), closing resources after iteration."""
    with zipfile.ZipFile(path) as z:
        with z.open(member) as source:
            head=source.readline()
            try:head_s=head.decode("utf-8-sig"); enc="utf-8-sig"
            except UnicodeDecodeError:head_s=head.decode("latin-1");enc="latin-1"
            delim=";" if head_s.count(";")>=head_s.count(",") else ","
            stream=io.TextIOWrapper(source,encoding=enc,errors="replace",newline="")
            # first header is decoded independently to avoid dropping first line on wrapper reset
            headers=next(csv.reader([head_s],delimiter=delim))
            reader=csv.DictReader(stream,fieldnames=headers,delimiter=delim)
            yield headers,reader

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--reference",default=REFERENCE)
    ap.add_argument("--timeout",type=int,default=DEFAULT_TIMEOUT)
    args=ap.parse_args()
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    ref=json.loads(Path(args.reference).read_text(encoding="utf-8"))
    names={str(x["ibge7"]):x["municipio"] for x in ref["municipalities"]}
    if len(names)!=34:raise RuntimeError("RMRP reference invalid: 34 expected")
    manifest={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"status":"in_progress",
              "scope":"RMRP34_by_proponent_ibge_only","semantics":"propostas/instrumentos/eventos; not investment",
              "files":[],"counts":{},"municipalities":{c:{"name":n,"propostas":0,"convenios":0,"desembolsos":0,"emendas":0} for c,n in names.items()},
              "failures":[]}
    def persist():
        (out/"manifest_join.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    persist()
    # Download each official dataset, preserve checksum; no R2 write.
    try:
        for item in SETS:
            d=download(out,item,args.timeout);manifest["files"].append(d);print(json.dumps({"download":item,"bytes":d["bytes_zip"],"sha":d["sha256"]}),flush=True);persist()
        datasets={x["name"]:x for x in manifest["files"]}
        proposals={}  # ID_PROPOSTA -> RMRP municipality code, only unique/single-state entries
        conflicting=set()
        all_p=0
        selected_p=0
        with (out/"propostas_rmrp.csv").open("w",encoding="utf-8",newline="") as dest:
            writer=None
            for h,reader in rows(datasets["siconv_proposta"]["path"],datasets["siconv_proposta"]["csv_member"]):
                required={"ID_PROPOSTA","COD_MUNIC_IBGE","UF_PROPONENTE"}
                if not required.issubset(h):raise RuntimeError("missing proposal columns "+str(required-set(h)))
                writer=csv.DictWriter(dest,fieldnames=h,delimiter=";",extrasaction="ignore");writer.writeheader()
                for row in reader:
                    all_p+=1
                    code=(row.get("COD_MUNIC_IBGE") or "").strip()
                    if code not in names:continue
                    if (row.get("UF_PROPONENTE") or "").strip().upper()!="SP":
                        raise RuntimeError("IBGE in RMRP with UF != SP: "+str(row.get("ID_PROPOSTA")))
                    key=(row.get("ID_PROPOSTA") or "").strip()
                    if not key:raise RuntimeError("proposal missing ID_PROPOSTA for municipality "+code)
                    if key in proposals and proposals[key]!=code:conflicting.add(key)
                    else:proposals[key]=code
                    writer.writerow(row);selected_p+=1;manifest["municipalities"][code]["propostas"]+=1
        for k in conflicting:proposals.pop(k,None)
        manifest["counts"]["siconv_proposta"]={"national_rows":all_p,"rmrp_rows":selected_p,"unique_proposal_ids":len(proposals),
                                                "ambiguous_proposal_ids":len(conflicting),"municipalities_with_rows":sum(x["propostas"]>0 for x in manifest["municipalities"].values())}
        if selected_p==0 or len(conflicting):raise RuntimeError("Proposal source missing or ambiguous IDs; crosswalk requires audit")
        print(json.dumps(manifest["counts"]["siconv_proposta"]),flush=True)
        persist()
        conv_to_city={}
        ambiguous_convenio=set()
        # Convenio key pair links to proponent municipality via ID_PROPOSTA.
        for dataset in ("siconv_convenio","siconv_desembolso","siconv_emenda"):
            d=datasets[dataset]; all_rows=linked=missing=0
            method=Counter(); unmatched_keys=[]
            with (out/(dataset+"_rmrp.csv")).open("w",encoding="utf-8",newline="") as dest:
                writer=None
                for h,reader in rows(d["path"],d["csv_member"]):
                    if dataset=="siconv_convenio" and not {"ID_PROPOSTA","NR_CONVENIO"}.issubset(h):
                        raise RuntimeError("convenio lacks ID_PROPOSTA/NR_CONVENIO")
                    if "ID_PROPOSTA" not in h and "NR_CONVENIO" not in h:
                        # No valid join key: schema only, not a zero-RMRP result.
                        raise RuntimeError(dataset+" lacks both supported linkage keys")
                    writer=csv.DictWriter(dest,fieldnames=["__ibge7_proponente","__vinculo"]+h,delimiter=";",extrasaction="ignore");writer.writeheader()
                    for row in reader:
                        all_rows+=1
                        proposal=(row.get("ID_PROPOSTA") or "").strip()
                        convenio=(row.get("NR_CONVENIO") or "").strip()
                        proposed_city=proposals.get(proposal)
                        convenio_city=conv_to_city.get(convenio)
                        if proposed_city and convenio_city and proposed_city!=convenio_city:
                            raise RuntimeError(dataset+": conflicting proposal/convenio municipalities")
                        city=proposed_city or convenio_city
                        if not city:
                            missing+=1
                            if len(unmatched_keys)<3:unmatched_keys.append({"ID_PROPOSTA":proposal,"NR_CONVENIO":convenio})
                            continue
                        method["ID_PROPOSTA" if proposed_city else "NR_CONVENIO"]+=1
                        if dataset=="siconv_convenio":
                            if not convenio:raise RuntimeError("matched convenio with missing NR_CONVENIO")
                            if convenio in conv_to_city and conv_to_city[convenio]!=city:ambiguous_convenio.add(convenio)
                            else:conv_to_city[convenio]=city
                        writer.writerow({"__ibge7_proponente":city,"__vinculo":"ID_PROPOSTA" if proposed_city else "NR_CONVENIO",**row})
                        linked+=1
                        col={"siconv_convenio":"convenios","siconv_desembolso":"desembolsos","siconv_emenda":"emendas"}[dataset]
                        manifest["municipalities"][city][col]+=1
                manifest["counts"][dataset]={"national_rows":all_rows,"rmrp_rows":linked,"unmatched_rows_national":missing,"headers":h,
                    "join_method":dict(method),"sample_unmatched_keys":unmatched_keys,
                    "municipalities_with_rows":sum(x[{"siconv_convenio":"convenios","siconv_desembolso":"desembolsos","siconv_emenda":"emendas"}[dataset]]>0 for x in manifest["municipalities"].values())}
            if ambiguous_convenio:raise RuntimeError("Multiple cities on same NR_CONVENIO: "+str(len(ambiguous_convenio)))
            print(json.dumps({"dataset":dataset,**manifest["counts"][dataset]}),flush=True)
            persist()
        manifest["status"]="joined_proponent_only_unclassified"
        manifest["warnings"]=["Estes sao municipios PROPONENTES; localizacao de obra pode ser diferente.",
             "As contagens nao representam investimentos confirmados nem recursos liberados para capital.",
             "Numeros de linhas de desembolso nao equivalem a numero de instrumentos; sem somatoria nesta fase.",
             "Nao foram recuperados pagamentos/planos de aplicacao, portanto classificacao de capital permanece pendente."]
    except Exception as e:
        manifest["status"]="error";manifest["failures"].append(str(e));persist();raise
    persist()
if __name__=="__main__":main()
