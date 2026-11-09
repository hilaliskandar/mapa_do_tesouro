#!/usr/bin/env python3
"""QA candidate contract and works references without making false financial joins."""
from __future__ import annotations
import csv,hashlib,json,os,re,unicodedata
from collections import defaultdict
from decimal import Decimal
from difflib import SequenceMatcher
from pathlib import Path
from deployment.download_r2_source import download_r2_object
ROOT=Path("build/rmsjrp-g05d-vinculos");ROOT.mkdir(parents=True,exist_ok=True)
FILES={
"contratos.csv":("rmsjrp/g05d/2026_11_09/olimpia_contratos/CONTRATOS_OLIMPIA_2024_2025_INVENTARIO.csv","e62c12c555843d8a3600b223096921cfe6e742987d1c9b0a65fd2ea1e6eb0b8f"),
"obras.csv":("rmsjrp/g05d/2026_11_09/olimpia_obras/OBRAS_OLIMPIA_2024_2025_INVENTARIO.csv","c9c304f6a3b0e83dcd168ebd2ceb539c43c934cd08ef384ddc3d6b62eea51689")}
for name,(key,sha) in FILES.items():
    dest=ROOT/name
    download_r2_object(account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],api_token=os.environ["CLOUDFLARE_API_TOKEN"],
        bucket=os.environ["CLOUDFLARE_R2_BUCKET"],object_key=key,output=dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha,(name,"source sha")
def csvread(path):
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter=";"))
contracts=csvread(ROOT/"contratos.csv")
works=csvread(ROOT/"obras.csv")
candidates=csvread(Path("editorial/rmsjrp/G05D_OBRAS_CONTRATOS_CANDIDATOS_2026_11_09.csv"))
assert len(contracts)==2512 and len(works)==82 and len(candidates)==3
def norm(s):
    return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",str(s)).encode("ascii","ignore").decode("ascii").lower()).strip()
def code(s):return re.sub(r"\D","",str(s).split("/")[0])
def currency(x):return Decimal(str(x)).quantize(Decimal(".01"))
res=[]
for c in candidates:
    n,year=c["contrato"].split("/")
    # JSON holds bare numeric contract id and signature date; process may include only base digits.
    matched=[x for x in contracts if code(x["numero_contrato"])==n
          and x["ano_assinatura"]==year
          and code(x["numero_processo"])==code(c["processo"])]
    unique={(x["ano_assinatura"],x["numero_contrato"],x["numero_processo"],x["contratada"],x["valor_contrato_fonte"]) for x in matched}
    same_supplier=[x for x in matched if norm(x["contratada"])==norm(c["contratada"])]
    exact_value=[x for x in matched if x["valor_contrato_fonte"] and currency(x["valor_contrato_fonte"])==currency(c["valor_contrato_R$"])]
    candidates_works=[w for w in works if norm(w["titulo"])==norm(c["titulo_obra_portal"])]
    res.append({"id":c["id"],"contrato":c["contrato"],"processo":c["processo"],
        "registros_cadastro_contratos":len(matched),"chaves_diferentes":len(unique),
        "fornecedor_exato_normalizado":int(bool(same_supplier)),
        "valor_contrato_igual_2_casas":int(bool(exact_value)),
        "registros_titulo_cadastro_obras":len(candidates_works),
        "status":"correspondencia_contrato_cadastro" if same_supplier and exact_value else ("ficha_oficial_sem_confirmacao_cadastro" if not matched else "conflito_a_investigar"),
        "aviso":"Nao implica vinculo com empenho, medicao ou liquidacao TCESP"})
out=ROOT/"QA_G05D_VINCULOS_CONTRATOS_OBRAS.csv"
with out.open("w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=res[0].keys(),delimiter=";")
    writer.writeheader();writer.writerows(res)
qa={"status":"pass","source_hashes":{x:y[1] for x,y in FILES.items()},
    "candidates_checked":len(res),"matches":res,"output_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
    "limitations":["No contract number in works dataset","A title match is search guidance only",
       "No empenho or mediation identifier in contracts dataset",
       "Contract total is not liquidation in DCA or TCESP"]}
(ROOT/"QA_G05D_VINCULOS.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"pass","matches":res,"output_sha256":qa["output_sha256"]},ensure_ascii=False))
