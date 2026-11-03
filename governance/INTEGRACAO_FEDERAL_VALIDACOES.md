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


## Registro 2026-11-03 — diagnóstico CI e territorialização conservadora G4

**GitHub:** PR [#213](https://github.com/hilaliskandar/mapa_do_tesouro/pull/213) permanece aberto como draft. Consulta de runs associados ao commit `b2890ee` retornou lista vazia; consulta de status combinado também não retornou checks. Não é prova de falha nem de sucesso do GitHub Actions. Tentativa de `git ls-remote` via container falhou por DNS `github.com`; não houve checkout/testes neste host. Portanto **G2/G3 não estão homologados por nova CI nem por staging real**.

**OpenAPI e amostra:** leitura pelo Crawl2AI dos esquemas `/obras/openapi.json`, `/parcerias/openapi.json` e `/especiais/openapi.json` confirmou os parâmetros `pagina` e `tamanho_da_pagina` nas rotas testadas. URLs com `pagina=1&tamanho_da_pagina=2` retornaram: Obrasgov projetos filtrados SP, `total_items=20837`; Parcerias propostas recebedoras SP, `total_items=13434`; Especiais programas, `total_items=16`. Em três propostas SP inspecionadas, `cd_ibge_recebedor` veio preenchido (ex.: São Paulo 3550308 e Ribeirão Preto 3543402). Em três obras consultadas, não foi observado campo municipal IBGE equivalente; não inferir localização da obra a partir do recebedor.

**Incremento G4:** novo [validador territorial](../pipeline/normalize/federal_territory.py), commit `b5928e7`, recebe cadastro IBGE explicitamente fornecido pelo chamador e só reconhece código exato de sete dígitos nele presente. Retorna `confirmado_recebedor`, `fora_do_universo` ou `em_revisao`; preserva papel `ente_recebedor_proposta`, sem afirmar localização do investimento ou ocorrência de pagamento. [Testes isolados](../tests/test_federal_territory.py), commit `f31746a`, cobrem códigos inválidos, ausência, município fora do cadastro, rejeição de correspondência por nome e não atribuição de valores financeiros. Workflow experimental passa a incluir QA territorial (commit `03a1af1`).

**Limitações:** não carregado cadastro integral SP645 pelo validador; a lista deve ser proveniente do cadastro canônico verificado. Não executada conciliação entre propostas, empenhos, pagamentos e obras. Não declarado G4 aprovado. Não houve alteração da base canônica, R2 privado ou Pages.

**Critérios para próximo gate:** (1) executar workflow com logs verificáveis, (2) validar snapshot real e hash, (3) recuperar cadastro SP645 canônico e testar unicidade/cobertura, (4) separar município do ente recebedor de município da obra, (5) só depois projetar agregados.


## Registro 2026-11-03 — G4: leitura direta do cadastro canônico SP645

**Evidência de esquema:** `data/schema/001_initial.sql` define `municipio(codigo_ibge, nome, uf, ativo)` e `universo_municipio(universo_id, codigo_ibge)`. `pipeline/build/export_state_api_v2.py` já consulta essas tabelas em junção para publicar catálogo municipal. O leitor novo preserva esse contrato e não cria cadastro derivado.

**Implementação:** 
- [`pipeline/normalize/federal_canonical_universe.py`](../pipeline/normalize/federal_canonical_universe.py), commit `5f488a8`: conexão SQLite via `mode=ro`, `PRAGMA query_only=ON`, leitura do universo `SP_645` e checagem de exatamente 645 códigos IBGE de sete dígitos, prefixo `35`, UF `SP`, integrantes ativos, integridade de junção e unicidade.
- [`tests/test_federal_canonical_universe.py`](../tests/test_federal_canonical_universe.py), commit `1fde853`: testes com SQLite sintético, banco inalterado, cardinalidade divergente, UF inválida, inativo e uso do normalizador de recebedor.
- Workflow experimental inclui esses testes (commit `fe68932`). **Não houve leitura do banco canônico real**, apenas código/testes para fazê-la quando o ambiente privado estiver disponível.

**CI e infraestrutura:** a consulta GitHub ao commit anterior `2ab911b` retornou `workflow_runs=[]` e `statuses=[]`. Esse resultado não permite concluir sucesso ou falha de Actions. O checkout por `git ls-remote` no ambiente local falhou com `Could not resolve host: github.com`. **Os testes desta revisão não foram executados localmente**; não marcar G4 homologado.

**Critérios ainda pendentes:** executar QA contra SQLite canônico privado aprovado; provar 645 códigos e testagem de casos fora do universo; validar dados reais das propostas (código do recebedor); verificar regras de localização de obras do Obrasgov; registrar hashes, CI e eventual divergência. Nenhum dado recebido nem publicado.


## Operação remota — 03/11/2026

O usuário não dispõe de runner local no computador atual. **Não exigir comandos ou instalações locais** para a continuidade. O fluxo escolhido é GitHub Actions hospedado (`ubuntu-latest`) a partir do PR #213. Atualizado `.github/workflows/federal-public-api-smoke.yml` (commit `7fd6302`) para compilar módulos, executar QA de staging e territorialização com mocks, efetuar três GETs públicos e salvar uma amostra mínima efêmera, exibindo no `GITHUB_STEP_SUMMARY` somente contagens e hash do manifesto, sem os registros brutos. O workflow já tem evento `pull_request` restrito a arquivos experimentais e `workflow_dispatch` para uso quando disponível; no caso de um novo workflow criado apenas na branch, a opção de execução manual pode depender de sua presença na branch padrão. **Não presumir que o workflow executou após o commit.** Ainda falta consultar os runs/checks da revisão para confirmar passagem. A infraestrutura privada e a produção seguem intocadas.

## Registro 2026-11-03 — Homologacao amostral remota efetivamente executada

**Ambiente:** sandbox remoto independente do computador do usuario, com checkout da branch `feat/integracao-transferencias-federais-pac-20261103`, commit exato `15c7c0565143825ebc6da6e1e5944907fad10d83`. Esse commit antecede esta atualizacao apenas documental. Nenhum comando executado no equipamento do usuario.

**Resultado verificavel no ambiente de execucao:**
- `python -m pytest -q tests/test_federal_public_api.py tests/test_federal_staging.py tests/test_federal_sample_staging.py tests/test_federal_territory.py tests/test_federal_canonical_universe.py`: **37 passed** (0.17s).
- `FEDERAL_API_LIVE_SMOKE=1 python -m pytest -q -s tests/test_federal_public_api_live.py`: **3 passed** (1.86s); GETs reais das tres APIs com primeira pagina de 2 linhas por fonte.
- `python -m pipeline.acquire.federal_sample_staging --output /tmp/mapa_federal_213_private_sample`: **status `staging_verified_local_only`**, 3 artefatos, 6 linhas; totais de origem informados pela API: Obrasgov-SP 20.837 projetos, Parcerias-SP 13.434 propostas, Especiais 16 programas. Totais **nao equivalem** a Novo PAC, a repasses realizados ou a cobertura de todos os 645 municipios.
- `verify_manifest` executado novamente sobre arquivos efetivamente gravados: **1 manifesto verificado, 3 arquivos, 6 registros, nenhum hash divergente**.
- Rodada de `pytest` sem ativar a variavel do smoke: **37 passed, 3 skipped**, indicando que chamadas HTTP reais continuam opt-in.

**Rastreabilidade do lote real (SHA-256):**
- Manifesto: `71b18d5c74a4ce06734d53509f116d7235b19eb4809f9ade31e671f7e767b2c7`.
- Obrasgov `projeto-investimento`: `541c65e378fd281ac761821a3a074c030d3f4e0039fdea2ca13329836940b413`.
- Parcerias `proposta`: `8fcbcac3cc57adc80e6cd52542df134cb60a04a25895f611b3c6d76f66501d0b`.
- Especiais `programas-especiais`: `fe61658be382846bb1a5ff6f8bb4e81212eabb6e58b46534ef54ad6444d273fd`.

**Diagnostico do GitHub Actions:** a busca de runs por branch mostrou 14 execucoes, todas referentes aos commits iniciais do PR, inclusive Core CI 41662568905 success no commit `11888db9`. A API de workflow `federal-public-api-smoke.yml` devolveu **404 Workflow not found**; esse workflow novo consta da branch do PR, mas nao esta registrado na `main`. Nao foi disparado job recente no GitHub Actions. A causa exata de todos os nao-disparos subsequentes nao foi conclusivamente demonstrada. **A homologacao desta rodada decorre do sandbox remoto, nao do GitHub Actions**.

**Decisoes de gate, com escopo rigoroso:**
- **G2: aprovado para conectividade e contrato amostral** do cliente das 3 APIs em 03/11/2026; ainda falta continuidade automatizada e controle de cobertura/paginacao ampla.
- **G3: aprovado somente para staging local isolado de 3 paginas**, escrita, manifesto e verificador SHA-256; **nao** homologado para armazenamento permanente R2, ingestao SQLite ou recuperacao operacional.
- **G4: testes unitarios aprovados em SQLite sintetico**; leitura do SQLite SP645 canonico real, verificacao dos 645 registros e correspondencia territorial em escala **ainda nao homologadas**.
- G5-G7 continuam pendentes. Nenhuma atualizacao no R2, SQLite canonico, Cloudflare Pages ou publicacao.

**Proxima etapa:** inventariar o caminho de snapshot privado/canonico aprovado, criar rotina de exportacao controlada e versionada apenas em ambiente de teste, e validar cobertura, chaves e conciliação sem duplicar cifras de empenho/pagamento. Nao expor registros brutos no Git.
