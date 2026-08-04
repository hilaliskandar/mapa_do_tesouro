"""Normalizacao auditavel das abas FINBRA para formato longo."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import re
import unicodedata
from typing import Any

import pandas as pd


ABAS_DADOS = {
    "receitas": "receitas",
    "despesas": "despesas",
    "despesa por funcao": "despesa_por_funcao",
}
ABAS_AUXILIARES = {
    "cobertura": "cobertura",
    "dicionario": "dicionario",
    "fontes": "fontes",
    "leia me": "leia_me",
}
CANDIDATOS_IDENTIFICADORES = {
    "ano": "ano",
    "exercicio": "ano",
    "municipio": "municipio",
    "nome_municipio": "municipio",
    "codigo_ibge": "codigo_ibge",
    "cod_ibge": "codigo_ibge",
    "codigo_municipio": "codigo_ibge",
    "uf": "uf",
    "sigla_uf": "uf",
    "populacao": "populacao",
}
IDENTIFICADORES_ORDEM = ("uf", "codigo_ibge", "municipio", "ano", "populacao")
PADRAO_CODIGO_CONTA = re.compile(r"^\s*([0-9]+(?:[.\-][0-9A-Za-z]+)*)\s*[-–:]\s*(.+?)\s*$")


@dataclass
class ResultadoNormalizacaoAba:
    aba_origem: str
    tipo: str
    arquivo_saida: str
    linhas_origem: int
    colunas_origem: int
    colunas_identificadoras: list[str]
    colunas_valores: int
    celulas_candidatas: int
    valores_preenchidos_origem: int
    registros_contabeis_preservados: int
    valores_ausentes_omitidos: int
    valores_nao_numericos: int
    cabecalhos_contabeis: int = 0
    cabecalhos_correspondidos_dicionario: int = 0
    cabecalhos_sem_dicionario: int = 0
    registros_sem_codigo_conta: int = 0
    registros_sem_estagio: int = 0
    duplicidades_observacao: int = 0
    anos: list[int] = field(default_factory=list)
    municipios: int | None = None
    codigos_ibge: int | None = None
    alertas: list[dict[str, str]] = field(default_factory=list)

    @property
    def valores_preservados(self) -> int:
        """Compatibilidade com relatorios das versoes anteriores."""
        return self.registros_contabeis_preservados


@dataclass
class ResultadoNormalizacao:
    arquivo_origem: str
    pasta_saida: str
    arquivo_dimensao_municipio_ano: str
    abas: list[ResultadoNormalizacaoAba]
    total_registros_contabeis: int
    total_celulas_auxiliares_preservadas: int
    total_ausentes_omitidos: int
    total_nao_numericos: int
    total_cabecalhos_sem_dicionario: int
    total_registros_sem_codigo_conta: int
    total_registros_sem_estagio: int
    total_duplicidades_observacao: int
    inconsistencias_populacao: int
    alertas_criticos: int
    alertas_relevantes: int
    status: str

    @property
    def total_valores_preservados(self) -> int:
        """Compatibilidade com o manifesto das versoes anteriores."""
        return self.total_registros_contabeis + self.total_celulas_auxiliares_preservadas

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def normalizar_texto(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = texto.strip().lower()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def _nome_aba_normalizado(nome: str) -> str:
    return normalizar_texto(nome).replace("_", " ")


def _mapear_identificadores(colunas: list[object]) -> dict[object, str]:
    mapeamento: dict[object, str] = {}
    usados: set[str] = set()
    for coluna in colunas:
        destino = CANDIDATOS_IDENTIFICADORES.get(normalizar_texto(coluna))
        if destino and destino not in usados:
            mapeamento[coluna] = destino
            usados.add(destino)
    return mapeamento


def _separar_codigo_descricao(valor: object) -> tuple[str | None, str]:
    texto = str(valor).strip()
    correspondencia = PADRAO_CODIGO_CONTA.match(texto)
    if correspondencia:
        return correspondencia.group(1).strip(), correspondencia.group(2).strip()
    return None, texto


def _decompor_coluna_contabil(rotulo: object) -> tuple[str | None, str | None, str]:
    """Decompoe cabecalho quando nao houver correspondencia no dicionario."""
    original = str(rotulo).strip()
    if "|" in original:
        estagio, conta = original.split("|", maxsplit=1)
        codigo, descricao = _separar_codigo_descricao(conta)
        return estagio.strip() or None, codigo, descricao
    codigo, descricao = _separar_codigo_descricao(original)
    return None, codigo, descricao


def _padronizar_identificadores(
    quadro: pd.DataFrame, mapeamento: dict[object, str]
) -> pd.DataFrame:
    resultado = quadro.rename(columns=mapeamento).copy()
    if "ano" in resultado.columns:
        resultado["ano"] = pd.to_numeric(resultado["ano"], errors="coerce").astype("Int64")
    if "codigo_ibge" in resultado.columns:
        resultado["codigo_ibge"] = (
            resultado["codigo_ibge"]
            .astype("string")
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
            .str.zfill(7)
        )
    if "municipio" in resultado.columns:
        resultado["municipio"] = resultado["municipio"].astype("string").str.strip()
    if "uf" in resultado.columns:
        resultado["uf"] = resultado["uf"].astype("string").str.strip().str.upper()
    if "populacao" in resultado.columns:
        resultado["populacao"] = pd.to_numeric(
            resultado["populacao"], errors="coerce"
        ).astype("Int64")
    return resultado


def _carregar_dicionario(livro: pd.ExcelFile) -> tuple[dict[tuple[str, str], dict[str, str | None]], pd.DataFrame]:
    nome_aba = next(
        (nome for nome in livro.sheet_names if _nome_aba_normalizado(nome) == "dicionario"),
        None,
    )
    if nome_aba is None:
        return {}, pd.DataFrame()

    quadro = pd.read_excel(livro, sheet_name=nome_aba)
    colunas = {normalizar_texto(coluna): coluna for coluna in quadro.columns}
    coluna_cabecalho = colunas.get("cabecalho_na_matriz")
    coluna_aba = colunas.get("aba")
    coluna_estagio = colunas.get("estagio_contabil")
    coluna_conta = colunas.get("conta_subconta_original")
    coluna_bloco = colunas.get("bloco")
    if coluna_cabecalho is None or coluna_conta is None:
        return {}, quadro

    mapa: dict[tuple[str, str], dict[str, str | None]] = {}
    for _, linha in quadro.iterrows():
        cabecalho = linha.get(coluna_cabecalho)
        if pd.isna(cabecalho):
            continue
        aba = linha.get(coluna_aba) if coluna_aba is not None else ""
        aba_chave = _nome_aba_normalizado(str(aba)) if pd.notna(aba) else ""
        conta_original = linha.get(coluna_conta)
        codigo, descricao = _separar_codigo_descricao(conta_original)
        estagio = linha.get(coluna_estagio) if coluna_estagio is not None else None
        bloco = linha.get(coluna_bloco) if coluna_bloco is not None else None
        mapa[(aba_chave, str(cabecalho).strip())] = {
            "estagio": None if pd.isna(estagio) else str(estagio).strip(),
            "codigo_conta": codigo,
            "descricao_conta": descricao,
            "bloco_dicionario": None if pd.isna(bloco) else str(bloco).strip(),
        }
    return mapa, quadro


def _metadados_cabecalhos(
    nome_aba: str,
    colunas_valores: list[object],
    dicionario: dict[tuple[str, str], dict[str, str | None]],
) -> pd.DataFrame:
    aba_chave = _nome_aba_normalizado(nome_aba)
    linhas: list[dict[str, object]] = []
    for coluna in colunas_valores:
        rotulo = str(coluna).strip()
        dados = dicionario.get((aba_chave, rotulo))
        if dados is not None:
            linhas.append(
                {
                    "rotulo_conta_original": coluna,
                    "estagio": dados["estagio"],
                    "codigo_conta": dados["codigo_conta"],
                    "descricao_conta": dados["descricao_conta"],
                    "origem_metadados": "dicionario",
                }
            )
        else:
            estagio, codigo, descricao = _decompor_coluna_contabil(coluna)
            linhas.append(
                {
                    "rotulo_conta_original": coluna,
                    "estagio": estagio,
                    "codigo_conta": codigo,
                    "descricao_conta": descricao,
                    "origem_metadados": "regra_contingencia",
                }
            )
    return pd.DataFrame(linhas)


def _normalizar_aba_dados(
    quadro: pd.DataFrame,
    nome_aba: str,
    bloco: str,
    pasta_saida: Path,
    dicionario: dict[tuple[str, str], dict[str, str | None]],
) -> tuple[ResultadoNormalizacaoAba, pd.DataFrame]:
    mapeamento = _mapear_identificadores(list(quadro.columns))
    alertas: list[dict[str, str]] = []
    obrigatorios = {"ano", "municipio", "codigo_ibge"}
    encontrados = set(mapeamento.values())
    faltantes = sorted(obrigatorios.difference(encontrados))
    if faltantes:
        alertas.append(
            {"nivel": "critico", "mensagem": f"Identificadores obrigatorios ausentes: {faltantes}"}
        )

    padronizado = _padronizar_identificadores(quadro, mapeamento)
    identificadores = [campo for campo in IDENTIFICADORES_ORDEM if campo in padronizado.columns]
    colunas_valores = [coluna for coluna in padronizado.columns if coluna not in identificadores]
    if any(normalizar_texto(coluna) == "populacao" for coluna in colunas_valores):
        alertas.append(
            {"nivel": "critico", "mensagem": "Populacao foi indevidamente mantida entre as contas."}
        )

    metadados = _metadados_cabecalhos(nome_aba, colunas_valores, dicionario)
    cabecalhos_sem_dicionario = int(
        metadados["origem_metadados"].eq("regra_contingencia").sum()
    )
    if cabecalhos_sem_dicionario:
        alertas.append(
            {
                "nivel": "relevante",
                "mensagem": f"{cabecalhos_sem_dicionario} cabecalhos nao foram localizados no dicionario.",
            }
        )

    celulas_candidatas = len(padronizado) * len(colunas_valores)
    preenchidos_origem = int(padronizado[colunas_valores].notna().sum().sum())
    longo = padronizado.melt(
        id_vars=identificadores,
        value_vars=colunas_valores,
        var_name="rotulo_conta_original",
        value_name="valor_original",
    )
    ausentes = int(longo["valor_original"].isna().sum())
    longo = longo[longo["valor_original"].notna()].copy()
    longo["valor"] = pd.to_numeric(longo["valor_original"], errors="coerce")
    nao_numericos = int(longo["valor"].isna().sum())
    if nao_numericos:
        alertas.append(
            {"nivel": "relevante", "mensagem": f"Foram encontrados {nao_numericos} valores nao numericos."}
        )

    longo = longo.merge(metadados, on="rotulo_conta_original", how="left", validate="many_to_one")
    longo.insert(0, "bloco", bloco)
    longo.insert(1, "aba_origem", nome_aba)

    sem_codigo = int(longo["codigo_conta"].isna().sum())
    sem_estagio = int(longo["estagio"].isna().sum())
    if sem_codigo:
        alertas.append(
            {"nivel": "relevante", "mensagem": f"{sem_codigo} registros ficaram sem codigo de conta."}
        )
    if sem_estagio:
        alertas.append(
            {"nivel": "relevante", "mensagem": f"{sem_estagio} registros ficaram sem estagio contabil."}
        )

    chave_observacao = [
        campo
        for campo in ("codigo_ibge", "ano", "estagio", "codigo_conta", "rotulo_conta_original")
        if campo in longo.columns
    ]
    duplicidades = int(longo.duplicated(subset=chave_observacao, keep=False).sum())
    if duplicidades:
        alertas.append(
            {"nivel": "critico", "mensagem": f"{duplicidades} registros pertencem a chaves contabeis duplicadas."}
        )

    if len(longo) != preenchidos_origem:
        alertas.append(
            {
                "nivel": "critico",
                "mensagem": "A quantidade de registros longos nao corresponde as celulas preenchidas da matriz.",
            }
        )

    colunas_saida = [
        "bloco",
        "aba_origem",
        *[campo for campo in ("uf", "codigo_ibge", "municipio", "ano") if campo in longo.columns],
        "estagio",
        "codigo_conta",
        "descricao_conta",
        "rotulo_conta_original",
        "origem_metadados",
        "valor",
        "valor_original",
    ]
    longo = longo[colunas_saida]
    caminho_saida = pasta_saida / f"{bloco}_longo.parquet"
    longo.to_parquet(caminho_saida, index=False)

    dimensao_colunas = [
        campo for campo in ("uf", "codigo_ibge", "municipio", "ano", "populacao") if campo in padronizado.columns
    ]
    dimensao = padronizado[dimensao_colunas].drop_duplicates().copy()

    anos = sorted(int(valor) for valor in longo["ano"].dropna().unique()) if "ano" in longo else []
    municipios = int(longo["municipio"].nunique()) if "municipio" in longo else None
    codigos = int(longo["codigo_ibge"].nunique()) if "codigo_ibge" in longo else None
    resultado = ResultadoNormalizacaoAba(
        aba_origem=nome_aba,
        tipo="dados",
        arquivo_saida=str(caminho_saida),
        linhas_origem=int(quadro.shape[0]),
        colunas_origem=int(quadro.shape[1]),
        colunas_identificadoras=identificadores,
        colunas_valores=len(colunas_valores),
        celulas_candidatas=celulas_candidatas,
        valores_preenchidos_origem=preenchidos_origem,
        registros_contabeis_preservados=int(len(longo)),
        valores_ausentes_omitidos=ausentes,
        valores_nao_numericos=nao_numericos,
        cabecalhos_contabeis=len(colunas_valores),
        cabecalhos_correspondidos_dicionario=len(colunas_valores) - cabecalhos_sem_dicionario,
        cabecalhos_sem_dicionario=cabecalhos_sem_dicionario,
        registros_sem_codigo_conta=sem_codigo,
        registros_sem_estagio=sem_estagio,
        duplicidades_observacao=duplicidades,
        anos=anos,
        municipios=municipios,
        codigos_ibge=codigos,
        alertas=alertas,
    )
    return resultado, dimensao


def _normalizar_aba_auxiliar(
    quadro: pd.DataFrame,
    nome_aba: str,
    nome_saida: str,
    pasta_saida: Path,
) -> ResultadoNormalizacaoAba:
    mapeamento = _mapear_identificadores(list(quadro.columns))
    padronizado = _padronizar_identificadores(quadro, mapeamento)
    caminho_saida = pasta_saida / f"auxiliar_{nome_saida}.parquet"
    padronizado.to_parquet(caminho_saida, index=False)
    identificadores = [campo for campo in IDENTIFICADORES_ORDEM if campo in padronizado.columns]
    anos = sorted(int(valor) for valor in padronizado["ano"].dropna().unique()) if "ano" in padronizado else []
    municipios = int(padronizado["municipio"].nunique()) if "municipio" in padronizado else None
    codigos = int(padronizado["codigo_ibge"].nunique()) if "codigo_ibge" in padronizado else None
    preenchidos = int(quadro.notna().sum().sum())
    return ResultadoNormalizacaoAba(
        aba_origem=nome_aba,
        tipo="auxiliar",
        arquivo_saida=str(caminho_saida),
        linhas_origem=int(quadro.shape[0]),
        colunas_origem=int(quadro.shape[1]),
        colunas_identificadoras=identificadores,
        colunas_valores=max(0, quadro.shape[1] - len(identificadores)),
        celulas_candidatas=int(quadro.shape[0] * quadro.shape[1]),
        valores_preenchidos_origem=preenchidos,
        registros_contabeis_preservados=0,
        valores_ausentes_omitidos=int(quadro.isna().sum().sum()),
        valores_nao_numericos=0,
        anos=anos,
        municipios=municipios,
        codigos_ibge=codigos,
        alertas=[],
    )


def _consolidar_dimensao(dimensoes: list[pd.DataFrame], pasta_saida: Path) -> tuple[Path, int]:
    if not dimensoes:
        caminho = pasta_saida / "dimensao_municipio_ano.parquet"
        pd.DataFrame().to_parquet(caminho, index=False)
        return caminho, 0

    combinado = pd.concat(dimensoes, ignore_index=True)
    chave = [campo for campo in ("codigo_ibge", "ano") if campo in combinado.columns]
    inconsistencias = 0
    if "populacao" in combinado.columns and chave:
        contagens = combinado.groupby(chave, dropna=False)["populacao"].nunique(dropna=True)
        inconsistencias = int((contagens > 1).sum())
    ordenacao = [campo for campo in ("codigo_ibge", "ano") if campo in combinado.columns]
    dimensao = combinado.drop_duplicates().sort_values(ordenacao).drop_duplicates(subset=chave, keep="first")
    caminho = pasta_saida / "dimensao_municipio_ano.parquet"
    dimensao.to_parquet(caminho, index=False)
    return caminho, inconsistencias


def normalizar_arquivo_finbra(caminho: Path, pasta_saida: Path) -> ResultadoNormalizacao:
    """Normaliza as abas, usa o dicionario e grava produtos auditaveis em Parquet."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    livro = pd.ExcelFile(caminho)
    dicionario, _ = _carregar_dicionario(livro)
    resultados: list[ResultadoNormalizacaoAba] = []
    dimensoes: list[pd.DataFrame] = []

    for nome_aba in livro.sheet_names:
        quadro = pd.read_excel(livro, sheet_name=nome_aba)
        nome_normalizado = _nome_aba_normalizado(nome_aba)
        if nome_normalizado in ABAS_DADOS:
            resultado, dimensao = _normalizar_aba_dados(
                quadro,
                nome_aba,
                ABAS_DADOS[nome_normalizado],
                pasta_saida,
                dicionario,
            )
            resultados.append(resultado)
            dimensoes.append(dimensao)
        elif nome_normalizado in ABAS_AUXILIARES:
            resultados.append(
                _normalizar_aba_auxiliar(
                    quadro, nome_aba, ABAS_AUXILIARES[nome_normalizado], pasta_saida
                )
            )
        else:
            caminho_saida = pasta_saida / f"nao_classificada_{normalizar_texto(nome_aba)}.parquet"
            quadro.to_parquet(caminho_saida, index=False)
            resultados.append(
                ResultadoNormalizacaoAba(
                    aba_origem=nome_aba,
                    tipo="nao_classificada",
                    arquivo_saida=str(caminho_saida),
                    linhas_origem=int(quadro.shape[0]),
                    colunas_origem=int(quadro.shape[1]),
                    colunas_identificadoras=[],
                    colunas_valores=int(quadro.shape[1]),
                    celulas_candidatas=int(quadro.shape[0] * quadro.shape[1]),
                    valores_preenchidos_origem=int(quadro.notna().sum().sum()),
                    registros_contabeis_preservados=0,
                    valores_ausentes_omitidos=int(quadro.isna().sum().sum()),
                    valores_nao_numericos=0,
                    alertas=[{"nivel": "relevante", "mensagem": "Aba nao classificada automaticamente."}],
                )
            )

    caminho_dimensao, inconsistencias_populacao = _consolidar_dimensao(dimensoes, pasta_saida)
    if inconsistencias_populacao:
        for resultado in resultados:
            if resultado.tipo == "dados":
                resultado.alertas.append(
                    {
                        "nivel": "critico",
                        "mensagem": f"Foram encontradas {inconsistencias_populacao} divergencias de populacao entre abas.",
                    }
                )
                break

    criticos = sum(1 for aba in resultados for alerta in aba.alertas if alerta["nivel"] == "critico")
    relevantes = sum(1 for aba in resultados for alerta in aba.alertas if alerta["nivel"] == "relevante")
    status = "reprovado" if criticos else "aprovado_com_alertas" if relevantes else "aprovado"
    abas_dados = [aba for aba in resultados if aba.tipo == "dados"]
    abas_auxiliares = [aba for aba in resultados if aba.tipo != "dados"]
    return ResultadoNormalizacao(
        arquivo_origem=caminho.name,
        pasta_saida=str(pasta_saida),
        arquivo_dimensao_municipio_ano=str(caminho_dimensao),
        abas=resultados,
        total_registros_contabeis=sum(aba.registros_contabeis_preservados for aba in abas_dados),
        total_celulas_auxiliares_preservadas=sum(aba.valores_preenchidos_origem for aba in abas_auxiliares),
        total_ausentes_omitidos=sum(aba.valores_ausentes_omitidos for aba in abas_dados),
        total_nao_numericos=sum(aba.valores_nao_numericos for aba in abas_dados),
        total_cabecalhos_sem_dicionario=sum(aba.cabecalhos_sem_dicionario for aba in abas_dados),
        total_registros_sem_codigo_conta=sum(aba.registros_sem_codigo_conta for aba in abas_dados),
        total_registros_sem_estagio=sum(aba.registros_sem_estagio for aba in abas_dados),
        total_duplicidades_observacao=sum(aba.duplicidades_observacao for aba in abas_dados),
        inconsistencias_populacao=inconsistencias_populacao,
        alertas_criticos=criticos,
        alertas_relevantes=relevantes,
        status=status,
    )
