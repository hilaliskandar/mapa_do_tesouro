# FED03B — classificação da natureza declarada nas propostas da Gestão de Parcerias

**Data:** 15/11/2026. **Fonte:** pacote privado `RMRP_Transferegov_Aquisicao_2026-11-15.zip`, 34 municípios da RMRP, 743 propostas capturadas na rota `/parcerias/proposta`. **Método:** abertura de cada JSON.gz das 34 consultas, inspeção de `categorias_despesa_proposta`, identificação por `id_proposta` e validação de `cd_ibge_recebedor` contra município consultado.

## Resultado
| Classe exclusiva por proposta | Quantidade |
|---|---:|
| Custeio | 588 |
| Investimento | 94 |
| Mista, custeio e investimento | 59 |
| Sem categoria informada | 2 |
| Total | 743 |

743 propostas com identificadores únicos, cobertura 34 municípios e zero divergências de código municipal nas páginas. O campo `categorias_despesa_proposta` é um **atributo de planejamento**, não um lançamento financeiro. Os rótulos `investimento_proposto` e `mista` **não significam investimento executado/pago nem GND4 homologado**. Nenhuma atribuição por proponente ao local de execução foi realizada.

## SQLite de ensaio
Cópia do `RMRP_FED03_STAGING_2026-11-15.sqlite` recebeu `parcerias_categoria_proposta` com 743 linhas, identificador original e IBGE recebedor, `estagio='proposta'` e `classificacao_pagamento='nao_comprovado'`; `integrity_check=ok` e `foreign_key_check` sem erros. Arquivo local `RMRP_FED03B_CATEGORIAS_2026-11-15.sqlite` com 3.022.848 bytes, SHA-256 `922b8579ca88bcd6dd89aaad0aef4bac56e7628f1f048885caf94b3b3c816c36`. JSON local de auditoria `RMRP_FED03B_CATEGORIAS_QA_2026-11-15.json`.

**Persistência:** relatório e script de processamento registrados na branch de desenvolvimento do GitHub. A cópia SQLite FED03B ainda requer upload e readback na pasta privada do Drive; não a marcar como persistida externamente. O FED03A no Drive permanece preservado e não foi alterado.

## Próximo gate documental
Capturar e correlacionar `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl` e ordens bancárias CGU, preservando cardinalidade `NR_MOV_FIN` 1:N com OBTV e vedando somas após fan-out. Qualquer classificação monetária como investimento pago exige suporte para o item de despesa e natureza GND4; a falta de `ID_ITEM_PAD` em `siconv_itens_dl` continua impedindo vínculo direto. Prosseguir também no vínculo de propostas/instrumentos e localização física, sem fundir homônimos ou valores iguais.

## Persistência em Drive

> **FED03B — pacote privado persistido e verificado:** [ZIP SQLite + QA + script](https://drive.google.com/file/d/1q_Oxx_MOtHEyfpQE6-fwbt2H6kSIucSg/view), ID `1q_Oxx_MOtHEyfpQE6-fwbt2H6kSIucSg`, 879.987 bytes, pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, `shared=false`, readback de metadados confirmado; SHA-256 do ZIP de origem local `819756d2ae67856d8027c2386a45dc874c9b176f565446b7736fe9e4b9c2b5f1`. Não houve comparação SHA-256 por redownload do ZIP remoto. Nenhuma promoção à base produtiva.

