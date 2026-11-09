# Handoff — Fase I RMSJRP
**Data:** 2026-11-09 | **Branch de execução:** `audit/rmsjrp-fase-i-2026-11-09`.

## Entregas verificadas
- Fonte DCA estadual Drive 2013–2025 efetivamente lida, 481 pares RMSJRP e 351 combinações variável/ano de cobertura; `MATRIZ_COBERTURA_DCA_2013_2025.csv`.
- Fonte Gate C 2025 e Gate D 2025 efetivamente lidas. 774 valores DCA vs Gate C conciliados (zero divergências acima de R$ 0,01); `MATRIZ_COBERTURA_LEGAL_2025.csv`.
- Sub-regiões PDUI: São José do Rio Preto 14; José Bonifácio 11; Tanabi 6; Nova Granada 6; mapeadas por IBGE em `MUNICIPIOS_SUBREGIOES_2025.csv`.
- Relatório substantivo: `RELATORIO_FASE_I_2026_11_09.md`.
- TCESP: workflow read-only executado com sucesso no run `42559912064` e artifact `13648618790`. R2 readback SHA aprovado para três produtos privados. 111/111 investimentos liquidados observados e 111/111 pares TCESP × DCA com diferença zero centavos. Recurso permanente: `rmsjrp/fase1/2026_11_09/tcesp/`.
- Nenhum arquivo de origem alterado; nenhuma publicação realizada.

## Bloqueadores e pendências
- TCESP confirmado; não executar nova coleta. Verificar somente as fontes legais faltantes por cobertura variável (RREO 18/37, DTP 18/37, DC/RCL 17/37, DCL 18/37; CAPAG 37/37).
- Bases RREO/RGF têm cobertura de 17–18/37 para vários indicadores legais em 2025; verificar complementos internos. CAPAG 37/37.
- Deflator, população por ano, geometria e CRS para fechar G01.
- Hash DCA recalculado da cópia binária R2 e aprovado no run `42559912064`; a leitura de Drive foi textual.

## Próxima ação exata
Após incorporar o PR desta Fase I, começar G04 com exame interno das ausências RREO/RGF, definição do IPCA médio anual e base de setembro/2026, série populacional e geometria EPSG:4674. Não recolher DCA/TCESP. Atualizar relatório e status ao encerrar cada gate; verificar PR/commit na main.


## Continuidade após G04 — 09/11/2026
- **Execução:** [run 42561177880](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561177880) `success`, artifact `13648798649`; script `editorial/rmsjrp/build_indicadores_g04.py`; `IPCA_MEDIA_ANUAL_SET2026.csv`.
- **Resultados:** 481 séries município-ano e 65 território-ano (quatro sub-regiões + total RMSJRP), 2013–2025; ausência preservada. Receitas correntes 2023/2024/2025: R$ 5.928.863.624,96 / 6.618.138.707,79 / 7.252.878.267,79 nominais. Investimentos liquidados nominais R$ 444.230.252,48 / 480.737.206,37 / 208.056.124,00; investimentos reais set/2026 R$ 513.232.108,92 / 532.167.431,30 / 219.312.039,99.
- **Persistência:** R2 privado `rmsjrp/g04/2026_11_09/`, três objetos com hashes/readback no `RELATORIO_G04_2026_11_09.md`. Não reconstruir dados de fonte externa.
- **Ressalvas:** fatores do IPCA média anual reproduzidos do Lote 17 RMRP (referência setembro/2026 7695,82); denominação populacional 2025 é repetição numérica de 2024 para 37/37 municípios, não nova estimativa observada. Falta definir cartografia métrica EPSG:4674 e ampliar RREO/RGF apenas a partir de acervo disponível, se possível.
- **Próxima ação:** executar G05 em lotes: tabela 2023–2025 regional e por quatro sub-regiões; explorar contribuições municipais para variação real 2023–2025; mapas somente com CRS comprovado; nenhuma atribuição causal antes de investigação. Iniciar novo chat lendo este arquivo, README e relatório G04, verificar commit atual de `main` e readback R2; após lote atualizar todos os registros de estado.


## Continuidade após G05-A/B/C — 09/11/2026
- **GitHub Actions comprovados:** [G05-A run 42561961530](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561961530), [G05-B run 42562212589](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562212589) e [G05-C run 42562450625](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562450625), todos `success`, artifacts `13649986299`, `13649449797` e `13650151673`.
- **Dados e QA:** R2 privado `rmsjrp/g05/2026_11_09/`: 15 território-ano 2023–2025, 15 variações territoriais, 111 contribuições municipais, 6 comparações polo/demais e 3 contagens de tendência; todos com paridade 111 pares TCESP/DCA. 2024–2025 investimento real regional −R$ 312,86 milhões; 29 municípios com queda, oito com aumento; polo −R$ 220,83 milhões. Fonte IPCA: média anual RMRP Lote 17, preços setembro/2026.
- **Programas e ações:** scripts e CSVs auditados 4.884 movimentos por chave órgão/programa/ação, 480 movimentos ranqueados. R2 `rmsjrp/g05/2026_11_09/programas_acoes/`, três arquivos com hashes descritos no relatório G05. Atenção a recodificações e estágios; cifras programáticas são NOMINAIS, enquanto quadro metropolitano é REAL.
- **Cartografia:** IBGE malha SP municipal 2022 (`SP_Municipios_2022.zip`, SHA `341664fdb610df9b92a8f01546e1a83474135cf686c4dcf6c2e0ea91552b0013`), CRS da PRJ EPSG:4674, 37/37 geometrias válidas, sem simplificação; dois mapas PNG e GeoJSON recortado no R2 `rmsjrp/g05/2026_11_09/cartografia/`. QA espacial de CRS, validade e cardinalidade, não auditoria topológica integral. Conferência visual realizada.
- **Relatório de resultados e hashes:** [`RELATORIO_G05_LOTE_A_2026_11_09.md`](RELATORIO_G05_LOTE_A_2026_11_09.md), incluindo complementos G05-B/C.
- **Situação atual:** G05-A/B/C QA técnico aprovado; **G05-D ainda PENDENTE**. A análise substantiva dos programas/ações mais relevantes deve confrontar contas, orçamentos, obras, contratos e classificações antes de afirmar causas. Especial atenção a programas Prefeitura SJR 9, Olímpia 45 e SEMAE SJR 31.
- **Ação exata seguinte:** revisar possível recodificação e documentos primários dos programas principais; após confronto, produzir análise G05-D; integrar mapas junto às respectivas seções do relatório, sem mover todas as figuras para atlas isolado; atualizar README, STATUS e manifesto. Não iniciar G06 ou fichas sem qualificar conclusões como preliminares.
