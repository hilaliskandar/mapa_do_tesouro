"""Comparacao municipal SVG exclusivamente para dados observados e mediana do grupo."""
import html,math

def esc(v):return html.escape(str(v),quote=True)
def num(v):return isinstance(v,(float,int)) and not isinstance(v,bool) and math.isfinite(v)

def charts(obj,shown,limit=4):
    selected=[]
    for key,detail in sorted((obj.get("variables") or {}).items()):
        latest=detail.get("latest") or {}
        group=detail.get("group_latest") or {}
        md=detail.get("metadata") or {}
        value=latest.get("value")
        median=(group.get("numeric") or {}).get("median")
        unit=md.get("unidade") or ""
        if latest.get("status")!="observado" or not num(value) or not num(median):continue
        if unit not in ("percentual","BRL","R$","reais","moeda","numero","habitantes"):continue
        if unit=="percentual" and (key in ("dtp_pct_rcl","dc_pct_rcl","dcl_pct_rcl","rgf_dtp_percentual_rcl","rgf02_dc_percentual_rcl","rgf02_dcl_percentual_rcl")):
            pass
        obs=group.get("observed");expected=group.get("expected")
        if not isinstance(obs,int) or not isinstance(expected,int) or obs<4 or obs>expected:continue
        selected.append((-(obs/expected),str(key),value,median,unit,str(md.get("nome") or key),obs,expected))
    selected.sort()
    if not selected:return '<section id="comparacoes"><h2>Comparações municipais</h2><p>Sem pares numéricos município e mediana com cobertura suficiente.</p></section>'
    cards=[]
    for _,key,value,median,unit,label,obs,expected in selected[:limit]:
        low=min(0,value,median);high=max(0,value,median)
        if high==low:high=low+1
        x=lambda v:90+460*(v-low)/(high-low)
        symbols=(f'<circle cx="{x(value):.2f}" cy="54" r="9" fill="#d97706"/>'
                 f'<rect x="{x(median)-7:.2f}" y="77" width="14" height="14" fill="#24769c"/>')
        svg=(f'<svg role="img" aria-label="Comparação de {esc(label)} entre município e mediana do grupo" viewBox="0 0 640 125">'
             f'<title>{esc(label)}</title><text x="8" y="58" font-size="13">Município</text>'
             f'<text x="8" y="89" font-size="13">Mediana</text><line x1="90" y1="107" x2="550" y2="107" stroke="#8899a7"/>'
             +symbols+'</svg>')
        cards.append(f'<article class="chart-card"><h3>{esc(label)}</h3>{svg}'
                     f'<p>Município: {esc(shown(value,unit,key))}. Mediana do universo: {esc(shown(median,unit,key))}.'
                     f' Cobertura: {obs}/{expected}. Escala própria. A diferença não é uma avaliação de desempenho.</p></article>')
    return '<section id="comparacoes"><h2>Município e mediana do universo</h2><p>Comparações descritivas dos mesmos indicadores e unidades, exclusivamente com valores observados. O ponto laranja representa o município e o quadrado azul a mediana; a posição não representa avaliação de gestão.</p><div class="chart-grid">'+''.join(cards)+'</div></section>'
