# Integração estadual de transferências e investimentos federais — SP_645

**Data:** 2026-11-09  
**Situação:** projeto documentado; inventário/ingestão estadual ainda não executados; sem mudança de dados, schema, R2 ou publicação.

## Decisão arquitetural

O projeto **não criará banco de dados ou plataforma paralela**. Utilizará o núcleo SQLite canônico do repositório `hilaliskandar/mapa_do_tesouro`, documentado em `governance/ARCHITECTURE.md` e `governance/DATA_MODEL.md`, com modelo longo, dados versionados, `artefato_fonte` e `observacao_proveniencia`. O bucket privado R2 **`financas-municipais-sp-canonico`** é a camada existente de guarda dos snapshots brutos, normalizados e artefatos volumosos, **não** um segundo banco de observações. A publicação atual segue `SQLite → materialização JSON static-first → Cloudflare Pages`; **D1 é opcional**, somente se surgirem consultas dinâmicas justificadas. Não há evidência de uma instância D1 já homologada como base operacional desta plataforma.

Evitar duplicação: (1) um único cadastro IBGE de 645 municípios; (2) universos regionais são filtros, não tabelas de origem independentes; (3) ingestão federal reusável e versionada na camada estadual; (4) estudos RMSJRP, RMRP, RMJ e outros consultam a mesma base; (5) cada fonte mantém identidade, conceito, data de competência, status e proveniência, mesmo quando se refere ao mesmo instrumento.

## Acervo reutilizável e motivação

- DCA 2013–2025: snapshot estadual em R2 `sp_645/dca/2013_2025/normalized.csv` e manifesto, sem substituição.
- TCESP estadual 2023–2025: agregados no R2 `tcesp/estadual/despesas/{ano}/run_.../`, sem substituição.
- RMSJRP G06-F2: **9.338 identificadores de propostas** em dois módulos (508 Parcerias e 8.830 Discricionárias/Legais), **74/74** consultas município–módulo e **231 páginas**, versionadas sob `rmsjrp/g06/2026_11_09/instrumentos_api_f2/`. São registros de propostas, **não** convênios celebrados ou pagamentos.
- RMSJRP G06-F3: amostra intencional de 37 registros de parceria e sete registros de empenho; um metadado de assinatura sem comprovação do documento. Preservados sob `rmsjrp/g06/2026_11_09/instrumentos_api_f3_amostra37/`. O G06-F4 permanece aberto; utilizar seus casos como sentinelas do novo coletor estadual.

## Fontes a inventariar, sem presumir cobertura

1. Transferegov: transferências discricionárias/legais, Gestão de Parcerias, transferências especiais e fundo a fundo, com documentação OpenAPI, situação e paginação de cada módulo.
2. Tesouro Nacional/Tesouro Transparente: FPM e transferências constitucionais/legais; distinguir normas e origens das transferências discricionárias.
3. Portal da Transparência federal: convênios, emendas, empenhos, ordens bancárias, pagamentos e outros datasets disponíveis; preferir arquivos completos quando melhor que requisições municipais.
4. Obrasgov/Novo PAC: contratos, localização, empreendimentos, execução e eventual vínculo de financiamento, respeitando escopo e datas dos cadastros.
5. Fontes municipais e TCESP: somente para conciliar crédito recebido, fonte de recursos, empenho, medição e liquidação locais.

O inventário deve registrar URL e endpoint, esquema, chave, tipo de transferência, licença, autenticação, filtros e paginação, cobertura histórica, atraso, limites, atualização retroativa e erros. **A existência de documentação de rota não prova sua operacionalidade ou completude.** Fundo a fundo retornou HTTP 500 no piloto RMSJRP e não pode ser marcado como ausência de recursos.

## Modelo lógico e prevenção de dupla contagem

A camada federal deve manter entidades próprias de **proposta**, **instrumento/parceria**, **partícipe/beneficiário**, **emenda**, **empenho federal**, **pagamento federal**, **obra/empreendimento** e **vínculo de conciliação municipal**, com chaves de origem compostas por sistema/módulo/identificador e datas. Antes da implementação, levantar os contratos e tabelas já existentes para optar por migrations incrementais sem alterar a semântica de `observacao`.

Separar município do beneficiário, sede do proponente, local da obra, executor e município efetivamente creditado. Uma relação territorial de obra ou beneficiário não equivale a ingresso de receita municipal. Registrar links por identificador explícito e nível de certeza; sem junções por similaridade isolada de valor/nome. Nunca somar linhas de módulos diferentes sem deduplicação jurídica comprovada. Não tratar valores de proposta, contrato ou empenho como pagamentos, nem pagamentos federais como despesas liquidadas municipais.

Novos indicadores anuais compatíveis com o modelo longo podem ser **derivados** apenas de eventos classificados, temporalizados e homologados. Valores ausentes continuam `ausente` ou `em_revisao`, jamais zero. Preservar diferenças entre transferência constitucional, legal, fundo a fundo, voluntária, especial e financiamento federal direto.

## Gates de execução e evidências

| Gate | Entrega | Critério de conclusão |
|---|---|---|
| FED00 | Inventário do acervo, SQLite/schema, R2, conectores e fontes | Matriz fonte–período–chave–disponibilidade, conferida; sem criar duplicata |
| FED01 | Contratos de dados, migrations propostas e crosswalk | Compatibilidade com modelo canônico e regressão, incluindo município IBGE |
| FED02 | Pilotos de aquisição em lote e API | Paginação, retries, limites, schemas, datas e versionamento testados |
| FED03 | Carga histórica estadual SP_645 | Contagem por fonte/ano/município, manifesto/hash/readback; cobertura documentada, não presumida |
| FED04 | Deduplicação e cadeia documental | Chaves únicas por módulo e vínculos com evidência; diferenças conciliadas |
| FED05 | Conciliação federal–municipal por amostra sentinela | Verificação de proposta 398 (SJR), sete empenhos G06-F3 e outros casos sem união por valor |
| FED06 | Indicadores e agregações regionais | Paridade 645 municípios + universos filtrados, regras de ausência e contas sem sobreposição |
| FED07 | Atualização incremental e retificações | Checkpoint, janelas de reprocessamento, comparação de versões, monitoramento de falhas |
| FED08 | Homologação integrada/publicação opcional | QA metodológico, regressão, hashes, prévia isolada e autorização explícita de promoção |

## Operação

Priorizar download integral de bases públicas para seleção por IBGE quando houver arquivos confiáveis; usar API paginada quando não houver lote ou para complementação e eventos recentes. Aquisições entram em `pipeline/acquire`; normalização em `pipeline/normalize` ou módulos equivalentes existentes; documentação/crosswalk em `data/catalogs`, `data/mappings` e `governance`. Usar workflows GitHub Actions e credenciais existentes sem expor segredos. Persistir originais e derivados em prefixo estadual próprio do mesmo bucket R2, a definir após inventário, por `fonte/versao/data_de_extracao`; nunca sobrescrever artefatos RMSJRP existentes.

Cadência inicial a validar conforme atualização da fonte: execução financeira diária quando publicada; propostas/instrumentos diária ou semanal; séries constitucionais semanal com conciliação mensal; obras semanal; QA e cobertura mensal. Usar captura incremental com correções retroativas e trilha de retificações; não presumir calendário uniforme.

## Controles editoriais e legais

A LC 200/2023 incide diretamente sobre o regime fiscal federal. A série de propostas, empenhos ou pagamentos, isoladamente, **não identifica efeito causal** do arcabouço sobre município. Cenários de RMSJRP G06-A/B seguem classificados como testes condicionais. Requerer prova de mecanismo, execução e explicações alternativas antes de quantificar impactos atribuíveis.

## Próxima operação exata e continuidade

1. Inspecionar `data/schema`, `pipeline/build`, a origem do SQLite produzido no build e os manifestos estaduais existentes; identificar migrations, índices e bindings **reais**.
2. Inventariar downloads nacionais e OpenAPI dos quatro módulos Transferegov, STN, Portal da Transparência e Obrasgov, anotando limites e cobertura; evitar coletar 645 municípios antes da decisão lote × API.
3. Produzir `MATRIZ_FONTES_FEDERAIS_SP645.csv` e proposta de schema/crosswalk em branch isolada. Gatilho de FED01: inventário validado.
4. Fazer piloto estadual controlado com a proposta 398/SJR, os sete empenhos G06-F3 e municípios de portes distintos; comparar com R2 já homologado.
5. Atualizar README principal, `governance/PROJECT_STATE.md` e este plano ao concluir cada gate; registrar run, commit, hashes, lacunas e **próxima ação exata**.

**Não executado nesta etapa:** nova ingestão, mudança do SQLite, criação de D1, alteração de R2, workflows, deployments ou publicação.

## Registro de execução FED00 — 09/11/2026

Foram produzidos [`MATRIZ_FONTES_FEDERAIS_SP645.csv`](MATRIZ_FONTES_FEDERAIS_SP645.csv) (11 conjuntos) e [`RELATORIO_FED00_INVENTARIO_2026_11_09.md`](RELATORIO_FED00_INVENTARIO_2026_11_09.md). Schema SQLite, tabelas de proveniência, integração TCESP e coletor regional Transferegov examinados por leitura direta de arquivos GitHub; fontes públicas nacionais validadas documentalmente. Nenhuma API estadual/CSV de dados foi integralmente extraída nesta etapa e o conteúdo do banco materializado/R2 live não foi auditado. **Status FED00: in_progress**, pendentes prova de arquivos, layouts, tamanhos, históricos, mapeamento operacional do build e consulta R2 read-only. Ação seguinte: auditoria técnica de pipeline de build + teste não destrutivo dos downloads nacionais. Preservar G06-F4 regional em paralelo.

## FED00-B — Reaproveitamento de APIs públicas, com prioridade ao Banco Central

A matriz atualizada [`MATRIZ_FONTES_FEDERAIS_SP645.csv`](MATRIZ_FONTES_FEDERAIS_SP645.csv) contém **14 conjuntos**, incluindo BCB SGS/IPCA, BCB SGS/Selic meta e ESTBAN municipal. API do BCB SGS 433 validada por consulta read-only via Crawl2AI, campos `data` e `valor`, três observações; ESTBAN identificado como fonte municipal com `CODMUN_IBGE`, mas download e layout ainda não homologados. Tesouro CKAN confirma históricos anuais e mensais e recurso 202610; Transferegov apresenta ZIPs de desembolsos e pagamentos no catálogo legado de 2023, cuja atualidade deve ser verificada. Relatório detalhado: [FED00](RELATORIO_FED00_INVENTARIO_2026_11_09.md).

Foi incorporado [`pipeline/acquire/probe_federal_sources.py`](../pipeline/acquire/probe_federal_sources.py), coletor de prova read-only de 5 APIs (dois SGS, dois OpenAPI, um CKAN), com limite de resposta, timeouts, hashes, QA e sem mutação de bases. **Ainda não foi executado em ambiente com conectividade HTTPS completa; uma consulta SGS isolada via Crawl2AI respondeu.** Próxima ação FED00: rodar script em runner GitHub Actions ou outro ambiente com DNS, analisar arquivos de transferências nacionais e validar o arquivo mais recente do ESTBAN. Priorizar **API para descoberta e atualização incremental; arquivo integral para carga histórica** quando oferecer cobertura maior com menor custo. Contabilizar estoque bancário e índice nacional como contexto, não transferências de receita municipal.

## FED00-C — Ponto de retomada após publicação dos pilotos

A base de metadados CKAN nacional foi recuperada e persistida em [`STN_CKAN_RECURSOS_TRANSFERENCIAS_SP645_2026_11_09.csv`](STN_CKAN_RECURSOS_TRANSFERENCIAS_SP645_2026_11_09.csv): **146 recursos, 6 nomes duplicados e 18 inconsistências de período entre título e URL**. Os conteúdos dos CSVs **não** foram lidos. Criados scripts `pipeline/acquire/probe_federal_sources.py` e `pipeline/acquire/probe_stn_transfer_csv.py` e dois workflows GitHub `fed00-api-probes.yml`, `fed00-stn-csv-pilot.yml` para execução pública de testes read-only (sem acesso R2). Critérios e estados individuais no [`STATUS_FED_SP645.csv`](STATUS_FED_SP645.csv); relatório [FED00](RELATORIO_FED00_INVENTARIO_2026_11_09.md).

**Próxima ação objetiva:** obter ID e conclusão dos dois Actions, ler `QA_FED00_API_PROBES.json` e `QA_FED00_STN_CSV.json`, sanar bloqueios HTTP caso existam, definir as chaves de município/competência a partir do CSV real, verificar a compatibilidade com o SQLite e somente então preparar a carga-piloto. Nenhuma integração fiscal está homologada nesta etapa.

## FED00-D/E — QA de arquivos e cobertura paulista (09/11/2026)

