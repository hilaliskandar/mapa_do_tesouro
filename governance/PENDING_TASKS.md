# Pendências operacionais

Atualizado em 2026-10-09.

Este arquivo é a fila canônica de tarefas do projeto. Ele não substitui issues do GitHub: uma tarefa só deve virar issue quando houver escopo executável, critério de aceite e dependências definidas.

## Prioridade P0 — saneamento e regressão

### P0.1 — Reconstruir build privado SP645 pós-RGF02

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

Objetivo: comprovar que a expansão estadual não introduziu regressões no baseline publicado.

Critérios de aceite:
- 30/30 municípios presentes;
- comparação de todos os campos comuns;
- diferenças classificadas entre atualização oficial, mudança metodológica e regressão;
- zero regressões não explicadas;
- registro de SHA-256 e relatório de QA.

### P0.3 — Regressão funcional do frontend F101–F118

Status: em saneamento. A lacuna F116 foi identificada e tratada na issue #110; a conclusão depende do CI e merge da correção.

Objetivo: impedir perda silenciosa de funcionalidades aprovadas.

Critérios de aceite:
- Panorama, perfil, séries, comparação e mapa funcionais;
- receitas, despesas, território, dívida/liquidez e CAPAG funcionais;
- catálogos de contas e indicadores disponíveis;
- crosswalk, fontes/cobertura e metodologia acessíveis;
- exportação aberta funcional;
- documentação canônica de cada variável/indicador acessível;
- comportamento de NA/zero validado.

## Prioridade P1 — consolidação analítica

### P1.1 — Atualizar cobertura multifuentes

Consolidar cobertura por variável, fonte, ano e universo. Diferenciar observado, ausente, não aplicável e em revisão.

### P1.2 — Recalcular derivados afetados

Recalcular apenas indicadores cujo conjunto de insumos mudou com as novas cargas. Indicadores legais devem continuar ligados aos demonstrativos próprios.

### P1.3 — Recalcular tipologias e pares quando aplicável

Executar somente se novos insumos alterarem marcadores observáveis. Preservar regra mínima de cobertura e não criar pares artificiais para municípios sem informação suficiente.

## Prioridade P2 — release estadual candidata

### P2.1 — Gerar manifesto da candidata

Registrar versão de dados, schema, metodologia, aplicação, timestamp e hashes.

### P2.2 — Validar checklist de promoção

Executar integralmente `governance/QA_CHECKLIST.md`, incluindo segurança, rollback e reprodução local.

### P2.3 — Decidir promoção

Somente após P0 e P1 concluídos. A produção TIC_TIM_30 permanece intocada até decisão explícita.

## Higiene de GitHub

Situação observada em 2026-10-09:

- issues abertas: 0;
- pull requests abertos: 0;
- PRs #96–#107: merged;
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