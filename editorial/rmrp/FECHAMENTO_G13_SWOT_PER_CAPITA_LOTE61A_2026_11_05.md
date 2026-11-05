# RMRP — G1-3 — QA dos indicadores de investimento real per capita nas 34 SWOT (05/11/2026)

**Corpus textual auditado:** `SWOT_CONSOLIDADAS_ISS_ICMS_LOTE61A.md` (34 matrizes municipais), não uma leitura binária do DOCX congelado do Lote 98. A coincidência textual entre esse corpus e o DOCX final deve ser comprovada antes do aceite editorial da versão-base.

**Fonte numérica:** `G13_SERIE_REAL_INVESTIMENTOS_DESPESAS_2023_2025_34_MUNICIPIOS.csv`, 102 registros município-ano da DCA Siconfi, IPCA de média anual, preços de setembro de 2026, população declarada na DCA.

## Resultado da auditoria dirigida
- **34/34** matrizes identificadas e associadas a código municipal, sem perda de municípios.
- **13** alegações explícitas de *variação do investimento real per capita entre 2023–2025* identificadas por critério textual restrito.
- **13/13** compatíveis com a série recalculada, tolerância inferior a 0,02 ponto percentual, considerando o arredondamento para centavos dos valores reais por habitante na matriz-base.
- **21** matrizes sem alegação capturada por esse padrão textual: **não testadas para esse indicador**, não devem ser apresentadas como conformes.
- Desvio absoluto máximo observado entre as alegações capturadas: **0.00661** ponto percentual.
- Os testes confirmam reprodução aritmética de números publicados sob esse método, **não** homologam a origem e o regime da população declarada, nem conferem outros percentuais e argumentos das SWOT.

## Controle da população
A população no arquivo DCA repete exatamente os valores de 2024 em 2025 para 34/34 municípios; de 2023 para 2024, nenhum valor municipal é igual. Essa repetição é indício de convenção/carga populacional distinta da série anual IBGE; **não implica que a população tenha ficado estável em termos demográficos**. A publicação de tendência por habitante deve documentar o denominador escolhido. O arquivo `FINBRA_PARTE5_parametros_temporais_IPCA_populacao_2013_2025` contém série IBGE metodologicamente diferente e deve ser cotejado de forma nominativa.

## Encaminhamento
1. Confirmar no próprio Lote 98, por leitura do DOCX congelado, se as 13 afirmações permanecem no texto final e se houve outras variações redigidas com expressões alternativas.
2. Rever a coerência narrativa de todas as 34 matrizes, incluindo indicadores de receita, posição relativa e a direção 2023→2024→2025, sem inferir causalidade de variação.
3. Decidir e registrar denominadores demográficos do Volume II; produzir teste de sensibilidade DCA vs IBGE antes do aceite.
4. Não editar o Lote 98 até encerrar o gate de consistência.
 
[Planilha CSV de auditoria completa](G13_AUDITORIA_SWOT_PER_CAPITA_LOTE61A_34_MUNICIPIOS.csv)
