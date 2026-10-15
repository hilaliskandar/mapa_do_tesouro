# Pendências operacionais

Atualizado em 2026-10-09.

Este arquivo é a fila canônica de tarefas do projeto. Ele não substitui issues do GitHub: uma tarefa só deve virar issue quando houver escopo executável, critério de aceite e dependências definidas.

## Prioridade P0 — saneamento e regressão

### P0.1 — Reconstruir build privado SP645 pós-RGF02

Status: concluído em 2026-10-09. Gate F aprovado; referência detalhada em `governance/QA_GATE_F_P0_2026_10_09.md`.

Objetivo: gerar novo artefato privado estadual usando o estado multifuentes mais recente, incluindo o RGF Anexo 02 pós-processado e os suplementos fill-only aprovados.

Critérios de aceite:
- 645 municípios presentes;
- nenhum valor observado sobrescrito por suplemento;
- ausência preservada como ausência;
- hashes de entrada e saída registrados;
- artifact privado reproduzível;
- sem alteração do painel público.

Dependências: PRs #103–#107 já incorporados.

### P0.2 — Regressão completa contra TIC_TIM_30

Status: concluído em 2026-10-09. Paridade aprovada; cinco diferenças CAPAG classificadas como revisão oficial de snapshot, sem regressão.

Objetivo: comprovar que a expansão estadual não introduziu regressões no baseline publicado.

Critérios de aceite:
- 30/30 municípios presentes;
- comparação de todos os campos comuns;
- diferenças classificadas entre atualização oficial, mudança metodológica e regressão;
- zero regressões não explicadas;
- registro de SHA-256 e relatório de QA.

### P0.3 — Regressão funcional do frontend F101–F118

Status: concluído em 2026-10-09. A lacuna F116 foi saneada pela issue #110 e PR #111; Core CI, Pages Preview e rebuild estadual posteriores ficaram verdes.

Objetivo: impedir perda silenciosa de funcionalidades aprovadas.

Critérios de aceite:
- Panorama, perfil, séries, comparação e mapa funcionais;
- receitas, despesas, território, dívida/liquidez e CAPAG funcionais;
- catálogos de contas e indicadores disponíveis;
- crosswalk, fontes/cobertura e metodologia acessíveis;
- exportação aberta funcional;
- documentação canônica de cada variável/indicador acessível;
- comportamento de NA/zero validado.

## Prioridade operacional atual

A produção multiuniverso foi concluída em 2026-10-09 com a release `v0.3.1`. O workflow `SP645 Pages Production` terminou verde no run `37912565493` e o QA remoto da URL principal foi aprovado. Não há gate de publicação pendente.

## Prioridade P1 — consolidação analítica

### P1.1 — Atualizar cobertura multifuentes

Status: concluído em 2026-10-09. A cobertura canônica agora contempla quatro estados, é recomposta após as transformações e possui visão separada por fonte. Relatório: `governance/P1_1_MULTISOURCE_COVERAGE_SP645.md`.

Consolidar cobertura por variável, fonte, ano e universo. Diferenciar observado, ausente, não aplicável e em revisão.

### P1.2 — Recalcular derivados afetados

Status: concluído em 2026-10-09. As issues #117 e #118 foram encerradas após confirmação da regra `absence_is_not_zero`; nenhuma imputação adicional foi autorizada e não houve novos derivados a recalcular.

Recalcular apenas indicadores cujo conjunto de insumos mudou com as novas cargas. Indicadores legais devem continuar ligados aos demonstrativos próprios.

### P1.3 — Recalcular tipologias e pares quando aplicável

Status: concluído em 2026-10-09. Como P1.2 não alterou a observabilidade, não houve necessidade de novo recálculo; permanecem válidos 440 municípios elegíveis a pares e 1.320 posições prioritárias.

Executar somente se novos insumos alterarem marcadores observáveis. Preservar regra mínima de cobertura e não criar pares artificiais para municípios sem informação suficiente.

