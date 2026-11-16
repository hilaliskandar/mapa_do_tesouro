#!/usr/bin/env python3
"""FED08 independent documentary audit of RMRP SICONV payments and project points.
No individual identifiers in the public QA JSON; detailed CSVs must stay private.
"""
import argparse,csv,datetime,json,sqlite3,collections,hashlib,zipfile
from pathlib import Path

def parsedate(s):
    try:return datetime.datetime.strptime(s.strip(),"%d/%m/%Y").date()
    except (ValueError,AttributeError):return None

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()

def audit(database,output):
    output.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(str(database))
    assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
    cols=("movimento","instrumento","proposta","municipio_proponente","pagamento","emissao_DL","situacao_DL","valor_centavos","dias_pagamento_apos_emissao")
    chronology=[];nonactive=[];by_status=collections.Counter();by_year=collections.Counter()
    years=collections.Counter();missing_dates=0
    query="""SELECT p.nr_mov_fin,p.nr_convenio,cv.proposta_id,cv.ibge_proponente,
    p.data_pag,d.data_emissao,d.status,p.valor_centavos
    FROM pagamento_fed03c p
    INNER JOIN dl_fed03c d ON p.id_dl=d.id_dl
    INNER JOIN convenio cv ON cv.numero=p.nr_convenio"""
    for row in c.execute(query):
        mov,conv,prop,ibge,paid,issued,status,amount=row
        pd=parsedate(paid);dd=parsedate(issued)
        if pd is None or dd is None:
            missing_dates+=1
            continue
        delta=(pd-dd).days
        years[pd.year]+=1
        if delta<0:
            chronology.append((*row,delta))
            by_status[status]+=1
            by_year[pd.year]+=1
        if status!="Ativo" and amount>0:
            nonactive.append((*row,delta))
    assert sum(years.values())==28503
    assert len(chronology)==808
    assert len(nonactive)==8
    assert sum(x[7] for x in nonactive)==27212091
    def writecsv(name,head,rows):
        path=output/name
        with path.open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.writer(f,delimiter=";");w.writerow(head);w.writerows(rows)
        return path
    chron_file=writecsv("FED08_PAGAMENTOS_ANTERIORES_DL_PRIVADO.csv",cols,chronology)
    dl_file=writecsv("FED08_DL_NAO_ATIVO_POSITIVO_PRIVADO.csv",cols,nonactive)
    geo_cols=("id_projeto","id_proposta","municipio_proponente","municipio_intersecao","status_intersecao","situacao_projeto","titulo","codigo_coordenada","latitude","longitude")
    geo_query="""SELECT pc.id_projeto,v.id_proposta,pr.ibge_proponente,g.municipio_ibge,g.status_espacial,
    o.situacao,o.titulo,g.source_row,coord.latitude,coord.longitude
    FROM projeto_coordenada_candidata_fed04b pc
    JOIN coordenada_intersecao_sp_fed04c g ON g.source_row=pc.source_row
    JOIN coordenada_proposta_fed04b coord ON coord.source_row=g.source_row
    JOIN vinculo_projeto_instrumento_fed04b v ON v.id_projeto=pc.id_projeto
    JOIN proposta pr ON pr.id=v.id_proposta
    JOIN obra_proponente o ON o.projeto_id=pc.id_projeto
    WHERE g.status_espacial<>'no_municipio_proponente' ORDER BY pc.id_projeto,g.source_row"""
    geo=list(c.execute(geo_query))
    assert len(geo)==20 and len({r[0] for r in geo})==19
    geofile=writecsv("FED08_PROJETOS_DIVERGENTES_PRIVADO.csv",geo_cols,geo)
    geo_stat=collections.Counter((r[4],r[5]) for r in geo)
    # The address of the source is never proof of physical execution.
    summary={
      "snapshot":"2026-11-15","executed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "count_payments":sum(years.values()),
      "payments_before_dl_issuance":len(chronology),
      "payments_before_dl_by_current_status":dict(sorted(by_status.items())),
      "payments_before_dl_by_payment_year":{str(k):v for k,v in sorted(by_year.items())},
      "payments_missing_or_invalid_dates":missing_dates,
      "positive_payments_with_nonactive_dl":len(nonactive),
      "positive_nonactive_dl_amount_centavos":sum(x[7] for x in nonactive),
      "divergent_project_coordinate_pairs":len(geo),
      "distinct_projects_with_divergent_coordinates":len({r[0] for r in geo}),
      "divergences_by_spatial_category_and_project_status":[
        {"spatial":k[0],"project_registry_status":k[1],"points":v}
        for k,v in sorted(geo_stat.items())],
      "source_stage":"cadastro_transferegov_obrasgov_ibge",
      "acceptances":{
        "identificador_e_vinculo_documental":"homologacao_tecnica_de_chaves",
        "quantitativos_cadastrais":"homologacao_tecnica",
        "natureza_gnd4_efetivamente_paga":"pendente",
        "estornos_devolucoes_e_fluxo_liquido":"pendente",
        "pontos_de_execucao_fisica":"pendente",
        "public_release_authorized":False},
      "caveats":[
        "Payment date preceding DL emission date does not by itself prove improper payment: verify source definitions and historical changes.",
        "Latest DL status can differ from status on the original payment date.",
        "A point recorded on a proposal is not evidence of execution at that point.",
        "No GND4/payment or executed location can be homologated with this evidence alone."
      ]
    }
    s=output/"FED08_AUDITORIA_PUBLICAVEL_SEM_IDS.json"
    s.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    pack=output/"RMRP_FED08_AUDITORIA_DOCUMENTAL_PRIVADA_2026-11-16.zip"
    with zipfile.ZipFile(pack,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in (chron_file,dl_file,geofile,s):z.write(f,f.name)
    with zipfile.ZipFile(pack) as z:assert z.testzip() is None
    c.close()
    return {"summary":summary,"private_zip_bytes":pack.stat().st_size,"private_zip_sha256":sha(pack)}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("sqlite",type=Path)
    parser.add_argument("out",type=Path)
    a=parser.parse_args()
    print(json.dumps(audit(a.sqlite,a.out),ensure_ascii=False))
