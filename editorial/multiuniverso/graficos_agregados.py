"""Decomposicao estrita de agregados selecionados, seguindo calculate_annual.AGGREGATIONS.

Exige que todas as parcelas e o agregado oficial estejam observados no mesmo ano
e que sua soma seja reconciliada antes de desenhar participacoes.
"""
import html,math
GROUPS=(
 ("tributos_imobiliarios","Tributos imobiliários selecionados",(
  ("dca_iptu_principal","IPTU principal"),("dca_itbi_principal","ITBI principal"))),
 ("transferencias_selecionadas","Transferências selecionadas",(
  ("dca_fpm_cota_mensal","FPM cota mensal"),("dca_icms_cota_parte","Cota-parte do ICMS"),("dca_ipva_cota_parte","Cota-parte do IPVA"))),
 ("despesa_territorial","Despesas territoriais selecionadas",(
  ("dca_func_urbanismo_liquidada","Urbanismo"),("dca_func_habitacao_liquidada","Habitação"),
  ("dca_func_saneamento_liquidada","Saneamento"),("dca_func_gestao_ambiental_liquidada","Gestão ambiental"),
  ("dca_func_transporte_liquidada","Transporte"))),
 ("despesas_capital_selecionadas","Despesas de capital selecionadas",(
  ("dca_investimentos_liquidada","Investimentos"),("dca_inversoes_financeiras_liquidada","Inversões financeiras"),
  ("dca_amortizacao_divida_liquidada","Amortização da dívida"))),
 ("receitas_capital_selecionadas","Receitas de capital selecionadas",(
  ("dca_operacoes_credito","Operações de crédito"),("dca_alienacao_bens","Alienação de bens"),
  ("dca_transferencias_capital","Transferências de capital"))),
)
def esc(v):return html.escape(str(v),quote=True)
def observed(obj):
    latest=(obj or {}).get("latest") or {}
    v=latest.get("value");year=latest.get("year")
    if latest.get("status")!="observado" or isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or year is None:return None
    return (float(v),str(year))
def reconcile(payload):
    variables=payload.get("variables") or {}
    accepted=[];rejected=[]
    for total_id,title,components in GROUPS:
        total=observed(variables.get(total_id))
        parts=[observed(variables.get(k)) for k,_ in components]
        if total is None or any(x is None for x in parts):
            rejected.append((total_id,"observação incompleta"))
            continue
        number,year=total
        if number<=0 or any(p[1]!=year or p[0]<0 for p in parts):
            rejected.append((total_id,"exercício divergente ou valor inválido"))
            continue
        summed=math.fsum(p[0] for p in parts)
        if not math.isclose(number,summed,rel_tol=1e-9,abs_tol=0.01):
            rejected.append((total_id,"soma das parcelas divergente"))
            continue
        accepted.append((total_id,title,year,number,[(k,label,p[0],100*p[0]/number) for (k,label),p in zip(components,parts)]))
    return accepted,rejected

def build(payload):
    accepted,rejected=reconcile(payload)
    if not accepted:
        return ('<section id="decomposicao"><h2>Decomposição de agregados selecionados</h2>'
                '<p>Nenhum conjunto de parcelas apresentou observações completas, mesmo exercício e '
                'reconciliação com o agregado oficial. Não foram calculadas participações estimadas.</p></section>')
    cards=[]
    for identifier,title,year,total,parts in accepted:
        rows=[]
        for key,label,value,pct in parts:
            width=5*pct
            width_label=f"{pct:.1f}".replace(".",",")
            rows.append(f'<tr><th scope="row">{esc(label)}</th><td>{width_label}%</td>'
                        f'<td><svg role="img" aria-label="{esc(label)}: {width_label}%" viewBox="0 0 500 22">'
                        f'<rect width="500" height="22" fill="#e7eff4" rx="3"/>'
                        f'<rect width="{width:.2f}" height="22" fill="#24769c" rx="3"/></svg></td></tr>')
        cards.append(f'<article class="chart-card" data-total="{esc(identifier)}"><h3>{esc(title)}</h3>'
                     f'<p>Exercício {esc(year)}. Denominador: {esc(identifier)}. Soma das parcelas reconciliada '
                     f'com o agregado, em valores monetários observados. Percentuais calculados por 100 × parcela ÷ agregado.</p>'
                     f'<div class="scroll"><table><thead><tr><th>Parcela</th><th>Participação</th><th>Distribuição</th></tr></thead><tbody>'
                     +''.join(rows)+'</tbody></table></div></article>')
    return ('<section id="decomposicao"><h2>Decomposição de agregados selecionados</h2>'
            '<p>Cada conjunto soma 100% apenas dentro de seu próprio agregado e exercício. '
            'Os agregados são recortes específicos das contas fiscais e não representam, necessariamente, '
            'toda a receita ou toda a despesa municipal. Gráficos omitidos quando não reconciliados.</p>'
            '<div class="chart-grid">'+''.join(cards)+'</div></section>')
