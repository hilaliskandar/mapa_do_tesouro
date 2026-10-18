# Auditoria externa dos indicadores constitutivos CAPAG — 16/10/2026

## Fontes e recorte
Foi comparado o arquivo oficial `capag-municipios-posicao-2026-set.xlsx`, SHA-256 `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`, com a tabela `observacao` do `sp645_private.sqlite` do build privado `38905063653`. Recorte: 645 municípios de SP, ano-base 2025, posição setembro/2026. Fonte oficial: aba `Prévia da CAPAG`, tabela das colunas A–L (identificador municipal em A, indicadores constitutivos em E, G, I), diferente da tabela auxiliar Y–AB que contém a classificação final.

## Resultados
| Indicador | Valores observados iguais | Ausências iguais | Divergências |
|---|---:|---:|---:|
| Indicador 1 | 644 | 1 | 0 |
| Indicador 2 | 642 | 3 | 0 |
| Indicador 3 | 623 | 22 | 0 |
| Total | 1.909 | 26 | 0 |

Todos os 1.935 pares (645 × 3) foram cotejados pela chave IBGE: valores com tolerância relativa/absoluta de 1e-10 e ausências como ausência, nunca imputadas. O JSON auditável `auditoria_capag_componentes_20261016.json` foi gerado e SHA-256 `2cddcf7e726ca9851204d42f0afab196ada6186f5e0d31ccc28cb8cd6b3291d5`.

**Resultado:** aprovado para esses componentes na versão privada reconstruída; não declarar que posições de outros meses/anos ou notas explicativas foram verificadas. A classificação CAPAG categórica (inclusive n.d.) foi testada separadamente, na segunda tabela oficial. Não confundir indicador numérico faltante com categoria final n.d.

## Condição para pré-publicação
Preparar API e HTMLs num único artefato imutável com caminhos relativos ou endereço público canônico verificável, e comparar hashes com o artefato privado aprovado. A existência de artefato técnico não autoriza publicar nem fazer merge do PR #198.
