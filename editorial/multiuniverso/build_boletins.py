#!/usr/bin/env python3
"""Gera boletins de universos editoriais a partir dos JSONs publicados, sem imputacao."""
import argparse
import hashlib
import html
import json
import pathlib
import re
import urllib.request

BASE = "https://finbra-tic-tim-referencia.pages.dev/data/api/v1"
EXCLUDE = {"RM_JUNDIAI"}
LABELS = {
    "receit": "Receitas e autonomia",
    "tribut": "Receitas e autonomia",
    "iptu": "Receitas e autonomia",
    "itbi": "Receitas e autonomia",
    "iss": "Receitas e autonomia",
    "transfer": "Receitas e autonomia",
    "despes": "Despesas e investimentos",
    "invest": "Despesas e investimentos",
    "urban": "Territorio",
    "habit": "Territorio",
    "sane": "Territorio",
    "ambient": "Territorio",
    "transport": "Territorio",
    "divid": "Divida, liquidez e CAPAG",
    "liquid": "Divida, liquidez e CAPAG",
    "caixa": "Divida, liquidez e CAPAG",
    "capag": "Divida, liquidez e CAPAG",
}
GROUPS = ["Receitas e autonomia","Despesas e investimentos","Territorio","Divida, liquidez e CAPAG","Outros indicadores"]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"financas-municipais-editorial-e2/1.0"})
    with urllib.request.urlopen(req,timeout=35) as stream:
        raw=stream.read()
    return json.loads(raw),hashlib.sha256(raw).hexdigest()

def esc(v):
    return html.escape(str(v if v is not None else ""),quote=True)

def fmt(v):
    if v is None:
        return "Não disponível"
    if isinstance(v,bool):
        return str(v)
    if isinstance(v,(float,int)):
        return f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    return str(v)

def group_for(k, metadata):
    st=(" ".join((str(k),str(metadata.get("label","")),str(metadata.get("name",""))))).lower()
    for pattern,name in LABELS.items():
        if pattern in st:return name
    return "Outros indicadores"

def value_for(row,*names):
    for n in names:
        if n in row and row[n] is not None:return row[n]
    return None

def normalize_universes(index):
    if isinstance(index,list): return index
    if isinstance(index,dict):
        for k in ("universes","items","publications"):
            if isinstance(index.get(k),list):return index[k]
    raise ValueError("Indice sem lista de universos no contrato esperado")

def year_values(payload):
    variables=payload.get("variables")
    if not isinstance(variables,(dict,list)):raise ValueError("context.variables ausente")
    for key,obj in (variables.items() if isinstance(variables,dict) else [(v.get("variable_id") or v.get("id"),v) for v in variables if isinstance(v,dict)]):
        if not isinstance(obj,dict):continue
        md=obj.get("metadata") or {}
        latest=obj.get("latest") or {}
        if not isinstance(latest,dict):latest={}
        yearly=obj.get("yearly") or {}
        if not latest and isinstance(yearly,dict):
            annual=[(str(y),data) for y,data in yearly.items() if isinstance(data,dict)]
            if annual:latest=sorted(annual)[-1][1]
        if latest:yield str(key),md,latest

def generate(payload, source_url):
    title=payload.get("name") or payload.get("publication_id")
    uid=payload.get("publication_id")
    members=payload.get("members") or []
    count=payload.get("member_count")
    if not uid or not title or not isinstance(members,list) or not isinstance(count,int):
        raise ValueError("Contexto sem identificacao/membros completos")
    if count!=len(members):raise ValueError(f"{uid}: membros {len(members)} != member_count {count}")
    items={g:[] for g in GROUPS}
    for key,md,latest in year_values(payload):
        coverage=latest.get("coverage") if isinstance(latest.get("coverage"),dict) else {}
        observed=value_for(latest,"observed","observed_count")
        expected=value_for(latest,"expected","expected_count")
        if observed is None:observed=value_for(coverage,"observed","observed_count")
        if expected is None:expected=value_for(coverage,"expected","expected_count")
        if observed is not None and expected is not None and int(observed)>int(expected):
            raise ValueError(f"{uid}: cobertura invalida {key}")
        numeric=latest.get("numeric") or {}
        median=value_for(numeric,"median","p50")
        q1=value_for(numeric,"q1","Q1","p25")
        q3=value_for(numeric,"q3","Q3","p75")
        unit=md.get("unidade") or md.get("unit") or ""
        label=md.get("nome") or md.get("label") or md.get("name") or key
        row=f"<tr><th scope='row'>{esc(label)}</th><td>{esc(fmt(median))}</td><td>{esc(fmt(q1))}</td><td>{esc(fmt(q3))}</td><td>{esc(observed)}/{esc(expected)}</td><td>{esc(unit)}</td></tr>"
        items[group_for(key,md)].append(row)
    if not any(items.values()):raise ValueError(f"{uid}: contexto sem variaveis aproveitaveis")
    if not any("Não disponível" not in row for group in items.values() for row in group):raise ValueError(f"{uid}: nenhuma estatistica quantitativa extraida")
    sections=[]
    for g in GROUPS:
        if items[g]:
            sections.append(f"<section><h2>{esc(g)}</h2><div class='scroll'><table><thead><tr><th>Conta ou indicador</th><th>Mediana</th><th>Q1</th><th>Q3</th><th>Cobertura</th><th>Unidade</th></tr></thead><tbody>{''.join(items[g])}</tbody></table></div></section>")
    municipal=", ".join(esc(m.get("name") or m.get("municipio") or m.get("codigo_ibge") or m) if isinstance(m,dict) else esc(m) for m in members)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Finanças municipais — {esc(title)}</title>
