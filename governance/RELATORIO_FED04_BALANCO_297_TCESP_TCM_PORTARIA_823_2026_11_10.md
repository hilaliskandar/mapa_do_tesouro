# FED04 — Balanço de conciliação dos 297 municípios inicialmente sem correspondência FNDE VAAT/VAAR 2025

**Data:** 10/11/2026. **Escopo:** DCA 2025, conta `RO1.7.1.5.00.0.0`, confrontada com Portaria MEC nº 823/2025 (fomento ETI), lançamentos analíticos de receitas municipais TCESP 2025 e IRIS/TCM-SP para a capital.

## 1. Diagnóstico revisado e evidência
A classificação original dos **297 municípios** como `somente_dca` decorria de cruzamento com relações FNDE **VAAT/VAAR**, sem incluir o mecanismo de fomento à criação de matrículas ETI. A extensão do universo revela que **277/297** municípios constam do cronograma ETI e **20/297** não constam, mas estes últimos possuem, em sua maioria, lançamentos de outras naturezas/modalidades de complemento do Fundeb na contabilidade municipal.

A revisão do cronograma pelas **Portarias MEC 669/2025 e 823/2025** demonstrou que, em **185/297**, o valor da DCA é idêntico, ao centavo, à soma das parcelas federais **outubro, novembro e dezembro de 2025 retificado**. É **correspondência com valores autorizados**, não comprovação de crédito bancário.

