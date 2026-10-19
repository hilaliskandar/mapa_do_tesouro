# Matriz de validação externa RREO, RGF e CAPAG — 16/10/2026

## Evidência disponível e limites
1. **RGF Anexos 01/02, exercícios 2023–2024.** Já existe prova independente `governance/QA_GATE_E_RGF_HISTORY_PARITY_2023_2024.md`, com 30 municípios, 60 chaves município–ano, 420 comparações e zero divergência na série estadual candidata. Essa validação **não prova automaticamente** a igualdade dos registros individuais da API E2; falta o confronto candidato aprovado → API para cada código e campo.
2. **CAPAG.** O catálogo `data/catalogs/capag_sp645_official_2026_09.yml` fixa o arquivo oficial de posição de setembro/2026 (Google Drive ID `1BlT2WxtBIGVeP1b4-GM3Auv0OdU6p7C9`, SHA-256 `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`), ano-base 2025, 645 municípios e categorias oficiais. A posição de referência e o ano-base devem permanecer distintos. Não usar recomposição DCA/RGF como substituta da nota oficial. Falta cotejo código-a-código contra a API E2.
3. **RREO.** Indicador `rreo_rcl_oficial` depende da definição demonstrativa e período legal. A existência de dados em JSON não constitui conferência externa contra anexo original. Falta selecionar e arquivar fonte oficial por município/exercício e confrontar números e ausências.
4. **DCA 2025.** Confronto oficial independente concluído para cinco municípios e 68 valores E2, com nenhuma divergência (run `38896144224`). Não extrapolar aos outros demonstrativos.

## Protocolo de aceite ainda pendente
- Recuperar cada arquivo fonte já identificado e verificar SHA-256 antes de extrair resultados.
- Confrontar a API E2 com os dados aprovados nos estudos RGF, preservando unidade percentual em **pontos percentuais**, e nunca aplicar fator adicional de 100.
- Para CAPAG, comparar classificação exata por código IBGE, tratar `n/d` como categoria oficial, não como ausência, e verificar que o universo inclui apenas os municípios definidos no contrato.
- Para RREO, selecionar anexo e período legal da fonte, preservar a RCL publicada e confrontar ausências; não derivar RCL da receita DCA.
- Gerar arquivo auditável por comparação com código IBGE, exercício/posição, indicador, status, fonte, valor oficial, valor editorial, diferença, tolerância e resultado. Bloquear conclusão se a evidência oficial não estiver disponível.

**Decisão:** manter o PR #198 em homologação. Este documento caracteriza fontes verificadas e requisitos de confronto futuro; não afirma uma validação cruzada RREO/RGF/CAPAG que ainda não tenha sido executada.
