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

## FED00-E — Resultado de cobertura estadual e competência real do arquivo STN

O segundo workflow [42654718716](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42654718716), artefato [13691785591](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42654718716/artifacts/13691785591), terminou com **success** e seu `QA_FED00_STN_CSV.json` foi aberto diretamente. Fonte: exatamente os **7.585.504 bytes**, SHA **`097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`**, previamente conferidos.

- **Brasil:** 126.807 linhas, UF preenchida em 126.807/126.807, 0 linhas com divergência estrutural, 27 siglas UF.
- **São Paulo:** **13.889 linhas**, **645 nomes municipais distintos** (`UF=SP`), todos com `ANO=2026`, `Mês=09`.
- **Brasil inteiro:** **126.807/126.807 linhas com `ANO=2026`, `Mês=09`**. A denominação do recurso **`202610` se refere a sua publicação/carga**, não à competência econômica da tabela. **A competência demonstrada do conteúdo é setembro de 2026**, não outubro.
- Distribuição paulista, por classificação original de `Transferência`: `AJUSTE FUNDEB` **4.708**; `FPM` **645**; `FPM 1%` **645**; `FUNDEB` **5.414**; `IOF-Ouro` **1**; `ITR` **632**; `LC 176/2020 (ADO25)` **610**; `Royalties` **1.234**. **Total = 13.889 linhas**. A classificação do arquivo não corresponde, por si, a oito categorias mutuamente exclusivas de receita municipal na DCA.
- Cabeçalho **não possui `codigo_ibge`**. Portanto **645 nomes distintos não implicam ainda 645 códigos IBGE homologados**. A importação para `observacao` permanece proibida até crosswalk validado.

Foi implementado um teste reprodutível na mesma rotina, utilizando a [API IBGE de municípios de SP](https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios): normalização determinística de nomes, procura de correspondência unívoca, controle do número de registros IBGE, das chaves de sete dígitos e dos 645 nomes distintos. Se e somente se resultar em **645 combinações unívocas**, o workflow escreve `STN_IBGE_SP_MATCH.csv` (formato `;`) com `municipio_stn`, `municipio_ibge`, `codigo_ibge`, `match_method`. Se houver ambiguidades ou faltantes, o relatório apresenta listas de revisão e **não gera crosswalk homologado**. Workflows [42655203386](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655203386) e [42655242340](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655242340) acionados após mudanças; **validar status e artefatos antes de informar homologação da chave**.

A próxima etapa não é nova coleta dos 645 municípios pela API: a **extração nacional de setembro/2026 já comprova cobertura nominal de SP645**, restando conferir identificação unívoca, classificação, valores e regras de integração no SQLite existente. Sem modificação do banco ou R2.

## FED00-F — Resiliência de acesso e critério estrito de QA

As duas execuções iniciais de conciliação IBGE, [42655203386](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655203386) e [42655242340](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655242340), tiveram **erro de timeout na consulta remota ao Tesouro**. Os respectivos workflows apresentaram `success` no nível do job porque tinham `continue-on-error: true`, **mas os relatórios de sondagem registraram `failed_or_unavailable`**; portanto essas execuções **não são homologadas** e não geraram crosswalk IBGE. Este fato não invalida o CSV previamente verificado na execução [42654718716](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42654718716), cujo SHA continua como evidência histórica datada.

Correções versionadas:
- `pipeline/acquire/probe_stn_transfer_csv.py` agora aplica três tentativas de acesso com recuo controlado, registra o estágio `catalog`, `csv_download`, `csv_inspected` ou `ibge_api_crosswalk`, e preserva as evidências CSV mesmo que a API IBGE falhe depois.
- Workflows `fed00-api-probes.yml` e `fed00-stn-csv-pilot.yml` deixam de ignorar o código de retorno do coletor: teste parcial/falho deve encerrar o *job* com falha, preservando o artefato por `if: always()`. Isso impede confundir sucesso da operação de upload de logs com aprovação da fonte.
- Novas execuções iniciadas: [42655850668](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655850668) e [42655891469](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655891469); verificar seus estados, o `QA_FED00_STN_CSV.json` e eventual `STN_IBGE_SP_MATCH.csv` antes de homologar a conciliação.

