# FED00-D — QA efetivo dos workflows federais e esquema de transferências STN
**Data de referência:** 09/11/2026. **Estado:** testes de origem comprovados e nova verificação territorial em execução; **nenhuma carga no banco canônico ou R2**.

## Execuções comprovadas por GitHub Actions e artefatos recuperados

### API federal / BCB
- Workflow [42651177787](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42651177787), job `129277614242`, conclusão **success** no job de auditoria; aviso metodológico: a própria sondagem retornou `partial` e código 2, explicitamente tratado como *continue-on-error* no workflow.
- Artefato [13689209731](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42651177787/artifacts/13689209731) `QA_FED00_API_PROBES.json` inspecionado diretamente: **4/5 endpoints `qa_pass`** e **1/5 `source_date_anomaly`**.
- `bcb_sgs_ipca_433`: três registros, 01/07/2026–01/09/2026, sem data futura na referência do runner, hash resposta `38c48e86239bda57162eac840aac4ce8d8b11d91eb70709921ffa95c7ccfdcff`.
- `bcb_sgs_selic_meta_432`: registros com datas de **07 a 09/12/2026**, futuras em relação ao registro de 09/11/2026; hash `45371430f2201434c3775dd10b551803b7a0b16864e88bf5f4cbae4bbdf3154d`. **Não homologar como informação observada até 09/11/2026.**
- Transferegov Parcerias: `openapi 3.1.0`, **18 caminhos**, SHA `b91d29099b6d17e36e88cb13067373ba763b8ec704aaa6e5a97a6b37901119a2`. Discricionárias: **13 caminhos**, SHA `269f37a85ae00c45823b596e2acd179c251a5d1b3e3730391fab233b59054106`.
- CKAN STN: **146 recursos (145 CSV + 1 PDF)**, catálogo SHA `be950f594382f692d3de4486304c41d7c0e5e03c8899bb9036c0d63aeea90060`.

### CSV STN: aquisição íntegra, interpretação territorial ainda em QA
- Workflow [42651092563](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42651092563), job `129277323771`, **success**, artefato [13689234572](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42651092563/artifacts/13689234572).
- Recurso CKAN `63b5f470-135f-4431-9158-ca8b7a43f61b`, título no catálogo `Transferencia_Mensal_Municipios_202610.csv`, **7.585.504 bytes** baixados, SHA-256 **`097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`**. Título e data de criação não certificam a competência contábil.
- CSV **Windows-1252 (`cp1252`)**, delimitador **`;`**, **126.807 linhas nacionais**, **10 campos**, **0 linhas com número de campos divergente**.
- Cabeçalho real e ordenado: `Município`; `UF`; `ANO`; `Mês`; `1º Decêndio`; `2º Decêndio`; `3º Decêndio`; `Item transferência`; `Transferência`; **campo final sem nome**.
- **Não existe coluna de código IBGE no arquivo testado.** A chave de integração territorial exigirá relação nome + UF → código IBGE oficial, com registro das ambiguidades. Não converter automaticamente município homônimo, município sem acento, abreviação ou nomes alterados em um ID arbitrário. Campos numéricos e classificações devem ser auditados antes de somas. Linhas nacionais não equivalem a número de municípios ou total de recursos de SP.

## Extensão territorial do teste

O script `pipeline/acquire/probe_stn_transfer_csv.py` foi aprimorado para registrar: distribuição de linhas por UF, linhas com UF=SP, número de nomes distintos de município de SP, cobertura efetiva de `ANO`/`Mês` no conteúdo e categorias de `Transferência`. A rotina **não atribui código IBGE**, não escreve observações no SQLite, não publica e não persiste arquivos no R2.

A alteração do script aciona automaticamente o workflow [42654718716](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42654718716). **O resultado da nova execução deverá ser confirmado por artefato e logs** antes de inserir contagens territoriais no README.

## Pendências de homologação

1. Recuperar o segundo artefato STN e verificar efetivos `sp_rows`, `sp_distinct_municipality_names`, `sp_period_counts`, `sp_transfer_types` e `uf_counts`.
2. Obter cadastro IBGE canônico da plataforma, produzir crosswalk nome/UF auditado e conferir os 645 municípios sem usar aproximações silenciosas.
3. Verificar se arquivos STN são cumulativos ou correspondem a uma única competência (inspecionar `ANO` e `Mês`), antes de compor séries temporais.
4. Examinar unidade e estrutura dos campos por decêndio antes de somar valores; não supor sinal, escala ou efeito contábil.
5. Manter `FED00=in_progress`; documentar falhas de API e anomalias de data sem classificá-las como ausência da fonte.
