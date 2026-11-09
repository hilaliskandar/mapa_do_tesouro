#!/usr/bin/env python3
"""RMSJRP G06: conditional 2027-2030 stress tests; not forecasts or causal estimates."""
from __future__ import annotations
import csv, hashlib, json, os
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from deployment.download_r2_source import download_r2_object

P=Path("build/rmsjrp-g06")
P.mkdir(parents=True,exist_ok=True)
CONFIG=Path("editorial/rmsjrp/PARAMETROS_G06_2027_2030.json")
cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
assert cfg["base_year"]==2025 and cfg["horizon"]==[2027,2028,2029,2030]
assert len(cfg["scenarios"])==3 and len({s["id"] for s in cfg["scenarios"]})==3
source_key="rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv"
source_sha="1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5"
source_path=P/"municipios_g04.csv"
download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],
 api_token=os.environ["CLOUDFLARE_API_TOKEN"],bucket=os.environ["CLOUDFLARE_R2_BUCKET"],
 object_key=source_key,output=source_path)
assert hashlib.sha256(source_path.read_bytes()).hexdigest()==source_sha
with source_path.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f,delimiter=";"))
assert len(rows)==481
r={ (x["cod_ibge"],int(x["ano"])):x for x in rows}
assert len(r)==481
municipal_codes=sorted({k[0] for k in r})
assert len(municipal_codes)==37
Q=Decimal("0.01")
def dec(x):return Decimal(str(x)) if x not in ("",None) else None
def f(x):return str(x.quantize(Q,rounding=ROUND_HALF_UP)) if x is not None else ""
def write(name,data):
    assert data
    file=P/name
    with file.open("w",encoding="utf-8",newline="") as f_out:
        w=csv.DictWriter(f_out,fieldnames=list(data[0]),delimiter=";");w.writeheader();w.writerows(data)
    return {"name":name,"sha256":hashlib.sha256(file.read_bytes()).hexdigest(),"rows":len(data)}
def investment_ratio(x):
    invest=dec(x["dca_investimentos_liquidada_real_set2026"])
    revenue=dec(x["dca_receita_corrente_bruta_real_set2026"])
    return invest/revenue if invest is not None and revenue is not None and revenue>0 else None

out=[]
for code in municipal_codes:
    base=r[code,2025]; prev=r[code,2024]
    rev=dec(base["dca_receita_corrente_bruta_real_set2026"])
    current=dec(base["dca_despesa_corrente_liquidada_real_set2026"])
    invest=dec(base["dca_investimentos_liquidada_real_set2026"])
    fpm=dec(base["dca_fpm_cota_mensal_real_set2026"])
    share25=investment_ratio(base);share24=investment_ratio(prev)
    for s in cfg["scenarios"]:
        growth_rev=dec(s["revenue_real_growth"]);growth_current=dec(s["current_expenditure_real_growth"])
        for year in cfg["horizon"]:
            duration=year-2025  # 2026 explicitly a hypothetical, not observed, bridge
            t=Decimal(duration)/Decimal(5)
            modeled_rev=rev*(1+growth_rev)**duration if rev is not None else None
            modeled_current=current*(1+growth_current)**duration if current is not None else None
            if share25 is None: share=None
            elif s["investment_share_method"]=="keep_2025_share":share=share25
            elif s["investment_share_method"]=="multiply_2025_share":
                ratio=dec(s["investment_share_factor_2030"])
                share=share25*(Decimal(1)+(ratio-1)*t)
            elif s["investment_share_method"]=="recover_half_positive_gap_to_2024_by_2030":
                share=share25+max((share24 or share25)-share25,Decimal(0))*dec(s["positive_gap_fraction_2030"])*t
            else:raise ValueError("unknown investment share method")
            modeled_invest=modeled_rev*share if modeled_rev is not None and share is not None else None
            cushion=(modeled_rev-modeled_current) if modeled_rev is not None and modeled_current is not None else None
            shock_base=fpm*dec(cfg["independent_sensitivity"]["fpm_real_shock_fraction"]) if fpm is not None else None
            out.append({"cod_ibge":code,"municipio":base["municipio"],"subregiao":base["subregiao"],
             "cenario":s["id"],"ano":year,"precos":"set_2026","tipo":"simulacao_condicional_nao_previsao",
             "base_2025_receita_real_R$":f(rev),"base_2025_despesa_corrente_real_R$":f(current),
             "base_2025_investimento_real_R$":f(invest),
             "base_2025_fpm_real_R$":f(fpm),
             "razao_investimento_2025_pct":f(share25*100) if share25 is not None else "",
             "razao_investimento_2024_pct":f(share24*100) if share24 is not None else "",
             "crescimento_receita_real_hipotetico_pct":f(growth_rev*100),
             "crescimento_despesa_corrente_real_hipotetico_pct":f(growth_current*100),
             "razao_investimento_projetada_pct":f(share*100) if share is not None else "",
             "receita_corrente_real_condicional_R$":f(modeled_rev),
             "despesa_corrente_real_condicional_R$":f(modeled_current),
             "investimento_real_condicional_R$":f(modeled_invest),
             "diferenca_receita_menos_despesa_corrente_R$":f(cushion),
             "sensibilidade_fpm_queda_10pct_base_2025_R$":f(shock_base),
             "populacao_futura":"","receita_per_capita_futura":"","investimento_per_capita_futuro":"",
             "ponte_2026":"hipotetica_nao_observada","efeito_lc200_estatuto":"nao_estimado",
             "fonte_base":"G04_R2_SHA_"+source_sha})
