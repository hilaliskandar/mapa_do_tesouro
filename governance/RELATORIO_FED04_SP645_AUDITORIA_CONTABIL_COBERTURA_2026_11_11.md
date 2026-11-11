# FED04 — Auditoria contábil 2025 e cobertura documental dos 645 municípios paulistas

**Data:** 11/11/2026. **Repositório:** `hilaliskandar/mapa_do_tesouro`, branch `fed04-catalog-safety-20261110`. **Situação:** QA documental avançado, sem homologação de repasses bancários, de série histórica ou publicação de indicadores. **PR #232 continua em rascunho.**

## 1. Universo, fontes e anti-imputação

Foram preservadas as **645 chaves IBGE7** da matriz original `governance/FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv` disponível na branch principal. O conjunto já concluído em `governance/FED04_297_CONCILIACAO_CONTABIL_MUNICIPAL_V3_2026_11_11.csv` contém 297 municípios. Os **348 restantes** foram auditados em duas classes mutuamente exclusivas:

- **156 municípios** com DCA originalmente informada, soma **R$221.860.862,85**; comparação da rubrica `RO1.7.1.5.00.0.0` contra a receita analítica TCESP natureza `1715xxxx`, em bruto e líquido;
- **192 municípios** sem valor DCA na matriz original, dos quais **191** com estado `linha_ausente` e **um** com `anexo_sem_registros`. **Nenhuma ausência foi convertida em zero.** Foi examinada a existência de linhas `1715xxxx` em cada CSV municipal do TCESP.

O download de ZIPs foi efetuado em sessão Browserless com `fetch` na origem `transparencia.tce.sp.gov.br`, descompactação do diretório central em `DecompressionStream('deflate-raw')` e CSV `windows-1252`. O navegador foi usado como alternativa à indisponibilidade de download direto; as páginas de transparência e a API SICONFI foram consultadas via Crawl2AI. Na API DCA 2025 utilizou-se `DCA-Anexo I-C`, município IBGE7 e conta `RO1.7.1.5.00.0.0`.

**Evidência contábil publicada por municípios e replicada por TCESP/TCM-SP não é, por si, prova bancária independente de transferência federal.**

## 2. Resultado dos 156 municípios com DCA informada

| Estado de conciliação | Municípios |
|---|---:|
| DCA igual à soma **bruta** dos registros TCESP | **127** |
| DCA igual à soma **líquida** TCESP | **26** |
| DCA bruta, deduções da DCA e líquido TCESP reconciliados por consulta adicional ao SICONFI | **2** |
| Divergência documental ainda não explicada | **1** |
| **Total** | **156** |

**155/156** têm correspondência contábil demonstrada, preservando as diferenças entre bruto e líquido.

**Correções de grafia de URL:** Florínea (`receitas-florinea-2025.zip`), DCA R$26.937,02 = soma de lançamentos positivos TCESP, líquido R$24.277,59 após dedução R$2.659,43; São **Luiz** do Paraitinga (`receitas-sao-luiz-do-paraitinga-2025.zip`), DCA = TCESP bruto/líquido **R$525.917,11**. Falhas iniciais 404 se referiam à construção incorreta de URL, não à inexistência da fonte.

**Anhumas:** DCA bruta R$196.256,59; coluna `Outras Deduções da Receita` **R$6.842,96**, consultada diretamente no SICONFI; líquido calculado **R$189.413,63**, idêntico ao TCESP. **Charqueada:** DCA bruta R$2.004.799,16, `Outras Deduções` R$79.315,54, líquido **R$1.925.483,62**, idêntico ao TCESP. Esses casos não devem permanecer como divergência monetária.

**Itaóca (IBGE 3522158) permanece em diligência:** SICONFI DCA `Receitas Brutas Realizadas` **R$121.331,64**, sem dedução da conta agregada no Anexo I-C consultado; TCESP `1715xxxx` bruto/líquido **R$104.632,18**, diferença **R$16.699,46**. TCESP mostra lançamentos `17155001` (VAAT) e `17155201` (VAAR) em 2025. A pesquisa complementar de RREO e balancetes por natureza, mês, ajustes, versão de transmissão e documentos FNDE é necessária; não imputar receita complementar nem concluir irregularidade com base nessa diferença.

Arquivos: [primeira leitura do 156](FED04_SP348_DCA156_POSITIVOS_CONFRONTO_TCESP_2026_11_11.csv) e [v2 após correção de slugs e deduções](FED04_SP348_DCA156_POSITIVOS_CONFRONTO_TCESP_V2_2026_11_11.csv).

## 3. Resultado dos 192 sem valor DCA na matriz original

| Resultado TCESP 2025 para natureza `1715xxxx` | Municípios |
|---|---:|
| Sem registros dessa natureza nos arquivos municipais recuperados | **175** |
| Com receita positiva dessa natureza no TCESP | **17** |
| **Total** | **192** |

