# INV-RMRP — Importação SQLite de desenvolvimento e QA das consultas territoriais

**Data:** 11/11/2026. **Escopo:** primeira carga testável de projetos Obrasgov candidatos em **cópia de SQLite de desenvolvimento**. Não altera a base canônica nem equivale a confirmação de investimentos executados.

## 1. Implementação

Arquivo: [`pipeline/build/import_inv_rmrp_obrasgov_dev.py`](../pipeline/build/import_inv_rmrp_obrasgov_dev.py). Entradas obrigatórias:
- `--source-db`: arquivo SQLite canônico pré-existente, utilizado somente para `sqlite3.backup()` na cópia;
- `--output-db`: caminho novo, diferente da origem e que não pode existir previamente;
- `--roster`: [34 IBGE7 da RMRP](INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv);
- `--candidates`: [224 projetos espacialmente triados](../app/static/data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json);
- `--schema`: [modelo relacional proposto](proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql), aplicado **somente na cópia**.

A cópia conserva `observacao`, `municipio`, `fonte`, `artefato_fonte` e os demais dados da origem. É recusada saída que coincida com a origem ou sobrescreva arquivo já existente. A conferência de todas as 34 chaves é bloqueante; erros de integridade referencial produzem rollback e descarte da cópia.

Entidades inseridas: `inv_projeto` e `inv_identificador_externo` (IDs oficiais Obrasgov), `inv_projeto_municipio` (município associado por ponto no polígono IBGE, papel `local_execucao`, mas registro candidato), `inv_localizacao` (pontos oficiais da API) e `inv_evento_financeiro` **exclusivamente no estágio `previsto`, com natureza não classificada**. Todo evento guarda referência a `artefato_fonte` da amostra, com hash SHA-256, e todo projeto mantém `qa_status='candidato'`.

**Não foram incluídos eventos de empenho, liquidação, pagamento, transferência efetiva nem instrumentos jurídicos**, pois a amostra Obrasgov não contém prova suficiente desses atos. Não há atribuição de custo territorial a municípios com múltiplos pontos, nem soma de projetos para métricas de investimento executado.

## 2. Resultado verificado por CI

Execução [GitHub Actions INV RMRP QA nº 43069017447](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43069017447) — **sucesso**. Teste com SQLite sintético construído dos esquemas efetivos `data/schema/001_initial.sql` + `004_provenance.sql` e 34 municípios inseridos do roster oficial. Isso testa a integração de esquema e dados de entrada **sem utilizar ou alterar a cópia canônica real em R2**.

| Critério | Contagem de QA |
|---|---:|
| Municípios da RMRP conferidos | 34 |
| Projetos Obrasgov candidatos importados | 224 |
| Relações projeto–município por interseção | 132 |
| Pontos válidos armazenados | 275 |
| Eventos de valor **previsto** | 226 |
| Eventos classificados como **pagos** | 0 |
| Projetos marcados como homologados | 0 |

O teste confirmou `PRAGMA integrity_check='ok'`, `PRAGMA foreign_key_check=[]`, unicidade de IDs, preservação da origem sem tabela `inv_projeto` e proibição de sobrescrever a saída. Os números de 132 relacionamentos podem superar 131 projetos com ao menos uma interseção, pois um projeto pode envolver mais de um município.

Os valores dos eventos propostos **não devem ser somados como pagamentos**, nem incorporados automaticamente ao indicador municipal de investimento liquidado. O campo `municipio` representa a interseção do ponto informado pela API, ainda sem confirmação documental independente.

## 3. Etapa seguinte para uso operacional da plataforma

1. Obter cópia verificável da **SQLite canônica real** (em ambiente autorizado) e executar o importador em arquivo separado, com backup e hash de origem.
2. Exportar tabelas de consulta estática por município, projeto e ano a partir do banco de desenvolvimento; manter marcador QA e proibir a agregação de previstos como executados.
3. Capturar de modo completo o universo Obrasgov/SP com o novo coletor, revisar localidades inconsistentes e atualizar os pontos do piloto.
4. Completar eventos financeiros federais e estaduais com documentos identificadores (Transferências Especiais/Parcerias, CGU, SIAFEM/SP) e classificar capital/custeio.
5. Executar 50 consultas de qualidade e só depois avaliar a homologação e publicação.

**Gates:** PR #233 segue rascunho. Nenhum merge, alteração no SQLite/D1/R2 produtivo, nem publicação como investimento realizado.
