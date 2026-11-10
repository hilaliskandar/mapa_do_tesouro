# FED04 — Oito exceções ETI conciliadas pela receita analítica do TCESP (2025)

**Data:** 10/11/2026. **Estado:** conciliação contábil **DCA 2025 × lançamentos analíticos TCESP 2025** concluída para 8/8; comparação bancária FNDE ainda pendente. **Não confundir ausência de parcela do cronograma federal com não pagamento**.

## 1. Nova fonte documental e procedimento reprodutível

O [Portal da Transparência do TCESP](https://transparencia.tce.sp.gov.br/) publica, em `/sites/default/files/csv/receitas-{slug}-2025.zip`, um CSV por município com campos `id_rec_arrec_detalhe`, `mes_referencia`, `ds_fonte_recurso`, `ds_cd_aplicacao_fixo`, `ds_cd_aplicacao_variavel`, `ds_d1`, `ds_dd2`, `ds_d3`, `ds_tipo`, `vl_arrecadacao`.

O ZIP oficial foi recuperado **diretamente do domínio TCESP por sessão Browserless**, porque os clientes de download da sessão atual não resolveram o domínio. A extração foi feita **dentro do navegador com DataView do diretório central ZIP + DecompressionStream('deflate-raw')**, e o CSV decodificado em `windows-1252` para preservar caracteres portugueses. Foi selecionada a natureza de receita `17155xxx` e conferida a agregação por identificador de lançamento, mês e natureza. O roteiro é reproduzível, sem necessidade de CAPTCHA ou de contornar mecanismos de autenticação; o conteúdo não foi inferido de snippets.

**Ressalva técnica:** os registros são **declarados pelos municípios ao TCESP** e ainda sujeitos a verificação do Tribunal. A evidência confirma consistência **entre duas representações contábeis municipais** (TCESP e DCA), mas não equivale a extrato de crédito federal independente.

## 2. Resultado 8/8, diferença zero

| Município | IBGE7 | DCA 2025 R$ | ETI `17155301` R$ | VAAR `17155201` R$ | Total TCESP R$ | Meses escriturados |
|---|---|---:|---:|---:|---:|---|
| Iracemápolis | 3521408 | 99456.88 | 83707.73 | 15749.15 | 99456.88 | VAAR:8, ETI:10, ETI:11, ETI:12 |
| Itapetininga | 3522307 | 607329.76 | 607329.76 | 0.00 | 607329.76 | ETI:10, ETI:11 |
| Cubatão | 3513504 | 340019.75 | 340019.75 | 0.00 | 340019.75 | ETI:10, ETI:12 |
| Ibirarema | 3519501 | 87438.17 | 87438.17 | 0.00 | 87438.17 | ETI:10, ETI:12 |
| Santo Antônio do Jardim | 3548104 | 58179.27 | 58179.27 | 0.00 | 58179.27 | ETI:10, ETI:12 |
| Águas de São Pedro | 3500600 | 33990.48 | 33990.48 | 0.00 | 33990.48 | ETI:11, ETI:12 |
| Itirapuã | 3523701 | 33438.02 | 33438.02 | 0.00 | 33438.02 | ETI:11 |
| Santa Rita d'Oeste | 3547403 | 3056.12 | 3056.12 | 0.00 | 3056.12 | ETI:10, ETI:12 |

Soma DCA 8 municípios: **R$ 1262908.45**, igual à soma dos respectivos lançamentos TCESP, **diferença R$0,00**. Total de **17 registros analíticos individuais**, preservados em CSV com ID de lançamento TCESP.

### Caso Iracemápolis — diferença antes inexplicada de R$15.749,15

A DCA de R$99.456,88 decompõe-se em **R$83.707,73 ETI** (`17155301`, outubro R$41.853,86; novembro R$20.926,93; dezembro R$20.926,94) e **R$15.749,15 VAAR** (`17155201`, agosto de 2025, ID `45864890`). A soma corresponde exatamente à DCA: **R$99.456,88**.

**Correção categorial necessária:** o rótulo anterior `SEM_BENEFICIO_2024_2025_IDENTIFICADO` inferia ausência de benefício apenas da **lista FNDE VAAT/VAAR** consultada. O lançamento municipal de VAAR existe; não comprova inscrição na lista de beneficiários examinada nem pagamento federal VAAR e requer investigação cruzada de versões e competência. A composição ETI+VAAR é **contábil**; não há indicação de desvio.

### Meses reais não devem ser inferidos apenas da fração do total

- Itapetininga: **outubro e novembro**.
- Cubatão: **outubro e dezembro**.
- Ibirarema: **outubro e dezembro**.
- Santo Antônio do Jardim: **outubro e dezembro** (**não** outubro+novembro, hipótese anterior incorreta).
- Águas de São Pedro: **novembro e dezembro** (**não** outubro, hipótese anterior incorreta).
- Itirapuã: **novembro**.
- Santa Rita d'Oeste: **outubro e dezembro**.

**Observações específicas de QA:** (i) Ibirarema apresenta natureza `17155301` de transferência federal, porém o campo de fonte de recursos no arquivo TCESP está marcado como **`02 - TRANSFERÊNCIAS E CONVÊNIOS ESTADUAIS-VINCULADOS`**; é necessária verificação da fonte de recurso antes de homologação. (ii) Itirapuã apresenta código variável de aplicação `00` não informado; não supor irregularidade. (iii) o TCESP não prova que as parcelas não vistas na receita 2025 **não foram pagas**; pode haver diferenças de escrituração, competência ou retificações.

## 3. Fontes específicas (ZIP oficial por município)

- [Iracemápolis](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-iracemapolis-2025.zip) — ID 45864890, VAAR mês 8, R$15749.15; ID 46035295, ETI mês 10, R$41853.86; ID 46116213, ETI mês 11, R$20926.93; ID 46198586, ETI mês 12, R$20926.94
- [Itapetininga](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-itapetininga-2025.zip) — ID 46036541, ETI mês 10, R$404886.51; ID 46117362, ETI mês 11, R$202443.25
- [Cubatão](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-cubatao-2025.zip) — ID 46024240, ETI mês 10, R$226679.82; ID 46190487, ETI mês 12, R$113339.93
- [Ibirarema](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-ibirarema-2025.zip) — ID 46085878, ETI mês 10, R$58292.10; ID 46235104, ETI mês 12, R$29146.07
- [Santo Antônio do Jardim](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-santo-antonio-do-jardim-2025.zip) — ID 46072449, ETI mês 10, R$38786.18; ID 46225432, ETI mês 12, R$19393.09
- [Águas de São Pedro](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-aguas-de-sao-pedro-2025.zip) — ID 46089830, ETI mês 11, R$16995.24; ID 46178279, ETI mês 12, R$16995.24
- [Itirapuã](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-itirapua-2025.zip) — ID 46162522, ETI mês 11, R$33438.02
- [Santa Rita d'Oeste](https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-santa-rita-d-oeste-2025.zip) — ID 46071035, ETI mês 10, R$2037.41; ID 46246441, ETI mês 12, R$1018.71

## 4. Continuidade

1. Reclassificar os **oito casos** como `DCA_CONCILIADA_COM_LANCAMENTOS_TCESP_2025`, com segundo indicador independente `PAGAMENTO_FEDERAL_A_COMPROVAR`. A distinção de gate é fundamental.
2. Investigar especificamente a origem e a modalidade de **VAAR em Iracemápolis**, que não tinha correspondência no conjunto de listas FNDE 2024/25 utilizado; revisar versões, eventuais ajustes e competência.
3. Investigar fontes bancárias para os sete casos com parcelas contábeis inferiores ao cronograma ETI retificado; não assumir inadimplência nem omissão.
4. Resolver a fonte `02` de Ibirarema, e validar campo de aplicação de Itirapuã.
5. Aplicar mesma técnica de CSV TCESP aos **92 casos com ETI não igual à DCA** no grupo dos 297, e aos 20 não listados no Anexo II ETI.
6. FED04 continua **in_progress**, PR nº 232 **draft**. Nenhum merge, alteração do banco produtivo, R2 ou publicação pública.

## 5. Artefatos
- `governance/FED04_8_PENDENCIAS_ETI_2025_LANCAMENTOS_TCESP_2026_11_10.csv`
- `governance/FED04_8_PENDENCIAS_ETI_2025_RECONCILIACAO_DCA_TCESP_2026_11_10.csv`
