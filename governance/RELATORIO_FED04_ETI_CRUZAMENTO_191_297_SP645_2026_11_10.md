# FED04 — Cruzamento ampliado ETI × DCA 2025, São Paulo (645 municípios)

**Data de referência:** 10/11/2026. **Situação:** auditoria documental, não conciliação bancária nem homologação de variáveis. Fonte primária: [Portaria MEC nº 669/2025, Anexo II](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-669-de-1o-de-outubro-de-2025/@@display-file/file), publicação 02/10/2025. A extração textual do PDF oficial foi realizada integralmente por serviço de leitura de documentos, em alternativa à instância Crawl2AI (que não retornou o PDF), e confrontada por chave IBGE7 com os CSV oficiais do projeto já versionados no GitHub.

## 1. QA de leitura e universos
- **452 registros de redes municipais de SP com código IBGE de sete dígitos** recuperados do Anexo II, sem duplicação de chave; os demais municípios paulistas não listados no Anexo não devem ser interpretados como beneficiários ETI.
- Matriz base DCA/FNDE **645/645** municípios; estrato antes classificado como `somente_dca`: **297/297**; subconjunto sem antecedente VAAT/VAAR 2024/2025: **191/191**.
- Fonte DCA: `governance/FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv`, conta `RO1.7.1.5.00.0.0` e valor anual bruto. A ausência de conta/valor no recorte **não é lançamento contábil de zero**; conservar `estado_dca` da matriz original.
- Regra monetária: `previsto_2025 = round_centavos(0,85 * eti_total_portaria)`, com valores da portaria em centavos. A soma das parcelas mensais já arredondadas pode diferir do cálculo direto em 1–2 centavos; não inferir divergência contábil daí. A portaria autoriza cronograma, **não comprova crédito bancário**.

## 2. Cruzamento 191 casos
- Os **191 municípios** constam **191/191** da relação federal ETI.
- **182/191 com valor DCA 2025 exatamente idêntico ao montante previsto 85% ETI**; soma DCA desse grupo: **R$ 64049983.11**.
- **9 municípios** com diferença monetária; soma DCA desse grupo: **R$ 1303975.90**.
- Total DCA do grupo inicial: **R$ 65353959.01**, do qual a conciliação monetária exata abrange **98.0047%**.

### Nove casos para auditoria documental específica

| IBGE7 | Município | DCA 2025 R$ | ETI federal 85% R$ | DCA − ETI 85% R$ | DCA / total ETI |
|---|---|---:|---:|---:|---:|
| 3522307 | Itapetininga | 607329.76 | 809773.03 | -202443.27 | 63.7500% |
| 3513504 | Cubatão | 340019.75 | 453359.66 | -113339.91 | 63.7500% |
| 3523701 | Itirapuã | 33438.02 | 133752.09 | -100314.07 | 21.2500% |
| 3500600 | Águas de São Pedro | 33990.48 | 67980.96 | -33990.48 | 42.5000% |
| 3519501 | Ibirarema | 87438.17 | 116584.22 | -29146.05 | 63.7500% |
| 3548104 | Santo Antônio do Jardim | 58179.27 | 77572.36 | -19393.09 | 63.7500% |
| 3521408 | Iracemápolis | 99456.88 | 83707.73 | 15749.15 | 100.9923% |
| 3547403 | Santa Rita d'Oeste | 3056.12 | 4074.82 | -1018.70 | 63.7500% |
| 3509304 | Cajobi | 41067.45 | 41070.95 | -3.50 | 84.9927% |

Há casos com DCA inferior ao 85% previsto e outro com DCA superior, inclusive percentuais que sugerem cronograma parcial ou outras fontes acumuladas. **Percentual semelhante a parcela não prova a origem**, exigindo controle do repasse e escrituração de cada município.

## 3. Cruzamento 297 casos originários
- **277/297 constam da relação ETI**, e **20/297 não constam da lista municipal ETI consultada**; estes 20 concentram **R$ 8270384.30** em DCA 2025.
- **184/297 apresentam valor DCA exatamente igual a 85% ETI**: R$ 65046678.02 de receita DCA.
- **93/297** têm ETI listado, mas DCA diferente do valor 85% previsto, o que **não constitui automaticamente divergência**: pode haver valor misto com VAAT/VAAR, outros ajustes, parcelas parciais, competência ou classificação.
- Atenção: os 106 municípios com antecedente VAAT/VAAR em 2024 não devem ser automaticamente justificados por esse ano; reavaliar com base na modalidade ETI 2025.

## 4. Cruzamento integral SP645
- **452/645** redes municipais SP listadas no Anexo II.
- **188/645** valores DCA exatamente iguais a 85% ETI (incluindo casos fora dos 297), representando **R$ 65702821.73**.
- **264/645** redes ETI listadas têm valores DCA diferentes; **193/645** municípios não estão no Anexo II.
- O status da DCA deve ser lido junto com `estado_dca`, para evitar confundir declaração ausente e zero efetivamente informado. Portanto a matriz SP645 serve como **cobertura** e não demonstra saldo estadual de irregularidade.

## 5. Implicações metodológicas
1. O estado `SEM_BENEFICIO_2024_2025_IDENTIFICADO` do conjunto dos 191 precisa ser qualificado: a **fonte ETI 2025 foi agora identificada para todos**. Não apagar valores históricos nem deduzir pagamentos.
2. A rubrica agregada de complementação ao Fundeb pode conter fontes/mecanismos diferentes. Não somar os valores de ETI sobre DCA, nem tratar 85% como comprovante de repasse.
3. Para os nove casos divergentes, obter balancetes mensais da receita 2025, abertura da natureza `171553`, comprovantes FNDE/SIGEF e cronologia de recebimento. Para os 93 casos mistos do grupo 297, verificar sobreposição VAAT/VAAR/ETI e ajustes anteriores.
4. A homologação exige validação bancária e contábil da natureza de cada parcela; o cruzamento aqui apenas estabelece **equivalência de valores entre registros e cronograma federal**.
5. FED04 permanece **in_progress**, PR #232 permanece **draft**; não alterar variáveis canônicas, banco produtivo, R2 ou publicação.

## 6. Arquivos deste lote
- `governance/FED04_ETI_2025_CONFRONTO_191_2026_11_10.csv`
- `governance/FED04_ETI_2025_CONFRONTO_297_2026_11_10.csv`
- `governance/FED04_ETI_2025_CONFRONTO_SP645_2026_11_10.csv`

**Controle de qualidade:** total de chaves IBGE7 únicas na portaria 452; conjuntos 191/297/645 consistentes; contagens exatas 182/184/188, respectivamente. Nenhuma migração ou publicação.
