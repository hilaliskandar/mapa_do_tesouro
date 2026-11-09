# FED04 — Contas ITR/Fundeb existentes no SICONFI DCA e papel complementar da STN

**Data da consulta:** 09/11/2026. **Objetivo:** verificar diretamente, nos registros analíticos `DCA-Anexo I-C` de 2025, se ITR, Fundeb e deduções já existem na contabilidade municipal, distinguindo sua existência da seleção de variáveis do painel. **O piloto de oito municípios não é ainda a auditoria estadual dos 645.** Não houve alteração da base SQLite canônica nem dos indicadores publicados.

## 1. Fontes primárias e definição das contas

Fonte pública: [API SICONFI](https://apidatalake.tesouro.gov.br/docs/siconfi/) `GET https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&id_ente=<codigo_ibge>&no_anexo=DCA-Anexo%20I-C`. Verificada a identificação da prefeitura, do exercício e do anexo. As consultas permitem discriminar a coluna contábil (`Receitas Brutas Realizadas`, `Deduções - FUNDEB`, `Outras Deduções da Receita`) por código de conta.

| Conceito | Conta DCA observada | Natureza | Interpretação permitida |
|---|---|---|---|
| Cota-parte do ITR | `RO1.7.1.1.52.0.0` | Transferência da União | Receita bruta **e** retenção Fundeb explicitamente identificáveis |
| Complementação da União ao Fundeb | `RO1.7.1.5.00.0.0` | Transferência da União | Montante agregado de complementação, sem identificar autonomamente VAAT/VAAR na linha geral |
| Recursos recebidos do Fundeb | `RO1.7.5.1.00.0.0` | Transferência do fundo | Repasse distribuído; **não** confundir com soma de componentes de formação/dedução |
| FPM — cota mensal regular | `RO1.7.1.1.51.1.0` | Transferência da União | A variável atual da plataforma já usa essa conta, excluindo cotas extraordinárias |

A [normalização DCA](../pipeline/DCA_NORMALIZATION.md) já utilizava FPM mensal e cotas ICMS/IPVA; o catálogo semântico mais abrangente ([`mapa_semantico_inicial.yaml`](../referencias/catalogos/mapa_semantico_inicial.yaml)) **já reconhecia Fundeb por descrição**, sem que isso significasse uma variável individualizada entre as 46 importadas no SQLite de 2025. **ITR também estava disponível na origem DCA, não entre as 46 variáveis importadas.**

## 2. Evidência de execução reprodutível e disponibilidade

A amostra read-only de oito códigos IBGE foi feita pelo [script](../pipeline/qa/audit_siconfi_dca_itr_fundeb_2025_pilot.py) e [workflow](../.github/workflows/fed04-dca-itr-fundeb-2025-pilot.yml) e concluída na [execução 42700053330](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42700053330), estado **`qa_pass_pilot_accounts_only`**. São **96 combinações município × conta × coluna**, das quais foram preservados valores originais, status de observação ou ausência, descrição da conta e hash dos registros recuperados.

- **Oito municípios consultados:** Ribeirão Preto, São Paulo, Rio das Pedras, Sarutaiá, São José do Rio Preto, Olímpia, Guarulhos e Barueri.
- **Sete** retornaram linhas no Anexo I-C de 2025.
- **Seis** apresentaram as quatro contas DCA analíticas na coluna `Receitas Brutas Realizadas`; nas seis, também existem linhas da coluna `Deduções - FUNDEB` para ITR e FPM regular.
- **Rio das Pedras (3544004)**: API retornou 206 linhas de DCA em 2025, mas **não identificou nenhuma das quatro contas analíticas selecionadas**, apesar de haver contas agregadas. O `extrato_entregas` registra DCA da Prefeitura com status `HO`, em **14/05/2026**. Trata-se de **lacuna de detalhamento/registro a verificar**, não de ausência de DCA nem prova de receita zero. A inspeção revelou combinação aparentemente atípica de receitas e deduções em linhas agregadas; requer QA próprio, sem correção por estimativa.
- **Sarutaiá (3551207)**: API não retornou linhas de `DCA-Anexo I-C` para 2025; o `extrato_entregas` consultado não identificou `Balanço Anual (DCA)` correspondente. **Não se afirma atraso ou inadimplência sem análise do prazo e possíveis revisões.** Situação diferente de Rio das Pedras.

O primeiro [run 42699915743](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42699915743) interrompeu o piloto ao encontrar Sarutaiá sem anexo. O procedimento foi corrigido: `anexo_sem_registros`, `linha_ausente`, `zero_explicito` e `observado` são estados distintos, e a execução corretiva foi aprovada.

## 3. Valores exemplificativos de 2025 e controle da dedução

| Conta e coluna | Ribeirão Preto | São Paulo |
|---|---:|---:|
| ITR — Receitas Brutas Realizadas | R$ 3.156.915,82 | R$ 1.789.890,25 |
| ITR — Deduções - FUNDEB | R$ 631.382,85 | R$ 357.977,99 |
| Fundeb — Complementação da União, Receita Bruta | R$ 1.965.920,82 | R$ 117.028.677,98 |
| Fundeb — Transferências de Recursos, Receita Bruta | R$ 374.856.163,75 | R$ 8.065.438.177,73 |

Esses valores foram apresentados **apenas para demonstrar que a origem contém as contas e colunas**. A linha de complemento agregado não isola VAAT e VAAR, enquanto o arquivo STN de setembro/2026 as distingue por item. **Não comparar diretamente valores anuais DCA 2025 com a fonte mensal STN 09/2026.** Não somar deduções com receitas sem estabelecer estágio e sinal.

## 4. Ganho informacional efetivo da STN versus a DCA

| Conteúdo | Já disponível na DCA bruta? | STN acrescenta | Decisão |
|---|---|---|---|
| ITR — cota-parte municipal | **Sim**, como conta de receita e dedução | Série mensal/decendial para verificação e sazonalidade, 1996–2026 | Criar variável analítica DCA própria **antes** de promover STN a indicador fiscal |
| Fundeb — transferências recebidas | **Sim**, conta agregada em DCA | Decomposição por origem de formação (FPM, FPE, ICMS, IPVA, ITR, etc.) e por eventos de ajuste | Módulo analítico complementar, sem somar componentes que se sobrepõem |
| Fundeb — complementação da União | **Sim**, conta agregada em DCA | Itens federais identificados como VAAT e VAAR no snapshot 09/2026 | Desagregação potencial, sujeita a verificação temporal/contábil |
| Dedução do ITR para Fundeb | **Sim**, coluna própria em DCA | Evento mensal de dedução/formação e relação com FPM | Conferência bruto/líquido, não nova receita |
| FPM mensal regular | **Sim**, variável atual `dca_fpm_cota_mensal` | Repasses mensais e decendiais e adicionais como rubrica distinta | Não duplicar |

A STN amplia sobretudo a **periodicidade, os eventos federais e o detalhamento da formação/distribuição do Fundeb**; a origem municipal DCA mantém precedência para receitas contabilmente declaradas.

## 5. Persistência, QA e próximos controles

O [run 42700053330](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42700053330) persistiu no bucket privado **`financas-municipais-sp-canonico`**, sob prefixo `sp_645/federal/governance/dca_itr_fundeb_2025/candidates/`:
- `CONTAS_ITR_FUNDEB_PILOTO_42700053330.csv`, **22.287 bytes**, SHA-256 `43198862709d619a00e322ccf9877527307573ac3e7cebe7779901ea6470f5ad`, **leitura de retorno confirmada**.
- `QA_ITR_FUNDEB_PILOTO_42700053330.json`, **3.285 bytes**, SHA-256 `1a290faee0215e944d208c75a9ecd22da5b096921aaea3bf642f9ac72b3e183b`, upload confirmado; sem leitura de retorno independente para esse JSON.

**Prioridades:**
1. Confrontar Rio das Pedras e Sarutaiá com `extrato_entregas`, versões/retificações e DCA detalhada; não imputar FPM, Fundeb ou ITR a partir de STN.
2. Ampliar cobertura **paulista de DCA 2025** para contas de ITR/Fundeb com processamento respeitando o limite oficial de requisições, sem criar novas observações canônicas.
3. Avaliar as contas e códigos históricos de receita de ITR e Fundeb por exercício **2013–2025**, evitando aplicar código de 2025 indiscriminadamente a anos com classificações diferentes.
4. Só depois escolher **variáveis novas** no catálogo e integrar aos indicadores; **não aplicar migration ou publicar valores neste gate**.

**Conclusão:** ITR e Fundeb **já eram escrituráveis/consultáveis no SICONFI DCA**, e a STN realmente **acrescenta granularidade e rastreabilidade**, especialmente para Fundeb. A lacuna da plataforma está na seleção e validação de variáveis, não na ausência dessas informações em toda a base de origem.
