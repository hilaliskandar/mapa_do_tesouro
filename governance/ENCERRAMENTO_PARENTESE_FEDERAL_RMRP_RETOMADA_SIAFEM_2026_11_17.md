# Encerramento do parêntese de aquisição federal RMRP34 e retomada SIAFEM estadual

**Data da decisão:** 17/11/2026. **Estado:** encerramento da prioridade extraordinária de aquisição Transferegov/Obrasgov **sem homologação ou conclusão de todas as modalidades**; retorno à expansão estadual SIAFEM/SP fora da RMRP, exercício 2025.

## Resultados preservados do parêntese

- Transferegov discricionárias: 1.793 convênios, 2.537 desembolsos, 28.503 movimentações de pagamento a favorecidos e staging privado com matriz município-ano; valor bruto observado dos desembolsos-pai R$ 714.989.114,47 e pagamentos nominais brutos R$ 627.287.678,10. Não somar etapas.
- Transferências Especiais: 34 beneficiários municipais, 284 planos de ação (R$ 93.046.325,06 previstos para investimento; R$ 3.257.000,00 custeio), 284 registros de empenho/minuta, 257 documentos hábeis e 257 registros de OP/OB, sendo 253 ordens enviadas ao banco e quatro pendentes com erro no SIAFI. Valor documental associado às ordens enviadas R$ 83.652.211,73; **não é confirmação de crédito bancário**.
- Gestão de Parcerias: 743 propostas por município recebedor, 672 com valor disponível de planejamento de gastos, soma R$ 256.473.787,83; sem recorte financeiro confirmado de pagamento. 
- Obrasgov: 218 fichas de projeto (recorte por proponente) com valores federais **previstos** de R$ 416.531.252,99; registros CIPI de contratos/empenhos em staging histórico, sem comprovação de execução territorial integral.
- SIAFEM da RMRP: série anual exata de 34/34 municípios, 2020–2026 até 12/11/2026, R$ 305.521.029,20 em liberações líquidas/estornos, sem diferença de conciliação.
- Painel HTML exploratório para RMRP, sub-regiões e municípios, **não publicado como sistema produtivo**. Dimensões municipais, estaduais e federais usam estágios e períodos próprios e não devem ser somadas como investimento público executado.

Relatórios: [aquisição federal](INV_RMRP_F03_F04_AQUISICAO_API_34_MUNICIPIOS_218_PROJETOS_2026_11_17.md), [cadeia Especiais](INV_RMRP_ESPECIAIS_CADEIA_MONETARIA_API_2026_11_17.md), [matriz federal de medidas](controls/investimentos_sp645/RMRP_FEDERAL_MEDIDAS_COMPILADAS_2026_11_17.csv), [série estadual RMRP](RELATORIO_INV_RMRP_SIAFEM_SERIE_ANUAL_EXATA_2020_2026_2026_11_12.md), [F01/F02](INV_RMRP_F01_F02_MATRIZ_FINANCEIRA_REAL_2026_11_17.md).

## Pendências preservadas, não bloqueadoras da retomada

Parcerias: instrumentos, documentos hábeis e ordens financeiras dos 743 registros; outras modalidades federais, Fundo a Fundo/TED conforme pertinência; comprovação de pagamento líquido, devoluções e não sobreposição; projetos Obrasgov fora do recorte por proponente; expansão territorial e integração pública. Nenhuma dessas pendências deve ser indevidamente declarada concluída.

## Retomada da fila estadual

- Branch operacional: `investimentos-territoriais-sp645-20261111`; workflow `sp645-siafem-annual-pilot-r2.yml`.
- Status do último checkpoint completo pré-parêntese: **420/611 municípios externos à RMRP consultados em 2025**, dos quais 363 reconciliados e 57 inconclusivos, R$ 716.144.696,19 em fluxo estadual líquido registrado; faltavam 191 consultas.
- **Próxima posição: offset 420, ano 2025, limite 25**. Conferir runs posteriores antes de disparar para evitar duplicação.
- Após cada run: verificar QA, SHA, gravação e readback no R2 privado; atualizar `execucoes.csv`, `snapshots.csv`, `cobertura.csv`, `pendencias.csv`, relatório e README sem chaves duplicadas.
- Manter as ausências inconclusivas fora de zeros imputados e em fila separada de retry seletivo.
- **Sem publicações, merge, mutação de D1 fiscal produtivo ou deploy**: `public_release_authorized=false`.

**O parêntese está encerrado como prioridade operacional, não como certificação de completude federal.**