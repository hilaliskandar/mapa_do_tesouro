# INV-RMRP — Reconsulta dos 11 planos CIENTE: resultado verificado

**Execução:** [GitHub Actions 43132157764](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43132157764) em 12/11/2026, 01:06 UTC (11/11, 22:06 BRT). **Artefato:** `inv-rmrp-especiais-11-ciente-43132157764`, ID `13906050639`, ZIP SHA-256 `782752bf9d9859c263167196b9bbd17a4db48bf03913404804be874f32db1200`. Manifesto JSON interno SHA-256 `1c8a70659ab567307f0ac63f4ed3348ad6b10ff8b81062011359e3d7de5f0d3f`.

## Resultado efetivamente conferido

O artefato `resultado.json` foi recuperado e lido: **11 planos, zero erros**, todos com exatamente um empenho retornado; dez mantiveram **um documento hábil e nenhuma OB retornada**; o plano `98635` (Santo Antônio da Alegria) manteve **empenho sem DH retornado**. **Nenhuma nova OB foi encontrada** nos 11 planos. A consulta não comprova crédito bancário nem ausência de pagamento; apenas o estado das três rotas examinadas naquele momento.

O inventário comparativo por plano está em [CSV de reconsulta dos 11 CIENTE](INV_RMRP_ESPECIAIS_11_CIENTE_RESULTADO_RECONSULTA_2026_11_11.csv). A fila anterior de 42 pendências continua preservada, e os 31 demais casos não foram reconsultados nesta execução.

## Verificação de CI e prévia

O workflow `43132157723` do Pages Preview teve resultado geral `failure` porque o job `rmj-browser-qa` falhou em **Install Chromium for QA**. Seu job separado `build-deploy-qa` **passou**: deploy Cloudflare no alias `pr-233`, QA local e remoto das quatro interfaces, incluindo 2.385 movimentações e 778 agrupamentos. A quarta prévia é [movimentacoes-especiais-rmrp-preview.html](https://pr-233.finbra-tic-tim-referencia.pages.dev/movimentacoes-especiais-rmrp-preview.html), classificada como **experimental, sem conciliação por plano**.

O workflow `43132157708` de QA offline de coletores falhou no teste `test_complete_34_and_no_personal_data_in_outputs`: o fixture colocava o CNPJ **fictício** dentro do campo sintético `id_lancamento_gestao_financeira` e o teste, corretamente, proibia essa sequência nas saídas. A correção altera apenas o ID sintético para não conter o CNPJ; não elimina nem relaxa os assertions de privacidade. Commit `204285a5664927b4d435fe2cfdaf25ddfa3ad5c8`; **nova execução de QA ainda precisa ser comprovada**.

## Próximos procedimentos

1. Conferir novo job de QA após correção do fixture e manter revisão da separação entre movimentos e dados pessoais.
2. Solicitar/identificar evidência documental de crédito efetivo e eventual estorno, sem junção por coincidência de valores ou datas.
3. Distinguir as 27 pendências com impedimento/rejeição e quatro com elaboração/análise dos 11 CIENTE já reconsultados.
4. Priorizar aquisição de liberações estaduais e vinculação a instrumentos, empenhos e liquidações; manter investimentos planejados e realizados separados e não aditivos.
5. Permanecer na PR #233, sem merge, mutações canônicas nem alteração do FED04.
