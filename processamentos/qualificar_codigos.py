"""Qualificacao auditavel de codigos, totais e classificacao funcional."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
import unicodedata
from typing import Any

import pandas as pd

ARQUIVOS_BLOCOS = {
    "receitas": "receitas_longo.parquet",
    "despesas": "despesas_longo.parquet",
    "despesa_por_funcao": "despesa_por_funcao_longo.parquet",
}

TERMOS_TOTAL = (
    "total",
    "subtotal",
    "receitas correntes",
    "receitas de capital",
    "despesas correntes",
    "despesas de capital",
    "receitas intraorcamentarias",
    "receitas exceto intraorcamentarias",
    "despesas intraorcamentarias",
    "despesas exceto intraorcamentarias",
)

TERMOS_DEDUCAO = (
    "deducao",
    "deducoes",
    "restituicao",
    "restituicoes",
    "retificacao",
    "retificacoes",
    "fundeb",
)

PADRAO_CODIGO_RECEITA = re.compile(
    r"^\s*(\d(?:\.\d{1,2}){2,7})\s*(?:[-–:]\s*)?(.+)?$"
)
PADRAO_CODIGO_DESPESA = re.compile(
    r"^\s*([1-9](?:\.\d{1,2}){1,5})\s*(?:[-–:]\s*)?(.+)?$"
)
PADRAO_FUNCAO_SUBFUNCAO = re.compile(r"(?<!\d)(\d{2})\.(\d{3})(?!\d)")
PADRAO_FUNCAO_FU = re.compile(r"\bFU\s*0?(\d{1,2})\b", flags=re.IGNORECASE)
PADRAO_FUNCAO_ISOLADA = re.compile(r"^\s*0?(\d{1,2})\s*(?:[-–:]\s*)?(.+)?$")


@dataclass
class ResultadoQualificacaoBloco:
    bloco: str
    arquivo_entrada: str
    arquivo_saida: str
    registros: int
    cabecalhos_distintos: int
    registros_com_codigo: int
    registros_sem_codigo_justificado: int
    registros_pendentes: int
    cabecalhos_pendentes: int
    registros_com_funcao: int
    registros_com_subfuncao: int
    funcoes_distintas: int
    subfuncoes_distintas: int
    agregados_funcionais_residuais: int
    registros_intraorcamentarios: int
    registros_deducao_receita: int


@dataclass
class ResultadoQualificacao:
    pasta_origem: str
    pasta_saida: str
    blocos: list[ResultadoQualificacaoBloco]
    total_registros: int
    total_registros_pendentes: int
    total_cabecalhos_pendentes: int
    arquivo_pendencias_parquet: str
    arquivo_pendencias_xlsx: str
    status: str

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _sem_acentos(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor))
    return "".join(c for c in texto if not unicodedata.combining(c)).lower().strip()


def _texto_linha(linha: pd.Series) -> str:
    partes = [linha.get("rotulo_conta_original"), linha.get("descricao_conta")]
    return " | ".join(str(p) for p in partes if pd.notna(p))


def _codigo_ausente(valor: object) -> bool:
    return pd.isna(valor) or str(valor).strip() == ""


def _extrair_codigo_do_texto(texto: object, bloco: str) -> tuple[str | None, str | None]:
    if pd.isna(texto):
        return None, None
    valor = str(texto).strip()
    padrao = PADRAO_CODIGO_RECEITA if bloco == "receitas" else PADRAO_CODIGO_DESPESA
    correspondencia = padrao.match(valor)
    if not correspondencia:
        return None, None
    codigo = correspondencia.group(1)
    descricao = correspondencia.group(2)
    return codigo, descricao.strip() if descricao else None


def _preencher_codigo_conta(resultado: pd.DataFrame, bloco: str) -> pd.DataFrame:
    quadro = resultado.copy()
    for indice, linha in quadro.iterrows():
        if not _codigo_ausente(linha.get("codigo_conta")):
            continue
        candidatos = [linha.get("descricao_conta"), linha.get("rotulo_conta_original")]
        for candidato in candidatos:
            codigo, descricao = _extrair_codigo_do_texto(candidato, bloco)
            if codigo:
                quadro.at[indice, "codigo_conta"] = codigo
                if descricao and (
                    pd.isna(linha.get("descricao_conta"))
                    or str(linha.get("descricao_conta")).strip() in {"", str(candidato).strip()}
                ):
                    quadro.at[indice, "descricao_conta"] = descricao
                quadro.at[indice, "origem_codigo_qualificado"] = "extraido_do_texto"
                break
    return quadro


def _classificar_tipo_registro(linha: pd.Series) -> str:
    texto = _sem_acentos(_texto_linha(linha))
    codigo = linha.get("codigo_conta")
    if "demais subfuncoes" in texto:
        return "agregado_funcional_residual"
    if any(termo in texto for termo in TERMOS_TOTAL):
        return "total_ou_subtotal"
    if _codigo_ausente(codigo):
        if "indicador" in texto or "percentual" in texto:
            return "indicador_auxiliar"
        return "nao_classificado"
    segmentos = [s for s in re.split(r"[.\-]", str(codigo)) if s]
    return "conta_terminal" if len(segmentos) >= 4 else "conta_sintetica"


def _extrair_funcao_subfuncao(linha: pd.Series) -> tuple[str | None, str | None]:
    codigo = "" if _codigo_ausente(linha.get("codigo_conta")) else str(linha.get("codigo_conta"))
    texto = f"{codigo} {_texto_linha(linha)}"
    correspondencia = PADRAO_FUNCAO_SUBFUNCAO.search(texto)
    if correspondencia:
        return correspondencia.group(1), correspondencia.group(2)
    correspondencia_fu = PADRAO_FUNCAO_FU.search(texto)
    if correspondencia_fu:
        return correspondencia_fu.group(1).zfill(2), None
    correspondencia_funcao = PADRAO_FUNCAO_ISOLADA.match(codigo or str(linha.get("descricao_conta", "")))
    if correspondencia_funcao:
        return correspondencia_funcao.group(1).zfill(2), None
    return None, None


def _classificar_natureza_operacao(linha: pd.Series, bloco: str) -> str:
    texto = _sem_acentos(_texto_linha(linha))
    codigo = "" if _codigo_ausente(linha.get("codigo_conta")) else str(linha.get("codigo_conta"))
    if "intraorcament" in texto:
        return "intraorcamentaria"
    if bloco == "receitas" and codigo[:1] in {"7", "8"}:
        return "intraorcamentaria"
    if bloco == "despesas":
        segmentos = codigo.split(".")
        if len(segmentos) >= 3 and segmentos[2].zfill(2) == "91":
            return "intraorcamentaria"
    return "orcamentaria"


def _classificar_deducao_receita(linha: pd.Series, bloco: str) -> bool:
    if bloco != "receitas":
        return False
    texto = _sem_acentos(_texto_linha(linha))
    return any(termo in texto for termo in TERMOS_DEDUCAO)


def _motivo_pendencia(linha: pd.Series) -> str | None:
    codigo = linha.get("codigo_conta")
    if not _codigo_ausente(codigo):
        return None
    tipo = linha.get("tipo_registro")
    if tipo in {
        "total_ou_subtotal",
        "indicador_auxiliar",
        "agregado_funcional_residual",
    }:
        return "ausencia_justificada_por_tipo"
    origem = linha.get("origem_metadados")
    if origem == "regra_contingencia":
        return "cabecalho_sem_correspondencia_no_dicionario"
    texto = _texto_linha(linha)
    if not texto.strip():
        return "campo_vazio"
    if re.match(r"^\s*\d", texto):
        return "formato_de_codigo_nao_reconhecido"
    return "codigo_ausente_no_dicionario"


def _qualificar_quadro(quadro: pd.DataFrame, bloco: str) -> pd.DataFrame:
    resultado = quadro.copy()
    if "origem_codigo_qualificado" not in resultado.columns:
        resultado["origem_codigo_qualificado"] = pd.NA
    resultado = _preencher_codigo_conta(resultado, bloco)
    resultado["tipo_registro"] = resultado.apply(_classificar_tipo_registro, axis=1)
    resultado["natureza_operacao"] = resultado.apply(
        lambda linha: _classificar_natureza_operacao(linha, bloco), axis=1
    )
    resultado["deducao_receita"] = resultado.apply(
        lambda linha: _classificar_deducao_receita(linha, bloco), axis=1
    )
    resultado["codigo_funcao"] = pd.NA
    resultado["codigo_subfuncao"] = pd.NA
    if bloco == "despesa_por_funcao":
        codigos = resultado.apply(_extrair_funcao_subfuncao, axis=1)
        resultado["codigo_funcao"] = codigos.map(lambda item: item[0]).astype("string")
        resultado["codigo_subfuncao"] = codigos.map(lambda item: item[1]).astype("string")
    resultado["motivo_ausencia_codigo"] = resultado.apply(_motivo_pendencia, axis=1)
    resultado["pendencia_revisao"] = resultado["motivo_ausencia_codigo"].notna() & ~resultado[
        "motivo_ausencia_codigo"
    ].eq("ausencia_justificada_por_tipo")
    return resultado


def _resumir_pendencias(quadro: pd.DataFrame, bloco: str) -> pd.DataFrame:
    pendentes = quadro[quadro["pendencia_revisao"]].copy()
    colunas = [
        "bloco",
        "rotulo_conta_original",
        "estagio",
        "descricao_conta",
        "origem_metadados",
        "motivo_ausencia_codigo",
        "quantidade_registros",
        "anos",
        "municipios",
        "valor_absoluto_acumulado",
    ]
    if pendentes.empty:
        return pd.DataFrame(columns=colunas)
    resumo = (
        pendentes.groupby(
            [
                "rotulo_conta_original",
                "estagio",
                "descricao_conta",
                "origem_metadados",
                "motivo_ausencia_codigo",
            ],
            dropna=False,
        )
        .agg(
            quantidade_registros=("valor", "size"),
            anos=("ano", lambda s: ", ".join(map(str, sorted(set(int(v) for v in s.dropna()))))),
            municipios=("codigo_ibge", "nunique"),
            valor_absoluto_acumulado=("valor", lambda s: float(s.abs().sum())),
        )
        .reset_index()
    )
    resumo.insert(0, "bloco", bloco)
    return resumo.sort_values(
        ["valor_absoluto_acumulado", "quantidade_registros"], ascending=False
    )


def qualificar_codigos(pasta_normalizacao: Path, pasta_saida: Path) -> ResultadoQualificacao:
    """Qualifica os Parquet normalizados e produz uma fila auditavel de revisao."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    resultados: list[ResultadoQualificacaoBloco] = []
    pendencias: list[pd.DataFrame] = []

    for bloco, nome_arquivo in ARQUIVOS_BLOCOS.items():
        entrada = pasta_normalizacao / nome_arquivo
        if not entrada.exists():
            raise FileNotFoundError(entrada)
        quadro = pd.read_parquet(entrada)
        qualificado = _qualificar_quadro(quadro, bloco)
        saida = pasta_saida / nome_arquivo.replace("_longo", "_qualificado")
        qualificado.to_parquet(saida, index=False)

        resumo = _resumir_pendencias(qualificado, bloco)
        pendencias.append(resumo)
        sem_codigo = qualificado["codigo_conta"].isna() | qualificado["codigo_conta"].astype(
            "string"
        ).str.strip().eq("")
        justificados = sem_codigo & qualificado["motivo_ausencia_codigo"].eq(
            "ausencia_justificada_por_tipo"
        )
        funcoes = qualificado["codigo_funcao"].dropna().astype("string")
        subfuncoes = qualificado["codigo_subfuncao"].dropna().astype("string")
        resultados.append(
            ResultadoQualificacaoBloco(
                bloco=bloco,
                arquivo_entrada=str(entrada),
                arquivo_saida=str(saida),
                registros=int(len(qualificado)),
                cabecalhos_distintos=int(qualificado["rotulo_conta_original"].nunique()),
                registros_com_codigo=int((~sem_codigo).sum()),
                registros_sem_codigo_justificado=int(justificados.sum()),
                registros_pendentes=int(qualificado["pendencia_revisao"].sum()),
                cabecalhos_pendentes=int(
                    qualificado.loc[qualificado["pendencia_revisao"], "rotulo_conta_original"].nunique()
                ),
                registros_com_funcao=int(funcoes.size),
                registros_com_subfuncao=int(subfuncoes.size),
                funcoes_distintas=int(funcoes.nunique()),
                subfuncoes_distintas=int(subfuncoes.nunique()),
                agregados_funcionais_residuais=int(
                    qualificado["tipo_registro"].eq("agregado_funcional_residual").sum()
                ),
                registros_intraorcamentarios=int(
                    qualificado["natureza_operacao"].eq("intraorcamentaria").sum()
                ),
                registros_deducao_receita=int(qualificado["deducao_receita"].sum()),
            )
        )

    quadro_pendencias = pd.concat(pendencias, ignore_index=True)
    parquet = pasta_saida / "pendencias_codigos_conta.parquet"
    xlsx = pasta_saida / "pendencias_codigos_conta.xlsx"
    quadro_pendencias.to_parquet(parquet, index=False)
    with pd.ExcelWriter(xlsx, engine="openpyxl") as escritor:
        quadro_pendencias.to_excel(escritor, sheet_name="Pendencias", index=False)
        pd.DataFrame([asdict(item) for item in resultados]).to_excel(
            escritor, sheet_name="Resumo", index=False
        )

    total_pendencias = sum(item.registros_pendentes for item in resultados)
    total_cabecalhos = sum(item.cabecalhos_pendentes for item in resultados)
    return ResultadoQualificacao(
        pasta_origem=str(pasta_normalizacao),
        pasta_saida=str(pasta_saida),
        blocos=resultados,
        total_registros=sum(item.registros for item in resultados),
        total_registros_pendentes=total_pendencias,
        total_cabecalhos_pendentes=total_cabecalhos,
        arquivo_pendencias_parquet=str(parquet),
        arquivo_pendencias_xlsx=str(xlsx),
        status="aprovado" if total_pendencias == 0 else "revisao_necessaria",
    )
