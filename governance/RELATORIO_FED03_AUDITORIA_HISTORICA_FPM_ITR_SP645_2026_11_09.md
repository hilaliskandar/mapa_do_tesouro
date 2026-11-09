# FED03 — Auditoria de cobertura histórica FPM e ITR (1996–2026), Brasil e SP645

**Referência:** 09/11/2026. **Estado:** `qa_pass_coverage_and_identity_only`. **Homologação da cobertura, da interpretação de estados de célula e da correspondência territorial atual, NÃO da semântica contábil, dos totais históricos ou das receitas municipais declaradas.**

## 1. Proveniência e execução

Fontes originais **nacionais** STN [Transferências Obrigatórias da União — por Município](https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-obrigatorias-da-uniao-por-municipio), preservadas no **bucket privado existente** `financas-municipais-sp-canonico`:

| Fonte | Chave R2 (prefixo `sp_645/federal/stn/historical/1996_2026/source/`) | Bytes | SHA-256 |
|---|---|---:|---|
| FPM | `FPM_NACIONAL_a86cad83.csv` | 30.493.612 | `a86cad831115e02518198f4873967785a82eb3cbae651ef8505aa498c2cab088` |
| ITR | `ITR_NACIONAL_9c93138d.csv` | 20.858.658 | `9c93138d30b3c384ccb05ea91edbb8e6ee6f807f26ee2ce359e0a3e5b25f44ec` |

Lidos com verificação de hash e confrontados à fonte municipal SP645 de setembro/2026 `STN_SP645_ITEMS_2026_09_FROM_097638ce.csv`, SHA `3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb`. As fontes têm 31 colunas anuais, **1996 a 2026**, codificação CP1252, delimitador `;`, unidade monetária de origem preservada; a estrutura se organiza em **município × mês** com os anos em colunas. Os valores `COD_MUN` são identificadores da STN/SIAFI, **não códigos IBGE de sete dígitos**.

[Script de auditoria](../pipeline/qa/audit_stn_historical_sp645_coverage.py) e [workflow](../.github/workflows/fed03-stn-historical-sp645-coverage.yml). Primeira execução [42686388005](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42686388005) interrompida pelo tratamento inicial de linhas sem chave município/mês; a execução [42686514788](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42686514788) classificou essas linhas, mas identificou negativas entre parênteses `(180.529,62)` como formato ainda não reconhecido. A **execução final** [42686820271](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42686820271) concluiu com **success**, artefato de QA [13705257111](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42686820271/artifacts/13705257111). Nela o parser reconheceu explicitamente negativos contábeis entre parênteses, exigindo **zero células inválidas** no conjunto Brasil e SP; o resultado foi `qa_pass_coverage_and_identity_only`.

## 2. Cobertura nacional e territorial

| Controle | FPM | ITR |
|---|---:|---:|
| Linhas físicas do CSV (excluído cabeçalho) | 66.848 | 66.842 |
| Linhas válidas município–mês (5.570 × 12) | **66.840** | **66.840** |
| Linhas finais sem chave territorial/mês | 8 | 2 |
| Códigos `UF + COD_MUN` distintos | **5.570** | **5.570** |
| Registros duplicados na chave `UF–COD_MUN–mês` | **0** | **0** |
| Códigos `COD_MUN` paulistas com identidade IBGE validada em setembro/2026 | **645** | **645** |
| Nomes paulistas sem correspondência após aliases controlados | **0** | **0** |
| Equivalências históricas explícitas | **2** | **2** |
| Células numéricas inválidas em todo o Brasil, após regra de sinal | **0** | **0** |

As linhas sem chave município/mês estão **documentadas e não contabilizadas como meses municipais**; tratam-se, no arquivo obtido, de linhas finais com campos territoriais e de mês vazios, não de transferências que possam ser alocadas artificialmente. A auditoria preserva quantidade e amostras dessas linhas em QA JSON.

O crosswalk `COD_MUN`–IBGE contém **645 associações unívocas**, idênticas nas fontes FPM e ITR e verificadas contra o universo paulista STN decendial 2026/09, já conciliado com o SQLite materializado. Exceções: `6401` Embu ↔ `3515004` Embu das Artes e `6717` Moji Mirim ↔ `3530805` Mogi-Mirim. **Não aplicar indiscriminadamente o cadastro atual a todos os anos históricos**: extinções, criações ou denominações municipais em datas anteriores exigem auditoria temporal.

## 3. Estados das células, sem imputação de valores

A auditoria distingue **positivo**, **negativo**, **zero explícito**, **ausente** (célula vazia ou traço) e **inválido**. Valores entre parênteses no formato brasileiro são classificados como **negativos**; não podem ser descartados como ausência nem invertidos por conveniência. Nenhuma soma monetária foi calculada.

### São Paulo — cobertura por anos selecionados

O universo de cada coluna anual paulista tem **7.740 posições município–mês** (645 municípios × 12 meses).

