# INV-RMRP — Recuperação auditada das transferências estaduais de investimento no SIAFEM/SP

**Data de consulta:** 12/11/2026. **Fonte oficial:** https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx. **Atualização exibida pelo sistema:** 12/11/2026. **Método:** navegador Browserless abriu o formulário ASP.NET; o POST com campos reais (incluindo estado da sessão) retornou a tabela grdTransferencia. A leitura textual do Crawl2AI havia recebido erro ASP.NET e não foi usada como prova de ausência de dados.

## Parâmetros exatos

- Municipio: cada um dos **34 municípios da RMRP**, selecionado individualmente na lista do próprio SIAFEM; Brodowski aparece na interface como BRODOSQUI. Territorialização mantida por IBGE7 do cadastro homologado.
- LiberacaoInicio = 01/01/2020; sem data final explícita (fonte atualizada até 12/11/2026).
- Beneficiado = Prefeituras; Tipo = Investimento.
- Não aplicar recorte Região Administrativa = RIBEIRAO PRETO, pois não equivale ao conjunto de 34 municípios metropolitanos.

## Resultado integral da consulta por convênio

- **752 convênios**, com cobertura **34/34 municípios**, distribuídos em dois lotes de 17 municípios, sem erro de consulta.
- **R$ 362.933.954,59**: soma de Valor Convênio da consulta. **R$ 305.521.029,20**: soma de Valor Liberado/Estornado, com preservação de centavos. NÃO somar os dois montantes entre si.
- **QA:** somas por linha reproduziram exatamente os totais oficiais de cada um dos 34 municípios; diferença regional **R$ 0,00**; zero chaves municipais repetidas na combinação codigo_ibge + numero_convenio_siafem. Nenhuma linha agregada apresenta valor liberado/estornado negativo, o que não exclui estornos internos em lançamentos individuais.
- A filtragem por data de liberação alcança convênios anteriores a 2020, desde que tenham liberações no período. **NÃO usar o ano da celebração para séries anuais de transferências**.
- Beneficiário “PREF. MUNICIPAL DE TAQUARAL” em 13 registros: abreviação nominal admitida pelo próprio filtro “Prefeituras” do SIAFEM, não indício de entidade privada.

### Totais por sub-região

| Sub-região | Municípios | Convênios | Valor liberado/estornado |
|---|---:|---:|---:|
| Ribeirão Preto | 15 | 324 | R$ 154.667.688,89 |
| Batatais | 7 | 162 | R$ 62.651.029,72 |
| Jaboticabal | 6 | 153 | R$ 53.353.392,85 |
| Mococa | 6 | 113 | R$ 34.848.917,74 |
| **RMRP** | **34** | **752** | **R$ 305.521.029,20** |

### Maiores totais municipais de valores liberados/estornados

Ribeirão Preto R$ 30.967.747,17 (41 convênios); Pradópolis R$ 20.063.468,96 (32); Santa Rita do Passa Quatro R$ 18.303.139,81 (31); Batatais R$ 16.972.500,88 (27); Sertãozinho R$ 16.865.491,90 (39). A comparação é descritiva, sem normalização por população ou necessidades territoriais.

## Arquivos versionados

- governance/INV_RMRP_SIAFEM_INVESTIMENTO_2020_LOTE_01_2026_11_12.csv: 338 registros / 17 municípios.
- governance/INV_RMRP_SIAFEM_INVESTIMENTO_2020_LOTE_02_2026_11_12.csv: 414 registros / 17 municípios.
- governance/INV_RMRP_SIAFEM_INVESTIMENTO_2020_LOTE_01_QA_2026_11_12.json e correspondente LOTE_02: totalizadores originais por município e parâmetros da consulta.
- governance/INV_RMRP_SIAFEM_ALTINOPOLIS_EVENTOS_PAGAMENTO_PILOTO_2026_11_12.csv: 32 eventos individualizados de 17/18 instrumentos selecionados; um instrumento (5128032684769\\19) retornou HTTP 500 na URL de detalhes.

## QA das páginas individuais de convênio

Página oficial exemplificativa: https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=13010111442%2F2020, com data 29/12/2020, modalidade INVESTIMENTO e item TRANSF.A MUNICIPIOS-EQUIP.MATER.PERMANENTE. Há objeto, órgão, status, valor e grade de eventos financeiros por data.

**Ponto decisivo:** a página individual retorna também lançamentos anteriores a 01/01/2020 em convênios com liberações posteriores a essa data. Exemplo: convênio 1700301313178/17 possui eventos em 2019, 2020, 2021 e 2022; a tabela resumida com filtro 2020+ apresenta R$ 574.858,77. Portanto, o processamento detalhado deverá filtrar as datas dos próprios eventos para conciliar com os totais de período. Valores individuais exibidos na coluna podem aparecer sem centavos (arredondados ou truncados na renderização), de modo que a precisão da coluna agregada não deve ser substituída por soma de valores textuais individualizados sem reconciliação.

**Erro documentado:** a página individual de 5128032684769\\19 devolveu HTTP 500 nesta rodada. Não significa inexistência de pagamentos, e não afeta o registro resumido do instrumento no primeiro lote.

## Distinção em relação ao Portal da Transparência

O ZIP https://www.transparencia.sp.gov.br/Dados%20Abertos/Convenios/convenio.zip foi baixado e descompactado; SHA-256 **1cca0556f08a1378bae52465796188788a5b3bb21e1b26c30c8c5c7d9a6b2b8f**, 188.630 bytes compactados, 983.141 bytes descompactados, 3.618 registros de dez colunas, sem cabeçalho. O pareamento nominal encontrou 66 linhas de 25 prefeituras da RMRP em 2023-2026 (arquivo INV_RMRP_CONVENIOS_ESTADUAIS_66_REGISTROS_BRUTOS_2026_11_12.csv). Essa fonte NÃO substitui o SIAFEM: contém instrumentos celebrados, não a série comprovada de liberações. O dicionário separa valor total previsto de valor efetivamente concedido, mas não esclarece a semântica da única coluna numérica do CSV sem cabeçalho; valores brutos foram preservados, **sem conversão monetária presumida**.

## Restrições de uso e gates

1. Total regional de R$ 305,52 milhões equivale a liberações/estornos de investimento para prefeituras no SIAFEM conforme filtros e atualização de 12/11/2026. Não comprova aplicação final, obra concluída nem investimento realizado pela prefeitura; não deve ser somado à despesa municipal de capital como se fosse gasto adicional.
2. Confirmar série de eventos financeiros individualizados (data, valor, item e natureza), com tratamento de estornos e HTTP 500; reconciliar valores agregados por período e possível perda de centavos da exibição detalhada.
3. Integrar esses instrumentos ao SQLite real em **cópia isolada**, com fontes e chaves oficiais, preservando séries TCESP.
4. Não promover o ZIP de convênios celebrados a desembolsos e não somar SIAFEM + convênios + execução municipal.
5. PR #233 em draft, sem merge nem mutação da base produtiva. FED04/PR #232 permanece preservada.
