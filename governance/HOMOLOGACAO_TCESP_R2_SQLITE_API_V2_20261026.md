# Estado de homologação TCESP — 26/10/2026

## Armazenamento R2
A auditoria de despesas estaduais TCESP 2023–2024, run 40263996213, teve ambos os jobs aprovados. Os artefatos QA foram preservados em armazenamento privado, com leitura de retorno e verificação SHA-256 de cinco objetos por exercício. Workflow run [40266854279](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40266854279), resultado `success` para 2023 e 2024.

Prefixos:
- `tcesp/estadual/despesas/2023/run_40263996213/`
- `tcesp/estadual/despesas/2024/run_40263996213/`
- `tcesp/estadual/despesas/2025/run_40262193781/` (persistência validada anteriormente, run 40263720734).

São preservados, por ano, `qa.json`, `r2_manifest.json` e os três CSVs agregados de investimentos grupo 44 por município/mês/estágio, programa e ação. Os ZIPs brutos estaduais de despesas NÃO estão neste lote.

## SQLite e API v2
Migração `data/schema/006_tcesp_investimentos.sql`; importação transacional `pipeline/build/import_tcesp_investimentos.py`. Exportação segregada de teste `pipeline/build/export_tcesp_investimentos_api_v2.py`. Workflow [40266890787](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40266890787) aprovado, com dados 2023–2025 e validação de estrutura de 1.932 arquivos municipais anuais, além de manifestos e agregados anuais. Nenhuma publicação pública ocorreu.

## Limites e próximos gates
- A execução de homologação foi em banco SQLite DESCARTÁVEL, não na base operacional. O site e a API pública não foram modificados.
- Antes de publicar, comparar o conjunto com a DCA e documentar diferenças contábeis, validar tamanho/performance de JSONs municipais, integrar a árvore da API complementar ao build existente, executar testes de regressão e preparar rollback.
- Dados TCESP são fonte adicional, nunca sobrescrever a DCA/FINBRA. Não comparar programas locais entre municípios automaticamente sem correspondência explícita.
- Exercício 2026 é parcial e ainda não faz parte desta camada estadual completa.
