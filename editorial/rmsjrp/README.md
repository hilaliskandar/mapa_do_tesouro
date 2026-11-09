# RMSJRP — continuidade operacional do estudo fiscal
**Atualizado:** 2026-11-09. **Estado:** Fase I e G04 concluídos quanto aos dados centrais. G05-A/B/C executados e auditados (diagnóstico, programas/ações e cartografia IBGE 2022); G05-D com primeira verificação documental executada e dez chaves contábeis auditadas; vinculação projeto–contrato ainda parcialmente pendente. Nenhum texto municipal ou cenário homologado.

## Ponto de partida
- Plano integral e sequência de gates: [PLANO_EXECUCAO_2026_11_09.md](PLANO_EXECUCAO_2026_11_09.md).
- Universo: `RM_SAO_JOSE_RIO_PRETO`, 37 municípios, já cadastrado em `data/catalogs/territorial_universes_sp_2025.yml` e `data/catalogs/publication_universes_sp.yml`.
- Referências metodológicas: [RMRP](../rmrp/README.md), [RMJ](../rmj/README.md) e [continuidade RM/AU](../../governance/CONTINUIDADE_OPERACIONAL_RM_AU_2026_10_18.md).
- Base DCA estadual 2013–2025: `sp_645/dca/2013_2025/normalized.csv`, snapshot R2 privado; hash canônico documentado `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`. Verificar readback e versão antes de filtrar.
- TCESP 2023–2025: objetos homologados em R2 `tcesp/estadual/despesas/{ano}/run_...`; detalhes em `governance/HOMOLOGACAO_TCESP_R2_SQLITE_API_V2_20261026.md`. Armazenamento não demonstra implantação pública.
- RREO/RGF/CAPAG: aproveitar snapshots atuais, conservando conceitos de demonstrações legais.
- Escopo: histórico 2013–2025, investimentos liquidados 2023–2025, cenários condicionais 2027–2030, fichas individuais de 37 cidades e agregados territoriais.
- Documentação de dados e QA precede redação; publicação, deploy e divulgação requerem decisão específica.

## Gate ativo
**G04 — Indicadores e cálculos: QA técnico aprovado; próximo G05.** Foram lidos DCA 2013–2025 (481/481 pares), Gate C/D 2025 (37 municípios), TCESP R2 2023–2025 (111/111 liquidados), e 111/111 pares DCA × TCESP com diferença zero. Run 42559912064, R2 privado readback. Ver [relatório G00–G03](RELATORIO_FASE_I_2026_11_09.md), [handoff](HANDOFF.md) e [matrizes de cobertura](MATRIZ_COBERTURA_DCA_2013_2025.csv). Indicadores RREO/RGF seguem parciais e sem imputação.

## Quadro de gates
| Gate | Conteúdo | Status inicial |
|---|---|---|
| G00 | Inventário de reuso, versão e hash | qa_pass |
| G01 | Território, sub-regiões, população, IPCA | in_progress — território aprovado; geometria e deflator pendentes |
| G02 | Filtro e QA DCA 2013–2025 | qa_pass |
| G03 | TCESP 2023–2025, RREO/RGF/CAPAG | qa_pass — cobertura legal parcial documentada |
| G04 | Indicadores, cálculos e reprodutibilidade | qa_pass — séries DCA; cautelas IPCA/população |
| G05 | Diagnóstico territorial, tabelas e mapas | in_progress — A/B/C aprovados; G05-D documentado parcialmente, 10/10 chaves QA, sem identificação causal |
| G06 | Arcabouço e cenários 2027–2030 | not_started |
| G07 | Cinco fichas-piloto e 32 fichas restantes | not_started |
| G08 | Sínteses territoriais e revisão substantiva | not_started |
| G09 | Revisão independente de 37 fichas | not_started |
| G10 | DOCX/PDF, mídia e prova visual | not_started |
| G11 | Persistência, homologação e publicação eventual | not_started |

