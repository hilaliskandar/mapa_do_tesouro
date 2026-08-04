"""Ponto de entrada da interface do Mapa do Tesouro."""

from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao


VERSAO_SISTEMA = "0.1.1"

st.set_page_config(page_title="Mapa do Tesouro", page_icon="🗺️", layout="wide")

st.title("Mapa do Tesouro")
st.write(
    "Aplicacao auditavel para processamento, analise e visualizacao territorial "
    "de dados fiscais municipais."
)

arquivo_finbra = st.file_uploader("Selecione a base FINBRA", type=["xlsx", "xls"])

st.caption(
    "A cartografia padrao sera obtida de tbrugz/geodata-br e armazenada em cache local. "
    "Uma fonte alternativa podera ser configurada futuramente."
)
arquivo_cartografia = st.file_uploader(
    "Cartografia alternativa opcional",
    type=["json", "geojson"],
)

if st.button("Iniciar validacao", type="primary"):
    if arquivo_finbra is None:
        st.error("A base FINBRA e obrigatoria.")
    else:
        gerenciador = GerenciadorExecucao(Path("execucoes"))
        contexto = gerenciador.criar_execucao(
            nome_arquivo_finbra=arquivo_finbra.name,
            nome_arquivo_cartografia=(
                arquivo_cartografia.name if arquivo_cartografia else "geojs-100-mun.json"
            ),
        )
        st.success(f"Execucao criada: {contexto.identificador}")
        st.json(contexto.como_dicionario())

st.info(
    f"Versao {VERSAO_SISTEMA}: estrutura inicial com cartografia remota configuravel, "
    "cache local e registro de procedencia."
)
