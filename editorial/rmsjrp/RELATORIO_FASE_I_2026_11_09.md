# RMSJRP — relatório de execução da Fase I (G00–G03)
**Data:** 2026-11-09. **Estado:** G00 e G02 com leitura direta e controles fiscais aprovados; G01 composição territorial aprovada, com cartografia analítica e deflator pendentes; G03 TCESP aprovado, indicadores legais disponíveis com cobertura parcial explicitada. Este documento não homologa todos os dados legais nem autoriza nova publicação.

## Fontes efetivamente recuperadas neste gate
1. Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, `DCA_SP_645_2013_2025_CANONICO.csv`, conteúdo CSV lido integralmente pelo conector (8.385 linhas de dados de 2013–2025, 645 municípios/ano). Hash canônico `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5` **recalculado e conferido por readback independente da cópia R2 no run 42559912064**; não se afirma rehash binário do download textual do Drive.
2. Drive ID `12XfaN7ati-wGgw_a5puwechp7ipFdWRG`, `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`, conteúdo tabular lido e selecionados 37 municípios.
3. Drive ID `1wYnFB8Dg000qrBM1do8pe083FlqWzHDk`, `FINBRA_SP645_INDICADORES_2025_GATE_D.xlsx`, conteúdo tabular lido, selecionados 37 municípios.
4. GitHub `data/catalogs/territorial_universes_sp_2025.yml`, `data/catalogs/publication_universes_sp.yml`, `governance/HOMOLOGACAO_TCESP_R2_SQLITE_API_V2_20261026.md`, documentos de integração RMJ/RMRP. **A documentação histórica foi seguida de leitura direta e confronto dos objetos privados R2, pelo run 42559912064**.
5. Legislação estadual LC 1.359/2021: https://www.al.sp.gov.br/repositorio/legislacao/lei.complementar/2021/lei.complementar-1359-24.08.2021.html. Sub-regiões: PDUI RMSJRP Produto P5, setembro/2022, https://rmsjrp.pdui.sp.gov.br/wp-content/uploads/P5-21-9-22.pdf . A subdivisão é instrumento analítico do PDUI, não criada expressamente pelo artigo 3º da LC.
6. Matrizes geradas no GitHub sob `editorial/rmsjrp/`: `MUNICIPIOS_SUBREGIOES_2025.csv`, `MATRIZ_COBERTURA_DCA_2013_2025.csv`, `MATRIZ_COBERTURA_LEGAL_2025.csv` e `STATUS_GATES.csv`.

## G00 — inventário de reuso
- FINBRA/DCA 2013–2025: dados reais **acessíveis no Drive**, sem extração externa.
- Gate C multifuentes e Gate D indicadores 2025: dados reais **acessíveis no Drive**, não somente descritos no README.
- R2 TCESP estadual 2023–2025: três manifestos e seus objetos de agregação efetivamente baixados e conferidos por SHA-256 no run 42559912064; a matriz regional e o confronto DCA foram preservados com readback no prefixo privado `rmsjrp/fase1/2026_11_09/tcesp/`.
- Componentes RREO/RGF/CAPAG: os campos presentes na planilha Gate C 2025 foram lidos, com cobertura regional demonstrada; indicadores legais ausentes permanecem NA e requerem decisão seletiva sobre fonte/snapshot antes de coletar.
- Nenhuma nova consulta estadual Siconfi ou TCESP foi realizada nesta fase.

## G01 — validação territorial
- Código do universo: `RM_SAO_JOSE_RIO_PRETO`; 37 códigos IBGE distintos e 37 nomes presentes no Gate C, sem duplicatas e sem município inesperado.
- Composição confirmada contra LC 1.359/2021; grafia institucional no texto pode diferir da grafia normalizada do Gate C (ex.: Bady Bassitt).
- Quatro agrupamentos definidos no PDUI: São José do Rio Preto (14), José Bonifácio (11), Tanabi (6), Nova Granada (6); soma 37. Relação nominal e códigos em `MUNICIPIOS_SUBREGIOES_2025.csv`.
- Pendente G01: verificar geometria/CRS EPSG:4674 e definir a série populacional e a base de preços constantes. `populacao_dca` existe em 478/481 pares, mas sua adequação a todos os exercícios comparáveis precisa ser examinada. Não calcular valores reais sem definir deflator.

