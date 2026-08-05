# Versao 0.6.1 — fechamento do mapa semantico

## Finalidade

A versao 0.6.1 fecha as lacunas identificadas antes do uso dos agregados semanticos como resultados analiticos. O aperfeicoamento ocorre automaticamente no inicio da etapa de agregacao.

## Correcoes historicas

Os codigos historicos `2.5.0.0.00.00.00` e `2.5.9.0.00.00.00`, observados ate 2017, passam a ser associados a `REV_OUTRAS_RECEITAS_CAPITAL`. A correcao preserva o codigo e a descricao originais e registra `origem_ajuste_semantico = regra_historica_2_5_ate_2017`.

## Compatibilidade entre conceitos

A matriz de compatibilidade examina os conceitos atribuídos ao mesmo registro. Conceitos pertencentes a grupos semanticos distintos sao considerados complementares. Conceitos diferentes dentro do mesmo grupo sao tratados como concorrentes e impedem a agregacao automatica ate revisao.

Esse controle evita somar indiscriminadamente correspondencias multiplas, como uma transferencia corrente geral e uma transferencia especifica.

## Componentes tributarios

A versao cria uma matriz especifica para IPTU, ISS e ITBI, discriminando:

- principal;
- divida ativa;
- multas e juros;
- multas e juros da divida ativa.

A matriz informa ano, codigo, descricao, quantidade de registros, municipios e valor absoluto de auditoria.

## Produtos

A pasta do mapa semantico passa a receber:

```text
registros_qualificados_semanticos_aperfeicoados.parquet
matriz_compatibilidade_semantica.parquet
matriz_componentes_tributarios.parquet
relatorio_consistencia_semantica.xlsx
resultado_aperfeicoamento_semantico.json
```

## Integracao com agregacoes

`agregar_conceitos_semanticos` executa o fechamento antes de calcular os agregados. Incompatibilidades no mesmo grupo interrompem a etapa. Registros ainda nao mapeados produzem `aprovado_com_alertas`.

A linhagem dos agregados inclui a origem do ajuste semantico, permitindo distinguir regras originais e correcoes historicas.
