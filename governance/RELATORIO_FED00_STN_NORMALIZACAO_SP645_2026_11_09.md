# FED00 — Normalização reversível dos registros de transferências STN para SP645

**Referência:** 09/11/2026. **Estado:** `qa_pass_staging_only`. A carga física de **fonte nacional** e de **extrato paulista candidato** está concluída e preservada no **mesmo bucket R2 existente**. **Não há integração monetária homologada, nem escrita no SQLite, nem alteração da publicação.**

## 1. Linhagem verificável

| Artefato | Local R2 (bucket `financas-municipais-sp-canonico`) | SHA-256 | Tamanho |
|---|---|---|---:|
| Fonte original STN nacional | `sp_645/federal/stn/2026_09/source/STN_MUNICIPIOS_2026_09_097638ce.csv` | `097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24` | 7.585.504 bytes |
| Correspondência territorial STN–código IBGE | `sp_645/federal/stn/2026_09/candidates/STN_IBGE_SP_MATCH_CANDIDATE_20c80f6464de.csv` | `20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c` | 39.503 bytes |
| Extrato SP645 de itens originais | `sp_645/federal/stn/2026_09/candidates/STN_SP645_ITEMS_2026_09_FROM_097638ce.csv` | `3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb` | 2.836.369 bytes |
| Manifesto QA do extrato | `sp_645/federal/stn/2026_09/candidates/QA_STN_SP645_ITEMS_2026_09_42663210067.json` | `3ed1fda459425bb418f76ca28bdc0a3457acc9a0ca8d1be772393619e65aa366` | 1.375 bytes |

**Fonte federativa:** catálogo CKAN oficial `transferencias-constitucionais-para-municipios`, recurso `63b5f470-135f-4431-9158-ca8b7a43f61b`. **Competência efetiva no conteúdo:** setembro de 2026, apesar do nome do arquivo original `202610`. Origem com 126.807 linhas nacionais, 13.889 SP.

**Código e comprovação:** [`pipeline/normalize/prepare_stn_sp645_items.py`](../pipeline/normalize/prepare_stn_sp645_items.py), workflow [`fed00-stn-staging-sp645.yml`](../.github/workflows/fed00-stn-staging-sp645.yml), [execução 42663210067](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42663210067), **success**, com download/readback SHA do CSV de origem, do crosswalk e do extrato. Artefato de QA [13695507093](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42663210067/artifacts/13695507093) recuperado e lido.

## 2. QA de grão, território e campos monetários

| Controle | Resultado |
|---|---:|
| Linhas do extrato paulista | **13.889** |
| Municípios IBGE distintos | **645** |
| Chaves únicas `IBGE–ano–mês–transferência–item` | **13.889** |
| Linhas repetidas nesse grão | **0** |
| Campos monetários (3 decêndios × 13.889) | **41.667** |
| Células em decimal com ponto | **26.450** |
| Células inteiras | **15.217** |
| Células com formato inválido | **0** |
| Campos extras não vazios na coluna sem nome do CSV fonte | **0** |

O arquivo de saída tem separador `;`, codificação UTF-8, conserva **literalmente** `decendio_1_raw`, `decendio_2_raw`, `decendio_3_raw`, `municipio_stn`, `transferencia`, `item_transferencia`, `source_resource_id` e `source_sha256`; todos os registros são identificados como `candidate_unreconciled_financial_unit`. Os códigos provêm da correspondência previamente verificada com a **tabela `municipio` e o universo `SP_645` do SQLite real** ([relatório](RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md)).

Distribuição das linhas por **classe literal da fonte**, não por conceito de receita municipal: `FUNDEB` 5.414; `AJUSTE FUNDEB` 4.708; `Royalties` 1.234; `FPM` 645; `FPM 1%` 645; `ITR` 632; `LC 176/2020 (ADO25)` 610; `IOF-Ouro` 1.

**Importante:** as linhas têm categorias e itens distintos, incluindo `DEDU`, `FPM`, `IPVA`, `FPE`, `IPIE`, `COUN VAAT` e `COUN VAAR`; não se pode calcular um total orçamentário somando todos os registros e decêndios sem avaliar desdobramentos, deduções e sobreposições. O arquivo preserva os valores em texto justamente para impedir uma conversão ou interpretação monetária não homologada.

## 3. Estado dos gates e próxima ação

- **FED00 (arquivamento + território + staging):** subcontroles concluídos, com `qa_pass_source_snapshot_only`, `qa_pass_identity_only` e `qa_pass_staging_only`. Gate global ainda **`in_progress`** por ausência de conciliação contábil.
- **FED01:** preparar modelo incremental de eventos mensais e classificação documental, reutilizando as tabelas `municipio`, `fonte`, `artefato_fonte` e `build` existentes, sem duplicar cadastro municipal.
- **FED02:** revisar dicionário oficial STN, unidades e semântica de `Item transferência` vs `Transferência`, distinguir bruto/líquido/dedução e classificar rubricas que não se equiparam à receita recebida.
- **FED03:** eventual importação de fatos federais para tabelas complementares, somente após aprovação de esquema e critérios de QA.

**Próxima ação exata:** levantar o dicionário de dados STN (metadados do dataset) e a classificação orçamentária SICONFI/FINBRA aplicável, produzir matriz rubrica–item–natureza–estágio–risco de dupla contagem. Os mesmos arquivos R2 serão reutilizados para estudos RMSJRP, RMRP e demais universos, sem novas consultas na API para setembro de 2026.

Nenhum valor foi agregado, deflacionado, atribuído causalmente à LC 200/2023 ou registrado como receita municipal observada.
