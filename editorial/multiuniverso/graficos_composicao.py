"""Barras de participacao entre contas contabeis pareadas do mesmo municipio.

Nunca soma medianas regionais nem chama agregados parciais de composicao total.
"""
import html,math
PAIRS=(
 ("dca_receita_tributaria_bruta","dca_receita_corrente_bruta","Receita tributária na receita corrente"),
 ("dca_investimentos_liquidada","dca_despesa_total_liquidada","Investimentos na despesa total liquidada"),
 ("dca_despesa_corrente_liquidada","dca_despesa_total_liquidada","Despesa corrente na despesa total liquidada"),
)
def esc(value):return html.escape(str(value),quote=True)
def finite(v):return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
def observed(item):
    if not isinstance(item,dict):return None
    latest=item.get("latest") or {}
    if latest.get("status")!="observado":return None
    v=latest.get("value")
    if not finite(v):return None
    # Nao extrapolar exercicio a partir do 'latest_year' global: exigi-lo do registro.
    year=latest.get("year")
    return (v,str(year)) if year is not None else None

def build(payload):
    variables=payload.get("variables") or {}
    entries=[];issues=[]
    for numerator,denominator,title in PAIRS:
        a=observed(variables.get(numerator));b=observed(variables.get(denominator))
        if not a or not b:
            issues.append(f"{title}: contas ausentes ou sem exercício explícito")
            continue
        na,ya=a;de,yd=b
        if ya!=yd or de<=0 or na<0 or na>de:
            issues.append(f"{title}: exercícios incompatíveis ou participação inválida")
            continue
        rate=100*na/de
        width=max(0,min(100,rate))
        label=f"{rate:.1f}".replace(".",",")
        svg=(f'<svg role="img" aria-label="{esc(title)}: {label}% em {esc(ya)}" viewBox="0 0 550 60">'
             f'<title>{esc(title)} — {label}%</title>'
             f'<rect x="0" y="17" width="500" height="22" rx="4" fill="#e8edf1"/>'
             f'<rect x="0" y="17" width="{5*width:.2f}" height="22" rx="4" fill="#24769c"/>'
             f'<text x="505" y="34" font-size="14">{label}%</text></svg>')
        entries.append(f'<article class="chart-card"><h3>{esc(title)}</h3>{svg}'
                       f'<p>Exercício {esc(ya)}. Numerador: {esc(numerator)}; denominador: {esc(denominator)}.'
                       f' Cálculo: 100 × numerador ÷ denominador. Fonte: DCA/Siconfi.</p></article>')
    if entries:
        return ('<section id="composicao"><h2>Participações contábeis selecionadas</h2>'
                '<p>Proporções não exaustivas, obtidas por divisão de valores observados do mesmo '
                'município e exercício. Não são parcelas de um gráfico único: os denominadores '
                'diferem e não devem ser somados.</p><div class="chart-grid">'+''.join(entries)+'</div></section>')
    return ('<section id="composicao"><h2>Participações contábeis selecionadas</h2>'
            '<p>Não há pares de contas observadas com mesmo exercício explícito para calcular '
            'participações defensáveis. Nenhum valor foi estimado ou substituído por zero.</p></section>')
