"""Construcao auditavel da hierarquia e do catalogo contabil.

A hierarquia e especifica para cada bloco:
- receita: estrutura posicional, com ascensao por substituicao por zeros;
- despesa por natureza: prefixos conceituais de categoria, grupo, modalidade,
  elemento e desdobramento;
- despesa por funcao: funcao e funcao.subfuncao.

Nos conceituais ausentes da declaracao sao gerados sem alterar os registros de origem.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

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
    codigos_observados: int
    nos_conceituais_gerados: int
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
    total_codigos_observados: int
    total_nos_conceituais_gerados: int
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


def _segmento_zero(segmento: str) -> str:
    return "0" * max(1, len(segmento))


def _eh_zero(segmento: str) -> bool:
    return bool(segmento) and set(segmento) == {"0"}


def _cadeia_receita(codigo: str) -> list[str]:
    """Retorna a cadeia da raiz ate o codigo preservando larguras historicas."""
    segmentos = _segmentos_codigo(codigo)
    if not segmentos:
        return []

    cadeia: list[str] = []
    for posicao in range(len(segmentos)):
        atual = [
            segmentos[i] if i <= posicao else _segmento_zero(segmentos[i])
            for i in range(len(segmentos))
        ]
        candidato = ".".join(atual)
        if candidato not in cadeia:
            cadeia.append(candidato)

    # Segmentos intermediarios iguais a zero nao criam novos niveis substantivos.
    cadeia_filtrada: list[str] = []
    for item in cadeia:
        partes = _segmentos_codigo(item)
        ultimo_nao_zero = max((i for i, p in enumerate(partes) if not _eh_zero(p)), default=0)
        canonico = ".".join(
            partes[i] if i <= ultimo_nao_zero else _segmento_zero(partes[i])
            for i in range(len(partes))
        )
        if canonico not in cadeia_filtrada:
            cadeia_filtrada.append(canonico)
    return cadeia_filtrada


def _cadeia_despesa(codigo: str) -> list[str]:
    segmentos = _segmentos_codigo(codigo)
    return [".".join(segmentos[:i]) for i in range(1, len(segmentos) + 1)]


def _cadeia_funcional(codigo: str) -> list[str]:
    segmentos = _segmentos_codigo(codigo)
    if not segmentos:
        return []
    if len(segmentos) == 1:
        return [segmentos[0].zfill(2)]
    # A classificacao funcional operacional e funcao -> funcao.subfuncao.
    return [segmentos[0].zfill(2), f"{segmentos[0].zfill(2)}.{segmentos[1].zfill(3)}"]


def _cadeia_codigo(codigo: str, bloco: str) -> list[str]:
    if bloco == "receitas":
        return _cadeia_receita(codigo)
    if bloco == "despesas":
        return _cadeia_despesa(codigo)
    return _cadeia_funcional(codigo)


def _nivel_hierarquico(codigo: str, bloco: str) -> int:
    cadeia = _cadeia_codigo(codigo, bloco)
    return len(cadeia)


def _primeiro_valido(serie: pd.Series) -> object:
    validos = serie.dropna()
    if validos.empty:
        return pd.NA
    textos = validos.astype("string").str.strip()
    textos = textos[textos.ne("")]
    return textos.iloc[0] if not textos.empty else pd.NA


def _pares_cadeia(cadeia: Iterable[str]) -> list[tuple[str, str]]:
    itens = list(cadeia)
    return [(itens[i - 1], itens[i]) for i in range(1, len(itens))]


def _construir_nos_e_relacoes(codigos: Iterable[str], bloco: str) -> tuple[set[str], set[tuple[str, str]]]:
    nos: set[str] = set()
    relacoes: set[tuple[str, str]] = set()
    for codigo in codigos:
        cadeia = _cadeia_codigo(codigo, bloco)
        nos.update(cadeia)
        relacoes.update(_pares_cadeia(cadeia))
    return nos, relacoes


def _construir_catalogo_observado(codificados: pd.DataFrame, bloco: str) -> pd.DataFrame:
    quadro = codificados.copy()
    quadro["codigo_conta"] = quadro["codigo_conta"].astype("string").str.strip()
    agrupadores = ["bloco", "codigo_conta"]
    catalogo = (
        quadro.groupby(agrupadores, dropna=False)
        .agg(
            descricao_conta=("descricao_conta", _primeiro_valido),
            tipo_registro=("tipo_registro", _primeiro_valido),
            natureza_operacao=("natureza_operacao", _primeiro_valido),
            codigo_funcao=("codigo_funcao", _primeiro_valido),
            codigo_subfuncao=("codigo_subfuncao", _primeiro_valido),
            primeira_ocorrencia=("ano", "min"),
            ultima_ocorrencia=("ano", "max"),
            anos_validos=("ano", "nunique"),
            municipios=("codigo_ibge", "nunique"),
            registros=("valor", "size"),
            soma_nominal_registros_observados=("valor", "sum"),
            soma_absoluta_para_auditoria=("valor", lambda s: float(s.abs().sum())),
        )
        .reset_index()
    )
    catalogo["origem_no"] = "observado"
    catalogo["codigo_observado"] = True
    catalogo["nivel_hierarquico"] = catalogo["codigo_conta"].map(
        lambda c: _nivel_hierarquico(str(c), bloco)
    )
    return catalogo


def _adicionar_nos_conceituais(
    catalogo_observado: pd.DataFrame, nos: set[str], bloco: str
) -> pd.DataFrame:
    observados = set(catalogo_observado["codigo_conta"].astype(str))
    faltantes = sorted(nos - observados)
    if not faltantes:
        return catalogo_observado

    conceituais = pd.DataFrame(
        {
            "bloco": bloco,
            "codigo_conta": faltantes,
            "descricao_conta": pd.NA,
            "tipo_registro": "no_conceitual",
            "natureza_operacao": pd.NA,
            "codigo_funcao": pd.NA,
            "codigo_subfuncao": pd.NA,
            "primeira_ocorrencia": pd.NA,
            "ultima_ocorrencia": pd.NA,
            "anos_validos": 0,
            "municipios": 0,
            "registros": 0,
            "soma_nominal_registros_observados": 0.0,
            "soma_absoluta_para_auditoria": 0.0,
            "origem_no": "conceitual_gerado",
            "codigo_observado": False,
            "nivel_hierarquico": [
                _nivel_hierarquico(codigo, bloco) for codigo in faltantes
            ],
        }
    )
    return pd.concat([catalogo_observado, conceituais], ignore_index=True)


def _construir_catalogo_bloco(quadro: pd.DataFrame, bloco: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    codificados = quadro[~quadro["codigo_conta"].apply(_codigo_ausente)].copy()
    if codificados.empty:
        return pd.DataFrame(), pd.DataFrame()

    observados = codificados["codigo_conta"].astype("string").str.strip().dropna().astype(str)
    nos, pares = _construir_nos_e_relacoes(observados, bloco)
    catalogo = _construir_catalogo_observado(codificados, bloco)
    catalogo = _adicionar_nos_conceituais(catalogo, nos, bloco)

    relacoes = pd.DataFrame(
        sorted(pares), columns=["codigo_pai", "codigo_filho"]
    )
    relacoes.insert(0, "bloco", bloco)
    if relacoes.empty:
        relacoes = pd.DataFrame(
            columns=["bloco", "codigo_pai", "codigo_filho", "nivel_hierarquico_filho"]
        )
    else:
        relacoes["nivel_hierarquico_filho"] = relacoes["codigo_filho"].map(
            lambda c: _nivel_hierarquico(c, bloco)
        )

    mapa_pai = dict(zip(relacoes["codigo_filho"], relacoes["codigo_pai"]))
    filhos = set(relacoes["codigo_pai"].astype(str))
    catalogo["codigo_pai"] = catalogo["codigo_conta"].map(mapa_pai).astype("string")
    codigos_catalogo = set(catalogo["codigo_conta"].astype(str))
    catalogo["pai_presente_no_catalogo"] = catalogo["codigo_pai"].map(
        lambda pai: False if pd.isna(pai) else str(pai) in codigos_catalogo
    )
    catalogo["possui_filhos"] = catalogo["codigo_conta"].astype(str).isin(filhos)
    catalogo["conta_terminal_calculada"] = ~catalogo["possui_filhos"]
    catalogo["classificacao_hierarquica"] = catalogo["possui_filhos"].map(
        {True: "sintetica", False: "terminal"}
    )
    catalogo["utilizavel_em_agregacao"] = catalogo["codigo_observado"] & catalogo[
        "conta_terminal_calculada"
    ]
    catalogo["regra_hierarquia"] = {
        "receitas": "posicional_com_zeros",
        "despesas": "prefixos_natureza_despesa",
        "despesa_por_funcao": "funcao_subfuncao",
    }[bloco]

    relacoes["pai_presente_no_catalogo"] = relacoes["codigo_pai"].isin(codigos_catalogo)
    relacoes["filho_observado"] = relacoes["codigo_filho"].isin(set(observados))
    return catalogo.sort_values(["nivel_hierarquico", "codigo_conta"]), relacoes


def construir_hierarquia_contabil(pasta_qualificacao: Path, pasta_saida: Path) -> ResultadoHierarquia:
    """Constroi catalogo mestre e relacoes pai-filho por regra especifica de bloco."""
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

        observados = int(catalogo["codigo_observado"].sum()) if not catalogo.empty else 0
        gerados = int((~catalogo["codigo_observado"]).sum()) if not catalogo.empty else 0
        sem_pai = int(
            (
                catalogo["codigo_pai"].notna()
                & ~catalogo["pai_presente_no_catalogo"]
            ).sum()
        ) if not catalogo.empty else 0
        resultados.append(
            ResultadoHierarquiaBloco(
                bloco=bloco,
                registros=int(len(quadro)),
                codigos_observados=observados,
                nos_conceituais_gerados=gerados,
                codigos_distintos=int(len(catalogo)),
                contas_terminais=int(catalogo["conta_terminal_calculada"].sum()) if not catalogo.empty else 0,
                contas_sinteticas=int(catalogo["possui_filhos"].sum()) if not catalogo.empty else 0,
                codigos_sem_pai_identificado=sem_pai,
                maior_nivel=int(catalogo["nivel_hierarquico"].max()) if not catalogo.empty else 0,
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
    total_observados = sum(item.codigos_observados for item in resultados)
    total_gerados = sum(item.nos_conceituais_gerados for item in resultados)
    total_relacoes = int(len(relacoes_final))
    total_orfaos = sum(item.codigos_sem_pai_identificado for item in resultados)
    status = "aprovado" if total_codigos > 0 and total_orfaos == 0 else "aprovado_com_alertas"
    if total_codigos == 0:
        status = "reprovado"

    resultado = ResultadoHierarquia(
        pasta_origem=str(pasta_qualificacao),
        pasta_saida=str(pasta_saida),
        blocos=resultados,
        total_codigos_distintos=total_codigos,
        total_codigos_observados=total_observados,
        total_nos_conceituais_gerados=total_gerados,
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
