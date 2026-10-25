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

## Segunda conferência documental — 25/10/2026
- Reconsultados os artifacts: inventário estadual inicial, run 40231222578, artifact 12612906187, presente e não expirado; RMJ 2025, run 38719698652, artifact 11963767921, presente e não expirado; São Carlos R2, run 40231520362, artifact 12613232136, presente e não expirado. Esta confirmação é sobre metadados dos artifacts, não leitura integral ou revalidação de todos os objetos brutos.
- Inspecionado diretamente `editorial/rmrp/inventario_tcesp_sp645_v2.py`: o script valida as contagens informadas nos três manifestos (102, 68, 16), exige 645 códigos na DCA, impede sobreposição de chave IBGE/ano/domínio e produz 10.320 posições. Ele **não demonstra por si só** existência e checksum de cada objeto armazenado; o rótulo `r2_validado` depende da validade do processo anterior de promoção e verificação dos manifestos.
- O modelo v2 ainda não incorpora RMJ nem TIC-TIM e não representa, diretamente, o status intermediário `artifact_temporario`. Os conjuntos RMJ comprovados documentalmente não devem ser inseridos como `r2_validado` sem persistência e readback.
- Tentativa de consultar a lista de execuções do workflow v2 pela interface disponível não retornou evidência acessível; **execução da v2 continua não confirmada**. Não se deve confundi-la com o sucesso do workflow v1 (run 40231222578).
- Rota de implementação delimitada: recuperar os 21 extratos RMJ identificáveis; catalogar e validar TIC-TIM por ano/município; somente depois executar inventário com estados separados e produzir fila `missing-only`. Esta segunda conferência não realizou novos downloads do TCESP nem alterou produção.

## Terceira conferência — leitura efetiva de artifacts ZIP (25/10/2026)
Recuperados via conector GitHub e inspecionados os conteúdos de:

1. `rmj-tcesp-2025-full-raw`, ID `11963767921`: ZIP com sete JSONs municipais, sete arquivos stderr vazios e `recovery_status.json` indicando `errors: []`, `cities: 7`. Em nova verificação independente, os sete JSONs apresentaram `bad_values: 0`, e as somas das listas de programas e ações reproduziram exatamente o total de investimentos liquidados de cada município. Soma regional independente: **26.542.555.907 centavos (R$ 265.425.559,07)**, diferença zero em ambas as granularidades. Esta verificação confirma a integridade contábil dos dados **presentes no artifact**, não a existência desses sete JSONs no R2.
2. `tcesp-sp645-matriz-cobertura-2023-2026`, ID `12612906187`: ZIP com `manifest.json` e `matriz_cobertura_tcesp_sp645_2023_2026.csv`. CSV inspecionado: **5.160 linhas**, colunas `codigo_ibge, ano, dominio, status, ultimo_mes_conhecido, acervo`. Distribuição exata: `cobertura_a_verificar=4982`, `persistido_r2_validado=102`, `persistido_r2_parcial=68`, `artifact_temporario_verificar=8`. São Carlos aparece no artifact antigo como temporário nos quatro exercícios x receitas/despesas. Este estado é **anterior** à promoção R2 de São Carlos, logo não deve ser apresentado como situação atual.

**Interpretação:** a matriz v1 possui duas categorias genéricas (despesas/receitas) para quatro anos e 645 municípios (5.160 posições); a v2 usa quatro domínios (10.320 posições). Não comparar contagens de posições entre matrizes como incremento de cobertura real. A v1 não inclui a RMJ como acervo persistido R2. A próxima validação deve ser executada sobre a v2 com leitura atual dos três manifestos e verificação de objetos R2; a reclassificação de RMJ/TIC-TIM deve ocorrer apenas após eventual promoção comprovada.

**Escopo desta etapa:** leitura dos dois ZIPs e reconciliação integral dos sete JSONs da RMJ; sem download de dados TCESP na fonte, sem escrita no R2, sem alterações em SQLite/API ou produção.
