# Integração candidata do RGF monetário 2023–2024 — 16/10/2026

## Implementação sob PR #198
O módulo `pipeline/build/integrate_rgf_gate_e.py` integra, no banco SQLite **privado em reconstrução**, três contas RGF monetárias `rgf_despesa_total_pessoal`, `rgf02_divida_consolidada` e `rgf02_divida_consolidada_liquida`, para 2023–2024, usando o CSV corrigido Gate E. O SHA-256 do CSV é fixado em `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`.

O procedimento requer 1.290 linhas município–ano, identificador municipal no SQLite e valor compatível com a chave. Atualiza **apenas** observação `nao_aplicavel` para `observado` quando a referência tem número; não altera o que já está `observado` sem concordância dentro de R$0,01; não substitui estados `ausente` ou `em_revisao`. Na ocorrência de inconsistência, faz rollback de toda a transação. Valores de referência vazios não se tornam zero. Preserva `fonte_id` específico dos Anexos 01/02 e `referencia_origem` com SHA-256.

O construtor `pipeline/build/build_sp645_private_site.py` passou a aceitar `--rgf-gate-e` e integra antes do cálculo e exportação. O workflow `.github/workflows/sp645-private-site-artifact.yml` baixa o artefato oficial aprovado e verifica SHA antes de chamar o construtor. Os testes sintéticos `tests/test_integrate_rgf_gate_e.py` incluem digest rejeitado, aplicação condicionada, e rollback em conflito.

## Portões e restrições
- Alterações estão exclusivamente no branch do PR e **não foram integradas ao main**.
- O workflow de reconstrução privada dispara apenas por `push` ao `main` ou `workflow_dispatch`: **não foi executado na ramificação candidata nesta etapa**.
- Não há, portanto, evidência ainda de 1.371 conflitos removidos na API pública nem de novos boletins reconstruídos sobre base corrigida.
- Para fechar o gate: executar rebuild privado controlado em ref testada, verificar relatório `qa_rgf_gate_e_integration.json`, inspecionar `observacao`, `cobertura` e a API v1/v2 reconstruídas, auditar todos os status no cotejo Gate E, e só então decidir publicação.
- O painel estadual publicado e o boletim da RMJ permanecem intocados.
