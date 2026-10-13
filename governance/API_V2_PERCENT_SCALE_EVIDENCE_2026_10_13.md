# Rastreabilidade da escala dos indicadores percentuais da API v2

Data: 13/10/2026. Estado: investigação de linhagem; **não constitui certificação geral**.

## Achados no código de ingestão
- O gerador de entradas canônicas `pipeline/build/sp645_private_input.py` define `scale: 0.01` para campos percentuais selecionados, incluindo `receita_tributaria_pct_receita_corrente`, `investimento_pct_receita_corrente` e `despesa_territorial_pct_despesa`.
- O mapeamento `data/mappings/base_multifuentes_sp645_2025.yml` define `scale: 0.01` para `dtp_pct_rcl`, `dc_pct_rcl` e `dcl_pct_rcl`.
- Portanto, há evidência de conversão de entradas percentuais para frações decimais durante a ingestão, para esses seis identificadores. Isso não comprova sozinho a escala em cada linha histórica nem dos demais onze percentuais.
- O exportador `pipeline/build/export_state_api_v2.py` ainda declara `storage_scale: nao_documentada` e `display_multiplier: null` para todos os indicadores. Não é adequado substituir esses valores indiscriminadamente por 100.

## Separação metodológica exigida
1. **Escala da fonte:** número expresso como percentual (por exemplo, 12,5) ou razão (0,125), conforme origem e exercício.
2. **Transformação de ingestão:** escala aplicada no mapeamento (por exemplo, 0,01).
3. **Escala interna:** valor efetivamente armazenado na tabela `observacao`.
4. **Apresentação:** multiplicador e símbolo que o consumidor da API deverá aplicar.
5. **Proveniência por exercício:** registro de qual fonte, mapeamento e fórmula sustenta a decisão.

## Matriz inicial dos 17 indicadores percentuais

| ID | Evidência atualmente identificada no código | Situação |
|---|---|---|
| receita_tributaria_pct_receita_corrente | sp645_private_input.py: scale=0.01 | Checagem de valores e períodos pendente |
| investimento_pct_receita_corrente | sp645_private_input.py: scale=0.01 | Checagem de valores e períodos pendente |
| despesa_territorial_pct_despesa | sp645_private_input.py: scale=0.01 | Checagem de valores e períodos pendente |
| dtp_pct_rcl | base_multifuentes_sp645_2025.yml: scale=0.01 | Checagem de valores e períodos pendente |
| dc_pct_rcl | base_multifuentes_sp645_2025.yml: scale=0.01 | Checagem de valores e períodos pendente |
| dcl_pct_rcl | base_multifuentes_sp645_2025.yml: scale=0.01 | Checagem de valores e períodos pendente |
| caixa_pos_rpnp_pct_rcl | Ainda sem comprovação de escala nesta auditoria | Pendente |
| fpm_pct_receita_corrente | Ainda sem comprovação de escala nesta auditoria | Pendente |
| gestao_ambiental_pct_territorial | Ainda sem comprovação de escala nesta auditoria | Pendente |
| habitacao_pct_territorial | Ainda sem comprovação de escala nesta auditoria | Pendente |
| icms_pct_receita_corrente | Ainda sem comprovação de escala nesta auditoria | Pendente |
| ipva_pct_receita_corrente | Ainda sem comprovação de escala nesta auditoria | Pendente |
| saneamento_pct_territorial | Ainda sem comprovação de escala nesta auditoria | Pendente |
| transferencias_selecionadas_pct_receita_corrente | Ainda sem comprovação de escala nesta auditoria | Pendente |
| transporte_pct_territorial | Ainda sem comprovação de escala nesta auditoria | Pendente |
| tributos_imobiliarios_pct_receita_tributaria | Ainda sem comprovação de escala nesta auditoria | Pendente |
| urbanismo_pct_territorial | Ainda sem comprovação de escala nesta auditoria | Pendente |

## Próximas provas
- Inspecionar valores observados em `sp645_private.sqlite` da execução canônica recente e reconciliar numeradores e denominadores para amostra estratificada por ano, município e indicador.
- Distinguir percentuais oficiais RGF de proporções derivadas sobre contas DCA, assegurando alinhamento temporal e denominadores positivos.
- Criar catálogo de escalas verificadas com evidências por indicador e período; só depois publicar `storage_scale` e `display_multiplier`.
- Garantir no teste automatizado que indicadores não certificados permaneçam sem multiplicador e sem selo de aprovação.

A aprovação do PR #153 exige consistência entre o catálogo e a auditoria; ela não substitui estas verificações numéricas.
