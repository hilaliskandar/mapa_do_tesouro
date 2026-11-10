# FED04 — Harmonização histórica preliminar das contas DCA, 2013–2025

**Data:** 10/11/2026. **Estado:** auditoria documental e crosswalk candidato; sem promoção para `data/catalogs/variables_core.yml`, `crosswalk_variavel`, `variavel`, `observacao` ou base publicada.

## 1. Objetivo e fontes efetivamente inspecionadas

Recuperados e lidos os anexos originais I-C de receita do SICONFI/FINBRA para **2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020 e 2021** da [pasta canônica do projeto no Drive](https://drive.google.com/drive/folders/1K_Raj0pKEyktVY5BVa_raOZ4cQdJ8HQ4), conforme IDs e SHA listados no [catálogo anual](../data/catalogs/finbra_dca_sp_drive_2013_2025.yml). Fontes 2020 e 2021 vieram em XLSX; as demais em CSV. Para **2022, 2023, 2024 e 2025**, inspeção da respectiva aba do XLSX suplementar `Receitas 2022-2025.xlsx`, ID `1FX1QFhv3_lUhfqxEW0z5KJ0EWGPoMZGQ`. **Os números 2022–2025 desta etapa descrevem exclusivamente esse suplemento**; o QA estadual 2025 já dispõe de fonte anual primária e deltas da API, e seus números finais de cobertura não devem ser substituídos pelas contagens do suplemento.

O arquivo [`FED04_CROSSWALK_DCA_ITR_FUNDEB_2013_2025_CANDIDATO.csv`](FED04_CROSSWALK_DCA_ITR_FUNDEB_2013_2025_CANDIDATO.csv) contém 52 posições (13 exercícios × quatro conceitos), anotando código, estágio, cobertura de valores, origem e estado de homologação. Este crosswalk é **uma hipótese técnica de conta e estágio observados**, e não prova de equivalência fiscal intertemporal.

## 2. Três regimes contábeis documentados

| Intervalo observado | FPM | ITR | Fundeb recebido | Complementação federal Fundeb |
|---|---|---|---|---|
| **2013–2017** | `RO1.7.2.1.01.02.00` (rubrica geral) | `RO1.7.2.1.01.05.00` | `RO1.7.2.4.01.00.00` | `RO1.7.2.4.02.00.00` |
| **2018–2021** | `RO1.7.1.8.01.2.0` (mensal) | `RO1.7.1.8.01.5.0` | `RO1.7.5.8.01.0.0` | `RO1.7.1.8.09.0.0` (observada em 2020–2021; ausente da seleção 2018–2019) |
| **2022–2025** | `RO1.7.1.1.51.1.0` (mensal) | `RO1.7.1.1.52.0.0` | `RO1.7.5.1.00.0.0` | `RO1.7.1.5.00.0.0` |

A coluna contábil de **2013** é `Receitas Realizadas`; nos arquivos inspecionados de **2014–2025** é `Receitas Brutas Realizadas`. **Não confundir** essas rubricas com `Deduções - FUNDEB`, `Deduções da Receita` ou transferências STN de competência mensal. Os anos 2018–2019 não apresentaram conta de complementação federal selecionada na busca da fonte original, mas **ausência de linha não equivale a ausência de transferência**.

**FPM exige revisão semântica especial:** 2013–2017 usa rubrica genérica de FPM e, a partir de 2015, há códigos separados para cotas extraordinárias `RO1.7.2.1.01.03.00` e `RO1.7.2.1.01.04.00`. Em 2018–2021, cotas extraordinárias figuram em `RO1.7.1.8.01.3.0` (dezembro) e `RO1.7.1.8.01.4.0` (julho). Em 2022–2025, o pai `RO1.7.1.1.51.0.0` pode abrigar a cota mensal e extraordinárias, e não pode ser somado à filha `RO1.7.1.1.51.1.0`. **Não declarar a rubrica 2013–2017 idêntica à cota mensal 2022–2025 sem prova pelo ementário.**

## 3. Presença de registros de receita: universo e cobertura

Contagens de **linhas da coluna de receita realizada**, não quantias monetárias ou municípios comprovadamente beneficiários. Base anual original de 2013–2021; XLSX suplementar em 2022–2025. Onde a rubrica não foi identificada, usar travessão documental, **não zero**.

| Ano | FPM (código principal conforme período) | ITR | Fundeb recebido | Complementação União |
|---|---:|---:|---:|---:|
| 2013 | 640 | 629 | 626 | 14 |
| 2014 | 626 | 609 | 615 | 4 |
| 2015 | 641 | 632 | 635 | 6 |
| 2016 | 642 | 622 | 632 | 9 |
| 2017 | 643 | 629 | 638 | 4 |
| 2018 | 643 | 628 | 640 | não identificada |
| 2019 | 636 | 622 | 635 | não identificada |
| 2020 | 644 | 629 | 645 | 1 |
| 2021 | 644 | 633 | 645 | 2 |
| 2022 | 642 | 634 | 640 | 5 |
| 2023 | 642 | 636 | 626 | 146 |
| 2024 | 645 | 638 | 628 | 202 |
| 2025 | 641 | 631 | 621 | 451 |

**Nota sobre 2025:** a matriz QA estadual completa de 645 municípios inclui valores verificados no CSV anual e deltas da API para Braúna/Tanabi. Portanto a cobertura já documentada como **643 FPM mensal, 633 ITR, 623 Fundeb recebido, 453 complementação federal** é a referência específica para **2025 SP645**, e não os valores de 641/631/621/451 do suplemento acima.

## 4. Distinções fundamentais para o modelo canônico

1. **ITR:** tratar `cota-parte do ITR` na receita de transferências (`RO1.7.*`) e **nunca confundir** com rubrica de imposto de competência municipal `RO1.1.1.2.01.*`, que também menciona ITR em pequenos números de declarações.
2. **Fundeb recebido:** componente de transferência distribuída ao município; não adicionar de forma automática a complementação da União sem checar em cada exercício se há sobreposição no demonstrativo.
3. **Complementação federal:** série de presença de código varia acentuadamente e não deve ser tomada como evolução substantiva dos benefícios sem conferir a legislação, o plano de contas e a composição VAAT/VAAF/VAAR.
4. **Deduções Fundeb:** manter coluna e natureza distintas de `receita bruta`. Os valores positivos do item STN `FUNDEB/DEDU` são registros de uma dedução identificada, não receita acrescida.
5. **Ausência:** registro faltante conserva estado `ausente` ou `em_revisao`; Sarutaiá permanece sem DCA 2025 localizável, mas tem RREO/MSC. Rio das Pedras mantém anomalia estrutural do I-C; não converter agregados em contas específicas.
6. **Reprodutibilidade:** cada observação futura deve carregar `codigo_ibge`, exercício, `variavel_id`, `fonte_id=SICONFI_DCA`, artefato SHA, código/coluna originais e identificação de regra no `crosswalk_variavel`; para valores recuperados de suplemento ou API, preservar a origem.
7. **Não duplicar:** contas DCA de 2025 já compõem agregados brutos; novos itens devem ser **decomposição analítica** e não receita a ser somada ao total da base.

## 5. Proposta de integração sem publicação

Conservar o esquema `data/schema/001_initial.sql` e o registro de proveniência `data/schema/004_provenance.sql`. Novas variáveis candidatas: `dca_itr_cota_parte_bruta`, `dca_fundeb_recebido_bruto`, `dca_fundeb_complementacao_uniao_bruta` e, em camada separada, `dca_itr_deducao_fundeb`. A cota FPM mensal existente **não deve ser recarregada**. Cadastrar crosswalks **ano/esquema/estágio** após revisão oficial, começando por 2025 e estendendo por regimes. Manter `publicavel=0` em qualquer piloto e tratar alterações no catálogo com cautela: `pipeline/build/load_catalog.py` atualmente **não persiste** as flags `publicavel` e `ativo` na instrução `INSERT`; carregar um catálogo candidato diretamente introduziria risco de publicação por default `publicavel=1`. **Portanto não adicionar candidatas aos catálogos carregados automaticamente antes de corrigir/testar essa propriedade**.

Critérios de aprovação antes da promoção: (i) ementário por exercício; (ii) unicidade por `municipio×ano×variavel`; (iii) tratamento de estado/ausência e dedução; (iv) teste de sobreposição com FPM/STN e contas-pai; (v) valores DCA em centavos, sem perda de precisão; (vi) regressão em SQLite temporário, `publicavel=0`; (vii) aprovação explícita do gate FED08 para exposição pública.

## 6. O que foi efetivamente realizado

**Concluído nesta etapa:** leitura de nove originais anuais 2013–2021 e quatro abas 2022–2025; identificação e contagem das rubricas selecionadas em 13 exercícios; crosswalk documental candidato com 52 posições; conferência do esquema e rotina real de carga do catálogo. **Não concluído:** revisão integral dos ementários oficiais, teste formal de equivalência de 2013–2017 FPM mensal, tratamento da complementação federal 2018–2019, validação de valores históricos por API, implantação na tabela `observacao` ou publicação de novas variáveis.
