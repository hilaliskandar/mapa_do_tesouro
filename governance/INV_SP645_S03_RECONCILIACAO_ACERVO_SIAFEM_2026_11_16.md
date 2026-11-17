# S03 — Reconciliação do acervo SIAFEM preexistente e aquisição piloto 16/11/2026

**Data:** 16/11/2026. **Finalidade:** corrigir o inventário operacional e evitar retrabalho na coleta estadual. **Status:** correção documentada, sem alteração na produção.

## 1. Correção da fotografia de cobertura

O catálogo inicial aberto em 16/11 indicava a Sefaz/SP apenas como página acessível e fonte cuja extração ainda seria criada. Essa descrição foi **incompleta**: existia, desde **12/11/2026**, coleta substancial, reconciliada e documentada da fonte oficial [SIAFEM/Transferências Voluntárias](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx).

**Conjunto anterior com prioridade canônica para a RMRP:**

- `governance/RELATORIO_INV_RMRP_SIAFEM_SERIE_ANUAL_EXATA_2020_2026_2026_11_12.md`
- `governance/INV_RMRP_SIAFEM_2020_2026_ANUAL_EXATO_QA_2026_11_12.json`
- `governance/INV_RMRP_SIAFEM_34_MUNICIPIOS_2020_2026_ANUAL_EXATO_2026_11_12.csv`
- `governance/INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv`
- `governance/inv_rmrp_siafem_anuais_exatos/lote_01...lote_05_2026_11_12.json`
- `governance/INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv`
- `pipeline/build/import_inv_rmrp_siafem_dev.py`
- `app/static/data/api/v3/investimentos/rmrp/siafem-sp-investimentos-anual-preview.json`

O relatório oficial interno comprova **238 consultas bem-sucedidas (34 municípios × 7 exercícios de 2020 a 2026)**, **752 convênios**, **889 registros convênio-ano**, **1.017 pagamentos**, e **R$ 305.521.029,20 de liberações líquidas/estornos**, com reconciliação por município, ano e instrumento **sem diferenças**. A consulta de 2026 tem corte em **12/11/2026** e NÃO representa exercício encerrado. Os valores são transferências classificadas como investimento pela Sefaz, NÃO aplicação/obras concluídas nem investimento municipal liquidado.

A documentação anterior também contém **1.010 eventos datados individuais de investimento** em 747 convênios acessíveis e cinco detalhes com HTTP 500. **O valor de evento exibido sem centavos não deve substituir a série anual exata**, pois a fonte do detalhe individual arredonda o valor visual. As cinco exceções de acesso foram contabilizadas nas consultas anuais exatas, portanto **não impedem** a série 2020–2026.

## 2. O que o novo piloto de 16/11 acrescentou

O Crawl2AI recuperou o HTML do formulário e a rota de detalhes; o runner GitHub Actions executou consulta por POST e abriu `Convenio.aspx`. O [workflow 43919951619](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43919951619) preservou em **R2 privado** um snapshot piloto de **2 instrumentos e 3 linhas de movimentação** para Ribeirão Preto com filtro **janeiro/2025, `Beneficiado=Prefeituras`, `Tipo=Ambos`**. É amostra **não comparável diretamente** ao filtro anterior **`Tipo=Investimento`** e ao ano completo. O arquivo bruto foi salvo em:

`r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/pilotos/ribeirao_preto/2025_01/f4123863841c4cbe21daa59171e45b391b5e99a843c7affc0b668686a1e22977/raw.json`

SHA-256 `f4123863841c4cbe21daa59171e45b391b5e99a843c7affc0b668686a1e22977`; readback validado, sem publicação.

O [QA 43920272152](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43920272152) apurou: **3/3 datas válidas**, **3/3 valores com formato monetário reconhecível**, **2 eventos datados no mês pesquisado** e **1 evento em junho/2025**. **A ficha do convênio apresenta movimentos de fora do intervalo de descoberta.** Apenas **1/2 instrumentos** teve número de linhas da ficha coincidente com a contagem apresentada na consulta. Isso não demonstra erro da série histórica anterior: os filtros do piloto diferem e as naturezas/períodos da ficha devem ser reclassificadas.

**Regra vinculante:** nunca atribuir todas as parcelas encontradas na ficha ao mês ou ao exercício do filtro original. A deduplicação exige chave do instrumento + identificador/evento ou conteúdo estável da linha, data efetiva, natureza e sinal; validar contra `quantidade_pagamentos` anual e totais oficiais. Não somar dados de dois snapshots sobrepostos.

## 3. Diretriz de execução corrigida

