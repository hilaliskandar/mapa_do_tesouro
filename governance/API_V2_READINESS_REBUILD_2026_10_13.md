# Resultado de prontidão da API v2 após correção da documentação
Data: 13/10/2026.
Fonte: artefato do GitHub Actions 38360896979, `data/api/v2/qa/readiness.json`, reconstrução com dados canônicos, após merge do PR #150.
Artefato: `sp645-private-site-38360896979` (ID 11795250292; sha256 do arquivo ZIP `22f9431f4d069c89fa2c43607b1bfdda4f3c3d8bd3c338d3f3c94a889993bc40`).

## Resultado
- 75 variáveis publicáveis; 27 sem lacuna de preenchimento dos campos exigidos pelo auditor, 48 com lacuna `cautelas`.
- 17 variáveis com `unidade=percentual` ainda com escala de armazenamento/exibição não certificada.
- Aprovação estrutural do artefato não é aprovação do conteúdo metodológico nem autorização de publicação.

## Lacunas em cautelas
### DCA e receitas/despesas (23)
- `dca_alienacao_bens`
- `dca_amortizacao_divida_liquidada`
- `dca_despesa_corrente_liquidada`
- `dca_despesa_total_liquidada`
- `dca_func_educacao_liquidada`
- `dca_func_gestao_ambiental_liquidada`
- `dca_func_habitacao_liquidada`
- `dca_func_saneamento_liquidada`
- `dca_func_saude_liquidada`
- `dca_func_transporte_liquidada`
- `dca_func_urbanismo_liquidada`
- `dca_icms_cota_parte`
- `dca_inversoes_financeiras_liquidada`
- `dca_investimentos_liquidada`
- `dca_iptu_principal`
- `dca_ipva_cota_parte`
- `dca_iss_principal`
- `dca_juros_encargos_liquidada`
- `dca_operacoes_credito`
- `dca_pessoal_encargos_liquidada`
- `dca_receita_corrente_bruta`
- `dca_receita_tributaria_bruta`
- `dca_transferencias_capital`

### Agregados e medidas auxiliares (11)
- `despesa_territorial`
- `despesas_capital_selecionadas`
- `diferenca_capital_selecionada`
- `gasto_social_selecionado`
- `populacao_dca`
- `receitas_capital_selecionadas`
- `saldo_corrente_simplificado`
- `servico_divida_liquidado`
- `transferencias_selecionadas`
- `tributos_imobiliarios`
- `tributos_selecionados`

### RGF/RREO (13)
- `rgf02_deducoes_divida_consolidada`
- `rgf02_demais_haveres_financeiros`
- `rgf02_disponibilidade_caixa`
- `rgf02_divida_consolidada`
- `rgf02_divida_consolidada_liquida`
- `rgf02_divida_contratual`
- `rgf02_outras_dividas`
- `rgf02_parcelamento_dividas`
- `rgf02_precatorios_vencidos_nao_pagos`
- `rgf02_restos_pagar_processados`
- `rgf_caixa_liquida_apos_rpnp`
- `rgf_despesa_total_pessoal`
- `rreo_rcl_oficial`

### CAPAG (1)
- `capag`

## Escala percentual não certificada (17)
- `caixa_pos_rpnp_pct_rcl`
- `dc_pct_rcl`
- `dcl_pct_rcl`
- `despesa_territorial_pct_despesa`
- `dtp_pct_rcl`
- `fpm_pct_receita_corrente`
- `gestao_ambiental_pct_territorial`
- `habitacao_pct_territorial`
- `icms_pct_receita_corrente`
- `investimento_pct_receita_corrente`
- `ipva_pct_receita_corrente`
- `receita_tributaria_pct_receita_corrente`
- `saneamento_pct_territorial`
- `transferencias_selecionadas_pct_receita_corrente`
- `transporte_pct_territorial`
- `tributos_imobiliarios_pct_receita_tributaria`
- `urbanismo_pct_territorial`

## Plano de resolução
1. Localizar cautelas originais nos catálogos e notas metodológicas. Para os itens sem texto comprovado, elaborar proposta editorial específica e submetê-la à revisão; não preencher em massa com frases genéricas.
2. Para cada percentual, fixar escala de armazenamento, multiplicador e fórmula normativa ou derivada documentada, mantendo campos explícitos no contrato de API; não converter por heurística.
3. Executar testes de paridade com o arquivo de indicadores Gate D de 2025 e controle de percentuais legais RGF/RREO, e recalcular o QA em nova construção.
4. Publicar somente após revisão editorial e controle de regressão da API v1 e painel.

Esta lista caracteriza ausência de cautelas segundo o contrato do auditor; não indica necessariamente inexistência de todo o método ou fonte original.
