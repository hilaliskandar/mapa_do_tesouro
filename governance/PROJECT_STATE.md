# Estado do projeto

Data de referência: 2026-10-09.

## Estado operacional

A `main` é a fonte de verdade.

O baseline público TIC-TIM 30 permanece publicado e protegido por CI, QA de paridade e contratos metodológicos.

A expansão estadual está no estado `p2_candidate_manifest_ready`: DCA 2013–2025, RREO 2025, CAPAG 2025, RGF 01/05 2025, RGF 02 2025, histórico RGF 2023–2024, tipologias/pares e cartografia SP645 já possuem artefatos e QA documentados. O foco imediato é recompor o build privado estadual com o RGF02 pós-processado e executar regressão funcional completa antes de qualquer promoção pública.

## Hierarquia de fontes operacionais

O acervo FINBRA/DCA no Google Drive é a fonte operacional preferencial para reconstrução histórica e processamento em lote:

`https://drive.google.com/drive/folders/1K_Raj0pKEyktVY5BVa_raOZ4cQdJ8HQ4`

O Siconfi externo deve ser usado para:

- validação por amostra;
- complementação incremental de lacunas;
- atualização posterior ao snapshot local;
- auditoria independente.

Não se deve repetir coleta estadual completa quando existir snapshot local adequado.

## Baseline público

- universo: `TIC_TIM_30`;
- período: 2013–2025;
- release funcional: v0.1.1;
- produção: `https://finbra-tic-tim-referencia.pages.dev`;
- preview: `https://preview.finbra-tic-tim-referencia.pages.dev`;
- metodologia territorial: `strict_complete`.

## SP_645

### Gate A — aprovado

A aquisição estadual independente de 2025 foi concluída:

- 645 municípios solicitados;
- 1.935 respostas brutas;
- zero falhas;
- 645 linhas normalizadas;
- 26 variáveis;
- zero issues;
- SHA-256 normalizado `619367dd8b2c5b3db6f7a6c902b41e2f2685616cf8560e2e852e7583f386eec7`.

### Gate B — série histórica caracterizada

Os anexos locais I-C, I-D e I-E foram inspecionados para todos os exercícios de 2013 a 2025.

A cardinalidade mínima anual na interseção dos três anexos é:

- 2013: 638;
- 2014: 625;
- 2015: 643;
- 2016: 643;
- 2017: 645;
- 2018: 643;
- 2019: 642;
- 2020: 645;
- 2021: 645;
- 2022: 644 no snapshot anual; I-C complementado localmente para 645;
- 2023: 645;
- 2024: 630 no snapshot anual; I-C complementado localmente para 645;
- 2025 local: 632;
- 2025 Gate A: 645.

O normalizador aceita CSV e XLSX locais, registra hashes, cobertura e códigos faltantes.

A fonte suplementar local de receitas foi validada empiricamente:

- 2022/Guaraçaí: 9 células preenchidas, zero conflitos, SHA-256 composto `387b61416817db342f94c86759811000ef40a627320308651ccd6e34cec7d9d0`;
- 2024/15 municípios: receitas estruturais e população presentes em 15/15, SHA-256 do suplemento `6638fece3b2849c5c24295787f32f68ea499df2eee3e418386cdf3638f6391b2`.

A primeira complementação seletiva externa foi executada para 2018:

- Anhumas (`3502408`) e Monte Aprazível (`3531407`);
- 6 respostas consultadas: 2 municípios × 3 anexos;
- zero falhas de requisição;
- os seis payloads retornaram `items=[]`;
- SHA-256 do delta normalizado `5e9aba6ee6d627eceeddd1e7648be8bd4abfe5476a34a339dd39da2ad2dd9a79`;
- decisão: preservar as lacunas como ausência confirmada da fonte atual, sem novas tentativas automáticas.

A segunda complementação seletiva externa foi executada para 2015:

- Ferraz de Vasconcelos (`3515707`) e Tanabi (`3553401`);
- 6 pares município–anexo consultados;
- zero falhas de requisição;
- os seis payloads retornaram `items=[]`;
- SHA-256 do delta normalizado `b4e0e5df5329a7eb0883914711103f870f5973049aafc9fe114db4bf735f1178`;
- decisão: classificar 2015 como `source_confirmed_absence` e retirar da fila automática.


### Crosswalk temporal concluído para receitas centrais

Foram comprovados diretamente nos arquivos locais quatro regimes:

- 2013: códigos antigos + `Receitas Realizadas`;
- 2014–2017: códigos antigos + `Receitas Brutas Realizadas`;
- 2018–2021: códigos intermediários + `Receitas Brutas Realizadas`;
- 2022+: códigos atuais + `Receitas Brutas Realizadas`.

As variantes estão explicitadas no mapping canônico. As despesas centrais permanecem no mesmo contrato observado.

### Automação e resoluções recentes

A fila seletiva do Gate B opera automaticamente em lote. Ausências confirmadas são encerradas sem nova consulta; o lote para quando recupera dados que exigem composição fill-only.

Resultados já consolidados:

