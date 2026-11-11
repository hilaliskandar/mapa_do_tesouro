# INV-RMRP — Primeira varredura federais, provas de cobertura e prévias consultáveis

**Data:** 11/11/2026. **Região-piloto:** 34 municípios RMRP, cadastro com IBGE7 verificado na API IBGE. **Ambiente:** branch `investimentos-territoriais-sp645-20261111`; nenhuma modificação do banco canônico, R2, D1 ou publicação; PR #233 em rascunho.

## 1. Transferegov — leitura integral paginada, sem snapshot integral

A rota `/parcerias/proposta?cd_ibge_recebedor={IBGE}&pagina={p}&tamanho_da_pagina=200` e a rota `/discricionarias/propostas?cod_munic_ibge={IBGE}&pagina={p}&tamanho_da_pagina=200` responderam por **34 municípios**, **68 combinações município×módulo**, leitura em todas as páginas reportadas, sem falha HTTP, sem repetição de `id_proposta` dentro da mesma combinação, total retornado equivalente ao total declarado pela API.

| Módulo | Registros lidos | Limitação |
|---|---:|---|
| Gestão de Parcerias | **743** | Campo de categoria selecionado não preenchido nos 743, outras tabelas de despesa devem ser consultadas |
| Discricionárias e Legais | **6.410** | Categorias são declaradas por proposta e podem ser mistas, não pagamentos |
| **Soma entre módulos** | **7.153** | **Não** é total deduplicado de projetos, convênios, obras ou repasses |

A distribuição de `categorias_proposta` do módulo Discricionárias/Legais: 4.254 sem categoria; 318 Execução de Custeio; 824 Obras e Serviços de Engenharia; 814 Equipamentos; 49 Equipamentos + Obras; 127 Equipamentos + Custeio; 17 Custeio + Obras; sete Custeio + Equipamentos + Obras. Não inferir que os projetos estão celebrados ou pagos, nem que `categoria não informada` seja investimento.

**Limite da coleta nesta interação:** a paginação foi percorrida para computar contagens, categorias e amostras, mas **as 7.153 respostas individualizadas NÃO foram persistidas na íntegra**. Para viabilizar essa aquisição reprodutível, foi criado o coletor `pipeline/acquire/collect_investimentos_rmrp.py` que guarda cada página original em `gzip JSON` com hash SHA-256, checa chaves municipais/IDs, produz manifesto, contagem, erros e bloqueia QA quando parcial. Há workflow manual `.github/workflows/inv-rmrp-transferegov-staging.yml` que apenas gera **artefatos temporários de Actions**, sem deploy ou R2. **O workflow não foi executado nesta rodada**, e a disponibilidade de `workflow_dispatch` na branch não principal dependerá dos controles do GitHub; não confundir criação do arquivo com execução de coleta.

**Arquivos verificados:**
- [Contagens município×módulo](INV_RMRP_TRANSFEREGOV_CONTAGEM_34X2_2026_11_11.csv)
- [Varredura paginada e distribuição de categorias](INV_RMRP_TRANSFEREGOV_VARREDURA_CATEGORIAS_34X2_2026_11_11.csv)
- [Amostra de 200 propostas em JSON para prévia](../app/static/data/api/v3/investimentos/rmrp/preview-amostras.json): máximo de quatro registros por município/módulo que mencionam investimento/obra/equipamento ou têm categoria relacionada, **amostra intencional enviesada**, não representativa.

## 2. Obrasgov — busca por título, não filtro territorial homologado

A rota `/obras/projeto-investimento?uf_principal=SP&desc_nome={nome}&pagina={p}&tamanho_da_pagina=200` foi consultada para **34 municípios**, percorrendo as páginas informadas no filtro. Resultado: **224 registros com 224 IDs distintos**, entre os quais Ribeirão Preto (26), Dumont (15), Pontal (15), Sertãozinho (14), Batatais (13) e Jaboticabal (12). As consultas retornaram resposta sem erros de aquisição.

O endpoint fornece projeto, organização responsável, situação, `pins` e `investimentos_previstos` por fonte. O recorte é **textual**: um projeto situado em algum município pode não mencionar seu nome; palavras como `Pontal` podem se referir a outro lugar. **Todos os 224 são candidatos à territorialização, não 224 projetos homologados localizados na RMRP.**

Arquivo: [candidatos Obrasgov em JSON](../app/static/data/api/v3/investimentos/rmrp/obrasgov-busca-textual-candidatos.json) com os campos originais principais, ID, coordenadas, fontes previstas e `qa_status` explícito. **Não interpretar `investimentos_previstos` como pagamentos ou montante executado.**

**Etapa obrigatória para substituir busca textual:** enumerar o universo SP pelo endpoint (estimativa 20.942 registros informados pela API em 11/11/2026, mas sujeito a nova contagem e paginação), recuperar todos os pins e/ou geometrias, comparar com polígonos municipais oficiais e validar recortes plurimunicipais. A RMRP é filtrada depois da aquisição estadual para evitar falsos negativos.

## 3. Primeiras interfaces de consulta sem backend novo

- [`app/static/investimentos-rmrp-preview.html`](../app/static/investimentos-rmrp-preview.html): filtros por município, sub-região, módulo e termo, usa 200 propostas candidatas com origem e recorte explícito, e informa contagem da API mas **não soma planejamentos**.
- [`app/static/obrasgov-rmrp-preview.html`](../app/static/obrasgov-rmrp-preview.html): filtros por município citado, situação cadastral, fonte prevista e texto; mostra coordenadas e links à API original, sem territorialização validada.

Os arquivos foram **criados na branch de desenvolvimento**, não há prova de teste de navegador/deploy/QA frontend. Não é uma consulta já disponível na plataforma pública.

## 4. Prioridade de engenharia seguinte

1. **Executar e testar o coletor** de páginas Transferegov para 34×2, gerar artefatos integrais e hashes/readback; revisar falhas e o escopo dos dados pessoais públicos antes de eventual exposição. O coletor criado é proposta operacional, ainda não homologada por execução.
2. Criar coletor estadual Obrasgov, capturar páginas de SP com checkpoint/QA e recortar 34 municípios por geometria **EPSG:4674 no modelo**, sem simplificar o polígono municipal; preservar WGS84 na fonte.
3. Ler **Especiais / beneficiários, empenhos, ordens bancárias** e **Parcerias / parceria, empenho, ordem de pagamento**, vinculando só por identificador juridicamente robusto. Não atribuir pagamento apenas por município ou sem prova.
4. Adquirir **Convênios SP** e **liberações efetivas SIAFEM** por município/CNPJ/instrumento, incluindo estornos e classificação investimento/custeio.
5. Carregar **cópia de desenvolvimento** do SQLite com o SQL proposto; executar QA de FK, unicidade, etapas, anti-dupla contagem e 50 consultas; só então gerar JSON v3 completo e prévia navegável Cloudflare.
6. Manter FED04, PR #232, e produção estáveis enquanto esta PR #233 segue rascunho.

**Gates de publicação:** nenhuma amostra candidata é promovida como observação de investimento público executado sem instrumento, natureza da despesa, localização confirmada e prova financeira correspondente.
