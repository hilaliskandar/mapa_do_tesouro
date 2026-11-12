# INV-RMRP — Auditoria de colisão dos identificadores SIAFEM em Batatais

**Data:** 12/11/2026. **Situação:** duas grafias de ID financeiramente não conciliadas; hipótese robusta de mesmo processo jurídico DETRAN 2447861/2019. **Não foi provada duplicação de valores nem autorizada dedução dos totais.**

## 1. Descoberta no inventário SIAFEM

Ao comparar os **752 identificadores brutos de convênio** do arquivo `governance/INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv`, agrupados por município IBGE7 e após remoção **apenas de pontuação**, detectou-se **uma colisão**:

| Identificador bruto | Consulta | Objeto da ficha | Liberações contidas no snapshot |
|---|---|---|---:|
| `5128032447861-19` | HTTP 200 | PROGRAMA RESPEITO A VIDA | **R$ 273.147,07**, 17/12/2021 |
| `5128032447861\19` | HTTP 500 | Indisponível | **R$ 334.000,00** em 2021 e **R$ 51.000,00** em 2022 |

A segunda grafia registra **R$ 385.000,00** em duas linhas instrumento–ano; a soma das duas grafias registra **R$ 658.147,07**. Os registros compartilham beneficiário Prefeitura Municipal de Batatais (CNPJ 45.299.104/0001-87), prefixo numérico e exercício original do instrumento, mas o segundo detalhamento não está acessível. Não eliminar nenhum lançamento por presunção de repetição.

URLs da fonte:
- https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=5128032447861-19
- https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=5128032447861%5C19

## 2. Instrumento público que explica a semelhança das chaves

Foi localizado o **extrato primário no Diário Oficial do Estado de São Paulo de 27/12/2019**, Poder Executivo, Seção I, vol. 129, nº 244, página 5. Trata-se do:

- **Convênio público DETRAN nº 101/2019**, **Processo DETRAN nº 2447861/2019**, assinado em **18/12/2019** com o Município de Batatais;
- **Objeto:** execução do Programa Respeito à Vida, conforme Decreto nº 64.293/2019 e plano de trabalho;
- **Valor conveniado original: R$ 689.301,77**, descrito no extrato como a ser transferido em **uma parcela**;
- **Fonte oficial:** https://www.imprensaoficial.com.br/Certificacao/GatewayCertificaPDF.aspx?notarizacaoID=48a00f3a-e29f-4a4e-8750-0b093218f072

A sequência `2447861/2019` do processo público aparece nas duas grafias dos números SIAFEM, o que fortalece a hipótese de pertencimento ao **mesmo convênio jurídico original**; entretanto, **não existe ainda prova de que a soma ou qualquer parcela individual esteja repetida contabilmente**.

**Conciliação parcial:**

- Valor original do termo: **R$ 689.301,77**;
- Soma de liberações registradas nas duas grafias: **R$ 658.147,07**;
- Diferença: **R$ 31.154,70**.

O extrato original prevê uma parcela, enquanto a fonte financeira apresenta três lançamentos distribuídos entre 2021–2022. O aparente desacordo pode decorrer de ajustes, estornos, fases contábeis ou outras circunstâncias **não comprovadas**. Não se presume qualquer explicação nem se deduz a diferença do saldo a liberar de um convênio sem ficha de reconciliação.

## 3. Conclusão e controle de risco

A classificação recomendada é `PROVAVEL_MESMO_PROCESSO_DETRAN_2447861_MAS_LANCAMENTOS_DISTINTOS_NAO_CONCILIADOS`.

Distinções essenciais:

1. **Identificadores:** existem 752 identificadores brutos únicos na amostra. Depois de normalização restrita de separadores, há uma família com duas grafias potencialmente equivalentes. Isso **não autoriza alterar a cardinalidade dos lançamentos**.
2. **Instrumento jurídico:** extrato DETRAN nº 101/2019 fornece um **identificador de processo público compartilhado por semelhança numérica**; a equivalência integral de sistemas requer confirmação oficial.
3. **Fluxos financeiros:** a coexistência de R$ 273.147,07 e R$ 385.000,00 não prova repetição do mesmo pagamento. Como a soma é inferior ao valor original do convênio, **a dedução de R$ 385 mil, proposta apenas com base na grafia, seria indevida**.
4. **Totais RMRP:** o agregado financeiro permanece **R$ 305.521.029,20**, **valor bruto da série de liberações/estornos tal como obtida da fonte**, com ressalva de conciliação documental desta família. Nada foi somado ou subtraído.
5. **Próximos documentos:** histórico de ordens de pagamento do DETRAN, plano de trabalho, termos aditivos, prestações de contas, eventuais chaves financeiras de ambos os registros e demonstrativo de pagamentos com data/ordem/conta para comprovar individualização dos fluxos. A documentação inicial do Programa Respeito à Vida e os lançamentos SIAFEM não demonstram execução física de intervenção viária.

## 4. Implementação de QA na PR 233

- Dossiê: `governance/INV_RMRP_BATATAIS_COLISAO_IDS_SIAFEM_5128032447861_2026_11_12.json`.
- Script: `pipeline/qa/qa_inv_rmrp_siafem_id_colisoes.py`.
- Workflow: `.github/workflows/inv-rmrp-siafem-id-colisoes-qa.yml`.

O teste exige 752 chaves brutas, 889 registros instrumento–ano, exatamente uma colisão conservadora de pontuação, **R$ 273.147,07 e R$ 385.000,00** nos registros respectivos, valor público **R$ 689.301,77**, diferença de **R$ 31.154,70**, sem fusão ou dedução e total estadual preservado.

**Governança:** a auditoria não altera R2, SQLite, D1 ou site produtivo; PR #233 draft; PR #232/FED04 não modificada.
