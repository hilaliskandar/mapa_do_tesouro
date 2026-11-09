# FED00 — Auditoria das rubricas STN e triagem de natureza contábil (SP645, setembro/2026)

**Referência:** 2026-11-09. **Resultado:** `qa_pass_descriptive_only`, complementado por `qa_pass_diagnostic_only` para FPM/Fundeb. **Nenhum total de receita municipal, nenhum lançamento SQLite e nenhuma publicação foram autorizados.**

## 1. Dicionário oficial, referência e hierarquia de evidências

O documento primário **Tesouro Transparente, “Metadados – Transferências Constitucionais Para Municípios”** está ligado ao dataset oficial [Transferências Constitucionais para Municípios](https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-constitucionais-para-municipios), recurso PDF `f7748189-6293-4999-bc6d-294428d949d8`, URL:

https://www.tesourotransparente.gov.br/ckan/dataset/af4e7c47-2132-4d9a-bd7c-34e28a210b03/resource/f7748189-6293-4999-bc6d-294428d949d8/download/metadados---transferencias-constitucionais---municipios.pdf

A leitura e inspeção da **página 1** desse PDF documental confirmou:
- **Unidade monetária R$ 1,00**, não R$ mil ou centavos em formato inteiro;
- frequência **mensal**, com colunas de primeiro, segundo e terceiro decêndios;
- **registro pelo critério de caixa**, base de extrações **SIAFI**;
- `Item que compõe a transferência` identifica componente da rubrica `Transferência`, e não um pagamento autônomo que se possa necessariamente acrescentar ao total da rubrica;
- parcelas de receitas federais passaram a compor Fundef/Fundeb, com deduções que chegaram a **20% a partir de 2009** segundo o histórico metodológico da STN;
- política de **revisão retroativa**, inclusive por estornos e erros, que pode alcançar o início do exercício em curso.

**Interpretação:** não confundir o registro de transferência da União no SIAFI (critério de caixa) com o lançamento da receita no sistema municipal (FINBRA/DCA), ou com o valor de um convênio específico. Não inferir a competência econômica do nome do arquivo: o lote CKAN `202610` contém `ANO=2026/Mês=09`. Eventual quantificação só pode usar política contábil de sinais, classes e deduções documentada.

## 2. Auditoria exaustiva de combinações de rubrica e item

**Fonte auditada, sem nova consulta federal:** `financas-municipais-sp-canonico/sp_645/federal/stn/2026_09/candidates/STN_SP645_ITEMS_2026_09_FROM_097638ce.csv`, SHA `3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb`. A integração com códigos IBGE foi aprovada **apenas quanto à identidade municipal** ([relatório de paridade SQLite](RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md)).

O código [`pipeline/qa/audit_stn_transfer_items.py`](../pipeline/qa/audit_stn_transfer_items.py) e [workflow 42666517409](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42666517409) executaram auditoria de **13.889 linhas**, **27 combinações distintas** de `Transferência × Item transferência`, mantendo **13.889 chaves originais**. Nos **41.667 campos decendiais**, existem **23.027 positivos**, **3.717 negativos** e **14.923 zeros**; não são contagens de pagamentos distintos. O total de campos é 13.889 × 3; não houve soma monetária.

### Classificação descritiva pelo texto literal da fonte

| Transferência | Itens literais observados | Linhas SP | Hipótese de triagem — NÃO homologada |
|---|---|---:|---|
| FPM | `FPM` | 645 | Identificar se valor principal representa líquido da dedução |
| FPM 1% | `FPM 1%` | 645 | Examinar componente adicional, sem somá-lo automaticamente ao FPM regular |
| FUNDEB | `DEDU`, `FPE`, `FPM`, `ICMS`, `IPI-EXP`, `IPVA`, `ITCMD`, `ITR`, `COUN VAAT`, `COUN VAAR` | 5.414 | Composição, dedução e complementação: evitar soma de parcelas com bases diferentes |
| AJUSTE FUNDEB | `FPE`, `FPM`, `ICME`, `IPIE`, `IPVA`, `ITCMD`, `ITR`, `AJUSTE FUNDEB VAAR` | 4.708 | Ajustes com sinais negativos, examinar referência e evento original |
| ITR | `ITR` | 632 | Conferir fluxo e dedução correspondente |
| LC 176/2020 (ADO25) | `LC 176/2020 (ADO25)` | 610 | Classificação legal específica, não equivaler automaticamente a outras rubricas |
| Royalties | `ANP`, `CFEM`, `FEP`, `ITA` | 1.234 | Verificar subcomponentes e natureza antes da agregação |
| IOF-Ouro | `IOF Ouro` | 1 | Conservar categoria própria e a especificidade territorial |

**Atenção:** no arquivo observado, `FUNDEB / DEDU` é uma linha com valores positivos nos três decêndios; isso não autoriza interpretar `DEDU` como uma transferência extra positiva. Os **3.717 campos negativos** ocorrem nos itens de `AJUSTE FUNDEB` (e não foram invertidos ou excluídos).

