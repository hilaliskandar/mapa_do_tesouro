"""Ponto de entrada da interface do Mapa do Tesouro."""

from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao
from processamentos.construir_hierarquia_contabil import construir_hierarquia_contabil
from processamentos.normalizar_finbra import normalizar_arquivo_finbra
from processamentos.qualificar_codigos import qualificar_codigos
from processamentos.validar_finbra import validar_arquivo_finbra
from relatorios.gerar_relatorio_normalizacao import (
    gerar_relatorio_html as gerar_relatorio_normalizacao_html,
    gerar_relatorio_json as gerar_relatorio_normalizacao_json,
)
from relatorios.gerar_relatorio_qualificacao import (
    gerar_relatorio_html as gerar_relatorio_qualificacao_html,
    gerar_relatorio_json as gerar_relatorio_qualificacao_json,
)
from relatorios.gerar_relatorio_validacao import (
    gerar_relatorio_html as gerar_relatorio_validacao_html,
    gerar_relatorio_json as gerar_relatorio_validacao_json,
)

VERSAO_SISTEMA = "0.4.0"

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
executar_normalizacao = st.checkbox("Normalizar a base apos a validacao", value=True)
executar_qualificacao = st.checkbox("Qualificar codigos e registros estruturais", value=True)
executar_hierarquia = st.checkbox(
    "Construir hierarquia e catalogo contabil",
    value=True,
    help=(
        "Gera o catalogo mestre de codigos, relacoes pai-filho, niveis hierarquicos, "
        "ocorrencias temporais e classificacao calculada entre contas sinteticas e terminais."
    ),
)

