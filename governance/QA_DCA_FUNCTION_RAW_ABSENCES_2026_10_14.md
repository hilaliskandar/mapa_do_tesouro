# Auditoria efetiva dos arquivos brutos DCA I-E 2025 — 14/10/2026

Fonte: artefato GitHub Actions `sp645-full-dca-2025-raw` (ID `11517325899`), execução de aquisição [#37693005628](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/37693005628), 645 arquivos municipais do anexo I-E. Comparação com contrato `data/mappings/dca_canonical_v1.yml` (coluna Despesas Liquidadas, código TotalDespesas, função 15/16/17/18/26).

| Função | Valor numérico não zero presente | Linha não encontrada | Zero explícito | Linha correspondente com campo vazio |
|---|---:|---:|---:|---:|
| Urbanismo | 639 | 6 | 0 | 0 |
| Habitação | 146 | 499 | 0 | 0 |
| Saneamento | 330 | 315 | 0 | 0 |
| Gestão ambiental | 527 | 118 | 0 | 0 |
| Transporte | 458 | 187 | 0 | 0 |

Os números reproduzem exatamente as lacunas observadas no workbook e no SQLite canônicos de 2025. Assim, as ausências nas cinco funções **não foram provocadas pela ingestão SQLite nem pela conversão de zeros numéricos em vazio**.

Busca complementar entre municípios sem a linha-padrão de liquidação:
- Urbanismo: 1 de 6 contém alguma linha relacionada em outro estágio e subfunção;
- Habitação: 13 de 499 têm linhas relacionadas em outro estágio; 12 possuem subfunção;
- Saneamento: 3 de 315 têm subfunção em outro estágio;
- Gestão ambiental: nenhum dos 118 tem linha relacionada;
- Transporte: 2 de 187 têm alguma linha relacionada em outro estágio; 1 possui subfunção.

Essas ocorrências **não provam valor liquidado** para a função faltante. Podem indicar valores empenhados ou outra estrutura no demonstrativo. Não substituir ausência por zero.

## Providências

1. Confrontar a semântica de linhas omitidas do Anexo I-E com o contrato/documentação oficial do SICONFI e da DCA.
2. Auditar os casos com subfunções presentes mas total liquidado ausente e conferir os estágios contábeis.
3. Manter `strict_sum` e não imputar zeros enquanto faltar comprovação documental.
4. Disponibilizar as cinco contas individuais e cobertura, mesmo onde o total territorial está ausente; considerar agregado parcial apenas com rótulo explícito e sem confundi-lo com o total.
5. Investigar fonte alternativa oficial de despesa por função para eventual reconciliação, sem fusão tácita de estágios/anos.