**Status do cruzamento STN–IBGE permanece `pending`**; nenhuma correspondência foi inventada ou promovida ao SQLite. Correções de resiliência não equivalem a carga estadual.

## FED00-G — Fallback controlado ao GeoJSON já empregado na plataforma

As execuções [42655850668](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655850668) e [42655891469](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42655891469) devolveram **a mesma prova de CSV nacional íntegro** (SHA `097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`, 13.889 registros SP, competência 09/2026) e **`ibge_api_failed`**, por timeout após três tentativas na API oficial IBGE. O primeiro job concluiu com `success` por versão anterior de `continue-on-error`; o segundo concluiu com `failure`, corretamente alinhado à classificação `partial`. **Nenhum dos dois gera cruzamento homologado.** Os metadados CSV são preservados mesmo quando a API de IBGE falha.

A rotina agora reutiliza como alternativa exatamente o GeoJSON estadual versionado em `https://raw.githubusercontent.com/tbrugz/geodata-br/c39dfb040bfd466fe2a476bafed00749c5c42f16/geojson/geojs-35-mun.json`, já empregado no [workflow Siconfi Smoke](../.github/workflows/siconfi-smoke.yml) e no [módulo de aquisição DCA](../pipeline/acquire/siconfi_dca.py), nos quais `feature.properties.id` é usado como código IBGE. Essa alternativa **não cria base de municípios separada**: é uma referência externa reprodutível para cotejar nomes; a identificação canônica permanece na tabela `municipio` do SQLite. A API do IBGE continua como fonte preferencial de verificação.

Se o recurso substituto permitir correspondência unívoca, o programa produz apenas `STN_IBGE_SP_MATCH_CANDIDATE.csv`, classificado como **`candidate_secondary_reference`**, e mantém o QA total **`partial`**, mesmo com 645 códigos distintos. Somente resposta oficial IBGE com 645/645 unívocos gera `STN_IBGE_SP_MATCH.csv` e `qa_pass`. A verificação secundária não é homologação do cadastro. Alterações no [script](../pipeline/acquire/probe_stn_transfer_csv.py) e no [workflow](../.github/workflows/fed00-stn-csv-pilot.yml) acionaram [42656735846](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42656735846) e [42656758013](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42656758013); **confirmar artefatos antes de informar resultado**.


## FED00-H — Auditoria de dez divergências de nomes com a referência territorial

O artefato [13693186113](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42656735846/artifacts/13693186113) contém `ibge_crosswalk_qa` e comprova **645 nomes de municípios no STN**, **645 geometrias municipais no GeoJSON versionado**, **635 correspondências normalizadas exatas**, nenhuma ambiguidade e **10 nomes sem correspondência**. A chamada primária à API IBGE falhou por timeout; a consulta à referência cartográfica versionada funcionou, SHA da fonte `dbaf27769eb9bc847043872b41490eafd84fcb78d807690ca0f3757713f7f347`.

Nomes STN pendentes e causa documentada:
- **Oito pontuações de apóstrofo:** `Aparecida DOeste`, `Estrela DOeste`, `Guarani DOeste`, `Palmeira DOeste`, `Santa Bárbara DOeste`, `Santa Clara DOeste`, `Santa Rita DOeste`, `São João do Pau DAlho`. A referência cartográfica e o IBGE atual registram, respectivamente, `d'Oeste` ou `d'Alho`; equivalência por normalização de apóstrofos, não fuzzy matching.
- **Duas mudanças/grafias de denominação:** `Embu das Artes` (STN e IBGE atual) corresponde ao código IBGE **3515004**, enquanto a referência cartográfica legada usa `Embu`; `Mogi-Mirim` (STN) corresponde a **3530805**, grafado `Mogi Mirim` no IBGE atual e `Moji Mirim` na referência legada. São necessárias duas exceções explícitas com verificação do código, não algoritmo de aproximação.

