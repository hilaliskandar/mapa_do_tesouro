# Gate C — integração multifuentes estaduais

Data de abertura: 2026-10-08.

## Objetivo

Integrar RREO, RGF e CAPAG ao universo SP645 sem degradar os contratos legais já validados no baseline TIC-TIM 30.

O Gate B DCA está concluído. O Gate C passa a tratar demonstrativos legais como objetos próprios, e não como derivação do DCA.

## Evidência local já validada

### RREO — RCL

A base local `FINBRA_RCL_OFICIAL_2015_2025` contém 33 municípios por exercício, 2015–2025, todos com status `OK`.

Contrato observado:

- anexo: RREO-Anexo 03;
- período: 6;
- conta: `ReceitaCorrenteLiquida`;
- linha: `RECEITA CORRENTE LÍQUIDA (III) = (I - II)`;
- coluna: `TOTAL (ÚLTIMOS 12 MESES)`.

### RGF — Anexo 01

A série local TIC-TIM 30 cobre 2015–2025.

Conceitos canônicos já validados:

- `DESPESA_TOTAL_PESSOAL`;
- `RCL_DENOMINADOR_LEGAL`;
- `DTP_PERCENTUAL_RCL`.

Regra temporal do denominador:

- 2015–2017: RCL limite legal;
- 2018+: RCL ajustada.

O percentual oficial do RGF deve prevalecer quando disponível.

### RGF — Anexo 05

A estrutura é comparável de forma direta a partir de 2019.

A regra já validada é usar a linha oficial de total para caixa, e não somar sublinhas manualmente.

Anos anteriores a 2019 permanecem preservados com sua vigência própria e não devem ser forçados à taxonomia 2019+.

### RGF — Anexo 02

A base local preserva taxonomia oficial, coluna, valor, população, fonte e URL.

Cobertura TIC-TIM 30:

- 2015: 27/30;
- 2016–2022: 30/30;
- 2023: 30/30 após retry;
- 2024–2025: 30/30.

### CAPAG

O acervo contém:

- snapshot oficial `capag-municipios-posicao-2026-set.xlsx`;
- ano-base 2025;
- posição setembro de 2026;
- base canônica TIC-TIM 30 derivada desse snapshot.

A classificação oficial prevalece sobre reconstruções locais.

## Regra central

Indicadores legais não serão calculados por proxy quando existe declaração oficial no RREO, RGF ou CAPAG.

Exemplo já comprovado: o grupo 3.1 liquidado do DCA capta universo orçamentário mais amplo e superestima a DTP legal. Portanto:

- DCA 3.1 pode ser mantido para análise estrutural;
- não pode substituir a DTP do RGF;
- não pode ser usado para verificar limite legal de pessoal.

## Ordem de expansão SP645

1. RREO Anexo 03, período 6, RCL anual;
2. RGF Anexo 01, 3º quadrimestre, Poder Executivo municipal;
3. RGF Anexo 05, com série comparável 2019+;
4. RGF Anexo 02, preservando taxonomia oficial;
5. CAPAG oficial;
6. denominadores complementares;
7. composição multifuentes e paridade contra TIC-TIM 30.

## Critério de aceite

Cada fonte estadual deve possuir:

- universo esperado e observado;
- ano/período/anexo explícitos;
- artefatos brutos ou snapshot oficial;
- hash;
- cobertura variável a variável;
- ausência preservada;
- regra temporal documentada;
- sentinelas de paridade com TIC-TIM 30;
- nenhuma alteração automática do painel público.

## Estado

`gate_c_contracts_defined`

O próximo trabalho não é coletar tudo indiscriminadamente. É localizar snapshots locais estaduais equivalentes, quando existirem, e usar aquisição externa apenas para lacunas ou validação.
