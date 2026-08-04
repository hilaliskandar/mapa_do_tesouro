"""Ponto de entrada da interface do Mapa do Tesouro."""

from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao
from processamentos.normalizar_finbra import normalizar_arquivo_finbra
from processamentos.validar_finbra import validar_arquivo_finbra
from relatorios.gerar_relatorio_normalizacao import (
    gerar_relatorio_html as gerar_relatorio_normalizacao_html,
    gerar_relatorio_json as gerar_relatorio_normalizacao_json,
)
from relatorios.gerar_relatorio_validacao import (
    gerar_relatorio_html as gerar_relatorio_validacao_html,
    gerar_relatorio_json as gerar_relatorio_validacao_json,
)


VERSAO_SISTEMA = "0.3.0"

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

executar_normalizacao = st.checkbox(
    "Normalizar a base apos a validacao",
    value=True,
    help="Converte as abas de dados para formato longo e grava arquivos Parquet auditaveis.",
)

if st.button("Criar execucao e processar", type="primary"):
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
                resultado_validacao = validar_arquivo_finbra(caminho_finbra)
                pasta_validacao = diretorio_execucao / "01_validacao_estrutural"
                caminho_validacao_json = gerar_relatorio_validacao_json(
                    resultado_validacao,
                    pasta_validacao / "resultado_validacao.json",
                )
                caminho_validacao_html = gerar_relatorio_validacao_html(
                    resultado_validacao,
                    pasta_validacao / "relatorio_validacao.html",
                )
                gerenciador.atualizar_manifesto(
                    diretorio_execucao,
                    {
                        "validacao_estrutural": {
                            "status": resultado_validacao.status,
                            "hash_finbra": resultado_validacao.hash_sha256,
                            "alertas_criticos": resultado_validacao.alertas_criticos,
                            "alertas_relevantes": resultado_validacao.alertas_relevantes,
                            "resultado_json": str(caminho_validacao_json),
                            "relatorio_html": str(caminho_validacao_html),
                        }
                    },
                )

            st.success(f"Execucao validada: {contexto.identificador}")
            colunas = st.columns(6)
            colunas[0].metric("Abas", len(resultado_validacao.abas))
            colunas[1].metric("Anos reconhecidos", len(resultado_validacao.anos_consolidados))
            colunas[2].metric("Municipios", resultado_validacao.total_municipios_estimado or 0)
            colunas[3].metric("Codigos IBGE", resultado_validacao.total_codigos_ibge or 0)
            colunas[4].metric("Alertas criticos", resultado_validacao.alertas_criticos)
            colunas[5].metric("Alertas relevantes", resultado_validacao.alertas_relevantes)
            st.write(f"**Status da validacao:** {resultado_validacao.status}")

            if executar_normalizacao and resultado_validacao.status != "reprovado":
                with st.spinner(
                    "Normalizando as abas. Esta etapa pode levar alguns minutos devido ao volume de contas..."
                ):
                    pasta_normalizacao = diretorio_execucao / "02_normalizacao"
                    resultado_normalizacao = normalizar_arquivo_finbra(
                        caminho_finbra,
                        pasta_normalizacao,
                    )
                    caminho_normalizacao_json = gerar_relatorio_normalizacao_json(
                        resultado_normalizacao,
                        pasta_normalizacao / "resultado_normalizacao.json",
                    )
                    caminho_normalizacao_html = gerar_relatorio_normalizacao_html(
                        resultado_normalizacao,
                        pasta_normalizacao / "relatorio_normalizacao.html",
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {
                            "normalizacao": {
                                "status": resultado_normalizacao.status,
                                "valores_preservados": resultado_normalizacao.total_valores_preservados,
                                "ausentes_omitidos": resultado_normalizacao.total_ausentes_omitidos,
                                "valores_nao_numericos": resultado_normalizacao.total_nao_numericos,
                                "alertas_criticos": resultado_normalizacao.alertas_criticos,
                                "alertas_relevantes": resultado_normalizacao.alertas_relevantes,
                                "resultado_json": str(caminho_normalizacao_json),
                                "relatorio_html": str(caminho_normalizacao_html),
                            }
                        },
                    )

                st.success("Normalizacao concluida.")
                metricas_normalizacao = st.columns(4)
                metricas_normalizacao[0].metric(
                    "Valores preservados",
                    f"{resultado_normalizacao.total_valores_preservados:,}",
                )
                metricas_normalizacao[1].metric(
                    "Ausentes omitidos",
                    f"{resultado_normalizacao.total_ausentes_omitidos:,}",
                )
                metricas_normalizacao[2].metric(
                    "Nao numericos",
                    f"{resultado_normalizacao.total_nao_numericos:,}",
                )
                metricas_normalizacao[3].metric(
                    "Status",
                    resultado_normalizacao.status,
                )
                st.dataframe(
                    [
                        {
                            "aba": aba.aba_origem,
                            "tipo": aba.tipo,
                            "linhas_origem": aba.linhas_origem,
                            "colunas_origem": aba.colunas_origem,
                            "colunas_valores": aba.colunas_valores,
                            "valores_preservados": aba.valores_preservados,
                            "ausentes_omitidos": aba.valores_ausentes_omitidos,
                            "nao_numericos": aba.valores_nao_numericos,
                            "alertas": len(aba.alertas),
                        }
                        for aba in resultado_normalizacao.abas
                    ],
                    use_container_width=True,
                )

            st.write(f"**Diretorio:** `{contexto.diretorio}`")
            st.json(contexto.como_dicionario())
        except Exception as erro:
            st.exception(erro)

st.info(
    f"Versao {VERSAO_SISTEMA}: validacao estrutural e normalizacao auditavel para formato "
    "longo, com preservacao dos rotulos originais, arquivos Parquet e relatorios por etapa."
)
