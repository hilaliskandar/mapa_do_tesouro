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

A fila corrente aguarda **execução manual do preview SP645 isolado** pelo workflow `SP645 Pages Candidate Preview`. P0 e P1 estão encerrados; P2.1–P2.3 estão decididos e a promoção pública permanece bloqueada até o QA remoto desse preview.

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

Status: decisão técnica registrada em 2026-10-09. A candidata SP645 não deve usar o fluxo público atual, pois ele materializa o snapshot TIC_TIM_30 já publicado. A estratégia aprovada é disponibilizar primeiro um preview estadual manual e isolado, sem alterar `VERSION`, o alias `preview` estável ou a produção. A promoção pública só pode ser reconsiderada após QA desse preview.

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