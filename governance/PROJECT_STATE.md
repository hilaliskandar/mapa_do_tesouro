# Estado do projeto

Data de referência: 2026-10-09.

## Estado operacional

A `main` é a fonte de verdade.

O baseline TIC-TIM 30 permanece preservado como referência de regressão e rollback. A produção pública vigente é estadual e multiuniverso na release `v0.4.0`, com API editorial estática v1 para boletins fiscais.

O estado operacional é `sp645_publication_api_live_v0_4_0`: a release `v0.4.0` está publicada, o workflow `SP645 Pages Production` foi aprovado no run `37917365471` e o QA remoto da URL principal passou. O painel expõe 13 universos analíticos; a camada editorial publica 11 universos, com 287 contextos município × universo.

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

## Estado após P2.3

A rota estadual de preview foi incorporada à `main` pelo PR #124.

- workflow: `SP645 Pages Candidate Preview`;
- gatilho: somente `workflow_dispatch`;
- alias padrão: `sp645-candidate`;
- QA dedicado: `deployment/qa_sp645_pages.py`;
- produção e alias `preview` estável permanecem intocados;
- `VERSION` permanece `0.1.1`.

A próxima ação é operacional e manual: executar o workflow estadual, validar o preview remoto e somente então reconsiderar promoção pública.

## SP645 em produção

Em 2026-10-09, o workflow manual `SP645 Pages Production` foi executado para a release `v0.2.0` e concluído com sucesso.

- workflow run: `37892171501`;
- commit executado: `e8e12b64e311b0243b7e637ee5bcc2244e6499a7`;
- release: `v0.2.0`;
- artifact: `11597769314`;
- artifact SHA-256: `44f6eced73970f99651d055586c027349a98cd78a082f943d1fceffa3e1a0c4c`;
- 645 municípios;
- 271 linhas de cobertura;
- QA local SP645: aprovado;
- deploy de produção: aprovado;
- QA remoto SP645: aprovado;
- URL de produção: `https://finbra-tic-tim-referencia.pages.dev`.

O universo estadual SP645 passa a ser a produção publicada. A release v0.2.0 permanece como referência congelada desta promoção.

## Universos territoriais metropolitanos

Em 2026-10-09 foi catalogada a composição 2025 de nove regiões metropolitanas paulistas e da Aglomeração Urbana de Franca, totalizando 10 universos e 255 municípios distintos.

O modelo canônico já suporta sobreposição por meio de `universo` e `universo_municipio`; os dados fiscais municipais permanecem únicos.

O cruzamento por código IBGE demonstrou que `TIC_TIM_30` é composto por todos os 20 municípios da RM de Campinas, todos os 7 municípios da RM de Jundiaí e Caieiras, Francisco Morato e Franco da Rocha, os três pertencentes à Sub-região Norte da RMSP.

Artefatos: `data/catalogs/territorial_universes_sp_2025.yml`, `data/catalogs/territorial_overlap_tictim30_2025.csv`, `data/catalogs/tictim30_territorial_decomposition_2025.csv` e `governance/TERRITORIAL_UNIVERSES_SP_2025.md`.

O próximo passo funcional é permitir seleção de universo territorial no frontend e recalcular estatísticas relativas, tipologias, marcadores e pares para o universo selecionado.


## Produção multiuniverso v0.3.1

Em 2026-10-09, a release `v0.3.1` foi promovida com sucesso à produção.

- workflow: `SP645 Pages Production`;
- run: `37912565493`;
- commit/tag: `159499fe5562a375cb1503f57e1675fc5ce01563` / `v0.3.1`;
- artifact: `11607452418`;
- artifact SHA-256: `7c15dc53da4fbd1b6c1914ded47816b2c8f3867ba47b185c6dc0d6e6fb1262cd`;
- QA local: aprovado;
- deploy: aprovado;
- QA remoto: aprovado;
- produção: `https://finbra-tic-tim-referencia.pages.dev`;
- universos publicados: 13;
- `SP_645`: 645 municípios;
- `TIC_TIM_30`: 30 municípios;
- `CIDADES_MEDIAS`: 33 municípios;
- 9 regiões metropolitanas;
- `AU_FRANCA`: 19 municípios.

