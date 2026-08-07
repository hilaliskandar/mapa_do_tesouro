from pathlib import Path


def teste_aplicacao_registra_versao_e_fechamento_semantico() -> None:
    conteudo = Path("aplicacao.py").read_text(encoding="utf-8")

    assert 'VERSAO_SISTEMA = "0.7.0"' in conteudo
    assert '"mapa_semantico_inicial"' in conteudo
    assert '"aperfeicoamento_semantico"' in conteudo
    assert '"registros_nao_mapeados_finais"' in conteudo
    assert '"incompatibilidades"' in conteudo
    assert '"indicadores"' in conteudo
