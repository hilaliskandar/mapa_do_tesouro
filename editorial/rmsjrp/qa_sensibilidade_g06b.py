#!/usr/bin/env python3
"""G06-B: independent ±1 percentage-point annual-growth tests; influence of metropolitan pole."""
from __future__ import annotations
import csv, hashlib, json, os
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from deployment.download_r2_source import download_r2_object

ROOT=Path("build/rmsjrp-g06b");ROOT.mkdir(parents=True,exist_ok=True)
PREFIX="rmsjrp/g06/2026_11_09/cenarios_v1/"
CFG=Path("editorial/rmsjrp/PARAMETROS_G06_2027_2030.json")
config=json.loads(CFG.read_text(encoding="utf-8"))
smap={x["id"]:x for x in config["scenarios"]}
assert len(smap)==3
def fetch(name,expected=None):
    output=ROOT/name
    download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],
        bucket=os.environ["CLOUDFLARE_R2_BUCKET"],object_key=PREFIX+name,output=output)
    sha=hashlib.sha256(output.read_bytes()).hexdigest()
    if expected:assert sha==expected,(name,sha,expected)
    return output
manifest=json.loads(fetch("QA_G06.json").read_text(encoding="utf-8"))
assert manifest["status"]=="pass" and manifest["n_municipal"]==444 and manifest["n_territorial"]==60
assert manifest["config_sha256"]==hashlib.sha256(CFG.read_bytes()).hexdigest()
artifact_sha={a["name"]:a["sha256"] for a in manifest["artifacts"]}
def read(name):
    with fetch(name,artifact_sha[name]).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))
