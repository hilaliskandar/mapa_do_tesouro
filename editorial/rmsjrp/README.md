# RMSJRP — continuidade operacional do estudo fiscal
**Atualizado:** 2026-11-09. **Estado:** Fase I executada com leitura direta de fontes; G00/G02/G03 QA aprovado para os componentes observados e G01 parcialmente pendente de cartografia métrica e deflator. Nenhum texto municipal ou cenário homologado.

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
**G04 — Indicadores e cálculos**, após Fase I. Foram lidos DCA 2013–2025 (481/481 pares), Gate C/D 2025 (37 municípios), TCESP R2 2023–2025 (111/111 liquidados), e 111/111 pares DCA × TCESP com diferença zero. Run 42559912064, R2 privado readback. Ver [relatório G00–G03](RELATORIO_FASE_I_2026_11_09.md), [handoff](HANDOFF.md) e [matrizes de cobertura](MATRIZ_COBERTURA_DCA_2013_2025.csv). Indicadores RREO/RGF seguem parciais e sem imputação.

## Quadro de gates
| Gate | Conteúdo | Status inicial |
|---|---|---|
| G00 | Inventário de reuso, versão e hash | qa_pass |
| G01 | Território, sub-regiões, população, IPCA | in_progress — território aprovado; geometria e deflator pendentes |
| G02 | Filtro e QA DCA 2013–2025 | qa_pass |
| G03 | TCESP 2023–2025, RREO/RGF/CAPAG | qa_pass — cobertura legal parcial documentada |
| G04 | Indicadores, cálculos e reprodutibilidade | not_started |
| G05 | Diagnóstico territorial, tabelas e mapas | not_started |
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
