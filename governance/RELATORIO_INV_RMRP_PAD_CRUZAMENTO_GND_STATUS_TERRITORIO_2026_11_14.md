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

