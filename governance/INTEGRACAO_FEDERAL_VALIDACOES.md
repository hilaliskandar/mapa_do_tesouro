# Diário de validação — Integração federal e Novo PAC

Documento incremental complementar ao [plano](INTEGRACAO_FEDERAL_PAC_PLANO.md) e ao [README principal](../README.md).

## Registro 2026-11-03 — Abertura de projeto

**Escopo realizado**
- Repositório `hilaliskandar/mapa_do_tesouro` e branch-base `main` identificados via GitHub.
- README canônico, `governance/PROJECT_STATE.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `PENDING_TASKS.md` e `QA_CHECKLIST.md` examinados.
- Arquitetura compatível com extensão: ingestão → normalização → SQLite → JSON static-first → Pages, snapshots privados R2, hashes, proveniência, QA e baseline `TIC_TIM_30`.
- Código de adaptadores, integração com D1/SQLite, pipelines e frontend **não foram modificados**.
- Dados das APIs públicas foram **testados em investigação anterior de outro projeto**, não homologados neste repositório. Leituras reais anteriores: Obrasgov (`/projeto-investimento`, `/empenho`, `/execucao-fisica`), Transferegov parcerias (`/programa`, `/proposta`, `/parceria`, `/empenho-parceria`) e transferências especiais (`/data-atualizacao`).
- Fontes Nova PAC/MCMV com recursos XLSX/ZIP/CSV localizadas previamente, mas arquivos binários **não inspecionados**.

**Gate G0:** documentação criada; revisão por PR ainda não realizada. **G1:** inspeção inicial, sem inventário completo de schema/código. **G2–G7:** não executados.

**Verificações e ressalvas**
- Sem teste local de código, pois o PR inicial contém exclusivamente documentação.
- Não se confirmou ainda nenhuma equivalência financeira entre empenho federal e receita municipal, nem cobertura Novo PAC por identificador.
- Não inferir implantação ou execução de automações pela abertura do PR.

**Próximo incremento:** inspecionar `pipeline/acquire/`, `data/schema/`, `pipeline/build/` e testes; desenhar adaptadores públicos com fixtures e confirmar em execução isolada. Documentar resultados aqui e no README em cada novo commit.

## Template obrigatório para novas rodadas

```text
Data/hora:
Gate:
Branch/commit:
Fonte / endpoint / versão OpenAPI:
Parâmetros e universo:
Artefatos (nome, SHA-256, MIME, data-base):
Cobertura, nulos e cardinalidade:
Testes e evidências (run/URL/log):
Diferenças contábeis e relações reprovadas:
Resultado: APROVADO | REPROVADO | PENDENTE | BLOQUEADO
Decisão, responsável e próximo passo:
Atualização realizada no README: SIM/NÃO
```

## Registro 2026-11-03 — Incremento G1/G2

- Inspecionados: `pipeline/acquire/`, `data/schema/`, testes, `pyproject.toml`, `pipeline/acquire/siconfi_dca.py` e `tests/test_siconfi_source.py`. O projeto ja usa testes pytest e clientes HTTP com retries, preservando snapshots brutos e manifests.
- Adicionado `pipeline/acquire/federal_public_api.py`: cliente GET de `obrasgov`, `parcerias` e `especiais`; allowlist de endpoints, filtros validados, limite de paginas/tamanho, HTTP timeout, retries transientes, validacao do contrato paginado. **Nao ha envio ao R2, SQLite ou Pages.**
- Adicionado `tests/test_federal_public_api.py`: testes isolados sem rede para filtros, ids, paginação, erros, retry 503, não-retry 403 e bloqueio de endpoint nao autorizado.
- Commits de implementacao: `facecfaa` e `11888db`.
- CI do commit `11888db`: workflows Core CI, SICONFI e prévia foram iniciados automaticamente pelo GitHub; **resultados ainda pendentes no momento deste registro**. A existência de workflow de Pages Preview nao significa promoção em produção. Confirmar alias e conteudo se implantado automaticamente.
- **G1:** pontos de extensão iniciais identificados, inventario estrutural completo pendente. **G2:** codigo + testes criados, **nao homologado** enquanto CI/consulta real neste repo não forem validados. G3–G7 seguem bloqueados.
- **Segurança:** nenhuma credencial usada, nenhuma API externa consumida pelo codigo experimental nesta rodada; somente mock de teste. Não alterar produção.


### CI verificado em 03/11/2026

No commit `11888db9`, o Core CI run `41662568905` terminou `success`. O workflow `bootstrap-ci.yml` inclui `python -m compileall -q pipeline` e `pytest -q tests`. Também terminaram com sucesso os runs `41662568831` (SICONFI Smoke), `41662568875` (State Smoke), `41662568886` (Baseline Crosscheck) e `41662568781` (SP645 Scale). Pages Preview run `41662568828` ainda estava em andamento na última consulta. A aprovação é de compilação e testes unitários simulados; nenhuma consulta externa realizada pelo novo cliente foi homologada. G2 segue parcialmente validado até testes HTTP reais, sem alterar produção.

## Registro 2026-11-03 — Smoke HTTP real de baixo volume

**Novos arquivos:** `tests/test_federal_public_api_live.py` (commit `dd39ecc`) e `.github/workflows/federal-public-api-smoke.yml` (commit `b5c5d65`). O teste é opt-in, com a variável `FEDERAL_API_LIVE_SMOKE=1`, realiza somente GET, primeira página de dois registros por serviço, não grava dados nem executa migrações. O workflow dispõe de permissões `contents: read` e limite de oito minutos, acionado somente em PR que altere caminhos específicos ou manualmente.

**Evidência das fontes externas, obtida via Crawl2AI e não pelo novo cliente Python:** 
- `https://api-publica.obrasgov.gestao.gov.br/obras/projeto-investimento?uf_principal=SP&tamanho_da_pagina=2` retornou `total_items=20837`, duas linhas e `id_projeto_investimento`.
- `https://api-publica.transferegov.gestao.gov.br/parcerias/proposta?sg_uf_recebedor=SP&tamanho_da_pagina=2` retornou `total_items=13434`, duas linhas e `id_proposta`, com campo `cd_ibge_recebedor`.
- `https://api-publica.transferegov.gestao.gov.br/especiais/programas-especiais?tamanho_da_pagina=2` retornou `total_items=16`, duas linhas e `id_programa`.

