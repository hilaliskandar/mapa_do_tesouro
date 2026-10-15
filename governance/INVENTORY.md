# Inventário canônico

Atualizado em 2026-10-09.

## Núcleo aprovado

### Dados e modelo

- schema SQLite versionado;
- modelo longo de observações;
- estados `observado`, `ausente`, `nao_aplicavel` e `em_revisao`;
- tabelas de proveniência;
- crosswalk temporal;
- cobertura;
- documentação de variáveis e seções metodológicas;
- estatísticas de janela;
- classificações relativas;
- pares municipais.

### Baseline TIC_TIM_30

- 30 municípios;
- 2013–2025;
- 75 objetos documentados;
- 29.250 observações após derivados na build de referência;
- 870 pares dirigidos;
- 30 geometrias;
- regra territorial `strict_complete`;
- paridade documentada contra painel v7 e Bloco 3;
- releases v0.1.0 e v0.1.1;
- produção e preview no Cloudflare Pages.

### Frontend

- Panorama;
- Perfil/seleção municipal;
- séries históricas;
- comparação;
- mapa temático;
- análises de receitas;
- despesas e investimento;
- território;
- dívida e liquidez;
- CAPAG;
- catálogo de contas e agregações;
- indicadores;
- crosswalk;
- fontes e cobertura;
- metodologia;
- modal “Como ler”.

### CI/CD

- Core CI;
- preview automático;
- QA remoto;
- promoção controlada de produção;
- smoke estadual Siconfi;
- crosscheck Siconfi versus baseline;
- piloto SP 645;
- contrato de snapshot privado.

## Expansão SP_645

### Piloto validado

- 645 municípios;
- 2020–2023;
- 2.580 município-ano;
- 5 variáveis de receita;
- 12.900 observações;
- 12.900 registros de proveniência;
- snapshot comprimido no R2 privado;
- SHA-256 comprimido: `3f5ebf5a6482b7627cd2c1bd121c722e53e2632fed2340ae5ccae7e02290088a`;
- objeto: `sp_645/pilot_2020_2023/snapshot.csv.gz`.

### Aquisição direta disponível

- DCA I-C, I-D e I-E;
- RREO Anexo 03 / RCL anual;
- RGF Anexos 01 e 05 com normalização legal;
- RGF Anexo 02 em formato longo;
- retries exponenciais;
- preservação de artefatos brutos;
- manifestos;
- hashes;
- normalização estadual;
- execução RGF shardada de contingência;
- QA estadual automático pós-run.

## Decisões consolidadas

- `despesa_territorial = strict_complete`;
- fórmula parcial territorial é apenas `legacy_partial`;
- DTP/RCL, DC/RCL e DCL/RCL permanecem oficiais, não proxies;
- cobertura é variável a variável;
- flags estruturais legadas não provam completude;
- Engenheiro Coelho/2024 permanece ausente em DCA;
- `dca_fpm_cota_mensal` significa cota mensal e exclui cotas extraordinárias.

## Material legado relevante

- aplicação Streamlit;
- normalização histórica;
- hierarquia contábil;
- mapa semântico;
- agregações semânticas;
- cartografia histórica;
- testes de reconciliação;
- painéis HTML anteriores;
- v7 e Bloco 3 como baselines analíticos/documentais.

## Ramos superados encerrados

Os PRs #18 e #20 foram encerrados sem merge porque suas funções foram substituídas pela linha posterior já integrada à `main`.

## Gate B DCA concluído

