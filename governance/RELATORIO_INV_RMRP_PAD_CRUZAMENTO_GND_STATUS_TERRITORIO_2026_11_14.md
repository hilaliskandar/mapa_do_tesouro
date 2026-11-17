# INV-RMRP — Auditoria cruzada do Plano de Aplicação Detalhado

**Data de verificação:** 14/11/2026. **Estado:** execução confirmada de classificação preliminar; sem homologação de investimento pago ou executado.

**Fonte de evidência:** GitHub Actions [run 43559500185](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43559500185), commit `26211302bce787d826e692a2488e820e51fb41ab`, job `132339781041`, `success`; artefato `14099102793`, nome `inv-rmrp-transferegov-plano`, ZIP SHA-256 da publicação do Actions `00ced3512096ec08bd33b30f11ed447e58586b9318c64e1ab9aa60707277e75f`, expiração indicada 28/11/2026. Os logs do job registram sucesso das etapas de download, cruzamento, QA e arquivamento.

## Evidência extraída do log

- 4.917.545 itens de PAD examinados em arquivo nacional, 28.456 vinculados por `ID_PROPOSTA` a 6.410 propostas de 34 municípios **proponentes** da RMRP.
- Identificadores `ID_ITEM_PAD`: 28.456 distintos; sem vazios ou duplicações.
- Natureza planejada: 16.156 candidatos GND4, 287 GND5, 50 GND6, 11.920 correntes e 43 indeterminados.
- Situação administrativa marginal: 15.342 `APROVADO`, 217 `EM_COMPLEMENTACAO`, 12.897 vazios.
- **Novo cruzamento auditado:** 7.917 itens com `GND4 AND SIT_ITEM=APROVADO`; destes, 7.911 têm `SIGLA=SP` e seis indicam outra UF.
- O predicado `SIGLA=SP` **não** atesta que o município de execução seja um dos 34 municípios da RMRP.

## Etapa seguinte adicionada ao workflow

Script `pipeline/qa/audit_inv_rmrp_pad_cross_tab.py` atualizado no commit `19b12d32e66fe2d5ffed4a8d425a5d4ecdfa1849` para acrescentar correspondência nominal exata, normalizada, de `MUNICIPIO` e `SIGLA=SP` com o cadastro de 34 municípios por IBGE7, preservando o nome do proponente em campo separado. O produto adiciona distribuição de situações de correspondência e pares proponente–município indicado, **ainda não auditados em nova execução nesta entrada**.

Não converter correspondência por nome em geolocalização homologada, pois a confirmação final requer código territorial da origem ou documentação do local de execução. Não agregar os valores de `VALOR_TOTAL_ITEM` como desembolso; não ratear os 2.537 eventos federais de desembolso por proporção arbitrária entre GNDs.

## Próximos gates

1. Conferir nova execução do workflow e os campos `gnd4_approved_destination_match` e `gnd4_approved_proponent_to_named_destination`, reconciliando a soma com 7.917.
2. Persistir artefato e bruto oficial em R2 privado com SHA256 e readback antes do vencimento do artefato Actions.
3. Validar municípios de execução com chaves oficiais, identificando casos fora da RMRP ou plurimunicipais.
4. Validar natureza GND4, validade documental dos itens e eventos efetivos de desembolso no nível de instrumento; segregar financiamento e execução física.
5. Não alterar painel, SQLite canônico ou produção antes de concluir QA.



## Execução de territorialização por nome — 14/11/2026

GitHub Actions [43560489903](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43560489903): `success`; artefato `14099754349` (`inv-rmrp-transferegov-plano`), checksum do ZIP de artefato `sha256:5d7548abb11719a1844c37f1e56df17f508dcfd099c84b7370b5ae7a63ee77b3`.

O log contém cruzamento oficial das 28.456 linhas e, **dentro dos 7.917 itens candidatos GND4 com SIT_ITEM=APROVADO**, identificou: **7.891 com correspondência nominal em um dos 34 municípios da RMRP**, **20 com município informado de SP sem correspondência com o cadastro RMRP** e **seis com UF diversa de SP**. A soma (7.891 + 20 + 6) reconcilia os 7.917 itens. Correspondência por nome não é homologação geoespacial, nem pagamento.

Em 14/11 foi acrescentada a rotina de `gnd4_approved_territorial_exceptions_all` para enumerar os 26 itens sem correspondência, preservar `ID_ITEM_PAD` e `ID_PROPOSTA`, bem como `gnd4_approved_other_rmrp_destination_count` para separar propostas com destino indicado em município da RMRP **diferente do proponente**. Commit `9cbb63e277bb9eb25b151e72d692cfa82fabcd76`; a nova execução [43561970362](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43561970362) encontrava-se em fila na consulta inicial. **Não atribuir valores derivados dessa nova rotina sem resultado e QA concluídos.**

Próximo gate: conferir enumeração e vínculos cruzados no novo log, verificar município de aplicação em fonte oficial por chave, cruzar sem arbitrariedade com número de convênio, `ID_PROPOSTA` e eventos de desembolso e persistir snapshots no R2 com readback. A metodologia continua limitada ao município proponente quando o dado territorial de execução não está validado.
