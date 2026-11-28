"""Leitura somente de universo municipal no SQLite canônico.

Este módulo NAO altera a base fiscal. O arquivo é aberto por URI SQLite
em modo read-only. A vinculação representa ente recebedor da proposta.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from urllib.parse import quote

from pipeline.normalize.federal_territory import match_recipient, MunicipalMatch


def load_universe_codes(
    database: Path,
    *,
    universe_id: str = "SP_645",
    expected_count: int = 645,
) -> frozenset[str]:
    """Lê municipio e universo_municipio conforme o schema canônico.

    Recusa universo incompleto, código fora de SP, inconsistência entre tabelas,
    códigos repetidos ou municípios não ativos. Nunca consulta o banco em escrita.
    """
    database = Path(database).resolve(strict=True)
    if not database.is_file():
        raise ValueError("SQLite canônico deve ser arquivo regular")
    if expected_count < 1:
        raise ValueError("expected_count deve ser positivo")
    uri = "file:" + quote(str(database), safe="/:") + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        con.execute("PRAGMA query_only=ON")
        rows = con.execute(
            """SELECT um.codigo_ibge, m.codigo_ibge, m.uf, m.ativo
               FROM universo_municipio AS um
               LEFT JOIN municipio AS m ON m.codigo_ibge=um.codigo_ibge
               WHERE um.universo_id=? ORDER BY um.codigo_ibge""",
            (universe_id,),
        ).fetchall()
    finally:
        con.close()
    if len(rows) != expected_count:
        raise ValueError(
            f"Universo {universe_id} incompleto: {len(rows)} vs {expected_count}"
        )
    codes: list[str] = []
    for code, municipality_code, uf, active in rows:
        if (
            not isinstance(code, str)
            or len(code) != 7
            or not code.isascii()
            or not code.isdigit()
            or not code.startswith("35")
            or municipality_code != code
            or uf != "SP"
            or active != 1
        ):
            raise ValueError(f"Municipio inválido no universo {universe_id}: {code}")
        codes.append(code)
    if len(set(codes)) != len(codes):
        raise ValueError("Codigo IBGE duplicado no universo")
    return frozenset(codes)


def match_with_canonical_sqlite(
    proposal: dict,
    *,
    database: Path,
    universe_id: str = "SP_645",
) -> MunicipalMatch:
    """Associa um recebedor a SP645, nao comprova pagamento nem local da obra."""
    codes = load_universe_codes(database, universe_id=universe_id)
    return match_recipient(proposal, municipal_ibge_codes=codes)
