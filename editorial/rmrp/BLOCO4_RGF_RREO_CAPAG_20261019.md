# RM de Ribeirão Preto — Bloco 4: RGF, RREO e CAPAG

Data da verificação: 19/10/2026. Fonte: artefato privado `sp645-private-site-38593209824`, universo `RM_RIBEIRAO_PRETO`, 34 municípios. Não é uma nova consulta às declarações fiscais oficiais e não autoriza publicação automática.

## Cobertura em 2025

| Variável | Valores observados / 34 |
|---|---:|
| rreo_rcl_oficial | 26 |
| rgf_despesa_total_pessoal | 26 |
| rgf02_divida_consolidada | 32 |
| rgf02_divida_consolidada_liquida | 26 |
| rgf_caixa_liquida_apos_rpnp | 26 |
| capag | 34 registros, quatro com valor textual n.d. |

CAPAG: A+ 1, A 4, B+ 1, B 2, C 21, D 1, n.d. 4. Classificações são do snapshot; não inferir situação fiscal atual.

## Restrições

A cobertura é incompleta em vários indicadores e não se deve inferir valor zero para municípios ausentes. Percentuais de pessoal e dívida têm escala ainda não certificada no relatório de prontidão da API v2; não usar números de porcentagem em publicação. Em 2023 e 2024, o snapshot não expõe as contas monetárias complementares RGF/RREO de modo comparável a 2025; isso não significa inexistência de documentos históricos.

## Artefatos e próximos passos

Na conversa do projeto foram gerados: `BLOCO4_COBERTURA_RGF_RREO_CAPAG.csv`, `BLOCO4_FICHAS_MUNICIPAIS_RGF_RREO_CAPAG.csv`, `BLOCO4_DIAGNOSTICO.json`, `CADERNO_RMRP_BLOCO_4_RGF_RREO_CAPAG.md` no diretório de trabalho `rmrp_caderno`.

A pesquisa preliminar de arquivos versionados do repositório encontrou procedimentos TCESP para a RMJ, mas não demonstrou existência de extratos completos equivalentes para os 34 municípios da RM de Ribeirão Preto. Verificar no acervo já existente antes de novas extrações. Reutilizar as rotinas metodológicas RMJ, sem assumir cobertura TCESP comprovada.
