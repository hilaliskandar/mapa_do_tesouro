# S00/S01 — primeiro ciclo de retomada sistêmica SP645

**Data:** 16/11/2026. **Estado:** documentação e descoberta inicial; não equivale a carga de microdados estaduais. **Branch:** `investimentos-territoriais-sp645-20261111`; PR #233 em draft.

## 1. Entregas realizadas

- Criado o catálogo inicial versionado em [`governance/controls/investimentos_sp645/`](controls/investimentos_sp645/), com `README.md`, `fontes.csv`, `endpoints.csv`, `execucoes.csv`, `snapshots.csv`, `cobertura.csv`, `pendencias.csv` e `conciliacoes.csv`.
- Registradas dez famílias de fontes prioritárias ou de referência, as duas páginas estaduais candidatas e pontos de auditoria federais. Os CSVs de execução, snapshot, cobertura e conciliação possuem **somente cabeçalho** até que ocorram coletas/QA com manifestos verificáveis; a ausência de linhas **não** representa ausência de transferências.
- Os estados federais permanecem declarados como resultados **documentados no histórico**, sem readback contemporâneo dos ZIPs privados ou validação completa dos conteúdos nesta execução. Isso mantém S00 aberto, com especial atenção às aquisições de 15/11 e complementos FED07–FED21.
- Não houve alteração no SQLite produtivo, R2, site público ou prévia privada. `public_release_authorized=false`.

## 2. Verificação de fontes estaduais em 16/11

### Portal da Transparência SP — Convênios

**Fonte oficial:** https://www.transparencia.sp.gov.br/Convenios

A página foi efetivamente recuperada pelo Crawl2AI; a consulta informa última atualização em **15/11/2026 11:03**. Identificados filtros de órgão/entidade, unidade, beneficiário, CNPJ, tipo de instrumento jurídico e ano de celebração. Há controles rotulados **Exportar CSV**, **Exportar PDF**, **Dados Abertos** e link a [dicionário XLSX](https://www.transparencia.sp.gov.br/Dicionarios/Dicion%C3%A1rio%20de%20dados_conv%C3%AAnios.xlsx). Na versão examinada, o seletor de anos apresenta 2023, 2024, 2025 e 2026. **Não se comprovou ainda o URL do CSV exportado, o volume total, o comportamento sem filtro ou a completude histórica**. Não foram baixados registros estaduais.

**Próximo teste:** inspecionar o mecanismo de download, testar CSV em lote sem filtros restritivos, conferir cabeçalhos, quantidade de linhas, identificadores, CNPJ e anos. Caso necessário, capturar o tráfego HTTP da consulta em navegador autenticado ou executor remoto, sem burlar controles de acesso.

### Sefaz-SP — Transferências Voluntárias / SIAFEM

**Fonte oficial:** https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx

A rota foi acessada pelo Crawl2AI, mas o Markdown extraído trouxe apenas a navegação da interface. Em leitura web oficial complementar, a página declarou dados atualizados até **15/11/2026**, registros de convênios com alguma liberação financeira **desde agosto/2007** e valores negativos para **cancelamentos ou estornos**. A consulta possui filtros por região administrativa, município, órgão, convenente/CNPJ, datas e valores de convênio e de liberação, beneficiado (prefeituras/entidades) e natureza (custeio/investimento). As páginas de resumos [por órgão](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Orgao.aspx) e [por região administrativa](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/RegiaoBeneficiadoNovo.aspx) são acessíveis e exibem agregados, mas não substituem o conjunto de **parcelas individuais com chaves e datas**. A extração em lote, API ou formato exportável permanece **não demonstrada**.

**Próximo teste:** identificar formulário ASP.NET, parâmetros de postback, controles e eventuais endpoints oficiais, validar obtenção de linhas de convênio e liberação com estornos. Preservar os campos de classificação Investimento/Custeio, beneficiário, CNPJ, data de liberação e número do convênio. Não confundir região administrativa de Ribeirão Preto com os 34 municípios da RMRP.

## 3. Gates ainda abertos

| Gate | Estado documentado | Próxima operação |
|---|---|---|
| S00 — Readback e inventário de pacotes | Parcial: referências FED e acervo histórico localizados; sem auditoria nova de conteúdo dos ZIPs | Conferir Drive/R2/manifestos, hashes e correspondência de volumes |
| S01 — Catálogo de fontes | Inicializado; dez famílias e seis rotas candidatas registradas | Completar dicionários, OpenAPI, limites, autenticação e histórico |
| S03 — Convênios SP | Página oficial e controles CSV confirmados | Baixar e validar CSV nacional/estadual; conferir abrangência |
| S03 — Sefaz-SP | Página e filtros identificados; extração em lote pendente | Validar protocolo de consulta e extrair eventos |
| S02 — Federal complementar | Dados anteriores documentados; lacunas de modalidades continuam | Checar efetivo acervo federal, priorizar API/CSV de alta cobertura |
| S05–S07 — integração | Sem nova integração neste ciclo | Iniciar após as primeiras tabelas estaduais normalizadas |

## 4. Critérios de QA para o primeiro arquivo estadual real

Um arquivo só poderá ter `qa_status=validado_estrutura` após registro de URL completa ou parâmetros, janela temporal, momento da coleta, HTTP, tamanho, SHA-256, dicionário, número de linhas, campos obrigatórios e identidade de fonte. `conciliado` requer teste de identificador de instrumento, cardinalidade, deduplicação, estornos e valores por exercício. `homologado` requer demonstração de ausência de soma cruzada com FINBRA/TCESP e classificação correta do estágio financeiro. Valores sem comprovação continuam `null`.

## 5. Prioridade imediata da próxima rodada

1. Resolver a exportação CSV do Portal da Transparência SP.
2. Testar obtenção de dados de liberação da Sefaz-SP em lote, incluindo convenente/município e classificação custeio/investimento.
3. Auditar arquivos federais já disponíveis, sem downloads redundantes.
4. Registrar as primeiras execuções reais nos controles CSV e preparar tabela `SP_CONV` e `SP_SEFAZ` em SQLite isolado.
5. Somente então ampliar o painel RMRP, sem bloquear por 19 projetos territorialmente controversos.

**Referência de direção:** [plano operacional SP645](PLANO_OPERACIONAL_COLETA_SISTEMATICA_TRANSFERENCIAS_SP645_2026_11_16.md). **Conservação:** resultados e exceções FED01–FED21 permanecem no README e nos relatórios, não foram eliminados.
