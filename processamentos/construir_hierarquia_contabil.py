"""Construcao auditavel da hierarquia e do catalogo contabil."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ARQUIVOS_QUALIFICADOS = {
    "receitas": "receitas_qualificado.parquet",
    "despesas": "despesas_qualificado.parquet",
    "despesa_por_funcao": "despesa_por_funcao_qualificado.parquet",
}


@dataclass
class ResultadoHierarquiaBloco:
    bloco: str
    registros: int
    codigos_distintos: int
    contas_terminais: int
    contas_sinteticas: int
    codigos_sem_pai_identificado: int
    maior_nivel: int


@dataclass
class ResultadoHierarquia:
    pasta_origem: str
    pasta_saida: str
    blocos: list[ResultadoHierarquiaBloco]
    total_codigos_distintos: int
    total_relacoes_pai_filho: int
    arquivo_catalogo_parquet: str
    arquivo_catalogo_xlsx: str
    arquivo_relacoes_parquet: str
    arquivo_resultado_json: str
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _codigo_ausente(valor: object) -> bool:
    return pd.isna(valor) or str(valor).strip() == ""


def _segmentos_codigo(codigo: object) -> list[str]:
    if _codigo_ausente(codigo):
        return []
    return [segmento.strip() for segmento in str(codigo).split(".") if segmento.strip()]


def _codigo_pai(codigo: object) -> str | None:
    segmentos = _segmentos_codigo(codigo)
    if len(segmentos) <= 1:
        return None
    return ".".join(segmentos[:-1])


def _nivel_hierarquico(codigo: object) -> int:
    return len(_segmentos_codigo(codigo))


def _primeiro_valido(serie: pd.Series) -> object:
    validos = serie.dropna()
    if validos.empty:
        return pd.NA
    textos = validos.astype("string").str.strip()
    textos = textos[textos.ne("")]
    return textos.iloc[0] if not textos.empty else pd.NA


def _construir_catalogo_bloco(quadro: pd.DataFrame, bloco: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    codificados = quadro[~quadro["codigo_conta"].apply(_codigo_ausente)].copy()
    if codificados.empty:
        return pd.DataFrame(), pd.DataFrame()

    codificados["codigo_conta"] = codificados["codigo_conta"].astype("string").str.strip()
    codificados["nivel_hierarquico"] = codificados["codigo_conta"].map(_nivel_hierarquico)
    codificados["codigo_pai"] = codificados["codigo_conta"].map(_codigo_pai).astype("string")

    agrupadores = ["bloco", "codigo_conta"]
    catalogo = (
        codificados.groupby(agrupadores, dropna=False)
        .agg(
            descricao_conta=("descricao_conta", _primeiro_valido),
            tipo_registro=("tipo_registro", _primeiro_valido),
            natureza_operacao=("natureza_operacao", _primeiro_valido),
            codigo_funcao=("codigo_funcao", _primeiro_valido),
            codigo_subfuncao=("codigo_subfuncao", _primeiro_valido),
            nivel_hierarquico=("nivel_hierarquico", "max"),
            codigo_pai=("codigo_pai", _primeiro_valido),
            primeira_ocorrencia=("ano", "min"),
            ultima_ocorrencia=("ano", "max"),
            anos_validos=("ano", "nunique"),
            municipios=("codigo_ibge", "nunique"),
            registros=("valor", "size"),
            valor_nominal_acumulado=("valor", "sum"),
            valor_absoluto_acumulado=("valor", lambda s: float(s.abs().sum())),
        )
        .reset_index()
    )

    codigos = set(catalogo["codigo_conta"].astype(str))
    catalogo["pai_presente_no_catalogo"] = catalogo["codigo_pai"].map(
        lambda pai: False if pd.isna(pai) else str(pai) in codigos
    )
    catalogo["possui_filhos"] = catalogo["codigo_conta"].map(
        lambda codigo: any(str(pai) == str(codigo) for pai in catalogo["codigo_pai"].dropna())
    )
    catalogo["conta_terminal_calculada"] = ~catalogo["possui_filhos"]
    catalogo["classificacao_hierarquica"] = catalogo.apply(
        lambda linha: "terminal" if linha["conta_terminal_calculada"] else "sintetica", axis=1
    )

    relacoes = catalogo.loc[
        catalogo["codigo_pai"].notna(),
        ["bloco", "codigo_pai", "codigo_conta", "nivel_hierarquico"],
    ].rename(columns={"codigo_conta": "codigo_filho"})
    relacoes["pai_presente_no_catalogo"] = relacoes["codigo_pai"].astype(str).isin(codigos)
    return catalogo, relacoes


def construir_hierarquia_contabil(pasta_qualificacao: Path, pasta_saida: Path) -> ResultadoHierarquia:
    """Constroi catalogo mestre e relacoes pai-filho a partir dos arquivos qualificados."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    catalogos: list[pd.DataFrame] = []
    relacoes: list[pd.DataFrame] = []
    resultados: list[ResultadoHierarquiaBloco] = []

    for bloco, nome_arquivo in ARQUIVOS_QUALIFICADOS.items():
        entrada = pasta_qualificacao / nome_arquivo
        if not entrada.exists():
            raise FileNotFoundError(entrada)
        quadro = pd.read_parquet(entrada)
        catalogo, relacao = _construir_catalogo_bloco(quadro, bloco)
        catalogos.append(catalogo)
        relacoes.append(relacao)

        sem_pai = 0
        maior_nivel = 0
        terminais = 0
        sinteticas = 0
        if not catalogo.empty:
            sem_pai = int(
                (catalogo["codigo_pai"].notna() & ~catalogo["pai_presente_no_catalogo"]).sum()
            )
            maior_nivel = int(catalogo["nivel_hierarquico"].max())
            terminais = int(catalogo["conta_terminal_calculada"].sum())
            sinteticas = int((~catalogo["conta_terminal_calculada"]).sum())
        resultados.append(
            ResultadoHierarquiaBloco(
                bloco=bloco,
                registros=int(len(quadro)),
                codigos_distintos=int(len(catalogo)),
                contas_terminais=terminais,
                contas_sinteticas=sinteticas,
                codigos_sem_pai_identificado=sem_pai,
                maior_nivel=maior_nivel,
            )
        )

    catalogo_final = pd.concat(catalogos, ignore_index=True) if catalogos else pd.DataFrame()
    relacoes_final = pd.concat(relacoes, ignore_index=True) if relacoes else pd.DataFrame()

    arquivo_catalogo_parquet = pasta_saida / "catalogo_contabil.parquet"
    arquivo_catalogo_xlsx = pasta_saida / "catalogo_contabil.xlsx"
    arquivo_relacoes = pasta_saida / "relacoes_pai_filho.parquet"
    arquivo_resultado = pasta_saida / "resultado_hierarquia.json"

    catalogo_final.to_parquet(arquivo_catalogo_parquet, index=False)
    relacoes_final.to_parquet(arquivo_relacoes, index=False)
    with pd.ExcelWriter(arquivo_catalogo_xlsx, engine="openpyxl") as escritor:
        catalogo_final.to_excel(escritor, sheet_name="Catalogo", index=False)
        relacoes_final.to_excel(escritor, sheet_name="Relacoes", index=False)
        pd.DataFrame([asdict(item) for item in resultados]).to_excel(
            escritor, sheet_name="Resumo", index=False
        )

    total_codigos = sum(item.codigos_distintos for item in resultados)
    total_relacoes = int(len(relacoes_final))
    status = "aprovado" if total_codigos > 0 else "reprovado"
    resultado = ResultadoHierarquia(
        pasta_origem=str(pasta_qualificacao),
        pasta_saida=str(pasta_saida),
        blocos=resultados,
        total_codigos_distintos=total_codigos,
        total_relacoes_pai_filho=total_relacoes,
        arquivo_catalogo_parquet=str(arquivo_catalogo_parquet),
        arquivo_catalogo_xlsx=str(arquivo_catalogo_xlsx),
        arquivo_relacoes_parquet=str(arquivo_relacoes),
        arquivo_resultado_json=str(arquivo_resultado),
        status=status,
    )
    pd.Series(resultado.como_dicionario()).to_json(
        arquivo_resultado, force_ascii=False, indent=2
    )
    return resultado
