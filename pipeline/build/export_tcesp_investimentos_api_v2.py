#!/usr/bin/env python3
"""Export TCESP investment views into a segregated preview-only API v2 namespace."""
import argparse,collections,json,pathlib,sqlite3
p=argparse.ArgumentParser();p.add_argument("--database",type=pathlib.Path,required=True);p.add_argument("--output",type=pathlib.Path,required=True)
a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
c=sqlite3.connect(f"file:{a.database}?mode=ro",uri=True);c.row_factory=sqlite3.Row
try:
 years=[dict(x) for x in c.execute("SELECT exercicio,lote_id,source_sha256,qa_status FROM tcesp_lote ORDER BY exercicio")]
 assert [x["exercicio"] for x in years]==[2023,2024,2025]
 def write(path,obj):
  pth=out/path;pth.parent.mkdir(parents=True,exist_ok=True)
  pth.write_text(json.dumps(obj,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
 base="data/api/v2/tcesp"
 write(base+"/manifest.json",{"source":"TCESP","dataset":"investimentos_grupo44","status":"preview_not_published","exercises":years,"measurement":"centavos","caution":"Municipal program/action codes not harmonized across municipalities."})
 for year in (2023,2024,2025):
  summary=[dict(x) for x in c.execute("""
   SELECT p.codigo_ibge,p.estagio,SUM(p.valor_centavos) valor_centavos
   FROM tcesp_investimento_programa p JOIN tcesp_lote l ON l.lote_id=p.lote_id
   WHERE l.exercicio=? GROUP BY p.codigo_ibge,p.estagio ORDER BY p.codigo_ibge,p.estagio""",(year,))]
  write(f"{base}/{year}/municipios.json",{"year":year,"source":"TCESP","rows":summary})
  assert len({r["codigo_ibge"] for r in summary})==644
  # per-municipality detail allows efficient direct static lookup
  for city in sorted({r["codigo_ibge"] for r in summary}):
   prog=[dict(x) for x in c.execute("""
    SELECT p.mes,p.estagio,p.orgao,p.cd_programa,p.ds_programa,p.valor_centavos
    FROM tcesp_investimento_programa p JOIN tcesp_lote l USING(lote_id)
    WHERE l.exercicio=? AND p.codigo_ibge=? ORDER BY p.mes,p.estagio,p.orgao,p.cd_programa,p.ds_programa""",(year,city))]
   acao=[dict(x) for x in c.execute("""
    SELECT a.mes,a.estagio,a.orgao,a.cd_programa,a.ds_programa,a.cd_acao,a.ds_acao,a.valor_centavos
    FROM tcesp_investimento_acao a JOIN tcesp_lote l USING(lote_id)
    WHERE l.exercicio=? AND a.codigo_ibge=? ORDER BY a.mes,a.estagio,a.orgao,a.cd_programa,a.cd_acao""",(year,city))]
   assert sum(x["valor_centavos"] for x in prog)==sum(x["valor_centavos"] for x in acao)
   write(f"{base}/{year}/municipios/{city}.json",{"codigo_ibge":city,"ano":year,"source":"TCESP","programas":prog,"acoes":acao})
 print(json.dumps({"status":"pass","years":[x["exercicio"] for x in years],"municipal_year_detail_files":1932,"namespace":base},ensure_ascii=False))
finally:c.close()