A `v0.3.1` não altera dados em relação à `v0.3.0`; corrige apenas a robustez do QA remoto durante a propagação do Cloudflare Pages.


## API editorial v0.4.0 em produção

Em 2026-10-09, a release `v0.4.0` foi promovida à produção.

- workflow: `SP645 Pages Production`;
- run: `37917365471`;
- commit/tag: `27f2b5056cbba56a9075a18b51013acbee597cea` / `v0.4.0`;
- artifact: `11610521760`;
- artifact SHA-256: `3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e`;
- QA local: aprovado;
- deploy: aprovado;
- QA remoto: aprovado;
- produção: `https://finbra-tic-tim-referencia.pages.dev`;
- base da API: `/data/api/v1`;
- 11 universos editoriais;
- 287 contextos município × universo;
- RMSP editorial: 38 municípios, com São Paulo excluída;
- Cidades Médias: 33 municípios, mantendo sobreposição deliberada com RM/AU.

As fontes das Skills `boletim-fiscal-municipal` e `boletim-fiscal-universo` estão versionadas em `skills/`.

## Retomada 2026-10-14 — gate editorial

A leitura da `main` confirmou a release pública registrada `v0.4.0`, com 13 universos analíticos, 11 editoriais e 287 contextos município × universo. A documentação do ciclo fiscal está consolidada em `governance/EDITORIAL_PILOT_PLAN_2026_10_14.md`. A próxima etapa é conferir o índice `/data/api/v1/publication/universes.json`, validar `context.json` e produzir um caderno-piloto para um universo editorial, proposto inicialmente como RM de Jundiaí. Não declarar dados públicos validados, edição finalizada ou publicada sem verificação dos payloads. O estado mais recente deste registro prevalece sobre instruções históricas de P0/P1/P2 anteriores à v0.4.0.

## Recuperação do artefato editorial — 2026-10-14

O ZIP do artifact GitHub Actions `11610521760`, release `v0.4.0`, run `37917365471`, foi recuperado e teve SHA-256 conferido: `3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e`. O índice interno contém 11 universos editoriais e soma 287 contextos; a contagem de JSONs municipais no ZIP é exatamente 287. O piloto `RM_JUNDIAI` contém 7 municípios e 50 variáveis no contexto, com série de 2025 e dados auditáveis. O endpoint público segue não verificado ao vivo. O campo `qa_status` do payload permanece `candidate` e exige conciliação editorial, embora o workflow de publicação esteja registrado como aprovado. Uma minuta quantitativa foi gerada em ambiente de análise; não foi publicada.

## Atualizacao editorial 2026-10-14

Artefato v0.4.0 recuperado do GitHub Actions (ID 11610521760), com integridade verificada. Para RM_JUNDIAI foram conferidos os sete contextos municipais e as 50 variaveis no contexto regional. Foi elaborada minuta analitica 0.2 com series 2021-2025 e CSV de auditoria. Nota metodologica: series historicas derivadas podem existir mesmo quando as contas DCA primarias nao aparecem na API editorial do mesmo ano. Despesa territorial strict_complete possui cobertura de 1/7 em 2025. Publicacao externa nao realizada. Revisar historicidade, proveniencia e QA antes de aprovar a edicao.

## Auditoria editorial quantitativa — RM Jundiai, 2026-10-14

Foram auditadas 42 comparacoes de seis indicadores relativos para os sete municipios em 2025: 35 paridades aritmeticas, zero divergencias calculaveis e sete nao testaveis por ausencia do agregado intermediario `tributos_imobiliarios` na API editorial. Evidencia: `governance/QA_EDITORIAL_RM_JUNDIAI_2026_10_14.md`. Foi elaborada minuta analitica 0.3 com fichas municipais, sem publicacao. Auditoria de serie historica 2021-2024 continua pendente por falta dos componentes primarios no JSON editorial.

