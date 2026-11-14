# INV-RMRP — Reorientação: investimentos territoriais com Transferegov como fonte primária
**Data:** 12/11/2026  
**Escopo:** 34 municípios da RMRP; extração comparável por bases oficiais; fase de definição e auditoria metodológica.  
**Situação:** metodologia documentada, **sem nova ingestão Transferegov neste registro**. Não alterar dados homologados, snapshots R2, SQLite/D1, publicações nem outros PRs.

## Decisão vinculante de escopo
O objeto principal é **investimento federal e estadual no território municipal**, NÃO toda transferência intergovernamental, receita corrente, FPM, ICMS, gasto de custeio ou notícia de obra.

**Ordem obrigatória**: 1) dados oficiais estruturados; 2) extração uniforme de todas as unidades territoriais; 3) controle de cobertura e integridade; 4) classificação de investimento; 5) conciliação de instrumentos e estágios financeiros; 6) documentação individual apenas para divergências ou aprofundamento. Não iniciar uma fila indiscriminada de notícias, PDFs municipais ou buscas por projetos.

## Transferegov: primeiro gate obrigatório
Fonte principal: https://api-publica.transferegov.gestao.gov.br/ ; catálogo de CSV do módulo Discricionárias e Legais: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados .

**Estado oficial verificado em 12/11/2026:** em 28/10/2026 foi anunciada a primeira entrega da nova API Discricionárias e Legais, relativa a *atos preparatórios*. Instrumentos e execução financeira permanecem em implantação gradual. Portanto, **não substituir o histórico CSV pela API incompleta**. As APIs de Transferências Especiais e Gestão de Parcerias exigem inventário independente de endpoints, campos, paginação e cobertura.

Arquivos CSV do Discricionárias e Legais a inspecionar e processar por chave de origem: Convênios; Propostas; Plano de Aplicação Detalhado; Emendas Parlamentares; Empenhos Realizados; Desembolsos/Ordem Bancária; Pagamentos a Favorecidos; OBTV; Meta/Cronograma Físico; aditivos. Capturar e documentar URLs efetivas, nomes dos arquivos, data do snapshot, layout real e SHA-256 antes de programar junções. **Arquivo listado no catálogo não equivale a download ou QA concluído.**

### Sequência de aquisição
1. Verificar disponibilidade e esquema dos arquivos nacionais integrais, sem fazer 34 consultas ad hoc, preservando bytes brutos e hash.
2. Ler os arquivos e dicionários reais e determinar chaves de proposta, instrumento, plano, empenho, ordem bancária, favorecido e município; não deduzir nomes de colunas.
3. Selecionar os 34 municípios por IBGE e, quando a fonte não fornece IBGE, executar correspondência municipal controlada com código/UF e registro das ambiguidades.
4. Preservar distinção entre município proponente/beneficiário, município executor e localização de obra. Um convênio plurimunicipal não pode ser automaticamente atribuído integralmente a cada local.
5. Classificar parcelas de capital por natureza da despesa ou plano de aplicação; quando não individualizável, status `investimento_nao_confirmado`, sem somá-la aos investimentos confirmados.
6. Disponibilizar tabelas independentes de **valor pactuado**, **empenho**, **desembolso/pagamento federal**, **aplicação documentada** e **investimento físico territorial**. Não somar esses estágios.
7. Reconciliar a camada Obrasgov apenas mediante chave explícita ou evidência documental; não somar novamente a obra a seu financiamento.
8. Publicar uma matriz de QA fonte × modalidade × exercício × município, com contagem bruta, selecionada, classificada, pendente, erros e data de extração.

### Transferências especiais
Analisar as emendas e pagamentos no módulo próprio; separar destino declarado, empenho, pagamento e comprovação da **parcela de capital**. A mera transferência especial não prova investimento. Preservar registros sem natureza comprovável fora da métrica principal.

## Fontes complementares e limites
- **Obrasgov:** camada de obra física federal localizada; pode não cobrir todos os investimentos e **não** equivale a ingresso em caixa municipal.
- **Fazenda SP / Transparência SP (SIAFEM):** liberação de transferência estadual, com classificação de objetos e natureza de capital a verificar; convênios de custeio não integram o agregado de investimentos.
- **Outros órgãos federais/estaduais:** somente para modalidades de investimento comprovadamente não abrangidas pelas fontes centrais, com metadados e limites; evitar inventário indiferenciado de repasses correntes.
- **DCA/Siconfi/TCESP:** conciliação das despesas municipais de capital/receitas de capital por conceito contábil e exercício; não equiparar transferência da União ao investimento liquidado pela Prefeitura.
- **Notícias, comunicados e PDFs individuais:** evidência complementar, nunca método principal de cobertura.

