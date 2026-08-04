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
            f"<td>{aba.valores_preservados:,}</td>"
            f"<td>{aba.valores_ausentes_omitidos:,}</td>"
            f"<td>{aba.valores_nao_numericos:,}</td>"
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
table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
th, td {{ border: 1px solid #bbb; padding: 8px; vertical-align: top; }}
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
<div class="cartao"><strong>Abas processadas</strong><br>{len(resultado.abas)}</div>
<div class="cartao"><strong>Valores preservados</strong><br>{resultado.total_valores_preservados:,}</div>
<div class="cartao"><strong>Ausentes omitidos</strong><br>{resultado.total_ausentes_omitidos:,}</div>
<div class="cartao"><strong>Nao numericos</strong><br>{resultado.total_nao_numericos:,}</div>
</div>
<h2>Resultado por aba</h2>
<table>
<thead><tr><th>Aba</th><th>Tipo</th><th>Linhas de origem</th><th>Colunas de origem</th><th>Colunas de valores</th><th>Valores preservados</th><th>Ausentes omitidos</th><th>Nao numericos</th><th>Alertas</th></tr></thead>
<tbody>{''.join(linhas)}</tbody>
</table>
<h2>Transformacoes aplicadas</h2>
<ul>
<li>preservacao integral do arquivo de entrada;</li>
<li>padronizacao de identificadores para <span class="codigo">uf</span>, <span class="codigo">codigo_ibge</span>, <span class="codigo">municipio</span> e <span class="codigo">ano</span>;</li>
<li>conversao das abas de dados do formato largo para o formato longo;</li>
<li>manutencao dos rotulos contabeis originais;</li>
<li>decomposicao preliminar em estagio, codigo e descricao da conta;</li>
<li>omissao apenas de celulas sem valor, com contabilizacao explicita;</li>
<li>preservacao dos valores originais e criacao de campo numerico separado;</li>
<li>gravacao em Parquet para as etapas seguintes.</li>
</ul>
<h2>Nota metodologica</h2>
<p>A normalizacao reorganiza a estrutura dos dados sem agregar contas, corrigir valores ou produzir interpretacoes. As classificacoes contabeis permanecem preliminares e serao validadas em etapa posterior.</p>
</body>
</html>"""
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho
