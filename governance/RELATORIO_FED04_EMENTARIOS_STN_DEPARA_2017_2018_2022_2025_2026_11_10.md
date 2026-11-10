# FED04 — Ementários originais e DE-PARA STN de 2017: auditoria de classificação

**Data:** 10/11/2026. **Estado:** evidência oficial nova recuperada e incorporada ao QA metodológico; **não equivale à homologação integral de 2013–2025**.

## 1. Recuperação oficial e verificação de conteúdo

O [workflow `FED04 - verificar ementarios oficiais STN`](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42834851103), da branch `fed04-catalog-safety-20261110`, concluiu **success** após recuperação de documentos e leitura de planilhas via `openpyxl` em modo somente leitura. A primeira tentativa [42834359826](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42834359826) recuperara 2018/2022/2025, mas 2017 dera timeout; a segunda recuperou os quatro documentos. Os binários foram lidos apenas em diretório temporário do runner; somente o JSON de auditoria foi retido [no artefato oficial 13772568491 da primeira rodada](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42834359826/artifacts/13772568491) e no artefato da segunda rodada. **Nenhuma fonte ou tabela municipal foi modificada.**

| Exercício do arquivo | Bytes | SHA-256 (conteúdo recuperado) | Evidência |
|---|---:|---|---|
| 2017 | 688.075 | `b0961b948b2dde5c2f075c30859f3b5b8ab3b06a9f56eca775921362ccb3bf4e` | Ementário `EmentárioNR_Set-2017.xlsx`, abas `Ementário Anterior`, **`DE-PARA`**, `Novo Ementário` |
| 2018 | 739.743 | `ff67ceb30260e597673db60e67fa02168182f737ac77bf5554ddccc74deba501` | Arquivo intitulado **Novo Ementário das NR 2019, versão junho/2018**, com `Alter_Vrs2019` |
| 2022 | 443.997 | `e102266d37018e23fb8331386d85297ccbc81cf12895ab218817a61f691a36fb` | Ementário natureza receita 2022, pós-Portaria 1567/2022, aba `ENR-2022` |
| 2025 | 307.546 | `00f3b02e82fe45abb94205c7614524703032a2e5212682cddd867ac1ef7c2b2b` | Ementário 2025, Portaria STN/MF 2.216 de **30/09/2025**, aba `ENR - 2025` |

**Cautelas de versão:** o arquivo associado ao link do ementário válido para 2018 traz nome e abas de **2019**, publicadas em junho/2018; isso pode refletir compilação prospectiva e não deve ser tratado como prova única do plano de contas obrigatório para declarações de 2018. O ementário 2025 recuperado inclui atualização de setembro de 2025; sua composição pode conter códigos antigos/alternativos, logo **presença da conta no XLSX não prova lançamento efetivo no Anexo I-C** nem vigência uniforme ao longo do ano.

## 2. Prova direta do DE-PARA oficial 2017

Na aba **`DE-PARA` do arquivo STN 2017**, quatro registros foram extraídos com título dos dois lados:

| Linha da aba | Natureza anterior | Descrição anterior | Natureza nova no DE-PARA | Descrição nova |
|---:|---|---|---|---|
| 594 | `17210102` | Cota-Parte do FPM — **Cota Mensal** | `17180121` | Cota-Parte FPM — **Cota Mensal — Principal** |
| 597 | `17210105` | Cota-Parte do ITR | `17180151` | Cota-Parte do ITR — **Principal** |
| 645 | `17240100` | Transferências de Recursos do Fundeb | `17580111` | Transferências Fundeb — **Principal** |
| 646 | `17240200` | Complementação da União ao Fundeb | `17580121` | Complementação da União ao Fundeb — **Principal** |

A [matriz de quatro correspondências](FED04_DEPARA_STN_2017_E_MUDANCA_COMPLEMENTACAO_2018.csv) registra as quatro linhas e referências. **Avanço de confiança:** para a cota regular do FPM, a descrição oficial do código anterior `17210102` esclarece a dúvida pendente: trata-se nominalmente de **cota mensal**, e não do total de cotas. Isso não elimina a necessidade de comparar valores e rubricas extraordinárias nos 645 municípios.

