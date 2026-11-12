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
