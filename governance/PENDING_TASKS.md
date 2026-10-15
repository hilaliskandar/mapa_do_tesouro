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
