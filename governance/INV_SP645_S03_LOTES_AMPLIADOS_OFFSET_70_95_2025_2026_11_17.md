# S03 — validação de lotes ampliados SIAFEM 2025, offsets 70 e 95 — 17/11/2026

**Escopo:** consultas Sefaz-SP / SIAFEM de transferências voluntárias a prefeituras, tipo investimento, exercício de liberação 2025. Os 34 municípios da RMRP previamente consultados em 2020–2026 foram excluídos do universo de expansão. **Destino:** staging e snapshots R2 privados. **Estado:** validação da aquisição e dos totalizadores da fonte; dados ainda sem homologação financeira. `public_release_authorized=false`.

## Modificações do coletor e da orquestração

A versão modificada de [`.github/workflows/sp645-siafem-annual-pilot-r2.yml`](../.github/workflows/sp645-siafem-annual-pilot-r2.yml) admite `limit` 5, 10, 15 ou 25 no `workflow_dispatch`, `offset` e `year` parametrizados, limite de execução de 30 minutos, exclusão do gatilho automático `push` e grupo de concorrência por branch/ano/offset para evitar duplicação simultânea. A rotina já admitia `--limit <=25`; não foi necessário elevar o teto interno do coletor.

O QA do workflow valida: hash bruto SHA-256; cardinalidade de consultas; unicidade de IBGE7 requeridos; separação exaustiva de respostas reconciliadas e consultas falhas; reconciliação por totalizador; e prefixo imutável privado com comprimento real `len25`, sem reaproveitar o prefixo `len5`. A concorrência evita simultaneidade por offset, mas **não impede reexecuções sequenciais de offsets já processados**; o inventário de cobertura deve ser checado antes de cada disparo.

## Execuções do piloto ampliado

| Offset | Evidência GitHub Actions | Municípios consultados | Reconciliados | Inconclusivos | Convênios-ano | Pagamentos agregados | Liberações líquidas e estornos |
|---:|---|---:|---:|---:|---:|---:|---:|
| 70 | [44027492348](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44027492348) | 25 | 20 | 5 | 53 | 56 | R$ 26.742.701,09 |
| 95 | [44027631705](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/44027631705) | 25 | 24 | 1 | 85 | 94 | R$ 80.520.381,14 |
| **Total adicional** | | **50** | **44** | **6** | **138** | **150** | **R$ 107.263.082,23** |

Ambos os workflows terminaram com `conclusion=success`; todos os resultados contabilizados como válidos tiveram reconciliação por totalizador, e ambos registraram `SP645_SIAFEM_PILOT_READBACK_PASS`, após a leitura de retorno do arquivo bruto no R2 privado.

- Offset 70: `raw.json` 25.928 bytes, SHA-256 `42ec879ec4b4ca11564b97cceca7aec1c00ab6082d0448bffac842d90ce16bc4`.
- Offset 95: `raw.json` 36.199 bytes, SHA-256 `dac6e0250e3cf885d5b679075b41c391b53246aa49e3a720009fec55f9be6f02`.

Prefixos privados de cada snapshot: `r2://financas-municipais-sp-canonico/sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_{70|95}_len25/{sha256}/`, com `raw.json` e `qa.json`.

## Consultas inconclusivas

- Offset 70: `3507209`, `3507308`, `3507456`, `3507704`, `3508009`.
- Offset 95: `3509809`.

Todos são classificados em `cobertura.csv` como `erro / ausencia_indeterminada` e possuem pendência própria em `pendencias.csv`. **Não representam transferência zero.** As consultas históricas inconclusivas anteriores também são preservadas.

## Cobertura acumulada — exercício 2025, fora da RMRP

Desde o início da expansão, **120 dos 611 municípios externos à RMRP foram consultados**. Destes, **101 tiveram resultado estruturalmente reconciliado** e **19 permanecem inconclusivos**. Os resultados válidos somam **314 convênios-ano**, **341 pagamentos agregados** e **R$ 215.849.622,63** de liberações líquidas e estornos de investimento. **491 municípios externos à RMRP ainda não foram consultados em 2025**.

O acumulado anterior (offsets 0–65) abrangia 70 consultas, 57 válidas, 13 inconclusivas, 176 convênios-ano, 191 pagamentos e R$ 108.586.540,40, documentado [no relatório anterior](INV_SP645_S03_LOTES_OFFSET_55_60_65_2025_2026_11_17.md). A duplicata lógica histórica do offset 0 não foi adicionada.

**Observações metodológicas:** o total da fonte refere-se a liberações líquidas/estornos de instrumentos com filtro de investimento; não representa valor celebrado, execução orçamentária municipal liquidada, valor individual de parcela, nem repasse federal. Não somar aos agregados RMRP34 ou FINBRA/TCESP sem modelo de fatos por estágio, exercício e fonte.

## Próximas providências

1. Conferir o histórico de execução e a cobertura antes de avançar ao **offset 120, com 25 municípios**, em série, sem paralelizar chamadas ao portal.
2. Melhorar o tratamento de erro para separar ausência comprovada na resposta oficial de parser/timeout ou mensagem não interpretada; manter o resultado inconclusivo enquanto a evidência for insuficiente.
3. Para expansão intensiva, acrescentar fila persistida/checkpoint e política de retry/backoff controlado para eventos transitórios, sem recolher municípios reconciliados.
4. Continuar os controles `execucoes.csv`, `snapshots.csv`, `cobertura.csv`, `pendencias.csv` e documentação por lote com SHA-256/R2.
5. Manter `public_release_authorized=false`, sem alterações em SQLite fiscal produtivo, D1, Pages ou API pública antes da homologação e autorização.