## Contrato de passagem entre chats
Sempre começar pela leitura do plano, deste README, dos registros de gate e do manifesto existente; consultar o commit da branch/main e o último handoff, conferir os artefatos remotos. Ao terminar, registrar data, gate, decisão, arquivos, URLs/IDs, SHA, testes, municípios concluídos, bloqueios e **próxima ação exata**, e verificar o readback dos arquivos de Drive/R2. Não trocar a fonte oficial, a escala de percentuais, o deflator ou texto aprovado silenciosamente. Manter ausência distinta de zero. A existência de arquivo no R2 não prova ingestão SQLite; um CI verde não prova deploy; um PDF gerado não prova revisão editorial.

## Registro inicial / próximo comando de trabalho
**2026-11-09 — Execução Fase I:** matriz de 37 municípios e quatro sub-regiões; 481 pares DCA com QA; 774 observações DCA–Gate C 2025 conciliadas; R2 TCESP 111 pares e DCA 111 pares conciliados em centavos, três objetos QA persistidos no R2 com hashes. Run [42559912064](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42559912064). **Próxima ação:** iniciar G04, resolvendo deflator IPCA médio anual, população, cartografia analítica e a verificação seletiva das ausências RREO/RGF. Ver HANDOFF.


## G04 — Execução comprovada e continuidade — 09/11/2026
- **Relatório:** [`RELATORIO_G04_2026_11_09.md`](RELATORIO_G04_2026_11_09.md), com indicadores, método, tabelas, hashes e cautelas; **workflow** [42561177880](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561177880), `success`.
- **Fonte DCA:** R2 estadual, SHA `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`. Reutilizados fatores anuais do IPCA, preços setembro/2026, [Lote 17 RMRP](../rmrp/IPCA_MEDIA_ANUAL_SET2026_LOTE17.md); fatores locais em `IPCA_MEDIA_ANUAL_SET2026.csv`. Não misturar IPCA de dezembro com média anual.
- **Produtos persistidos no R2 privado:** `rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv` (481 linhas, SHA `1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5`); `SERIES_TERRITORIAIS_2013_2025.csv` (65 linhas, SHA `70438537957f6b31bdf80e2e6705a5153735757a42d6cc8129067006087f6268`); `QA_G04.json` (SHA `dc4c9324a304a08d3d6f1cd5bc7ca446239ad4bf29688babb707adc9928a9fd1`). Readback e hash aprovados.
- **Resultado de controle:** receita corrente real RMSJRP +11,61% 2023–2025; investimento liquidado real −57,27% no mesmo intervalo; não inferir causalidade a partir dessas variações.
- **Denominador demográfico:** a base DCA contém a mesma população numérica em 2024 e 2025 para todos os 37 municípios; não tratar 2025 como atualização populacional independente. Existem três populações ausentes em anos anteriores; agregados incompletos permanecem NA.
- **Próxima ação exata G05:** recuperar as séries de 65 território-ano do R2, produzir as tabelas da trajetória de 2023, 2024 e 2025 e a desagregação municipal, testar as diferenças entre polo/demais municípios e preparar mapas somente com malha cujo CRS analítico esteja comprovado. Conferir fonte das 19 lacunas RREO/RGF sem nova coleta estadual. Atualizar README/HANDOFF ao final de cada lote; sem alterações no portal público.