## Saneamento dos PRs em 2026-10-15

PR #166 incorporado por squash, commit `38b9ff67148335949bb0bde47fa9eb3238632b7e` (fonte bruta Gate A para auditoria). PR #167 incorporado por squash, commit `aed6572a365dcc698d147ad6de29f8a55c1a84cc` (evidencia bruta de ausencias DCA I-E 2025). Ambos tiveram Core CI e Pages Preview aprovados nos respectivos commits antes da incorporacao. Consulta posterior: nenhuma issue aberta e somente PR #143 aberto, em rascunho. O PR #143 requer QA editorial e de publicacao antes de merge; a producao v0.4.0 nao foi deliberadamente alterada por deploy nesta etapa. Nao inferir zero das linhas funcionais ausentes. Data da atualizacao: 2026-10-15.

## Revisão PR 143 — 2026-10-15

O PR #143 continua em rascunho, sem merge e sem alteração da publicação estadual. Artefato TCESP RMJ `11680818755` recuperado, contendo 14 extrações 2023–2024 sem erros. O CSV DCA histórico do Drive (`1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`) foi obtido diretamente. A comparação independente entre investimento liquidado da DCA e totais TCESP em centavos aprovou **14/14 casos, zero divergências**. Evidência metodológica: `editorial/rmj/QA_PR143_INTEGRACAO_2026_10_15.md`, no ramo do PR. Os workflows do PR incluem 23 municípios complementares, mas a extração não é requisito da produção regular FINBRA. Permanecem pendentes validação do HTML, QA independente do preview, reconciliação do contrato editorial de 11 vs 12 universos, eventual deflação documentada e aprovação editorial antes de merge.

## Ajuste do fluxo de QA editorial RMJ — 2026-10-15

O workflow especifico `RMJ Editorial Preview` na branch do PR #143 foi simplificado no commit `5bd75808a899d66970a19295c5cf2f3e821ddc81`. A extracao TCESP repetitiva foi removida do caminho critico, preservando o teste offline de formato, validacao HTML/JS, deploy isolado Cloudflare, QA Playwright desktop e celular, capturas e verificacao HTTP. As 14 conciliacoes TCESP x DCA previamente aprovadas permanecem registradas no caderno `editorial/rmj/QA_PR143_INTEGRACAO_2026_10_15.md` do ramo. CI geral estava em fila/execucao na ultima consulta; NAO afirmar gate Playwright aprovado sem evidence de job e results.json. PR #143 permanece em rascunho; producao estadual preservada.

## QA funcional do boletim RMJ aprovado — 2026-10-15

PR #143 continua aberto/em rascunho para revisao editorial e decisao de publicacao. O workflow Pages Preview run `38688538329` foi concluido com os dois jobs aprovados, `build-deploy-qa` e `rmj-browser-qa`. A evidencia Playwright foi recuperada do artifact ID `11950979797`, que contem `rmj-desktop.png`, `rmj-mobile.png`, `results.json`. Testes executados em 1366x900 e 390x844: 23 secoes, 7 perfis, 5 linhas historicas, 8 linhas de cruzamento, 5 tendencias, 5 linhas IPCA, 4 indicadores legais, conteudo dinamico carregado, nenhum erro JavaScript e nenhum overflow horizontal nos dois tamanhos. Gate funcional aprovado, com evidencia real e sem Browserless. As 14 reconciliacoes TCESP/DCA anteriores e auditoria do IPCA permanecem validas. Producao principal sem merge nem alteracao.

## RMJ PR #143 — aprovacao tecnica integral da ultima revisao 2026-10-15

