# RMSJRP — continuidade operacional do estudo fiscal
**Atualizado:** 2026-11-09. **Estado:** planejamento registrado em branch, ainda sem homologação da base regional ou texto final.

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
**G00 — INVENTÁRIO E RECUPERAÇÃO DE FONTES.** Nenhum gate foi executado pela simples criação dos documentos. A primeira ação operacional deverá verificar HEAD/main/PR, ler inventário de fontes, confirmar objetos no Drive/R2 e registrar as variáveis efetivamente acessíveis. Não realizar coleta externa antes da matriz de lacunas.

## Quadro de gates
| Gate | Conteúdo | Status inicial |
|---|---|---|
| G00 | Inventário de reuso, versão e hash | not_started |
| G01 | Território, sub-regiões, população, IPCA | not_started |
| G02 | Filtro e QA DCA 2013–2025 | not_started |
| G03 | TCESP 2023–2025, RREO/RGF/CAPAG | not_started |
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
**2026-11-09 — Planejamento:** arquivo detalhado criado em ramo documental, sem cálculo, extração ou publicação. **Próxima ação exata:** executar G00, cruzando a lista dos 37 códigos com os manifests DCA, TCESP, RREO, RGF e CAPAG; gerar `INVENTARIO_REUSO.md` e `MATRIZ_COBERTURA.csv`, com evidencia de readback; em seguida proceder a G01.
