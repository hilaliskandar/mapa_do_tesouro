# RMSJRP — G05-D | Contratos municipais de Olímpia e três vinculações candidatas
**Data de execução: 09/11/2026.** **Estado:** recuperação e QA do cadastro contratual **aprovados**; três correspondências entre ficha oficial de licitação e cadastro de contratos **confirmadas por número/processo/fornecedor/valor**, com presença dos mesmos títulos no cadastro de obras. **G05-D permanece em andamento**: não houve vínculo documental com a liquidação da despesa, nem identificação causal do programa 45.

## 1. Obtenção e QA dos arquivos
O portal CKAN [Contratos](https://dadosabertos.olimpia.sp.gov.br/dataset/contratos) anuncia recursos JSON e CSV, porém as URLs de download e a API datastore consultadas pelo runner GitHub em 09/11/2026 responderam **HTTP 404**, nas execuções [42566701035](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42566701035) e [42566809945](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42566809945). Isso não foi interpretado como ausência do conjunto de contratos.

Foi utilizada fonte alternativa **do próprio portal municipal**, os endpoints:
- `https://www.olimpia.sp.gov.br/portal/dados-abertos/contratos/2024`
- `https://www.olimpia.sp.gov.br/portal/dados-abertos/contratos/2025`

O script `editorial/rmsjrp/auditar_contratos_olimpia_g05d.py` e o workflow `.github/workflows/rmsjrp-g05d-contratos-olimpia.yml` recuperaram ambos, preservaram os JSON de origem, o CSV normalizado e relatório de QA com **leitura de retorno e SHA-256 no R2 privado**: [run 42566965367](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42566965367) `success`. A versão anterior [42566899631](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42566899631) já havia obtido os dados e confirmado os hashes; o último run acrescentou controle de sobreposição.

Localização dos objetos no bucket `financas-municipais-sp-canonico`: `rmsjrp/g05d/2026_11_09/olimpia_contratos/`:
- `CONTRATOS_OLIMPIA_2024_RAW.json`: SHA `bf4242d7b442db659effbb6824ee98356b9ce869c20fc83ddadf5fef4e8b9d2e`.
- `CONTRATOS_OLIMPIA_2025_RAW.json`: SHA `3a8397df2218ffcd9ccf76cc48c9e690d62fceeba917737f4b1c571ae43277b7`.
- `CONTRATOS_OLIMPIA_2024_2025_INVENTARIO.csv`: 2.512 linhas, SHA `e62c12c555843d8a3600b223096921cfe6e742987d1c9b0a65fd2ea1e6eb0b8f`.
- `QA_G05D_CONTRATOS_OLIMPIA.json`: SHA `c9381cbb9a0d95f4aeda08e6c52114b5a0ac00d8f6feb34d8908154005d3c767`.

### Cobertura e identidade
| Controle | Resultado |
|---|---:|
| Registros no endpoint 2024 | 1.396 |
| Registros no endpoint 2025 | 1.116 |
| Linhas recuperadas somando endpoints | **2.512** |
| Chaves compostas coincidentes entre endpoints | **543** |
| Chaves compostas distintas na união (ano de assinatura, número, processo, contratada) | **1.958** |
| Registros totais com assinatura em 2024 nas listagens (incluindo repetições) | 1.270 |
| Registros totais com assinatura em 2025 nas listagens (incluindo repetições) | 534 |

**Cautela cardinal:** 2.512 não significa 2.512 contratos individuais. As 543 sobreposições entre endpoints coexistem com repetições internas de chaves. As 1.958 chaves compostas **não são um número homologado de contratos jurídicos únicos** sem controle de aditivos, registros complementares e identidade do ente contratante. O endpoint também contém assinaturas de 2019–2026. Não somar valores das listagens nem interpretá-las como despesa anual.

Os **11 campos observados** são `nomeContratada`, `dataAssinatura`, `dataInicioVigencia`, `dataFimVigencia`, `dataVigencia`, `valorContrato`, `numeroContrato`, `numeroProcesso`, `tipoLicitacao`, `situacao`, `tipo`. **Não há objeto contratual, número de empenho, medição, programa, ação ou natureza da despesa no JSON**, logo não se pode relacionar diretamente título de obra e classificação TCESP por meio apenas desse dataset.

## 2. Três vínculos documentais estabelecidos
Os objetos de obra foram identificados nas respectivas fichas oficiais de licitação, e os dados dos contratos foram confrontados com o JSON recuperado no R2:

| Obra listada | Nº do contrato | Processo | Empresa | Valor de contrato |
|---|---|---|---|---:|
| Implantação de Anel Viário no Jardim Alvorada | **558/2023** | 136344/2023 | B.G. Borges Morando Construtora Ltda | R$ 3.320.489,98 |
| Recapeamento asfáltico com CBUQ | **189/2024** | 137300/2023 | B.G. Borges Morando Construtora Ltda | R$ 4.962.843,85 |
| Duplicação da Via João Custódio Sobrinho, fase 01 | **115/2024** | 140113/2023 | Base Infraestrutura e Serviços Ltda | R$ 5.694.859,16 |

**Fontes oficiais primárias:**
- Anel viário: https://www.olimpia.sp.gov.br/portal/editais/0/1/3878/ (concorrência 14/2023).
- Recapeamento CBUQ: https://www.olimpia.sp.gov.br/portal/editais/0/1/3927/ (concorrência 17/2023; aditivos cadastrados em 2025).
- Via João Custódio: https://www.olimpia.sp.gov.br/portal/editais/0/1/3999/ (concorrência 23/2023; aditivo de 26/11/2024, acréscimo R$ 696.890,47 e supressão R$ 114.336,90, declarados na ficha). Estes valores são **alterações contratuais**, não liquidações.

A matriz de referência é `editorial/rmsjrp/G05D_OBRAS_CONTRATOS_CANDIDATOS_2026_11_09.csv`. Foi criada a rotina `editorial/rmsjrp/qa_g05d_vinculos_contratos_obras.py` para checar contra os dois snapshots do R2; [run 42567153224](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42567153224) `success`. Para **três de três** candidatos: número/ano do contrato, processo, fornecedor normalizado e valor em duas casas coincidiram com registro do cadastro oficial. Os títulos das três obras aparecem em ambos os endpoints de obras (dois registros por título), com **um conjunto de chaves contratuais distinto por candidato** nos snapshots de contratos; contagens de dois ou quatro registros nos endpoints não são novos contratos. O resultado de QA está no R2 privado `rmsjrp/g05d/2026_11_09/olimpia_vinculos/`:
- `QA_G05D_VINCULOS_CONTRATOS_OBRAS.csv` SHA `b7ee857413162b65582e4cfd83fc1838fb3637d0b664e555d75f8b288a03bfdf`;
- `QA_G05D_VINCULOS.json` SHA `2f83fa3a4699e5e57240d0be7d17bd2578101f225248a3d746ce21c38aee1bea`.

**Interpretação do QA:** a ficha de licitação identifica concretamente o objeto e o contrato, e o contrato é recuperável no cadastro JSON municipal. O título semelhante do inventário de obras indica **candidato robusto**, mas o cadastro de obras não publica contrato/processo, por isso a identificação 1:1 da mesma unidade física exige peça complementar. **Ainda não existe ligação documental com notas de empenho, medições ou liquidação TCESP**. Não vincular automaticamente os três valores aos programas 45/31 ou somá-los à série fiscal.

## 3. Implicações para o diagnóstico fiscal
- A existência de contratos e aditivos em 2024–2025 é incompatível com a inferência automática de que ausência de um código contábil em 2025 implica inexistência de obras.
- As informações permitem preparar a investigação de obras específicas, mas **não permitem concluir que as três obras expliquem os R$ 46,67 milhões liquidados em 2024 no programa 45 da concessão de saneamento**. As três têm objetos urbanísticos/viários e não foram vinculadas ao programa de concessão. É indevido usá-las para justificar a queda do programa.
- O programa 31 — Projetos e Obras Públicas — permanece sem associação comprovada aos três contratos; confirmar ação/órgão/nota de empenho antes de atribuir a eles valores fiscais.
- Não foi demonstrado nexo causal da LC 200/2023. Os mecanismos indiretos da regra fiscal federal permanecem hipótese a ser testada com dados de transferências e execução de convênios.

## 4. Próxima ação reproduzível e mudança de chat
1. Pesquisar as fichas de contrato e documentação de empenhos/medições dos três processos 136344/2023, 137300/2023 e 140113/2023; verificar o objeto de cada despesa e identificar a ação orçamentária, sem correspondência por similaridade textual isolada.
2. Prosseguir nos contratos de Monte Aprazível 08/2024 (recapeamento) e na ação de infraestrutura de São José do Rio Preto 1003/1004, SeMAE 1029.
3. **Não reexecutar** a coleta estadual DCA/TCESP nem os JSON já preservados sem motivo explícito de atualização/versionamento.
4. Manter `G05-D=in_progress` até que vínculo contratual-financeiro ou decisão metodológica de limitação seja documentado. G06 pode ser iniciado como análise condicional, sem pressupor causalidade.

**Handoff obrigatório:** ler README, este relatório, a matriz de candidatos e os registros de QA antes da próxima operação. Os outputs brutos ficam no R2 privado e os scripts/relatórios no GitHub, com hashes e runs identificados.
