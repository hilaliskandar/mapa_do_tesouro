"""Construcao do mapa semantico anual a partir de regras externas versionadas.

A etapa associa registros ja selecionados sem dupla contagem a identificadores
semanticos estaveis. As regras ficam fora do codigo, em YAML, e podem limitar
bloco, periodo, codigo e descricao. Registros nao mapeados e ambiguidades ficam
explicitamente disponiveis para revisao humana.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import re
import unicodedata

import pandas as pd
import yaml


@dataclass
class ResultadoMapaSemanticoBloco:
    bloco: str
    registros_selecionados: int
    registros_mapeados: int
    registros_nao_mapeados: int
    correspondencias_semanticas: int
    ambiguidades: int
    conceitos_distintos: int


@dataclass
class ResultadoMapaSemantico:
    arquivo_regras: str
    pasta_selecao: str
    pasta_hierarquia: str
    pasta_saida: str
    versao_catalogo: str
    blocos: list[ResultadoMapaSemanticoBloco]
    total_registros_selecionados: int
    total_registros_mapeados: int
    total_registros_nao_mapeados: int
    total_correspondencias_semanticas: int
    total_ambiguidades: int
    arquivo_mapa_parquet: str
    arquivo_mapa_xlsx: str
    arquivo_registros_parquet: str
    arquivo_pendencias_xlsx: str
    arquivo_resultado_json: str
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _normalizar_texto(valor: object) -> str:
    if pd.isna(valor):
        return ""
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def _contem_termo(texto: str, termo: str) -> bool:
    termo_normalizado = _normalizar_texto(termo)
    if not termo_normalizado:
        return False
    if " " not in termo_normalizado:
        return re.search(rf"\b{re.escape(termo_normalizado)}\b", texto) is not None
    return termo_normalizado in texto


def _lista(valor: object) -> list[str]:
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(item) for item in valor]
    return [str(valor)]


def _carregar_regras(caminho: Path) -> tuple[str, list[dict[str, Any]]]:
    if not caminho.exists():
        raise FileNotFoundError(caminho)
    conteudo = yaml.safe_load(caminho.read_text(encoding="utf-8")) or {}
    regras = conteudo.get("regras", [])
    if not isinstance(regras, list) or not regras:
        raise ValueError("O catalogo semantico nao possui regras validas.")
    obrigatorios = {"id_semantico", "grupo_semantico", "bloco"}
    for indice, regra in enumerate(regras, start=1):
        faltantes = obrigatorios.difference(regra)
        if faltantes:
            raise ValueError(f"Regra {indice} sem campos obrigatorios: {sorted(faltantes)}")
    return str(conteudo.get("versao", "nao_informada")), regras


def _regra_corresponde(linha: pd.Series, regra: dict[str, Any]) -> bool:
    if str(linha["bloco"]) != str(regra["bloco"]):
        return False

    ano = int(linha["ano"])
    if regra.get("ano_inicial") is not None and ano < int(regra["ano_inicial"]):
        return False
    if regra.get("ano_final") is not None and ano > int(regra["ano_final"]):
        return False

    codigo = str(linha.get("codigo_conta", ""))
    padrao_codigo = regra.get("codigo_regex")
    if padrao_codigo and re.search(str(padrao_codigo), codigo) is None:
        return False

    descricao = _normalizar_texto(linha.get("descricao_conta", ""))
    contem_algum = _lista(regra.get("descricao_contem_algum"))
    contem_todos = _lista(regra.get("descricao_contem_todos"))
    nao_contem = _lista(regra.get("descricao_nao_contem"))

    if contem_algum and not any(_contem_termo(descricao, termo) for termo in contem_algum):
        return False
    if contem_todos and not all(_contem_termo(descricao, termo) for termo in contem_todos):
        return False
    if nao_contem and any(_contem_termo(descricao, termo) for termo in nao_contem):
        return False
    return True


def _escolher_regras(linha: pd.Series, regras: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], bool]:
    candidatas = [regra for regra in regras if _regra_corresponde(linha, regra)]
    if not candidatas:
        return [], False

    escolhidas: list[dict[str, Any]] = []
    ambigua = False
    por_grupo: dict[str, list[dict[str, Any]]] = {}
    for regra in candidatas:
        por_grupo.setdefault(str(regra["grupo_semantico"]), []).append(regra)

    for regras_grupo in por_grupo.values():
        maior_prioridade = max(int(regra.get("prioridade", 0)) for regra in regras_grupo)
        melhores = [
            regra for regra in regras_grupo if int(regra.get("prioridade", 0)) == maior_prioridade
        ]
        escolhidas.extend(melhores)
        if len(melhores) > 1:
            ambigua = True
    return escolhidas, ambigua


def construir_mapa_semantico(
    pasta_selecao: Path,
    pasta_hierarquia: Path,
    arquivo_regras: Path,
    pasta_saida: Path,
) -> ResultadoMapaSemantico:
    """Aplica o catalogo semantico aos registros selecionados por recorte."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    versao_catalogo, regras = _carregar_regras(arquivo_regras)

    selecao = pd.read_parquet(pasta_selecao / "selecao_agregacao_hierarquica.parquet")
    selecao = selecao[selecao["selecionado_para_agregacao"]].copy()
    catalogo = pd.read_parquet(pasta_hierarquia / "catalogo_contabil.parquet")
    descricoes = catalogo[catalogo["codigo_observado"]][
        ["bloco", "codigo_conta", "descricao_conta", "origem_no"]
    ].drop_duplicates(["bloco", "codigo_conta"])
    base = selecao.merge(descricoes, on=["bloco", "codigo_conta"], how="left")

    linhas: list[dict[str, Any]] = []
    for identificador, linha in base.reset_index(drop=True).iterrows():
        escolhidas, ambigua = _escolher_regras(linha, regras)
        dados_base = linha.to_dict()
        dados_base["id_registro_semantico"] = int(identificador)
        if not escolhidas:
            linhas.append(
                {
                    **dados_base,
                    "id_semantico": pd.NA,
                    "grupo_semantico": pd.NA,
                    "confianca_mapeamento": pd.NA,
                    "interpretacao": pd.NA,
                    "prioridade_regra": pd.NA,
                    "status_mapeamento": "nao_mapeado",
                    "ambiguidade": False,
                }
            )
            continue
        for regra in escolhidas:
            linhas.append(
                {
                    **dados_base,
                    "id_semantico": regra["id_semantico"],
                    "grupo_semantico": regra["grupo_semantico"],
                    "confianca_mapeamento": regra.get("confianca", "nao_informada"),
                    "interpretacao": regra.get("interpretacao", ""),
                    "prioridade_regra": int(regra.get("prioridade", 0)),
                    "status_mapeamento": "ambiguo" if ambigua else "mapeado",
                    "ambiguidade": ambigua,
                }
            )

    registros = pd.DataFrame(linhas)
    mapa = registros[registros["id_semantico"].notna()][
        [
            "bloco",
            "ano",
            "codigo_conta",
            "descricao_conta",
            "id_semantico",
            "grupo_semantico",
            "confianca_mapeamento",
            "interpretacao",
            "prioridade_regra",
            "status_mapeamento",
        ]
    ].drop_duplicates()

    pendencias = (
        registros[registros["status_mapeamento"].isin(["nao_mapeado", "ambiguo"])]
        .groupby(
            ["bloco", "ano", "codigo_conta", "descricao_conta", "status_mapeamento"],
            dropna=False,
        )
        .agg(
            registros=("id_registro_semantico", "nunique"),
            municipios=("codigo_ibge", "nunique"),
            valor_absoluto=("valor_recorte", lambda serie: float(serie.abs().sum())),
        )
        .reset_index()
        .sort_values(["status_mapeamento", "valor_absoluto"], ascending=[True, False])
    )

    arquivo_mapa_parquet = pasta_saida / "mapa_semantico_codigos.parquet"
    arquivo_mapa_xlsx = pasta_saida / "mapa_semantico_codigos.xlsx"
    arquivo_registros = pasta_saida / "registros_selecionados_semanticos.parquet"
    arquivo_pendencias = pasta_saida / "pendencias_mapa_semantico.xlsx"
    arquivo_resultado = pasta_saida / "resultado_mapa_semantico.json"

    mapa.to_parquet(arquivo_mapa_parquet, index=False)
    registros.to_parquet(arquivo_registros, index=False)
    with pd.ExcelWriter(arquivo_mapa_xlsx, engine="openpyxl") as escritor:
        mapa.to_excel(escritor, sheet_name="Mapa semantico", index=False)
        pd.DataFrame(regras).to_excel(escritor, sheet_name="Regras", index=False)
    with pd.ExcelWriter(arquivo_pendencias, engine="openpyxl") as escritor:
        pendencias.to_excel(escritor, sheet_name="Pendencias", index=False)

    resumos: list[ResultadoMapaSemanticoBloco] = []
    for bloco, quadro in registros.groupby("bloco", dropna=False):
        ids = quadro["id_registro_semantico"].nunique()
        mapeados = quadro[quadro["id_semantico"].notna()]["id_registro_semantico"].nunique()
        resumos.append(
            ResultadoMapaSemanticoBloco(
                bloco=str(bloco),
                registros_selecionados=int(ids),
                registros_mapeados=int(mapeados),
                registros_nao_mapeados=int(ids - mapeados),
                correspondencias_semanticas=int(quadro["id_semantico"].notna().sum()),
                ambiguidades=int(quadro[quadro["ambiguidade"]]["id_registro_semantico"].nunique()),
                conceitos_distintos=int(quadro["id_semantico"].nunique()),
            )
        )

    total_selecionados = int(base.shape[0])
    total_mapeados = int(registros[registros["id_semantico"].notna()]["id_registro_semantico"].nunique())
    total_ambiguidades = int(registros[registros["ambiguidade"]]["id_registro_semantico"].nunique())
    status = "aprovado"
    if total_selecionados == 0:
        status = "reprovado"
    elif total_ambiguidades > 0:
        status = "aprovado_com_alertas"

    resultado = ResultadoMapaSemantico(
        arquivo_regras=str(arquivo_regras),
        pasta_selecao=str(pasta_selecao),
        pasta_hierarquia=str(pasta_hierarquia),
        pasta_saida=str(pasta_saida),
        versao_catalogo=versao_catalogo,
        blocos=resumos,
        total_registros_selecionados=total_selecionados,
        total_registros_mapeados=total_mapeados,
        total_registros_nao_mapeados=total_selecionados - total_mapeados,
        total_correspondencias_semanticas=int(registros["id_semantico"].notna().sum()),
        total_ambiguidades=total_ambiguidades,
        arquivo_mapa_parquet=str(arquivo_mapa_parquet),
        arquivo_mapa_xlsx=str(arquivo_mapa_xlsx),
        arquivo_registros_parquet=str(arquivo_registros),
        arquivo_pendencias_xlsx=str(arquivo_pendencias),
        arquivo_resultado_json=str(arquivo_resultado),
        status=status,
    )
    pd.Series(resultado.como_dicionario()).to_json(arquivo_resultado, force_ascii=False, indent=2)
    return resultado
