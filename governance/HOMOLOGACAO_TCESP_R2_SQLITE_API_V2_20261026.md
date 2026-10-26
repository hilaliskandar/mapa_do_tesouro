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

## Validação de interação em Chromium — 26/10/2026
- Workflow `.github/workflows/tcesp-browser-qa.yml` e script `deployment/qa_tcesp_browser.py`; [execução 40320429776](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40320429776) concluída `success`.
- Teste de interface em navegador Chromium headless após recompor SQLite isolado 2023–2025, reconstruir API prévia, conferir integridade e simular HTTP local.
- Cenários implementados: carregamento inicial 2025 liquidado/programas, mudança para ações, troca de exercício 2023, filtro sem ocorrências, remoção de filtro, rejeição de IBGE incompleto e recuperação após correção; verificação de erros JavaScript.
- Artefato de evidência `tcesp-browser-qa`, ID `12648742249`; também artefatos de tamanho `12648218089` e HTTP `12648093299`.
- **Não equivale a regressão completa do painel fiscal ou aprovação de publicação pública**; faltam integração com navegação principal, checagem de acessibilidade ampliada, correspondência contábil TCESP/DCA e implantação em ambiente de homologação externo.

## Regressão integrada concluída — execução 40322855496
- Run `40322855496` terminou `success` na execução sobre cópia do acervo fiscal real da prévia; a rotina `deployment/qa_pages.py`, a incorporação opcional e o HTTP local passaram.
- Artefato `12650696973`: `real-qa-tcesp.json`, `real-http-qa.json`, `real-browser-qa.json`. Conferência do relatório do Chromium: `status=pass`, sete cenários (`default_2025_liquidado_programas`, `change_to_actions`, `change_year_2023`, `filter_zero_rows`, `clear_filter`, `invalid_ibge_rejected`, `recover_after_invalid`), `js_errors=[]`.
- O endpoint remoto `/data/api/v2/manifest.json` não foi homologado: execução anterior obteve HTTP 403; nova consulta externa também não conseguiu acessá-lo. O teste aprovado usa os dados fiscais v1 reais e os derivados TCESP isolados; não prova a acessibilidade pública da API v2 principal.
- Nenhuma publicação ou alteração da base fiscal pública efetuada.

## Diagnóstico de conteúdo HTTP da API v2 remota — 26/10/2026
- Sondagem somente leitura: [run 40325414635](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40325414635), `success`, ferramenta `deployment/diagnose_v2_remote.py`, artefato de evidência `remote-v2-http-diagnostic`.
- URL `https://preview.finbra-tic-tim-referencia.pages.dev`: `/data/manifest.json` retornou HTTP 200 e `application/json`, prefixo com JSON.
- **Diferentemente do erro HTTP 403 observado na tentativa anterior**, nesta sondagem `/data/api/v2/manifest.json` e `/data/api/v2/catalog/municipalities.json` retornaram HTTP 200, mas `text/html; charset=utf-8`, sem JSON. Possível fallback HTML da plataforma, a confirmar com configuração de rotas/artefatos. **Acessibilidade de JSON da API v2 não homologada.**
- Proibir interpretação de `HTTP 200` isolado como aprovação de endpoint JSON. Testes externos devem verificar também `Content-Type`, parse JSON e o contrato de dados esperado. Sem publicação.

## Verificação da existência da API v2 estadual no artefato privado
- Em [execução 40326152205](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40326152205) a validação integral `deployment/qa_api_v2.py` passou para o artefato privado da execução `40317752109` (`sp645-private-site-40317752109`).
- Artefato contém `data/api/v2/manifest.json` JSON: 645 municípios, 174.795 observações e catálogo de 75 variáveis; catálogo de municípios JSON íntegro com 645 entradas.
- Na mesma auditoria, o alias `preview.finbra-tic-tim-referencia.pages.dev` persistiu retornando HTML para dois caminhos `/data/api/v2/*.json`. Logo, a fonte dos dados v2 **está materializada no artefato estadual privado**; a prévia examinada não entrega esses arquivos corretamente. É necessário verificar o alias SP645 efetivo e o processo de publicação antes de qualquer implantação, sem substituir inadvertidamente o snapshot v1.
- A execução de auditoria foi somente leitura; não realizou deploy. Controle obrigatório: aceitar endpoint apenas se `Content-Type` JSON, parse JSON válido e esquema correto.

## Inventário conclusivo de deployments Cloudflare Pages — 26/10/2026
- Consulta **somente leitura** ao endpoint de administração Cloudflare Pages do projeto `finbra-tic-tim-referencia`, varrendo as 25 páginas de 20 deployments (492 registros no total). A conta confirmou o alias isolado `sp645-candidate` em **09/10/2026 10:20:44 UTC**, deployment `cfbac01c-d9f6-4a43-a672-c203b85bff37`, branch `sp645-candidate`, commit `9c381a86b41bce6eb3fad07aa8d0cf7a0ab56a4a`, status `success`.
- Também houve deployments anteriores `sp645-candidate` em 09/10/2026 09:02 UTC (`ac88c1ec-f43c-4f41-93c7-c3c8b052a7b8`) e 08:58 UTC (`7b6519de-ccde-4625-bd88-e174e3c28b79`). Nenhum deployment dessa branch posterior a 09/10 foi encontrado no histórico retornado.
- Alias `preview`: último deployment localizado em **07/10/2026 16:17 UTC**, ID `d3c41b36-a042-44c4-a6e6-3acf34f5c412`; implantação `main` mais recente localizada em **09/10/2026 10:26 UTC**, ID `bfa41be5-1eb3-4fcb-827a-fbe9ca3e6ce4`. Os demais deploys recentes na conta são principalmente branches `pr-*`.
- O artefato SP645 privado homologado (`run 40317752109`, 26/10/2026; QA `40326152205`) **é posterior ao último deploy conhecido do alias estadual**. Assim, a ausência de JSON da API v2 em `sp645-candidate` é consistente com uma implantação antiga; a inspeção de deployments não demonstra por si só se existia fallback HTML naquela versão.
- **Próximo passo autorizado tecnicamente, ainda não executado:** preparar e homologar um novo deployment de **prévia isolada**, com nome de branch específico e verificações externas de JSON e regressão, sem alterar `main`, `preview` ou `sp645-candidate` até a aprovação da versão substituta. Não foi feito deploy nesta diligência.

## Prévia externa da API v2 SP645 aprovada — 26/10/2026
- Workflow [40329504327](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40329504327) terminou com `success`: artefato SP645 já validado recuperado, contratos locais `qa_api_v2.py` e `qa_sp645_pages.py` aprovados, implantação apenas no alias `sp645-v2-qa-20261026` e verificações HTTP externas `qa_remote_sp645_v2_json.py` e `qa_sp645_pages.py` aprovadas.
- URL: `https://sp645-v2-qa-20261026.finbra-tic-tim-referencia.pages.dev`; os aliases anteriores e a branch de produção não foram alterados.
- O êxito comprova a entrega externa da **API fiscal v2 estadual** no novo alias, não a publicação da camada adicional TCESP de investimentos. Próximo passo: compor camada TCESP com site SP645, homologar externamente e documentar comparabilidade contábil antes da promoção.