- 645 municípios;
- 2013–2025;
- 8.385 município-ano;
- 26 variáveis;
- zero issues de normalização;
- snapshot multianual SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`;
- arquivo canônico no Drive;
- snapshot e manifesto no R2 privado;
- fila seletiva histórica encerrada;
- ausências históricas confirmadas preservadas como ausência.

## Gate C — estado atual

### RREO 2025

- 645/645 municípios consultados;
- 531 RCL observadas;
- 114 ausências preservadas;
- zero falhas;
- zero issues de normalização;
- cobertura da variável: 82,33%;
- as 114 ausências têm RCL em outra fonte oficial, mas não são imputadas ao RREO.

### CAPAG 2025

- snapshot oficial posição setembro de 2026;
- 645/645 municípios paulistas;
- classificação oficial preservada, inclusive `n.d.`;
- suplemento local RGF/CAPAG catalogado variável a variável.

### RGF

- Anexos 01/05: carga SP645 2025 concluída em 645/645;
- zero falhas e zero issues;
- composição CAPAG fill-only validada com 366 células adicionais e zero conflitos;
- SHA-256 composto `48b50b2df44eaddc2fc1c4ed096c057c2bea5d61cb850b37dc23e6037962aa24`;
- fallback automático em cinco shards disponível;
- consolidação e QA automáticos em ambos os caminhos;
- Anexo 02: carga estadual 2025 concluída; 530 municípios observados, 43.920 linhas longas, 40 códigos de conta, zero falhas e zero conflitos; SHA-256 canônico `8e4709727aa8fbf0023056982fe7927f5bd8e323354807604dbdc2a91cf8d75a`; suplemento CAPAG fill-only adiciona 100 Dívidas Consolidadas e 114 RCL brutas, zero conflitos; composto SHA-256 `0b31196dd1a692632b7c2b48a044ed64f5f56493eb8d50f818810cdd583fc139`.

## Pendências estruturais

1. reconstruir o build privado SP645 após a correção do pós-processamento do RGF Anexo 02;
2. executar regressão final de dados e interface contra TIC-TIM 30;
3. recalcular somente indicadores, tipologias e pares afetados por novos insumos válidos;
4. fechar a documentação de cobertura multifuentes por variável e exercício;
5. validar integralmente F101–F118, inclusive mapa, exportação, crosswalk, fontes e metodologia;
6. registrar manifesto, hashes e versão da candidata estadual;
7. manter a promoção pública bloqueada até QA integral e decisão explícita de release.

## Higiene do repositório

Situação em 2026-10-09:

- issues abertas: 0;
- pull requests abertos: 0;
- PRs #96–#107 incorporados à `main`;
- nenhuma pendência conhecida depende de fechamento manual de issue ou PR;
- tarefas futuras devem nascer de `governance/PENDING_TASKS.md` e só virar issue quando houver escopo executável, critério de aceite e dependências definidas.

## Gate F — P0 concluído

- rebuild privado SP645 pós-RGF02 aprovado;
- paridade TIC_TIM_30 preservada, zero regressões;
- requisitos F101–F118 auditados;
- F116 implementado como exportação CSV do recorte anual;
- Core CI: 132 testes aprovados no PR #111;
- Pages Preview: build, deploy e validação remota aprovados;
- novo build estadual privado aprovado no run `37884817757`;
- artifact ID `11596071795`, SHA-256 `97bfb257191862e176ad779d323187974ecf9434dc3e4c960cc94a2fb395c3f7`;
- fila corrente: P1.1, cobertura multifuentes.

## Atualização do inventário — 2026-10-14

- Estado de referência: `main` do repositório; versão pública informada `v0.4.0` (2026-10-09).
- Plataforma publicada segundo manifesto: 13 universos analíticos; camada editorial estática v1 para 11 universos; 287 contextos município × universo.
- Fontes documentais para a continuidade: `README.md`, `CHANGELOG.md`, `governance/PROJECT_STATE.md`, `governance/PENDING_TASKS.md`, `skills/boletim-fiscal-municipal/SKILL.md`, `skills/boletim-fiscal-universo/SKILL.md`, respectivos `references/api.md` e `references/editorial.md`.
- Novo artefato de governança: `governance/EDITORIAL_PILOT_PLAN_2026_10_14.md`.
- Baseline `TIC_TIM_30` preservado; nenhuma nova transformação de dados ou reconstrução dos snapshots foi executada nesta retomada.
- Pendência editorial: aferir integridade do índice e dos contextos da API, produzir e validar caderno-piloto, congelar modelo editorial antes da expansão a 11 universos.
- As seções antigas denominadas 'Pendências estruturais' registram o histórico de trabalho, não constituem fila ativa após as releases v0.2.0–v0.4.0.

## Evidência quantitativa recuperada — 2026-10-14

- Artifact oficial v0.4.0: ID `11610521760`; ZIP de 9,5 MiB aproximadamente, 2.566 entradas; SHA-256 `3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e`.
- Índice `data/api/v1/publication/universes.json`: 11 universos editoriais; soma das cardinalidades 287; arquivos municipais encontrados 287.
- Contexto `data/api/v1/publication/universes/RM_JUNDIAI/context.json`: sete municípios (Cabreúva, Campo Limpo Paulista, Itupeva, Jarinu, Jundiaí, Louveira e Várzea Paulista); 50 variáveis.
- Build `multifuentes-v0.4-cef702e5edbd`, versão de dados `sp645-private-site-2021-2025-v1`; metadado interno `qa_status=candidate` requer esclarecimento antes de qualquer selo editorial definitivo.
- Documento de trabalho não publicado: `caderno_piloto_fiscal_rm_jundiai_2026.md` gerado a partir do artefato, com síntese 2025, cobertura e fichas municipais resumidas.

## Continuação do caderno-piloto — 2026-10-14

A release `v0.4.0` foi recuperada diretamente do artifact GitHub Actions ID `11610521760` (run `37917365471`), SHA-256 `3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e`. Foram efetivamente inspecionados o índice editorial, `RM_JUNDIAI/context.json` e os sete JSONs municipais. O índice registra 11 universos e soma 287 posições município × universo; o contexto `RM_JUNDIAI` contém 50 variáveis e 7 municípios.

Uma segunda minuta analítica foi produzida, com quadros de 2025, séries 2021–2025 de indicadores selecionados, CSV de auditoria e advertência sobre a disponibilidade dos indicadores derivados em contraste com as contas DCA primárias (ausentes dos payloads editoriais anteriores a 2025). O agregado territorial `strict_complete` tem cobertura de apenas 1/7 em 2025. A minuta permanece sem publicação externa.

Próximas tarefas: validar numeradores e denominadores históricos contra dados primários; revisar o status interno `qa_status=candidate` à luz do QA da release pública; conferir rastreabilidade do texto editorial; aprofundar as fichas municipais antes de promover o caderno. Não presumir que o ZIP local persista em novos ambientes, mas recuperá-lo pelo workflow/artifact ID acima.

### QA editorial adicional (2026-10-14)

Novo registro `governance/QA_EDITORIAL_RM_JUNDIAI_2026_10_14.md`: artefato de origem 11610521760, 42 comparacoes de formulas de 2025, 35 conferidas, sete nao testaveis, zero divergencias calculaveis. Minuta analitica v0.3 com sete fichas municipais gerada em ambiente de trabalho. A minuta nao constitui publicacao oficial. Regra de exibicao percentual e lacunas das contas historicas constam do registro.

## Saneamento dos PRs em 2026-10-15

PR #166 incorporado por squash, commit `38b9ff67148335949bb0bde47fa9eb3238632b7e` (fonte bruta Gate A para auditoria). PR #167 incorporado por squash, commit `aed6572a365dcc698d147ad6de29f8a55c1a84cc` (evidencia bruta de ausencias DCA I-E 2025). Ambos tiveram Core CI e Pages Preview aprovados nos respectivos commits antes da incorporacao. Consulta posterior: nenhuma issue aberta e somente PR #143 aberto, em rascunho. O PR #143 requer QA editorial e de publicacao antes de merge; a producao v0.4.0 nao foi deliberadamente alterada por deploy nesta etapa. Nao inferir zero das linhas funcionais ausentes. Data da atualizacao: 2026-10-15.

## Revisão PR 143 — 2026-10-15

O PR #143 continua em rascunho, sem merge e sem alteração da publicação estadual. Artefato TCESP RMJ `11680818755` recuperado, contendo 14 extrações 2023–2024 sem erros. O CSV DCA histórico do Drive (`1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`) foi obtido diretamente. A comparação independente entre investimento liquidado da DCA e totais TCESP em centavos aprovou **14/14 casos, zero divergências**. Evidência metodológica: `editorial/rmj/QA_PR143_INTEGRACAO_2026_10_15.md`, no ramo do PR. Os workflows do PR incluem 23 municípios complementares, mas a extração não é requisito da produção regular FINBRA. Permanecem pendentes validação do HTML, QA independente do preview, reconciliação do contrato editorial de 11 vs 12 universos, eventual deflação documentada e aprovação editorial antes de merge.

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