| Ano | FPM positivo | FPM ausente | ITR positivo | ITR zero explícito | ITR negativo | ITR ausente |
|---|---:|---:|---:|---:|---:|---:|
| 1996 | 7.500 | 240 | 6.197 | 0 | 0 | 1.543 |
| 2000 | 7.740 | 0 | 6.203 | 0 | 0 | 1.537 |
| 2007 | 7.740 | 0 | 6.633 | 0 | **281** | 826 |
| 2010 | 7.740 | 0 | 6.525 | 0 | 0 | 1.215 |
| 2016 | 7.740 | 0 | — | **813** | 0 | — |
| 2023 | 7.740 | 0 | 7.075 | 0 | 0 | 665 |
| 2024 | 7.740 | 0 | 7.307 | **433** | 0 | 0 |
| 2025 | 7.740 | 0 | 7.207 | 0 | 0 | 533 |
| 2026 | **6.450** | **1.290** | 5.945 | 0 | 0 | 1.795 |

**Nota:** as células ITR positivas/ausentes de 2016 foram omitidas da tabela sintética acima; os valores completos constam na matriz de 124 linhas. Em **2026**, o FPM mostra 6.450 valores positivos (645 × dez meses) e **1.290 células ausentes**, equivalentes aos meses novembro e dezembro. Portanto, **o arquivo histórico não cobre o ano civil integral de 2026** na data auditada. Em 1996, 240 posições do FPM de SP estão ausentes; não se atribui a causa sem confrontar a evolução territorial e de repasses.

### Visão acumulada nacional, 1996–2026 (todas as posições, sem soma monetária)

| Estado | FPM — Brasil | ITR — Brasil | FPM — SP | ITR — SP |
|---|---:|---:|---:|---:|
| Células sem valor | **22.656** | **306.167** | **1.530** | **31.805** |
| Zeros explícitos | **0** | **12.307** | **0** | **1.246** |
| Valores negativos | **2** | **1.557** | **1** | **281** |
| Formatos numéricos não reconhecidos | **0** | **0** | **0** | **0** |

A classificação das **281 células ITR negativas de SP em 2007** e dos **813 zeros explícitos de SP em 2016** impede a substituição desses estados por `NULL` ou por outras hipóteses. A concentração de negativos pode refletir ajustes/estornos, mas a causa específica **não foi comprovada** na fonte e deve ser estudada antes da promoção fiscal.

## 4. Artefatos persistidos e conferência de integridade

O workflow final arquivou **apenas derivados de QA e candidatos**, sem alterar os arquivos originais, no bucket `financas-municipais-sp-canonico`:

| Objeto no prefixo `sp_645/federal/stn/historical/1996_2026/candidates/` | SHA-256 | Estado |
|---|---|---|
| `STN_1996_2026_COVERAGE_BR_SP.csv` | `678f68b588707c34c84630973629ef6722dd6e6538de56d79aaa95b644defeb3` | Readback SHA aprovado |
| `STN_202609_COD_MUN_IBGE_SP645.csv` | `c90c31678c1f2c1dfc269e85d158aaeade790908e277dcf83c6617cf3af59b7a` | Readback SHA aprovado |
| `QA_STN_1996_2026_COVERAGE_42686820271.json` | `df8d00f2adfe212fd74dfa3f9752132f9db9f6f4064ab426af4b32c7a6c0bd6e` | Upload aprovado; sem readback JSON específico |

A matriz de cobertura possui **124 linhas** (2 fontes × 2 territórios BR/SP × 31 anos). O CSV de correspondências possui **645 linhas**; ambas as saídas permanecem no R2 canônico e no [artefato de auditoria 13705257111](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42686820271/artifacts/13705257111).

## 5. Consequências para o modelo de integração

1. **Habilitar apenas o estágio de preparação**, não a carga no SQLite canônico. `FED03` continua `in_progress` até validação por ano/município com evolução territorial, unidade monetária e regras de retificação.
2. Projetar o formato **longo e rastreável** `COD_MUN_origem / codigo_ibge_validado / ano / mes / transfer_id / valor_raw / sinal_normalizado / estado_celula / source_sha / resource_id`, mantendo traço/célula vazia como **ausência**, zero como **zero**, e negativo contábil como **valor negativo**.
3. **Evitar dupla contagem do FPM de setembro**: o arquivo histórico de setembro/2026 já contém FPM regular + adicional FPM 1%; a série anual `dca_fpm_cota_mensal` tem conceito distinto.
4. Comparar dados de Fundeb e receitas municipais apenas após harmonizar fluxos, deduções e competência; a paridade entre dois arquivos da STN não comprova igualdade com receita municipal DCA/SICONFI.
5. Auditar explicitamente **1996 (lacunas FPM)**, **2007 (ITR negativo)**, **2016/2024 (zeros explícitos ITR)** e **2026 (meses ainda não informados)** como casos de teste de regras históricas.
6. A análise foi somente documental e quantitativa descritiva, sem reescrever fontes ou séries; **nenhuma migration aplicada, nenhum novo indicador fiscal publicado**.

**Ponto exato de continuidade:** produzir dicionário de normalização histórica de células com testes unitários (inclusive negativo entre parênteses); validar correspondência de códigos para períodos anteriores às criações e mudanças municipais; em seguida, projetar staging histórico por competência com QA e guardar apenas artefatos candidatos no R2.
