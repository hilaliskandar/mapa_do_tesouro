#!/usr/bin/env python3
"""Confronta serie RGF 2023-2024 aprovada com API de publicacao E2.

A base candidata foi previamente cotejada com planilhas de referencia TIC-TIM
30 no Gate E. Este teste e uma segunda etapa, nao uma nova coleta oficial.
"""
import argparse,csv,json,math,pathlib
from build_boletins import BASE,fetch,normalize_universes,EXCLUDE
FIELDS={
 "rgf_despesa_total_pessoal":"rgf_despesa_total_pessoal",
 "rgf02_divida_consolidada":"rgf02_divida_consolidada",
 "rgf02_divida_consolidada_liquida":"rgf02_divida_consolidada_liquida",
 "rgf_dtp_percentual_rcl":"dtp_pct_rcl",
 "rgf02_dc_percentual_rcl":"dc_pct_rcl",
 "rgf02_dcl_percentual_rcl":"dcl_pct_rcl",
}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--candidate",required=True);p.add_argument("--base",default=BASE);p.add_argument("--out",required=True)
 a=p.parse_args()
 with open(a.candidate,encoding="utf-8",newline="") as f:
  rows={(str(r["cod_ibge"]),int(r["ano"])):r for r in csv.DictReader(f)}
 ix,_=fetch(a.base.rstrip("/")+"/publication/universes.json")
 report=[]
 missing=[]
 for e in normalize_universes(ix):
  uid=e["publication_id"]
  if uid in EXCLUDE:continue
  base=a.base.rstrip("/")+"/publication/universes/"+uid
  ctx,_=fetch(base+"/context.json")
  for member in ctx["members"]:
   code=str(member["codigo_ibge"])
   if not any((code,year) in rows for year in (2023,2024)):continue
   obj,_=fetch(base+"/municipalities/"+code+".json")
   for field,target in FIELDS.items():
    detail=(obj.get("variables") or {}).get(target)
    if detail is None:
     missing.append({"universe":uid,"code":code,"year":None,"field":field,"type":"variable_not_exported"})
     continue
    series={int(y["year"]):y for y in detail.get("series",[]) if y.get("year") is not None}
    for year in (2023,2024):
     reference=rows.get((code,year))
     if reference is None:continue
     if field not in reference:raise ValueError("Coluna de referência inexistente: "+field)
     ref=reference[field]
     observation=series.get(year)
     val=(observation or {}).get("value") if (observation or {}).get("status")=="observado" else None
     if ref in ("",None) and val is None:continue
     if ref in ("",None) or val is None:
      reason=("year_absent" if observation is None else ("status_"+str(observation.get("status")) if observation.get("status")!="observado" else "null_value"))
      missing.append({"universe":uid,"code":code,"year":year,"field":field,"ref":ref,"api":val,"type":reason})
      continue
     normalized=float(val)*100 if target in ("dtp_pct_rcl","dc_pct_rcl","dcl_pct_rcl") else float(val)
     delta=abs(float(ref)-normalized)
     tolerance=0.01
     report.append({"universe":uid,"code":code,"year":year,"variable":target,"reference":float(ref),"api_raw":float(val),"api_same_unit":normalized,"difference":delta,"pass":delta<=tolerance})
 from collections import Counter
 missing_reasons=dict(Counter(x.get("type","unknown") for x in missing))
 out={"missing_reasons":missing_reasons,"comparison_scope":"Gate E approved reference vs E2 API, not direct official RGF","compared":len(report),"mismatches":[r for r in report if not r["pass"]],"availability_mismatches":missing,"values":report}
 pathlib.Path(a.out).parent.mkdir(parents=True,exist_ok=True)
 pathlib.Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 if len(report)<30 or out["mismatches"] or missing:raise ValueError(f"RGF nao homologado: {len(report)} comparacoes, {len(out['mismatches'])} divergencias de valor, {len(missing)} de disponibilidade")
 print("RGF x API E2 aprovado:",len(report),"comparacoes")
if __name__=="__main__":main()