## Contrato mínimo de dados
Manter chaves `source_system`, `module`, `source_record_id`, `instrument_id`, `municipality_ibge7`, `beneficiary_id`, `execution_location`, `fiscal_year`, `event_date`, `financial_stage`, `expense_category`, `amount_nominal`, `classification_status`, `source_url`, `snapshot_date`, `sha256`, `qa_status`. Conservar campos originais em estrutura bruta. Cada linha monetária deve ter unidade e semântica inequívocas; números de termo, proposta, convênio e ordem bancária não são a mesma chave.

## Gate prioritário e entregáveis
**INV-FED00:** matriz auditada de arquivos Transferegov, endpoints e cobertura histórica real. Aprovação exige ao menos um arquivo oficial obtido e analisado com layout, hash e chave de ligação documentados, mais plano verificável para os demais arquivos; documentação isolada NÃO aprova extração.

**INV-FED01:** download integral nacional, normalização e seleção RMRP 34/34, matriz município-ano-modalidade e exclusões de custeio, com QA de zero/ausente.

**INV-FED02:** conciliação proposta → instrumento → eventos financeiros → aplicação de capital, sem duplicação e com incertezas registradas.

**INV-EST00:** auditar a base estadual SIAFEM já coletada; separar desembolsos de **investimentos confirmados** e evitar apresentar a soma integral de convênios como investimentos.

**INV-TER00:** obras federais e estaduais executadas diretamente no território, em camada autônoma e sem aditividade automática.

**INV-REL00:** séries comparáveis por município/sub-região, inflação ajustada com convenção do estudo, valores absolutos e per capita, percentuais de cobertura e painel de qualidade.

## Reaproveitamento do projeto e não regressão
A branch `investimentos-territoriais-sp645-20261111` e o PR #233 já contêm acervo SIAFEM RMRP, sondagens Obrasgov e diversas investigações de contratos. **Não apagar o acervo**. Porém o inventário estadual de R$ 305.521.029,20 em liberações/estornos, 2020–12/11/2026, conforme README da própria branch, **não pode ser rotulado como investimento confirmado**, pois inclui registros ainda sem classificação contábil e conciliação física. Revisar o vocabulário e os indicadores antes de comparação com investimento municipal.

A pesquisa por documentos específicos de Serrana, Batatais, Ribeirão Preto e Pradópolis deve ficar subordinada aos casos selecionados pelas bases administrativas; suspender a expansão generalizada da fila de 752 chaves estaduais até concluir a extração federal estruturada. Preservar as erratas e controles de não dupla contagem já homologados.

## Situação e limitações desta rodada
- Documentação oficial do Transferegov e estado da API consultados em 12/11/2026.
- Tentativa de download via ambiente de execução local: falha DNS de `repositorio.dados.gov.br`. Tentativa Crawl2AI das páginas oficiais: falha interna; acesso à documentação confirmado via consulta web.
- **Nenhum CSV de dados Transferegov foi extraído ou classificado nesta rodada; não há contagem ou valores novos.**
- Próxima ação exata: obter o índice e os ZIP/CSV nacionais reais de Convênios, Plano de Aplicação, Desembolsos e Pagamentos pelo runner GitHub Actions ou via conector funcional; produzir manifesto de arquivos e um piloto de extração RMRP completo. Não começar por busca documental municipal.

## Fontes oficiais verificadas
1. Portal APIs: https://api-publica.transferegov.gestao.gov.br/
2. Catálogo CSV: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados
3. Comunicado da API de 28/10/2026: https://www.gov.br/transferegov/pt-br/noticias/noticias/2026/outubro/transferegov-disponibiliza-nova-api-de-dados-abertos
4. Cronograma oficial: https://www.gov.br/transferegov/pt-br/comunicados/comunicados-gerais/2026/comunicado-24-2026-cronograma-de-disponibilizacao-da-apis-de-dados-abertos-do-discricionarias-legais