## Prioridade P2 — release estadual candidata

### P2.1 — Gerar manifesto da candidata

Status: concluído em 2026-10-09. Manifesto privado criado em `data/catalogs/sp645_candidate_2026_10_09.yml`, sem alteração de `VERSION` e sem promoção pública.

Registrar versão de dados, schema, metodologia, aplicação, timestamp e hashes.

### P2.2 — Validar checklist de promoção

Status: concluído em 2026-10-09. Evidências consolidadas em `governance/QA_P2_2_SP645_CANDIDATE.md`; rollback documentado em `deployment/ROLLBACK.md`.

Executar integralmente `governance/QA_CHECKLIST.md`, incluindo segurança, rollback e reprodução local.

### P2.3 — Decidir promoção

Status: concluído em 2026-10-09. O preview estadual isolado foi aprovado, a release `v0.2.0` foi criada e o workflow `SP645 Pages Production` foi executado com sucesso, incluindo QA remoto.

Somente após P0 e P1 concluídos. A produção TIC_TIM_30 permanece intocada até decisão explícita.

## Higiene de GitHub

Situação observada em 2026-10-09:

- issues abertas: 0;
- pull requests abertos: 0;
- PRs até #124 incorporados;
- issues #110, #113, #115, #117, #118, #121 e #123 encerradas;
- não há PR encalhado ou issue aberta a sanear.

Política:

1. não abrir issue apenas para documentar estado;
2. abrir issue para falha reproduzível, decisão pendente ou tarefa executável;
3. cada issue deve conter escopo, dependências e critério de aceite;
4. PR deve referenciar a tarefa/issue correspondente quando houver;
5. branch superada deve ser encerrada após merge ou substituição explícita;
6. documentação canônica deve ser atualizada no mesmo ciclo da mudança técnica.

## Ordem recomendada

`P0.1 → P0.2 → P0.3 → P1.1 → P1.2 → P1.3 → P2.1 → P2.2 → P2.3`
## Pós-release v0.3.1

A release estadual multiuniverso `v0.3.1` está congelada e publicada. O workflow manual `SP645 Pages Production` foi executado no run `37912565493` com sucesso. O QA remoto aprovou a URL principal de produção. `SP_645` permanece como universo padrão; TIC_TIM_30, CIDADES_MEDIAS, nove regiões metropolitanas e AU_FRANCA estão disponíveis como recortes analíticos sobrepostos.

## Prioridade atual após release v0.4.0 — 2026-10-14

As seções anteriores sobre v0.3.1 e os gates P0/P1/P2 são históricas: conforme `PROJECT_STATE.md`, a versão v0.4.0 e a API editorial v1 já foram promovidas em 2026-10-09. A fila ativa é:

- [ ] E1.1 Validar `publication/universes.json`: 11 universos editoriais, publicação e contagem de contextos (287), metadados de build e disponibilidade pública.
- [ ] E1.2 Identificar `publication_id` da RM de Jundiaí e validar o contexto de universo e os arquivos municipais com os scripts já versionados.
- [ ] E1.3 Produzir o caderno-piloto com síntese regional, receitas, despesas, território, dívida, liquidez, CAPAG e fichas municipais, somente onde houver valores observados.
- [ ] E1.4 Conferir cada afirmação quantitativa contra os JSONs e documentar cobertura, período, fontes, versões e lacunas.
- [ ] E1.5 Revisar metodologia e redação; arquivar manifesto e SHA-256; decidir sobre aprovação editorial.
- [ ] E2 Congelar o modelo aprovado e expandir aos outros dez universos.

Contrato, metodologia e aceite: `governance/EDITORIAL_PILOT_PLAN_2026_10_14.md`. Nenhuma publicação editorial foi autorizada automaticamente por esta atualização.

## Andamento E1 — 2026-10-14

