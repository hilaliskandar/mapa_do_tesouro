# Versao 0.5.1

A versao corrige os problemas observados na execucao 0.5.0.

## Alteracoes centrais

1. O mapa semantico passa a ser aplicado aos registros qualificados, antes da selecao hierarquica.
2. A selecao hierarquica e dividida em totalizacao e decomposicao.
3. A conciliacao entre contas-pai e filhos passa a ser armazenada em produto proprio.
4. O catalogo semantico declara nivel e finalidade de cada conceito.
5. Todas as 28 funcoes orcamentarias recebem correspondencia inicial.
6. Despesas Correntes e Despesas de Capital recebem conceitos proprios de totalizacao.
7. A cobertura passa a ser medida por registros, codigos e valor absoluto.
8. Um bloco obrigatorio com cobertura zero reprova a etapa semantica.

## Ordem do processamento

```text
validacao
-> normalizacao
-> qualificacao
-> hierarquia
-> mapa semantico
-> selecao de totalizacao e decomposicao
```

## Produtos novos

```text
05_mapa_semantico/
06_selecao_hierarquica/
├── selecao_totalizacao.parquet
├── selecao_decomposicao.parquet
├── conciliacao_hierarquica.parquet
└── selecao_hierarquica.xlsx
```

A selecao de totalizacao nao deve ser usada para indicadores de composicao. A selecao de decomposicao preserva as folhas observadas, mas cada indicador ainda devera declarar conceito, estagio, natureza da operacao, sinal e periodo de vigencia.