Ramo editorial no commit `b2e34892ea3ebfa78868b87bf0cf80d94c5f6b94`: Core CI run `38691253732` e Pages Preview run `38691253722`, ambos `success`. Jobs `rmj-browser-qa` e `build-deploy-qa` aprovados. Artifact Playwright ID `11952755020` inspecionado: desktop 1366x900 e mobile 390x844, 23 secoes, 7 perfis, 5 linhas historicas, 8 cruzamentos, 5 linhas IPCA, 4 linhas legais, sem overflow horizontal e sem erros JS nos dois tamanhos. Preview remoto atualizado com linguagem voltada ao publico externo. Auditoria anterior 14/14 TCESP/DCA e IPCA 60 registros preservada. **Pendente somente decisao de governanca/editorial sobre promover/mesclar PR #143 e publicar definitivamente**; nenhum merge ou alteracao da producao principal foi efetuado nesta revisao.

## Encerramento do PR #143 — 15/10/2026

O PR #143 foi promovido de rascunho para revisao e **integrado a `main`** via squash merge no commit `f8f390250de3fe9f2df3a8cf4fbfdc00f30db28f`; GitHub confirmou estado `closed` e `merged=true`. Ultima revisao antes do merge: Core CI `38691253732` e Pages Preview `38691253722` aprovados; o job `rmj-browser-qa` concluiu com sucesso e artifact Playwright ID `11952755020` (desktop e celular) foi recuperado e auditado. Conciliacoes TCESP x DCA 2023-2024: 14/14 exatas. Medias anuais IPCA 2021-2025 validadas contra 60 registros SIDRA/IBGE. HTML publico integrado em `editorial/rmj/index.html`; preview isolado disponivel em `https://rmj-piloto.finbra-tic-tim-referencia.pages.dev/` e consultado apos merge. **Publicacao definitiva no endereco principal: nao comprovada**. As afirmacoes historicas de que PR estava aberto ou sem merge descrevem o estado da epoca e ficam superadas por este registro. Proxima etapa: decidir e verificar o endereco editorial definitivo e o mecanismo de publicacao sem modificar automaticamente a API/base estadual existente.

## Publicacao independente RMJ confirmada — 15/10/2026

Projeto Cloudflare Pages `financas-rmj` criado na conta existente, com `production_branch=main`, sem substituicao do projeto estadual `finbra-tic-tim-referencia`. Workflow GitHub `.github/workflows/publish-rmj.yml` criado na main pelo commit `a68569beb65741a0174ce112eb554bf9bc5e228d`; publica apenas `editorial/rmj/index.html` e `_headers` depois das verificacoes estruturais. API Cloudflare confirmou deploy no projeto `financas-rmj` com estado `success` e URL de deploy `https://fcf06794.financas-rmj.pages.dev`. URL definitiva `https://financas-rmj.pages.dev/` consultada via Crawl2AI em 2026-10-15: titulo e conteudo RMJ recuperados, texto público sem aviso de piloto/versao interna, fontes DCA presentes. Publicacao definitiva confirmada; revalidar a cada nova alteracao de `editorial/rmj/index.html` pelos controles previstos. Manter dominios e ciclos de publicacao estadual e RMJ separados.

## Composicao percentual das contas RMJ publicada — 2026-10-15

PR #169 (`editorial/rmj-composicao-20261015`) criado, aprovado no Core CI run `38701345394` e Pages Preview run `38701345346`, com job `rmj-browser-qa` concluido com sucesso; promovido e integrado por squash commit `ae2fea93337dce3cd86a7fe6a7d978c396eebaec`. A secao publica de contas agora mostra participacao percentual de cada receita selecionada sobre receita corrente bruta e de cada despesa selecionada sobre despesa total liquidada; na RMJ, calcula-se a razao entre somas dos sete municipios, respeitando cobertura integral e valores ausentes. Publicacao automatica Cloudflare `financas-rmj` confirmada por deploy `https://7e6aa273.financas-rmj.pages.dev` status success, e consulta direta `https://financas-rmj.pages.dev/` retornou texto novo 'Participação no total de referência' e metodologia de agregacao regional. Nao foi alterado o projeto estadual.

## Comparacao fiscal RMJ publicada — 15/10/2026