- [x] E1.1a Integridade do pacote de publicação: SHA-256 confere, 11 universos e 287 arquivos municipais confirmados.
- [ ] E1.1b Disponibilidade HTTP pública e validação remota: não comprovadas no ambiente.
- [x] E1.2a Identificado `RM_JUNDIAI`, conferidos sete membros e 50 variáveis no contexto.
- [x] E1.3a Produzida minuta quantitativa interna para 2025; não publicada.
- [ ] E1.3b Completar caderno narrativo e fichas com trajetórias e fontes por indicador.
- [ ] E1.4 Rodar validação automatizada de todas as fichas, consistência de escalas, cobertura e QA editorial.
- [ ] E1.5 Conciliar `qa_status=candidate` nos JSONs com aprovação externa da release antes de promover a edição.

## Continuação do caderno-piloto — 2026-10-14

A release `v0.4.0` foi recuperada diretamente do artifact GitHub Actions ID `11610521760` (run `37917365471`), SHA-256 `3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e`. Foram efetivamente inspecionados o índice editorial, `RM_JUNDIAI/context.json` e os sete JSONs municipais. O índice registra 11 universos e soma 287 posições município × universo; o contexto `RM_JUNDIAI` contém 50 variáveis e 7 municípios.

Uma segunda minuta analítica foi produzida, com quadros de 2025, séries 2021–2025 de indicadores selecionados, CSV de auditoria e advertência sobre a disponibilidade dos indicadores derivados em contraste com as contas DCA primárias (ausentes dos payloads editoriais anteriores a 2025). O agregado territorial `strict_complete` tem cobertura de apenas 1/7 em 2025. A minuta permanece sem publicação externa.

Próximas tarefas: validar numeradores e denominadores históricos contra dados primários; revisar o status interno `qa_status=candidate` à luz do QA da release pública; conferir rastreabilidade do texto editorial; aprofundar as fichas municipais antes de promover o caderno. Não presumir que o ZIP local persista em novos ambientes, mas recuperá-lo pelo workflow/artifact ID acima.

### Etapa E1 — progresso de 2026-10-14

- [x] Recuperar artefato original da release v0.4.0 por GitHub Actions e confirmar SHA-256.
- [x] Identificar RM_JUNDIAI, sete municipios e 50 variaveis no contexto editorial.
- [x] Auditar razoes de 2025: 35/35 testaveis reconciliadas; sete sem agregado intermediario acessivel.
- [x] Elaborar minuta comparativa 0.3 e sete fichas descritivas, ainda nao publicadas.
- [ ] Recompor proveniencia das razoes historicas 2021-2024 nas fontes primarias.
- [ ] Expor/reconciliar agregado tributos_imobiliarios para o QA dos sete casos restantes.
- [ ] Revisar diferenca entre escala armazenada e formula do catalogo.
- [ ] Validar o significado de qa_status=candidate e o snapshot CAPAG.
- [ ] Aprovar caderno somente apos reconciliacao e revisao editorial.

## Saneamento dos PRs em 2026-10-15

PR #166 incorporado por squash, commit `38b9ff67148335949bb0bde47fa9eb3238632b7e` (fonte bruta Gate A para auditoria). PR #167 incorporado por squash, commit `aed6572a365dcc698d147ad6de29f8a55c1a84cc` (evidencia bruta de ausencias DCA I-E 2025). Ambos tiveram Core CI e Pages Preview aprovados nos respectivos commits antes da incorporacao. Consulta posterior: nenhuma issue aberta e somente PR #143 aberto, em rascunho. O PR #143 requer QA editorial e de publicacao antes de merge; a producao v0.4.0 nao foi deliberadamente alterada por deploy nesta etapa. Nao inferir zero das linhas funcionais ausentes. Data da atualizacao: 2026-10-15.

## Revisão PR 143 — 2026-10-15