## Execução complementar de 13/11/2026 — endereço oficial funcional e piloto isolado
- O endereço **operacional verificado em Browserless** para catálogo de downloads é `https://api-publica.transferegov.gestao.gov.br/downloads`; não usar links antigos `repositorio.dados.gov.br/seges/detru/`, descontinuados em 31/08/2026. Endereço atual do arquivo: `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/{nome}.zip`.
- A página retornou HTTP 200, lista de **65 arquivos ZIP**, com data de atualização exibida 12/11/2026. Existem, entre outros, `siconv_convenio.zip` (17,6 MB exibidos), `siconv_desembolso.zip` (16,1 MB), `siconv_emenda.zip` (7,9 MB), `siconv_empenho.zip` (22,5 MB), `siconv_plano_aplicacao_detalhado.zip` (279,9 MB) e `siconv_pagamento.zip` (357,3 MB). Os tamanhos são metadados do catálogo, não atestado de download integral de todos.
- Teste de download **efetivo** de `siconv_convenio.zip` via navegador remoto: HTTP 200, **18.501.744 bytes ZIP**, membro único `siconv_convenio.csv` (71.002.033 bytes descompactados), método ZIP deflate. Até este ponto só foram verificadas metainformações ZIP; **cabeçalho, número de linhas, filtro de RMRP, classificação do plano de capital e valores ainda não foram verificados**.
- A leitura integral por navegador remoto encontrou restrição HTTP **429 Too Many Requests** em tentativa subsequente. O runtime local continua sem resolução DNS; isso **não invalida o endereço oficial já testado**, mas torna necessário executar a leitura dos CSVs em ambiente de rede adequado, como GitHub Actions.
- Coletor de arquivos ZIP com manifesto/hash, leitura em streaming e seleção territorial **somente por coluna IBGE explícita**: [`pipeline/acquire/inv_rmrp_transferegov_zip.py`](../pipeline/acquire/inv_rmrp_transferegov_zip.py), commits `3a7001b4` e `bf75a61a`. Se um arquivo não trouxer IBGE7 direto, o status é `schema_only_requires_territory_crosswalk`, e não se afirma ausência de municípios. Não somar resultados até confirmar chave de proposta/instrumento e natureza da despesa.
- Workflow de aquisição-piloto em branch, somente `siconv_convenio`, `siconv_desembolso`, `siconv_emenda`, com artefatos de QA e CSV territorial selecionado: [`.github/workflows/inv-rmrp-transferegov-smoke.yml`](../.github/workflows/inv-rmrp-transferegov-smoke.yml), commit `b7bb78b5`. A existência do workflow **não comprova que uma execução tenha sido concluída**. Nenhum dado Transferegov foi incorporado à base canônica, nem houve promoção pública.
- Próximo gate: inspecionar resultado do workflow, validar formato e nomes de colunas reais, eventualmente construir crosswalk por ID de instrumento/proposta, conferir a cobertura 34/34 e só então ampliar plano de aplicação e pagamento, conservando distinção de despesa de capital.

## Resultados confirmados dos workflows de 13/11/2026
**Smoke oficial 1:** [run 43409135374](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43409135374), `success`. Arquivos nacionais efetivamente baixados e processados:
- `siconv_convenio.csv`: **288.852** registros; estrutura inclui `NR_CONVENIO`, `ID_PROPOSTA` e campos de valores pactuados/empenhados/desembolsados. Não possui chave IBGE direta no layout lido.
- `siconv_desembolso.csv`: **386.864** registros; precisa de crosswalk de instrumento para municipalização.
- `siconv_emenda.csv`: **298.538** registros; precisa de crosswalk de proposta/instrumento para municipalização.
- Total **974.254 linhas fonte**, incluindo classes de registro distintas, **não** obras, investimentos ou transferências somáveis. Os três status `schema_only_requires_territory_crosswalk` são apropriados; `selected=0` no primeiro smoke **não significa ausência de instrumentos**.

**Smoke oficial 2:** [run 43410911718](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43410911718), `success`. Arquivo `siconv_proposta.csv`: **1.160.558 registros nacionais**, dos quais **6.410 linhas** com `COD_MUNIC_IBGE` dos **34 municípios RMRP**, e `UF_PROPONENTE=SP` disponível para controle. Cabeçalho observado contém `ID_PROPOSTA`, `UF_PROPONENTE`, `MUNIC_PROPONENTE`, `COD_MUNIC_IBGE`, `MODALIDADE`, `IDENTIF_PROPONENTE`, `SIT_PROPOSTA`, `OBJETO_PROPOSTA`, `ITEM_INVESTIMENTO`, `VL_GLOBAL_PROP`, `VL_REPASSE_PROP`. Os **34/34 municípios possuem propostas** nessa base, mas isto não prova convênio assinado ou desembolso. Artefato temporário [14029657053](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43410911718/artifacts/14029657053).

