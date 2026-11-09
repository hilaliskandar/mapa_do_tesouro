#!/usr/bin/env python3
"""G06-E: audit 2023-25 exposure indicators, not federal program impact."""
from __future__ import annotations
import csv, hashlib, json, os
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from deployment.download_r2_source import download_r2_object

ROOT=Path("build/rmsjrp-g06e");ROOT.mkdir(parents=True,exist_ok=True)
KEY="rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv"
SHA="1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5"
src=ROOT/"G04_MUNICIPIOS.csv"
download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],
 api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=os.environ["CLOUDFLARE_R2_BUCKET"],
 object_key=KEY,output=src)
assert hashlib.sha256(src.read_bytes()).hexdigest()==SHA
with src.open(encoding="utf-8-sig",newline="") as f: data=list(csv.DictReader(f,delimiter=";"))
assert len(data)==481
indexed={(x["cod_ibge"],int(x["ano"])):x for x in data}
assert len(indexed)==481
cities=sorted({k[0] for k in indexed})
assert len(cities)==37
groups={"São José do Rio Preto":14,"José Bonifácio":11,"Tanabi":6,"Nova Granada":6}
assert Counter(indexed[(c,2025)]["subregiao"] for c in cities)==groups
# Each row is an exposure proxy category, not a summable decomposition.
# The gross tax aggregate and principal taxes overlap and MUST NOT be added.
classes=[
 ("fpm_cota_mensal","transferencia_constitucional_federal","dca_fpm_cota_mensal","reparticao_CF_art159","observado_serie_dca","Não confundir com transferências discricionárias"),
 ("icms_cota_parte","transferencia_constitucional_estadual","dca_icms_cota_parte","reparticao_constitucional_estadual","observado_serie_dca","Não constitui desembolso discricionário da União"),
 ("ipva_cota_parte","transferencia_constitucional_estadual","dca_ipva_cota_parte","reparticao_constitucional_estadual","observado_serie_dca","Não constitui desembolso discricionário da União"),
 ("iss_principal","tributo_municipal_proprio","dca_iss_principal","CF_competencia_municipal","observado_serie_dca","Principal; exclui componentes acessórios; IBS separado"),
 ("iptu_principal","tributo_municipal_proprio","dca_iptu_principal","CF_competencia_municipal","observado_serie_dca","Principal; não é receita adicional à tributária bruta"),
 ("itbi_principal","tributo_municipal_proprio","dca_itbi_principal","CF_competencia_municipal","observado_serie_dca","Principal; sensível ao ciclo imobiliário"),
 ("receita_tributaria_bruta","agregado_contabil_nao_aditivo","dca_receita_tributaria_bruta","DCA_agregado","observado_serie_dca","Contém componentes tributários; não somar a ISS IPTU ITBI"),
 ("fundeb_ou_complementacao","transferencia_educacional_regime_proprio",None,"CF_art212A_e_norma_setorial","pendente_fonte_individualizada","Não inferir do FPM ou receita corrente"),
 ("sus_fundo_a_fundo","transferencia_legal_saude",None,"normas_sus_especificas","pendente_fonte_individualizada","Separar repasse regular de transferência voluntária"),
 ("transferencias_legais_federais_outras","transferencia_legal_federal",None,"norma_programa","pendente_fonte_individualizada","Classificar por programa/lei e exercício"),
 ("convenios_pac_contratos_repasse","transferencia_discricionaria_ou_capital",None,"LRF_art25_e_instrumento","pendente_instrumento_e_execucao","Precisa de identificação de programa, empenho e pagamento federal"),
 ("emendas_transferencias_especiais","emenda_ou_transferencia_especial",None,"CF_166A_e_regulacao","pendente_instrumento_e_execucao","Ver modalidade e pagamentos, não supor teto federal"),
]
assert len(classes)==12
D=Decimal
q=D("0.01")
def v(x):return D(x) if x not in ("",None) else None
def m(x):return str(x.quantize(q,rounding=ROUND_HALF_UP)) if x is not None else ""
rows=[]
for c in cities:
    by={year:indexed[c,year] for year in (2023,2024,2025)}
    assert len({x["municipio"] for x in by.values()})==1
    base=by[2025]
    denominator=v(base["dca_receita_corrente_bruta_nominal"])
    assert denominator is not None and denominator>0
    for name,kind,field,norm,status,warning in classes:
        rec={"cod_ibge":c,"municipio":base["municipio"],"subregiao":base["subregiao"],
             "categoria":name,"natureza_juridica":kind,"base_legal_classificatoria":norm,
             "natureza_medida":"proxy_contabil_nao_impacto","estado_evidencia":status,
             "federal_discricionaria":"sim" if name=="convenios_pac_contratos_repasse" else "nao_determinado" if name in ("fundeb_ou_complementacao","transferencias_legais_federais_outras","emendas_transferencias_especiais") else "nao",
             "despesa_sujeita_ao_teto_federal":"exige_classificacao_programa" if name in ("convenios_pac_contratos_repasse","transferencias_legais_federais_outras","emendas_transferencias_especiais","fundeb_ou_complementacao","sus_fundo_a_fundo") else "nao_inferivel_de_receita_municipal",
             "numerador_fonte_campo":(field or ""),"denominador":"dca_receita_corrente_bruta_nominal_2025",
             "observacao":warning,"federal_orgao":"","programa_federal":"","acao_federal":"",
             "instrumento_id":"","empenho_federal":"","pagamento_federal":"",
             "recebimento_municipal_conciliado":"","empenho_municipal":"",
             "medicao_execucao":"","liquidacao_municipal_relacionada":"",
             "atribuicao_causal_lc200":"nao_demonstrada",
             "fonte_snapshot_sha256":SHA}
        for year in (2023,2024,2025):
            nominal=v(by[year][field+"_nominal"]) if field else None
            real=v(by[year][field+"_real_set2026"]) if field else None
            rec[f"valor_{year}_nominal_R$"]=m(nominal)
            rec[f"valor_{year}_real_set2026_R$"]=m(real)
        current=v(rec["valor_2025_nominal_R$"])
        rec["participacao_receita_corrente_2025_pct"]=m(D(100)*current/denominator) if current is not None else ""
        rows.append(rec)
