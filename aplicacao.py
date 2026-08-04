"""Ponto de entrada da interface do Mapa do Tesouro."""

from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao


st.set_page_config(page_title="Mapa do Tesouro", page_icon="🗺️", layout="wide")

st.title("Mapa do Tesouro")
st.write(
    "Aplicacao auditavel para processamento, analise e visualizacao territorial "
    "de dados fiscais municipais."
)

arquivo_finbra = st.file_uploader("Selecione a base FINBRA", type=["xlsx", "xls"])
arquivo_cartografia = st.file_uploader("Selecione a cartografia municipal", type=["json", "geojson"])

if st.button("Iniciar validacao", type="primary"):
    if arquivo_finbra is None:
        st.error("A base FINBRA e obrigatoria.")
    else:
        gerenciador = GerenciadorExecucao(Path("execucoes"))
        contexto = gerenciador.criar_execucao(
            nome_arquivo_finbra=arquivo_finbra.name,
            nome_arquivo_cartografia=arquivo_cartografia.name if arquivo_cartografia else None,
        )
        st.success(f"Execucao criada: {contexto.identificador}")
        st.json(contexto.como_dicionario())

st.info(
    "Versao 0.1.0: estrutura inicial. As etapas de validacao, indicadores, mapas e "
    "relatorios serao incorporadas progressivamente."
)