**Decisão técnica:** territorializar primeiro propostas por `COD_MUNIC_IBGE`, depois vincular `siconv_convenio` por `ID_PROPOSTA`, e `siconv_desembolso` e `siconv_emenda` exclusivamente por IDs oficiais de proposta ou número de convênio (se presentes no respectivo layout). Registrar separadamente **município do proponente** e **município de execução**; não presumir coincidência. Campo `ITEM_INVESTIMENTO` não substitui uma auditoria contábil da parcela de capital.

**Implementação de junção (ainda sujeita a homologação):** [coletor crosswalk](../pipeline/acquire/inv_rmrp_transferegov_join.py) commit `fa76f2fb`, [workflow isolado](../.github/workflows/inv-rmrp-transferegov-join.yml) commit `ca7e53d4`. O crosswalk não gera totais financeiros e falha diante de chaves conflitantes. A execução deve ser inspecionada antes de afirmar resultados.

## Cruzamento oficial de quatro conjuntos — 13/11/2026
**Execução:** [GitHub Actions 43411132741](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43411132741), `success`. A ingestão ocorreu **somente em diretório temporário no runner**, com manifesto e CSVs RMRP arquivados como artefato do Actions, sem alterar R2/SQLite/D1 ou APIs de produção.

| Arquivo oficial | Registros nacionais | Registros vinculados RMRP | Chave de ligação | Cobertura entre 34 proponentes |
|---|---:|---:|---|---:|
| siconv_proposta | 1.160.558 | 6.410 | COD_MUNIC_IBGE | 34/34 |
| siconv_convenio | 288.852 | 1.793 | ID_PROPOSTA | 34/34 |
| siconv_desembolso | 386.864 | 2.537 | NR_CONVENIO validado na camada de convênios | 34/34 |
| siconv_emenda | 298.538 | 1.240 | ID_PROPOSTA | 34/34 |

**Controle de duplicidades:** na amostra de 6.410 propostas vinculadas há 6.410 `ID_PROPOSTA` distintos e zero conflitos de IBGE na chave de proposta. Isto não certifica unicidade jurídica das demais classes, mas demonstra ligação por chave administrativa, em vez de inferência por nome, município ou valores. `siconv_desembolso` tem colunas `ID_DESEMBOLSO`, `NR_CONVENIO`, `DATA_DESEMBOLSO`, `ANO_DESEMBOLSO`, `VL_DESEMBOLSADO`. `siconv_emenda` contém `ID_PROPOSTA`, `NR_EMENDA`, `VALOR_REPASSE_PROPOSTA_EMENDA` e `VALOR_REPASSE_EMENDA`.

**Interpretação:** os 1.793 são linhas na tabela de convênios associadas a proponentes dos 34 municípios; os 2.537 são eventos de desembolso e os 1.240 são linhas de emendas, não totais monetários nem investimentos realizados. A seleção é pelo **município do proponente**. Projetos estaduais, consórcios sediados fora da RMRP ou execução física no território podem exigir territorialização adicional e não estão incluídos automaticamente. Desembolsos precisam ser associados às parcelas de capital dos planos de aplicação antes de qualquer total de investimento.

**Próximo gate:** sondagem do layout do arquivo nacional `siconv_plano_aplicacao_detalhado` e teste de junção com `ID_PROPOSTA` ou `NR_CONVENIO`, verificando classificadores oficiais de natureza da despesa/itens. Não derivar investimento apenas da palavra `ITEM_INVESTIMENTO` e não inferir parcela de capital proporcional quando houver mistura custeio/capital.

## Resultados do Plano de Aplicação Detalhado — 13/11/2026
**Execução oficial:** [run 43411550312](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43411550312) `success`, artefato temporário [14029941642](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43411550312/artifacts/14029941642), SHA-256 do ZIP do artefato `cd244eddfa4e3122ff13c882986fa05c6a28cf7aada77fbdf4b4c5664a13bfa6`. Fonte: ZIP oficial `siconv_plano_aplicacao_detalhado`, junção exata de `ID_PROPOSTA` com 6.410 propostas RMRP por `COD_MUNIC_IBGE`.

