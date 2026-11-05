# Lote 97 — Verificação fiscal e jurídica do Volume II e edição incremental

**Data:** 05/11/2026. **Status:** diligências jurídico-fiscais e revisão editorial executadas, nova cópia renderizada, **sem homologação final do Volume II**. Fonte de trabalho preservada: `RMRP_VOLUME_II_INTEGRACAO_FISCAL_LOTE96.docx` (64 páginas).

## 1. Conferência normativa em texto oficial atualizado

A leitura do texto atualizado da **Lei Complementar nº 227, de 13/01/2026** pela Câmara dos Deputados, via Crawl2AI, recuperou diretamente os arts. 109, 110, 112, 114, 115, 116 e 117: https://www2.camara.leg.br/legin/fed/leicom/2026/leicomplementar-227-13-janeiro-2026-798657-normaatualizada-pl.html . Também verificada como norma correlata a LC 214/2025 em https://www2.camara.leg.br/legin/fed/leicom/2025/leicomplementar-214-16-janeiro-2025-796905-normaatualizada-pl.html .

**Dispositivos diretamente conferidos:**

- **Art. 109, I:** de 2029 a 2032, **80%** do produto de arrecadação do IBS destinado a cada ente é retido para o mecanismo de redistribuição transitória; **art. 110, I:** retenção adicional de **5%** do saldo após a retenção do art. 109 de 2029 a 2077, vinculada à distribuição complementar nos termos do art. 117. Percentuais de retenção **não são alíquotas municipais nem prova de perda de receita**.
- **Art. 114:** distribuição da parcela retida proporcionalmente ao coeficiente, calculado pela receita média de referência do ente dividida pela receita média de referência do conjunto dos Estados, DF e Municípios; não há substituição simples de ISS por IBS.
- **Art. 115, III e § 6º:** para municípios, referência fundamentada na arrecadação do **ISS** e na **cota-parte de ICMS do art. 158, IV, a, da Constituição**, com critérios específicos de composição, inclusive Simples Nacional, multas e juros, dívida ativa quando cabíveis; **art. 115, § 2º:** valores anuais **2019–2026** corrigidos até 2026 conforme **variação nominal agregada da arrecadação tributária**; **não utilizar IPCA como substituto dessa correção legal**.
- **Art. 116, § 1º:** CGIBS deve publicar os coeficientes e valores componentes **até 31/08/2027**; **art. 116, § 2º:** uso de informação Siconfi; **§§ 3º–4º:** outras fontes e hipóteses de estimativa na ausência/inconsistência de dados, segundo critérios legais; **§ 7º:** contestação motivada no prazo de **30 dias** da publicação; **§ 8º:** prazo de resposta do Comitê Gestor segundo a norma.
- **Art. 112, § 7º:** possibilidade de apuração agregada e utilização de períodos mais curtos ou estimativas **excepcionalmente em 2027–2028**, não equivalendo à projeção individual disponível para cada município.
- **Art. 117:** mecanismo de distribuição complementar aos entes com maior perda de participação relativa, segundo critérios próprios, de 2029 a 2096.

**Encaminhamento jurídico:** construir dossiê por município com receita de ISS (incluindo componentes alcançados pela lei), cota-parte de ICMS creditada, fonte municipal/pagadora e dados Siconfi de 2019–2026; verificar os coeficientes efetivamente publicados em 2027 e eventuais contestações. **Não simular ganhos e perdas de IBS em 2027–2030 com a simples soma de ISS e ICMS da DCA, e não transpor o deflator IPCA usado nas receitas de capital para o cálculo jurídico da referência.**

## 2. Rechecagem direta dos demonstrativos fiscais em 05/11/2026

Consultados novamente, via Crawl2AI, os dados oficiais STN `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/` nos filtros pertinentes a cada tipo de RGF e RREO, com retorno numérico idêntico ao registrado nos Lotes 92–94:

| Município | Documento | Campo | Valor |
|---|---|---|---:|
| Pontal | RGF Anexo 06, 3º quadrimestre/2025 | RCL | R$ 13.494.039,69 |
| Pontal | RREO Anexo 03, 6º bimestre/2025 | RCL (últimos 12 meses) | R$ 209.571.785,24 |
| Pontal | RGF Anexo 06, 3º quadrimestre/2025 | DTP/RCL ajustada | 805,41% |
| Barrinha | RGF simplificado, Anexo 02, 2º semestre/2025 | DCL/RCL ajustada | 26,62% |
| Barrinha | RGF simplificado, Anexo 06, 2º semestre/2025 | DCL/RCL ajustada | 31,40% |
| Orlândia | RGF simplificado, Anexo 02, 2º semestre/2025 | DCL/RCL ajustada | -6,55% |
| Orlândia | RGF simplificado, Anexo 06, 2º semestre/2025 | DCL/RCL ajustada | -6,59% |

A diferença de RCL de Pontal entre RGF e RREO permanece **R$ 196.077.745,55**. Barrinha diverge **4,78 pontos percentuais** entre anexos e Orlândia **0,04 ponto percentual**. **Não se encontrou nessas respostas de API uma retificação que saneasse as divergências**, não sendo correto afirmar que nenhuma retificação exista em outra fonte ou declaração. **Os indicadores permanecem sob QA/quarentena** para qualquer conclusão de descumprimento de limite fiscal; preservar valores reportados, sem substituição automática.

