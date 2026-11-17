#!/usr/bin/env python3
"""FED09 private-only API extension: disbursement grouped by source empenho code.
Does not calculate GND4 paid or attribute the physical place of an investment.
"""
import argparse,collections,hashlib,json,shutil,sqlite3,zipfile
from pathlib import Path

ROOT=Path("data/api/v3/investimentos/rmrp")
EXPECTED={"33":26356753482,"34":25000000,"44":45050185885}

def jload(p):return json.loads(p.read_text(encoding="utf-8"))
def jsave(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def build(source_site,sqlite,output_site,outzip):
    if output_site.exists():raise RuntimeError("Destination already exists, refuse overwrite")
    shutil.copytree(source_site,output_site)
    api=output_site/ROOT
    assert (output_site/".rmrp-fed07-private-preview").exists()
    db=sqlite3.connect(sqlite)
    assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
    units=db.execute("""SELECT d.ibge_proponente,substr(e.natureza,1,2),sum(l.valor_grupo_centavos)
      FROM empenho_desembolso_fed08b l
      JOIN empenho_fed08b e ON e.id_empenho=l.id_empenho AND e.nr_convenio=l.nr_convenio
      JOIN desembolso_fluxo d ON d.id_desembolso=l.id_desembolso
      JOIN desembolso_empenho_qa_fed08b qa ON qa.id_desembolso=l.id_desembolso
      WHERE qa.status_reconciliacao='reconciliado'
      GROUP BY d.ibge_proponente,substr(e.natureza,1,2)""").fetchall()
    byibge=collections.defaultdict(dict)
    for ibge,code,value in units:byibge[ibge][code]=value
    assert {code:sum(byibge[ibge].get(code,0) for ibge in byibge) for code in EXPECTED}==EXPECTED
    count_byibge=dict(db.execute("""SELECT d.ibge_proponente,count(*)
      FROM desembolso_fluxo d JOIN desembolso_empenho_qa_fed08b qa ON qa.id_desembolso=d.id_desembolso
      WHERE qa.status_reconciliacao='reconciliado' GROUP BY d.ibge_proponente"""))
    failures=collections.Counter()
    for ibge,stat,cnt in db.execute("""SELECT d.ibge_proponente,qa.status_reconciliacao,count(*)
      FROM desembolso_fluxo d JOIN desembolso_empenho_qa_fed08b qa ON qa.id_desembolso=d.id_desembolso
      WHERE qa.status_reconciliacao!='reconciliado' GROUP BY 1,2"""):failures[(ibge,stat)]=cnt
    assert sum(count_byibge.values())==2535 and sum(failures.values())==2
    index=jload(api/"municipios.json")
    municipalities=index["municipios"]
    assert len(municipalities)==34
    for m in municipalities:
        ibge=m["ibge"]
        doc_path=api/"municipios"/(ibge+".json")
        doc=jload(doc_path)
        doc.setdefault("evidencias_auditadas",{})["desembolsos_conciliados_natureza_empenho"]={
          "etapa":"transferido","municipio_papel":"sede_executor",
          "codigo_orcamentario_fonte":"siconv_empenho.NATUREZA_DESPESA",
          "natureza_codigos_iniciais_33_34_44_valor_grupos_centavos":{k:byibge.get(ibge,{}).get(k,0) for k in EXPECTED},
          "desembolsos_com_ponte_e_soma_reconciliada":count_byibge.get(ibge,0),
          "desembolsos_divergentes":failures[(ibge,"divergente")],
          "desembolsos_sem_ponte":failures[(ibge,"sem_ponte")],
          "qa_status":"em_revisao","natureza_44_e_investimento_pago":False,
          "valor_investimento_executado_centavos":None,
          "ressalva":"Natureza associada ao empenho no fluxo de desembolso, nao GND4 pago ao favorecido ou investimento municipal executado."
        }
        assert doc["totais_por_dimensao"]["federal_pagamentos_diretos_investimento_centavos"] is None
        jsave(doc_path,doc)
    grouped={}
    for m in municipalities:
        sub=m["subregiao_rmrp_codigo"]
        group=grouped.setdefault(sub,collections.Counter())
        ibge=m["ibge"]
        group["desembolsos_reconciliados"]+=count_byibge.get(ibge,0)
        for k in EXPECTED:group["prefixo_"+k+"_centavos"]+=byibge.get(ibge,{}).get(k,0)
    for sub,amounts in grouped.items():
        p=api/"subregioes"/(sub+".json")
        j=jload(p)
        j["evidencias_de_natureza_do_empenho_na_etapa_desembolso"]={
         **amounts,"qa_status":"em_revisao","investimento_pago_homologado":False}
        jsave(p,j)
    assert len(grouped)==4
    # Annual disbursement classification must be traceable to source year, not payment date.
    annual=db.execute("""SELECT d.ano_desembolso,substr(e.natureza,1,2),sum(l.valor_grupo_centavos)
       FROM empenho_desembolso_fed08b l JOIN empenho_fed08b e
       ON e.id_empenho=l.id_empenho AND e.nr_convenio=l.nr_convenio
       JOIN desembolso_fluxo d ON d.id_desembolso=l.id_desembolso
       JOIN desembolso_empenho_qa_fed08b qa ON qa.id_desembolso=d.id_desembolso
       WHERE qa.status_reconciliacao='reconciliado'
       GROUP BY d.ano_desembolso,substr(e.natureza,1,2)""").fetchall()
    year=collections.defaultdict(dict)
    for y,code,v in annual:year[str(y)][code]=v
    for y in range(2008,2027):
        p=api/"anos"/(str(y)+".json")
        d=jload(p)
        d["desembolso_por_natureza_codigo_empenho_centavos"]={
         "prefixos":{code:year.get(str(y),{}).get(code,0) for code in EXPECTED},
         "etapa":"transferido","qa_status":"em_revisao","comprovacao_gnd4_pago":False}
        assert d["comprovacao_gnd4_pago"] is False
        jsave(p,d)
    manifest=jload(api/"manifest.json")
    manifest["coverage"]["desembolsos_com_natureza_empenho_e_grupos_reconciliados"]=2535
    manifest["coverage"]["desembolsos_em_revisao_sem_ponte_ou_valor_divergente"]=2
    manifest["sources_fed09"]=[
        {"module":"siconv_empenho","sha256":"755b29d84bff3ad65482364035d880f15682637f901486974dfa24b1e72d8a59"},
        {"module":"siconv_empenho_desembolso","sha256":"07c48daf6e4892faa634377fe84e867a6f6ba04d310582f5a53fd58176bfd825"},
        {"module":"siconv_empenho_cipi","sha256":"5b4ef56013025d3d26d26a765eb2e690d93fa2916a70886d746575b2bffb4108"}]
    manifest["publication_gate"]="blocked_no_gnd4_paid_or_physical_execution_homologation"
    manifest["public_release_authorized"]=False
    jsave(api/"manifest.json",manifest)
    pending=jload(api/"pendencias.json")
    pending.setdefault("financeiro",[]).append("2.535 desembolsos vinculados a grupos de empenho conciliados com natureza codigo; nao equivalem a pagamento final GND4.")
    pending["financeiro"].append("Um desembolso sem ponte e outro com diferenca de R$ 88.000,00 permanecem fora da classificacao.")
    jsave(api/"pendencias.json",pending)
    # Prevent source-tagged classified transfers from being mistaken for paid projects
    for item in (api/"projetos").glob("*.json"):
        p=jload(item)
        assert p["valores_investimento_pago_centavos"] is None
        assert not p["localizacao_fisica"]["pontos"]
    db.close()
    from pipeline.qa.validate_rmrp_api_v3_fed07 import validate
    qa=validate(api)
    assert qa["technical_checks_passed"]>=1603
    assert sum(x["prefixo_44_centavos"] for x in grouped.values())==EXPECTED["44"]
    assert sum(x["desembolsos_reconciliados"] for x in grouped.values())==2535
    report={"api_qa":qa,"year_count":19,"municipios":34,"subregioes":4,
            "desembolsos_reconciliados":2535,"desembolsos_pendentes":2,
            "classification_prefix_sums_centavos":EXPECTED,
            "public_release_authorized":False}
    jsave(output_site/"QA_FED09_NATUREZA_EMPENHO_PRIVADO.json",report)
    with zipfile.ZipFile(outzip,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in output_site.rglob("*"):
            if p.is_file() and p.name!=".rmrp-fed07-private-preview":
                z.write(p,p.relative_to(output_site))
    with zipfile.ZipFile(outzip) as z:assert z.testzip() is None
    report["archive_bytes"]=outzip.stat().st_size
    report["archive_sha256"]=sha(outzip)
    return report

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("source_site",type=Path);ap.add_argument("sqlite",type=Path)
    ap.add_argument("output_site",type=Path);ap.add_argument("output_zip",type=Path)
    x=ap.parse_args()
    print(json.dumps(build(x.source_site,x.sqlite,x.output_site,x.output_zip),ensure_ascii=False))
