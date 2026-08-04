"""Relatorios da qualificacao de codigos e pendencias."""

from __future__ import annotations

import html
import json
from pathlib import Path

from processamentos.qualificar_codigos import ResultadoQualificacao


def gerar_relatorio_json(resultado: ResultadoQualificacao, caminho: Path) -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(resultado.como_dicionario(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return caminho


def gerar_relatorio_html(resultado: ResultadoQualificacao, caminho: Path) -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    linhas = []
    for bloco in resultado.blocos:
        linhas.append(
            "<tr>"
            f"<td>{html.escape(bloco.bloco)}</td>"
            f"<td>{bloco.registros:,}</td>"
            f"<td>{bloco.cabecalhos_distintos:,}</td>"
            f"<td>{bloco.registros_com_codigo:,}</td>"
            f"<td>{bloco.registros_sem_codigo_justificado:,}</td>"
            f"<td>{bloco.registros_pendentes:,}</td>"
            f"<td>{bloco.cabecalhos_pendentes:,}</td>"
            f"<td>{bloco.registros_com_funcao:,}</td>"
            f"<td>{bloco.registros_com_subfuncao:,}</td>"
            f"<td>{bloco.funcoes_distintas:,}</td>"
            f"<td>{bloco.subfuncoes_distintas:,}</td>"
            f"<td>{bloco.agregados_funcionais_residuais:,}</td>"
            f"<td>{bloco.registros_intraorcamentarios:,}</td>"
            f"<td>{bloco.registros_deducao_receita:,}</td>"
            "</tr>"
        )

    conteudo = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Relatorio de qualificacao de codigos</title>
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
<h1>Relatorio de qualificacao de codigos</h1>
<p><strong>Status:</strong> {html.escape(resultado.status)}</p>
<div class="resumo">
<div class="cartao"><strong>Registros processados</strong><br>{resultado.total_registros:,}</div>
<div class="cartao"><strong>Registros pendentes</strong><br>{resultado.total_registros_pendentes:,}</div>
<div class="cartao"><strong>Cabecalhos pendentes</strong><br>{resultado.total_cabecalhos_pendentes:,}</div>
<div class="cartao"><strong>Planilha de revisao</strong><br><span class="codigo">pendencias_codigos_conta.xlsx</span></div>
</div>
<h2>Resultado por bloco</h2>
<table>
<thead><tr><th>Bloco</th><th>Registros</th><th>Cabecalhos</th><th>Com codigo</th><th>Ausencia justificada</th><th>Registros pendentes</th><th>Cabecalhos pendentes</th><th>Registros com funcao</th><th>Registros com subfuncao</th><th>Funcoes distintas</th><th>Subfuncoes distintas</th><th>Agregados residuais</th><th>Intraorcamentarios</th><th>Deducoes de receita</th></tr></thead>
<tbody>{''.join(linhas)}</tbody>
</table>
<h2>Regras aplicadas</h2>
<ul>
<li>extracao de codigos de receita e despesa com ou sem hifen, travessao ou dois-pontos;</li>
<li>classificacao de cada registro como conta terminal, conta sintetica, total ou subtotal, agregado funcional residual, indicador auxiliar ou nao classificado;</li>
<li>reconhecimento de codigos funcionais no formato NN.NNN e de agregados no formato FUxx;</li>
<li>identificacao de operacoes intraorcamentarias por rotulo, categorias 7 e 8 da receita e modalidade 91 da despesa;</li>
<li>identificacao preliminar de deducoes, restituicoes, retificacoes e registros associados ao Fundeb;</li>
<li>distincao entre ausencia de codigo justificada e pendencia efetiva de revisao;</li>
<li>agrupamento das pendencias por cabecalho, com quantidade de registros, anos, municipios e valor absoluto acumulado;</li>
<li>preservacao dos arquivos normalizados originais.</li>
</ul>
<h2>Produtos</h2>
<ul>
<li><span class="codigo">{html.escape(resultado.arquivo_pendencias_parquet)}</span></li>
<li><span class="codigo">{html.escape(resultado.arquivo_pendencias_xlsx)}</span></li>
</ul>
<p>O status <strong>revisao_necessaria</strong> nao significa perda de dados. Indica que existem cabecalhos sem codigo e sem justificativa automatica suficiente para uso nas agregacoes.</p>
</body>
</html>"""
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho
