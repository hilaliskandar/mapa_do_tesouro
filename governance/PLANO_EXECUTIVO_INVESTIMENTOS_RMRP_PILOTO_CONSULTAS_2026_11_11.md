# Plano executivo do piloto RMRP — aquisição, incorporação e consulta de investimentos territoriais

**Data:** 11/11/2026. **Status:** desenho operacional aprovado como prioridade proposta, com modelos e consultas em desenvolvimento; sem carga nova no banco produtivo nem liberação pública.  
**Universo-piloto:** 34 municípios da Região Metropolitana de Ribeirão Preto (RMRP), agrupados pelas quatro sub-regiões do estudo fiscal.  
**Repositório:** `hilaliskandar/mapa_do_tesouro`, branch `investimentos-territoriais-sp645-20261111`, PR #233 *draft*.  
**Aproveitamento:** [pré-inventário RMRP lote 37](../editorial/rmrp/PRE_INVENTARIO_CARTEIRA_LOTE37.md), [investimentos municipais TCESP](../data/schema/006_tcesp_investimentos.sql), [modelo canônico](DATA_MODEL.md), [G06-F3 RMSJRP](../editorial/rmsjrp/RELATORIO_G06F3_VINCULOS_2026_11_09.md), [plano territorial SP645](PLANO_PRIORIZACAO_INVESTIMENTOS_TERRITORIAIS_SP645_2026_11_11.md).

## 1. Por que RMRP como primeiro piloto

A RMRP oferece **34 municípios** e indicadores fiscais já disponíveis. O lote 37 contém **34/34 valores de investimentos municipais liquidados em 2025** e **33/34 transferências de capital**, com lacuna em **Santa Cruz da Esperança**, que não deve virar zero. Existem extrações TCESP 2023–2025 com 102 pares município-ano e auditoria 101/102 de investimentos liquidados; **Guatapará/2023** permanece como exceção de **R$10.176,00** na confrontação histórica. Estes controles permitem regressão, sem confundir recursos transferidos com gasto investido.

As quatro sub-regiões devem ser derivadas dos metadados territoriais existentes; **não criar municípios duplicados**. O piloto começa com códigos IBGE7 recuperados por correspondência validada com `municipio` e `universo_municipio`. A lista de 34 localidades e respectivos agrupamentos foi copiada de modo rastreável para [`INV_RMRP_34_MUNICIPIOS_PILOTO.csv`](INV_RMRP_34_MUNICIPIOS_PILOTO.csv); a primeira versão do checklist preservava a coluna IBGE em branco até a conferência oficial. A [segunda versão com 34 códigos IBGE7 conferidos contra a API do IBGE para os 645 municípios paulistas](INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv) está pronta, com 34 correspondências nominais únicas; resta validar 34/34 chaves no cadastro SQLite canônico antes da ingestão. Não foi usada correspondência aproximada nem atribuição presumida.

## 2. Delimitação do produto

O painel deve responder separadamente:

1. **Carteira**: quais obras/projetos no município? objeto, localização, executor, financiador, fonte e etapa.
2. **Transferências**: quais instrumentos federais/estaduais são associados ao município, quanto foi comprometido e quanto foi efetivamente transferido, com identificação do favorecido e documentos.
3. **Execução final**: quanto a prefeitura liquidou em investimentos? Quanto foi executado diretamente pelo governo estadual/federal **no território**, comprovado por projeto/obra/contrato?
4. **Comparação fiscal**: cotejar entradas de transferências de capital e investimentos municipais liquidado, sem atribuir causalidade ou vínculo um-para-um sem documentos.
5. **Qualidade de dados**: quais projetos têm localização comprovada, quais pagamentos são homologados, quais instrumentos ainda não foram vinculados, qual cobertura por fonte e por ano?

**Regra fundamental:** transferência União→município→obra aparece como fluxo de financiamento e como gasto final; não somar os dois como se fossem investimentos independentes. Valor previsto/contratado/empenhado não é pagamento. Valor global da obra não deve ser somado às parcelas federais e estaduais que a financiam.

## 3. Aquisição de dados — ordem concreta do piloto

### Frente A: Obrasgov — descobrir intervenções situadas na RMRP

- O endpoint `/obras/projeto-investimento` da nova API Obrasgov admite `uf_principal=SP` e `tamanho_da_pagina` de até **200**, porém **não expõe filtro direto por código IBGE na especificação consultada**. A API declarou **20.942 registros para SP** em 11/11/2026, contagem ainda não auditada.
- Assim, **obter o inventário SP de forma paginada** (estimativa de cerca de 105 páginas com 200 itens, sujeita a paginação real), gravando snapshot completo antes de filtrar RMRP. Isso permite reutilizar a mesma aquisição na futura expansão SP645 e evita vieses de busca por nome.
- Deduplicar por `id_projeto_investimento` com *snapshot date* e controlar `total_items`, páginas esperadas, duplicatas, vazios, mudanças de paginação, *rate limiting*, retries/backoff e retificações.
- Atribuir município pela geometria `pins` da própria fonte (**WKT POINT longitude,latitude**) e por interseção com limites municipais homologados; preferir identificador de município explicitamente documentado na API quando houver. **Não geocodificar o centroide como se fosse local exato**. Preservar geometria CRS WGS84 `EPSG:4326` na origem e, se for reprojetar, usar `EPSG:4674` no modelo territorial do projeto; gravar precisão e fonte. Para projetos plurimunicipais, manter relação N:M e não fazer rateio sem regra explícita.
- Consultar `/geometria`, `/contrato`, `/empenho`, `/execucao-fisica` **pelos identificadores de projetos RMRP**. Contrato, empenho e percentual físico devem ficar em entidades distintas, sem inferir pagamento.
- Caso-sentinela: projetos cadastrados em Ribeirão Preto, Sertãozinho, Guariba e Guatapará, cobrindo porte e heterogeneidade territorial. Cada sentinela requer documento com local e ato de execução.

