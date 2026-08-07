"""Reconciliacao dos alertas da normalizacao com a etapa de qualificacao.

A normalizacao e deliberadamente conservadora: registros sem codigo e cabecalhos
fora do dicionario sao sinalizados antes que a classificacao semantica seja
executada. Este modulo nao apaga esses alertas. Ele verifica se a etapa seguinte
os resolveu ou justificou e produz um estado final auditavel.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import json

from processamentos.normalizar_finbra import ResultadoNormalizacao
from processamentos.qualificar_codigos import ResultadoQualificacao


@dataclass
class ResultadoReconciliacaoNormalizacao:
    status_inicial: str
    status_final: str
    alertas_iniciais: int
    alertas_resolvidos: int
    alertas_pendentes: int
    alertas_criticos_pendentes: int
    registros_sem_codigo_iniciais: int
    registros_pendentes_qualificacao: int
    cabecalhos_sem_dicionario_iniciais: int
    cabecalhos_pendentes_qualificacao: int
    arquivo_resultado_json: str
    detalhes: list[dict[str, Any]]

    def como_dicionario(self) -> dict[str, Any]:
        return asdict(self)


def _classificar_alerta(
    nivel: str,
    mensagem: str,
    qualificacao: ResultadoQualificacao,
) -> tuple[str, str]:
    texto = mensagem.lower()

    if "registros ficaram sem codigo de conta" in texto:
        if qualificacao.total_registros_pendentes == 0:
            return "resolvido", "Registros sem codigo foram classificados ou justificados na qualificacao."
        return "pendente", "Ainda existem registros pendentes na qualificacao."

    if "cabecalhos nao foram localizados no dicionario" in texto:
        if qualificacao.total_cabecalhos_pendentes == 0:
            return "resolvido", "Cabecalhos foram recuperados por contingencia ou resolvidos na qualificacao."
        return "pendente", "Ainda existem cabecalhos pendentes na qualificacao."

    if nivel == "critico":
        return "pendente", "Alerta critico da normalizacao exige correcao na propria etapa."

    return "pendente", "Alerta nao possui regra automatica de reconciliacao."


def reconciliar_alertas_normalizacao(
    normalizacao: ResultadoNormalizacao,
    qualificacao: ResultadoQualificacao,
    pasta_saida: Path,
) -> ResultadoReconciliacaoNormalizacao:
    """Reconcilia alertas esperados da normalizacao contra a qualificacao posterior."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    detalhes: list[dict[str, Any]] = []

    for aba in normalizacao.abas:
        for alerta in aba.alertas:
            situacao, justificativa = _classificar_alerta(
                alerta["nivel"], alerta["mensagem"], qualificacao
            )
            detalhes.append(
                {
                    "aba": aba.aba_origem,
                    "nivel": alerta["nivel"],
                    "mensagem": alerta["mensagem"],
                    "situacao": situacao,
                    "justificativa": justificativa,
                }
            )

    resolvidos = sum(item["situacao"] == "resolvido" for item in detalhes)
    pendentes = sum(item["situacao"] == "pendente" for item in detalhes)
    criticos_pendentes = sum(
        item["situacao"] == "pendente" and item["nivel"] == "critico" for item in detalhes
    )

    if criticos_pendentes:
        status_final = "reprovado"
    elif pendentes:
        status_final = "aprovado_com_alertas"
    else:
        status_final = "aprovado"

    arquivo = pasta_saida / "resultado_normalizacao_reconciliada.json"
    resultado = ResultadoReconciliacaoNormalizacao(
        status_inicial=normalizacao.status,
        status_final=status_final,
        alertas_iniciais=len(detalhes),
        alertas_resolvidos=int(resolvidos),
        alertas_pendentes=int(pendentes),
        alertas_criticos_pendentes=int(criticos_pendentes),
        registros_sem_codigo_iniciais=normalizacao.total_registros_sem_codigo_conta,
        registros_pendentes_qualificacao=qualificacao.total_registros_pendentes,
        cabecalhos_sem_dicionario_iniciais=normalizacao.total_cabecalhos_sem_dicionario,
        cabecalhos_pendentes_qualificacao=qualificacao.total_cabecalhos_pendentes,
        arquivo_resultado_json=str(arquivo),
        detalhes=detalhes,
    )
    arquivo.write_text(
        json.dumps(resultado.como_dicionario(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return resultado
