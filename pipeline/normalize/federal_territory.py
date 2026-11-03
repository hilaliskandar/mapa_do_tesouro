"""Classificacao territorial conservadora de propostas Transferegov.

O municipio recebedor nao e necessariamente o municipio da obra, nem o
recebimento foi comprovado so pela existencia da proposta.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, Mapping


@dataclass(frozen=True)
class MunicipalMatch:
    proposal_id: str | None
    municipality_code: str | None
    status: str
    role: str = "ente_recebedor_proposta"
    reason: str = ""


def _code(raw: Any) -> str | None:
    """Aceita somente IBGE literal com 7 digitos; nao infere por municipio."""
    if isinstance(raw, bool) or raw is None:
        return None
    if isinstance(raw, int):
        raw = str(raw)
    if not isinstance(raw, str):
        return None
    value = raw.strip()
    return value if len(value) == 7 and value.isascii() and value.isdigit() else None


def match_recipient(
    proposal: Mapping[str, Any],
    *,
    municipal_ibge_codes: Collection[str],
) -> MunicipalMatch:
    """Valida membro do cadastro SP645 fornecido; nunca atribui localizacao da obra."""
    codes = set(municipal_ibge_codes)
    if not codes or any(_code(value) != value for value in codes):
        raise ValueError("Cadastro municipal invalido; exigir codigos IBGE literais")
    proposal_id = proposal.get("id_proposta")
    if proposal_id is None:
        pid = None
    elif isinstance(proposal_id, (str, int)) and not isinstance(proposal_id, bool):
        pid = str(proposal_id)
    else:
        pid = None
    raw = proposal.get("cd_ibge_recebedor")
    code = _code(raw)
    if code is None:
        return MunicipalMatch(pid, None, "em_revisao", reason="codigo_ibge_ausente_ou_invalido")
    if code not in codes:
        return MunicipalMatch(pid, code, "fora_do_universo", reason="codigo_nao_consta_do_cadastro")
    return MunicipalMatch(pid, code, "confirmado_recebedor", reason="codigo_ibge_em_cadastro")


def municipal_summary(
    proposals: list[Mapping[str, Any]], *, municipal_ibge_codes: Collection[str]
) -> dict[str, Any]:
    """Contagem de propostas, nao de repasses, obras ou municipios distintos."""
    results = [
        match_recipient(row, municipal_ibge_codes=municipal_ibge_codes)
        for row in proposals
    ]
    counts: dict[str, int] = {}
    for item in results:
        counts[item.status] = counts.get(item.status, 0) + 1
    return {
        "record_count": len(results),
        "status_counts": counts,
        "matches": results,
        "financial_value": None,
        "notice": "Contagens de propostas; nao equivalem a transferencias ou pagamentos.",
    }