### Frente B: Transferegov — instrumentos federais e eventos financeiros

- **Transferências Especiais:** `/beneficiarios-especiais` filtra `uf_beneficiario`, `id_ente` e CNPJ; `/empenhos-especiais` filtra `id_plano_acao`; `/ordens-pagamentos-ordens-bancarias-especiais` filtra identificadores financeiros e não aceita filtro municipal direto no contrato examinado. Validar **cadeia de IDs antes de associar pagamento a município**.
- **Gestão de Parcerias:** `/proposta` filtra `cd_ibge_recebedor`, `/parceria` usa `id_proposta`, `/empenho-parceria` usa `id_parceria`. A rota `/ordem-pagamento` **não oferece `id_parceria` como filtro**: requer chave documental entre `id_documento_habil`, números SIAFI, UG ou outra relação explícita. **Não juntar por valor e data apenas**.
- **Discricionárias e Legais:** `/propostas` filtra `cod_munic_ibge`; baixar **CSV nacional histórico**, quando disponível e validado, para instrumentos/execução, complementando API ainda em evolução. Separar propostas rejeitadas/canceladas das celebradas e executadas.
- **Classificar capital x custeio na origem:** categorias de despesa da proposta (`categorias_despesa_proposta`, `in_tipo_gnd`, objeto/natureza); proposta `75094` de S. José do Rio Preto é **Custeio/Serviços** e deve ser excluída da contagem de investimento.
- Recorte piloto por código IBGE/cadastro canônico, nunca somente por nome de município.

### Frente C: Estado de São Paulo — convênios, repasses e execução direta

- **Portal de Convênios SP:** validar exportação CSV, dicionário, exercício, concedente, beneficiário/CNPJ, número, objeto, vigência e valores. Para o piloto RMRP, filtrar beneficiários e instrumento; obter *snapshots* nacionais/estaduais quando viável, sem descartar municípios pluribeneficiários.
- **Sefaz-SP/SIAFEM — Transferências Voluntárias:** extrair **liberações efetivas** e estornos, inclusive distinguir classificação **Investimento** e **Custeio** da própria consulta. O portal informa liberações desde agosto de 2007; não confundir valor de convênio com valor liberado.
- **Despesas estaduais diretas:** testar SIGEO/SIAFEM por órgão, programa, ação, contrato e possível identificador local de obra. **Despesa estadual de secretaria com sede em São Paulo não pode ser integralmente territorializada a São Paulo**, nem distribuída por população sem justificativa.
- Integrar entidades setorais e obras diretas do Estado em segunda rodada após homologar os instrumentos e liberações.

### Frente D: Município — reaproveitar TCESP e DCA

- Não reingerir as séries de investimentos municipais TCESP que já estão em esquema `006_tcesp_investimentos.sql`; usá-las em **consulta de comparação**, por município/ano/estágio. O importador existente opera em banco de desenvolvimento e o exportador já demonstra materialização JSON por município.
- Vincular documentos da fonte de financiamento/obra à execução municipal **somente quando instrumento, empenho, contrato, ação ou nota/recebedor permitirem ligação documental**. Código e nome de programa/ação variam entre municípios.
- Ano de transferência federal e ano de investimento municipal podem divergir; consultar a série temporal sem impor igualdade anual.

## 4. Persistência de dados e esquema proposto

**Contrato SQL proposto, não aplicado:** [`proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql`](proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql).

- `inv_projeto`: entidade de intervenção com chave estável interna.
- `inv_identificador_externo`: sistema + módulo + ID de projeto/obra, impedindo fusão inadvertida de APIs.
- `inv_instrumento`, `inv_projeto_instrumento`: convênio/termo/contrato e relação com projeto mediante prova documental.
- `inv_ator`: ente repassador, executor e favorecido (CNPJ e papel por evento).
- `inv_projeto_municipio`: relação N:M município/projeto + papel territorial + precisão + rateio auditável.
- `inv_localizacao`: coordenadas, método, CRS e artefato de origem.
- `inv_evento_financeiro`: fato **por documento e estágio** em centavos inteiros; estorno com sinal; origem de pagamento identificada; distingue transferência intergovernamental de despesa direta e natureza investimento/custeio.
- `inv_execucao_fisica`: percentuais e marcos físicos com data.
- `inv_vinculo_documental`: provas entre eventos e entidades, com estado do vínculo e URL/hash.

