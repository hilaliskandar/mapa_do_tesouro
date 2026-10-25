#!/usr/bin/env python3
"""Reconcile 2025 TCESP revenue municipality names against SP645 canonical roster."""
import argparse,csv,json,pathlib,re,unicodedata,collections
p=argparse.ArgumentParser();p.add_argument("--dca",required=True);p.add_argument("--qa",required=True);p.add_argument("--out",required=True);a=p.parse_args()
def norm(s):
 s=unicodedata.normalize("NFKD",str(s or ""));s="".join(c for c in s if not unicodedata.combining(c))
 return re.sub(r"[^A-Z0-9]+"," ",s.upper()).strip()
with open(a.dca,encoding="utf-8-sig",newline="") as f:
 reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
code_key="cod_ibge"
name_options=["municipio","nome_municipio","nm_municipio","nome","ds_municipio","ente","municipio_nome"]
name_key=next((x for x in name_options if x in fields),None)
if not name_key:
 name_key=next((x for x in fields if "municip" in x.lower() and x!=code_key),None)
if not name_key:raise RuntimeError("Cannot identify municipal-name column in DCA: "+repr(fields))
roster={}
for row in rows:
 k=row[code_key];v=row[name_key]
 if k in roster and norm(roster[k])!=norm(v):raise RuntimeError("Conflicting name "+k)
 roster[k]=v
assert len(roster)==645
with open(a.qa,encoding="utf-8") as f: qa=json.load(f)
source=qa["linhas_por_municipio"]
lookup=collections.defaultdict(list)
for code,name in roster.items():lookup[norm(name)].append({"codigo_ibge":code,"nome_dca":name})
matched={};unmatched=[];ambiguous=[]
for name in source:
 possible=lookup.get(norm(name),[])
 if len(possible)==1:matched[name]=possible[0]
 elif len(possible)==0:unmatched.append(name)
 else:ambiguous.append({"nome_tcesp":name,"possiveis":possible})
covered={x["codigo_ibge"] for x in matched.values()}
missing=[{"codigo_ibge":k,"nome_dca":v} for k,v in sorted(roster.items()) if k not in covered]
result={"status":"conferido","dca_name_column":name_key,"dca_rows":len(rows),"municipios_ibge":len(roster),"nomes_tcesp":len(source),"correspondencias_exatas_normalizadas":len(matched),"nao_correspondentes_tcesp":unmatched,"ambiguos":ambiguous,"municipios_dca_sem_match":missing,"cobertura_confirmada_ibge":len(covered),"advertencia":"Matching exato apos retirada de acentos e pontuacao. Nomes divergentes nao sao corrigidos automaticamente. Jurisdicao nao e determinada apenas por este teste."}
out=pathlib.Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2)[:20000])