Os [relatórios das execuções](RELATORIO_FED00_QA_WORKFLOWS_2026_11_09.md) foram recuperados em ZIP e auditados: BCB/Transferegov/STN API **4/5 `qa_pass`**, com SGS Selic registrando data futura. Fonte CKAN STN `63b5f470-135f-4431-9158-ca8b7a43f61b`, SHA de CSV `097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`, **126.807 linhas brasileiras**, **13.889 linhas SP**, **645 nomes paulistas distintos**, 0 problemas de largura ou UF. Todas as linhas têm `ANO=2026` e `Mês=09`, apesar do nome do recurso `202610`. Atualizado o piloto para testar correspondência de nomes com os códigos IBGE retornados pela API oficial; somente `645/645` identificações unívocas devem gerar `STN_IBGE_SP_MATCH.csv`. Exigir leitura de artefatos antes de homologar. Próximo passo: analisar [runs 42655242340](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655242340) e [42655203386](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655203386), verificar nomes não conciliados e testar valores/decêndios. Não publicar nem modificar base.

## FED00-I — Ponto de retomada: crosswalk candidato completo

O [relatório de QA FED00](RELATORIO_FED00_QA_WORKFLOWS_2026_11_09.md) comprova 645/645 identidades municipais STN→códigos IBGE da referência geográfica versionada, zero ambiguidades e 12 exceções de nome documentadas. Artefato [13693486021](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42657409755/artifacts/13693486021), SHA do CSV candidato `20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c`. O resultado continua `candidate_secondary_reference` (e não `qa_pass`), devido a timeout da API IBGE no runner. Criado workflow [FED00 arquivamento R2](../.github/workflows/fed00-archive-stn-crosswalk-r2.yml) para preservar evidência no **bucket existente**, prefixo de candidatos, com validação SHA/readback; [run 42657908820](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42657908820) requer confirmação. Próxima diligência: verificar persistência, conciliar com `municipio` SQLite e auditar valores/decêndios antes de importar indicadores.

## FED00-J — Arquivamento candidate R2 finalizado

A execução [42658172768](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42658172768) homologou somente **persistência e readback** da tabela candidata 645/645 STN→código IBGE no bucket existente `financas-municipais-sp-canonico`, sob `sp_645/federal/stn/2026_09/candidates/STN_IBGE_SP_MATCH_CANDIDATE_20c80f6464de.csv`, SHA `20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c`, 39.503 bytes. O QA JSON também foi enviado. Comprovação e restrições no [relatório FED00](RELATORIO_FED00_QA_WORKFLOWS_2026_11_09.md). **FED00 continua `in_progress`** até paridade com `municipio` SQLite, validação da fonte IBGE, análise de valores e competência, e definição de esquema incremental. Não criar banco paralelo, não alterar `observacao` nem publicar.

## FED00-K — Chaves territoriais homologadas contra o banco real

O [relatório `RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md`](RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md) comprova o estado `qa_pass_identity_only` do teste [42661684901](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42661684901): `SP_645` do SQLite materializado possui **645/645 códigos equivalentes à tabela STN candidata**, sem códigos extras/faltantes/duplicados nem UF diferente de SP. Dez diferenças de nome foram registradas, sem modificar `municipio.nome`. O gate FED00 continua aberto até prova contábil dos decêndios, classificação, competência e integração sem dupla contagem.

## FED00-L — Fonte nacional STN preservada com readback

A execução [42662690269](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42662690269) preservou o **arquivo completo** do STN de competência setembro/2026 no mesmo bucket R2 da plataforma: `sp_645/federal/stn/2026_09/source/STN_MUNICIPIOS_2026_09_097638ce.csv`, SHA `097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`, 7.585.504 bytes, readback aprovado. Relatório `QA_STN_SOURCE_2026_09_42662690269.json` também persistido. Com essa prova, não é necessário repetir a API STN para o mesmo arquivo quando se produz recorte regional ou municipal; consultar o R2 por hash e filtrar pela identidade IBGE já homologada no SQLite (645/645; [relatório](RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md)). O QA monetário inicial encontrou 41.667 células SP de inteiros ou decimais com ponto, zero células não padronizadas e zero repetição do grão tentativo `UF–Município–Ano–Mês–Transferência–Item`; **isso não aprova somar nem denominar os valores como receita municipal recebida**. FED00 permanece aberto para semântica contábil, deduções, Fundeb, decêndios e crosswalk entre rubricas/contas.
