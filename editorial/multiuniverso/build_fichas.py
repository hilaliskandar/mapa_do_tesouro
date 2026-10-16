#!/usr/bin/env python3
"""Acrescenta fichas municipais independentes para cada universo publicado."""
import argparse,hashlib,html,json,pathlib,urllib.request
from build_boletins import source_reference, BASE, EXCLUDE, fetch, normalize_universes, esc, shown
from graficos_municipais import charts as municipal_charts
from graficos_composicao import build as composition_charts

def build_profile(obj, base, uid, publication_name):
    municipality=obj["municipality"]
    name=municipality["nome"]
    code=str(municipality["codigo_ibge"])
    if str(obj.get("publication_universe",{}).get("publication_id"))!=uid:
        raise ValueError(f"{uid}/{code}: universo divergente")
    groups={}
    observed=0
    for key,detail in sorted(obj.get("variables",{}).items()):
        metadata=detail.get("metadata") or {}
        label=metadata.get("nome") or key
        unit=metadata.get("unidade") or ""
        latest=detail.get("latest") or {}
        state=latest.get("status") or "não informado"
        value=latest.get("value") if state=="observado" else None
        if value is not None:observed+=1
        relative=detail.get("relative_latest") or {}
        group_latest=detail.get("group_latest") or {}
        numeric=group_latest.get("numeric") or {}
        median=numeric.get("median")
        position=relative.get("rank_desc")
        if position is None:position=relative.get("rank")
        covobs=group_latest.get("observed")
        covexp=group_latest.get("expected")
        entries=[]
        for record in detail.get("series") or []:
            if not isinstance(record,dict) or record.get("year") is None:continue
            value_year=record.get("value") if record.get("status")=="observado" else None
            entries.append(f"{esc(record['year'])}: {esc(shown(value_year,unit,key))}")
        series=" · ".join(entries)
        row=(f"<tr><th scope='row'>{esc(label)}</th><td>{esc(shown(value,unit,key))}</td>"
             f"<td>{esc(shown(median,unit,key))}</td><td>{esc(covobs)}/{esc(covexp)}</td>"
             f"<td>{esc(state)}</td><td>{esc(position) if position is not None else '—'}</td></tr>")
        group=detail.get("editorial_group") or metadata.get("grupo") or "Demais contas"
        groups.setdefault(group,[]).append((row,key,series,metadata))
    sections=[]
    for group, entries in groups.items():
        tab="".join(x[0] for x in entries)
        historical="".join("<details><summary>"+esc(x[3].get("nome") or x[1])+"</summary><p>"+esc(x[2] or "Não há série adicional disponível.")+"</p></details>" for x in entries)
        sections.append(f"<section><h2>{esc(group.replace('_',' ').capitalize())}</h2><div class='scroll'><table><thead><tr><th>Conta ou indicador</th><th>Município</th><th>Mediana do grupo</th><th>Cobertura</th><th>Situação</th><th>Posição</th></tr></thead><tbody>{tab}</tbody></table></div><h3>Evolução registrada</h3>{historical}</section>")
    figure=municipal_charts(obj,shown)
    composition=composition_charts(obj)
    url=f"{base}/publication/universes/{uid}/municipalities/{code}.json"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Finanças municipais — {esc(name)}</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:1080px;margin:auto;padding:24px;color:#22303a;background:#f7fafc}}section,header{{background:white;padding:20px;border:1px solid #e3e7ea;border-radius:12px;margin:15px 0}}table{{width:100%;border-collapse:collapse;font-size:.9rem}}td,th{{text-align:left;padding:9px;border-bottom:1px solid #ddd}}.scroll{{overflow:auto}}a{{color:#13618c}}a:focus-visible,summary:focus-visible{{outline:3px solid #d77b00;outline-offset:3px}}@media(max-width:650px){{body{{padding:10px}}section,header{{padding:14px}}td,th{{padding:7px}}}}.chart-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:12px}}.chart-card{{padding:12px;border:1px solid #dce5ec;border-radius:10px}}.chart-card svg{{width:100%;height:auto}}details{{border-bottom:1px solid #eee;padding:6px 0}}summary{{cursor:pointer}}</style></head><body>