if st.button("Criar execucao e processar", type="primary"):
    if arquivo_finbra is None:
        st.error("A base FINBRA e obrigatoria.")
    else:
        try:
            gerenciador = GerenciadorExecucao(Path("execucoes"), versao_sistema=VERSAO_SISTEMA)
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
                    arquivo_cartografia.getvalue(), arquivo_cartografia.name, diretorio_execucao
                )

            with st.spinner("Validando a estrutura da base FINBRA..."):
                resultado_validacao = validar_arquivo_finbra(caminho_finbra)
                pasta_validacao = diretorio_execucao / "01_validacao_estrutural"
                validacao_json = gerar_relatorio_validacao_json(
                    resultado_validacao, pasta_validacao / "resultado_validacao.json"
                )
                validacao_html = gerar_relatorio_validacao_html(
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
                            "resultado_json": str(validacao_json),
                            "relatorio_html": str(validacao_html),
                        }
                    },
                )

            st.success(f"Execucao validada: {contexto.identificador}")
            colunas = st.columns(6)
            colunas[0].metric("Abas", len(resultado_validacao.abas))
            colunas[1].metric("Anos", len(resultado_validacao.anos_consolidados))
            colunas[2].metric("Municipios", resultado_validacao.total_municipios_estimado or 0)
            colunas[3].metric("Codigos IBGE", resultado_validacao.total_codigos_ibge or 0)
            colunas[4].metric("Alertas criticos", resultado_validacao.alertas_criticos)
            colunas[5].metric("Alertas relevantes", resultado_validacao.alertas_relevantes)

            resultado_normalizacao = None
            if executar_normalizacao and resultado_validacao.status != "reprovado":
                with st.spinner("Normalizando matrizes e conciliando metadados..."):
                    pasta_normalizacao = diretorio_execucao / "02_normalizacao"
                    resultado_normalizacao = normalizar_arquivo_finbra(caminho_finbra, pasta_normalizacao)
                    normalizacao_json = gerar_relatorio_normalizacao_json(
                        resultado_normalizacao, pasta_normalizacao / "resultado_normalizacao.json"
                    )
                    normalizacao_html = gerar_relatorio_normalizacao_html(
                        resultado_normalizacao, pasta_normalizacao / "relatorio_normalizacao.html"
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {
                            "normalizacao": {
                                "status": resultado_normalizacao.status,
                                "registros_contabeis": resultado_normalizacao.total_registros_contabeis,
                                "cabecalhos_sem_dicionario": resultado_normalizacao.total_cabecalhos_sem_dicionario,
                                "registros_sem_codigo": resultado_normalizacao.total_registros_sem_codigo_conta,
                                "duplicidades": resultado_normalizacao.total_duplicidades_observacao,
                                "inconsistencias_populacao": resultado_normalizacao.inconsistencias_populacao,
                                "resultado_json": str(normalizacao_json),
                                "relatorio_html": str(normalizacao_html),
                            }
                        },
                    )
                st.success("Normalizacao concluida.")

            resultado_qualificacao = None
            if executar_qualificacao and resultado_normalizacao is not None:
                with st.spinner("Qualificando codigos, totais, deducoes e funcoes..."):
                    pasta_qualificacao = diretorio_execucao / "03_classificacao_contabil"
                    resultado_qualificacao = qualificar_codigos(
                        diretorio_execucao / "02_normalizacao", pasta_qualificacao
                    )
                    qualificacao_json = gerar_relatorio_qualificacao_json(
                        resultado_qualificacao, pasta_qualificacao / "resultado_qualificacao.json"
                    )
                    qualificacao_html = gerar_relatorio_qualificacao_html(
                        resultado_qualificacao, pasta_qualificacao / "relatorio_qualificacao.html"
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {
                            "qualificacao_codigos": {
                                "status": resultado_qualificacao.status,
                                "registros": resultado_qualificacao.total_registros,
                                "registros_pendentes": resultado_qualificacao.total_registros_pendentes,
                                "cabecalhos_pendentes": resultado_qualificacao.total_cabecalhos_pendentes,
                                "pendencias_xlsx": resultado_qualificacao.arquivo_pendencias_xlsx,
                                "resultado_json": str(qualificacao_json),
                                "relatorio_html": str(qualificacao_html),
                            }
                        },
                    )
                st.success("Qualificacao concluida.")
                metricas = st.columns(4)
                metricas[0].metric("Registros", f"{resultado_qualificacao.total_registros:,}")
                metricas[1].metric("Pendentes", f"{resultado_qualificacao.total_registros_pendentes:,}")
                metricas[2].metric("Cabecalhos pendentes", f"{resultado_qualificacao.total_cabecalhos_pendentes:,}")
                metricas[3].metric("Status", resultado_qualificacao.status)

            if executar_hierarquia and resultado_qualificacao is not None:
                with st.spinner("Construindo catalogo e relacoes hierarquicas..."):
                    pasta_hierarquia = diretorio_execucao / "04_hierarquia_contabil"
                    resultado_hierarquia = construir_hierarquia_contabil(
                        diretorio_execucao / "03_classificacao_contabil", pasta_hierarquia
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {
                            "hierarquia_contabil": {
                                "status": resultado_hierarquia.status,
                                "codigos_distintos": resultado_hierarquia.total_codigos_distintos,
                                "relacoes_pai_filho": resultado_hierarquia.total_relacoes_pai_filho,
                                "catalogo_parquet": resultado_hierarquia.arquivo_catalogo_parquet,
                                "catalogo_xlsx": resultado_hierarquia.arquivo_catalogo_xlsx,
                                "relacoes_parquet": resultado_hierarquia.arquivo_relacoes_parquet,
                                "resultado_json": resultado_hierarquia.arquivo_resultado_json,
                            }
                        },
                    )
                st.success("Hierarquia contabil concluida.")
                metricas_hierarquia = st.columns(3)
                metricas_hierarquia[0].metric(
                    "Codigos distintos", f"{resultado_hierarquia.total_codigos_distintos:,}"
                )
                metricas_hierarquia[1].metric(
                    "Relacoes pai-filho", f"{resultado_hierarquia.total_relacoes_pai_filho:,}"
                )
                metricas_hierarquia[2].metric("Status", resultado_hierarquia.status)
                st.dataframe(
                    [
                        {
                            "bloco": item.bloco,
                            "codigos": item.codigos_distintos,
                            "terminais": item.contas_terminais,
                            "sinteticas": item.contas_sinteticas,
                            "sem_pai_no_catalogo": item.codigos_sem_pai_identificado,
                            "maior_nivel": item.maior_nivel,
                        }
                        for item in resultado_hierarquia.blocos
                    ],
                    use_container_width=True,
                )
                st.write(f"**Catalogo contabil:** `{resultado_hierarquia.arquivo_catalogo_xlsx}`")

            st.write(f"**Diretorio:** `{contexto.diretorio}`")
            st.json(contexto.como_dicionario())
        except Exception as erro:
            st.exception(erro)

st.info(
    f"Versao {VERSAO_SISTEMA}: preparacao auditavel dos dados e construcao inicial "
    "da hierarquia e do catalogo contabil."
)