**Situação de homologação:** Consulta externa direta comprovada; teste do cliente Python conectado às APIs **ainda não confirmado** (consulta ao histórico de workflows do commit `b5c5d65` não retornou execução correspondente). Tentativa de execução via host local não foi possível devido à indisponibilidade de DNS para github.com. Evitar classificar o gate G2 como aprovado por extrapolação. Reavaliar workflow/CI após evento de PR com log explícito, depois repetir amostra e criar snapshot com hash em staging, no G3. Não houve ingestão ou publicação.


## Registro 2026-11-03 — Implementação inicial do G3 (staging local)

- Verificações dos commits de smoke HTTP `b5c5d65` e `8ccd87a` via consulta GitHub a runs associados: a consulta **não retornou execuções**. Portanto, o teste do próprio cliente contra APIs reais ainda não pode ser homologado; as respostas externas anteriores continuam sendo evidência separada do Crawl2AI.
- Criado `pipeline/acquire/federal_staging.py` (commit `46a16a1`): grava JSON canônico UTF-8 de cada página em pasta local explícita, nomes content-addressed SHA-256, manifesto por lote com contagem, URL e hash, reutilização idempotente, verificação de integridade e validação dos domínios oficiais.
- Criado `tests/test_federal_staging.py` (commit `abf4644`): cenários sem rede para roundtrip de hash, repetição sem segundo manifesto, revisão de valores, corrupção detectada, fonte/URL não autorizada, página repetida e distinção zero vs nulo.
- **Limite:** o código de staging usa uma pasta local fornecida explicitamente, não faz upload ao R2 nem cria snapshots persistentes em infraestrutura. Os testes foram adicionados ao PR; a CI desse commit **não foi confirmada ainda**, logo não marcar G3 aprovado.
- **Segurança:** não há novo serviço, automação de coleta ou escrita na base fiscal. Não acrescentar registros brutos ao Git, pois payloads podem conter identificadores e informações pessoais de beneficiários.
- Próximos critérios: 1) confirmar CI dos testes de staging; 2) confirmar smoke HTTP real do cliente; 3) persistir em diretório isolado um lote real e validar hashes, origem, granularidade e ausência de segredos; 4) somente então avaliar R2 privado e expansão de escopo.


## Registro 2026-11-03 — G2/G3: cadeia de smoke e staging real controlado

**Evidência metodológica de API:** os OpenAPI oficiais Obrasgov, Transferegov Parcerias e Especiais especificam parâmetros de paginação `pagina` e `tamanho_da_pagina`. Leitura das amostras públicas mostrou `cd_ibge_recebedor` nas propostas do Transferegov (exemplos com códigos de sete dígitos), mas não forneceu campo `cod_ibge` municipal equivalente em três projetos do Obrasgov. Territorialização territorial **dependerá de nova verificação de chaves/geometria**; não converter localização textual em código definitivo.

**Implementação:** 
- `pipeline/acquire/federal_sample_staging.py` (commit `6863dfe`): três GETs, primeira página com tamanho 2, interrupção se resposta de uma fonte vier vazia, armazenamento local explícito, verificação de SHA dos artefatos e manifesto; saída impressa somente com IDs de manifesto e contagens, sem dados brutos.
- `tests/test_federal_sample_staging.py` (commit `c3a71cb`): teste de ponta a ponta com cliente simulado, idempotência, abortamento de lote incompleto e rejeição de saída relativa.
- `.github/workflows/federal-public-api-smoke.yml` atualizado (commit `2dd1148`) para realizar testes unitários sem rede, smoke HTTP de todas as três APIs e gravação temporária de pequeno lote real em `RUNNER_TEMP`, sem upload de artefatos ou conexão a produção.

**Status no momento do registro:** os endpoints oficiais foram consultados com sucesso por Crawl2AI e os parâmetros validados contra OpenAPI; **não foi localizado run do novo workflow na consulta de runs por commit `2dd1148`**. Testes e staging real pelo próprio Python **não homologados**. G2 e G3 permanecem parcialmente implementados e pendentes de validação. A impossibilidade de acessar github.com via DNS no container impediu checkout/teste local nesse ambiente; isso não prova falha do código.

**Próxima decisão:** identificar logs de um run `Federal Public APIs - Isolated Live Smoke` com commit da branch, verificar explicitamente `success` e saída de manifesto; se falhar, corrigir a causa antes de usar R2 ou SQLite. Manter ausência/zero separados e não promover as observações à API editorial.

