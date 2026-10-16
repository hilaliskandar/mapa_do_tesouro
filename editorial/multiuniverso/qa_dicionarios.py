#!/usr/bin/env python3
"""Auditoria do dicionario e comparacao entre os dez universos."""
import collections,json,pathlib,sys
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "build/editorial-universes")
manifest=json.loads((root/"manifest.json").read_text(encoding="utf-8"))
records=[]
for edition in manifest["editions"]:
    uid=edition["publication_id"]
    rows=json.loads((root/uid/"dicionario.json").read_text(encoding="utf-8"))
    if len(rows)!=50 or len({r["variavel_id"] for r in rows})!=len(rows):
        raise AssertionError(f"{uid}: catalogo inesperado, duplicado ou incompleto")
    for r in rows:
        if not r.get("nome") or not r.get("unidade") or not r.get("editorial_group"):
            raise AssertionError(f"{uid}/{r['variavel_id']}: nome/unidade/grupo ausente")
        src=r["metadados_originais"]
        if r["fonte_id"]!=(src.get("fonte_preferencial_id") or src.get("fonte_id")):
            raise AssertionError(f"{uid}/{r['variavel_id']}: fonte divergente")
        if r["descricao"]!=(src.get("definicao") or src.get("descricao")):
            raise AssertionError(f"{uid}/{r['variavel_id']}: definicao divergente")
        if r["formula"]!=src.get("formula"):
            raise AssertionError(f"{uid}/{r['variavel_id']}: formula divergente")
    records.append((uid,rows))
catalog={}
for uid,rows in records:
    for row in rows:
        key=row["variavel_id"]
        current=(row["nome"],row["unidade"],row["editorial_group"],row["formula"],row["fonte_id"])
        if key in catalog and catalog[key]!=current:
            raise AssertionError(f"Metadados divergentes entre universos: {key}")
        catalog[key]=current
counts={k:sum(x.get(k) is not None for x in records[0][1]) for k in ("nome","unidade","editorial_group","fonte_id","descricao","formula","tipo","periodicidade","cautelas","como_ler")}
result={"universos":len(records),"variaveis_unicas":len(catalog),"atributos_preenchidos_no_catalogo":counts,"unidades":dict(collections.Counter(r["unidade"] for r in records[0][1])),"grupos":dict(collections.Counter(r["editorial_group"] for r in records[0][1])),"sem_fonte_preferencial":[r["variavel_id"] for r in records[0][1] if not r.get("fonte_id")]}
out=root/"qa_dicionarios.json"
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
