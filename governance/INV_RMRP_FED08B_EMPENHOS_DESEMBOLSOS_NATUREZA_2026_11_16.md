# FED08B — natureza da despesa por empenho e conciliação dos desembolsos

**Processamento em 16/11/2026 sobre snapshot oficial de 15/11/2026.** **Aceite parcial:** cadeia documental de empenho para desembolso examinada. Não constitui comprovação de GND4 **pago a favorecido**, despesa municipal executada ou investimento físico localizado.

## Fontes nacionais efetivamente adquiridas e preservadas

| Arquivo nacional | Linhas nacionais | Linhas selecionadas para RMRP | ZIP bytes | SHA-256 da origem | Cópia Drive privada |
|---|---:|---:|---:|---|---|
| `siconv_empenho.zip` | 441.415 | **2.486** | 23.644.993 | `755b29d84bff3ad65482364035d880f15682637f901486974dfa24b1e72d8a59` | [Arquivo](https://drive.google.com/file/d/1y3k6nOFeMXxqN8od8hnAlFahZWihkQ08/view) |
| `siconv_empenho_desembolso.zip` | 393.062 | **2.592** | 3.990.080 | `07c48daf6e4892faa634377fe84e867a6f6ba04d310582f5a53fd58176bfd825` | [Arquivo](https://drive.google.com/file/d/1AMHb5NyDBBZf2Nqv6uigJp_Iiy6-O513/view) |
| `siconv_empenho_cipi.zip` | 56.105 | **257** | 1.574.111 | `5b4ef56013025d3d26d26a765eb2e690d93fa2916a70886d746575b2bffb4108` | [Arquivo](https://drive.google.com/file/d/1Nme2jpLCBds77trpZ3nFjN_ncrH90k0G/view) |

A origem dos arquivos está em `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/<nome>.zip`. Os três foram baixados e testados na origem e, **individualmente**, recuperados do Drive privado com SHA-256 idêntico e CRC íntegro. Metadados `shared=false`, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`.

## Chaves e cardinalidade

O script [`pipeline/qa/audit_rmrp_fed08b_empenhos.py`](../pipeline/qa/audit_rmrp_fed08b_empenhos.py) vincula:

1. `siconv_empenho.ID_EMPENHO` **e** `siconv_empenho.NR_CONVENIO` (chave composta);
2. `siconv_empenho_desembolso.ID_EMPENHO` e `ID_DESEMBOLSO`;
3. `desembolso_fluxo.id_desembolso`, `numero_convenio` e `valor_centavos` da base regional.

Dois `ID_EMPENHO` são reutilizados em convênios diferentes. Uma junção baseada exclusivamente no ID do empenho seria incorreta: **17 vínculos de desembolso** tocam um dos identificadores reutilizados, e só a chave composta resolve univocamente cada ocorrência. Todas as 2.592 linhas de vínculo selecionadas tiveram correspondência com empenho do mesmo convênio; nenhuma FK órfã.

Os **2.537 desembolsos** da região receberam status de QA:

| Resultado | Desembolsos |
|---|---:|
| Soma dos grupos de empenho coincide exatamente com desembolso | **2.535** |
| Soma dos grupos inferior ao valor do desembolso | **1** |
| Sem vínculo de empenho no CSV oficial | **1** |

A divergência do primeiro caso é de **R$ 88.000,00**; o ID e os valores individuais permanecem no arquivo privado. Não ajustar nem ratear automaticamente. O outro desembolso sem vínculo também permanece fora dos valores classificados.

## Natureza do empenho como atributo de desembolso — não de pagamento final

A consulta da natureza orçamentária dos **2.535 desembolsos com grupos reconciliados** devolveu:

| Prefixo de código de `NATUREZA_DESPESA` do empenho | Soma dos valores dos grupos vinculados |
|---|---:|
| `44` — categoria econômica 4, grupo de natureza 4, quando o código observa a estrutura brasileira usual | **R$ 450.501.858,85** |
| `33` — categoria econômica 3, grupo 3 | **R$ 263.567.534,82** |
| `34` — código atípico, sujeito a revisão antes de classificação substantiva | **R$ 250.000,00** |
| **Total classificado por código nos grupos reconciliados** | **R$ 714.319.393,67** |

Esses valores provêm de `VALOR_GRUPO`, por relacionamento com empenhos, e **não são aditivos** ao valor-pai dos desembolsos nem aos pagamentos de favorecidos. A classificação `44` caracteriza a **natureza orçamentária vinculada ao empenho**, e não comprova que o município executou a despesa capital nem que o pagamento a favorecido ocorreu com a mesma natureza.

Há **257 registros de empenho CIPI associados a 193 projetos distintos** dentre os 218 da carteira; empenho não prova execução física.

## Artefatos e aceite

[**Banco SQLite e QA FED08B privados**](https://drive.google.com/file/d/1IhdpGNx6f5aGu5qtpv1XshKNck8Dr39I/view), 5.728.097 bytes, SHA-256 `bfa04d63b9670f79f812fd53b236506ff45efb444d75afa1b456cfcf47d5693d`; CRC e SHA-256 de readback aprovados. Inclui `RMRP_FED08B_EMPENHO_DESEMBOLSO_PRIVADO.sqlite`, arquivo JSON agregado sem identificadores e CSV privado com os dois desembolsos pendentes. Banco: `integrity_check=ok`, zero violações FK.

**Homologado tecnicamente para análise privada:** origem, integridade, vínculo e atributo de natureza de empenho dos grupos com reconciliação exata.

**Ainda não homologado para indicadores públicos:** pagamentos GND4 efetivamente executados, valor líquido após devoluções/estornos, localização física da obra, rateio por município beneficiário e quaisquer somas entre estágios. `public_release_authorized=false`.

**Próximos gates:** inspecionar em documentos oficiais os dois desembolsos inconciliáveis, validar o significado dos códigos atípicos `34`, buscar fonte que vincule documento/itens de execução à natureza GND do pagamento e executar revisão territorial individual dos 19 projetos divergentes de coordenada.
