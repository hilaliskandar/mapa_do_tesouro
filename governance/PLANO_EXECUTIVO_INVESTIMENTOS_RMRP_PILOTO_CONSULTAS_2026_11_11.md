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
