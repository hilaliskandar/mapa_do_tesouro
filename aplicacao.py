"""Ponto de entrada da interface do Mapa do Tesouro."""

from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao
from processamentos.validar_finbra import validar_arquivo_finbra
from relatorios.gerar_relatorio_validacao import (
    gerar_relatorio_html,
    gerar_relatorio_json,
)


VERSAO_SISTEMA = "0.2.1"

st.set_page_config(page_title="Mapa do Tesouro", page_icon="🗺️", layout="wide")

st.title("Mapa do Tesouro")
st.write(
    "Aplicacao auditavel para processamento, analise e visualizacao territorial "
    "de dados fiscais municipais."
)

arquivo_finbra = st.file_uploader("Selecione a base FINBRA", type=["xlsx", "xls"])

st.caption(
    "A cartografia padrao sera obtida de tbrugz/geodata-br e armazenada em cache local. "
    "Uma fonte alternativa pode ser fornecida para testes."
)
arquivo_cartografia = st.file_uploader(
    "Cartografia alternativa opcional",
    type=["json", "geojson"],
)

if st.button("Criar execucao e validar", type="primary"):
    if arquivo_finbra is None:
        st.error("A base FINBRA e obrigatoria.")
    else:
        try:
            gerenciador = GerenciadorExecucao(
                Path("execucoes"), versao_sistema=VERSAO_SISTEMA
            )
            contexto = gerenciador.criar_execucao(
                nome_arquivo_finbra=arquivo_finbra.name,
                nome_arquivo_cartografia=(
                    arquivo_cartografia.name if arquivo_cartografia else "geojs-100-mun.json"
                ),
            )
            diretorio_execucao = Path(contexto.diretorio)
            caminho_finbra = gerenciador.preservar_arquivo_enviado(
                arquivo_finbra.getvalue(),
                arquivo_finbra.name,
                diretorio_execucao,
            )
            if arquivo_cartografia is not None:
                gerenciador.preservar_arquivo_enviado(
                    arquivo_cartografia.getvalue(),
                    arquivo_cartografia.name,
                    diretorio_execucao,
                )

            with st.spinner("Lendo e validando as abas da base FINBRA..."):
                resultado = validar_arquivo_finbra(caminho_finbra)
                pasta_validacao = diretorio_execucao / "01_validacao_estrutural"
                caminho_json = gerar_relatorio_json(
                    resultado, pasta_validacao / "resultado_validacao.json"
                )
                caminho_html = gerar_relatorio_html(
                    resultado, pasta_validacao / "relatorio_validacao.html"
                )
                gerenciador.atualizar_manifesto(
                    diretorio_execucao,
                    {
                        "validacao_estrutural": {
                            "status": resultado.status,
                            "hash_finbra": resultado.hash_sha256,
                            "alertas_criticos": resultado.alertas_criticos,
                            "alertas_relevantes": resultado.alertas_relevantes,
                            "resultado_json": str(caminho_json),
                            "relatorio_html": str(caminho_html),
                        }
                    },
                )

            st.success(f"Execucao validada: {contexto.identificador}")
            colunas = st.columns(6)
            colunas[0].metric("Abas", len(resultado.abas))
            colunas[1].metric("Anos reconhecidos", len(resultado.anos_consolidados))
            colunas[2].metric("Municipios", resultado.total_municipios_estimado or 0)
            colunas[3].metric("Codigos IBGE", resultado.total_codigos_ibge or 0)
            colunas[4].metric("Alertas criticos", resultado.alertas_criticos)
            colunas[5].metric("Alertas relevantes", resultado.alertas_relevantes)
            st.write(f"**Status:** {resultado.status}")
            st.write(f"**Diretorio:** `{contexto.diretorio}`")
            st.dataframe(
                [
                    {
                        "aba": aba.nome,
                        "tipo": aba.tipo_aba,
                        "linhas": aba.linhas,
                        "colunas": aba.colunas,
                        "anos": ", ".join(map(str, aba.anos_encontrados)),
                        "municipios": aba.municipios_encontrados,
                        "codigos_ibge": aba.codigos_ibge_encontrados,
                        "alertas": len(aba.alertas),
                    }
                    for aba in resultado.abas
                ],
                use_container_width=True,
            )
            st.json(contexto.como_dicionario())
        except Exception as erro:
            st.exception(erro)

st.info(
    f"Versao {VERSAO_SISTEMA}: validacao distingue abas de dados e auxiliares, reconhece "
    "cabecalhos com acentos e extrai exercicios apenas de colunas temporais explicitas."
)
