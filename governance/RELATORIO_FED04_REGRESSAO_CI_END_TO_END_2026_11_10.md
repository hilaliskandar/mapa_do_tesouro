# FED04 — Regressão CI e proteção ponta a ponta da publicação fiscal

**Emissão:** 10/11/2026. **Estado:** testes Core CI e escala aprovados na branch; Pages Preview sob verificação; PR **#232 em rascunho**, sem merge.

## 1. Escopo e mudanças da branch

Branch [`fed04-catalog-safety-20261110`](https://github.com/hilaliskandar/mapa_do_tesouro/tree/fed04-catalog-safety-20261110), PR [#232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232):

1. `pipeline/build/load_catalog.py`: carrega `publicavel` e `ativo` quando explicitamente fornecidos; preserva os estados em caso de omissão no catálogo; valida opções 0/1.
2. `pipeline/build/export_publication_api.py`: seleção de variáveis editoriais exige `publicavel=1 AND ativo=1`. Se o catálogo editorial referenciar variável bloqueada, a exportação falha antes de criar arquivos de divulgação. Evita contorno indireto das flags.
3. `tests/test_fed04_catalog_flags.py`: testes de carregamento, idempotência e proteção de visão `v_observacao_publicavel`.
4. `tests/test_export_publication_api.py`: regressão adicional para seleção editorial com `(publicavel,ativo)=(0,1),(1,0),(0,0)`.
5. `tests/test_fed04_integracao_sp645_isolada.py`: fixture sintético de **645 municípios** em SQLite descartável, quatro variáveis fiscais candidatas com valores, uma variável basal com 645 observações. Compara `v_observacao_publicavel`, `export_state_api_v2` e `export_regional_api_v2`, com garantia de não exposição de valores candidatos.
6. `.github/workflows/pages-preview.yml`: fixa **Ubuntu 24.04** exclusivamente no job `rmj-browser-qa`, pois Playwright 1.56.1 não suporta o Ubuntu 26.04 do runner `ubuntu-latest` usado em 10/11/2026. Alteração operacional de CI, sem mudança no frontend.

## 2. Execuções e diagnóstico

| GitHub Actions | Run ID | Resultado verificado |
|---|---:|---|
| Core CI, após correção inicial do carregador | [42813873201](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42813873201) | **194 testes aprovados** |
| SP 645 Scale Test inicial | [42813873217](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42813873217) | **Sucesso** |
| Pages Preview inicial | [42813873245](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42813873245) | **Falha apenas no job `rmj-browser-qa`**; build, deploy, testes e validação da prévia do job `build-deploy-qa` aprovados |
| Core CI após proteção editorial | [42816902639](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42816902639) | **195 testes aprovados** |
| Core CI após correção de fixture do teste SP645 | [42817420446](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42817420446) | **196 testes aprovados** |
| SP 645 Scale Test após correção | [42817420459](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42817420459) | **Sucesso** |
| Pages Preview após pinagem de Ubuntu 24.04 | [42817420434](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42817420434) | **Em execução na última consulta registrada neste relatório; verificar conclusão antes de homologar** |

### Falha intermediária — diagnosticada e corrigida no fixture

Uma rodada anterior `42817230713` terminou com **195 testes aprovados e um teste novo reprovado**, porque a base de ensaio não cadastrara `fonte_id='SICONFI_DCA'` antes de inserir variáveis candidatas com chave estrangeira. Isso era **defeito de preparação da fixture sintética**, não problema fiscal do SQLite de produção. A fonte foi cadastrada no teste e a execução `42817420446` aprovou **196/196**.

### Falha de navegador — causa comprovada

O log do job `129821876987`, no run `42813873245`, informa: `Playwright does not support chromium on ubuntu26.04-x64`. A instalação do Chromium foi interrompida antes dos testes de interação. A pinagem do runner do job RMJ em `ubuntu-24.04` é uma correção candidata com confirmação de CI pendente. **Não atribuir a falha ao carregador DCA ou a dados da API**.

## 3. Contratos de publicação examinados

- **SQL `v_observacao_publicavel`:** filtra por `publicavel=1`; não filtra `ativo`. A flag `publicavel=0` é indispensável.
- **API estadual v2:** filtra valores por `publicavel=1 AND ativo=1`; mantém **metadados** de variáveis bloqueadas no catálogo público com `api_available=false`, conforme contrato já testado em `tests/test_export_state_api_v2.py`. Esse comportamento não revela valores; se a intenção de produto for ocultar inclusive nomes/códigos candidatos, será necessária alteração e versionamento adicional de contrato.
- **API regional v2:** filtra valores e variáveis por `publicavel=1 AND ativo=1`; teste sintético SP645 confirma apenas variável basal visível.
- **API editorial de publicação v1:** antes da correção da branch, selecionava registros segundo YAML editorial sem validar as flags SQL. A alteração da branch exige ambas as flags e falha com erro explícito se alguma variável bloqueada for selecionada. Regressão automatizada cobre os três estados bloqueados.

## 4. Situação e próximo gate

**Aprovado:** testes de segurança no runner Core CI do GitHub, **196/196**, e teste estadual de escala no head `2933c7d15b172f5630191597922e0a9e7d48c13f`. **Não aprovado ainda:** conclusão da validação de navegador na prévia, verificação em SQLite canônico real já materializado e equivalência contábil histórica das quatro contas (especialmente FPM 2013–2017 e Fundeb).

**Decisão:** manter **PR #232 em rascunho**, não aplicar migração e não promover `governance/proposals/FED04_VARIAVEIS_DCA_ITR_FUNDEB_CANDIDATAS.yml` aos catálogos operacionais. Não há alteração em `observacao`, R2 canônico ou painel público.
