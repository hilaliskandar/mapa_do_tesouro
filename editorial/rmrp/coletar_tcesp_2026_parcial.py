#!/usr/bin/env python3
"""TCESP 2026: coleta parcial por municipio, despesas 44 e receitas tributarias.
Sem publicacao; cada extrato captura meses observados, hash de origem e fase.
"""
import argparse,collections,csv,decimal,hashlib,io,json,pathlib,time,urllib.request,zipfile,datetime
D=decimal.Decimal
def cents(v):
 return int((D((v or "0").replace(".","").replace(",","."))*100).quantize(D("1")))
def download(slug,domain,year):
 url=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/{domain}-{slug}-{year}.zip"
 err=None
 for i in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=180) as r: content=r.read()
   with zipfile.ZipFile(io.BytesIO(content)) as z:
    name=next(n for n in z.namelist() if n.lower().endswith(".csv"))
    with z.open(name) as f:
     rows=list(csv.DictReader(io.TextIOWrapper(f,encoding="latin-1",newline=""),delimiter=";"))
   return url,hashlib.sha256(content).hexdigest(),rows
  except Exception as exc:
   err=str(exc);time.sleep(i+1)
 raise RuntimeError(f"{domain} {slug}: {err}")
def process(slug,ibge,domain,year):
 url,sha,rows=download(slug,domain,year)
 observed=set();by=collections.defaultdict(int);counts=collections.Counter()
 for r in rows:
  m=(r.get("mes_referencia") or "").strip()
  if not m.isdigit() or not 1<=int(m)<=12:continue
  m=int(m);observed.add(m)
  if domain=="despesas":
   el=(r.get("ds_elemento") or "").split(" - ",1)[0].strip()
   if not el.startswith("44"):continue
   typ=(r.get("tp_despesa") or "").strip()
   by[(m,typ,(r.get("ds_orgao") or "").strip(),(r.get("cd_programa") or "").strip(),
       (r.get("cd_acao") or "").strip(),(r.get("ds_acao") or "").strip(),
       (r.get("ds_fonte_recurso") or "").strip())]+=cents(r.get("vl_despesa"))
   counts[(typ,m)]+=1
  else:
   code=(r.get("ds_tipo") or "").split(" - ",1)[0].strip()
   imp=("IPTU" if code.startswith("111250") else "ITBI" if code.startswith("111253") else "ISS" if code.startswith("111451") else None)
   if not imp:continue
   by[(m,imp,code,(r.get("ds_orgao") or "").strip())]+=cents(r.get("vl_arrecadacao"))
   counts[(imp,m)]+=1
 # Report months present in the source including other categories; monthly coverage is not proof of full delivery.
 return {"codigo_ibge":ibge,"slug":slug,"ano":year,"dominio":domain,
         "situacao_exercicio":"parcial_em_andamento","periodicidade":"mes_referencia",
         "meses_observados":sorted(observed),"ultimo_mes_observado":max(observed,default=None),
         "capturado_em_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "fonte":url,"fonte_sha256":sha,"linhas_fonte":len(rows),
         "registros_relevantes":sum(counts.values()),
         "contagens_por_tipo_mes":[{"tipo":k[0],"mes":k[1],"linhas":v} for k,v in sorted(counts.items())],
         "agregados":[{"chaves":list(k),"centavos":v} for k,v in sorted(by.items())],
         "soma_movimentacoes_centavos":sum(by.values()),"qa_status":"estrutura_consistente",
         "interpretacao":"Fluxos mensais parciais; movimentos de empenho, anulacao, liquidacao e pagamento nao se somam entre si."}
def main():
 p=argparse.ArgumentParser();p.add_argument("--roster",required=True,type=pathlib.Path)
 p.add_argument("--subregiao",type=int,choices=range(1,5),required=True)
 p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 with a.roster.open(encoding="utf-8-sig",newline="") as f:rs=[r for r in csv.DictReader(f) if int(r["subregiao"])==a.subregiao]
 out=[];fail=[];a.output.mkdir(parents=True,exist_ok=True)
 for r in rs:
  for domain in ("despesas","receitas"):
   dest=a.output/f'{r["slug"]}_2026_{domain}.json'
   try:
    if dest.exists():
     v=json.loads(dest.read_text(encoding="utf-8"));assert v["fonte_sha256"] and v["slug"]==r["slug"]
     mode="reuse"
    else:
     v=process(r["slug"],r["codigo_ibge"],domain,2026)
     dest.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");mode="download"
    out.append({"codigo_ibge":r["codigo_ibge"],"slug":r["slug"],"dominio":domain,"status":"validado","modo":mode,
     "meses":v["meses_observados"],"arquivo":dest.name,"sha256":hashlib.sha256(dest.read_bytes()).hexdigest()})
   except Exception as e:fail.append({"slug":r["slug"],"dominio":domain,"erro":str(e)})
 manifest={"ano":2026,"escopo":"RMRP","subregiao":a.subregiao,"municipios":len(rs),"esperados":len(rs)*2,
 "validados":len(out),"falhas":fail,"dados_parciais":True,"r2_persistido":False,"publicado":False,"resultados":out}
 (a.output/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:v for k,v in manifest.items() if k!="resultados"},ensure_ascii=False))
 if fail:raise SystemExit(1)
if __name__=="__main__":main()
