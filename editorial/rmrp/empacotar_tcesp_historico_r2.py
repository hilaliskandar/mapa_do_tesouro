#!/usr/bin/env python3
"""Empacota 102 extratos historicos RMRP, sem consulta ao TCESP."""
import argparse,csv,hashlib,json,pathlib,tarfile,collections
p=argparse.ArgumentParser();p.add_argument("--input",type=pathlib.Path,required=True);p.add_argument("--roster",type=pathlib.Path,required=True);p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
with a.roster.open(encoding="utf-8-sig",newline="") as f: rr=list(csv.DictReader(f))
expect={(r["slug"],y) for r in rr for y in (2023,2024,2025)}
got={}; records=[]
for fp in sorted(a.input.rglob("*.json")):
 try:d=json.loads(fp.read_text(encoding="utf-8"))
 except Exception:continue
 if not {"slug","year","investimento_44_liquidado_centavos"}.issubset(d):continue
 k=d["slug"],int(d["year"])
 if k not in expect:continue
 if k in got:raise SystemExit(f"duplicate {k}")
 if d.get("bad_values")!=0 or len(d.get("sha256_zip",""))!=64:raise SystemExit(f"bad metadata {k}")
 total=int(d["investimento_44_liquidado_centavos"])
 if total!=sum(int(x[-1]) for x in d["programas_44_liquidado_completos"]) or total!=sum(int(x[-1]) for x in d["acoes_44_liquidado_completas"]):raise SystemExit(f"reconciliation error {k}")
 got[k]=fp
 records.append({"slug":k[0],"year":k[1],"municipio_ibge":next(x["codigo_ibge"] for x in rr if x["slug"]==k[0]),"source_url":d["url"],"source_sha256":d["sha256_zip"],"extract_sha256":hashlib.sha256(fp.read_bytes()).hexdigest(),"liquidado_centavos":total,"path":str(fp.relative_to(a.input))})
if set(got)!=expect:raise SystemExit(f"missing {sorted(expect-set(got))}")
a.output.mkdir(parents=True,exist_ok=True);tar=a.output/"rmrp_tcesp_investimentos_2023_2025_102.tar.gz"
with tarfile.open(tar,"w:gz") as z:
 for fp in got.values():z.add(fp,arcname=str(fp.relative_to(a.input)))
sha=hashlib.sha256(tar.read_bytes()).hexdigest()
manifest={"snapshot_id":"rmrp_tcesp_2023_2025_run_39203495737","universe":"RMRP_34","source_run":39203495737,
"municipios":34,"years":[2023,2024,2025],"pairs":102,"domain":"investimento_despesa_44_liquidado",
"data_status":"historico_coletado","publication_authorized":False,"archive_sha256":sha,
"archive_size":tar.stat().st_size,"records":records}
(a.output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"pairs":len(records),"municipios":34,"sha256":sha,"bytes":tar.stat().st_size}))
