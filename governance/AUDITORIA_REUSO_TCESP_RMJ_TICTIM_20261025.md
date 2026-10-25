# Inventário preliminar de reuso TCESP — RMJ, TIC-TIM e matriz SP645
Data: 2026-10-25. Natureza: auditoria documental, sem nova coleta TCESP, sem alteração da API pública.

## Evidências verificadas nesta retomada
- RMRP histórico: 102 pares município-ano (34 x 2023-2025), preservação R2 documentada no README raiz, chave `tcesp/rmrp/2023_2025/run_39203495737/`.
- RMRP parcial 2026: 68 documentos (receitas/despesas), preservação R2 documentada, chave `tcesp/rmrp/2026/run_40229219185/`. Receitas de Jardinópolis somente até maio; demais coberturas regionais indicadas até agosto.
- São Carlos: 16 documentos 2023-2026 com R2 documentado em `tcesp/sao-carlos/2023_2026/acervo_20261025/`. Run 40231520362 possui artifact de manifesto.
- RMJ: 21 extratos município-ano para sete municípios x 2023-2025 documentados em `editorial/rmj/README.md`; os sete JSONs de 2025 foram conciliados 7/7 em `editorial/rmj/CONCILIACAO_PROGRAMAS_ACOES_COMPLETA_2025.md`. Run 38719698652 possui artifact `rmj-tcesp-2025-full-raw` (ID 11963767921; no momento consultado, não expirado). Documentação de 2023-2024 aponta artifact 11680818755. **Ainda não comprovada persistência R2 do acervo bruto RMJ**; não marcar como `r2_validado`.
- TIC-TIM: workflow legado `.github/workflows/tictim-tcesp-complemento-23.yml` prevê 23 slugs e 2023-2025, três jobs anuais; isso é capacidade de coleta, não prova de 69 extratos efetivamente coletados ou preservados. Necessário localizar runs/artifacts e conciliar.
- Inventário estadual inicial: run 40231222578, artifact `tcesp-sp645-matriz-cobertura-2023-2026` (ID 12612906187).
- Workflow mais recente `.github/workflows/tcesp-inventario-sp645-v2.yml` já inclui os três manifestos R2 e o código `editorial/rmrp/inventario_tcesp_sp645_v2.py`, produzindo matriz 645 x 4 anos x 4 domínios = 10.320 posições. **Execução/homologação do workflow v2 não foi confirmada nesta leitura**. Não refazer a lógica ou presumir que a matriz v2 foi gerada.

## Distinções obrigatórias
1. Acervo temporário do GitHub Actions, manifesto R2, objeto R2 com checksum validado, ingestão SQLite e disponibilização em API pública são estados diferentes.
2. Produtos de investimentos liquidados e movimentos de investimentos podem corresponder à mesma fonte bruta; não somar coberturas como se fossem observações independentes.
3. `nao_inventariado_no_r2` não significa ausência no TCESP. 2026 é parcial.
4. Não substituir DCA/FINBRA automaticamente. Preservar Guatapará 2023 (R$ 10.176,00) e São Carlos 2024 (aprox. R$ 3,16 milhões) como divergências documentadas até resolução específica.

## Sequência segura, sem coleta redundante
1. Verificar run/artifact do inventário v2 e, se houver, validar contagens, meses e SHA-256 contra manifestos R2.
2. Recuperar os artefatos RMJ 2023-2025 e seu inventário de 21 pares; verificar schemas, hashes, granularidade e fonte original; promover a R2 apenas por fluxo de persistência com readback e QA.
3. Localizar runs de TIC-TIM 23 e distinguir success, partial e failure por ano/município; promover somente registros efetivamente validados.
4. Reconstruir matriz com proveniência em categorias `r2_validado`, `artifact_temporario`, `presente_nao_validado`, `nao_inventariado` e `conflito`. Deduplicar por IBGE, ano, domínio e tipo de produto.
5. Gerar fila `missing-only` somente após inventariar R2 e artefatos, com prioridade para exercícios fechados e atualização intencional de meses de 2026.
6. Integrar no SQLite em camada TCESP separada e condicionar API/publicação a testes de regressão.

## Fonte de verdade
README raiz; `governance/PLANO_INCREMENTAL_TCESP_SP645_20261025.md`; `editorial/rmj/README.md`; `editorial/rmj/CONCILIACAO_PROGRAMAS_ACOES_COMPLETA_2025.md`; workflows de inventário v2, reuso, RMJ backfill e TIC-TIM complemento 23.