rows=read("G06_SIMULACOES_444_MUNICIPIOS.csv")
regions=read("G06_SIMULACOES_60_TERRITORIOS.csv")
assert len(rows)==444 and len(regions)==60
P=Decimal("0.01")
ONE=Decimal(1)
def dec(s):return Decimal(str(s)) if s not in ("",None) else None
def monetary(x):return str(x.quantize(P,rounding=ROUND_HALF_UP))
def save(name,rr):
    assert rr
    path=ROOT/name
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0]),delimiter=";")
        w.writeheader();w.writerows(rr)
    return {"name":name,"rows":len(rr),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
sensitivity=[]
pole=[]
extremes=[]
# Do not modify scenario v1. Each perturbation holds other scenario parameters fixed.
for scen,settings in smap.items():
    for year in (2027,2028,2029,2030):
        subset=[r for r in rows if r["cenario"]==scen and int(r["ano"])==year]
        assert len(subset)==37
        n=year-2025
        for variable in ("receita","despesa_corrente"):
            g=dec(settings["revenue_real_growth"] if variable=="receita" else settings["current_expenditure_real_growth"])
            for direction,delta in (("menos_1pp",Decimal("-0.01")),("mais_1pp",Decimal("0.01"))):
                agg_delta=Decimal(0)
                agg_invest_delta=Decimal(0)
                for x in subset:
                    base_key=("base_2025_receita_real_R$" if variable=="receita" else "base_2025_despesa_corrente_real_R$")
                    value=dec(x[base_key])
                    assert value is not None
                    effect=value*((ONE+g+delta)**n-(ONE+g)**n)
                    agg_delta+=effect
                    if variable=="receita":
                        share=dec(x["razao_investimento_projetada_pct"])
                        if share is not None:agg_invest_delta+=effect*share/100
                sensitivity.append({"cenario":scen,"ano":year,"variavel":variable,
                    "choque_independente":direction,"variacao_taxa_anual_pp":monetary(100*delta),
                    "diferenca_nivel_real_em_relacao_g06v1_R$":monetary(agg_delta),
                    "diferenca_investimento_real_mecanica_R$":monetary(agg_invest_delta) if variable=="receita" else "",
                    "interpretacao":"teste_de_sensibilidade_nao_efeito_lc200",
                    "ponte_2026":"hipotetica"})
        if year==2030:
            for grp in ("polo","demais"):
                rr=[x for x in subset if (x["cod_ibge"]=="3549805")==(grp=="polo")]
                expected=1 if grp=="polo" else 36
                assert len(rr)==expected
                revenue=sum(dec(x["receita_corrente_real_condicional_R$"]) for x in rr)
                investment=sum(dec(x["investimento_real_condicional_R$"]) for x in rr)
                expense=sum(dec(x["despesa_corrente_real_condicional_R$"]) for x in rr)
                pole.append({"cenario":scen,"ano":year,"recorte":grp,
                    "municipios":expected,"receita_corrente_real_R$":monetary(revenue),
                    "investimento_real_R$":monetary(investment),
                    "despesa_corrente_real_R$":monetary(expense),
                    "proporcao_investimento_na_receita_pct":monetary(investment/revenue*100)})
        # Extreme values are review flags, not exclusion.
        for x in subset:
            ratio=dec(x["razao_investimento_projetada_pct"])
            if ratio is not None and (ratio>20 or ratio<0):
                extremes.append({"cenario":scen,"ano":year,"cod_ibge":x["cod_ibge"],"municipio":x["municipio"],
                   "razao_investimento_pct":x["razao_investimento_projetada_pct"],
                   "limiar_de_alerta_pct":20,"acao":"revisar valor-base 2024 e nao excluir automaticamente"})
assert len(sensitivity)==48 and len(pole)==6
# Reconcile pole and remainder to metro totals; monetary rounding tolerance 2 cents.
for x in regions:
    if int(x["ano"])!=2030 or x["territorio"]!="RMSJRP":continue
    rr=[p for p in pole if p["cenario"]==x["cenario"]]
    assert len(rr)==2
    for f1,f2 in [("receita_corrente_real_condicional_R$","receita_corrente_real_R$"),
                  ("investimento_real_condicional_R$","investimento_real_R$"),
                  ("despesa_corrente_real_condicional_R$","despesa_corrente_real_R$")]:
        assert abs(sum(dec(z[f2]) for z in rr)-dec(x[f1]))<=Decimal("0.02"),(x["cenario"],f1)
artifacts=[
save("G06B_SENSIBILIDADES_48.csv",sensitivity),
save("G06B_POLO_DEMAIS_2030.csv",pole)]
if extremes:
    artifacts.append(save("G06B_ALERTAS_EXTREMOS.csv",extremes))
qa={"status":"pass","base_g06_source_manifest_sha256":hashlib.sha256((ROOT/"QA_G06.json").read_bytes()).hexdigest(),
"scenario_count":len(smap),"sensitivity_rows":len(sensitivity),
"polo_demais_rows":len(pole),"extreme_flags":len(extremes),
"extreme_threshold_pct":20,"not_forecast":True,"not_causal":True,
"artifacts":artifacts,
"summary_2030":[{"cenario":s,
    "sensibilidades":[{k:rr[k] for k in ("variavel","choque_independente","diferenca_nivel_real_em_relacao_g06v1_R$","diferenca_investimento_real_mecanica_R$")} for rr in sensitivity if rr["cenario"]==s and rr["ano"]==2030],
    "polo_share_investment_pct":monetary(dec(next(x for x in pole if x["cenario"]==s and x["recorte"]=="polo")["investimento_real_R$"])/sum(dec(x["investimento_real_R$"]) for x in pole if x["cenario"]==s)*100)}
 for s in smap],
"caveats":["±1 pp is hypothetical and isolated, not a standard error or confidence interval",
"investment change when revenue shocked is mechanical because investment share held constant",
"no future population","no attribution to LC200 or proposed PLOA 2027"]}
(ROOT/"QA_G06B.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","rows":48,"pole":6,"extremes":len(extremes),"summary_2030":qa["summary_2030"]},ensure_ascii=False))
