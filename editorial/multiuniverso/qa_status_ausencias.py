#!/usr/bin/env python3
"""Distingue observacao zero, ausencia, nao aplicabilidade e lacunas no recorte E2."""
import argparse,collections,json,math
from pathlib import Path
from graficos_agregados import GROUPS

def inspect(root):
 manifest=json.loads((root/"publicacoes/manifest.json").read_text(encoding="utf-8"))
 rows=manifest["municipal_profiles"]
 if len(rows)!=280:raise ValueError("Manifesto diferente de 280 fichas")
 results={}
 for total_id,title,components in GROUPS:
  keys=(total_id,)+tuple(k for k,_ in components)
  results[total_id]={"titulo":title,"contas":{key:collections.Counter() for key in keys},
                     "combinações":collections.Counter(),"exemplos":[]}
 for item in rows:
  uid=item["publication_id"];code=str(item["codigo_ibge"])
  file=root/"data/api/v1/publication/universes"/uid/"municipalities"/(code+".json")
  payload=json.loads(file.read_text(encoding="utf-8"))
  vars=payload.get("variables",{})
  for total_id,title,components in GROUPS:
   keys=(total_id,)+tuple(k for k,_ in components)
   statuses=[]
   for key in keys:
    variable=vars.get(key)
    if not isinstance(variable,dict):status="fora_catalogo"
    else:
     latest=variable.get("latest")
     if not latest:status="sem_registro_ultimo_ano"
     else:
      value=latest.get("value");status=str(latest.get("status") or "sem_status")
      if status=="observado":
       if isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value):
        status="observado_zero" if value==0 else "observado_nao_zero"
       else:status="observado_sem_valor_numerico"
    results[total_id]["contas"][key][status]+=1
    statuses.append(status)
   signature=" | ".join(statuses)
   results[total_id]["combinações"][signature]+=1
   if len(results[total_id]["exemplos"])<5 and any(s not in ("observado_zero","observado_nao_zero") for s in statuses):
    results[total_id]["exemplos"].append({"universo":uid,"codigo_ibge":code,"municipio":payload.get("municipality",{}).get("nome"),"status":dict(zip(keys,statuses))})
 return {"fichas":len(rows),"nota":"Contagem de fichas por universo; municipios podem se repetir. Valor zero observado nao foi imputado.","agregados":{key:{"titulo":value["titulo"],"contas":{k:dict(v) for k,v in value["contas"].items()},"combinações":dict(value["combinações"]),"exemplos":value["exemplos"]} for key,value in results.items()}}

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
 a=p.parse_args();result=inspect(a.root);a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(json.dumps({"fichas":result["fichas"],"contas":{k:v["contas"] for k,v in result["agregados"].items()}},ensure_ascii=False))
