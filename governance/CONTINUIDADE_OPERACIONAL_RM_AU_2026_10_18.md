# Continuidade operacional — Finanças Municipais SP e cadernos RM/AU

Atualização: 2026-10-18. Estado: registro de reconstrução documental, **não** autorização de deploy.

## Finalidade

Impedir perda de trabalho entre chats, versões de API, releases e artefatos editoriais. Esta página é o primeiro ponto de retomada da frente fiscal. **Nunca começar um novo motor de cálculo, nova coleta estadual, nova API ou novo gerador antes de consultar o estado e o inventário existentes.**

## Fontes de verdade e sua precedência

1. Código e contratos: branch/commit efetivo no GitHub; distinguir `main`, branches e PRs.
2. Produção: consulta e evidências do endpoint público, seu manifesto, build e hashes. Um merge ou execução bem-sucedida não prova que o conteúdo foi implantado.
3. Homologação: pacote exato, manifesto, contagem, hashes e parecer do respectivo gate.
4. Inventário e memória: `governance/INVENTORY.md`, `governance/PROJECT_STATE.md` e registros de handoff.
5. Conversas e documentos de trabalho: evidência histórica, não substituem inspeção do repositório ou payload.

## Estado recuperado em 18/10/2026

- O README da `main` ainda descrevia a release estadual v0.4.0/API editorial v1 como próximo ponto. Esse trecho é **histórico e insuficiente** para representar a frente editorial da RMJ.
- Documentação posterior: `governance/PROJECT_STATE.md` registra o projeto independente `financas-rmj.pages.dev` e confirmação de implantação do PR #196 em 15/10; não confundir com o portal estadual.
- Os históricos de conversa recuperados mencionam PRs #143 (geração editorial), #144 (evolução de API) e #198 (ampliação de catálogo). A situação de merge/implantação de cada um **não foi verificada nesta atualização**.
- Auditoria documental anterior do pacote E2, workflow run `38944712710`, registrou dez boletins, 280 fichas HTML e 626 hashes coincidentes.
- A auditoria E2 encontrou 50 variáveis nos 287 JSONs municipais, enquanto a revisão do catálogo associada ao PR #198 continha 57, incluindo `inversoes_financeiras`, `operacoes_credito` e `alienacao_bens`. Isso foi diagnosticado como **diferença entre versões do catálogo**, não como perda de dados DCA. A existência das 57 variáveis na produção atual permanece a verificar.
- O caderno PDF `Finanças Municipais – Regiões Metropolitanas | RMJ` v3.10 foi trabalhado fora do pipeline da plataforma; a candidata com 245 páginas e apêndice de 21 questões NÃO é prova de dados homologados na API.
- Documentação e pacote experimentais do gerador RM/AU v1.2 validam contratos sintéticos; **não** devem substituir a API, os indicadores e os dados já publicados.

## Contrato de retomada de cada novo chat

1. Ler esta página e os três arquivos `README.md`, `governance/PROJECT_STATE.md`, `governance/INVENTORY.md`, além de `governance/PENDING_TASKS.md`.
2. Verificar branch, HEAD, PRs relevantes e inventário de releases; não usar contagens desatualizadas do README como estado corrente.
3. Conferir API publicada: `/data/api/v1/publication/contract.json`, `publication/universes.json`, contexto de `RM_JUNDIAI`, fichas municipais e metadados de build. Buscar versão nova somente se o código e o contrato a provarem.
4. Registrar em uma tabela: **desenvolvido / integrado / homologado / implantado / acessível / completo**, com data, URLs, commits e evidências separadas.
5. Reconstruir o conjunto de dados do **snapshot publicado e homologado**, nunca misturar arquivos de releases diferentes.
6. Antes de qualquer implementação, consultar `data/catalogs/publication_variables_v1.yml`, exportador `pipeline/build/export_publication_api.py`, Skills editoriais e testes existentes.
7. Preservar a versão pública; correções novas em branch e com testes, sem rebuild ou implantação sem autorização.
8. Ao terminar, atualizar estado, inventário, pendências e handoff com mudanças, evidências, bloqueios e próxima ação exata.

## Gates específicos para fechar a divergência API/E2

- G-API-01: localizar commit, branch e estado do PR #198; comparar 50 e 57 variáveis sem modificar dados.
- G-API-02: conferir contrato, dados e escala dos percentuais (`ratio_0_1` vs `percent`) e separar QA do snapshot, artefato e deploy.
- G-API-03: comparar build homologado E2 (run 38944712710), `main`, eventual branch posterior e produção, com hashes de arquivos.
- G-API-04: mapear cada dado necessário aos cadernos regionais para a API; nenhuma consulta externa na produção editorial quando já houver dado válido disponibilizado.
- G-API-05: só promover catálogo/artefato revisado após cobertura, paridade fiscal, QA HTML/CSV, regressão e autorização.

