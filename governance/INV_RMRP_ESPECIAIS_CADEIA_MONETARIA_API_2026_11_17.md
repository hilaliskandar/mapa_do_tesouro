# RMRP34 — Transferências Especiais: aquisição monetária de planos, empenhos, documentos e ordens

**Data da captura:** 17/11/2026. **Fonte primária:** API oficial do Transferegov, módulo de Transferências Especiais, consultada diretamente com Crawl2AI. **Escopo:** 34 beneficiários municipais da RMRP, identificados pelo cadastro oficial de beneficiários para SP. **Objetivo:** ampliar cobertura monetária, **sem conciliar** estornos, extratos bancários nem atribuir despesas executadas. `public_release_authorized=false`.

## 1. Procedimento e cobertura

Os 628 beneficiários de SP foram consultados em quatro páginas, 34 deles associados exatamente aos municípios RMRP pela denominação normalizada. A lista de 284 planos de ação foi extraída por `id_beneficiario`, com `total_pages=1` e contagem de linhas idêntica à declarada para cada município.

A sequência financeira foi consultada por chaves **documentais explícitas**:
1. `/planos-acao-especiais?id_beneficiario={id}` → **284 planos com 284 IDs distintos**;
2. `/empenhos-especiais?id_plano_acao={id}` → **284 registros de empenho/minuta**, cada um ligado ao seu plano, sem falhas e com 284 IDs distintos;
3. `/documentos-habeis-especiais?id_empenho={id}` → **257 documentos hábeis distintos**, relacionados a **252 planos**, e **32 planos sem documento retornado**, em 284 consultas verificadas;
4. `/ordens-pagamentos-ordens-bancarias-especiais?id_dh={id}` → **257 registros OP/OB distintos**, cada qual com ID de DH correspondente; 257/257 consultas e IDs únicos, nenhuma falha de obtenção.

Todas as respostas foram inspecionadas quanto a `total_items`, `total_pages`, cardinalidade da página e ID oficial do objeto solicitado. O retorno de `total_items=0` nos 32 documentos ausentes **não foi convertido em transação de valor zero**.

## 2. Montantes por estágio — nunca somar as colunas

| Estágio documentado | Registros | Total bruto associado | Semântica |
|---|---:|---:|---|
| Planos de ação: `valor_investimento_plano_acao` | 284 planos, sendo parte com valor de custeio | **R$ 93.046.325,06** | Investimento **previsto no plano**, não gasto |
| Planos de ação: `valor_custeio_plano_acao` | 284 planos, com custeio em parte deles | **R$ 3.257.000,00** | Custeio previsto no plano |
| Registros `empenhos-especiais` — categorias investimento e custeio juntas | 284 | **R$ 96.303.325,06** | Empenho/minuta, incluindo registros não enviados |
| Empenhos `descricao_situacao_empenho=Enviado` | **252** | **R$ 85.659.825,06** | Registro enviado, sem prova isolada de pagamento |
| Empenhos `Minuta de Empenho` | **32** | **R$ 10.643.500,00** | Minutas; não declarar empenho confirmado |
| Documentos hábeis `Enviado com Sucesso` | **257** | **R$ 85.451.825,06** | Valor de documentos, inclusive vários por um mesmo plano |
| Ordens OP/OB `OB Enviada à instituição bancária para pagamento` | **253** | **R$ 83.652.211,73** | Valor dos DH associados às ordens enviadas; **não comprova crédito definitivo** |
| Ordens `OP Pendente (Retorno com erro no envio ao SIAFI)` | **4** | **R$ 1.799.613,33** | Valor dos DH associados às quatro operações com erro; nenhuma OB emitida registrada |

**Atenção:** a tabela de ordens não apresenta um campo de valor próprio nas respostas desse endpoint; os valores apresentados nas duas últimas linhas são os **montantes dos documentos hábeis-pai vinculados por `id_dh`**, com um registro de ordem por documento. Assim, são **valores associados ao estágio das ordens**, e não `valor_pago` explicitamente publicado no endpoint. Não igualar `OB Enviada` a `OB Liquidada/Paga`.

Os 32 planos sem documentos correspondem a 32 minutas de empenho na série examinada. Não foi executada conciliação de `id_plano_acao` com extrato bancário, devoluções, subtransações e prova do gasto final.

## 3. Arquivos efetivamente persistidos

Todos na branch de desenvolvimento `investimentos-territoriais-sp645-20261111`, sob `governance/controls/investimentos_sp645/`:

- `RMRP_ESPECIAIS_PLANOS_2026_11_17_B01.csv` a `B06.csv`: **284 planos** com códigos IBGE, ano, categoria, situação, capital/custeio previstos em centavos e URL da API;
- `RMRP_ESPECIAIS_PLANOS_IDS_2026_11_17.csv`: chaves intermediárias;
- `RMRP_ESPECIAIS_EMPENHOS_2026_11_17_B01.csv` a `B15.csv`: **284 registros de empenho/minuta**, datas, situação, valor;
- `RMRP_ESPECIAIS_EMPENHOS_IDS_2026_11_17.csv`: 284 IDs de empenho;
- `RMRP_ESPECIAIS_DOCUMENTOS_HABEIS_2026_11_17_B01.csv` a `B15.csv`: **257 documentos**, 32 respostas sem documento, valores, situação, data e ID;
- `RMRP_ESPECIAIS_DH_IDS_2026_11_17.csv`: 257 IDs de documentos;
- `RMRP_ESPECIAIS_ORDENS_BANCARIAS_2026_11_17_B01.csv` a `B13.csv`: **257 registros de ordem**, situação exata, número de OB quando disponível, datas e valor de DH-pai associado, com URL da fonte.

Não foram publicados dados de bancos/contas da API, somente chaves oficiais dos documentos e medidas agregáveis. **Os CSVs são staging de fonte pública em GitHub, não deploy do sistema nem homologação fiscal.** O workflow R2 preparado na branch não foi despachado (404 no catálogo de workflows de execução), portanto não há novo snapshot R2 desse ciclo.

## 4. Lacunas e próxima aquisição

- **Gestão de Parcerias:** 743 propostas (34 municípios) obtidas, 672 com valor de planejamento; ainda requer `id_proposta → id_parceria → id_documento_habil → id_op` para valores efetivos, sem repetir as propostas.
- **Transferegov Especiais:** eventos `gestao-financeira-lancamentos-especiais`, `gestao-financeira-subtransacoes-especiais`, devoluções e confirmação efetiva do pagamento não coletados; solicitar por chaves oficiais se necessário. Por ora, **sem reconciliação financeira**, conforme pedido.
- **Obrasgov:** 218 fichas com valor **previsto** da fonte Federal, mas não foram apurados novos pagamentos da nova API. Não adicionar estes valores aos instrumentos federais existentes.

Este resultado **não é** total do investimento federal executado na RMRP. Os valores de planos, empenhos, DH e ordens são representações de etapas parcialmente sobrepostas e não devem ser somados entre si nem a FINBRA/TCESP/SIAFEM.