PR #170 promovido e integrado por squash commit `366e6baa1e14e933c6d108b0cce7aefd6bcc9d7f`. Core CI run `38702178603` e Pages Preview run `38702178622` aprovados, com job `rmj-browser-qa` success e evidencias em artifact `11956244681`. Adicionada ao boletim tabela comparativa selecionavel por ano (2021-2025) dos sete municipios e agregado RMJ, contendo participacao tributaria na receita corrente bruta, investimentos na despesa total liquidada e despesas correntes na despesa total liquidada. Metodo regional: proporcao entre somas, sem fazer media de percentuais; ausencia de informacao impede calculo. Cloudflare Pages `financas-rmj` confirmou deploy de producao `https://c8b5a32a.financas-rmj.pages.dev` em estado success; extracao direta do endereco principal `https://financas-rmj.pages.dev/` confirmou publicacao do titulo 'Como varia a estrutura fiscal entre os municípios?' e respectivo texto metodologico. Producao estadual preservada.

## Evolucao nominal e real das contas RMJ — publicada em 15/10/2026

PR #171 integrado a `main` pelo squash commit `b51b50c7ff48b2d64f87c037dc385c6a25942f64`. Core CI run `38706872551` e Pages Preview run `38706872642` concluiram com `success`; `rmj-browser-qa` validou interacoes desktop/celular, incluindo tabela de evolucao e troca de municipio. A secao 'O que mudou de 2021 a 2025?' apresenta variacao nominal, variacao real corrigida pelo IPCA medio anual e mudanca em pontos percentuais da participacao tributaria na receita corrente e de investimentos/despesas correntes na despesa total liquidada. O agregado regional usa somas completas dos sete municipios e nao imputa dados faltantes. Cloudflare `financas-rmj` registrou deploy de producao `https://cec78d8c.financas-rmj.pages.dev` com status success. Extracao direta de `https://financas-rmj.pages.dev/` confirmou nova secao e explicacoes metodologicas no conteudo publico. Projeto estadual preservado.

## Sinteses municipais interpretativas RMJ publicadas — 15/10/2026

O PR #172 foi integrado por squash commit `e62971f87aa0802b063b022a45b9385825ea43ed`, apos Core CI run `38709492532` e Pages Preview run `38709492266` terminarem em sucesso, incluindo `rmj-browser-qa` com verificacao interativa das sinteses municipais em desktop e celular. A nova secao publica 'Sete trajetórias fiscais em perspectiva' gera texto individual para sete municipios com evolucao real 2021-2025 de receita corrente, tributaria, investimentos e despesas correntes, e mudancas de suas participacoes. Nao atribui causas ou resultados fisicos sem evidencias complementares. Projeto Cloudflare `financas-rmj` registrou deploy de producao `https://4f7ced74.financas-rmj.pages.dev` com estado `success`; leitura do endereco principal `https://financas-rmj.pages.dev/` confirmou secao e ressalva contra inferencia causal. O painel estadual nao foi alterado.

## Auditoria de completude editorial RMJ — 15/10/2026

PR #173 integrado por squash merge `284b115ec43f5d6f68e5caadb7c750e6ca4a6b6d`, após Core CI `38712237448` e Pages Preview `38712237396` aprovados, incluindo Playwright. Novo inventario `editorial/rmj/AUDITORIA_COMPLETUDE_COHERENCIA_2026_10_15.md` classifica cobertura existente e lacunas reais. Corrigida contradição na seção investigacao: programa 2025 identificado nos sete municípios; ações destacadas em Jundiaí; o que falta é atribuição interanual e investigação por contratos/obras, não iniciar programa/ação de zero. Deploy Cloudflare `https://1995d0b9.financas-rmj.pages.dev` success; site canônico de publicação `https://financas-rmj.pages.dev/` inspecionado e texto novo presente. Recomenda-se impedir novas frentes de indicadores sem checagem prévia do inventario. Projeto estadual não alterado.