Aproveitar as tabelas canônicas `municipio`, `fonte`, `artefato_fonte` e `build`. **Não** substituir `observacao` anual por registros de projeto: `observacao` continua representando agregados aprovados; os eventos individualizados ficam em tabelas próprias, com agregação derivada por SQL.

**Regra de staging:** arquivos brutos/normalizados completos em bucket R2 privado `financas-municipais-sp-canonico`, prefixos de nova família `investimentos/sp645/{fonte}/{data_extracao}/` para extração nacional, com filtro RMRP documentado por manifesto. Cargas e SQL executados apenas em **SQLite de desenvolvimento**, transacionais e reversíveis. Tabela `artefato_fonte` conserva URL, hash SHA-256, data e tamanho, com QA de recepção e readback; IDs de lote e versões não podem sobrescrever outros projetos.

## 5. Interface e consultas do piloto — contrato static-first

Criar no preview (somente após dados reais e QA) endpoints de **arquivos JSON estáticos**, sem D1 nem servidor de consulta em runtime inicialmente:

| Recurso materializado | Conteúdo |
|---|---|
| `/data/api/v3/investimentos/rmrp/manifest.json` | `data_version`, fontes, datas, cobertura, status QA, checksum e limitações |
| `/data/api/v3/investimentos/rmrp/municipios.json` | 34 municípios, sub-regiões, cobertura por fonte, totais **por estágio** |
| `/data/api/v3/investimentos/rmrp/municipios/{IBGE7}.json` | Carteira de projetos e índices de instrumentos/eventos do município |
| `/data/api/v3/investimentos/rmrp/projetos/{id_seguro}.json` | Projeto, geometria, relação territorial, fontes, vínculos documentais e linha do tempo |
| `/data/api/v3/investimentos/rmrp/anos/{ano}.json` | Agregados anuais por setor, executor, financiador, estágio, com cobertura |
| `/data/api/v3/investimentos/rmrp/pendencias.json` | Lacunas, vínculos sem comprovação, dados em revisão e falhas de acesso |

Não colocar URLs internas R2 e segredos nesses arquivos. Identificadores de projeto podem conter caracteres especiais; criar **slug seguro, reversível e com mapeamento**, sem usar IDs arbitrários como path inseguro.

**Filtros de interface:** município ou sub-região; exercício/período; esfera financiadora; esfera executora; origem de recurso; setor/subsetor; natureza (obra/equipamento/outro); tipo de instrumento; estágio jurídico; estágio financeiro; situação física (cadastrada/execução/concluída/paralisada); projetos geolocalizados ou sem localização; apenas valores documentados.

**Consultas exemplo:**
- `Ribeirão Preto, 2025, obras com localização validada, valor previsto federal, situação atual, pagamentos comprovados e fonte de cada valor`.
- `Sertãozinho: carteira de projetos por setor, financiador e estágio, 2023–2026`.
- `RMRP: valores transferidos aos municípios por ano, separando União e Estado, e despesas de investimento municipais liquidadas, sem somar os dois`.
- `Sub-região de Jaboticabal: projetos paralisados e sem atualização cadastral há 12 meses`, se os campos de data/etapa estiverem disponíveis.
- `Guatapará: divergências TCESP × DCA nos investimentos de 2023 e possíveis projetos/transferências, sem presumir que se explicam causalmente`.

**Princípio de desempenho:** primeiro JSON municipal e índices regionais pequenos; detalhes carregados sob demanda. Pré-calcular agregações por estágio e ano, e não enviar todo o inventário estadual de obras ao navegador. Considerar R2 público com cache ou D1 **somente se** arquivos estáticos e filtros pré-calculados não atenderem a latência e frequência de atualização. Manter interface existente de investimentos TCESP em regressão.

## 6. Critérios de QA e gates em execução

| Gate | Entregável mínimo RMRP | Teste bloqueante |
|---|---|---|
| R0 | Universo RMRP | 34 códigos IBGE7 únicos, quatro sub-regiões, correspondência com `municipio` |
| R1 | Inventário fonte/rota | OpenAPI/CSV acessível, licença, chaves, paginação, modalidade, cobertura real |
| R2 | Captura Obrasgov/SP | Todas as páginas enumeradas, IDs únicos, hashs, pins/geometry, sucesso ou falhas documentadas |
| R3 | Captura Transferegov | Propostas, instrumentos e eventos por ID, classificação capital/custeio, 34 municípios; sem união especulativa |
| R4 | Convênios e liberações SP | Instrumentos por CNPJ/código, repasses e estornos conferidos, sem duplicidade instrumento/parcelas |
| R5 | Modelo de dados em cópia de desenvolvimento | FK e unicidade, integridade, estado `ausente` distinto de zero, histórico intacto |
| R6 | Ligações documentais | Matriz de cobertura de vínculos; 100% dos vínculos publicados com evidência oficial |
| R7 | Prévia de consulta RMRP | 34 páginas/códigos consultáveis, filtro por município/sub-região, ano, setor, fase, fonte; 50 consultas QA |
| R8 | Revisão e expansão SP645 | QA contra TCESP/DCA e decisões metodológicas, somente depois promover |

