# INV-RMRP — Expansão do cruzamento de convênios estaduais para os 34 municípios

**Data da atualização:** 12/11/2026. **Branch:** `investimentos-territoriais-sp645-20261111`, PR #233 (draft). **Natureza:** inventário territorial e priorização de provas; **não** se trata de cruzamento completo homologado entre convênios públicos e IDs SIAFEM.

## 1. Universo recuperado e auditoria

O arquivo canônico `governance/INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv` contém **752 instrumentos únicos** de transferências voluntárias estaduais classificadas como investimento para prefeituras dos **34 municípios da RMRP**, dos quais **747** possuem objeto, órgão concedente e situação recuperados nas páginas oficiais individuais; **cinco** fichas permaneceram com exceção técnica, sem preenchimento inferido.

O arquivo `governance/INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv` contém **889** registros instrumento–ano (2020–2026), **1.017** pagamentos contabilizados pela fonte e **R$ 305.521.029,20** em valores liberados/estornados com centavos. São valores de fluxo estadual, não despesas municipais liquidadas ou custos de obras.

O novo `governance/INV_RMRP_SIAFEM_CROSSWALK_COBERTURA_34_MUNICIPIOS_2026_11_12.json` cruza territorialmente os dois arquivos, reproduz números, identifica exceções e ordena municípios por valor financeiro observado, **sem acrescentar nenhum lançamento**. O script `pipeline/qa/qa_inv_rmrp_crosswalk_cobertura_34.py` verifica as 752 chaves únicas, 889 pares instrumento–ano, 34 municípios, 747 leituras positivas, cinco falhas explícitas e conciliação de valores, além dos dois estudos de caso de Serrana. [Workflow de QA 43260585846](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43260585846): **success**.

## 2. Priorização inicial de municípios

| Município | Instrumentos SIAFEM | Liberações/estornos 2020–2026 |
|---|---:|---:|
| Ribeirão Preto | 41 | R$ 30.967.747,17 |
| Pradópolis | 32 | R$ 20.063.468,96 |
| Santa Rita do Passa Quatro | 31 | R$ 18.303.139,81 |
| Batatais | 27 | R$ 16.972.500,88 |
| Sertãozinho | 39 | R$ 16.865.491,90 |
| Cravinhos | 22 | R$ 15.906.237,97 |
| Serrana | 35 | R$ 14.997.041,10 |

A prioridade indica **onde começar a buscar documentos e testar relações**; a ordenação não é índice de carência, de prioridade de política pública nem de execução física.

## 3. Procedimento de correspondência entre identificadores

A evidência documental já recuperada em Serrana estabelece dois casos metodologicamente distintos:

- **101375/2024** (convênio público, Contrato municipal 126/2024) ↔ **51010120240581081** (ficha SIAFEM): **alta confiança documental composta**, pois coincidem **data da celebração, concedente, beneficiário/CNPJ, valor de R$ 300.000,00, contrapartida de R$ 3.501,56 e objeto**. Liberação SIAFEM de R$ 258.624,91 em 10/01/2025 e valor igual ao contrato municipal. **Ainda não foi recuperado documento com ambos os números simultaneamente**; não classificar como correspondência por chave literal.
- **100540/2024** (convênio público, Contrato municipal 078/2024, Demanda 062650) ↔ **51010120240419991** (ficha SIAFEM): **candidato forte**, mesmo beneficiário, objeto e órgão estadual; **duas liberações**, R$ 474.977,26 em 23/08/2024 e R$ 203.978,45 em 30/04/2025, total R$ 678.955,71, igual ao contrato municipal. **Não recuperado o termo integral 100540 ou documento com os dois identificadores**. Valor inicial da dotação/estimativa licitatória publicado em 2024, R$ 949.954,53, **não deve ser substituído pelo valor contratado**: são categorias e momentos distintos.

O arquivo `governance/INV_RMRP_SERRANA_CROSSWALK_100540_101375_SIAFEM_510101_2026_11_12.json` preserva os critérios, as fontes, os valores e o estado de cada hipótese. Há **zero relações numéricas literais homologadas**, **uma correspondência composta de alta confiança** e **um candidato forte**. Os demais 750 instrumentos não têm dossiê de crosswalk individual homologado no trabalho até esta data; **isso não demonstra inexistência de contrato ou convênio externo**.

## 4. Localização da possível chave administrativa oficial

A documentação institucional de São Paulo demonstra integração entre sistemas de gestão e contabilidade, sem oferecer diretamente uma tabela pública completa de equivalência:

