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
