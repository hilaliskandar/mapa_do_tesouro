# Versao 0.6.0 — agregacoes semanticas auditaveis

## Finalidade

A versao 0.6.0 inaugura a camada de resultados analiticos do Mapa do Tesouro. O sistema deixa de apenas qualificar, hierarquizar e classificar contas e passa a produzir valores organizados por conceito fiscal, municipio, exercicio, estagio e natureza da operacao.

## Regra de selecao por finalidade

Os conceitos classificados com `finalidade_semantica = totalizacao` utilizam a selecao hierarquica de totalizacao. Essa selecao privilegia contas-pai conciliadas e impede a soma simultanea de pais e descendentes.

Os conceitos de composicao e indicador utilizam a selecao de decomposicao. Essa selecao preserva folhas observadas e permite calcular itens como IPTU, ISS, ITBI, investimentos e funcoes orcamentarias.

A separacao e obrigatoria porque uma unica selecao nao atende simultaneamente aos objetivos de totalizar e decompor a estrutura fiscal.

## Produtos

A etapa gera:

```text
07_agregacoes_semanticas/
├── agregados_semanticos.parquet
├── agregados_semanticos.xlsx
├── painel_semantico_municipio_ano.parquet
├── linhagem_agregados_semanticos.parquet
└── resultado_agregacoes_semanticas.json
```

### Base longa

`agregados_semanticos.parquet` contem uma linha por combinacao de:

- bloco;
- codigo IBGE;
- municipio;
- ano;
- estagio;
- natureza da operacao;
- grupo semantico;
- conceito semantico;
- nivel semantico;
- finalidade semantica.

O campo `valor_nominal` preserva os valores monetarios tal como declarados. Nenhuma deflacao ou conversao per capita e aplicada nesta etapa.

### Painel largo

`painel_semantico_municipio_ano.parquet` transforma os conceitos em colunas, mantendo nas linhas municipio, ano, estagio e natureza da operacao. Esse produto prepara o calculo de indicadores, series temporais, comparacoes territoriais e mapas.

### Linhagem

`linhagem_agregados_semanticos.parquet` registra os codigos e identificadores que compoem cada agregado. A linhagem permite reconstruir o valor calculado, localizar a conta original e auditar a confianca do mapeamento.

## Prevencao de dupla contagem

A etapa nao soma indiscriminadamente todas as correspondencias semanticas. Cada conceito e processado segundo sua finalidade. Correspondencias complementares de grupos distintos permanecem disponiveis, mas cada indicador futuro devera declarar explicitamente quais conceitos e grupos utiliza.

## Limitacoes atuais

Os valores ainda sao nominais. A deflacao para junho de 2026, os calculos per capita e os indicadores compostos serao implementados em etapas posteriores.

Os codigos historicos ainda nao mapeados permanecem na fila de pendencias do mapa semantico e nao sao incorporados silenciosamente aos agregados.

## Validacao esperada

A etapa deve ser considerada aprovada quando:

- houver agregados gerados;
- os municipios e anos esperados estiverem presentes;
- nenhum conceito for somado duas vezes para o mesmo registro;
- a linhagem reproduzir os valores da base longa;
- conceitos de totalizacao utilizarem apenas a selecao de totalizacao;
- conceitos analiticos utilizarem apenas a selecao de decomposicao.
