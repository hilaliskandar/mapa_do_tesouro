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

## Gate adicional de integridade e tamanho da API complementar
- Execução [40268446243](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40268446243), `success`, artifact `12627472295`, relatório QA recuperado e examinado.
- Script `deployment/qa_tcesp_api_v2_preview.py` e workflow `.github/workflows/tcesp-api-v2-size-gate.yml`.
- 1.932 arquivos municipais/anuais (644 por exercício, 2023–2025), todos verificados contra os totais da API por município e estágio. Programa e ação têm somatórios iguais em cada arquivo.
- Maior JSON individual: 557.520 bytes; mediana: 92.705 bytes; todos abaixo do limite de 2.000.000 bytes. Status QA `pass`.
- Resultado é de **preview isolada**, não de implantação pública. Pendente integração do módulo ao build regular do site e testes HTTP, interface e regressão da API v2 principal.

## Interface experimental para investimentos — 26/10/2026
- Página `app/static/tcesp-investimentos.html` e script `app/static/tcesp-investimentos.js` adicionados como **prévia independente** do painel fiscal, sem alterar sua navegação pública.
- Filtros de município por código IBGE, exercício 2023–2025, estágio, nível programa/ação e busca textual; os totais são calculados em centavos, sem misturar estágios, e apresentados em reais.
- A rotina `deployment/stage_tcesp_api_v2.py` passou a copiar HTML e JS juntamente com a API isolada. A verificação HTTP passou a conferir a entrega e a paridade de bytes dos arquivos da interface.
- Primeira execução 40317801473 falhou por exigência textual excessivamente restritiva no teste HTTP do arquivo JS, sem erro de integridade ou de dados. Corrigido; [run 40317933869](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40317933869) concluído **success**, artefato HTTP `12647154610` e auditoria tamanho `12648350308`.
- **Limite:** o teste valida geração, incorporação e entrega dos arquivos, mas ainda não substitui um teste de interação em navegador real com navegação, filtros e acessibilidade, nem uma implantação autenticada de preview no ambiente externo. Sem publicação de produção.
