# Versao 0.7.0 — motor declarativo de indicadores

A versao 0.7.0 inicia formalmente a camada de indicadores do Mapa do Tesouro.

## Principio central

As formulas nao ficam embutidas no codigo Python. Cada indicador e definido em `referencias/catalogos/indicadores_iniciais.yaml`, com identificador, nome, grupo analitico, operacao, conceitos do numerador e denominador, multiplicador, unidade, interpretacao e referencia metodologica.

O motor usa somente `agregados_semanticos.parquet`, portanto opera depois da qualificacao contabil, hierarquia, fechamento semantico e selecao contra dupla contagem.

## Tratamento de ausencias

Ausencia de conceito necessario nao e convertida em zero. O resultado recebe `status_calculo = dados_insuficientes` e o valor do indicador permanece ausente. Denominadores iguais a zero tambem nao produzem razoes.

## Indicadores iniciais

O catalogo inicial inclui autonomia tributaria estrita, dependencia de transferencias correntes, FPM e ICMS, participacoes de IPTU, ISS e ITBI na receita tributaria, investimentos na despesa de capital, pessoal como proxy nas despesas correntes e juros nas despesas correntes.

As formulas sao propositalmente limitadas aos conceitos ja consolidados. Valores reais, indicadores per capita e medidas dependentes de RGF, RREO ou informacoes patrimoniais permanecem fora desta versao.

## Produtos

A etapa `08_indicadores` gera:

- `indicadores.parquet`;
- `indicadores.xlsx`;
- `painel_indicadores_municipio_ano.parquet`;
- `cobertura_indicadores.parquet`;
- `resultado_indicadores.json`.

A planilha Excel registra indicadores, painel, cobertura e copia do catalogo utilizado, permitindo auditoria da formula aplicada em cada execucao.

## Proximas etapas

A validacao da base real deve preceder a introducao de deflacao e denominadores populacionais. A etapa seguinte devera distinguir explicitamente valores nominais e reais, incorporar fatores IPCA para precos de junho de 2026 e integrar populacao anual para calculos per capita.