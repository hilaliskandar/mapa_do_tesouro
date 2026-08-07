from pathlib import Path
from types import SimpleNamespace

from processamentos.reconciliar_alertas_normalizacao import reconciliar_alertas_normalizacao


def teste_reconciliacao_resolve_alertas_encaminhados_a_qualificacao(tmp_path: Path) -> None:
    normalizacao = SimpleNamespace(
        status="aprovado_com_alertas",
        total_registros_sem_codigo_conta=15233,
        total_cabecalhos_sem_dicionario=36,
        abas=[
            SimpleNamespace(
                aba_origem="Receitas",
                alertas=[
                    {"nivel": "relevante", "mensagem": "28 cabecalhos nao foram localizados no dicionario."},
                    {"nivel": "relevante", "mensagem": "6730 registros ficaram sem codigo de conta."},
                ],
            ),
            SimpleNamespace(
                aba_origem="Despesas",
                alertas=[
                    {"nivel": "relevante", "mensagem": "8 cabecalhos nao foram localizados no dicionario."},
                    {"nivel": "relevante", "mensagem": "1877 registros ficaram sem codigo de conta."},
                ],
            ),
            SimpleNamespace(
                aba_origem="Despesa por funcao",
                alertas=[
                    {"nivel": "relevante", "mensagem": "6626 registros ficaram sem codigo de conta."}
                ],
            ),
        ],
    )
    qualificacao = SimpleNamespace(
        total_registros_pendentes=0,
        total_cabecalhos_pendentes=0,
    )

    resultado = reconciliar_alertas_normalizacao(normalizacao, qualificacao, tmp_path)

    assert resultado.status_inicial == "aprovado_com_alertas"
    assert resultado.status_final == "aprovado"
    assert resultado.alertas_iniciais == 5
    assert resultado.alertas_resolvidos == 5
    assert resultado.alertas_pendentes == 0
    assert (tmp_path / "resultado_normalizacao_reconciliada.json").exists()