**Cobertura mínima de piloto:** 34/34 municípios reconhecidos pelo cadastro; mapa de fontes com todos os estados (consultado, sem ocorrência, erro, não coberto); carteira Obrasgov RMRP construída com ID real e geolocalização validada; pelo menos um conjunto de instrumentos Transferegov e um conjunto de liberações Sefaz-SP importado com QA; **nenhuma meta numérica artificial de registros ou pagamentos**.

**Regras críticas:** valores desconhecidos `NULL`/ausente; retorno HTTP 500 é erro, não ausência; se uma fonte só possui proposta, publicar "proposta" e não "obra financiada"; repasse recebido e investimento liquidado sem chave não se ligam automaticamente; não somar efeitos de estorno duas vezes; não somar financiamento privado e gasto público sem classificação.

## 7. Sequência de entregas

**Entrega 1 — RMRP e extração reprodutível.** Concluir cadastro 34/34, criar coletores read-only Obrasgov SP e Transferegov RMRP, extrair CSV estaduais/CGU; gerar manifestos, hashes, QA de paginação e exemplos de eventos, sem alterar produção. Avaliar 2 fontes federais + 1 estadual por primeiro lote.

**Entrega 2 — Carteira e conciliação.** Executar migração apenas em cópia de desenvolvimento, importar projetos/atores/instrumentos/municipalizações, preservar TCESP existente e marcar vínculos financeiros documentados; rever ambiguidades e estornos.

**Entrega 3 — Consultas e prévia RMRP.** Produzir JSON v3, interface própria integrada ao painel, filtros e mapas. Testar 34 municípios, quatro sub-regiões, 50 combinações de filtro, latência, compressão de JSON e prevenção de dupla contagem.

**Entrega 4 — Expansão.** Após homologação RMRP, promover coletores e dados já capturados do filtro estadual SP645, sem repetir toda aquisição nacional, mantendo municípios sem cobertura e projetos plurimunicipais.

**Estado atual em 11/11/2026:** plano, inventário de 14 fontes, OpenAPI oficiais consultados e amostras Obrasgov/Transferegov; **ainda não foram executadas a captura integral, migração de banco, interface de consulta ou publicação**.

## 8. Próxima operação exata

1. **Concluir o QA SQLite** dos 34 municípios com IBGE7 já identificados na API oficial do IBGE e comparar os agrupamentos sub-regionais com o cadastro do projeto; rejeitar divergências.
2. Enumerar Obrasgov `uf_principal=SP` página 1..N, 200 registros/página, com retries e checkpoint; filtrar por geometria municipal RMRP para gerar `obrasgov_rmrp_snapshot.csv` e lista de IDs.
3. Consultar Transferegov `/parcerias/proposta?cd_ibge_recebedor=...` e `/discricionarias/propostas?cod_munic_ibge=...`, além de Especiais, com paginação completa; **classificar Custeio vs Investimento**.
4. Identificar e baixar arquivos de convênios/liberações estaduais, preservando número jurídico, datas, estorno e valor, e arquivo CGU de pagamentos quando tiver chave de vínculo.
5. Validar SQL de proposta contra cópia de SQLite do repositório e geração de JSON static-first, incluindo teste automatizado para impedir publicação de evento sem `qa_status=homologado`.


## Atualização operacional de 15/11/2026 — pós-aquisição e integração controlada

**Escopo:** piloto RMRP34, quatro sub-regiões, expansão futura SP645. **Base confirmada:** Drive privado com `RMRP_Transferegov_Aquisicao_2026-11-15.zip` (ID `11iALaLrY5lnsghUsnbPr34mcNTfD5E6E`, 2.977.843 bytes) e `RMRP_Obrasgov_2026-11-15.zip` (ID `1CuZfRUTv1Oa_Z9pHkctq48-q2KuCaIS1`, 82.065 bytes), pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Metadados e estado não compartilhado conferidos em 15/11. O relato da execução anterior registra readback de hashes; esta atualização **não** equivale à inspeção de todas as linhas dos ZIPs.

**Coleta confirmada:** Transferegov 34 municípios, 68 pares município–módulo, 80 páginas, 743 propostas Parcerias, 6.410 propostas Discricionárias; recortes nacionais com 1.793 convênios, 2.537 linhas de desembolso e 1.240 registros de emendas. Obrasgov 218/218 candidatos selecionados por município proponente (91 concluídos, 77 cadastrados, 42 em execução, 6 cancelados, 2 inacabados), nenhuma geometria retornada e zero linhas atuais nas rotas de contrato/empenho; registrar divergência com três linhas de empenho observadas em quatro projetos na captura anterior de 12/11. Nenhum zero de resposta implica ausência de gasto em outras fontes. A seleção de 218 **não** é o universo das obras fisicamente na RMRP.

### Gates ordenados e critérios de aceite