## G05 — Diagnóstico territorial e cartografia — 09/11/2026
- **Documento substantivo e inventário:** [`RELATORIO_G05_LOTE_A_2026_11_09.md`](RELATORIO_G05_LOTE_A_2026_11_09.md). Retomada no [HANDOFF](HANDOFF.md).
- **G05-A**: 15 séries território-ano, 15 variações territoriais, 111 contribuições municipais; 2024–2025: investimentos reais −R$ 312,86 mi, 29/37 municípios com queda; São José do Rio Preto −R$ 220,83 mi. [run 42561961530](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561961530). R2 `rmsjrp/g05/2026_11_09/` e hashes no relatório.
- **G05-B**: reuso TCESP 2023–2025 por órgão/programa/ação, 4.884 movimentos por chave e 111 conciliações municipal-ano em centavos; [run 42562212589](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562212589). R2 `rmsjrp/g05/2026_11_09/programas_acoes/`. **Diferenças nominais por programa não são diferenças reais do município**, nem provam descontinuidade física de obra.
- **G05-C**: IBGE malha municipal SP 2022, SIRGAS2000 EPSG:4674, 645 feições no estado, 37 feições selecionadas e válidas, sem simplificação geométrica. Dois mapas de investimentos (variação 2024–2025 e per capita 2025) + GeoJSON regional com readback R2. [run 42562450625](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562450625), R2 `rmsjrp/g05/2026_11_09/cartografia/`. Origem oficial e SHA no relatório.
- **G05-D pendente:** confrontar os movimentos principais a documentação de execução física, contratos, reclassificações e programas; somente depois incorporar interpretações individualizadas e homologar texto. Os mapas devem entrar nos pontos analíticos adequados, não em um atlas separado.
- **Próxima ação exata:** usar `G05B_MAIORES_MOVIMENTOS.csv` e `G05B_TRANSICOES_PROGRAMA_ACAO_2023_2025.csv` já persistidos, levantar evidências para os programas SJR Prefeitura 9/SEMAE 31, Olímpia 45, Monte Aprazível 14, comparar mudanças de código/órgão e documentar o que permanece hipótese. Depois fechar G05-D com QA editorial e retomar G06.


## G05-D — Diligência documental e crítica dos mecanismos — 09/11/2026
**Status:** primeira rodada realizada; `partial_evidence`, ainda não homologação final de projetos. [Relatório de confronto documental](RELATORIO_G05D_DOCUMENTAL_2026_11_09.md) e [matriz de dez chaves](MATRIZ_EVIDENCIAS_G05D_2026_11_09.csv). [QA GitHub Actions 42563455585](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42563455585): `success`, dez de dez valores TCESP por chave/ano coincidentes em centavos; matriz SHA `04fdb0b0867e1e9386dcf50108c1cce1d1b3a8649fae2684b8693488b4ea6036`.
- **São José do Rio Preto:** Prefeitura programa 9 −R$ 171,98 milhões nominais (2024–2025); ações 1003 e 1004 com quedas de R$ 72,42 e R$ 60,60 milhões; correspondência temática no PPA, porém não nos contratos individuais. SeMAE programa 31 −R$ 13,09 milhões; o parecer ARES-PCJ 34/2025 confirma investimentos físicos executados/em andamento, sem vinculação exata a cada liquidação TCESP.
- **Olímpia:** programa 45 (Concessão Água e Esgoto) R$ 46,67 milhões liquidados em 2024 e sem lançamento na mesma chave em 2025. Contrato de concessão Sabesp nº 398/2023 confirmado; possível efeito extraordinário/codificação requer identificação de destino e contratos. Programa 31 aumentou R$ 7,72 milhões; isso não prova recodificação do programa 45.
- **Monte Aprazível:** ação 1010 Pavimentação/Recapeamento −R$ 7,23 milhões nominais. Leis municipais 3.978 e 3.997/2024 confirmam créditos autorizados estaduais/federais para a mesma rubrica, mas não equivalem a liquidações nem explicam toda a queda.
- **Restrições:** dados do TCESP por programa são nominais; totais regionais reais usam IPCA médio anual. Distinguir ausência de lançamento e zero. Não atribuir quedas à LC 200/2023. Crawl2AI falhou tecnicamente; leitura foi efetuada por busca/recuperação web alternativa. As peças PDF foram examinadas textualmente, sem prova visual por screenshot.
**Próxima ação exata:** complementar G05-D com contratos/empenhos/medições dos programas prioritários, sobretudo Prefeitura SJR programa 9, SeMAE 31/1029, Olímpia 45/31 e Monte Aprazível 14/1010; vincular evidência de execução física a identificadores fiscais ou manter a conclusão limitada. Atualizar matriz, relatório e HANDOFF após cada lote, sem apagar a versão corrente. O G06 prospectivo não herda causalidade não demonstrada.


