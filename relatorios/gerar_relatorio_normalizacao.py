"""Geracao dos relatorios da etapa de normalizacao."""

from __future__ import annotations

import html
import json
from pathlib import Path

from processamentos.normalizar_finbra import ResultadoNormalizacao


def gerar_relatorio_json(resultado: ResultadoNormalizacao, caminho: Path) -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(resultado.como_dicionario(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return caminho


def gerar_relatorio_html(resultado: ResultadoNormalizacao, caminho: Path) -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    linhas = []
    for aba in resultado.abas:
        alertas = "<br>".join(
            f"<strong>{html.escape(alerta['nivel'])}</strong>: {html.escape(alerta['mensagem'])}"
            for alerta in aba.alertas
        ) or "Sem alertas"
        linhas.append(
            "<tr>"
            f"<td>{html.escape(aba.aba_origem)}</td>"
            f"<td>{html.escape(aba.tipo)}</td>"
            f"<td>{aba.linhas_origem:,}</td>"
            f"<td>{aba.colunas_origem:,}</td>"
            f"<td>{aba.colunas_valores:,}</td>"
            f"<td>{aba.valores_preenchidos_origem:,}</td>"
            f"<td>{aba.registros_contabeis_preservados:,}</td>"
            f"<td>{aba.cabecalhos_correspondidos_dicionario:,}</td>"
            f"<td>{aba.cabecalhos_sem_dicionario:,}</td>"
            f"<td>{aba.registros_sem_codigo_conta:,}</td>"
            f"<td>{aba.registros_sem_estagio:,}</td>"
            f"<td>{aba.duplicidades_observacao:,}</td>"
            f"<td>{alertas}</td>"
            "</tr>"
        )

    conteudo = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Relatorio de normalizacao FINBRA</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
h1, h2 {{ color: #17324d; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 16px; font-size: 12px; }}
th, td {{ border: 1px solid #bbb; padding: 7px; vertical-align: top; }}
th {{ background: #eef3f7; }}
.resumo {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
.cartao {{ border: 1px solid #ccc; padding: 12px; border-radius: 6px; }}
.codigo {{ font-family: Consolas, monospace; }}
</style>
</head>
<body>
<h1>Relatorio de normalizacao FINBRA</h1>
<p><strong>Arquivo:</strong> {html.escape(resultado.arquivo_origem)}</p>
<p><strong>Status:</strong> {html.escape(resultado.status)}</p>
<div class="resumo">
<div class="cartao"><strong>Registros contabeis</strong><br>{resultado.total_registros_contabeis:,}</div>
<div class="cartao"><strong>Celulas auxiliares</strong><br>{resultado.total_celulas_auxiliares_preservadas:,}</div>
<div class="cartao"><strong>Cabecalhos sem dicionario</strong><br>{resultado.total_cabecalhos_sem_dicionario:,}</div>
<div class="cartao"><strong>Inconsistencias de populacao</strong><br>{resultado.inconsistencias_populacao:,}</div>
</div>
<h2>Controles semanticos consolidados</h2>
<ul>
<li>valores ausentes omitidos nas matrizes contabeis: <strong>{resultado.total_ausentes_omitidos:,}</strong>;</li>
<li>valores preenchidos nao numericos: <strong>{resultado.total_nao_numericos:,}</strong>;</li>
<li>registros sem codigo de conta: <strong>{resultado.total_registros_sem_codigo_conta:,}</strong>;</li>
<li>registros sem estagio contabil: <strong>{resultado.total_registros_sem_estagio:,}</strong>;</li>
<li>duplicidades de observacao: <strong>{resultado.total_duplicidades_observacao:,}</strong>;</li>
<li>dimensao municipio-ano: <span class="codigo">{html.escape(resultado.arquivo_dimensao_municipio_ano)}</span>.</li>
</ul>
<h2>Resultado por aba</h2>
<table>
<thead><tr><th>Aba</th><th>Tipo</th><th>Linhas</th><th>Colunas</th><th>Contas</th><th>Preenchidos na origem</th><th>Registros contabeis</th><th>Cabecalhos no dicionario</th><th>Sem dicionario</th><th>Sem codigo</th><th>Sem estagio</th><th>Duplicidades</th><th>Alertas</th></tr></thead>
<tbody>{''.join(linhas)}</tbody>
</table>
<h2>Transformacoes aplicadas</h2>
<ul>
<li>preservacao integral do arquivo de entrada;</li>
<li>padronizacao de identificadores para <span class="codigo">uf</span>, <span class="codigo">codigo_ibge</span>, <span class="codigo">municipio</span>, <span class="codigo">ano</span> e <span class="codigo">populacao</span>;</li>
<li>separacao da populacao em uma dimensao municipio-ano, sem trata-la como conta financeira;</li>
<li>conversao das abas contabeis do formato largo para o formato longo;</li>
<li>uso da aba Dicionario como fonte primaria de estagio, codigo e descricao;</li>
<li>aplicacao de regra de contingencia apenas para cabecalhos ausentes do dicionario;</li>
<li>reconciliacao entre celulas preenchidas da matriz e registros longos;</li>
<li>controle de codigos ausentes, estagios ausentes e chaves duplicadas;</li>
<li>gravacao dos produtos em Parquet para as etapas seguintes.</li>
</ul>
<h2>Regra de aprovacao</h2>
<p>A etapa e reprovada quando ha perda de registros, populacao tratada como conta, divergencia populacional entre abas, ausencia de identificadores obrigatorios ou duplicidade de observacoes. Cabecalhos ausentes do dicionario e metadados contabeis incompletos geram alertas relevantes.</p>
</body>
</html>"""
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho
