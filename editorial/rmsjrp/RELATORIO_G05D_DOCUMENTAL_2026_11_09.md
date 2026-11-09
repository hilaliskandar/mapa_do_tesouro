# RMSJRP — G05-D: confronto documental e revisão das interpretações do investimento
**Data:** 09/11/2026. **Situação:** primeira rodada documental executada; dez chaves contábeis prioritárias confrontadas com fontes oficiais. **QA documental parcial; não homologar identificação causal nem o encerramento integral do G05.** Dados de investimentos são nominais e liquidados, salvo indicação expressa em contrário.

## 1. Material examinado, proveniência e método
**Origem fiscal:** `rmsjrp/g05/2026_11_09/programas_acoes/G05B_TRANSICOES_PROGRAMA_ACAO_2023_2025.csv` no R2 privado, SHA-256 `02bbf839bf849fc374ee3dcb64aad8dc9695c6972cfaec2cff89ee741ccd5d31`. Foram efetivamente reexaminados os movimentos de 2024 para 2025 por chave exata de órgão, programa e ação, distinguindo lançamentos presentes de códigos ausentes. A verificação original dos 111 pares município–ano consta do [run G05-B 42562212589](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562212589).

**Fontes documentais:** páginas de contratos e comunicados das prefeituras, legislação orçamentária, PPA, parecer regulatório e portal de obras. Pesquisa de descoberta realizada em 09/11/2026. Tentativas de leitura pelo Crawl2AI conectado falharam por erro interno; a leitura documental foi feita por mecanismo alternativo de recuperação web. As fontes permanecem identificadas abaixo por URL, tipo e data. **Limite:** a extração textual de dois PDFs oficiais foi conferida; a visualização por screenshot desses PDFs retornou erro de cache, portanto não foi homologada conferência visual de suas páginas. Não declarar inspeção de todas as peças contratuais anexas.

**Arquivos produzidos:** [matriz de dez chaves](MATRIZ_EVIDENCIAS_G05D_2026_11_09.csv) e este relatório. A matriz tem três níveis de evidência: A = correspondência objetiva de código ou documentação direta da execução física contextual; B = documento oficial que corrobora tema, objeto ou instrumento, sem vinculação financeira projeto a projeto; C = hipótese ou correspondência ainda sem comprovação documental. Um nível A contextual **não** valida a causalidade da variação contábil.

## 2. São José do Rio Preto: infraestrutura urbana e SeMAE

### 2.1. Programa da Prefeitura 9 — Planejamento e Infraestrutura Urbana
Nos lançamentos TCESP referentes à Prefeitura Municipal, o programa 9 apresentou **R$ 180.693.872,93** liquidados em 2024 e **R$ 8.715.278,17** em 2025, **redução nominal de R$ 171.978.594,76**. As duas maiores ações dentro do programa, identificadas pela mesma chave órgão/programa/ação, são:
- Ação **1003 — Construção, Ampliação e Reforma em Áreas Públicas**: R$ 77.525.880,35 (2024) e R$ 5.108.068,35 (2025), diferença **−R$ 72.417.812,00**.
- Ação **1004 — Pavimentação Asfáltica e Recapeamento**: R$ 61.548.790,29 (2024) e R$ 946.501,52 (2025), diferença **−R$ 60.602.288,77**.

O PPA municipal 2022–2025 identifica essas categorias como ações planejadas; a peça legislativa corresponde a valores de planejamento, não à execução liquidada: https://legislacaodigital.com.br/SaoJoseDoRioPreto-SP/LeisOrdinarias/14041/pdf/2. A documentação do PPA 2026–2029 evidencia **nova codificação** do programa de infraestrutura, incluindo programa 0078 e ação de pavimentação 1064 (https://riopreto.siscam.com.br/arquivo?Id=642260). **Proibição metodológica:** a mudança de numeração no próximo ciclo não pode ser usada para interpretar a passagem 2024–2025 como encerramento de programa, nem comparada por código sem tabela de equivalência.

**Interpretação apta ao manuscrito:** a redução de investimento contabilizada na infraestrutura urbana da Prefeitura concentrou parte substancial da queda nominal municipal. **Não demonstrado:** quais contratos e obras específicas explicaram o movimento, a situação física de cada intervenção e a hipótese de vínculo causal com a LC 200/2023.