| Gate | Prioridade | Trabalho | Aceite verificável |
|---|---|---|---|
| G-FED-01 | P0 | Readback dos ZIPs privados; inventário de membros, esquemas, chaves, datas, SHA-256 e número de linhas por arquivo; comparar manifestos com logs da aquisição | Zero corrupção e 34/34 municípios; divergências descritas, sem eliminar registros |
| G-FED-02 | P0 | Normalizar proposta, convênio, parceria, instrumento, projeto e movimentação; testar cardinalidades com chaves oficiais, em SQLite isolado | 0 chaves sintéticas sem origem; relatório de joins 1:1/1:N, órfãos e duplicados |
| G-FED-03 | P0 | Confrontar `NR_MOV_FIN` com OBTV, DL, itens DL, eventos e ordens bancárias CGU; identificar estornos, retenções, competência, moeda e estágio | Um `VL_PAGO` por movimento, sem multiplicação por OBTV; não confundir PAD GND4 aprovado com pagamento de investimento |
| G-FED-04 | P0/P1 | Vincular 441 linhas de coordenadas das propostas, 150 registros CIPI do recorte e projetos Obrasgov; validar por geometria municipal, fonte e precisão; buscar inventário paginado SP | `municipio_proponente`, `municipio_beneficiario` e `municipio_execucao` em papéis distintos; sem imputação por sede/centroide |
| G-FED-05 | P1 | Complementar transferências especiais (beneficiário→plano→empenho→ordem), parcerias (proposta→parceria→empenho→documento), CGU ordens bancárias; registrar cobertura por modalidade | Documento/ID de cada aresta, ausência ≠ zero, valores por estágio sem soma cruzada |
| G-FED-06 | P1 | Persistir cópia canônica imutável no R2 privado, por fonte/snapshot, e manifesto no Drive/README; derivar RMRP e SP645 sem downloads redundantes | Upload e readback, SHA-256, permissões, retenção e versão confirmados |
| G-FED-07 | P2 | Aplicar SQL proposto em SQLite de desenvolvimento; alimentar JSON `/data/api/v3/investimentos/rmrp/` e visualização privada | FK/unique, 50 testes de consulta, 34 municípios, quatro sub-regiões e controle de não duplicidade |
| G-FED-08 | P2 | Homologar prévia e planejar incremental com retificações retroativas; nenhuma promoção pública automática | Manifesto QA aprovado, métricas reconciliadas, documentação de limitações e autorização de publicação |

**Regra de publicação progressiva:** permitir carteira de projetos, objetos, vínculos e status **documentados**, inclusive valores previstos ou contratados rotulados corretamente. Bloquear os agregados de `investimento federal pago/executado` ou mapas físicos sem vínculo comprovado. Valores planejados, empenhados, desembolsados, pagos ao favorecido e investimentos municipais liquidados são medidas distintas e não aditivas. A relação nacional pagamento→OBTV já demonstrou 1:N (`NR_MOV_FIN` único em pagamentos e repetido no detalhamento). `siconv_itens_dl` contém `ID_DL`, mas **não** `ID_ITEM_PAD`; ligação de item pago→GND4 exige documento adicional.

**Execução:** começar por G-FED-01 com os pacotes existentes; não repetir 80 páginas/218 consultas. Em G-FED-04, considerar a cobertura independente de obras cuja entidade proponente não seja município da RMRP. Manter tabelas fiscais e site produtivo intocados até homologação. O backlog de 11/11 preserva estados históricos; este adendo prevalece em caso de status divergente.


### Execução FED06 — 15/11/2026

Validação realizada sobre a cópia **privada** da API estática. FED05 produziu 56 JSON; FED06 agregou 218 fichas de projetos Obrasgov, totalizando **274 JSON**. Manifesto contém SHA-256 de Transferegov e Obrasgov e explicitamente bloqueia publicação. Os 34 arquivos municipais receberam atributos formais do contrato, com indicadores não homologados mantidos em `null`. A bateria de **432 verificações** concluiu com **427 testes de integridade aprovados, zero falhas de integridade e dois gates de publicação bloqueados**: (a) índice das quatro sub-regiões requer correspondência oficial município–sub-região, não inferível da dimensão RA/RG/RM/AU; (b) homologação financeira/territorial depende FED03C e FED04B. [Relatório](INV_RMRP_FED06_QA_PREVIA_API_V3_2026_11_15.md). Não houve deploy. O ZIP FED06 permanece no ambiente da sessão atual, sem confirmação de upload ao Drive privado. Planejamento subsequente: documentar dimensão sub-regional, concluir pagamentos/OBTV/DL e validar coordenadas antes de promover indicador monetário ou mapa de execução física.


### Gate FED06B concluído — 15/11/2026

