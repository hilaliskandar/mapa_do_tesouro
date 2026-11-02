# Lote 39 — recuperação da receita de capital bruta de 2025 e inventário I-C 2020–2025

**Data:** 01/11/2026. **Status:** rubrica sintética 2025 extraída e totalizada para 34/34 municípios; série 2020–2024 com arquivos-fontes localizados, ainda não extraída/homologada. Sem pesquisa externa: exclusivamente arquivos Drive já arquivados.

## Fonte e escopo

Inventário FINBRA_DCA_CANONICA_FINAL_2013_2025_2026-09-26 (Drive ID `14i5tnXO6IC6dugU-4w-D_5ogbCWV3RLGoUED-YrGh90`) identificou anexos I-C:
- 2020: Drive `1l5E_in3CFmz_PDUcgK8kEABbtRCMpYnu`, formato XLSX, 645 municípios SP;
- 2021: `1m8SwRQooXJRd6RHHzr7UVnnbUSqYMW8R`, XLSX, 645;
- 2022: `1q8ZjZ1W7L8cOY1bqOLHxBDFYGrgPb63s`, XLSX, 644;
- 2023: `1SeGGScw5Vd9PrZzLBDcPg9KDXDAjjjRI`, XLSX, 645;
- 2024: `1ZJyPzXbwB7jvnrOmQXjv5tS1Fpuq5enu`, XLSX, 630;
- 2025: `185x_7zgX9aGOy0Z6Drh-iA9vBY83JU1F`, CSV, 632 municípios SP.

A presença na enumeração de arquivos não prova a cobertura específica dos 34 municípios da RMRP para 2020–2024. Essa verificação é o próximo gate.

## Extração efetiva do arquivo original 2025

Arquivo original 2025 obtido por conector Drive; linhas de municípios da RMRP filtradas por código IBGE do cadastro territorial versionado. Critério simultâneo: coluna `Coluna = Receitas Brutas Realizadas` e `Identificador da Conta = siconfi-cor_RO2.0.0.0.00.0.0`; valores brutos em reais nominais, com vírgula decimal convertida para ponto para operação. Não foram somadas contas filhas. Foi localizada observação de receita de capital bruta para **34/34 municípios**.

| Território | Municípios | Observados | Receita de capital bruta realizada em 2025, R$ nominais |
|---|---:|---:|---:|
| Sub-região de Ribeirão Preto | 15 | 15 | 233.092.440,70 |
| Sub-região de Jaboticabal | 6 | 6 | 32.712.302,23 |
| Sub-região de Mococa | 6 | 6 | 36.523.843,09 |
| Sub-região de Batatais | 7 | 7 | 25.614.199,12 |
| **RMRP** | **34** | **34** | **327.942.785,14** |

A soma das quatro sub-regiões confere com o total metropolitano: R$ 327.942.785,14. Este cálculo não equivale a receita de capital líquida, caixa disponível ou destinação comprovada a investimentos. O arquivo bruto não altera a observação parcial no indicador distinto `dca_transferencias_capital` (Santa Cruz da Esperança) do Lote 36.

## Diferenças conceituais e próximos testes

- Contrastar conta sintética `RO2.0.0.0` com componentes de crédito, alienação e transferências, sem pressupor que a soma dos três esgote a hierarquia.
- Conferir para cada exercício 2020–2024 conta `RO2.0.0.0`, estágio equivalente, cobertura 34/34, duplicidades e status, e mudança classificatória em 2022. O inventário indica arquivos localizados, **não extrações concluídas**.
- Revisar a planilha 2015–2019 do Lote 38 (167/170 observações) para compatibilização em série única a valores correntes e reais (IPCA médio anual, base set/2026).
- Associar recursos a projetos somente mediante instrumento identificado, estágios e fonte original, não por coincidência de valores anuais.

**Gate E4:** novo dado de capital bruto 2025 observado e somado, sujeito à auditoria contábil final. **Gate E5/E6:** carteira individualizada e parâmetros futuros permanecem pendentes. Não anualizar 2026 parcial. Nenhuma projeção futura atribuída.
