# Decisão metodológica — agregado territorial

## Status

**Aprovada em 2026-10-06.**

Regra canônica: `strict_complete`.

## Definição

```text
despesa_territorial =
    Urbanismo
  + Habitação
  + Saneamento
  + Gestão Ambiental
  + Transporte
```

O agregado somente é calculado quando os cinco componentes estão observados.

Se qualquer componente estiver ausente, o agregado permanece `NA`.

## Evidência

O caderno metodológico da frente FINBRA/DCA estabelece como regras permanentes:

- ausência não é zero;
- valores parciais permanecem identificados como parciais;
- indicadores derivados só são promovidos quando todos os componentes exigidos estão presentes;
- esforço territorial possui cobertura estrita limitada;
- camadas parciais não devem ser promovidas automaticamente.

Na matriz bruta de despesa por função:

- existem 28 funções de despesa liquidada;
- foram observadas 6.138 células não vazias nessas funções;
- não existe zero explícito entre essas células;
- para as cinco funções territoriais, 85 dos 390 pares município-ano têm todos os componentes;
- 304 pares possuem combinação parcial de 1 a 4 componentes.

Portanto, não há base metodológica suficiente para transformar automaticamente ausência de uma função em zero.

## Regra legada

O Bloco 3 v0.7 usava:

```excel
=IF(COUNT(Urbanismo,Habitação,Saneamento,Gestão Ambiental,Transporte)=0,
   "",
   SUM(Urbanismo,Habitação,Saneamento,Gestão Ambiental,Transporte))
```

Essa regra é preservada como `legacy_partial` exclusivamente para:

- reprodução histórica;
- testes de regressão;
- comparação com tipologias e pares antigos.

Ela não é a regra canônica do novo núcleo.

## Impacto

A mudança de `legacy_partial` para `strict_complete` altera a cobertura da dimensão territorial e, consequentemente, algumas tipologias e pares municipais.

Isso é uma mudança metodológica documentada, não uma regressão de software.

## Governança

Nenhum frontend, API ou exportação poderá recalcular o agregado territorial por conta própria. Todos devem consumir o valor produzido pelo pipeline canônico.
