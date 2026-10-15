# Extração integral TCESP de investimentos — programas e ações 2023–2024

**Data:** 15/10/2026. **Universo:** sete municípios da RM de Jundiaí; despesas liquidadas do grupo de natureza 44.

## Fonte efetivamente reaberta

Artefato GitHub Actions ID `11680818755`, ZIP com 14 arquivos JSON (`cabreuva_2023.json` a `varzea-paulista_2024.json`). Cada JSON contém endereço de origem da Despesa Detalhada do TCESP, `sha256_zip`, investimento liquidado em centavos, `programas_44_liquidado_completos` e `acoes_44_liquidado_completas`.

## Extração e conciliação

- **301 linhas de programas** dos 14 arquivos.
- **678 linhas de ações** dos 14 arquivos.
- **14 de 14** verificações de soma de programas versus investimento liquidado com diferença zero.
- **14 de 14** verificações de soma de ações versus investimento liquidado com diferença zero.
- Não foram somados valores empenhados ou pagos aos liquidados; o universo é exclusivamente investimento liquidado.
- Foram gerados os arquivos `rmj_programas_investimentos_2023_2024.csv`, `rmj_acoes_investimentos_2023_2024.csv` e `rmj_controle_conciliacao_programas_acoes_2023_2024.csv`, entregues nesta conversa, além do extrator `extrair_programas_rmj.py`.
- Chave principal de programa: município + exercício + código do programa, com descrição preservada; chave de ação: município + exercício + código do programa + código da ação, com descrição preservada.
- O mesmo código não deve ser considerado prova de continuidade de escopo ou entrega física entre exercícios.

## Limite da etapa atual

A extração integral auditada corresponde **somente a 2023 e 2024**. O material publicado de 2025 contém conciliação dos totais dos sete municípios e destaques de programas, mas os **14 conjuntos equivalentes completos por programa e ação para uma matriz trienal ainda não foram demonstrados nesta etapa**. Não preencher por inferência.

## Prioridade para o próximo processamento

Localizar ou recuperar os sete arquivos TCESP 2025 de Despesa Detalhada, aplicar exatamente os mesmos filtros e produzir listas integrais de programas e ações com verificações em centavos contra R$ 265.425.559,07 (DCA / TCESP 2025). Depois construir tabela 2023–2025 com estado de correspondência de códigos, descrições e ações, verificando mudanças de classificação pelas peças PPA/LOA pertinentes.

**Importante:** as bases CSV desta extração foram entregues em arquivos da conversa, mas não foram inseridas na página pública. O documento não declara nova conciliação da fonte completa 2025.