- Portal SP Sem Papel: https://www.spsempapel.sp.gov.br/ — os módulos de Demandas e Emendas organizam convênios e transferências.
- Manual oficial **Código Único**: https://treinamentos.spsempapel.sp.gov.br/midiateca_adm/assets/ec104b11-a345-4767-a11f-dc939f3e1f92 — explica como pesquisar processos no Contabiliza/SP (SIAFEM) a partir do **Código Único**, com campos `Cód. Único`, `Número Processo` e `Número Sem Papel`. **Não está demonstrado que o número longo do campo Convenio da ficha pública SIAFEM seja o próprio Código Único de processo.**
- Documentação de integração SP Sem Papel/SIAFEM: https://www.al.sp.gov.br/repositorio/ementario/anexos/5858af9e-2ff3-48d4-98db-afbc1f01388b.pdf — relata a interoperabilidade de convênios pelo módulo Demandas e as evoluções de integração contábil.

**Rota para prova de identidade:** procurar nos documentos e sistemas oficiais campo comum que atravesse `número público do termo`, `Demanda/Processo Sem Papel`, `Código Único` e `identificador SIAFEM`; registrar literalmente número, data, órgão e URL da evidência. Não forçar equivalência entre diferentes espécies de identificadores.

**Limitação de recuperação:** Crawl2AI retornou erro interno em URLs testadas nesta rodada; fontes oficiais complementares foram verificadas por pesquisa web e, nas etapas anteriores, navegador Browserless. Isso não altera a integridade dos snapshots do SIAFEM já versionados, mas impõe cautela na interpretação de documentos ainda não capturados integralmente.

## 5. Próximos passos técnicos

1. Montar coletor incremental de **contratos e termos municipais por IBGE7**, separado da base SIAFEM: número público, processo, demanda, código único se existir, contrato, objeto, órgão concedente, valor previsto/contratado, data, URL, hash e estado de leitura. Iniciar pelos municípios de maior volume, **sem descartar os demais**.
2. Testar matching determinístico por ID oficial compartilhado, mantendo **status de hipótese** quando houver somente convergência de município, objeto, período e valores. A hipótese deve ser refutável e a pontuação de similaridade jamais promover vínculo automaticamente.
3. Vincular contratos a obras, trechos e projetos somente por documentação específica; considerar endereço/local físico, não apenas sede da prefeitura ou ponto aproximado do Obrasgov.
4. Preservar os dados de 2020–2026 do SIAFEM, não incorporar os R$ 937.580,62 dos dois casos ao total de R$ 305.521.029,20 já computado. A quantia de R$ 937.580,62 **é um subtotal contido na série**.
5. Manter PR #233 draft, FED04/PR #232 sem alterações e produção R2/D1/SQLite intocada.

**Conclusão:** a capacidade de seleção e auditoria está preparada para os 34 municípios. A pesquisa individual de contratos públicos e a obtenção de chaves administrativas faltantes permanecem etapas abertas. O QA confirma **cobertura e não aditividade**, não homologação de 752 correspondências.

## 6. Caso de controle negativo fora de Serrana — Pradópolis

