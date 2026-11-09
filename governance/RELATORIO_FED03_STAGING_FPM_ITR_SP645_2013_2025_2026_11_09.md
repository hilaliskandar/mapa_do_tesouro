# FED03 — Staging histórico reversível de FPM e ITR, SP645, 2013–2025

**Referência:** 09/11/2026. **Estado:** `qa_pass_reversible_staging_only`; **sem homologação contábil DCA/FINBRA, sem migration SQLite, sem alteração de indicadores e sem publicação**.

## 1. Objetivo, escopo e origem

Foi produzido um extrato mensal padronizado e reversível de **13 exercícios, 2013–2025, 645 municípios paulistas e duas fontes STN (FPM e ITR)**. O período coincide com a extensão principal do histórico DCA da plataforma, mas **não implica que os valores possuam equivalência contábil automática**.

Os quatro objetos de entrada foram lidos do **mesmo R2 canônico `financas-municipais-sp-canonico`**, conferindo SHA-256 antes de processar:

| Fonte | Local R2 | SHA-256 |
|---|---|---|
| STN FPM nacional (1996–2026, colunas por ano) | `sp_645/federal/stn/historical/1996_2026/source/FPM_NACIONAL_a86cad83.csv` | `a86cad831115e02518198f4873967785a82eb3cbae651ef8505aa498c2cab088` |
| STN ITR nacional (1996–2026, colunas por ano) | `sp_645/federal/stn/historical/1996_2026/source/ITR_NACIONAL_9c93138d.csv` | `9c93138d30b3c384ccb05ea91edbb8e6ee6f807f26ee2ce359e0a3e5b25f44ec` |
| Crosswalk de 645 códigos STN `COD_MUN`→IBGE7 verificados para setembro/2026 | `sp_645/federal/stn/historical/1996_2026/candidates/STN_202609_COD_MUN_IBGE_SP645.csv` | `c90c31678c1f2c1dfc269e85d158aaeade790908e277dcf83c6617cf3af59b7a` |
| Matriz de cobertura histórica por fonte/território/ano | `sp_645/federal/stn/historical/1996_2026/candidates/STN_1996_2026_COVERAGE_BR_SP.csv` | `678f68b588707c34c84630973629ef6722dd6e6538de56d79aaa95b644defeb3` |

O procedimento [`stage_stn_historical_fpm_itr_sp645.py`](../pipeline/normalize/stage_stn_historical_fpm_itr_sp645.py) executa conversão **linha município/mês × coluna ano** para um formato longo de registros por `IBGE7–ano–mês–FPM/ITR`. Os dados de origem CP1252, separados por `;`, são extraídos como `valor_raw` e `valor_decimal`, com `estado_celula` explícito.

**Não há transformação de `COD_MUN` em IBGE por heurística:** a associação exige correspondência anterior no crosswalk QA aprovado. Os nomes históricos são mantidos e os zeros são separados dos traços e campos vazios.

## 2. Resultado de QA do extrato

[Workflow 42687597408](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42687597408), conclusão **success**, estado `qa_pass_reversible_staging_only`. Artefato [13704314992](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42687597408/artifacts/13704314992) com relatório `QA_STN_FPM_ITR_SP645_2013_2025.json`.

| Indicador | FPM | ITR | Total |
|---|---:|---:|---:|
| Registros municipais mensais | **100.620** | **100.620** | **201.240** |
| Valores positivos | 100.620 | 90.447 | 191.067 |
| Zeros explícitos | 0 | **1.246** | 1.246 |
| Ausentes (`NULL` conceitual; não zero) | 0 | **8.927** | 8.927 |
| Negativos | 0 | 0 | 0 |
| Município–ano–mês–fonte duplicados | 0 | 0 | 0 |

O sistema de validação confrontou **todas as contagens anuais por estado da célula** com a matriz histórica auditada de 124 linhas. Cada fonte possui **645 municípios × 12 meses × 13 anos**, totalizando 100.620 linhas. Nos anos 2016 e 2024, os **813 e 433 zeros de ITR** identificados na matriz histórica são preservados como `zero_explicito`; não foram imputados. Em 2025, por exemplo, há **533 posições de ITR ausentes**. O total de 8.927 ausências ITR dos 13 anos não foi preenchido.

O output possui colunas `codigo_ibge`, `uf`, `cod_mun_stn`, `municipio_origem`, `ano`, `mes`, `transferencia_origem`, `valor_raw`, `valor_decimal`, `estado_celula`, `source_sha256`, `status_contabil`. O último campo permanece `candidato_sem_conciliacao_dca` para todos os registros; nenhum foi promovido a variável fiscal canônica.

## 3. Persistência e integridade

Foi preservado no bucket R2 existente:

`sp_645/federal/stn/historical/2013_2025/candidates/STN_FPM_ITR_SP645_2013_2025_CANDIDATE.csv`

- **Tamanho:** 32.954.152 bytes
- **SHA-256:** `da38a2444cce5121ea81d504991fb85cc1cdedbfab28e0d06600ba1c14c9ff45`
- **Readback SHA:** aprovado no mesmo [workflow 42687597408](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42687597408)
- **QA JSON preservado:** `sp_645/federal/stn/historical/2013_2025/candidates/QA_STN_FPM_ITR_SP645_2013_2025_42687597408.json`, SHA-256 `504ecab3239b2dd5a2758d13501ebc06c2c9e46111166e62003afc70733afdee` (upload comprovado; readback JSON não testado)

A primeira execução [42687379206](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42687379206) falhou **antes de processar os registros** por erro de transcrição do SHA-256 esperado do ITR no workflow (61 caracteres em vez de 64). O SHA do arquivo em R2 estava correto; a referência no workflow foi reparada e a execução [42687597408](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42687597408) validou os quatro insumos e concluiu o staging. Nenhum dado parcial da tentativa rejeitada foi importado ou persistido como candidato homologado.

## 4. Critérios para promover os dados ao SQLite único

1. **Não copiar o FPM histórico diretamente para `dca_fpm_cota_mensal`.** Em setembro de 2026, a fonte histórica foi provada idêntica à soma de FPM regular e adicional de 1% (EC 112/2021). A mesma composição deve ser identificada por mês/exercício, principalmente julho, setembro e dezembro, antes de decidir sobre qualquer série anual.
2. **Preservar os estados:** `ausente` não é valor zero, `zero_explicito` não é ausência; negativos contábeis entre parênteses não são inválidos. A série normalizada de 2013–2025 SP não contém células negativas, mas o auditor histórico nacional confirmou negativos em 2001, 2004, 2007 e 2025 conforme fonte/território.
3. **Auditar identidade histórica:** o crosswalk é homologado para os 645 municípios **em setembro de 2026**; para anos anteriores, considerar criação, denominação, UF e possíveis alterações territoriais, especialmente antes de 2013.
4. **Documentar origem:** cada observação deve ter `COD_MUN` literal, IBGE7 validado, competência mensal, tipo, valor original, valor decimal e hash nacional.
5. **Confrontar estágio de caixa STN com natureza de receita municipal e deduções Fundeb**, usando MCASP e RREO/MSC do ente, em mesma competência. A paridade fonte STN × STN não comprova escrituração municipal DCA.
6. **Testar regressão e migrar somente após homologação.** A proposta de tabelas decendiais/fatos permanece em `governance/proposals`, sem migração para `data/schema` ou escritas em `observacao`.
7. **Nunca sobrescrever os snapshots R2 originais**, identificados por SHA de origem. Caso a STN retifique a série histórica, criar nova versão, comparar hash e gerar relatório de diferenças antes de substituição lógica.

**Próxima operação recomendada:** elaborar uma matriz de composição de FPM (regular/adicionais) por ano e mês, auditando temporalmente a cobertura das cotas extraordinárias; propor esquema de séries mensais candidatas compatível com `DCA 2013–2025`, sem validar receitas pela mera igualdade entre arquivos STN.


## 5. Cópia imutável identificada pelo conteúdo

A execução subsequente [42688035033](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42688035033) verificou a **reprodutibilidade exata** do CSV (201.240 linhas; SHA-256 `da38a2444cce5121ea81d504991fb85cc1cdedbfab28e0d06600ba1c14c9ff45`) e guardou uma cópia com **nome versionado pelo hash** em `sp_645/federal/stn/historical/2013_2025/candidates/STN_FPM_ITR_SP645_2013_2025_da38a244.csv`, 32.954.152 bytes, **readback SHA aprovado**. Esse é o objeto **preferencial para novas consultas e derivados**. A chave anterior terminada em `_CANDIDATE.csv` foi mantida como registro da primeira execução, mas não deverá ser utilizada como referência canônica de versão. A workflow agora inclui comparação explícita com SHA-256 completo e rejeitará mudanças de conteúdo sem escolha deliberada de uma nova chave. QA JSON da reexecução em `sp_645/federal/stn/historical/2013_2025/candidates/QA_STN_FPM_ITR_SP645_2013_2025_42688035033.json`, upload comprovado, SHA `d0b4694be72920561ba1f22b39cb17673a5a9bae6a9decdb4d7c6b1f861e6911`; readback específico do QA JSON não testado. **A cópia é apenas candidata; sem migração ou novos indicadores.**
