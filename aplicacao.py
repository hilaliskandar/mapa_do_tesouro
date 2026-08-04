"""Ponto de entrada da interface do Mapa do Tesouro."""

from dataclasses import asdict
from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao
from processamentos.construir_hierarquia_contabil import construir_hierarquia_contabil
from processamentos.construir_mapa_semantico import construir_mapa_semantico
from processamentos.normalizar_finbra import normalizar_arquivo_finbra
from processamentos.qualificar_codigos import qualificar_codigos
from processamentos.selecionar_agregacao_hierarquica import selecionar_agregacao_hierarquica
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

VERSAO_SISTEMA = "0.5.1"
ARQUIVO_REGRAS_SEMANTICAS = Path("referencias/catalogos/mapa_semantico_inicial.yaml")

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
executar_hierarquia = st.checkbox("Construir hierarquia e catalogo contabil", value=True)
executar_mapa_semantico = st.checkbox(
    "Aplicar mapa semantico aos registros qualificados",
    value=True,
    help=(
        "Classifica todos os codigos antes de qualquer selecao de totalizacao, preservando "
        "contas detalhadas como IPTU, ISS, ITBI e transferencias."
    ),
)
executar_selecao = st.checkbox(
    "Produzir selecoes de totalizacao e decomposicao",
    value=True,
    help=(
        "Gera uma selecao para totais sem dupla contagem e outra para composicao analitica "
        "baseada nas folhas observadas de cada recorte."
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
                    {"validacao_estrutural": {
                        "status": resultado_validacao.status,
                        "hash_finbra": resultado_validacao.hash_sha256,
                        "alertas_criticos": resultado_validacao.alertas_criticos,
                        "alertas_relevantes": resultado_validacao.alertas_relevantes,
                        "resultado_json": str(validacao_json),
                        "relatorio_html": str(validacao_html),
                    }},
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
                        {"normalizacao": {
                            "status": resultado_normalizacao.status,
                            "registros_contabeis": resultado_normalizacao.total_registros_contabeis,
                            "cabecalhos_sem_dicionario": resultado_normalizacao.total_cabecalhos_sem_dicionario,
                            "registros_sem_codigo": resultado_normalizacao.total_registros_sem_codigo_conta,
                            "duplicidades": resultado_normalizacao.total_duplicidades_observacao,
                            "inconsistencias_populacao": resultado_normalizacao.inconsistencias_populacao,
                            "resultado_json": str(normalizacao_json),
                            "relatorio_html": str(normalizacao_html),
                        }},
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
                        {"qualificacao_codigos": {
                            "status": resultado_qualificacao.status,
                            "registros": resultado_qualificacao.total_registros,
                            "registros_pendentes": resultado_qualificacao.total_registros_pendentes,
                            "cabecalhos_pendentes": resultado_qualificacao.total_cabecalhos_pendentes,
                            "pendencias_xlsx": resultado_qualificacao.arquivo_pendencias_xlsx,
                            "resultado_json": str(qualificacao_json),
                            "relatorio_html": str(qualificacao_html),
                        }},
                    )
                st.success("Qualificacao concluida.")

            resultado_hierarquia = None
            if executar_hierarquia and resultado_qualificacao is not None:
                with st.spinner("Construindo hierarquias especificas por bloco..."):
                    pasta_hierarquia = diretorio_execucao / "04_hierarquia_contabil"
                    resultado_hierarquia = construir_hierarquia_contabil(
                        diretorio_execucao / "03_classificacao_contabil", pasta_hierarquia
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {"hierarquia_contabil": {
                            "status": resultado_hierarquia.status,
                            "codigos_distintos": resultado_hierarquia.total_codigos_distintos,
                            "codigos_observados": resultado_hierarquia.total_codigos_observados,
                            "nos_conceituais_gerados": resultado_hierarquia.total_nos_conceituais_gerados,
                            "relacoes_pai_filho": resultado_hierarquia.total_relacoes_pai_filho,
                            "catalogo_xlsx": resultado_hierarquia.arquivo_catalogo_xlsx,
                            "resultado_json": resultado_hierarquia.arquivo_resultado_json,
                        }},
                    )
                st.success("Hierarquia contabil concluida.")

            resultado_mapa = None
            if executar_mapa_semantico and resultado_hierarquia is not None:
                with st.spinner("Aplicando conceitos semanticos a todos os codigos qualificados..."):
                    pasta_mapa = diretorio_execucao / "05_mapa_semantico"
                    resultado_mapa = construir_mapa_semantico(
                        diretorio_execucao / "03_classificacao_contabil",
                        diretorio_execucao / "04_hierarquia_contabil",
                        ARQUIVO_REGRAS_SEMANTICAS,
                        pasta_mapa,
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {"mapa_semantico": {
                            "status": resultado_mapa.status,
                            "versao_catalogo": resultado_mapa.versao_catalogo,
                            "registros_avaliados": resultado_mapa.total_registros_avaliados,
                            "registros_mapeados": resultado_mapa.total_registros_mapeados,
                            "registros_nao_mapeados": resultado_mapa.total_registros_nao_mapeados,
                            "ambiguidades": resultado_mapa.total_ambiguidades,
                            "mapa_xlsx": resultado_mapa.arquivo_mapa_xlsx,
                            "pendencias_xlsx": resultado_mapa.arquivo_pendencias_xlsx,
                            "resultado_json": resultado_mapa.arquivo_resultado_json,
                        }},
                    )
                st.success("Mapa semantico concluido.")
                metricas_mapa = st.columns(5)
                metricas_mapa[0].metric("Avaliados", f"{resultado_mapa.total_registros_avaliados:,}")
                metricas_mapa[1].metric("Mapeados", f"{resultado_mapa.total_registros_mapeados:,}")
                metricas_mapa[2].metric("Nao mapeados", f"{resultado_mapa.total_registros_nao_mapeados:,}")
                metricas_mapa[3].metric("Ambiguidades", f"{resultado_mapa.total_ambiguidades:,}")
                metricas_mapa[4].metric("Status", resultado_mapa.status)
                st.dataframe([asdict(item) for item in resultado_mapa.blocos], use_container_width=True)

            resultado_selecao = None
            if executar_selecao and resultado_hierarquia is not None:
                with st.spinner("Produzindo selecoes de totalizacao e decomposicao..."):
                    pasta_selecao = diretorio_execucao / "06_selecao_hierarquica"
                    resultado_selecao = selecionar_agregacao_hierarquica(
                        diretorio_execucao / "03_classificacao_contabil",
                        diretorio_execucao / "04_hierarquia_contabil",
                        pasta_selecao,
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {"selecao_hierarquica": {
                            "status": resultado_selecao.status,
                            "registros_avaliados": resultado_selecao.total_registros_avaliados,
                            "selecionados_totalizacao": resultado_selecao.total_selecionados_totalizacao,
                            "selecionados_decomposicao": resultado_selecao.total_selecionados_decomposicao,
                            "divergencias_conciliacao": resultado_selecao.total_divergencias_conciliacao,
                            "totalizacao_parquet": resultado_selecao.arquivo_totalizacao_parquet,
                            "decomposicao_parquet": resultado_selecao.arquivo_decomposicao_parquet,
                            "conciliacao_parquet": resultado_selecao.arquivo_conciliacao_parquet,
                            "selecao_xlsx": resultado_selecao.arquivo_selecao_xlsx,
                            "resultado_json": resultado_selecao.arquivo_resumo_json,
                        }},
                    )
                st.success("Selecoes hierarquicas concluidas.")
                metricas = st.columns(5)
                metricas[0].metric("Avaliados", f"{resultado_selecao.total_registros_avaliados:,}")
                metricas[1].metric("Totalizacao", f"{resultado_selecao.total_selecionados_totalizacao:,}")
                metricas[2].metric("Decomposicao", f"{resultado_selecao.total_selecionados_decomposicao:,}")
                metricas[3].metric("Divergencias", f"{resultado_selecao.total_divergencias_conciliacao:,}")
                metricas[4].metric("Status", resultado_selecao.status)
                st.dataframe([asdict(item) for item in resultado_selecao.blocos], use_container_width=True)

            st.write(f"**Diretorio:** `{contexto.diretorio}`")
            st.json(contexto.como_dicionario())
        except Exception as erro:
            st.exception(erro)

st.info(
    f"Versao {VERSAO_SISTEMA}: mapa semantico anterior a selecao e modos separados "
    "de totalizacao e decomposicao analitica."
)
