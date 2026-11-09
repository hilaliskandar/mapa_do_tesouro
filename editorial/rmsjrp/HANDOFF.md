# Handoff — Fase I RMSJRP
**Data:** 2026-11-09 | **Branch de execução:** `audit/rmsjrp-fase-i-2026-11-09`.

## Entregas verificadas
- Fonte DCA estadual Drive 2013–2025 efetivamente lida, 481 pares RMSJRP e 351 combinações variável/ano de cobertura; `MATRIZ_COBERTURA_DCA_2013_2025.csv`.
- Fonte Gate C 2025 e Gate D 2025 efetivamente lidas. 774 valores DCA vs Gate C conciliados (zero divergências acima de R$ 0,01); `MATRIZ_COBERTURA_LEGAL_2025.csv`.
- Sub-regiões PDUI: São José do Rio Preto 14; José Bonifácio 11; Tanabi 6; Nova Granada 6; mapeadas por IBGE em `MUNICIPIOS_SUBREGIOES_2025.csv`.
- Relatório substantivo: `RELATORIO_FASE_I_2026_11_09.md`.
- TCESP: workflow somente leitura e script criados para recuperar R2; conferir último run e artifact antes de atualizar o status.
- Nenhum arquivo de origem alterado; nenhuma publicação realizada.

## Bloqueadores e pendências
- Conferir run `RMSJRP Fase I - QA read-only TCESP R2` e verificar reais 111 pares; falhas de runner devem ser corrigidas na branch.
- Bases RREO/RGF têm cobertura de 17–18/37 para vários indicadores legais em 2025; verificar complementos internos. CAPAG 37/37.
- Deflator, população por ano, geometria e CRS para fechar G01.
- Hash original DCA conhecido por inventário, ainda sem nova leitura binária independente.

## Próxima ação exata
Consultar último run do workflow R2 da branch, ler jobs/logs e validar artifact; se falhar, corrigir erro reproduzível. Depois aprofundar as 19 ausências RREO/RGF via snapshots privados já existentes, antes de abrir coleta externa. Atualizar relatório e status; registrar PR, commit e readback dos arquivos na main após QA.
