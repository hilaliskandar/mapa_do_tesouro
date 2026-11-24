# INV-RMRP — FED03: pagamentos e disponibilidade de OBTV

Data da verificação: 14/11/2026. Não envolve alterações à produção.

## Leitura oficial de pagamentos

O primeiro workflow FED03, [43612546925](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43612546925), recuperou integralmente `siconv_pagamento.zip` e contou **7.575.512** registros nacionais, mas terminou em `failure` porque a tentativa de consultar o arquivo presumido `siconv_obtv.zip` devolveu HTTP 404.

O workflow corrigido, [43617744602](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43617744602), terminou em **success**, preservou o catálogo da fonte no artefato `14121824845` (digest do artefato `sha256:8748a7f701a3c7a6077c9b9020c3970823edad26bc7c18c9d2222af0f822a67e`) e confirmou as colunas:

`NR_MOV_FIN`, `NR_CONVENIO`, `IDENTIF_FORNECEDOR`, `NOME_FORNECEDOR`, `TP_MOV_FINANCEIRA`, `DATA_PAG`, `NR_DL`, `DESC_DL`, `VL_PAGO`, `ID_DL`, `DATA_EMISSAO_DL`.

A documentação do layout não significa classificação concluída dos diferentes tipos de movimentação, pagamentos líquidos, estornos ou natureza econômica da aplicação. Por razões de minimização de dados, os artefatos publicáveis não devem incluir `IDENTIF_FORNECEDOR`, `NOME_FORNECEDOR` ou `DESC_DL`.

A denominação e endereço de OBTV permanecem **não verificados**. HTTP 404 para uma URL pressuposta não equivale à inexistência de registros OBTV em outros conjuntos, relatórios ou endpoints oficiais.

## Junção read-only por convênio

A implementação `pipeline/acquire/inv_rmrp_fed03_payment_join.py` e o workflow `.github/workflows/inv-rmrp-fed03-payment-join.yml` consultam os arquivos oficiais nacionais `siconv_proposta`, `siconv_convenio` e `siconv_pagamento`. Usam `COD_MUNIC_IBGE`/UF para delimitar os proponentes da RMRP, `ID_PROPOSTA` para vincular convênios e `NR_CONVENIO` para relacionar linhas de pagamento. O produto é uma contagem não monetária por município proponente e manifesto com hashes dos arquivos ZIP, sem microdados de fornecedores.

Execução iniciada [43617824183](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43617824183). Na consulta inicial a leitura das fontes nacionais estava em curso, sem conclusão. **Não atribuir cobertura, contagem regional de linhas pagas, nem sucesso ao job antes de verificar o log.**

## Gate seguinte

1. Validar contagem e conservação dos registros de pagamento selecionados.
2. Conferir o domínio real de `TP_MOV_FINANCEIRA`, o layout de `VL_PAGO`, sinal, possível estorno/cancelamento, e semântica de `DATA_PAG` versus `DATA_EMISSAO_DL`. Classificação monetária somente depois da reconciliação de tais campos e do controle do exercício.
3. Cruzar pagamentos somente por `NR_CONVENIO`, preservando distinção entre pagamento a fornecedor, desembolso do concedente e despesas de investimento em PAD GND4, sem atribuir por rateio percentual.
4. Investigar o catálogo real de OBTV, sem assumir nome do arquivo.
5. Persistir snapshots em R2 privado com hash/readback após QA; não promover à produção e não divulgar informações bancárias ou de favorecidos.