1. **Priorizar reutilização da série anual exata RMRP** como fonte de valores estaduais para protótipo privado e integração com FINBRA/TCESP; `import_inv_rmrp_siafem_dev.py` e os QA existentes devem ser examinados antes de qualquer carga nova.
2. **Não repetir as 238 consultas** nem os 752 detalhes já preservados, exceto atualização incremental desde o corte de 12/11 e casos identificados de retificação. Preservar a versão 12/11 para auditoria.
3. **Foco P0 de expansão estadual:** construir rotina reutilizável para os **645 municípios de SP**; inventariar códigos internos de município vs IBGE7, realizar contagem piloto por novos municípios e ano e capturar séries com valores em centavos, com filtros `Beneficiado=Prefeituras` e `Tipo=Investimento`.
4. **Escopo de modalidades:** a série de investimento não cobre necessariamente repasses de custeio, outras entidades beneficiárias ou execução direta do Estado. Tratar como fontes/medidas distintas e não presumir ausência.
5. **Portal Convênios SP:** ZIP oficial 2023–2026 (3.618 linhas) gravado no R2 em 16/11; não combinar valor contratado/previsto com SIAFEM liberado sem crosswalk comprovado.
6. **Publicação:** a prévia está em branch e `public_release_authorized=false`, de modo que QA de fonte não significa promoção produtiva.

## 4. Estado do controle

- `SP_CONV`: arquivo estadual ZIP 2023–2026 validado estruturalmente e preservado no R2; sem homologação financeira/cobertura municipal.
- `SP_SEFAZ`: **RMRP34 com série exata já consolidada em 12/11**, piloto adicional de dados de parcelas em 16/11, **SP645 não coletado sistematicamente**.
- `S00`: corrigir sempre a visão de cobertura por auditoria do histórico de fontes existentes **antes** de iniciar nova coleta.
- Próximo gate recomendável: reaproveitar o crosswalk municipal e os scripts QA 2020–2026, verificar se o SQLite isolado já incorpora SIAFEM na prévia, e preparar aquisição incremental SP645 com metodologia regional previamente validada.

**Não se alterou a produção, nem se deu por homologado valor individual arredondado.**

## 5. Teste de importação em SQLite fiscal real — executado em 16/11

A execução [GitHub Actions 43920767531](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43920767531) releu o arquivo fiscal canônico 2025 de R2 por SHA-256, reconstruiu um SQLite isolado e executou o importador SIAFEM pré-existente em **uma cópia nova do banco**, seguido de QA de integridade e regressão fiscal. Todos os passos concluíram com sucesso. A saída do importador registrou `source_unchanged=true`, `instruments=752`, `instrument_year_rows=889`, `municipalities=34`, `payments_count=1017`, `amount_cents=30552102920` e `financial_event_rows_added=0`. Ou seja, trata-se de **agregados de convênio-ano**, não de eventos individuais inventados nem novo total financeiro. Produção preservada.

## 6. Cadastro IBGE7 x código interno SIAFEM para SP645 — concluído

O [script de crosswalk](../pipeline/qa/build_sp645_siafem_crosswalk.py) confrontou a dimensão oficial de municípios `DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv` com as opções do campo `Municipio` da página oficial SIAFEM recuperada pelo Crawl2AI. Resultado [GitHub Actions 43921159164](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43921159164):

- **645 códigos IBGE7 distintos**; **648 opções não vazias** no seletor (não equivalem a 648 municípios paulistas).
- **639 associações exatas** de nome normalizado e **6 aliases literais inspecionados na própria fonte**. `unmapped_ibge7=[]`.
- Aliases documentados: Brodowski/BRODOSQUI, Nova Luzitânia/NOVA LUSITANIA, Salmourão/SALMORAO, Severínia/SEVERINEA, Sud Mennucci/SUD MENUCCI e Suzanápolis/SUZANOPOLIS.
- [CSV com 645 códigos](controls/investimentos_sp645/crosswalk_ibge_siafem_2026_11_16.csv) e [QA estruturado](controls/investimentos_sp645/crosswalk_ibge_siafem_qa_2026_11_16.json) gravados na branch de desenvolvimento, **sem fuzzy matching**, com código IBGE e código local distintos.

**Importância:** resolve a dependência territorial para iniciar aquisição SIAFEM por município/ano para os 611 municípios externos à RMRP, mas **a correspondência territorial não significa que essas consultas financeiras já tenham sido executadas**. O próximo lote será particionado por município/ano com checkpoint, CSV/manifesto privado e QA de fonte. Não repetir as 238 consultas regionais do dia 12/11.

**Status de entrega desta etapa:** fonte SP_CONV preservada no R2; SIAFEM RMRP34 série exata já existente e integrada em cópia SQLite; microdados do piloto mensal guardados no R2, com problema de janela temporal documentado; crosswalk 645/645 obtido. Dados financeiros SP645 fora da RMRP ainda não adquiridos.