- **4.917.545** itens de plano nacionais; **28.456** itens vinculados aos **34 municípios proponentes** da RMRP.
- Triagem dos itens por `COD_NATUREZA_DESPESA`, categoria econômica inicial: **16.493** `candidato_capital`; **11.920** `candidato_corrente`; **43** `indeterminado`. A soma é 28.456.
- **0** linhas com `ID_ITEM_PAD` vazio; **0** linhas com identificador `ID_ITEM_PAD` repetido no recorte selecionado. Unicidade não significa que todas as versões e valores possam ser somados sem revisão da situação dos itens.
- `SIGLA` da localização do item: **28.290 itens SP** e **166 itens nas demais UFs** (DF 22, MG 6, BA 48, CE 3, TO 8, PA 3, MS 4, RO 4, MT 7, AC 4, AM 36, RN 19, RS 2). A localização do item **não** pode ser equiparada ao município proponente, mesmo quando está dentro de SP.
- Códigos mais frequentes no conjunto selecionado: `44905199` (4.378 itens), `33903999` (2.569), `44905208` (2.155), `44905299` (1.908), `33903099` (1.332). Estes são códigos observados; nomes e semântica de cada desdobramento requerem dicionário oficial e validação da codificação utilizada no Transferegov.
- **Não foi somado `VALOR_TOTAL_ITEM`**. Trata-se de **itens de aplicação planejada**, não de pagamentos ou investimentos liquidados. O resultado **não** autoriza atribuir integralmente os eventos de desembolso aos itens de capital de um mesmo convênio.
- A classificação por primeiro dígito da natureza (3 corrente, 4 capital) é **triagem provisória**, a ser conferida por fonte e exercício; os 43 códigos indeterminados precisam ser examinados e os 166 itens localizados fora de SP devem ser separados.
- Código de seleção: [`pipeline/acquire/inv_rmrp_transferegov_plano.py`](../pipeline/acquire/inv_rmrp_transferegov_plano.py). Workflow: [`inv-rmrp-transferegov-plano.yml`](../.github/workflows/inv-rmrp-transferegov-plano.yml). Os resultados estão apenas no artefato temporário de Actions; ainda falta um snapshot durável aprovado em R2 com manifesto e readback, além da conciliação de valores.

**Próximo gate técnico:** inspecionar a distribuição `SIT_ITEM` e a validade dos 43 indeterminados, verificar dicionário oficial de `COD_NATUREZA_DESPESA`, identificar itens com divergência territorial e apurar valores **somente depois** de homologar escopo de planos e campos. Reconciliar eventual parcela de capital com movimentos de desembolso em nível de instrumento, sem rateios arbitrários nem dupla contagem.

## Refinamento da classificação GND e estado dos itens — 13/11/2026
A execução [43411817563](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43411817563) concluiu `success` a reclassificação dos mesmos **28.456 itens** do Plano de Aplicação para os 34 municípios proponentes:
- **16.156** itens `candidato_investimento_gnd4` (código `44...`, grupo Investimentos);
- **287** itens `capital_inversao_financeira_gnd5` (`45...`);
- **50** itens `capital_amortizacao_divida_gnd6` (`46...`);
- **11.920** itens de despesa corrente (`3...`);
- **43** indeterminados, **todos com código `99999999`**.
A soma dos três grupos de capital (16.156+287+50) corresponde aos **16.493** anteriormente classificados como `candidato_capital`. **NÃO divulgar os 16.493 como investimentos**, pois 337 itens pertencem a outros GNDs de capital; mesmo os 16.156 do GND 4 representam natureza planejada, não execução financeira comprovada.

**`SIT_ITEM` observado:** `APROVADO` **15.342** itens; `EM_COMPLEMENTACAO` **217**; campo vazio **12.897**. A classificação de natureza deve ser cruzada com a situação administrativa antes de aprovar qualquer valor. Campo vazio **não** é aprovado por presunção. Não foram detectados IDs de item duplicados ou vazios no recorte.

**Territorialização:** 166 itens pertencem a propostas vinculadas a proponentes RMRP, mas registram localização do item fora do estado de São Paulo. Exemplo verificável: proposta `771446` do proponente Ribeirão Preto possui itens localizados em Palmas/TO, Marabá/PA, Campo Grande/MS, Parecis/RO, Barra do Garças/MT e Salvador/BA. **Não atribuir automaticamente esses itens como investimentos fisicamente realizados na RMRP.** A localização dentro de SP, por si, também não comprova estar dentro dos 34 municípios; validar `MUNICIPIO` com código territorial.

**Próximo controle exigido:** definir coorte com GND 4 e situação aprovada, homologar categoria com classificação oficial, tratar os 43 códigos `99999999`, resolver localização física dos itens (inclusive os 166 externos a SP) e identificar eventual gasto territorial realizado diretamente por outro ente. Somente então poderão ser tabulados valores de aplicação *prevista*, separados de pagamentos federais efetivos e de investimentos liquidados no orçamento municipal. Preservar origem e SHA-256 dos arquivos; não produzir soma inferencial de `VALOR_TOTAL_ITEM` e `VL_DESEMBOLSADO`.