### 2.2. Programa do SeMAE 31 — Investimentos; ação 1029
O SeMAE liquidou no programa 31 **R$ 40.195.630,86** em 2024 e **R$ 27.108.093,10** em 2025, diferença nominal de **−R$ 13.087.537,76**. No seu interior, a ação 1029, Perfuração de Poços e Construção de Reservatórios, registrou **R$ 29.301.108,66** em 2024 e **R$ 10.010.482,90** em 2025, diferença de **−R$ 19.290.625,76**. A queda da ação pode ser superior à do programa porque outras ações registraram compensações.

**Corroboração independente de obras físicas:** Parecer Consolidado ARES-PCJ 34/2025, julho/2025, seção 3.4 e tabelas TEC 8–10, registra fiscalizações sobre investimentos do SeMAE, poço PTG11 em execução (37% na referência do parecer), reforma do PTG10 (82%), interceptor Córrego da Onça/Lagoa (48%), além de ações concluídas. O parecer identifica obras não previstas e separa empreendimentos previstos que não começaram. Fonte: https://www.arespcj.com.br/public/media/arquivos/1752499446-parecer_consolidado_-_34_2025_-_so_jos_do_rio_preto.pdf. O PPA também contém ação 1029 e previsão financeira, mas a edição-base foi originalmente produzida em 2021 e **não substitui a última LOA/PPA atualizada**.

**Conclusão delimitada:** o SeMAE apresentou menor volume de liquidação do grupo 44 em 2025, **sem interrupção generalizada das obras**, pois há documentação de execução física em curso no mesmo período. Não afirmar que os valores do parecer regulatório são subconjuntos coincidentes da ação 1029: falta o identificador do contrato/empenho e a reconciliação entre fontes.

## 3. Olímpia: concessão de saneamento, recursos extraordinários e mudança de classificação

A Prefeitura liquidou **R$ 46.671.064,76 em 2024** no programa 45 — Concessão Água e Esgoto. O programa **não possui lançamento em 2025 na mesma chave** (não converter célula não observada em despesa total nula). A ação 1002, Obras e Instalações, concentrou R$ 28.327.721,07 em 2024, igualmente sem registro em 2025 nessa classificação. Simultaneamente, o programa 31 — Projetos e Obras Públicas registrou R$ 4.011.361,63 em 2024 e **R$ 11.734.697,77 em 2025**, aumento nominal de **R$ 7.723.336,14**; isso não prova migração de projetos entre programas.

**Concessão confirmada:** contrato municipal nº **398/2023** com **Sabesp Olímpia S/A**, assinado em 11/10/2023, vigência até 10/10/2053, objeto de abastecimento de água e esgotamento sanitário, valor contratual divulgado de R$ 1.182.494.891,42. Fonte: https://www.olimpia.sp.gov.br/portal/contrato/4095. Segundo comunicado da Prefeitura de 11/12/2023, a Sabesp assumiu a operação e o DAEMO entrou em fase de transição/extinção: https://www.olimpia.sp.gov.br/portal/noticias/0/3/6543/servicos-de-agua-e-esgoto-comecam-a-ser-operados-pela-sabesp-em-olimpia. Fato relevante da Sabesp em 22/05/2023 informa **outorga fixa de R$ 148 milhões** (https://mzgroup.com.br/fatosrelevantes/fato-relevante-sabesp-vence-concorrencia-publica-do-municipio-de-olimpia/). Esse valor de outorga contratual **não é** o mesmo conceito da despesa de investimento liquidada de R$ 46,67 milhões.