A matriz integral do diagnóstico foi arquivada no **mesmo bucket R2**:
- `sp_645/federal/stn/2026_09/candidates/STN_SP645_MATRIZ_RUBRICAS_2026_09.csv`, 4.349 bytes, SHA-256 `788be1cc3e87e63d1175bd7bea247ca26b2148a52c0138b077c919c2f09181d2`, **readback aprovado**;
- `sp_645/federal/stn/2026_09/candidates/QA_STN_SP645_RUBRICAS_2026_09_42666517409.json`, SHA-256 `344fda9da4ed3caaa49f95ebfe2565d1e6e943cefbb834ac501f49624db22710`.

### Diagnóstico exploratório de FPM versus FUNDEB/DEDU

O código [`pipeline/qa/audit_stn_fpm_fundeb_relations.py`](../pipeline/qa/audit_stn_fpm_fundeb_relations.py), workflow [42666819556](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42666819556), verificou **645/645 municípios** com registros de `FPM/FPM`, `FUNDEB/DEDU` e `FUNDEB/FPM`; **zero grupos faltantes**. Os valores foram somados **apenas dentro do mesmo item e mês para formar razões exploratórias**, sem totais estaduais e sem promover qualquer valor a receita municipal.

- Razão mensal **`FUNDEB/DEDU ÷ FPM/FPM`**: mínimo **0,2499999600**, mediana **0,2533690232**, máximo **0,5350149177**. **Nenhum município** na tolerância de 0,001 em torno de 0,20.
- Razão **`FUNDEB/FPM ÷ FPM/FPM`**: mínimo **0,0044529413**, mediana **0,0527098431**, máximo **1,3735987297**.
- A proporção 0,25 em alguns municípios é **compatível em tese** com uma dedução de 20% da base bruta quando o denominador é um saldo de 80%, mas **não prova** que o arquivo adote essa relação de forma geral. O máximo 0,535 demonstra a necessidade de identificar outras composições, estornos, bases e deduções antes de formular regra.
- QA preservado em `sp_645/federal/stn/2026_09/candidates/QA_STN_FPM_FUNDEB_RATIOS_2026_09_42666819556.json`, SHA-256 `532ca7758a2e0f791689c810919cc2daf6a5bf257cdcf765f105f766cec2dd3a`.

**Importante:** razões adimensionais são controles empíricos; não constituem medidas de capacidade fiscal, transferência líquida, arrecadação ou resultado orçamentário.

## 3. Regras para a próxima implementação

1. Preservar **as duas colunas literais** `transferencia` e `item_transferencia` junto a `codigo_ibge`, `ano`, `mes`, `decendio`, `resource_id`, `source_sha256` e versão do artefato.
2. Configurar **natureza de operação** (`principal`, `componente`, `deducao`, `ajuste`, `complementacao`, `outro`) apenas após validação de documentação aplicável a **cada par**. A matriz produzida possui **sinalizadores de triagem não homologados**, não classificação definitiva.
3. Não somar simultaneamente `FPM/FPM` e `FUNDEB/DEDU` nem `FUNDEB/FPM` sem equação explícita de bruto/líquido e prova de não sobreposição.
4. Não transformar numerais zero do arquivo em ausências. Não somar células negativas a positivas se sua natureza não foi identificada; conservar sinal e trilha do fato.
5. Confrontar o **mesmo mês**, código IBGE, categoria e natureza de receita com dados municipais, distinguindo defasagens de registro, retenções constitucionais e retificações.
6. Reusar o SQLite canônico: propor tabela **complementar de fatos decendiais** ligada a `municipio`, `fonte` e `artefato_fonte`. A inserção em `observacao` anual só poderá ocorrer após QA de agregação e de conceito.
7. Para histórico, identificar o arquivo pelo `resource_id` e **pela competência interna**; versionar hashes diferentes sem sobrescrever o snapshot já arquivado. A STN declara política de revisão retroativa.

## 4. Conclusão de gates

- **FED00:** fonte, identidade, staging, e matriz descritiva de rubricas **com QA e R2 concluídos**; **homologação contábil continua aberta**.
- **FED01:** há subsídios para especificação de entidades de fatos, mas **nenhuma migration aplicada**.
- **FED02:** dicionário oficial localizado, unidade/regime identificados e relações exploratórias medidas; sem conciliação operacional com DCA.
- **FED03:** um mês nacional e derivado SP645 preservados no R2. Cobertura histórica e ingestão produtiva **não executadas**.

**Próxima operação exata:** produzir especificação/migration SQL **proposta** para tabela de eventos decendiais, chave de origem e classificação auditável, testar com cópia isolada do SQLite e comparar com as variáveis existentes antes de homologar somas por rubrica. Nenhuma mudança no painel ou na base fiscal observada.
