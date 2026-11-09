# RMSJRP — relatório de execução da Fase I (G00–G03)
**Data:** 2026-11-09. **Estado:** G02 com auditoria estrutural e confronto de valores aprovados; G00/G01 parcialmente concluídos; G03 em conferência. Este documento não homologa todos os dados legais nem autoriza nova publicação.

## Fontes efetivamente recuperadas neste gate
1. Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, `DCA_SP_645_2013_2025_CANONICO.csv`, conteúdo CSV lido integralmente pelo conector (8.385 linhas de dados de 2013–2025, 645 municípios/ano). Hash documentado no projeto: `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`; **hash bruto não foi recalculado nesta execução**.
2. Drive ID `12XfaN7ati-wGgw_a5puwechp7ipFdWRG`, `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`, conteúdo tabular lido e selecionados 37 municípios.
3. Drive ID `1wYnFB8Dg000qrBM1do8pe083FlqWzHDk`, `FINBRA_SP645_INDICADORES_2025_GATE_D.xlsx`, conteúdo tabular lido, selecionados 37 municípios.
4. GitHub `data/catalogs/territorial_universes_sp_2025.yml`, `data/catalogs/publication_universes_sp.yml`, `governance/HOMOLOGACAO_TCESP_R2_SQLITE_API_V2_20261026.md`, documentos de integração RMJ/RMRP. **A leitura documental da persistência TCESP não é uma leitura de seus objetos R2**.
5. Legislação estadual LC 1.359/2021: https://www.al.sp.gov.br/repositorio/legislacao/lei.complementar/2021/lei.complementar-1359-24.08.2021.html. Sub-regiões: PDUI RMSJRP Produto P5, setembro/2022, https://rmsjrp.pdui.sp.gov.br/wp-content/uploads/P5-21-9-22.pdf . A subdivisão é instrumento analítico do PDUI, não criada expressamente pelo artigo 3º da LC.
6. Matrizes geradas no GitHub sob `editorial/rmsjrp/`: `MUNICIPIOS_SUBREGIOES_2025.csv`, `MATRIZ_COBERTURA_DCA_2013_2025.csv`, `MATRIZ_COBERTURA_LEGAL_2025.csv` e `STATUS_GATES.csv`.

## G00 — inventário de reuso
- FINBRA/DCA 2013–2025: dados reais **acessíveis no Drive**, sem extração externa.
- Gate C multifuentes e Gate D indicadores 2025: dados reais **acessíveis no Drive**, não somente descritos no README.
- R2 TCESP estadual 2023–2025: documentação de persistência e QA anterior localizada; acesso real ao bucket privado depende de readback em GitHub Actions. Não classificar como homologação regional enquanto esse teste não terminar.
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

TCESP: reuso de armazenamento privado no bucket `financas-municipais-sp-canonico`, prefixos anuais documentados; exige leitura e verificação dos hashes do manifesto. Foi implementado script read-only `qa_tcesp_r2_regional.py` e workflow `.github/workflows/rmsjrp-fase1-r2-check.yml`, acionável na branch de auditoria. O script deve produzir, **quando aprovado**, `MATRIZ_TCESP_RMSJRP_2023_2025.csv` e `RESULTADO_TCESP_R2.json` como artifact temporário do Actions; a existência do código/workflow não garante a presença dos resultados. O fechamento de G03 depende do resultado do run e do relatório de paridade agregados por município/mês/estágio, programa e ação.

## Próximos critérios de encerramento
1. Registrar resultado final do workflow R2, run, cobertura 111 pares, erros de leitura/QA e local dos artefatos. Não confundir workflow criado, run executado e run aprovado.
2. Verificar se snapshots RREO/RGF adicionais já existem em R2/Drive para os 19 municípios sem RCL e os outros campos legais; não iniciar nova coleta antes de pesquisa interna.
3. Validar geometria/CRS, base populacional e deflator para encerrar G01.
4. Recalcular hash exato do CSV DCA por leitura bruta, ou manter ressalva expressa; arquivar manifestos de SHA e relatório.
5. Só avançar para G04 com G03 documentado, separando campos faltantes não bloqueantes de lacunas essenciais.

**Status:** G00 em andamento; G01 em andamento; G02 QA de estrutura/confronto aprovado; G03 em andamento/bloqueado na leitura externa e lacunas legais. Não declarar Fase I integralmente concluída sem esses controles.