**Cautela interpretativa prioritária:** a concessão e o ingresso extraordinário de recursos justificam examinar efeitos transitórios no orçamento e a destinação dos recursos, mas não há ainda vinculação demonstrada entre cada liquidação do programa 45 e a outorga. O portal municipal de obras fornece potencial evidência de projetos, início/fim, situação e valor para 2024 e 2025 (https://dadosabertos.olimpia.sp.gov.br/pt_BR/dataset/relacao-de-obras-publicas), porém os recursos anuais não foram extraídos e reconciliados projeto a projeto nesta rodada. **Portanto o programa 45 constitui explicação contábil concentradora; sua causa administrativa e financeira específica exige nova diligência.**

## 4. Monte Aprazível: pavimentação, créditos vinculados e base de comparação

O programa 14 — Infraestrutura de Serviços Urbanos liquidou **R$ 9.968.976,54** em 2024 e **R$ 406.282,00** em 2025, diferença nominal de **−R$ 9.562.694,54**. Sua ação 1010 — Pavimentação e Recapeamento Asfáltico registra **R$ 7.548.559,17** e **R$ 316.482,20**, respectivamente, redução de **R$ 7.232.076,97**.

**Comprovação normativa da rubrica e das fontes em 2024:**
- Lei municipal **3.978/2024** autorizou crédito especial de **R$ 400.000,00** no código `15.451.0014.1.010`, grupo 4.4.90.51, com **recursos estaduais** destinados ao recapeamento (Diário Oficial de 29/01/2024): https://www.dosp.com.br/leituratexto?p=MTU1NTIzNQ%3D%3D.
- Lei municipal **3.997/2024** autorizou **R$ 359.980,00**, mesma ação e natureza, com **transferência da União** para recapeamento (Diário Oficial de 18/04/2024): https://www.dosp.com.br/leituratexto?p=MTY1NTE2NA%3D%3D.
- Outros dispositivos de 2024 registram saldos vinculados e créditos para a mesma finalidade: https://dosp.com.br/exibe_do.php?i=NDUyMTgz.

**Limite de comparabilidade:** as autorizações são créditos orçamentários e não demonstram liquidação. As duas transferências de R$ 759.980,00 são apenas parte da estrutura de financiamento e não explicam diretamente a redução líquida de R$ 7,23 milhões da ação. Não se pode afirmar que o investimento menor de 2025 decorreu de corte federal ou estadual sem trajetória dos repasses, empenhos, contratos e medições.

## 5. Resultado comparativo e revisão das hipóteses
- A região apresentou queda real dos investimentos de 2024 a 2025 já demonstrada no G05-A. **Os movimentos G05-D são nominais por chave TCESP e NÃO devem ser somados aos totais reais regionais sem deflação e verificação de componentes.**
- **São José do Rio Preto:** menor liquidação em obras e infraestrutura urbana, com evidência independente de obras ainda executadas pelo SeMAE. Hipóteses em aberto: calendário financeiro das obras, concentração atípica em 2024, revisão de programas e cronograma.
- **Olímpia:** caso especialmente sensível a evento extraordinário de concessão e eventual recodificação/deslocamento de investimentos. A ausência do código 45 em 2025 não demonstra ausência de intervenções em água/esgoto nem causalidade fiscal federal.
- **Monte Aprazível:** aumento/uso de créditos vinculados a pavimentação em 2024 e menor liquidação em 2025. Seria indevida inferência de cancelamento de convênios a partir apenas da diferença por exercício.
- A documentação encontrada permite **qualificar a interpretação**, mas não validar que as quedas sejam um efeito identificável da **LC 200/2023**. A legislação do regime fiscal federal incide primariamente na União; impactos indiretos municipais exigem rastrear mecanismos específicos.

## 6. Cobertura documental e pendências observáveis
| Conjunto | Evidência comprovada | Pendente para conclusão |
|---|---|---|
| SJR Prefeitura programa 9, ações 1003/1004 | TCESP e classificação de obras no PPA | Identificar empenhos/contratos/obras específicas e execução física de 2024–2025 |
| SJR SeMAE programa 31, ação 1029 | TCESP + PPA e parecer regulatório com cronogramas e medições | Vincular contrato/medição/identificador contábil a cada obra e verificar recodificações |
| Olímpia programas 45 e 31 | TCESP + contrato de concessão e portal de obras | Vinculação da outorga, cronologia dos pagamentos, destinação orçamentária e correspondência projetos/códigos |
| Monte Aprazível programa 14, ação 1010 | TCESP + leis municipais de crédito vinculadas | Execução dos créditos, convênios, contratos, parcelas e medições |

## 7. Persistência e retomada
`MATRIZ_EVIDENCIAS_G05D_2026_11_09.csv` registra dez chaves com valores nominais, links primários e limitações. Próxima ação concreta: realizar os confrontos documentais faltantes **só para as chaves prioritárias**, começando pela despesa da concessão em Olímpia e por obras/códigos do programa 9 de São José do Rio Preto. Preservar todas as fontes e resultados, registrar novas provas no README, sem coleta estadual indiscriminada.

**Status de gate:** G05-A/B/C = QA técnico aprovado; G05-D = **em andamento, revisão documental parcial**, não `approved`; G06 = ainda não iniciado. O relatório ainda requer revisão de estilo e alegações antes da publicação editorial.
