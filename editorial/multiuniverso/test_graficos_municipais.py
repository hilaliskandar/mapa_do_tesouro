#!/usr/bin/env python3
"""Testa exclusao de ausentes e comparacao com a mesma escala."""
from graficos_municipais import charts

def shown(v,unit,key):return str(v)
def main():
    context={"variables":{
     "receita":{"metadata":{"nome":"Receita","unidade":"BRL"},"latest":{"status":"observado","value":120.0},"group_latest":{"observed":6,"expected":8,"numeric":{"median":100.0}}},
     "ausente":{"metadata":{"nome":"Ausente","unidade":"BRL"},"latest":{"status":"ausente","value":100},"group_latest":{"observed":8,"expected":8,"numeric":{"median":90}}},
     "parcial":{"metadata":{"nome":"Parcial","unidade":"BRL"},"latest":{"status":"observado","value":25},"group_latest":{"observed":2,"expected":8,"numeric":{"median":15}}}
    }}
    result=charts(context,shown)
    assert "Receita" in result and "120.0" in result and "100.0" in result
    assert "Ausente" not in result and "Parcial" not in result
    assert result.count('class="chart-card"')==1
    print("QA municipal: observado, comparavel, cobertura e ausencia OK")
if __name__=="__main__":main()
