#!/usr/bin/env python3
"""Testes unitarios das regras de sintese e da apresentação fiscal."""
import copy
from build_boletins import generate, shown

def make_context(observed=4,expected=4):
    return {
        "publication_id":"TEST_GROUP","name":"Universo de teste","member_count":4,
        "members":[{"nome":f"Município {i}","codigo_ibge":str(3500000+i)} for i in range(4)],
        "latest_year":2025,
        "variables":{"investimento_pct":{"editorial_group":"despesas","metadata":{"nome":"Investimento / Receita","unidade":"percentual"},
            "latest":{"observed":observed,"expected":expected,"numeric":{"median":12.0,"q1":9.0,"q3":16.0}},
            "yearly":[{"year":2025,"observed":observed,"expected":expected,"numeric":{"median":12.0}}]}}
    }

def main():
    assert shown(12.0,"percentual","investimento_pct_receita_corrente")=="12,00%"
    assert shown(.4099,"percentual","dtp_pct_rcl")=="40,99%"
    assert shown(.0221,"percentual","dc_pct_rcl")=="2,21%"
    assert shown(0,"percentual")=="0,00%"
    assert shown(None,"percentual")=="Não disponível"
    full=generate(make_context(),"https://example.org/context.json")
    assert "Síntese comparativa das contas com cobertura integral" in full
    assert "12,00%" in full and "9,00%" in full and "16,00%" in full
    assert "Evolução das medianas municipais" in full
    partial=generate(make_context(observed=3),"https://example.org/context.json")
    assert "Não há variáveis numéricas com cobertura integral" in partial
    assert "Síntese comparativa das contas com cobertura integral" not in partial
    invalid=make_context(expected=5)
    try:
        generate(invalid,"https://example.org/context.json")
    except ValueError:
        pass
    else:
        raise AssertionError("Denominador incompatível foi aceito")
    print("QA semantico aprovado: percentual, cobertura e condicao narrativa.")

if __name__=="__main__":main()