assert len(out)==444 and len({(a["cod_ibge"],a["ano"],a["cenario"]) for a in out})==444
assert all(a["populacao_futura"]=="" and a["investimento_per_capita_futuro"]=="" for a in out)

groups={"São José do Rio Preto":14,"José Bonifácio":11,"Tanabi":6,"Nova Granada":6}
assert {g:sum(r[c,2025]["subregiao"]==g for c in municipal_codes) for g in groups}==groups
aggregates=[]
fields_to_sum=[
 "base_2025_receita_real_R$","base_2025_despesa_corrente_real_R$","base_2025_investimento_real_R$",
 "base_2025_fpm_real_R$","receita_corrente_real_condicional_R$",
 "despesa_corrente_real_condicional_R$","investimento_real_condicional_R$",
 "diferenca_receita_menos_despesa_corrente_R$","sensibilidade_fpm_queda_10pct_base_2025_R$"]
for s in cfg["scenarios"]:
    for year in cfg["horizon"]:
        selection=[a for a in out if a["cenario"]==s["id"] and a["ano"]==year]
        assert len(selection)==37
        for group in [*groups,"RMSJRP"]:
            items=[a for a in selection if group=="RMSJRP" or a["subregiao"]==group]
            expected=37 if group=="RMSJRP" else groups[group]
            assert len(items)==expected
            item={"territorio":group,"cenario":s["id"],"ano":year,
                  "municipios_esperados":expected,"precos":"set_2026",
                  "tipo":"simulacao_condicional_nao_previsao"}
            for field in fields_to_sum:
                vals=[dec(x[field]) for x in items]
                valid=sum(v is not None for v in vals)
                item[field+"_observados"]=valid
                # Aggregation based on unrounded numbers needs tolerance for rounded municipality inputs.
                item[field]=f(sum(vals,Decimal(0))) if valid==expected else ""
            rev=dec(item["receita_corrente_real_condicional_R$"])
            inv=dec(item["investimento_real_condicional_R$"])
            item["razao_investimento_projetada_pct"]=f(100*inv/rev) if rev is not None and inv is not None and rev>0 else ""
            item["populacao_futura"]=""
            item["efeito_lc200_estatuto"]="nao_estimado"
            aggregates.append(item)
assert len(aggregates)==60

# Reconcile rounded monetary totals with subregions; 37 * R$0.005 possible in worst case.
for scenario in [s["id"] for s in cfg["scenarios"]]:
 for year in cfg["horizon"]:
    region=next(a for a in aggregates if a["cenario"]==scenario and a["ano"]==year and a["territorio"]=="RMSJRP")
    subs=[a for a in aggregates if a["cenario"]==scenario and a["ano"]==year and a["territorio"]!="RMSJRP"]
    for field in fields_to_sum:
        if not region[field]:continue
        assert all(x[field] for x in subs)
        delta=abs(sum(dec(x[field]) for x in subs)-dec(region[field]))
        assert delta<=Decimal("0.02"),(scenario,year,field,delta)

artifacts=[write("G06_SIMULACOES_444_MUNICIPIOS.csv",out),
           write("G06_SIMULACOES_60_TERRITORIOS.csv",aggregates)]
qa={"status":"pass","n_municipal":444,"n_territorial":60,"n_cities":37,"n_subregions":4,
"years":cfg["horizon"],"scenarios":[x["id"] for x in cfg["scenarios"]],
"source_sha256":source_sha,"config_sha256":hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
"missing_2025_counts":{k:sum(not a[k] for a in out if a["ano"]==2027 and a["cenario"]=="continuidade")
 for k in ["base_2025_receita_real_R$","base_2025_despesa_corrente_real_R$","base_2025_investimento_real_R$","base_2025_fpm_real_R$"]},
"limitations":["Conditional parameters set for stress-testing, not estimated","No observed 2026 or forecast 2026",
"No future population or per capita forecast","No project-level execution forecast",
"No automatic FPM cut or IBS municipal projection","No causal inference from LC200"],
"artifacts":artifacts,
"region_2030":[{k:v for k,v in a.items() if k in ("cenario","ano","receita_corrente_real_condicional_R$","despesa_corrente_real_condicional_R$","investimento_real_condicional_R$","razao_investimento_projetada_pct")} for a in aggregates if a["territorio"]=="RMSJRP" and a["ano"]==2030]}
(P/"QA_G06.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"municipal":444,"territorial":60,
  "missing":qa["missing_2025_counts"],"region_2030":qa["region_2030"]},ensure_ascii=False))