## G02 — FINBRA/DCA 2013–2025
- 37 municípios × 13 exercícios = **481 pares município-ano**, 481 presentes e 481 chaves únicas; nenhum par ausente; todas as linhas com `qa_issue_count=0` no snapshot.
- Matriz de **351 combinações variável × ano**, com observados, ausentes e percentual; ausência nunca convertida em zero.
- Cobertura consolidada: receita corrente 478/481; receita tributária 477/481; IPTU 476/481; ITBI 464/481; ISS 467/481; despesa corrente liquidada 478/481; investimentos liquidados 477/481; transferências de capital 430/481. Os campos de cobertura parcial como inversões financeiras, juros, habitação, crédito e saneamento devem permanecer faltantes quando vazios.
- Em 2023–2025, receita corrente, receita tributária e investimentos liquidados: **111/111 pares** por indicador.
- Lacunas nas três variáveis centrais: Onda Verde/2014 — receita corrente, tributária e investimentos; Tanabi/2015 — as três; Poloni/2017 — tributária e investimentos; Monte Aprazível/2018 — as três. São **11 células ausentes** em quatro pares, não 11 pares ausentes.
- Crosscheck **774 valores** não vazios de DCA 2025 vs Gate C 2025, por código IBGE/campo, tolerância 1 centavo: **zero divergências** e zero conflitos de preenchimento nas variáveis do confronto. Isso comprova fidelidade entre os dois snapshots consultados, não sua auditoria independente contra demonstrativos primários.

## G03 — camadas legais e TCESP
A base Gate C 2025 contém 37/37 classificações CAPAG e 37/37 indicadores 1,2,3; as notas oficiais são do snapshot, não novos cálculos de CAPAG. Campos legais observados:
- RREO/RCL anual: 18/37;
- RGF despesa total com pessoal, denominador legal e DTP/RCL: 18/37 cada;
- RGF caixa líquido após restos a pagar não processados: 18/37;
- RGF02 DC/RCL: 17/37; DCL/RCL: 18/37;
- `rgf02_rcl_bruta`: 37/37, **não intercambiável automaticamente** com RREO RCL anual e denominador legal de DTP.
- O Gate D reproduz os campos derivados para os observados; campos vazios não foram imputados.

TCESP: leitura direta dos três snapshots privados R2, SHA dos manifestos e nove agregados conferidos, recorte 37 × 3 = **111/111 pares com investimentos liquidados**. Totais dos investimentos liquidados do grupo 44: 2023 **R$ 444.230.252,48**, 2024 **R$ 480.737.206,37**, 2025 **R$ 208.056.124,00**. Agregados por município/mês/estágio, programa e ação reconciliados em centavos. O DCA canônico foi recuperado adicionalmente do R2, hash validado, e **111 valores municipais-anuais TCESP × DCA comparados, zero divergências** (precisão centavos). Ver run [42559912064](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42559912064) e artefato `13648618790`. Script `qa_tcesp_r2_regional.py` e workflow `.github/workflows/rmsjrp-fase1-r2-check.yml`. Três arquivos derivados persistidos no R2 privado sob `rmsjrp/fase1/2026_11_09/tcesp/` e readback SHA aprovado: `RESULTADO_TCESP_R2.json` SHA `3672d3254671c3557b0fb6ecd05cb8540d693de5b8a59e7885edd98fc36e8497`; `MATRIZ_TCESP_RMSJRP_2023_2025.csv` SHA `5aa597f2a4f18caebdc8b652113f4745953919abe6c6c201ab9c29fc0f509a53`; `CONFRONTO_TCESP_DCA_2023_2025.csv` SHA `07f305bb0137c5b558c1fb07f7cd89a5d1d44828f496ac9197d43ce08953a0c6`. O artifact do Actions é temporário; o R2 é o acervo persistente. Esse confronto demonstra equivalência nos 111 pares deste recorte e dos conceitos testados; não estende automaticamente a equivalência a outras despesas ou regiões.

## Encaminhamento após a verificação
1. **G00 — evidências de fontes recuperadas:** DCA e Gate C/D no Drive, DCA e TCESP com readback independente no R2, QA reproduzível. O inventário permanece aberto somente para fontes legais complementares que ampliem a cobertura, não para reabrir coleta geral.
2. **G01 — recorte territorial validado:** 37 códigos e quatro sub-regiões do PDUI conciliados. A cartografia SP645 (`governance/QA_SP645_CARTOGRAPHY.md`) possui 645 polígonos sem geometria nula e é aprovada para visualização web, mas **não declara CRS explícito**. Para mapas analíticos e métricos deve ser utilizada geometria documentada em EPSG:4674. A seleção do IPCA médio anual — preços de setembro/2026 conforme comparabilidade com RMRP — depende da homologação dos fatores exatos no G04.
3. **G02 — aprovado quanto à estrutura, preenchimento e paridade 2025 Gate C**, com as 11 células vazias documentadas, sem imputação.
4. **G03 — TCESP aprovado** (111/111, 0 divergências com DCA neste recorte; readback privado). **RREO/RGF em cobertura parcial**, não considerar 19 ausências como zero. CAPAG 37/37; a complementação seletiva dos indicadores legais fica documentada como pendência para G04/G06, sem bloquear a utilização dos dados completos disponíveis.
5. Próxima etapa G04: definir deflatores de fluxos anuais, denominadores populacionais, calcular e validar indicadores; antes, verificar se snapshots RREO/RGF mais completos já existem, sem recolher o que está homologado.

**Síntese:** Fase I executada e fonte nuclear DCA/TCESP recuperada com QA; limitações legais, monetárias e cartográficas explicitadas. Não representa homologação de cenários, textos municipais, imagens ou publicação.
