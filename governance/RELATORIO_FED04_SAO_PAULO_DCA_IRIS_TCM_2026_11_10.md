# FED04 — São Paulo: conciliação bruta/líquida DCA 2025 e IRIS TCM-SP

**Data:** 10/11/2026. **Fonte independente da DCA:** [IRIS, Tribunal de Contas do Município de São Paulo, Receita 2025](https://iris.tcm.sp.gov.br/dadosAbertos.html); [CSV ZIP oficial](https://iris.tcm.sp.gov.br/assets/data/receita/csvReceita2025.zip), atualizado em 10/10/2026. O arquivo tem 17.645 linhas de dados, após descompactação; o arquivo comprimido consultado tinha 633.835 bytes.

O pacote oficial foi obtido por Browserless no domínio do próprio TCM-SP, aberto em navegador e extraído com `DecompressionStream('deflate-raw')`. Foram filtrados lançamentos da empresa Prefeitura do Município de São Paulo, transferências correntes da União, complemento ao Fundeb, naturezas `17155201` (VAAR) e `17155301` (ETI), com `Arrecadado` e indicador de dedução.

## Contas identificadas

| Natureza | Componentes 2025 | Receita bruta R$ | Deduções R$ | Líquido R$ |
|---|---|---:|---:|---:|
| VAAR `17155201` | janeiro 81.406.237,19; abril 4.055.655,67; dedução abril -648.058,98 | **85.461.892,86** | **-648.058,98** | **84.813.833,88** |
| ETI `17155301` | outubro 15.783.392,56; novembro 7.891.696,28; dezembro 7.891.696,28 | **31.566.785,12** | 0,00 | **31.566.785,12** |
| Total | | **117.028.677,98** | -648.058,98 | **116.380.619,00** |

**DCA 2025, conta `RO1.7.1.5.00.0.0`, `Receitas Brutas Realizadas`: R$117.028.677,98. Diferença para receita bruta TCM-SP: R$0,00.** O montante VAAR líquido R$84.813.833,88 também coincide com o valor anteriormente examinado no demonstrativo municipal de educação (RREO/MDE). Assim a diferença anterior era da comparação entre VAAR líquido e DCA agregada bruta incluindo ETI.

O fomento ETI contabilizado de outubro a dezembro soma os R$31.566.785,12 previstos no Anexo II retificado da Portaria MEC 823/2025. **A conciliação contábil e normativa não substitui comprovação bancária de desembolso federal.**

## Artefatos e QA

- `governance/FED04_SAO_PAULO_IRIS_TCM_2025_LANCAMENTOS_2026_11_10.csv`: seis movimentos não nulos separados por mês, código, modalidade e indicador de dedução. Zero não é usado como sinônimo de dados ausentes; foram omitidas linhas mensais de valor 0.
- Arquivo de origem integral: https://iris.tcm.sp.gov.br/assets/data/receita/csvReceita2025.zip .
- As naturezas são identificadas mediante as colunas originais de origem, espécie, desdobramento e tipo da receita, mantendo semântica contábil. Base IRIS não é o padrão CSV TCESP; requer parser separado.
- São Paulo sai da fila de **conciliação contábil DCA × fonte municipal independente**, mas continua na fila de confirmação de crédito federal e QA do crosswalk.

FED04 em andamento, PR #232 draft, sem merge nem atualização de produção.