<style>body{{font:16px/1.55 system-ui,Arial,sans-serif;max-width:1120px;margin:auto;padding:30px;color:#1a2934;background:#f8fafc}}header,section{{background:white;padding:24px;margin:18px 0;border:1px solid #e0e6ea;border-radius:12px}}h1{{line-height:1.2}}h2{{font-size:1.25rem}}table{{border-collapse:collapse;width:100%;font-size:.9rem}}td,th{{padding:10px;border-bottom:1px solid #e3e8ed;text-align:left}}td{{white-space:nowrap}}.scroll{{overflow-x:auto}}a{{color:#145d8a}}small{{color:#52606d}}</style></head>
<body><header><p>Finanças municipais • Edição de referência</p><h1>{esc(title)}</h1><p>Panorama e diferenças fiscais entre {count} municípios. Valores e distribuições conforme disponibilidade das declarações oficiais.</p><p><small>Exercício mais recente do contexto: {esc(payload.get('latest_year','não informado'))}</small></p></header>
<section><h2>Como interpretar</h2><p>Mediana é o valor central dos municípios com observação. Q1 e Q3 delimitam a metade central da distribuição. A cobertura indica quantos municípios possuem dados válidos para cada conta ou indicador. Ausência não significa zero. Diferenças contábeis não demonstram, por si, qualidade de gestão, causalidade ou resultados físicos.</p></section>
{''.join(sections)}
<section><h2>Municípios integrantes</h2><p>{municipal}</p></section>
<section><h2>Fontes e metodologia</h2><p>Base estadual FINBRA/Siconfi e demonstrativos complementares identificados no catálogo oficial do projeto. Indicadores legais seguem a fonte própria. Os valores não devem ser somados quando a cobertura for incompleta. A presente edição apresenta estatísticas municipais do contexto; não substitui os demonstrativos fiscais oficiais.</p><p><a href="{esc(source_url)}">Consultar contexto fiscal e metadados de origem</a></p></section></body></html>"""

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base",default=BASE)
    p.add_argument("--out",default="build/editorial-universes")
    args=p.parse_args()
    base=args.base.rstrip("/")
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    index,ih=fetch(base+"/publication/universes.json")
    entries=normalize_universes(index)
    records=[]
    seen=set()
    for entry in entries:
        uid=entry.get("publication_id") if isinstance(entry,dict) else None
        if not uid or not re.fullmatch(r"[A-Za-z0-9_-]+",uid) or uid in seen:
            raise ValueError("publication_id ausente, repetido ou inseguro")
        seen.add(uid)
        if uid in EXCLUDE:continue
        url=f"{base}/publication/universes/{uid}/context.json"
        ctx,ch=fetch(url)
        if ctx.get("publication_id") != uid:raise ValueError(f"{uid}: context nao corresponde ao indice")
        folder=out/uid;folder.mkdir(exist_ok=True)
        page=generate(ctx,url)
        (folder/"index.html").write_text(page,encoding="utf-8")
        records.append({"publication_id":uid,"name":ctx.get("name"),"member_count":ctx["member_count"],"context_sha256":ch,"html_sha256":hashlib.sha256(page.encode()).hexdigest(),"source":url})
    if len(entries)!=11 or len(records)!=10:
        raise ValueError(f"Contrato esperado: 11 universos e 10 boletins adicionais; recebido {len(entries)} e {len(records)}")
    (out/"manifest.json").write_text(json.dumps({"index_sha256":ih,"editions":records},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{len(records)} boletins gerados, nenhum publicado.")
if __name__=="__main__":main()
