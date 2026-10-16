"""Graficos SVG autocontidos, feitos somente a partir de estatisticas observadas no contexto."""
import html,math

def esc(v):return html.escape(str(v),quote=True)
def valid(v):return isinstance(v,(float,int)) and not isinstance(v,bool) and math.isfinite(v)
def normalize_years(v):
    if isinstance(v,dict):return [dict(row,year=year) for year,row in v.items() if isinstance(row,dict)]
    return v if isinstance(v,list) else []

def candidates(context):
    out=[]
    variables=context.get("variables") or {}
    iterator=variables.items() if isinstance(variables,dict) else []
    for key,obj in iterator:
        if not isinstance(obj,dict):continue
        md=obj.get("metadata") or {}
        unit=md.get("unidade") or md.get("unit") or ""
        if unit not in ("percentual","BRL","R$","reais","moeda","numero","habitantes"):continue
        latest=obj.get("latest") or {}
        nums=latest.get("numeric") or {}
        q1=nums.get("q1",nums.get("p25"));med=nums.get("median",nums.get("p50"));q3=nums.get("q3",nums.get("p75"))
        obs=latest.get("observed",latest.get("observed_count"))
        exp=latest.get("expected",latest.get("expected_count"))
        if any(not valid(v) for v in (q1,med,q3)):continue
        if not q1<=med<=q3:continue
        if not isinstance(obs,int) or not isinstance(exp,int) or obs<4 or obs>exp:continue
        yearly=[]
        for row in normalize_years(obj.get("yearly")):
            numeric=row.get("numeric") or {}
            value=numeric.get("median",numeric.get("p50"))
            y=row.get("year")
            if valid(value) and str(y).isdigit():
                yearly.append((int(y),value,row.get("observed",row.get("observed_count")),row.get("expected",row.get("expected_count"))))
        yearly=sorted(set(yearly),key=lambda z:z[0])
        out.append(dict(key=str(key),label=str(md.get("nome") or md.get("label") or key),unit=unit,q1=q1,median=med,q3=q3,observed=obs,expected=exp,yearly=yearly,group=obj.get("editorial_group")))
    return out

def build(context,shown,limit=6):
    values=candidates(context)
    groups=("receitas","despesas","territorio","divida_liquidez","capag")
    selected=[]
    for group in groups:
        chosen=next((v for v in values if v["group"]==group),None)
        if chosen is not None:selected.append(chosen)
    for v in values:
        if len(selected)>=limit:break
        if v not in selected:selected.append(v)
    if not selected:
        return "<section id='graficos'><h2>Gráficos de distribuição</h2><p>Sem estatísticas numéricas e cobertura suficiente para gráficos comparáveis.</p></section>"
    charts=[]
    for obj in selected:
        q1,med,q3=(obj[x] for x in ("q1","median","q3"))
        low=min(0,q1) if q1>=0 else q1
        high=max(q3,med)
        if high==low:high=low+1
        scale=lambda v:75+500*(v-low)/(high-low)
        y=68
        label=esc(obj["label"]);unit=esc(obj["unit"]);key=esc(obj["key"])
        bar=f'<line x1="{scale(q1):.2f}" y1="{y}" x2="{scale(q3):.2f}" y2="{y}" stroke="#24769c" stroke-width="12" stroke-linecap="round"/>'
        bar+=f'<circle cx="{scale(med):.2f}" cy="{y}" r="8" fill="#d97706" stroke="white" stroke-width="2"/>'
        bar+=f'<line x1="75" y1="101" x2="575" y2="101" stroke="#9baab5" stroke-width="1"/>'
        for x,v in ((75,low),(575,high)):
            bar+=f'<text x="{x}" y="121" text-anchor="middle" font-size="13">{esc(shown(v,obj["unit"],obj["key"]))}</text>'
        svg=f'<svg role="img" aria-label="Intervalo interquartil e mediana de {label}" viewBox="0 0 650 140" preserveAspectRatio="xMidYMid meet"><title>{label}</title><text x="75" y="30" font-size="15">Q1: {esc(shown(q1,obj["unit"],obj["key"]))} · Mediana: {esc(shown(med,obj["unit"],obj["key"]))} · Q3: {esc(shown(q3,obj["unit"],obj["key"]))}</text>{bar}</svg>'
        trend=""
        if len(obj["yearly"])>=2:
            rows="".join(f'<tr><th scope="row">{yr}</th><td>{esc(shown(v,obj["unit"],obj["key"]))}</td><td>{esc(obs)}/{esc(exp)}</td></tr>' for yr,v,obs,exp in obj["yearly"])
            trend=f'<details><summary>Evolução anual observada</summary><table><thead><tr><th>Ano</th><th>Mediana</th><th>Cobertura</th></tr></thead><tbody>{rows}</tbody></table></details>'
        charts.append(f'<article class="chart-card" data-indicator="{key}"><h3>{label}</h3>{svg}<p>Unidade: {unit}. Cobertura: {obj["observed"]}/{obj["expected"]} municípios. Barra azul: Q1 a Q3; ponto laranja: mediana. Escala individual deste gráfico.</p>{trend}</article>')
    return '<section id="graficos"><h2>Distribuição de indicadores entre municípios</h2><p>Gráficos calculados exclusivamente com quartis e medianas numéricas presentes no contexto fiscal. Não representam médias estaduais, séries inventadas nem valores dos municípios sem observação. Escalas individuais impedem comparação visual direta da extensão entre indicadores.</p><div class="chart-grid">'+''.join(charts)+'</div></section>'