**Os 192 ZIPs municipais foram recuperados.** O total **bruto** de receita `1715` dos 17 com lançamentos positivos é **R$1.712.379,83**; líquido deve ser tratado separadamente quando houver deduções.

Os **17 casos** foram consultados individualmente na API SICONFI DCA 2025:
- **15** municípios apresentam Anexo I-C com registros, **sem a conta agregada** `RO1.7.1.5.00.0.0` na resposta recuperada;
- **1**, **Santa Fé do Sul (IBGE 3546603)**, apresenta a conta no SICONFI atual com **R$116.370,65**, exatamente igual ao bruto TCESP. A ausência na matriz original é **diferença de cobertura/versão da extração**, e o valor não deve ser adicionado silenciosamente à base original;
- **1**, **Sarutaiá (IBGE 3551207)**, tem Anexo I-C com **zero registros recuperados**, porém TCESP positivo de **R$127.974,05**.

Dos 16 casos originalmente rotulados `somente_fnde`, **6** têm receita `1715` positiva no TCESP e **10** não têm registros na natureza examinada. Dos 176 casos originalmente `sem_positivo_nas_fontes_selecionadas`, **11** apresentam receita `1715` positiva no TCESP e **165** não exibem essa natureza. Estes são recortes de **presença de conta**, nunca de pagamento federal ou zero econômico.

Após retirar Santa Fé do Sul, **16 municípios** permanecem com **R$1.596.009,18 de receita bruta positiva no TCESP e sem a respectiva conta/registro na DCA consultada**. É um saldo **sob investigação de cobertura e classificação**, não dívida, desvio ou irregularidade demonstrada.

Arquivos: [192 sem DCA, evidência TCESP](FED04_SP348_DCA192_AUSENTES_AUDITORIA_TCESP_2026_11_11.csv); [17 casos examinados na API SICONFI](FED04_SP348_17_RECEITAS_TCESP_SEM_DCA_MATRIZ_API_2026_11_11.csv).

## 4. Balanço estadual SP645 — estados mutuamente exclusivos

| Situação em 2025 | Municípios |
|---|---:|
| Conciliação municipal do grupo original SP297 | **297** |
| Outros municípios com DCA e conciliação TCESP (após QA de deduções) | **155** |
| Santa Fé do Sul: DCA recuperada na API atual e confirmada TCESP | **1** |
| Itaóca: DCA e TCESP com diferença ainda não esclarecida | **1** |
| Sem DCA na fonte consultada, mas com receita `1715` positiva no TCESP | **16** |
| Sem DCA e sem lançamento `1715` nos registros TCESP examinados | **175** |
| **Total** | **645** |

Assim há **453/645 municípios com conciliação monetária contábil demonstrada**, **uma divergência monetária ainda em aberto** (Itaóca), **16 pendências de cobertura DCA**, e **175 casos de ausência de conta/lançamento neste recorte**, que não devem ser convertidos em zeros.

- A **DCA original** continha valor para **453 municípios**, somando **R$487.348.518,81** nesse recorte.
- A **API atual** permitiu recuperar uma conta adicional em Santa Fé do Sul de **R$116.370,65**, elevando a soma provisória de linhas positivas identificadas a **R$487.464.889,46**, **sem homologar alteração canônica**.
- Não somar R$1.596.009,18 do TCESP dos outros 16 à DCA: isso misturaria fontes e critérios de disponibilidade.

Artefato estadual completo: [`FED04_SP645_AUDITORIA_CONTABIL_COBERTURA_V1_2026_11_11.csv`](FED04_SP645_AUDITORIA_CONTABIL_COBERTURA_V1_2026_11_11.csv), com 645 chaves únicas, bases brutas/deduções/líquidas, estados de QA e fontes.

## 5. Próximas ações e restrições

1. **Itaóca:** determinar origem dos R$16.699,46 confrontando DCA detalhada, RREO/MSC 2025, balancete municipal e eventuais versões retificadas, inclusive modalidade VAAT.
2. **16 casos sem DCA mas com receita TCESP:** identificar competência da declaração, lacunas de integração e eventual lançamento em outros quadros/contas. Não preencher contas originalmente ausentes sem trilha de auditoria e homologação.
3. **175 municípios sem conta em ambas as fontes:** registrar estado `sem_registro_nas_fontes_examinadas`, não `zero`; auditar relação com cronograma FNDE e transferências bancárias.
4. Investigar discrepâncias de identificação das modalidades **VAAF, VAAT, VAAR e ETI** e fontes `02`/`05`.
5. Comprovar **desembolsos efetivos** FNDE/BB por município, modalidade e competência, evitando equivaler Portaria de distribuição a repasse bancário.
6. Concluir QA histórico 2013–2025, revisar gates FED00–FED08 e decidir homologação canônica apenas com evidências suficientes.

**Proibições mantidas:** FED04 `in_progress`, PR nº 232 `draft`, quatro variáveis candidatas `publicavel=0`, `ativo=0`; não executar merge, deploy, migração, nem alterar SQLite/D1/R2 produtivos.
