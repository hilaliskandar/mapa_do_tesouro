"""Ponto de entrada da interface do Mapa do Tesouro."""

from pathlib import Path

import streamlit as st

from nucleo.gerenciador_execucao import GerenciadorExecucao
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

VERSAO_SISTEMA = "0.3.4"

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
executar_qualificacao = st.checkbox(
    "Qualificar codigos e gerar fila de revisao",
    value=True,
    help=(
        "Extrai codigos com variacoes de formato, classifica totais, operacoes "
        "intraorcamentarias, deducoes, funcoes e subfuncoes."
    ),
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

            resultado_normalizacao = None
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

            if (
                executar_qualificacao
                and resultado_normalizacao is not None
                and resultado_normalizacao.status != "reprovado"
            ):
                with st.spinner(
                    "Qualificando codigos, totais, intraorcamentarias, deducoes e funcoes..."
                ):
                    pasta_qualificacao = diretorio_execucao / "03_classificacao_contabil"
                    resultado_qualificacao = qualificar_codigos(
                        diretorio_execucao / "02_normalizacao", pasta_qualificacao
                    )
                    caminho_qualificacao_json = gerar_relatorio_qualificacao_json(
                        resultado_qualificacao,
                        pasta_qualificacao / "resultado_qualificacao.json",
                    )
                    caminho_qualificacao_html = gerar_relatorio_qualificacao_html(
                        resultado_qualificacao,
                        pasta_qualificacao / "relatorio_qualificacao.html",
                    )
                    gerenciador.atualizar_manifesto(
                        diretorio_execucao,
                        {
                            "qualificacao_codigos": {
                                "status": resultado_qualificacao.status,
                                "registros": resultado_qualificacao.total_registros,
                                "registros_pendentes": resultado_qualificacao.total_registros_pendentes,
                                "cabecalhos_pendentes": resultado_qualificacao.total_cabecalhos_pendentes,
                                "pendencias_parquet": resultado_qualificacao.arquivo_pendencias_parquet,
                                "pendencias_xlsx": resultado_qualificacao.arquivo_pendencias_xlsx,
                                "resultado_json": str(caminho_qualificacao_json),
                                "relatorio_html": str(caminho_qualificacao_html),
                            }
                        },
                    )

                st.success("Qualificacao concluida.")
                metricas_qualificacao = st.columns(4)
                metricas_qualificacao[0].metric(
                    "Registros qualificados", f"{resultado_qualificacao.total_registros:,}"
                )
                metricas_qualificacao[1].metric(
                    "Registros pendentes", f"{resultado_qualificacao.total_registros_pendentes:,}"
                )
                metricas_qualificacao[2].metric(
                    "Cabecalhos pendentes", f"{resultado_qualificacao.total_cabecalhos_pendentes:,}"
                )
                metricas_qualificacao[3].metric("Status", resultado_qualificacao.status)
                st.dataframe(
                    [
                        {
                            "bloco": bloco.bloco,
                            "registros": bloco.registros,
                            "cabecalhos": bloco.cabecalhos_distintos,
                            "com_codigo": bloco.registros_com_codigo,
                            "ausencia_justificada": bloco.registros_sem_codigo_justificado,
                            "registros_pendentes": bloco.registros_pendentes,
                            "cabecalhos_pendentes": bloco.cabecalhos_pendentes,
                            "registros_com_funcao": bloco.registros_com_funcao,
                            "registros_com_subfuncao": bloco.registros_com_subfuncao,
                            "funcoes_distintas": bloco.funcoes_distintas,
                            "subfuncoes_distintas": bloco.subfuncoes_distintas,
                            "agregados_residuais": bloco.agregados_funcionais_residuais,
                            "intraorcamentarios": bloco.registros_intraorcamentarios,
                            "deducoes_receita": bloco.registros_deducao_receita,
                        }
                        for bloco in resultado_qualificacao.blocos
                    ],
                    use_container_width=True,
                )
                st.write(
                    f"**Planilha de revisao:** `{resultado_qualificacao.arquivo_pendencias_xlsx}`"
                )

            st.write(f"**Diretorio:** `{contexto.diretorio}`")
            st.json(contexto.como_dicionario())
        except Exception as erro:
            st.exception(erro)

st.info(
    f"Versao {VERSAO_SISTEMA}: qualificacao normativa de codigos, totais, operacoes "
    "intraorcamentarias, deducoes, funcoes, subfuncoes e fila auditavel de revisao."
)