A dimensão de **quatro sub-regiões da RMRP** foi validada pelo art. 4º da LC paulista 1.290/2016, associada a 34 códigos IBGE7 oficiais e incorporada à prévia privada: 15 + 6 + 6 + 7 municípios, zero lacunas e sobreposições. A API conta agora 280 JSON, incluindo `subregioes.json` e quatro endpoints `subregioes/{codigo}.json`. Totais de propostas/convênios/desembolsos/obras por município proponente permanecem conservados, **sem atribuição física implícita**. [Dimensão](DIM_RMRP34_IBGE_SUBREGIOES_LC1290_2016_2026_11_15.csv), [relatório QA](INV_RMRP_FED06B_SUBREGIOES_QA_2026_11_15.md), [pacote privado Drive](https://drive.google.com/file/d/1gjLGe4IfK5WipARJ7SBo9WcsGWtrFoQ5/view). Armazenamento SHA-256 e CRC readback aprovados; nada publicado.

**Atualização de pendências:** a subdivisão oficial RMRP está resolvida. Ordem atual: (1) FED03C sobre ZIPs nacionais de pagamentos/OBTV/DL, preservando 1:N e estágios; (2) FED04B coordenadas e vínculos físicos de obras; (3) testes de prévia visual privada e homologação de indicadores. A plataforma pública não pode ser promovida automaticamente.


### Gate FED06C — 15/11/2026

Gerada prévia HTML local, autocontida e privada, derivada do FED06B e dos 280 JSON da API v3; filtros por 4 sub-regiões legais e município, contagens por proponente e série regional anual de desembolsos com estágio corretamente rotulado. JS passou em `node --check`, ZIP CRC e SHA256 de readback aprovados, sem chamadas à rede e sem deploy. [Relatório](INV_RMRP_FED06C_PREVIA_LOCAL_QA_2026_11_15.md); [pacote Drive](https://drive.google.com/file/d/1twgK_RpEKkLvCQ8-Xbsdu-5ieWy35m4c/view). Persistem FED03C (pagamento/OBTV/DL e natureza da despesa), FED04B (coordenadas/documentos e localização real) e homologação do dashboard em prévia restrita.


### Reabertura de FED03C/FED04B — execução do runner em 15/11/2026

Foi inspecionada diretamente a cópia SQLite FED04A e os pacotes regionais armazenados. Não existem nos ZIPs regionais os arquivos nacionais de pagamentos/OBTV/DL/coordenadas; o acesso DNS externo no executor segue bloqueado. Concluiu-se **preparo e teste reproduzível**, não aquisição nacional: reconciliador FED03C testado com um pagamento e duas linhas OBTV, novo leitor FED04B testado com coordenada candidata, ausente e inválida. Os resultados reais das bases nacionais **continuam pendentes** e devem ser executados somente com ZIPs oficiais versionados no runner autorizado. [Relatório de execução](INV_RMRP_FED03C_FED04B_RUNNER_TESTADO_2026_11_15.md) e [scripts/teste no Drive privado](https://drive.google.com/file/d/1JgQksYyudLpszduwiR26gvLeixugdSHk/view). Proibida promoção de pagamentos e geometrias sem prova documental. O portal novo de downloads `https://api-publica.transferegov.gestao.gov.br/downloads` foi confirmado por ligação navegável no portal oficial, mas não se obteve nesta sessão o arquivo binário nacional.


### Gate de aquisição nacional — fontes verificadas em 15/11/2026

A consulta dinâmica via Crawl2AI à página oficial de [downloads Discricionárias e Legais](https://api-publica.transferegov.gestao.gov.br/downloads) mostrou 65 arquivos e confirmou o catálogo dos sete ZIPs exigidos, todos com data 15/11/2026. [Manifesto de URLs e tamanhos](INV_RMRP_CATALOGO_SICONV_ZIPS_2026_11_15.json). Esta validação corrige o antigo bloqueio de descoberta de fontes, **mas não substitui transferência binária nem QA de ZIP**: DNS do ambiente executor indisponível, tentativa de navegador alternativo bloqueada por limite de uso. A próxima aquisição deve privilegiar `siconv_coordenadas_obra.zip` (2,9 MB), `siconv_contrato_cipi.zip` (4,1 MB) e `siconv_dados_obrasgov_geral.zip` (767 KB) para FED04B; em seguida `siconv_obtv_convenente.zip` (56 MB), `siconv_dl.zip` (206,4 MB), `siconv_pagamento.zip` (357,3 MB) e `siconv_itens_dl.zip` (523,1 MB) para FED03C. Registrar cabeçalhos, `Last-Modified`, `ETag` quando existentes, CRC, SHA256, data e contagem de linhas, sem subir microdados nacionais ao GitHub. [Ensaios robustos FED03C](INV_RMRP_FED03C_HARDENING_TESTES_2026_11_15.md) passaram, mas não há conciliação financeira real homologada. A API estática FED06C permanece privada.


### Gate de aquisição nacional — persistência do coletor em 15/11/2026

O Drive privado foi conferido: os 13 ZIPs existentes de aquisição regional, QA e desenvolvimento já estavam gravados. Em complemento, o **coletor incremental dos 7 ZIPs nacionais** foi implementado e submetido a três testes unitários aprovados (download/reuso, ZIP corrompido, erro de rede), com manifesto idempotente e SHA-256/CRC por arquivo. [ZIP com script e testes no Drive privado](https://drive.google.com/file/d/1L_aQ1Zdh-_rNj_Hojg2f4vQzlIZ3bYO6/view), readback integral e metadados confirmados; [relatório de execução](INV_RMRP_COLETOR_NACIONAL_SICONV_EXECUCAO_2026_11_15.md). O runner tentou obter os três arquivos pequenos `siconv_coordenadas_obra`, `siconv_contrato_cipi` e `siconv_dados_obrasgov_geral`, mas todas as tentativas falharam com DNS `Temporary failure in name resolution`; **nenhum ZIP nacional foi recuperado ou inserido no Drive**. Próxima execução deve ocorrer em runner com DNS/HTTPS; arquivar fonte oficial com CRC/SHA256 e readback antes do FED04B e da conciliação FED03C. Sem promoção à produção.


### FED04B e FED03C — aquisição e recorte nacional real em 15/11/2026

O runner remoto com DNS/HTTPS funcional baixou e validou por SHA-256/CRC os **sete ZIPs nacionais** previstos. Três territoriais foram preservados no Drive com readback íntegro. No FED04B foram retidas 441 coordenadas de 265 propostas, 218 pontes projeto→instrumento→convênio→proposta e 336 associações candidatas, além de 150 linhas CIPI; 6 coordenadas requerem revisão geográfica. [Relatório FED04B](INV_RMRP_FED04B_DADOS_REAIS_QA_2026_11_15.md).

No FED03C, leitura de 7.575.512 pagamentos nacionais selecionou 28.503 movimentos de 1.286 convênios RMRP; dos arquivos OBTV, DL e itens DL resultaram respectivamente 395, 28.256 e 39.498 registros vinculados ao recorte. Banco SQLite derivado sem erros de integridade, nenhuma repetição de movimentos financeiros e sem somar pagamentos após junções 1:N. [Relatório FED03C](INV_RMRP_FED03C_PAGAMENTOS_REAIS_QA_2026_11_15.md) e [SQLite/QA privados](https://drive.google.com/file/d/1ZXhCXe-nDMadChIoV2QzoYHczBTigJsJ/view), readback SHA-256/CRC aprovado. ZIPs brutos nacionais de pagamentos, OBTV e DL já no Drive, arquivo bruto de itens DL ainda com upload grande pendente de confirmação. **Gates de publicação continuam fechados** até conciliação com estornos/CGU, natureza GND paga demonstrada, limites IBGE EPSG:4674 e comprovação física de localização. Nenhuma alteração do site produtivo.


### FED03D/FED04C — atualização do diagnóstico em 15/11/2026

**FED04C:** interseção espacial final da etapa exploratória com fonte IBGE 2024, 645 municípios SP, SIRGAS 2000 EPSG:4674: 381 pontos de propostas no município proponente, 49 em outros municípios RMRP, 5 em SP fora da RMRP, 4 fora de SP e 2 pontos `0,0`; 430/441 pontos da carteira de propostas dentro da RMRP; 216/218 projetos com associação a pelo menos um ponto interno. Interseção não homologa localização física de obra. **FED03D:** 28.503 pagamentos (1.286 instrumentos), R$ 627.287.678,10 em movimentos nominais brutos — não capital pago nem valor líquido; 22.318 movimentos `COM OBTV`, 395 linhas na tabela específica `siconv_obtv_convenente`, 33 pagamentos zero e 34 DL não ativos associados, sujeitos a revisão. [Relatório completo](INV_RMRP_FED03D_FED04C_AUDITORIA_REAL_2026_11_15.md). Fontes/SQLite/QA no Drive privado com readback SHA-256/CRC confirmado. **Gates restantes:** apurar estornos e natureza de despesa paga por documentação oficial; auditar pontos fora do município proponente e comprovar o local material das intervenções; homologar indicadores antes de atualizar API pública. Nenhuma promoção executada.


### FED04D/FED03E — triagem documental e espacial em 15/11/2026

Com base no SQLite real FED04C e na malha IBGE, as **441 coordenadas** foram classificadas por vínculo documental: **336** vinculadas a projetos Obrasgov, **24** a convênio sem projeto identificado e **81** a propostas sem convênio. Das 60 coordenadas divergentes do município proponente, 36 são de propostas sem convênio, 4 de convênio sem obra e apenas 20 de propostas com projeto Obrasgov. O maior agrupamento (30 pontos) é de uma proposta **rejeitada de Ribeirão Preto**, apontando Altinópolis; não projetar esses pontos como obras executadas. Do lado financeiro, 34 pagamentos com DL não `Ativo` foram segregados em 26 de valor zero e **8 positivos, somando R$ 272.120,91**, candidatos a verificação de documentos e estornos. [Relatório FED04D/FED03E](INV_RMRP_FED04D_FED03E_HIERARQUIA_EVIDENCIA_2026_11_15.md), [base SQLite, casos e QA no Drive privado](https://drive.google.com/file/d/1qQ2nidb5u3M8fXEULYhQoHBVKI_g4ETH/view), SHA-256/CRC de readback aprovados. O gate de classificação territorial/homologação financeira **permanece fechado**; próxima verificação deve abranger os 20 pontos divergentes com projeto vinculado e os oito pagamentos positivos ligados a DL não ativo. Nenhum deploy efetuado.


### FED07 — incorporação aditiva à prévia local, 16/11/2026

O pacote FED07 foi associado a uma **cópia privada** dos arquivos do frontend `app/static` sem alterar código público. Os seis JSON v3 preexistentes foram preservados; os **279 endpoints FED07** foram adicionados, totalizando **285** na pasta. Manifesto bloqueia publicação. A rotina de integração [`deployment/materialize_rmrp_fed07_private.py`](../deployment/materialize_rmrp_fed07_private.py) exige marcador privado e recusa sobrescrita ou escrita na árvore de produção. Testes: **1.603 verificações de API**, **33 testes de aplicação/regressão aprovados**, incluindo API v2 e SP645/TCESP. Arquivos no Drive: [ZIP de dados FED07](https://drive.google.com/file/d/1ZgwVepB-zpJGw3BsSPviYADy8PbMEdma/view) e [site de teste local integrado](https://drive.google.com/file/d/1whZO3RZABn9aIS3SrF5_8DqGdyBSwTZT/view), com CRC/SHA-256 verificados. [Relatório de homologação técnica parcial](INV_RMRP_FED07_HOMOLOGACAO_PARCIAL_PREVIA_API_2026_11_16.md). **Restam** homologação de natureza de capital paga, estornos, ponto físico de obra, QA do build remoto/visual e aceite dos dados TCESP de períodos históricos antes de release pública. Nenhum deploy realizado.


### FED08B/FED09 — natureza de empenho nos desembolsos, 16/11/2026

Adquiridos e preservados no Drive privado três ZIPs nacionais: `siconv_empenho`, `siconv_empenho_desembolso`, `siconv_empenho_cipi`; hashes e CRC de readback verificados. Foram localizados 2.486 empenhos de convênios RMRP, 2.592 links de grupos e 257 empenhos CIPI em 193 projetos. A conciliação dos 2.537 desembolsos aprovou 2.535 sem diferença, mantendo um sem ponte e um com divergência de R$ 88 mil. As naturezas `44`, `33`, `34` foram materializadas na **prévia privada FED09** por município, sub-região e exercício, sempre como **atributo do empenho relacionado ao desembolso**, não valor de capital pago ou despesa municipal executada. [Relatório FED08B](INV_RMRP_FED08B_EMPENHOS_DESEMBOLSOS_NATUREZA_2026_11_16.md), [FED09](INV_RMRP_FED09_PREVIA_NATUREZA_EMPENHO_2026_11_16.md) e [ZIP da plataforma privada](https://drive.google.com/file/d/1BpoxzYgVfTIQ7rIhsEQQGNUhG563EoHQ/view). QA: 1.603 checks de API e 288 HTTP local corretos, seis endpoints antigos preservados; sem deploy. Pendências: natureza efetivamente paga de cada favorecido, estornos, 808 inconsistências cronológicas de DL, 19 projetos com coordenada divergente, dois desembolsos incompletos e testes restritos de Pages/TCESP antes de release pública.


### FED08C/FED10 — fontes físicas de execução e evidência documental, 16/11/2026

Após a incorporação financeira FED09, houve aquisição e persistência no Drive privado de **cinco ZIPs oficiais**: execução física CIPI, medições e itens de medição, resumo físico-financeiro e projeto básico/SPA. O cruzamento com os **19 projetos Obrasgov** que possuem coordenadas de proposta divergentes identificou **15 com registros de execução física CIPI**, **12 com medições**, **7 com ao menos uma medição aceita**, **14 com resumo físico-financeiro**, **18 com projeto básico e SPA homologada**. Nenhum registro confere, isoladamente, localização física comprovada: a API permanece com **0 pontos homologados**. [Relatório FED08C/FED10](INV_RMRP_FED08C_FED10_EXECUCAO_FISICA_2026_11_16.md), [pacote privado individual](https://drive.google.com/file/d/1yZEUy-gV2z2auUtmqDQbWjU4agU5nP7R/view), [nova prévia FED10 integrada](https://drive.google.com/file/d/1OZ0Qpn6nch8R2WEQuBlsgoc1ZHu5m7HF/view), com hashes e CRC de readback aprovados. FED10 incluiu evidências em 19 projetos sem alterar financiamento GND4 (`null`) e sem publicar pins. QA: 1.603 checks de API e 288 HTTP local 200. Próxima prioridade: documentação georreferenciada específica dos 19 projetos, validação de valor/natureza de pagamento final e testes de Pages restritos. A release pública permanece bloqueada.


### FED11 — dois desembolsos inconciliáveis e fontes de localização, 16/11/2026

A conciliação histórica foi aprofundada com quatro ZIPs originais do Transferegov, salvos no Drive privado e verificados por readback SHA-256/CRC: `siconv_desembolso`, `siconv_inst_cont_metas_submetas_po_modulo_empresas`, `siconv_projeto_basico_metas_modulo_empresas` e `siconv_projeto_basico_submetas_modulo_empresas`. Um desembolso com diferença de **R$ 88.000,00** tem no mesmo convênio empenho `44` de igual valor, mas **não dispõe de vínculo oficial por ID_DESEMBOLSO**; hipótese documental a testar, não ajuste automático. Outro desembolso de R$ 194.720,80 tem comprovantes de registro SIAFI no CSV nacional mas segue sem ponte de empenho no módulo. Na tabela de metas contratuais (47.595 linhas nacionais), nenhuma das 19 propostas prioritárias tem correspondência por ID_PROPOSTA direto; próximas etapas devem reconstituir ponte entre ACFFO/QCI, metas, submetas e documentos geográficos, sem geocodificação presumida. [Relatório FED11](INV_RMRP_FED11_EXCECOES_DESEMBOLSOS_METAS_2026_11_16.md), [dois casos privados](https://drive.google.com/file/d/1bbAOkWv9C8XgvhvDnR5I6POvUDnFAQwz/view). A prévia FED10 privada está preservada; a ausência de navegador Chromium/Firefox/Playwright no runner foi constatada, logo permanece pendente QA visual de uma versão restrita do Pages. Nenhum campo de execução paga ou localização física foi promovido ao site público.