## Registro de execução e handoff mínimo

Para cada mudança, registrar: data/hora; objetivo; repositório/branch/commit; API e build consultados; fontes; arquivos alterados; comandos/testes e resultados; pendências e impedimentos; links permanentes; próxima ação. Nunca declarar conclusão pelo mero planejamento.

## Limites

Este registro é uma salvaguarda documental. Não confirma que a API v2 ou o catálogo de 57 variáveis esteja em produção; não aprova homologação substantiva do PDF nem autoriza deploy. Fontes originais permanecem nos históricos, no inventário e no projeto; fontes oficiais externas são responsabilidade do pipeline da plataforma, não do gerador editorial.

## Confronto direto da main — 18/10/2026

O arquivo `data/catalogs/publication_variables_v1.yml` lido diretamente da `main` possui **50 entradas de variáveis**; SHA do blob `10aa9162fcbbdfeba3978a93de76e3acd105da88`. As três chaves adicionais de capital não constam desse catálogo. O exportador `pipeline/build/export_publication_api.py` foi inspecionado (blob `e9f84bee332c77f8fc01a154b183f3ff65f6cdae`) e utiliza o catálogo para construir contextos. Assim, **o catálogo ampliado de 57 variáveis registrado no histórico do PR #198 não está integrado ao arquivo canônico da `main` nesta leitura**. Isso NÃO prova que a API pública atual apresente 50: acesso independente ao endpoint não foi possível neste ambiente. Próximo passo: identificar o commit/branch do PR #198, confrontar o artefato E2 e a implantação pública com hashes, sem executar deploy.

## Revisão diretamente inspecionada do PR #198

O GitHub aceitou a referência `refs/pull/198/head` e retornou `data/catalogs/publication_variables_v1.yml`, blob SHA `47947286ee607bcc2bf2728c7b4b0417320f7ade`, com **57 variáveis**. A `main` tem 50, blob SHA `10aa9162fcbbdfeba3978a93de76e3acd105da88`. Diferença reproduzível diretamente entre fontes, sem estimativas. A leitura de `refs/pull/143/head` e `refs/pull/144/head` para o mesmo arquivo retornou o catálogo de 50. A existência do ref do PR NÃO demonstra merge, aprovação ou implantação. É proibido substituir a versão pública com base apenas nessa diferença.

## Camada adicional recuperada — API v2 com 75 variáveis

A fonte `governance/API_V2_READINESS_REBUILD_2026_10_13.md`, lida na `main`, registra o workflow run `38360896979` (artefato privado ID `11795250292`, SHA-256 ZIP `22f9431f4d069c89fa2c43607b1bfdda4f3c3d8bd3c338d3f3c94a889993bc40`) após o PR #150: **75 variáveis publicáveis**; 48 com lacuna editorial no campo `cautelas`; 17 percentuais com escala armazenamento/exibição ainda não certificada. Aprovação estrutural não é homologação nem prova de publicação da API v2. Não tratar a evolução 50→57 do catálogo editorial v1 como limite do contrato v2. Próxima ação: confirmar endpoints e manifesto reais da API v2, certificar escalas e documentação, e mapear o gerador RM/AU ao contrato mais completo validado.

## Auditoria de certificação API v2 — 18/10/2026

Foram recuperados diretamente os registros `governance/API_V2_REAL_DATA_AUDIT_2026_10_13.md`, `API_V2_READINESS_REBUILD_2026_10_13.md`, `API_V2_PERCENT_SCALE_EVIDENCE_2026_10_13.md` e `API_V2_PERCENT_PROVENANCE_2026_10_14.md` na main.

- API v2 construída a partir de dados canônicos no run `38355047393`: 645 fichas, 13 universos, 75 variáveis, 174.795 observações, 2021–2025. O relatório afirma explicitamente **não ter realizado deploy público da API v2** naquele gate.
- Reconstrução run `38360896979`: 75 variáveis; 48 com lacuna em cautelas; 17 com escala percentual não certificada.
- Análises de 14/10: 11.374 percentuais importados conciliados e 5.420 razões de 2025 conciliadas aritmeticamente, sem demonstrar comparabilidade temporal. Run `38593209824`, PR #160: diferenças de proveniência entre séries importadas e cálculos de 2025.
- Decisão: **não preencher metadados em massa nem adotar multiplicador 100 sem prova por variável e exercício**; a geração editorial deve bloquear narrativa comparativa de séries com linhagens heterogêneas sem reconciliação.
- Bloqueios atuais: certificação da escala percentual, documentação de cautelas e evidência de implantação pública posterior. Não abrir novas coletas externas editoriais por esta lacuna.
