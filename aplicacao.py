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


VERSAO_SISTEMA = "0.3.2"

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
    "Cartografia alternativa opcional", type=["json", "geojson"]
)
executar_normalizacao = st.checkbox(
    "Normalizar a base apos a validacao",
    value=True,
    help="Converte as abas contabeis para formato longo, aplica o dicionario e cria a dimensao municipio-ano.",
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
                arquivo_finbra.getvalue(), arquivo_finbra.name, diretorio_execucao
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
                    resultado_validacao, pasta_validacao / "resultado_validacao.json"
                )
                caminho_validacao_html = gerar_relatorio_validacao_html(
                    resultado_validacao, pasta_validacao / "relatorio_validacao.html"
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
                    "Normalizando as abas, conciliando o dicionario e validando a populacao..."
                ):
                    pasta_normalizacao = diretorio_execucao / "02_normalizacao"
                    resultado_normalizacao = normalizar_arquivo_finbra(
                        caminho_finbra, pasta_normalizacao
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
                                "registros_contabeis": resultado_normalizacao.total_registros_contabeis,
                                "celulas_auxiliares": resultado_normalizacao.total_celulas_auxiliares_preservadas,
                                "ausentes_omitidos": resultado_normalizacao.total_ausentes_omitidos,
                                "valores_nao_numericos": resultado_normalizacao.total_nao_numericos,
                                "cabecalhos_sem_dicionario": resultado_normalizacao.total_cabecalhos_sem_dicionario,
                                "registros_sem_codigo": resultado_normalizacao.total_registros_sem_codigo_conta,
                                "registros_sem_estagio": resultado_normalizacao.total_registros_sem_estagio,
                                "duplicidades": resultado_normalizacao.total_duplicidades_observacao,
                                "inconsistencias_populacao": resultado_normalizacao.inconsistencias_populacao,
                                "dimensao_municipio_ano": resultado_normalizacao.arquivo_dimensao_municipio_ano,
                                "alertas_criticos": resultado_normalizacao.alertas_criticos,
                                "alertas_relevantes": resultado_normalizacao.alertas_relevantes,
                                "resultado_json": str(caminho_normalizacao_json),
                                "relatorio_html": str(caminho_normalizacao_html),
                            }
                        },
                    )

                st.success("Normalizacao concluida.")
                metricas = st.columns(6)
                metricas[0].metric(
                    "Registros contabeis", f"{resultado_normalizacao.total_registros_contabeis:,}"
                )
                metricas[1].metric(
                    "Sem dicionario", f"{resultado_normalizacao.total_cabecalhos_sem_dicionario:,}"
                )
                metricas[2].metric(
                    "Sem codigo", f"{resultado_normalizacao.total_registros_sem_codigo_conta:,}"
                )
                metricas[3].metric(
                    "Sem estagio", f"{resultado_normalizacao.total_registros_sem_estagio:,}"
                )
                metricas[4].metric(
                    "Populacao divergente", f"{resultado_normalizacao.inconsistencias_populacao:,}"
                )
                metricas[5].metric("Status", resultado_normalizacao.status)
                st.dataframe(
                    [
                        {
                            "aba": aba.aba_origem,
                            "tipo": aba.tipo,
                            "contas": aba.colunas_valores,
                            "preenchidos_origem": aba.valores_preenchidos_origem,
                            "registros_contabeis": aba.registros_contabeis_preservados,
                            "cabecalhos_no_dicionario": aba.cabecalhos_correspondidos_dicionario,
                            "sem_dicionario": aba.cabecalhos_sem_dicionario,
                            "sem_codigo": aba.registros_sem_codigo_conta,
                            "sem_estagio": aba.registros_sem_estagio,
                            "duplicidades": aba.duplicidades_observacao,
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
    f"Versao {VERSAO_SISTEMA}: populacao separada das contas, dicionario como fonte primaria, "
    "reconciliacao quantitativa e controles semanticos da normalizacao."
)