## G05-D — Diligência complementar contratual, 09/11/2026
**Relatório:** [`RELATORIO_G05D_DILIGENCIAS_COMPLEMENTARES_2026_11_09.md`](RELATORIO_G05D_DILIGENCIAS_COMPLEMENTARES_2026_11_09.md). **Matriz com sete novas evidências e status da prova:** [`G05D_DILIGENCIAS_COMPLEMENTARES_2026_11_09.csv`](G05D_DILIGENCIAS_COMPLEMENTARES_2026_11_09.csv).
- **Olímpia:** SEC Formulário 20-F 2024 Sabesp, Nota 11(i), documenta financiamento intragrupo de parcelas da outorga fixa e segunda parcela de R$ 80,707 milhões. Concessão confirmada; **não identificada a correspondência com R$ 46,67 milhões de liquidação TCESP no programa 45 em 2024**, nem com 2025. Portal municipal de obras oferece JSON 2024/2025, mas valor de contrato não é liquidação anual.
- **Monte Aprazível:** contrato de recapeamento 08/2024 (Coplan, R$ 1.772.387,89, vigência até 07/06/2025) e primeiro aditivo (R$ 395.147,63) identificados; adjudicação de concorrência 01/2024 (Inova, R$ 635.499,00) também. Não há ainda vinculação da despesa liquidada da ação 1010 com os contratos.
- **Rio Preto:** continuam faltando cruzamentos entre contrato, obra, empenho, ação 1003/1004 e liquidação TCESP; não adotar valores de contratação como execução.
- **Origem da documentação:** documentos oficiais e SEC; Crawl2AI apresentou falha técnica, adotada recuperação alternativa. PDFs de diário foram lidos textualmente, mas screenshot devolveu erro; não foi homologada inspeção visual das páginas.
**Status:** G05-D `in_progress`, ampliação documental **não causal**. **Próxima ação exata:** extrair registros de obras municipais de Olímpia, localizar os empenhos/medições do contrato 08/2024 em Monte Aprazível e os contratos/ações 1003/1004 da Prefeitura Rio Preto; comparar chaves e períodos, anotando ausência como não verificada, nunca zero. Consultar relatório e HANDOFF antes de repetir pesquisa.


## Verificação de consistência — 09/11/2026
Foi realizada conferência de readback do PR #219 e das matrizes, dos endpoints oficiais de obras de Olímpia e da evidência de concessão/contrato. Ver [VERIFICACAO_CONSISTENCIA_G05D_2026_11_09.md](VERIFICACAO_CONSISTENCIA_G05D_2026_11_09.md).
**Correção de gate:** a geometria EPSG:4674 já foi validada no G05-C (37/37); não permanece pendência cartográfica no G01. G01 mantém restrições demográficas da base DCA (população de 2025 repete 2024) e método IPCA médio anual.
**Cautela reforçada:** os JSON municipais de Olímpia para 2024/2025 retornam dados, mas incluem empreendimentos de outros anos e atualizações posteriores ao ano indicado; não são séries de liquidação de cada exercício e não têm correspondência financeira demonstrada com TCESP. G05-D permanece `in_progress` e o vínculo contrato–empenho–medição–liquidação não foi demonstrado.
**Próxima ação exata:** capturar versões e hashes dos JSONs, identificar processo/contrato por outras fontes, conferir empenhos e medições para os casos prioritários e atualizar matriz. Não recapturar DCA/TCESP.