assert len(rows)==444
assert len({(x["cod_ibge"],x["categoria"]) for x in rows})==444
assert all(x["valor_2025_nominal_R$"]=="" for x in rows if x["estado_evidencia"]!="observado_serie_dca")
assert all(x["atribuicao_causal_lc200"]=="nao_demonstrada" for x in rows)
assert all(x["pagamento_federal"]=="" for x in rows)
summaries=[]
for group in list(groups)+["RMSJRP"]:
    cc=[x for x in cities if group=="RMSJRP" or indexed[x,2025]["subregiao"]==group]
    expected=37 if group=="RMSJRP" else groups[group]
    assert len(cc)==expected
    den=sum(v(indexed[x,2025]["dca_receita_corrente_bruta_nominal"]) for x in cc)
    for name,kind,field,norm,status,warning in classes:
        subset=[x for x in rows if x["cod_ibge"] in cc and x["categoria"]==name]
        assert len(subset)==expected
        nums=[v(x["valor_2025_nominal_R$"]) for x in subset]
        have=sum(x is not None for x in nums)
        total=sum((x for x in nums if x is not None),D(0)) if have==expected else None
        summaries.append({"territorio":group,"municipios_esperados":expected,"municipios_com_valor":have,
         "categoria":name,"natureza_juridica":kind,"estado_evidencia":status,
         "valor_2025_nominal_R$":m(total),
         "participacao_receita_corrente_pct":m(D(100)*total/den) if total is not None else "",
         "denominador_receita_corrente_R$":m(den),
         "nao_somar_categorias":"sim","efeito_lc200":"nao_estimada"})
assert len(summaries)==60
assert all(x["valor_2025_nominal_R$"]=="" for x in summaries if x["municipios_com_valor"]==0)
# Each regional total equals sum of four territorial totals for that SAME category.
for name,*_ in classes:
    whole=next(x for x in summaries if x["territorio"]=="RMSJRP" and x["categoria"]==name)
    parts=[x for x in summaries if x["territorio"]!="RMSJRP" and x["categoria"]==name]
    if whole["valor_2025_nominal_R$"]:
        assert sum(v(x["valor_2025_nominal_R$"]) for x in parts)==v(whole["valor_2025_nominal_R$"])
    else: assert all(x["valor_2025_nominal_R$"]=="" for x in parts)
def output(name,records):
    p=ROOT/name
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=records[0].keys(),delimiter=";")
        w.writeheader();w.writerows(records)
    return {"name":name,"rows":len(records),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
art=[output("G06E_MATRIZ_EXPOSICAO_37x12.csv",rows),output("G06E_RESUMO_TERRITORIAL_5x12.csv",summaries)]
qa={"status":"pass","source_sha256":SHA,"universo_municipios":37,
"categorias":len(classes),"municipio_categoria":444,"territorio_categoria":60,
"2025_fundamentado_serie_DCA_categorias":7,"pendentes_sem_imputacao":5,
"base_price":"setembro_2026","observacoes":["7 categorias contábeis com sobreposição; não somar",
"FPM e cota-parte do ICMS/IPVA são transferências constitucionais distintas",
"5 modalidades dependem de outras fontes e são NA, nunca zero",
"Sem identificação de convênios, empenhos e pagamentos federais",
"Sem atribuição causal da LC 200 e sem supor teto municipal"],
"artifacts":art,
"regional_2025":[{"categoria":x["categoria"],"valor":x["valor_2025_nominal_R$"],
"participacao_pct":x["participacao_receita_corrente_pct"],"cobertura":x["municipios_com_valor"]}
for x in summaries if x["territorio"]=="RMSJRP"]}
(ROOT/"QA_G06E.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","municipios":37,"linhas":444,"resumo":60,
"region":qa["regional_2025"]},ensure_ascii=False))