Exemplos de URLs parametrizadas:
- https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2006&id_ente=3540200&co_poder=E
- https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo?an_exercicio=2025&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2003&id_ente=3540200
- https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=S&nr_periodo=2&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2002&id_ente=3505609&co_poder=E
- https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=S&nr_periodo=2&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2006&id_ente=3534302&co_poder=E

## 3. FNDE Guariba — tentativa de CSV oficial e limitação operacional

Persistem dados contratuais dos Lotes 88–90: Contrato 043/2025 R$ 8.576.160,36 (lote escola R$ 8.211.319,86, lote adequações R$ 364.840,50), ordem autorizativa de início de 12/09/2025, e Termo FNDE 959097/2024 com valores originais que não se confundem com desembolsos efetivos. **Desembolsos e pagamentos ainda não reconciliados em base federal oficial.**

Na presente rodada foram identificadas duas rotas documentais oficiais para download dos dados:
- novo catálogo https://api-publica.transferegov.gestao.gov.br/downloads (CSV em ZIP; consulta de 05/11 mostrou listagem de 65 arquivos, atualizados em 04/11/2026);
- catálogo histórico de 17/07/2026 no repositório https://repositorio.dados.gov.br/seges/detru/ , com arquivos `siconv_convenio.csv.zip` e `siconv_desembolso.csv.zip`.

**Teste técnico real:** solicitações HEAD via Python Requests às duas fontes em contêiner retornaram **erro de DNS (NameResolutionError)**. **Nenhum ZIP foi baixado ou conciliado nesta rodada**. Não inferir pagamentos do FNDE com base somente em valores orçamentários da obra, nem promover saldos de agregadores secundários a evidência homologada.

## 4. Edição incremental do Volume II

Foi produzida nova cópia de `RMRP_VOLUME_II_INTEGRACAO_FISCAL_LOTE96.docx`, denominada `RMRP_VOLUME_II_VERIFICACAO_JURIDICA_LOTE97.docx`, por edição localizada no segmento jurídico da Parte III, adjacente ao parágrafo sobre 2027–2030.

**Foram adicionados três parágrafos de análise substantiva**:
1. componentes da receita média de referência municipal, período 2019–2026 e critério legal específico de atualização;
2. competência do CGIBS, divulgação dos coeficientes até 31/08/2027, contestação em 30 dias e necessidade de dossiê municipal documentado;
3. retenção redistributiva em 2029–2032 e complemento, sem confundir percentuais legais com projeções de impacto fiscal.

A redação anterior foi preservada, sem exclusão de seções, de figuras ou de matrizes SWOT. Rodapés identificados como **Lote 97**. **Não houve atualização dos cálculos fiscais, mudança de cenário, substituição de valores nem alegação de homologação.**

## 5. Renderização e inspeção

- Novo DOCX: `/mnt/data/RMRP_VOLUME_II_VERIFICACAO_JURIDICA_LOTE97.docx`, aproximadamente 2,4 MB;
- PDF renderizado: `/mnt/data/RMRP_LOTE97_RENDER/RMRP_VOLUME_II_VERIFICACAO_JURIDICA_LOTE97.pdf`;
- Script: `/mnt/data/revisar_lote97.py`;
- **65 páginas**, contra 64 do Lote 96;
- **65/65 páginas com conteúdo textual**;
- **nenhum bloco de texto fora dos limites das páginas**, conforme análise geométrica com PyMuPDF;
- Documento conserva **45 tabelas** e elementos gráficos anteriores; contagem de imagens no PDF mudou de 896 ocorrências de imagem no Lote 96 para 910 na nova paginação, diferença relacionada à repetição de elementos gráficos no layout. A contagem de ocorrências em PDF não equivale ao número de mapas;
- **Páginas 56 e 57 verificadas visualmente**, inserção jurídica íntegra, sem sobreposição ou truncamento; o último parágrafo continua na página seguinte por fluxo natural de texto. **Não foi reexecutada inspeção manual ampliada de todas as 65 páginas** nesta rodada, mas houve controle automático global e inspeção das páginas alteradas.

**Persistência:** este dossiê, ao contrário dos binários, é arquivado no GitHub; os DOCX/PDF permanecem acessíveis como arquivos gerados na conversa, sem confirmação de envio ao Drive.

## 6. Pendências antes de homologação

- Esclarecimento documental e possíveis retificações RGF/RREO de Pontal, Barrinha e Orlândia, com manifestação dos órgãos responsáveis quando apropriado.
- Revisão jurídica ampla da LC 214/2025 e LC 227/2026, inclusive atos infralegais, para não confundir leitura dirigida dos arts. 109–117 com exame exaustivo da transição.
- Consolidação auditada de ISS/ICMS 2019–2026 por município, com as definições específicas do art. 115; exercício 2026 ainda em curso na data da diligência.
- Conciliação bancária e contábil das transferências FNDE Guariba 959097/2024 e do crédito especial do terreno.
- Cinco casos DCA sem conta sintética de receita de capital, mantidos NA e documentados nos Lotes 94/95.
- Inspeção final de 65 páginas, mapa 15, fontes, referências e qualidade visual; revisão para público externo e homologação.

**Resultado:** atualização jurídico-editorial verificável e rechecagem de três exceções fiscais; **Volume II permanece em pré-homologação**, com versão do Lote 96 preservada.