A investigação avançou do piloto de Serrana para Pradópolis, segundo maior volume de liberações SIAFEM no inventário da RMRP. Identificou-se **Convênio público nº 100556/2024**, Processo **SGRI-PRC-2024-00085-DM**, celebrado em **12/04/2024** pela Secretaria de Governo e Relações Institucionais e pelo Município de Pradópolis, com objeto de **pavimentação asfáltica e sinalização viária na Rua Eureste Barbeta e Rua Abundio Del Campo Monsalve, no Distrito Industrial**, com compromisso estadual previsto **até R$ 997.533,27**. Fonte primária: Diário Oficial do Estado de São Paulo, **22/04/2024**, Caderno Executivo Seção I, vol. 134, nº 76, p. **182/242**, [PDF oficial](https://do-api-publication-pdf.doe.sp.gov.br/v1/editions/8920e39b-38e0-4e50-a304-9569c61b6b02).

Foi examinada a ficha [SIAFEM nº 51010120240425077](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=51010120240425077). Embora **também indique celebração em 12/04/2024**, órgão concedente SGRI, Prefeitura de Pradópolis e objeto genérico de pavimentação, apresenta **valor de convênio de R$ 498.766,64**, liberação acumulada **R$ 495.000,00**, saldo **R$ 3.766,64** e data de publicação cadastral **13/04/2024**. A diferença para o valor estadual previsto no convênio público é de **R$ 498.766,63**. A semelhança com aproximadamente metade do valor original **não comprova divisão do instrumento em dois lançamentos ou parcelas**. A descrição SIAFEM não nomeia as duas ruas do Distrito Industrial. Quatro outras fichas SGRI da Prefeitura de Pradópolis também foram inspecionadas, sem chave literal de reconciliação com `100556/2024`.

**Decisão:** `CANDIDATO_DATA_OBJETO_COM_VALOR_DIVERGENTE_SEM_CROSSWALK`. Não homologar por data e semelhança de objeto. Não atribuir ao termo 100556 o valor de R$ 495 mil liberado pela ficha interna nem somar o valor pactuado ao fluxo financeiro SIAFEM já consolidado. Registrar o caso como **controle negativo** no QA, para impedir que o método produza falsos vínculos ao ser aplicado a 34 municípios.

Arquivo de evidência: `governance/INV_RMRP_PRADOPOLIS_100556_2024_SIAFEM_DIVERGENCIA_2026_11_12.json`. O script `pipeline/qa/qa_inv_rmrp_crosswalk_cobertura_34.py` foi ampliado para exigir correspondência do beneficiário, **distinguir convergência de data de equivalência documental**, e testar a divergência exata de centavos. A fonte estadual de abril de 2024 e a ficha consultada em novembro de 2026 têm temporalidades diferentes: não se presumiu ausência ou irregularidade de execução.

**Encaminhamento:** localizar o termo original integral 100556/2024 e eventual aditamento, a Demanda/Processo SGRI-PRC-2024-00085-DM e a ficha de Código Único do SP Sem Papel/Contabiliza; só então avaliar se o ID interno do SIAFEM corresponde ao convênio público.


## 7. Segundo caso de correspondência composta — Ribeirão Preto, praça do Complexo Ribeirão Verde

A ampliação da pesquisa ao município de maior valor agregado SIAFEM no piloto, **Ribeirão Preto**, identificou o **Convênio público 101849/2023**, Processo **SGRI-PRC-2023-00461-DM**, cujo objeto é **construção de praça no Complexo Ribeirão Verde**. O Diário Oficial estadual de **17/07/2023**, Volume 133, nº 34, caderno Executivo Seção I, página 1, publica previsão de **R$ 400.000,00 de responsabilidade do Estado**, data de assinatura **14/07/2023**: [PDF oficial certificado](https://www.imprensaoficial.com.br/Certificacao/GatewayCertificaPDF.aspx?notarizacaoID=a39072cf-8827-4b26-bc65-f393bd00e5f3).

A **Lei Municipal nº 14.909, de 27/02/2024**, reproduzida no Diário Oficial de Ribeirão Preto nº 11.860, 01/03/2024, autoriza crédito especial para o **mesmo Convênio 101849/2023 e a mesma praça**, com **R$ 400.000,00 estaduais + R$ 410.612,92 municipais = R$ 810.612,92**. A reprodução pesquisada foi https://pt.scribd.com/document/721868543/Diario-Oficial-2024-03-01; **a recaptura da edição no portal oficial municipal ainda está pendente**. Esse registro representa autorização orçamentária municipal, não desembolso ao construtor nem obra concluída.

A [ficha SIAFEM nº 51010120231186228](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=51010120231186228), consultada diretamente, confirma **órgão concedente SGRI, beneficiário Prefeitura Municipal de Ribeirão Preto, objeto genérico de praça, valor estadual de R$ 400.000,00, contrapartida municipal de R$ 410.612,92 e valor total de R$ 810.612,92**, além de liberação total **R$ 400.000,00 em 12/12/2025**. Essa liberação já integra os R$ 305.521.029,20 da série SIAFEM: **não somar novamente**.

**Divergência temporal que impede homologação por chave inequívoca:** o extrato DOE informa assinatura **14/07/2023**, enquanto a ficha SIAFEM indica celebração **12/07/2023** e publicação em 13/07/2023. A diferença de dois dias foi preservada, sem presumir se decorre de erro material ou de etapas distintas de registro. Também não há documento que traga os números **101849/2023** e **51010120231186228** simultaneamente. A classificação apropriada é **`CORRESPONDENCIA_COMPOSTA_ALTA_CONFIANCA_COM_DIVERGENCIA_DATA_2_DIAS_SEM_CHAVE_LITERAL`**, e não vínculo determinístico homologado.

O caso foi documentado em `governance/INV_RMRP_RIBEIRAO_PRETO_101849_2023_SIAFEM_51010120231186228_2026_11_12.json`, com URLs e estados de confirmação. O QA `pipeline/qa/qa_inv_rmrp_crosswalk_cobertura_34.py` exige os três valores exatamente iguais nos documentos estadual, municipal e SIAFEM, preserva a divergência de data e proíbe a homologação literal indevida.

**Balanço da frente de crosswalk dos 34 municípios:** agora há **duas correspondências documentais compostas de alta confiança** (Serrana 101375 e Ribeirão Preto 101849), **um candidato forte** (Serrana 100540) e **um caso de controle negativo** (Pradópolis 100556). **Zero vínculos identificados por chave pública/interna literal publicada**. Os demais 748 instrumentos SIAFEM ainda não foram confrontados individualmente em dossiês de crosswalk, o que não implica que não possuam contratos ou projetos executados. Não há novos valores nem atualizações dos totais SIAFEM.
