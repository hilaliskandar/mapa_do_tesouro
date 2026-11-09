#!/usr/bin/env python3
"""Validate G05-D source-to-claim matrix against immutable private TCESP G05-B source."""
import csv,hashlib,json,os
from decimal import Decimal
from pathlib import Path
from deployment.download_r2_source import download_r2_object
ROOT=Path("build/rmsjrp-g05d")
ROOT.mkdir(parents=True,exist_ok=True)
KEY="rmsjrp/g05/2026_11_09/programas_acoes/G05B_TRANSICOES_PROGRAMA_ACAO_2023_2025.csv"
SHA="02bbf839bf849fc374ee3dcb64aad8dc9695c6972cfaec2cff89ee741ccd5d31"
src=ROOT/"fonte_tcesp_g05b.csv"
download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],
  bucket=os.environ["CLOUDFLARE_R2_BUCKET"],object_key=KEY,output=src)
assert hashlib.sha256(src.read_bytes()).hexdigest()==SHA,"fonte_R2_divergente"
matrix=Path("editorial/rmsjrp/MATRIZ_EVIDENCIAS_G05D_2026_11_09.csv")
with matrix.open(encoding="utf-8",newline="") as f:
  claims=list(csv.DictReader(f,delimiter=";"))
with src.open(encoding="utf-8",newline="") as f:
  original=list(csv.DictReader(f,delimiter=";"))
assert len(claims)==10
assert len({(r["municipio"],r["nivel"],r["orgao"],r["programa"],r["acao"]) for r in claims})==10
orgs={"Prefeitura":"PREFEITURA MUNICIPAL DE ","SeMAE":"SERVIÇO MUNICIPAL AUTONÔMO DE ÁGUA E ESGOTO-SEMAE."}
results=[]
for c in claims:
  level="acao" if c["nivel"]=="ação" else c["nivel"]
  matches=[r for r in original if r["inicio"]=="2024" and r["fim"]=="2025"
    and r["municipio"]==c["municipio"] and r["nivel"]==level
    and r["cd_programa"]==c["programa"] and r["cd_acao"]==c["acao"]
    and (r["orgao"]==orgs["SeMAE"] if c["orgao"]=="SeMAE" else r["orgao"].startswith(orgs["Prefeitura"]))]
  assert len(matches)==1,(c["municipio"],c["programa"],c["acao"],len(matches))
  m=matches[0]
  def money(x):
    return Decimal(x) if x else None
  for year,source_field in ((2024,"valor_inicio_centavos"),(2025,"valor_fim_centavos")):
    claim=money(c[f"liquidado_{year}_nominal_R$"])
    orig=money(m[source_field])
    assert (claim is None)==(orig is None),(year,c["municipio"],c["programa"])
    if claim is not None:assert claim*100==orig,(year,c["municipio"],claim,orig)
  assert money(c["diferenca_nominal_R$"])*100==Decimal(m["variacao_centavos"]),c
  assert c["fonte_contabil"]==KEY
  assert c["url_documento_primario"].startswith("https://")
  results.append({"municipio":c["municipio"],"programa":c["programa"],"acao":c["acao"],
                  "nivel":c["nivel"],"diferenca_reais":c["diferenca_nominal_R$"],"status":"pass"})
qa={"status":"pass","chaves":len(results),"fonte_sha256":SHA,
    "matriz_sha256":hashlib.sha256(matrix.read_bytes()).hexdigest(),
    "scope":"2024/2025 group44 liquidado, exact org/program/action keys",
    "all_values_match_cents":True,
    "limitations":["No contract-level reconciliation","No causal attribution","Missing program in 2025 is not proof of cancelled works"],
    "results":results}
(ROOT/"QA_G05D_CONTABIL.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":qa["status"],"chaves":qa["chaves"],
                  "matriz_sha256":qa["matriz_sha256"],"all_values_match_cents":True}))
