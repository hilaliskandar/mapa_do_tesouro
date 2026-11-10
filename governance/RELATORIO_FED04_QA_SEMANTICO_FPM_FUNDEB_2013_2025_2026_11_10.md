# FED04 — Auditoria semântica por fonte oficial: FPM, ITR e Fundeb (2013–2025)

**Data de pesquisa:** 10/11/2026. **Resultado:** avanço na evidência semântica, mas **sem homologação histórica integral** e sem alteração da base canônica. Este relatório distingue documentos efetivamente lidos, extrações da API e hipóteses contábeis.

## 1. Fontes oficiais verificadas

1. [STN — edições anteriores do ementário da receita](https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/edicoes-anteriores-ementario-da-receita-orcamentaria/edicao_anterior_ementario-da-classificacao-por-natureza-de-receita-tabela-de-codigos): página **recuperada por Crawl2AI**; lista ementários de 2014–2023 com links documentais por exercício (2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023). O conteúdo dos arquivos XLSX anexos **não foi integralmente extraído nesta etapa**. O link documental é índice de fontes e não valida sozinho todas as rubricas.
2. [STN — ementário atual e de 2024–2027](https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/ementario-da-classificacao-por-natureza-de-receita-tabela-de-codigos): página **recuperada por Crawl2AI**, incluindo referência ao ementário válido para 2025. Os links para binários `thot-arquivos.tesouro.gov.br` não puderam ser processados pelo Crawl2AI na diligência; **não declarar leitura do arquivo 2025**.
3. [SICONFI — nota de 11/01/2017 sobre o novo ementário](https://siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=9102): texto **recuperado**; confirma reorganização da codificação e existência de um de-para elaborado pela STN no processo de transição.
4. [TCESP — receitas municipais de Matão em 2016](https://transparencia.tce.sp.gov.br/municipio/matao/2016/receitas): página **recuperada**; classifica a subalínea `17210102` como cota-parte do Fundo de Participação dos Municípios e `17210105` como cota-parte do ITR. **Evidência concreta paulista para o regime 2013–2017**, mas sem equivalência matemática exaustiva de todas as transferências.
5. [FNDE — relatório de gestão 2021, financiamento da educação básica](https://www.gov.br/fnde/pt-br/acesso-a-informacao/transparencia-e-prestacao-de-contas/relatorio-de-gestao-1/relatorios-de-gestao-anos-anteriores/relatorio-de-gestao-2021/resultados-da-gestao-1/financiamento-da-educacao-basica): texto **recuperado**; documenta a passagem ao Novo Fundeb a partir de 2021, com complementação VAAF e VAAT e implementação do VAAR a partir de 2023, bem como os percentuais anuais do mecanismo.
6. [FNDE — página de consultas, repasses e bases por exercício](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/consultas): página **recuperada**; fornece caminhos oficiais de verificação com STN, Banco do Brasil e portarias históricas de 2013 a 2026.
7. [API oficial SICONFI DCA Anexo I-C](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente=3550308) para São Paulo, ID IBGE `3550308`, exercícios 2013, 2015, 2017, 2018, 2021, 2022, 2023, 2024 e 2025. Respostas de 2015, 2017, 2018, 2021–2025 contêm descrições e valores de contas, sem paginação pendente. Para **2013**, o endpoint devolveu **zero linhas** para São Paulo: não presumir ausência na fonte anual original (os registros originais 2013 já estão no Drive).

## 2. Confirmação direta na API: evolução dos códigos

| Conceito | 2015/2017 | 2018/2021 | 2022/2023/2025 |
|---|---|---|---|
| FPM principal/cota mensal | `RO1.7.2.1.01.02.00`, título genérico FPM | `RO1.7.1.8.01.2.0`, **cota mensal** explícita | `RO1.7.1.1.51.1.0`, **cota mensal** explícita |
| ITR transferido | `RO1.7.2.1.01.05.00` | `RO1.7.1.8.01.5.0` | `RO1.7.1.1.52.0.0` |
| Fundeb recebido | `RO1.7.2.4.01.00.00` | `RO1.7.5.8.01.0.0` | `RO1.7.5.1.00.0.0` |

**Limitação:** descrições de conta extraídas para São Paulo são provas de uso/denominação no município e exercício, mas **não equivalem a aprovação universal de mesma composição contábil para os 645 municípios**. O título do Fundeb nos exercícios antigos pode reter terminologia obsoleta, que não substitui a verificação do regime legal vigente.

## 3. Reconciliação FPM: contas-pai e contas-filhas em São Paulo

Receitas brutas do Anexo I-C da API, município `3550308`, em reais:

| Ano | Conta-pai FPM `RO1.7.1.1.51.0.0` | Cota mensal `...51.1.0` | Extraordinárias `...51.2.0` | `...51.3.0` (julho quando existente) | Diferencial do pai em centavos |
|---|---:|---:|---:|---:|---:|
| **2022** | 541.154.611,32 | 499.039.881,84 | 21.735.214,84 | 20.379.514,64 | 0 |
| **2023** | 567.985.226,72 | 515.979.509,71 | 52.005.717,01 | — | 0 |
| **2024** | 661.555.496,68 | 599.650.417,75 | 61.905.078,93 | — | 0 |
| **2025** | 728.228.425,40 | 676.877.384,80 | 51.351.040,60 | — | 0 |

**Conclusão localizada, elevada confiança:** nos quatro exercícios, o FPM principal e as cotas extraordinárias reproduzem **exatamente** o total da conta-pai para este município. A representação mudou: em 2022 existem subcontas diferentes para julho e dezembro; nos anos 2023–2025 a conta `...51.2.0` é intitulada «cotas extraordinárias». A informação bruta **não deve somar pais e filhos**, e o código `...51.2.0` não significa apenas dezembro de 2023 em diante.

Em 2015 e 2017, a API de São Paulo mostra a conta `RO1.7.2.1.01.02.00` intitulada genericamente FPM, sem subcontas extras no retorno selecionado. As contas `17210103` e `17210104`, quando existentes em outras fontes, precisam de exame específico: **a equivalência de 2013–2017 com o FPM mensal é fortemente corroborada pelo padrão histórico, mas não homologada por ementário/de-para baixado e auditoria de valores municipais**. Em 2018/2021, o título de cota mensal está explícito e há contas separadas para cotas extras.

## 4. Rupturas do Fundeb — codificação versus comparabilidade substantiva

O **Novo Fundeb a partir de 2021**, documentado pelo FNDE, incorporou complementações da União com modalidades distintas. Os parâmetros nacionais divulgados pelo FNDE mostram VAAF/VAAT em 2021 e 2022 e VAAR a partir de 2023. Logo:

- A série `fundeb_distribuicao_bruta` pode seguir um conceito administrativo nominado «Fundeb recebido» entre regimes, mas **a base de redistribuição, financiamento e regras legais mudou em 2021**. Preservar `regime_legal` e não afirmar comparabilidade substantiva irrestrita.
- `fundeb_complementacao_uniao_bruta` **não deve ser interpretada como uma série homogênea** do antigo Fundeb até 2025: separar ao menos `pre_2021`, `2021_2022_vaaf_vaat`, `2023_2025_vaaf_vaat_vaar`. O número de municípios com conta preenchida **não é número confirmado de beneficiários por modalidade**.
- A presença de cinco municípios em 2022 no suplemento e 451 em 2025, isoladamente, é **sinal de variação de reporte/cobertura ou de política pública**, sem causalidade estabelecida. É preciso cruzar DCA com os registros oficiais de repasse do FNDE/STN para distinguir cobertura de transferências efetivas.
- Não adicionar `complementacao` à conta de distribuição ordinária sem demonstrar que são valores mutuamente exclusivos e sem sobreposição nos demonstrativos utilizados.

## 5. Saída para o crosswalk

Produzida [`FED04_MATRIZ_EVIDENCIAS_SEMANTICAS_2013_2025_2026_11_10.csv`](FED04_MATRIZ_EVIDENCIAS_SEMANTICAS_2013_2025_2026_11_10.csv) com **52 linhas** (quatro conceitos × 13 exercícios), cada uma com código, grau de comprovação na API, ressalva de equivalência e regime do Fundeb. Trata-se de **camada de QA adicional**, sem reescrever retroativamente o [crosswalk inicial](FED04_CROSSWALK_DCA_ITR_FUNDEB_2013_2025_CANDIDATO.csv) ou promover catálogos de produção.

**Gates aprovados nesta diligência:**
- identificação da mudança de regime contábil em 2018 e 2022 por cruzamento de fonte anual com API amostral;
- reconciliação exata da decomposição FPM São Paulo em **2022–2025 (4/4 exercícios; diferenças iguais a zero)**;
- confirmação documental da ruptura legal do Fundeb em **2021**, e expansão das modalidades de complementação em **2023**;
- registro explícito da lacuna da API de 2013, que não invalida a fonte histórica já preservada.

**Gates ainda abertos:**
1. baixar/ler em detalhe os ementários por exercício e o de-para STN para atualizar a equivalência contábil;
2. verificar o antigo FPM 2013–2017 em mais municípios e perante dados STN para evitar mistura de cotas;
3. validar se a linha «complementação União» DCA representa corretamente VAAF/VAAT/VAAR e reconciliá-la com os repasses oficiais por município e ano;
4. auditar valores históricos por amostragem e o esquema de ausências, inclusive 2013 sem retorno de API;
5. resolver a situação DCA de Sarutaiá e a anomalia do Anexo I-C de Rio das Pedras;
6. somente após esses pontos decidir sobre promoção de variáveis e aprovação de publicação FED08.

**Produção:** nenhuma alteração da base SQLite canônica, do R2, das séries existentes ou da publicação. O [PR #232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232) continua em rascunho; as regressões técnicas aprovadas não são homologação semântica.
