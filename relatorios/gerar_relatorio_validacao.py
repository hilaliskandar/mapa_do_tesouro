"""Geracao de relatorios da validacao estrutural FINBRA."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path

from processamentos.validar_finbra import ResultadoValidacao


def gerar_relatorio_json(resultado: ResultadoValidacao, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(resultado.como_dicionario(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return destino


def gerar_relatorio_html(resultado: ResultadoValidacao, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    linhas_abas = []
    for aba in resultado.abas:
        alertas = "<br>".join(
            f"<strong>{escape(alerta['nivel'])}</strong>: {escape(alerta['mensagem'])}"
            for alerta in aba.alertas
        ) or "Sem alertas"
        linhas_abas.append(
            "<tr>"
            f"<td>{escape(aba.nome)}</td>"
            f"<td>{aba.linhas}</td>"
            f"<td>{aba.colunas}</td>"
            f"<td>{', '.join(map(str, aba.anos_encontrados)) or '-'}</td>"
            f"<td>{aba.municipios_encontrados if aba.municipios_encontrados is not None else '-'}</td>"
            f"<td>{aba.codigos_ibge_encontrados if aba.codigos_ibge_encontrados is not None else '-'}</td>"
            f"<td>{alertas}</td>"
            "</tr>"
        )

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Relatorio de validacao FINBRA</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
h1, h2 {{ color: #17324d; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
th, td {{ border: 1px solid #bbb; padding: 8px; vertical-align: top; }}
th {{ background: #eef3f7; }}
.codigo {{ font-family: Consolas, monospace; word-break: break-all; }}
.resumo {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
.cartao {{ border: 1px solid #ccc; padding: 12px; border-radius: 6px; }}
</style>
</head>
<body>
<h1>Relatorio de validacao estrutural FINBRA</h1>
<p><strong>Arquivo:</strong> {escape(resultado.arquivo)}</p>
<p><strong>Hash SHA-256:</strong> <span class="codigo">{resultado.hash_sha256}</span></p>
<p><strong>Status:</strong> {escape(resultado.status)}</p>
<div class="resumo">
<div class="cartao"><strong>Abas</strong><br>{len(resultado.abas)}</div>
<div class="cartao"><strong>Alertas criticos</strong><br>{resultado.alertas_criticos}</div>
<div class="cartao"><strong>Alertas relevantes</strong><br>{resultado.alertas_relevantes}</div>
</div>
<h2>Cobertura identificada</h2>
<p><strong>Anos:</strong> {', '.join(map(str, resultado.anos_consolidados)) or 'nao reconhecidos'}</p>
<p><strong>Municipios estimados:</strong> {resultado.total_municipios_estimado if resultado.total_municipios_estimado is not None else 'nao reconhecidos'}</p>
<p><strong>Codigos IBGE:</strong> {resultado.total_codigos_ibge if resultado.total_codigos_ibge is not None else 'nao reconhecidos'}</p>
<h2>Resultado por aba</h2>
<table>
<thead><tr><th>Aba</th><th>Linhas</th><th>Colunas</th><th>Anos</th><th>Municipios</th><th>Codigos IBGE</th><th>Alertas</th></tr></thead>
<tbody>{''.join(linhas_abas)}</tbody>
</table>
<h2>Nota metodologica</h2>
<p>Esta etapa verifica estrutura, cobertura e problemas formais do arquivo. Nenhuma conta e reclassificada e nenhum valor e alterado. A base de entrada permanece preservada para auditoria.</p>
</body>
</html>"""
    destino.write_text(html, encoding="utf-8")
    return destino
