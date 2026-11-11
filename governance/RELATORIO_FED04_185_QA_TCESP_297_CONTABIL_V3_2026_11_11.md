# FED04 — Auditoria analítica municipal dos 185 casos ETI e matriz contábil v3, 297/297

**Data:** 11/11/2026. **Gates:** todas as 297 contas DCA 2025 no estrato anteriormente "somente DCA VAAT/VAAR" possuem equivalência contábil municipal documental; **isso não significa que pagamentos FNDE tenham sido verificados nem que a série histórica esteja homologada**.

## 1. Procedimento e fontes

Partiu-se da [matriz v2 de 297 casos](FED04_297_CONCILIACAO_CONSOLIDADA_V2_2026_11_11.csv), selecionando exatamente os **185 municípios** cuja equivalência anterior era exclusivamente `DCA = soma dos valores mensais ETI previstos na Portaria MEC 823/2025`, sem conferência analítica municipal.

Os arquivos **Receita Detalhada 2025** de cada município foram recuperados da [plataforma oficial TCESP](https://transparencia.tce.sp.gov.br/), URLs `https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-{slug}-2025.zip`. O ZIP foi descompactado dentro de sessão Browserless por leitura do diretório central (`DataView`) e fluxo `DecompressionStream('deflate-raw')`, com CSV `windows-1252`. Filtraram-se contas de natureza `1715xxxx`, mantendo os lançamentos positivos e negativos separados. Cada município foi testado por comparação exata em centavos contra **(a) soma dos lançamentos positivos**, ou, se não igual, **(b) soma líquida após deduções**.

A normalização automática de slugs falhou em três nomes: **Santa Bárbara d'Oeste, Aparecida d'Oeste e São João do Pau d'Alho**. Os endereços oficiais conservam `d-oeste`/`d-alho`; os três arquivos foram recuperados mediante pesquisa do link na página de cada município no TCESP e repetição do teste. O histórico de erros de URL não deve ser confundido com arquivo inexistente.

**Controle de origem:** TCESP publica **declarações feitas pelo próprio município**. A correspondência entre a DCA e a publicação estadual de receitas analíticas aumenta a rastreabilidade e permite localizar natureza, mês e valores; não se trata de auditoria de banco nem evidência externa do efetivo desembolso federal.

## 2. Resultado para os 185

| Critério de comparação com a DCA 2025 | Municípios |
|---|---:|
| DCA igual ao **bruto** da conta `1715` no TCESP | **178** |
| DCA igual ao **líquido** da conta `1715` no TCESP | **7** |
| Valores sem equivalência monetária | **0** |
| ZIP municipal definitivamente indisponível | **0** |
| **Total de municípios** | **185** |

O total de receitas DCA desse grupo é **R$65.087.745,47**. Todos já apresentavam identidade com o cronograma oficial ETI da Portaria MEC 823/2025, e agora também têm confirmação de escrituração municipal em fonte contábil analítica por natureza de receita. **A diferença agregada de comparação na base adequada (bruta ou líquida) é R$0,00**. Os 185 códigos são únicos; nenhum caso foi descartado por falha de slug.

Artefatos analíticos do lote:
- [70 maiores, resumo](FED04_ETI_70_PRIORITARIOS_TCESP_RESUMO_2026_11_11.csv) e [lançamentos](FED04_ETI_70_PRIORITARIOS_TCESP_LANCAMENTOS_2026_11_11.csv). O resumo bruto do lote preserva o erro inicial de URL para Santa Bárbara d'Oeste; a matriz v3 utiliza o arquivo já recuperado no lote de 116.
- [115 restantes e repetição Santa Bárbara d'Oeste](FED04_ETI_115_RESTANTES_E_SBO_TCESP_RESUMO_2026_11_11.csv) e [lançamentos](FED04_ETI_115_RESTANTES_E_SBO_TCESP_LANCAMENTOS_2026_11_11.csv). O resumo bruto preserva erros iniciais de `slug` para Aparecida d'Oeste e São João do Pau d'Alho.
- [Recuperação manual dos dois slugs restantes](FED04_ETI_2_SLUGS_APOSTROFO_TCESP_2026_11_11.csv).
- [Matriz consolidada v3](FED04_297_CONCILIACAO_CONTABIL_MUNICIPAL_V3_2026_11_11.csv): substitui **somente a situação e o suporte documental** dos 185 casos; preserva DCA monetária, IBGE7, histórico v1/v2 e demais 112 casos.

## 3. Balanço atualizado do conjunto 297

| Classe documental | Municípios |
|---|---:|
| DCA = TCESP bruto **e** cronograma ETI MEC 823 | **178** |
| DCA = TCESP líquido **e** cronograma ETI MEC 823 | **7** |
| DCA reconciliada com receita TCESP, outros 109 casos | **109** |
| Piracicaba: TCESP VAAR + portal municipal ETI + deduções SICONFI | **1** |
| Teodoro Sampaio: TCESP lançamento a lançamento + deduções da DCA original | **1** |
| São Paulo: IRIS/TCM-SP VAAR+ETI, com dedução separada | **1** |
| **Total de municípios com equivalência contábil municipal documentada** | **297** |

**R$265.487.655,96 de DCA 2025** nesse recorte possuem suporte monetário em fonte analítica municipal. Nos 185, a correspondência também é exata com o cronograma de fomento ETI. Os outros 112 contêm modalidades ou competências adicionais e foram conciliados em documentos anteriores.

Os valores da DCA de alguns municípios correspondem a **receita bruta**, enquanto outros correspondem à **líquida**. Essa diferença de reporte precisa ser auditada por **coluna DCA, natureza, estornos e demais deduções**, evitando agregação homogênea incorreta. O caso de Teodoro Sampaio mostrou uma estrutura em que um estorno já estava absorvido na bruta declarada e outra dedução aparecia em coluna própria: não subtrair lançamentos duas vezes.

## 4. Gates e pendências seguintes

**Concluído para o recorte SP297:** comparação documental contábil de 2025 em 297/297, diferença monetária zero quando se seleciona explicitamente a base comparável; a evidência contábil provém de fonte publicada pelos municípios, pelo TCESP ou pelo TCM-SP.

**Não concluído:**
1. Comprovação das **transferências bancárias efetivas do FNDE**, segregadas por município, competência e modalidade.
2. Homologação de semântica **VAAR, VAAF, VAAT, ETI**, inclusive divergência entre código `17155201` e variável de aplicação rotulada como VAAF, e fontes 02/05.
3. Reconciliação estadual **SP645**, contemplando as outras categorias de municípios que não integraram esse estrato de 297.
4. Série **2013–2025**, sobreposição de agregações e quebras estruturais, além de demais gates FED00–FED08.

**Restrições preservadas:** FED04 `in_progress`, PR #232 `draft`, variáveis candidatas não publicáveis, sem migração, merge, deploy ou alteração de D1, R2 e SQLite produtivos.

## 5. Reprodutibilidade e alertas

- Manter sempre os dois estados separadamente: `conciliacao_contabil` e `liberacao_federal`.
- Persistir URL do CSV ZIP exato e identificadores dos lançamentos contábeis; os resultados por município estão nos arquivos de lançamentos.
- Na base do TCESP, o CSV normalmente separa campos por `;`, utiliza valores em formato monetário brasileiro e codificação Windows-1252; toda soma deve ser em centavos inteiros, não em float sem arredondamento monetário.
- **Não inferir zero** em município sem linha ou arquivo; registrar `ausente`, `erro_http`, `indisponivel` e `nao_verificado` distintamente.
- Não substituir as matrizes v1 e v2; o [v3](FED04_297_CONCILIACAO_CONTABIL_MUNICIPAL_V3_2026_11_11.csv) é a versão canônica **apenas da auditoria exploratória** deste estrato e não autoriza publicação dos indicadores fiscais.