- 2013, 2015, 2016, 2018 e 2019: `source_confirmed_absence`;
- 2022: resolvido por suplemento local de receitas;
- 2024: `resolved_composite_fill_only`, 645 linhas, zero conflitos, SHA-256 `81804ece28290ddaec5360b1ff57059fbb3f53ceb15e466c940f4db467f68c63`;
- 2024 está armazenado no Drive e no R2 privado em `sp_645/dca/2024/normalized.csv`.

## Gate B DCA — concluído

A série estadual canônica contém:

- 645 municípios por exercício;
- 2013–2025;
- 8.385 município-ano;
- 26 variáveis;
- zero issues de normalização;
- SHA-256 multianual `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`;
- Drive file ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`;
- R2 `sp_645/dca/2013_2025/normalized.csv`;
- manifesto R2 `sp_645/dca/2013_2025/manifest.json`.

A fila seletiva DCA está vazia. As lacunas não recuperáveis em 2013, 2014, 2015, 2016, 2018 e 2019 foram confirmadas por consulta seletiva ao Siconfi e permanecem como ausência.

## Gate C — contratos multifuentes definidos

As fontes legais passam a ser tratadas separadamente:

- RREO Anexo 03, período 6: RCL anual oficial;
- RGF Anexo 01, 3º quadrimestre: DTP, denominador legal e percentual oficial;
- RGF Anexo 05: caixa e restos a pagar, com comparabilidade direta a partir de 2019;
- RGF Anexo 02: taxonomia oficial preservada;
- CAPAG: classificação oficial por snapshot, com posição e ano-base distintos.

O DCA permanece fonte analítica e não substitui declarações legais dessas fontes.

## Gate C — progresso consolidado

### RREO 2025

- 645/645 consultas concluídas;
- 531 RCL observadas;
- 114 ausências;
- zero falhas;
- zero issues;
- SHA-256 normalizado `d66d92bd8b75e319d0c6bb432961e791f2c5ad10d25f197b3a10db512ed75ba3`.

### CAPAG 2025

- snapshot oficial posição setembro de 2026;
- 645/645 municípios paulistas;
- suplemento local RGF/CAPAG catalogado para reduzir deltas externos.

### RGF 2025

- Anexos 01/05: carga estadual concluída para 645/645 municípios;
- zero falhas de aquisição;
- zero issues de normalização;
- base API SHA-256 `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`;
- composição fill-only com CAPAG local: 366 células adicionais, zero conflitos;
- composto SHA-256 `48b50b2df44eaddc2fc1c4ed096c057c2bea5d61cb850b37dc23e6037962aa24`;
- DTP, RCL legal e percentual oficial permanecem 530/645 e não recebem suplemento;
- caixa bruta não vinculada sobe para 635/645;
- RP liquidados anteriores: 478/645;
- RP liquidados do exercício: 501/645;
- RP não liquidados anteriores: 490/645;
- demais obrigações: 108/645;
- caixa líquida antes/depois RPNP permanece 528/645;
- fallback shardado permanece como contingência;
- Anexo 02: carga estadual concluída; 530 municípios observados, 43.920 linhas longas, 40 códigos de conta, zero falhas e zero conflitos;
- SHA-256 canônico do Anexo 02 `8e4709727aa8fbf0023056982fe7927f5bd8e323354807604dbdc2a91cf8d75a`;
- suplemento CAPAG fill-only adiciona 100 Dívidas Consolidadas e 114 RCL brutas, zero conflitos;
- composto RGF02 SHA-256 `0b31196dd1a692632b7c2b48a044ed64f5f56493eb8d50f818810cdd583fc139`.

## Base multifuentes canônica 2025

A base integrada SP645 2025 foi materializada e armazenada no Drive:

- file ID `12XfaN7ati-wGgw_a5puwechp7ipFdWRG`;
- 645 municípios;
- 64 campos;
- SHA-256 `ffd626cfde3fa1c79d7a552d5b3a8ad2e3509dce5efcc9c62c39eb76c3796566`.

A prontidão dos indicadores foi medida por interseção real dos insumos, preservando ausência.

## Gate D — indicadores 2025 calculados

O artefato privado de indicadores contém 645 municípios e 25 indicadores:

- Drive file ID `1wYnFB8Dg000qrBM1do8pe083FlqWzHDk`;
- SHA-256 `adb9b5b6abbd3f439f3b39cc356522d21430de74117de4bf9ca1589c40e9c161`;
- indicadores fiscais DCA: 641–644 municípios;
- DTP/RCL: 530;
- DC/RCL: 476;
- DCL/RCL: 530;
- caixa após RPNP/RCL: 528;
- CAPAG I1/I2/I3: 645;
- indicadores territoriais strict_complete: 65.

## Paridade TIC-TIM 30 — 2025

A build estadual foi comparada diretamente ao baseline multifuentes TIC-TIM 30:

- 30/30 municípios presentes;
- 55 campos comuns;
- 54/55 campos em paridade integral;
- única diferença substantiva: nota final CAPAG em 5 municípios;
- as cinco diferenças correspondem a revisão oficial entre `CAPAG Ano Base 2025` e a `Prévia da CAPAG` de setembro de 2026;
- regressões detectadas: zero.

## Gate E — histórico mínimo aprovado

O histórico RGF 2023–2024 corrigido contém:

- 1.290 município-ano;
- DTP/RCL legal 2023 em 527/645 e 2024 em 530/645;
- dívida consolidada e DCL preservadas do histórico original;
- SHA-256 `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`.

A paridade histórica contra o baseline TIC-TIM 30 foi aprovada:

- 30 municípios;
- 60 chaves município-ano;
- 420 comparações;
- zero divergências.

## Gate E — tipologias e pares em QA privado

A entrada SP645 2021–2025 contém 3.225 linhas.

Classificação com pelo menos três anos:

- base tributária: 645;
- investimento: 645;
- territorial: 56;
- DTP: 505;
- DC: 439;
- DCL: 505;
- liquidez: 0.

Pares:

- 440 municípios com pelo menos quatro marcadores;
- 205 sem par elegível;
- 1.320 posições prioritárias;
- 40 pares principais recíprocos.

Artifact privado no Drive: `1zA0zNM_pYzkMk88XttNi17on6w_l98__`.

## Cartografia estadual validada

A geometria web pinada contém 645 Polygons e corresponde exatamente ao universo SP645 por código IBGE.

Ela está aprovada para visualização do painel. Como o GeoJSON não declara CRS, análises métricas continuam reservadas a camadas com CRS explícito, preferencialmente EPSG:4674.

## Gate F — P0 aprovado

Em 2026-10-09, o ciclo P0 foi encerrado:

- P0.1 rebuild privado SP645 pós-RGF02: aprovado;
- P0.2 regressão contra TIC_TIM_30: aprovada, zero regressões;
- P0.3 regressão funcional F101–F118: aprovada após saneamento de F116;
- issue #110 encerrada pelo PR #111;
- commit de integração F116: `256ecdaa64ddc38f0ccd7a8d38dbbab7cc588e5f`;
- Gate F pós-merge: run `37884817757`, aprovado;
- artifact privado: ID `11596071795`, SHA-256 `97bfb257191862e176ad779d323187974ecf9434dc3e4c960cc94a2fb395c3f7`;
- 645 municípios, 645 geometrias, 440 municípios elegíveis a pares, 1.320 posições prioritárias e 11.501 células Gate D comparadas.

Detalhes em `governance/QA_GATE_F_P0_2026_10_09.md`.

## Próximo gate operacional

1. P1.1 — consolidar cobertura multifuentes por variável, fonte, exercício e universo, preservando observado, ausente, não aplicável e em revisão;
2. P1.2 — recalcular somente indicadores derivados afetados por novos insumos válidos;
3. P1.3 — recalcular tipologias e pares somente se a observabilidade mudar;
4. P2 — preparar candidata estadual, manifesto e checklist de promoção;
5. manter a produção pública TIC_TIM_30 intocada até decisão explícita de release.

## P1.1 — cobertura multifuentes concluída

Em 2026-10-09, a cobertura estadual foi consolidada após as transformações:

- 645 municípios;
- 271 combinações variável × ano;
- quatro estados canônicos de cobertura;
- zero linhas implícitas classificadas como ausência no rebuild de referência;
- `coverage.json` para cobertura final;
- `coverage_sources.json` para contribuição por fonte;
- histórico 2021–2024 classificado como histórico mínimo, não base estadual completa;
- relatório detalhado em `governance/P1_1_MULTISOURCE_COVERAGE_SP645.md`.

A prioridade passa a P1.2: verificar a semântica das lacunas em contas esparsas e recalcular somente os derivados cuja ampliação de cobertura seja metodologicamente demonstrável.

## P2.1 — manifesto da candidata

Em 2026-10-09 foi criado o manifesto privado da candidata estadual em `data/catalogs/sp645_candidate_2026_10_09.yml`.

O manifesto registra universo SP_645, período 2021–2025, commits de referência, workflow, artifact, SHA-256, cobertura, paridade e política de não publicação.

`VERSION` permanece `0.1.1`; portanto, nenhum workflow de release foi acionado por esta etapa.

A prioridade atual é P2.2: executar integralmente `governance/QA_CHECKLIST.md`, com evidência de segurança, reprodutibilidade e rollback, antes de qualquer decisão de release.

## P2.3 — decisão de promoção

O fluxo público atual não é apto a promover SP645 porque `pages-preview.yml`, `pages-production.yml`, `deployment/materialize_preview.py` e `deployment/qa_pages.py` estão contratualmente ligados ao baseline TIC_TIM_30.

A decisão é não promover produção neste estado. Foi criada uma rota manual e isolada de preview estadual em `.github/workflows/pages-sp645-candidate.yml`, validada por `deployment/qa_sp645_pages.py` e protegida por teste de contrato.

O workflow só pode ser acionado por `workflow_dispatch`, usa alias separado e não altera `VERSION`, `preview` estável ou produção automaticamente.

A próxima decisão de release depende de executar esse preview manual e aprovar seu QA remoto.
