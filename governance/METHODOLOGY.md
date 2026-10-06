# Metodologia — princípios consolidados

Este documento consolida princípios herdados do `mapa_do_tesouro` e do trabalho FINBRA/TIC-TIM atual.

## Princípios

- preservar dados brutos e proveniência;
- não transformar ausência em zero;
- não alterar silenciosamente valores declarados;
- distinguir contas sintéticas e terminais;
- evitar dupla contagem entre conta-pai e contas-filhas;
- manter estágios contábeis separados;
- separar dados oficiais, agregações analíticas, indicadores derivados e classificações oficiais;
- registrar mudança classificatória como possível quebra de série;
- tratar indicadores legais a partir dos demonstrativos próprios;
- apresentar valores absolutos, per capita e relativos conforme a natureza da variável;
- usar rankings e pares como instrumentos comparativos, não como juízo normativo.

## Pipeline lógico

```text
ingest
→ validate
→ normalize
→ classify
→ hierarchy
→ harmonize
→ aggregate
→ indicators
→ coverage
→ build
→ QA
→ publish
```

## Universo inicial

A base nasce estadual. `TIC_TIM_30` é o primeiro universo analítico operacional, não uma limitação estrutural.