**Ressalva de hierarquia:** o DE-PARA aponta para códigos novos terminados em `1` (**principal**). A DCA anual de 2018 utiliza códigos de agregação terminados em `0` em diversas contas: `RO1.7.1.8.01.2.0` para cota FPM mensal e `RO1.7.1.8.01.5.0` para ITR; `RO1.7.5.8.01.0.0` para distribuição Fundeb. Portanto **não são correspondências literais de código**, mas sim comparações de níveis do ementário: principal específico versus conta agregadora.

## 3. Nova divergência importante — complementação União/Fundeb

O DE-PARA de 2017 associa `17240200` a `17580121`, isto é, **rubrica de complementação do Fundeb dentro das transferências Fundeb**. Contudo, no ementário de 2018 recuperado, a aba `Alter_Vrs2019`, linha **230**, registra:

- Código `17180900`;
- Descrição «Transferências de Recursos de Complementação da União ao Fundo de Manutenção e Desenvolvimento da Educação Básica e de Valorização dos Profissionais da Educação — FUNDEB»;
- Observação explícita: **inclusão de conta para detalhamento mais apropriado à definição da origem dos recursos**.

O [crosswalk candidato inicial](FED04_CROSSWALK_DCA_ITR_FUNDEB_2013_2025_CANDIDATO.csv) já utilizava `RO1.7.1.8.09.0.0` para a complementação de 2018–2021. Agora a proveniência deve distinguir **2017 DE-PARA, inclusão documentada no arquivo de 2018 (com referência à edição 2019) e uso efetivo na DCA anual**. Não há autorização para trocar o código histórico indiscriminadamente: a definição de `17180900` pode ter entrado em vigor em data posterior à transição inicial.

O crosswalk **foi atualizado apenas em sua condição candidata**, assinalando `codigo_observado_transicao_em_revisao` para 2020–2021 e `nao_detectado_fonte_transicao_em_revisao` para 2018–2019. A ausência de linha nunca foi convertida em zero. **Nenhuma migração contábil foi executada.**

## 4. Confronto amostral ampliado da hierarquia FPM na API DCA

A [matriz de 15 consultas oficiais](FED04_QA_FPM_HIERARQUIA_15_CASOS_2026_11_10.csv) inclui Campinas, Ribeirão Preto, São Carlos, Osasco e Rio das Pedras em 2022, 2023 e 2025, a partir de `/ords/siconfi/tt/dca?an_exercicio={ano}&no_anexo=DCA-Anexo%20I-C&id_ente={ibge}`.

- **14/15** combinações continham conta-pai FPM e contas-filhas; nesses casos o **diferencial em centavos foi zero**.
- **Rio das Pedras 2022 e 2023:** conta-pai de FPM e conta-filha coexistem, com igualdade até o centavo.
- **Rio das Pedras 2025:** ausentes conta-pai e todas as rubricas-filhas selecionadas; trata-se de **ruptura localizada da declaração entre 2023 e 2025** e não ausência permanente de estrutura FPM na série municipal.
- O caso Campinas 2025 retornou uma única rubrica-filha, com paridade zero. Isso não é prova automática de presença ou ausência das cotas extraordinárias, apenas de fechamento aritmético das rubricas declaradas.

## 5. Situação de evidência e gates seguintes

**Comprovado diretamente:** recuperação/assinatura dos quatro XLSX; DE-PARA nominal 2017 FPM, ITR, Fundeb e complementação; conta 17180900 inserida em edição de 2018/2019; consistência de pai/filhas em 14 casos novos; anomalia de Rio das Pedras de 2025 não caracteriza toda a série.

**Ainda não comprovado:** vigência de todos os códigos do ementário 2018 para a DCA de 2018, mutações subsequentes e sua data de eficácia, equivalência dos valores históricos DCA/STN em toda a população, homogeneidade das modalidades de complementação antes/depois do Novo Fundeb, condições de receitas Fundeb em todos os municípios. **Não somar conta-pai com parcelas nem usar o número de linhas como beneficiários efetivos.**

**Próximas verificações:** rever versões com portarias de vigência e arquivos de mudanças; comparar rubricas 17180900/17580121 por ano em fontes oficiais de execução municipal; ampliar reconciliação FPM em 2013–2017 com identificação de cotas extras e com STN; investigar Rio das Pedras 2025 frente a 2024 e Sarutaiá DCA ausente; manter cenário de integração apenas `publicavel=0`, sem integração automática a catálogo ou publicação.

**Segurança:** PR #232 segue em rascunho e FED04 em andamento. Não foi modificado o SQLite canônico, o R2 ou os indicadores do painel.
