# FED04 — Fechamento do confronto documental e contábil dos 297 casos DCA/FNDE 2025

**Data:** 11/11/2026. **Situação:** todos os 297 casos apresentam **correspondência monetária com fonte oficial**; **não há homologação bancária nem validação completa das modalidades e da comparabilidade histórica**. O PR #232 continua em rascunho.

## 1. Fechamento das duas pendências

### 1.1 Piracicaba — código IBGE 3538709

A consulta com parâmetros explícitos ao [Portal da Transparência de Piracicaba, exercício 2025](https://transparencia.piracicaba.sp.gov.br/relatorio/evolucao-receita/?filtered=1&ano_exercicio=2025&desc_natureza=171553) demonstrou a receita de fomento à criação de matrículas em educação em tempo integral, natureza `17155301`, competência 2025:

| Mês | ETI escriturado |
|---|---:|
| Outubro | R$ 490.423,43 |
| Novembro | R$ 245.211,71 |
| Dezembro | R$ 245.211,74 |
| **Total ETI 2025** | **R$ 980.846,88** |

Fonte com VAAR e ETI no mesmo extrato: [consulta FUNDEB, 2025](https://transparencia.piracicaba.sp.gov.br/relatorio/evolucao-receita/?filtered=1&ano_exercicio=2025&desc_natureza=FUNDEB). O portal indica R$1.222.804,58 de **VAAR líquido** (janeiro R$1.089.196,88; novembro R$133.607,70); o TCESP, nos lançamentos analíticos desta mesma natureza `17155201`, mostra R$1.544.429,54 de **receita bruta** e deduções de R$321.624,96 (R$1.222.804,58 líquido). As naturezas do extrato municipal permitem concluir:

| Componente | Bruto | Deduções | Líquido |
|---|---:|---:|---:|
| VAAR `17155201` | R$1.544.429,54 | −R$321.624,96 | R$1.222.804,58 |
| ETI `17155301` | R$980.846,88 | R$0,00 | R$980.846,88 |
| **Total** | **R$2.525.276,42** | **−R$321.624,96** | **R$2.203.651,46** |

A [API SICONFI, DCA 2025, Anexo I-C, conta `RO1.7.1.5.00.0.0`](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&id_ente=3538709&no_anexo=DCA-Anexo%20I-C), informa as colunas **Receitas Brutas Realizadas = R$2.525.276,42** e **Outras Deduções da Receita = R$321.624,96**. Resultado líquido, R$2.203.651,46; **diferença entre a composição oficial e a DCA: R$0,00**.

**Nota crítica:** os valores TCESP e portal municipal provêm de registros municipais de uma mesma escrituração e podem ter diferenças de atualização; a conciliação não comprova ainda créditos realizados pelo FNDE. A receita ETI foi omitida no arquivo TCESP de receita analítica recuperado anteriormente, mas é publicada no portal municipal oficial.

### 1.2 Teodoro Sampaio — código IBGE 3554300

Fonte de lançamento: [TCESP, receitas municipais de 2025](https://transparencia.tce.sp.gov.br/municipio/teodoro-sampaio/2025), [CSV ZIP](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-teodoro-sampaio-2025.zip), nas naturezas `17155201` (complementação VAAR, aplicação municipal descrita como VAAF) e `17155301` (ETI).

| Lançamento | Data contábil (mês) | Valor |
|---|---|---:|
| VAAR `17155201`, id 43899111 | janeiro | +R$135.714,41 |
| Ajuste `17155201`, id 44316938 | abril | −R$76.875,17 |
| VAAR `17155201`, id 44317030 | abril | +R$6.097,72 |
| Ajuste `17155201`, id **44317031** | abril | **−R$1.695,27** |
| ETI `17155301`, ids 46086875, 46162033, 46236218 | outubro–dezembro | +R$192.009,29 |

**Confronto de colunas:**
- Receitas positivas: **R$333.821,42**.
- Menos ajuste/estorno de R$76.875,17: **R$256.946,25**.
- Menos lançamento de R$1.695,27: **R$255.250,98**.
- A [DCA original no SICONFI, conta `RO1.7.1.5.00.0.0`](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&id_ente=3554300&no_anexo=DCA-Anexo%20I-C) registra **Receitas Brutas Realizadas R$256.946,25** e **Outras Deduções da Receita R$1.695,27**, com líquido calculado R$255.250,98. **Diferença: R$0,00**.
- É incorreto subtrair novamente o ajuste de R$76.875,17 sobre os R$256.946,25, pois ele já está refletido na base bruta declarada à DCA.
- O código `17155201` consta no TCESP com descrição VAAR, mas o campo `ds_cd_aplicacao_variavel` utiliza o termo VAAF; **a modalidade precisa de análise semântica, não de recodificação automática**.

## 2. Balanço 297 casos e evidência, sem dupla contagem

| Classe de correspondência | Municípios | Limite da evidência |
|---|---:|---|
| DCA idêntica às parcelas ETI previstas outubro–dezembro (Portaria MEC 823/2025) | 185 | Cronograma autorizado, sem confirmação de lançamento municipal individual |
| DCA conciliada com receitas brutas/líquidas TCESP | 109 | Coerência contábil municipal, sem confirmação de repasse bancário FNDE |
| DCA conciliada com IRIS/TCM-SP | 1 | Capital, VAAR bruto + ETI, com deduções separadas |
| DCA conciliada com TCESP + portal municipal + DCA/SICONFI — Piracicaba | 1 | Composição VAAR+ETI, bruto/deduções/líquido |
| DCA conciliada com TCESP + DCA/SICONFI — Teodoro Sampaio | 1 | Estornos em bruto e dedução explicitada |
| **Total com correspondência monetária documental** | **297** | **Não equivale a 297 desembolsos federais homologados** |

O grupo original representa **R$265.487.655,96 de DCA 2025**; **100%** do valor possui agora pelo menos uma modalidade de correspondência. Não interpretar esse resultado como comprovação bancária ou universal de integridade das colunas: os 185 municípios conciliados com cronograma precisam de verificação municipal adicional para igualar o patamar dos outros 112.

## 3. Reprodutibilidade e versionamento

O consolidado v1 `governance/FED04_297_CONCILIACAO_CONSOLIDADA_CONTABIL_ETI_TCESP_TCM_2026_11_10.csv` é preservado **sem edição** como linha de base. O **v2** `governance/FED04_297_CONCILIACAO_CONSOLIDADA_V2_2026_11_11.csv` corrige somente os dois casos, preservando as 297 chaves IBGE e o total DCA.

Fontes a consultar no crosswalk:
- [Portaria MEC 823/2025, Anexo II retificado](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-823-de-12-de-dezembro-de-2025/@@display-file/file)
- [TCESP — transparência de receitas](https://transparencia.tce.sp.gov.br/)
- [SICONFI — API DCA](https://apidatalake.tesouro.gov.br/docs/siconfi/)
- [IRIS/TCM-SP, receitas 2025](https://iris.tcm.sp.gov.br/dadosAbertos.html)

## 4. Próximas validações obrigatórias

1. Validar as receitas analíticas municipais dos **185** atualmente iguais apenas ao cronograma ETI, mantendo `fonte_cronograma` e `fonte_contabil` como verificações independentes.
2. Investigar divergências entre classificação VAAR/VAAF e fonte 02/05 por código de natureza, aplicação e competência: nenhuma recodificação automática.
3. Obter **liberações efetivas FNDE**, por município, mês, modalidade e competência, distinguindo cronograma autorizado de ingresso bancário realizado.
4. Executar QA para **SP645 e histórico 2013–2025**, incluindo classificação bruta/líquida, valores ausentes e quebras de série 2021/2023/2025; conferir gates FED08 antes de publicar.
5. Não executar merge do PR #232, migrações, alterações em SQLite/R2 produtivos nem publicação dos quatro indicadores candidatos.

**Estado:** FED04 `in_progress`, PR #232 `draft`, homologação bancária pendente.
