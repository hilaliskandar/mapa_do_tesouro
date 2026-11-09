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