Nos demais registros, foi recuperada a receita analítica dos arquivos ZIP municipais do [TCESP](https://transparencia.tce.sp.gov.br/) por Browserless (diretório central do ZIP + `DecompressionStream('deflate-raw')`, CSV em Windows-1252), preservando identificador de lançamento, natureza, competência, fonte e variável de aplicação.

O **TCESP não disponibilizou arquivo de São Paulo** na mesma estrutura. Para a capital utilizou-se o arquivo de receita 2025 do [IRIS do Tribunal de Contas do Município de São Paulo](https://iris.tcm.sp.gov.br/dadosAbertos.html), [ZIP](https://iris.tcm.sp.gov.br/assets/data/receita/csvReceita2025.zip), que discrimina receitas VAAR/ETI e deduções.

## 2. Balanço global

| Categoria de evidência | Municípios | Interpretação |
|---|---:|---|
| DCA = cronograma ETI 2025 retificado | **185** | Equivalência de valor com previsão federal, sem confirmação municipal independente |
| DCA = receita bruta ou líquida TCESP | **109** | Equivalência contábil municipal; distinguir bruto, líquido e deduções |
| DCA = receita bruta IRIS/TCM-SP (São Paulo) | **1** | Correspondência contábil independente |
| Não conciliados com fonte contábil examinada | **2** | Piracicaba e Teodoro Sampaio |
| **Total** | **297** | **295** com algum tipo de correspondência monetária documentada |

Valor DCA 2025 do universo inicial: **R$265.487.655,96**. Valor DCA coberto por equivalência monetária nas três primeiras categorias: **R$262.705.433,29 (98,9520%)**. Os dois casos em aberto correspondem a **R$2.782.222,67** de DCA; isso é **valor sob diligência**, não divergência financeira comprovada. As categorias são mutuamente exclusivas para contagem.

## 3. QA do recorte dos 20 municípios sem ETI

Os **20 arquivos oficiais** foram recuperados e analisados. **19 têm DCA coincidente com a soma de lançamentos positivos da natureza da complementação**; **Ibiúna** apresenta DCA coincidente com a soma **líquida** de receitas e deduções. **Pindorama** tem R$72.131,33 em receitas positivas e R$11.877,77 em deduções, gerando líquido R$60.253,56: a DCA corresponde à **bruta**. **Sorocaba** tem R$2.599.269,81 brutos e dedução R$85.122,48, gerando líquido R$2.514.147,33: a DCA corresponde à **bruta**. A triagem preliminar de apenas valores líquidos havia produzido dois falsos positivos de divergência, corrigidos pela auditoria bruta/líquida.

**Atenção:** alguns lançamentos estão na natureza contábil `17155201` denominada VAAR, embora a variável de aplicação municipal descreva VAAF. Não resolver a modalidade exclusivamente por um dos campos; a contabilidade requer confronto com a documentação de financiamento, data de referência e ementário. Existem também fontes municipais `02` (estadual) em rubricas de complementação da União, a investigar como critério de codificação local.

## 4. Os 92 casos com ETI listado, mas DCA distinta do cronograma

Foram examinados **24 prioritários + 68 restantes**, com matriz analítica de cada lote. No lote dos 24, **22** conciliaram por receita bruta/líquida do TCESP; São Paulo foi conciliada em base municipal alternativa do TCM-SP. No lote dos 68, **66** conciliaram diretamente; Santa Rita d'Oeste não foi recuperada com o `slug` automático, mas sua receita de 2025 já havia sido localizada na auditoria anterior dos oito casos (arquivo `receitas-santa-rita-d-oeste-2025.zip`), com DCA igual a R$3.056,12. Isso resulta em **90/92** casos com equivalência contábil municipal demonstrada. Os **dois restantes** seguem abaixo.

### Piracicaba (IBGE 3538709)

- DCA 2025: **R$2.525.276,42**
- TCESP, lançamento de complementação localizado sob `17155201`: bruto **R$1.544.429,54**, deduções **R$321.624,96**, líquido **R$1.222.804,58**.
- Fomento ETI autorizado para outubro–dezembro de 2025 na Portaria 823: **R$980.846,88**.
- Relação aritmética: **R$1.544.429,54 + R$980.846,88 = R$2.525.276,42**, idêntica à DCA. Todavia o **lançamento ETI de R$980.846,88 não foi localizado na receita analítica TCESP examinada**. A identidade soma VAAR bruto + ETI previsto é hipótese de composição, não conciliação contábil por fonte municipal independente. Verificar balancete municipal da receita, DCA desagregada e créditos FNDE.

### Teodoro Sampaio (IBGE 3554300)

- DCA 2025: **R$256.946,25**.
- Contas `17155201` + `17155301` no TCESP: bruto **R$333.821,42**, deduções **R$78.570,44**, líquido **R$255.250,98**.
- Diferença para líquido contábil: **R$1.695,27**; diferença para bruto: **-R$76.875,17**. Não confundir uma com a outra.
- Necessário verificar colunas de receitas brutas, deduções e receita líquida da DCA individual, eventuais estornos e classificação por fonte. Não imputar `R$1.695,27` como irregularidade sem prova de comparabilidade de regimes e períodos.

### São Paulo (IBGE 3550308): caso encerrado na conciliação contábil

O IRIS/TCM-SP registrou **R$85.461.892,86 VAAR bruto**, dedução **R$648.058,98**, VAAR líquido **R$84.813.833,88**, mais **R$31.566.785,12 ETI**. A soma **bruta = R$117.028.677,98**, exatamente DCA 2025. A comparação anterior entre VAAR líquido e DCA bruta produziu falsa divergência. [Relatório individual](RELATORIO_FED04_SAO_PAULO_DCA_IRIS_TCM_2026_11_10.md).

## 5. Controle de proveniência e próximos gates

- [Matriz consolidada 297](FED04_297_CONCILIACAO_CONSOLIDADA_CONTABIL_ETI_TCESP_TCM_2026_11_10.csv) tem **297 chaves IBGE7**, estados mutuamente exclusivos, valor DCA e coluna de critério de correspondência.
- [20 sem ETI, bruta/líquida](FED04_TCESP_20_SEM_ETI_AUDITORIA_BRUTA_LIQUIDA_2026_11_10.csv), [lançamentos dos 20](FED04_TCESP_20_SEM_ETI_LANCAMENTOS_2026_11_10.csv).
- [24 mistos prioritários](FED04_TCESP_24_MISTOS_PRIORITARIOS_RESUMO_2026_11_10.csv), [lançamentos dos 24](FED04_TCESP_24_MISTOS_PRIORITARIOS_LANCAMENTOS_2026_11_10.csv).
- [68 mistos restantes](FED04_TCESP_68_MISTOS_RESTANTES_RESUMO_2026_11_10.csv), [lançamentos dos 68](FED04_TCESP_68_MISTOS_RESTANTES_LANCAMENTOS_2026_11_10.csv).
- [Casos dos oito inicialmente divergentes](RELATORIO_FED04_8_EXCECOES_ETI_CONCILIADAS_TCESP_2026_11_10.md); [São Paulo IRIS TCM](FED04_SAO_PAULO_IRIS_TCM_2025_LANCAMENTOS_2026_11_10.csv).

**Controles de qualidade:** 297 registros; 185 + 109 + 1 + 2 = 297; não duplicar Santa Rita d'Oeste entre auditorias; não promover equivalência ao cronograma a confirmação bancária. Em alguns municípios DCA foi igual à receita líquida e em outros à receita bruta, exigindo revisão dos nomes das colunas e das deduções antes de homogeneizar a base.

**Permanecem pendentes:** (i) esclarecimento contábil dos dois casos; (ii) confirmação dos desembolsos FNDE/SIGEF por competência e modalidade; (iii) revisão do universo 645 e do histórico 2013–2025; (iv) fontes de recurso e semântica da classificação VAAR/VAAF/ETI.

**Status:** FED04 `in_progress`; PR nº 232 `draft`; **sem merge, deploy, alteração no SQLite/R2 produtivos ou publicação**.
