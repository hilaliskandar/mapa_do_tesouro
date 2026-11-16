# S03 — persistência no R2, perfil do CSV de convênios e primeiro POST real Sefaz-SP

**Data:** 16/11/2026. **Escopo:** incorporar bases oficiais sistemáticas sem alterar a produção. **Estado:** ZIP/SQLite de convênios preservados e validados estruturalmente; consulta Sefaz em piloto de uma competência, ainda sem captura de parcelas como dataset.

## 1. Armazenamento privado — concluído

Após inspeção da página por **Crawl2AI**, a URL oficial `https://www.transparencia.sp.gov.br/Dados%20Abertos/Convenios/convenio.zip` foi adquirida e validada por GitHub Actions, utilizando os scripts existentes `deployment/upload_r2_source.py` e `deployment/download_r2_source.py`, as credenciais de CI já existentes e o bucket R2 já adotado pelo projeto.

**Evidência da execução:** [GitHub Actions 43914386820](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43914386820), job 133464503976, concluído com sucesso. Leitura de retorno de **ambos** os arquivos e consulta direta à listagem do bucket Cloudflare confirmam a persistência.

- Bucket privado: `financas-municipais-sp-canonico`
- Prefixo de snapshot: `sp_645/estadual/convenios/snapshots/1cca0556f08a1378bae52465796188788a5b3bb21e1b26c30c8c5c7d9a6b2b8f/`
- `convenio.zip`: 188.630 bytes, SHA-256 `1cca0556f08a1378bae52465796188788a5b3bb21e1b26c30c8c5c7d9a6b2b8f`.
- `staging.sqlite`: 1.699.840 bytes, SHA-256 `47b29b5d6c216be76cc473f987b250924ecb5b5ef65eb3df0b0911dfb3482bd6`.
- `source.manifest.json`: 739 bytes, hash registrado no log do CI.
- Teste pós-download: tabela `sp_convenios_raw` com 3.618 linhas, exercícios 2023=323, 2024=938, 2025=1.912, 2026=445.

**Alcance da validação:** integridade física, chaves locais por snapshot/linha, leitura de retorno e estrutura. Nenhum conjunto foi disponibilizado publicamente; ainda não foram definidos valores efetivamente pagos de convênios.

## 2. Perfil dos dez campos — concluído como diagnóstico

A execução [43915069168](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43915069168) leu o **SQLite do R2**, com SHA-256 conferido, e executou [`pipeline/qa/profile_sp_convenios_sqlite.py`](../pipeline/qa/profile_sp_convenios_sqlite.py) sem imprimir nomes/identificadores individuais.

| Coluna bruta | Formato observado | Distintos até 5 mil | Vazios |
|---|---|---:|---:|
| col_01 | Numérico (exercício) | 4 | 0 |
| col_02 | Texto, uma categoria | 1 | 0 |
| col_03 | Texto categórico | 21 | 0 |
| col_04 | Texto categórico | 51 | 0 |
| col_05 | Texto de beneficiário | 1.121 | 0 |
| col_06 | Principalmente numérico; candidato a identificador, não confirmado | 1.087 | 151 |
| col_07 | Data ISO | 317 | 0 |
| col_08 | Data ISO | 379 | 0 |
| col_09 | Texto/identificador, em parte vazio | 2.209 | 1.404 |
| col_10 | Formato numérico; conceito financeiro exato pendente | 1.912 | 0 |

**Regra:** perfil de formato não comprova significado do campo. O dicionário XLSX do portal descreve mais atributos que o ZIP, inclusive `Valor Total do Convênio` e `Valor Concedido`. Não afirmar que `col_10` seja o valor efetivamente repassado; mapear por documentação do próprio ZIP e comparação com detalhes oficiais. Também não confundir 1.121 denominações de beneficiários com o número de municípios.

## 3. Sefaz-SP — protocolo Web Forms validado em ambiente remoto

Fonte: `https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx`. O Crawl2AI forneceu HTML completo com formulário `method=post`, campos ASP.NET `__VIEWSTATE`, `__EVENTVALIDATION`, `Municipio`, `LiberacaoInicio`, `LiberacaoFim`, `Beneficiado`, `Tipo` e botão real `btnPesquisa`. A opção `Municipio=0582` corresponde a Ribeirão Preto **no cadastro interno da Sefaz**, não sendo código IBGE7.

O script [`pipeline/coleta/probe_sp_siafem_webforms.py`](../pipeline/coleta/probe_sp_siafem_webforms.py) reutilizou sessão, obteve GET e executou POST real para **Ribeirão Preto, janeiro/2025, beneficiado Prefeituras**, sem registrar os dados individuais em logs. [Workflow 43914847617](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43914847617) concluído com sucesso:

- GET: HTTP 200; POST: HTTP 200;
- Título retornado: `PesquisaComposta`;
- Conteúdo da resposta: 84.765 bytes;
- Tabela `grdTransferencia` presente, com quatro linhas `tr` no HTML;
- Estado de formulário ASP.NET presente na resposta.

**Limitação:** as quatro linhas de tabela não equivalem automaticamente a quatro transferências; podem incluir cabeçalho e totalização. O teste valida **comunicação/protocolo**, não extração, identificação de parcelas, totais ou classificação capital/custeio.

## 4. Próximas operações do lote

1. Implementar parser da tabela `grdTransferencia` com análise de linhas de cabeçalho, totalização, paginação, identificador, montante, valor negativo e data de liberação; executar QA de uma competência/município antes de ampliar.
2. Definir plano de varredura da Sefaz por períodos e municípios com checkpoint, reintentos, intervalos e proteção de limites; distinguir **Região Administrativa** e **RMRP34**, e cruzar código interno `0582` com IBGE7 mediante tabela oficial.
3. Finalizar semântica de cada `col_01..col_10` do arquivo de convênios SP comparando o dicionário e a estrutura de detalhes de instrumentos; criar camada tipada apenas para atributos com correspondência comprovada.
4. Produzir contagem de convenentes municipais SP645/RMRP34 sem inferir município a partir de nome ambíguo; atribuir `ibge7` somente com prova verificável.
5. Manter o acervo privado intacto; criar agregados aptos à prévia apenas após QA financeiro.

**Estado final:** `SP_CONV`: `snapshot_persistido=true`, `qa_estrutura=validado`, `qa_financeiro=pendente`; `SP_SEFAZ`: `protocolo_post_validado=true`, `dataset_parcelas_pendente=true`. `public_release_authorized=false`.
