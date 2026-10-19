# Primeiro módulo executado da Nota Técnica v1.3 — ITBI e composição das receitas

Data 19/10/2026. Fonte principal: `DCA_SP_645_2013_2025_CANONICO.csv`, arquivo Google Drive `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`; roster `editorial/rmrp/municipios_subregioes_tcesp.csv`. Referência metodológica: [Nota Técnica v1.3](https://docs.google.com/document/d/1SvarT65MQMU-qmpjqFzxLjf0d4uKkXpkegmjVCIJZ14/edit), seção 7. O documento é intitulado v1.3 no Drive, mas o corpo examinado conserva cabeçalho “Versão 1.2”; tratar como divergência documental a reconciliar, não como nova metodologia.

## Cobertura e operação

34 municípios × 13 anos = 442 registros municipais. ITBI principal presente em 434 registros; média móvel nominal trianual calculada somente com três anos consecutivos válidos em 354; CV quinquenal calculado apenas com pelo menos três observações da janela temporal em 306, explicitando n válido. 13 anos × cinco recortes territoriais = 65 registros agregados. Totais integrais publicados apenas se todos os municípios do respectivo recorte apresentarem dado. Nenhuma imputação de zero.

## ITBI principal em 2025

| Recorte | Municípios com dado | ITBI (R$) | Participação na receita corrente | Participação na receita tributária |
|---|---:|---:|---:|---:|
| SR1 | 15/15 | 231.235.749,80 | 2,82% | 9,77% |
| SR2 | 6/6 | 20.157.461,79 | 1,43% | 7,45% |
| SR3 | 6/6 | 11.128.555,93 | 1,23% | 7,10% |
| SR4 | 7/7 | 22.830.336,82 | 1,72% | 10,51% |
| **RMRP** | **34/34** | **285.352.104,34** | **2,41%** | **9,48%** |

Participações calculadas por razão entre somas do mesmo exercício e recorte, não médias municipais. O módulo também expõe IPTU principal, ISS principal, FPM, cota-parte ICMS e IPVA, receitas corrente e tributária para análises posteriores, sem declará-las receita própria ampliada ou transferências totais.

## Limitações e próximos cálculos

- Não equiparar ITBI arrecadado a número de transmissões ou valorização dos imóveis.
- Não calcular “ITBI caixa ampliado”: o caderno metodológico FINBRA A8 o considerou não reconstituível defensavelmente na série histórica.
- Médias e coeficientes de variação deste primeiro módulo usam valores **nominais**. Antes de empregá-los para comparações de dinâmica econômica, executar o mesmo módulo com valores reais por IPCA, sob a data-base canônica explicitada.
- A participação do ITBI na RCL oficial depende do RREO e não pode ser substituída silenciosamente por receita corrente bruta da DCA.
- Próximos módulos: dependência FPM/ICMS/IPVA e autonomia de tributos principais; poupança/pressão corrente com ressalva de ajuste; séries e janelas móveis em valores reais; cobertura do esforço territorial; itens de RGF/RREO/CAPAG condicionados às respectivas fontes.

Os CSVs derivados desta execução estão em `/mnt/data/rmrp_nota_tecnica/` no ambiente de trabalho: `modulo_itbi_receitas_municipal_2013_2025.csv`, `modulo_itbi_receitas_subregional_2013_2025.csv`, `QA_MODULO.json` e `build.py`. Para preservação permanente, anexar os quatro arquivos ao repositório ou Drive. O documento atual não equivale a fechamento dos 72 conceitos.

**SCN:** fonte IBGE `02_estrutura_scn.pdf` é referência de conceitos e fluxos econômicos; investimento 4.4 liquidado da DCA não é sinônimo de formação bruta de capital fixo do SCN.