<header><p><a href="../index.html">Voltar ao boletim do universo</a></p><h1>{esc(name)}</h1><p>{esc(publication_name)} · Código IBGE {esc(code)}</p><p>Exercício de referência: {esc(obj.get("latest_year"))} · Indicadores e contas com observação no último ano: {observed}/{len(obj.get("variables",{}))}</p></header>
<section><h2>Como ler a ficha</h2><p>Os valores são os declarados ou calculados na base fiscal, segundo a fonte de cada conta. A mediana e a posição são relativas ao universo indicado. As posições não representam nota de gestão. A ausência de informação não corresponde a zero, e as séries podem ter coberturas diferentes.</p></section>
{figure}
{composition}
{''.join(sections)}
<section><h2>Notas específicas sobre RREO, RGF e CAPAG</h2><p><strong>RREO:</strong> a RCL do Anexo 03, sexto bimestre, corresponde ao total dos últimos 12 meses e não deve ser substituída por valor de outra fonte quando ausente.</p><p><strong>RGF:</strong> valores monetários de pessoal e dívida e percentuais legais possuem escalas diferentes; indicadores percentuais são exibidos em pontos percentuais, sem alterar os valores canônicos. Os registros históricos ausentes não são zeros nem casos automaticamente inaplicáveis.</p><p><strong>CAPAG:</strong> a categoria oficial corresponde à posição de setembro de 2026, ano-base 2025. A classificação n.d. é uma categoria oficial, diferente da situação de dado ausente. Comparações de notas entre posições distintas exigem verificar a revisão do Tesouro.</p></section>
<section><h2>Fontes e notas de interpretação</h2><p>Dados FINBRA/Siconfi e demonstrativos complementares previstos na base editorial. Não se deve confundir movimentação contábil, execução física ou resultado de política pública. Indicadores oficiais e derivados seguem suas metodologias específicas.</p>{source_reference(url)}</section></body></html>"""

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--base",default=BASE)
    parser.add_argument("--out",default="build/editorial-universes")
    args=parser.parse_args()
    base=args.base.rstrip("/")
    out=pathlib.Path(args.out)
    idx,_=fetch(base+"/publication/universes.json")
    manifest_path=out/"manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    all_profiles=[]
    for entry in normalize_universes(idx):
        uid=entry["publication_id"]
        if uid in EXCLUDE:continue
        context,_=fetch(f"{base}/publication/universes/{uid}/context.json")
        title=context["name"]
        members=context["members"]
        folder=out/uid
        (folder/"municipios").mkdir(parents=True,exist_ok=True)
        links=[]
        for member in members:
            code=str(member["codigo_ibge"])
            url=f"{base}/publication/universes/{uid}/municipalities/{code}.json"
            municipal,sha=fetch(url)
            if str(municipal.get("municipality",{}).get("codigo_ibge"))!=code:
                raise ValueError("Código municipal não confere")
            page=build_profile(municipal,base,uid,title)
            (folder/"municipios"/f"{code}.html").write_text(page,encoding="utf-8")
            links.append(f'<li><a href="municipios/{esc(code)}.html">{esc(member["nome"])}</a></li>')
            all_profiles.append({"publication_id":uid,"codigo_ibge":code,"source_sha256":sha,"html_sha256":hashlib.sha256(page.encode("utf-8")).hexdigest()})
        index_file=folder/"index.html"
        index_html=index_file.read_text(encoding="utf-8")
        marker='<section id="fichas"><h2>Municípios integrantes</h2>'
        if marker not in index_html:raise ValueError(f"{uid}: estrutura do boletim alterada")
        added=f"<section><h2>Fichas municipais</h2><p>As fichas apresentam valores individuais, medianas do respectivo grupo, situação da informação e séries disponíveis.</p><ul>{''.join(links)}</ul></section>"
        new_html=index_html.replace(marker,added+marker,1)
        index_file.write_text(new_html,encoding="utf-8")
        for edition in manifest["editions"]:
            if edition["publication_id"]==uid:
                edition["html_sha256"]=hashlib.sha256(new_html.encode("utf-8")).hexdigest()
    if len(all_profiles)!=280:raise ValueError(f"Esperadas 280 fichas; produzidas {len(all_profiles)}")
    manifest["municipal_profiles"]=all_profiles
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Geradas {len(all_profiles)} fichas em dez universos, sem publicação.")
if __name__=="__main__":main()