O PR #143 continua em rascunho, sem merge e sem alteração da publicação estadual. Artefato TCESP RMJ `11680818755` recuperado, contendo 14 extrações 2023–2024 sem erros. O CSV DCA histórico do Drive (`1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`) foi obtido diretamente. A comparação independente entre investimento liquidado da DCA e totais TCESP em centavos aprovou **14/14 casos, zero divergências**. Evidência metodológica: `editorial/rmj/QA_PR143_INTEGRACAO_2026_10_15.md`, no ramo do PR. Os workflows do PR incluem 23 municípios complementares, mas a extração não é requisito da produção regular FINBRA. Permanecem pendentes validação do HTML, QA independente do preview, reconciliação do contrato editorial de 11 vs 12 universos, eventual deflação documentada e aprovação editorial antes de merge.

## Ajuste do fluxo de QA editorial RMJ — 2026-10-15

O workflow especifico `RMJ Editorial Preview` na branch do PR #143 foi simplificado no commit `5bd75808a899d66970a19295c5cf2f3e821ddc81`. A extracao TCESP repetitiva foi removida do caminho critico, preservando o teste offline de formato, validacao HTML/JS, deploy isolado Cloudflare, QA Playwright desktop e celular, capturas e verificacao HTTP. As 14 conciliacoes TCESP x DCA previamente aprovadas permanecem registradas no caderno `editorial/rmj/QA_PR143_INTEGRACAO_2026_10_15.md` do ramo. CI geral estava em fila/execucao na ultima consulta; NAO afirmar gate Playwright aprovado sem evidence de job e results.json. PR #143 permanece em rascunho; producao estadual preservada.

## Encerramento do PR #143 — 15/10/2026

O PR #143 foi promovido de rascunho para revisao e **integrado a `main`** via squash merge no commit `f8f390250de3fe9f2df3a8cf4fbfdc00f30db28f`; GitHub confirmou estado `closed` e `merged=true`. Ultima revisao antes do merge: Core CI `38691253732` e Pages Preview `38691253722` aprovados; o job `rmj-browser-qa` concluiu com sucesso e artifact Playwright ID `11952755020` (desktop e celular) foi recuperado e auditado. Conciliacoes TCESP x DCA 2023-2024: 14/14 exatas. Medias anuais IPCA 2021-2025 validadas contra 60 registros SIDRA/IBGE. HTML publico integrado em `editorial/rmj/index.html`; preview isolado disponivel em `https://rmj-piloto.finbra-tic-tim-referencia.pages.dev/` e consultado apos merge. **Publicacao definitiva no endereco principal: nao comprovada**. As afirmacoes historicas de que PR estava aberto ou sem merge descrevem o estado da epoca e ficam superadas por este registro. Proxima etapa: decidir e verificar o endereco editorial definitivo e o mecanismo de publicacao sem modificar automaticamente a API/base estadual existente.

## Publicacao independente RMJ confirmada — 15/10/2026

Projeto Cloudflare Pages `financas-rmj` criado na conta existente, com `production_branch=main`, sem substituicao do projeto estadual `finbra-tic-tim-referencia`. Workflow GitHub `.github/workflows/publish-rmj.yml` criado na main pelo commit `a68569beb65741a0174ce112eb554bf9bc5e228d`; publica apenas `editorial/rmj/index.html` e `_headers` depois das verificacoes estruturais. API Cloudflare confirmou deploy no projeto `financas-rmj` com estado `success` e URL de deploy `https://fcf06794.financas-rmj.pages.dev`. URL definitiva `https://financas-rmj.pages.dev/` consultada via Crawl2AI em 2026-10-15: titulo e conteudo RMJ recuperados, texto público sem aviso de piloto/versao interna, fontes DCA presentes. Publicacao definitiva confirmada; revalidar a cada nova alteracao de `editorial/rmj/index.html` pelos controles previstos. Manter dominios e ciclos de publicacao estadual e RMJ separados.