Uma comparação de conteúdo **IBGE oficial atual vs GeoJSON cartográfico versionado**, indexada por `id` de sete dígitos, comprovou **645/645 códigos idênticos** e **quatro diferenças de nome**:
- `3515004`: IBGE `Embu das Artes` vs GeoJSON `Embu`;
- `3516101`: IBGE `Florínea` vs GeoJSON `Florínia`;
- `3530805`: IBGE `Mogi Mirim` vs GeoJSON `Moji Mirim`;
- `3550001`: IBGE `São Luiz do Paraitinga` vs GeoJSON `São Luís do Paraitinga`.

As quatro diferenças **não são quatro municípios distintos** e os códigos não devem ser remapeados por semelhança. O STN conserva `Florínia` e `São Luís do Paraitinga`, coincidentes com a referência legada nesses dois casos. A identificação é por código 7 dígitos, preservando a forma literal da fonte e a denominação IBGE no catálogo editorial.

**Correção implementada:** normalizador explícito de apóstrofos e duas equivalências condicionadas ao identificador `3515004`/`3530805`, somente quando a origem é o GeoJSON já usado na plataforma. Caso os 645 pareamentos se confirmem, gera-se `STN_IBGE_SP_MATCH_CANDIDATE.csv` **como candidato**, sem homologação como resultado da API IBGE ao vivo. A execução [42657206584](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42657206584) deverá ter artefato conferido antes de qualquer afirmação de 645/645 pareamentos efetivos. Nenhuma importação ou publicação.

## FED00-I — Crosswalk completo 645 por 645 em situação candidata

A execução [42657409755](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42657409755) gerou efetivamente o artefato [13693486021](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42657409755/artifacts/13693486021), recuperado e aberto. A sondagem preserva **SHA do CSV STN `097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`**, 13.889 registros SP, competência **2026/09**, **645 nomes STN**, **645 registros da referência cartográfica**, **645 matches com códigos distintos**, **zero unmatched/ambiguidades** e **duas exceções explícitas de denominação**. O arquivo `STN_IBGE_SP_MATCH_CANDIDATE.csv` foi verificado independentemente: **645 linhas; 645 códigos únicos; 645 nomes STN únicos; SHA-256 `20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c`**. O QA permanece **`partial`** e o job **`failure`**, intencionalmente, pois a fonte cartográfica alternativa não substitui a validação online do cadastro IBGE canônico.

As divergências de nomes têm [tabela de exceções versionada](STN_IBGE_EXCECOES_NOMES_2026_11_09.csv), com **12 casos relevantes**: oito grafias com apóstrofos, duas associações explícitas a códigos IBGE e duas diferenças entre grafia histórica STN/GeoJSON e denominação atual do IBGE. O catálogo de nomes oficiais da plataforma não será sobrescrito.

Para evitar perda do candidato em 30 dias, foi criado [workflow de arquivamento no bucket R2 existente](../.github/workflows/fed00-archive-stn-crosswalk-r2.yml), com gatilho `push`/manual, auditoria prévia rigorosa de 645 chaves e SHA, envio sob `sp_645/federal/stn/2026_09/candidates/` e leitura de retorno para verificação. A execução [42657908820](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42657908820) deve ser verificada antes de afirmar persistência em R2. **O prefixo `candidates` não é conjunto canônico de observações e o SQLite e o site permanecem inalterados.**

**Próximo gate:** leitura do arquivamento R2 e confronto dos 645 IDs com a tabela `municipio` do SQLite canônico; depois validar as rubricas e valores decendiais do STN com referências FINBRA/DCA, controlando que outubro/2026 no nome significa lote publicado e que a competência efetiva é setembro/2026.
