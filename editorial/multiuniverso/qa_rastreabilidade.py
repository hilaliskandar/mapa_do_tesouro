#!/usr/bin/env python3
"""Documenta dependencias de formulas sem fabricar fontes ausentes."""
import json, pathlib, re, sys

def audit(folder):
    manifest=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
    overview=[]
    for edition in manifest["editions"]:
        uid=edition["publication_id"]
        file=folder/uid/"dicionario.json"
        rows=json.loads(file.read_text(encoding="utf-8"))
        ids={x["variavel_id"]:x for x in rows}
        records=[]
        for row in rows:
            if row.get("fonte_id"):continue
            formula=row.get("formula") or ""
            tokens=set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*",formula))
            known=sorted(t for t in tokens if t in ids and t!=row["variavel_id"])
            external=sorted(t for t in tokens if t not in ids and not t.isupper())
            sourced=sorted({ids[t]["fonte_id"] for t in known if ids[t].get("fonte_id")})
            records.append({
                "variavel_id":row["variavel_id"],
                "tipo":row.get("tipo"),
                "formula":row.get("formula"),
                "dependencias_presentes":known,
                "fontes_diretas_identificadas_nas_dependencias":sourced,
                "referencias_fora_do_recorte_ou_nao_resolvidas":external,
                "rastreabilidade_integral_confirmada":bool(known) and not external and all(ids[t].get("fonte_id") for t in known),
                "nota":"Fontes das parcelas nao equivalem a fonte preferencial do indicador derivado.",
            })
        out=folder/uid/"rastreabilidade.json"
        out.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
        overview.append({"universo":uid,"sem_fonte_preferencial":len(records),
                         "com_referencias_nao_resolvidas":sum(bool(r["referencias_fora_do_recorte_ou_nao_resolvidas"]) for r in records),
                         "rastreabilidade_imediata":sum(r["rastreabilidade_integral_confirmada"] for r in records)})
    (folder/"qa_rastreabilidade.json").write_text(json.dumps(overview,ensure_ascii=False,indent=2),encoding="utf-8")
    assert len(overview)==10 and all(x["sem_fonte_preferencial"]==15 for x in overview)
    print(json.dumps(overview,ensure_ascii=False))
if __name__=="__main__":
    audit(pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "build/editorial-universes"))
