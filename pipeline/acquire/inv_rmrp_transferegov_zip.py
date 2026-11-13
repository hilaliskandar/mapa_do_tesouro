#!/usr/bin/env python3
"""Extrai amostra territorial de ZIPs oficiais Transferegov, sem tocar no banco produtivo.

Uso: python pipeline/acquire/inv_rmrp_transferegov_zip.py --out-dir /tmp/inv_rmrp --sets siconv_convenio,siconv_desembolso
Dependencias: biblioteca padrao Python 3.11+. Um snapshot e uma fonte de eventos por arquivo.
Nao certifica investimento; todos os valores devem ser classificados por plano de aplicacao.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen
import zipfile
from datetime import datetime, timezone

BASE = "https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/"
DEFAULT_SETS = ("siconv_convenio", "siconv_desembolso", "siconv_emenda", "siconv_empenho", "siconv_plano_aplicacao_detalhado")
SAFE_SETS = set(DEFAULT_SETS) | {"siconv_proposta", "siconv_pagamento", "siconv_coordenadas_obra", "siconv_dados_obrasgov_geral"}
REF = "governance/INV_RMRP_SIAFEM_CROSSWALK_COBERTURA_34_MUNICIPIOS_2026_11_12.json"
# Somente colunas territorialmente explicitas podem filtrar registros; nunca usar
# substring de nome ou numero da proposta para atribuir um investimento.
IBGE_COLS = ("COD_MUNIC_IBGE", "COD_MUNICIPIO_IBGE", "CODIGO_IBGE", "COD_IBGE", "COD_MUNICIPIO", "COD_MUNIC_PROPOSTA", "COD_MUNIC_CONVENENTE", "MUNICIPIO_IBGE")
CITY_COLS = ("MUNIC_PROPONENTE", "MUNIC_CONVENENTE", "MUNICIPIO_PROPONENTE", "MUNICIPIO_CONVENENTE", "MUNICIPIO")
UF_COLS = ("UF_PROPONENTE", "UF_CONVENENTE", "UF", "ESTADO")
def read_csv_rows(file):
    sample = file.readline()
    encoding = "utf-8-sig"
    try: sample.decode(encoding)
    except UnicodeError: encoding = "latin-1"
    # Arquivos oficiais usualmente separam por ponto e virgula; verificar o layout real.
    first = sample.decode(encoding, errors="replace")
    sep = ";" if first.count(";") >= first.count(",") else ","
    stream = io.TextIOWrapper(file, encoding=encoding, errors="replace", newline="")
    return first, stream, sep, encoding

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    p.add_argument("--sets", default=",".join(DEFAULT_SETS))
    p.add_argument("--reference", default=REF)
    p.add_argument("--timeout", type=int, default=240)
    args = p.parse_args()
    targets = args.sets.split(",")
    if not targets or any(x not in SAFE_SETS for x in targets):
        raise SystemExit("Conjunto nao permitido: " + repr(targets))
    ref = json.loads(Path(args.reference).read_text(encoding="utf-8"))
    municipalities = {r["ibge7"]: r["municipio"] for r in ref["municipalities"]}
    assert len(municipalities) == 34
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    manifest = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "scope": "RMRP_34", "source_system": "Transferegov downloads", "sets": []}
    for name in targets:
        url = BASE + name + ".zip"
        filename = out / (name + ".zip")
        h = hashlib.sha256()
        entry = {"set": name, "url": url, "status": "started", "source_zip": str(filename)}
        try:
            req = Request(url, headers={"User-Agent":"financas-rmrp-auditoria/0.1", "Accept": "application/zip"})
            with urlopen(req, timeout=args.timeout) as response, filename.open("wb") as w:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk: break
                    h.update(chunk); w.write(chunk)
            entry.update({"sha256_zip": h.hexdigest(), "bytes_zip": filename.stat().st_size})
            with zipfile.ZipFile(filename) as z:
                candidates = [e for e in z.infolist() if e.filename.lower().endswith(".csv")]
                entry["csv_members"] = [dict(name=e.filename, size=e.file_size) for e in candidates]
                if len(candidates)!=1: raise ValueError("ZIP sem membro CSV unico; inspecao manual necessaria")
                member=candidates[0]
                with z.open(member) as source:
                    raw = source.readline()
                    encoding = "utf-8-sig"
                    try: head = raw.decode(encoding)
                    except UnicodeDecodeError: encoding="latin-1"; head=raw.decode(encoding,errors="replace")
                    delimiter = ";" if head.count(";")>=head.count(",") else ","
                    stream = io.TextIOWrapper(source, encoding=encoding, errors="replace", newline="")
                    # Reconstruir o primeiro registro, preservando eventuais quebras de linha.
                    reader = csv.DictReader(io.StringIO(head + stream.read()), delimiter=delimiter)
                    cols = reader.fieldnames or []
                    key = next((c for c in cols if c.strip().upper() in IBGE_COLS), None)
                    # A existencia de campo territorial nao prova que esteja preenchido com IBGE7.
                    counts = {x:0 for x in municipalities}
                    examples=[]; total=0; selected=0; rejected_territory=0; invalid_territory=0
                    selected_path=out/(name + "_rmrp.csv")
                    with selected_path.open("w",encoding="utf-8",newline="") as f:
                        writer=csv.DictWriter(f,fieldnames=cols,delimiter=";",extrasaction="ignore")
                        writer.writeheader()
                        for row in reader:
                            total+=1
                            if not key:
                                if len(examples)<3: examples.append({k:row.get(k,"")[:100] for k in cols[:8]})
                                continue
                            code=(row.get(key) or "").strip()
                            if code in municipalities:
                                writer.writerow(row); selected+=1; counts[code]+=1
                            elif not code or len(code)!=7 or not code.isdigit():
                                invalid_territory+=1
                            else: rejected_territory+=1
                    entry.update({"csv_rows":total,"headers":cols,"encoding":encoding,"delimiter":delimiter,
                                  "ibge_column":key,"selected_rows":selected,
                                  "invalid_territory":invalid_territory,"rejected_other_municipalities":rejected_territory,
                                  "municipality_counts":counts,"examples_when_no_ibge":examples,
                                  "selected_csv":str(selected_path)})
                    # Nao usar o CSV selecionado como cobertura homologada se nao houver chave territorial.
                    entry["status"]="extracted_by_ibge" if key else "schema_only_requires_territory_crosswalk"
        except Exception as exc:
            entry["status"]="error";entry["error"]=str(exc)
        manifest["sets"].append(entry)
        (out/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps({"set":name,"status":entry["status"],"rows":entry.get("csv_rows"),"selected":entry.get("selected_rows"),"error":entry.get("error")},ensure_ascii=False),flush=True)
    if any(e["status"]=="error" for e in manifest["sets"]): raise SystemExit(2)
if __name__=="__main__":main()
