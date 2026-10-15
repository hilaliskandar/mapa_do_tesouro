# Auditoria das formulas editoriais — RM Jundiai (2025)

Data da auditoria: 2026-10-14.

Fonte: GitHub Actions run 37917365471; artifact 11610521760; SHA-256 3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e; release v0.4.0.

Escopo: sete municipios, seis indicadores relativos e 42 checagens de indicador/numerador/denominador no exercicio 2025.

Resultado: 35 verificacoes reproduziram a razao publicada com tolerancia absoluta inferior a 1e-8. Sete nao sao testaveis no payload porque `tributos_imobiliarios` nao aparece como agregado autonomo no contexto municipal, embora `tributos_imobiliarios_pct_receita_tributaria` esteja presente. Zero divergencias entre as 35 comparacoes calculaveis.

Advertencia: as formulas descritivas no catalogo exprimem porcentagem como 100 vezes a razao; os valores no payload sao fracoes. A conversao para exibicao exige multiplicacao por 100. A paridade aritmetica nao substitui auditoria da conta de origem, comprovacao do crosswalk temporal ou validacao dos demonstrativos legais.

Para 2021–2024, os indicadores `receita_tributaria_pct_receita_corrente` e `investimento_pct_receita_corrente` constam como observados mesmo quando as contas primarias DCA correspondentes aparecem como nao aplicaveis no JSON editorial. Portanto, ainda nao ha prova da reconstruibilidade historica apenas com a API publica.

O agregado `despesa_territorial` observado por `strict_complete` possui cobertura 1/7 em 2025 e nao deve originar soma regional.

Situacao editorial: caderno analitico v0.3 produzido em ambiente de trabalho, nao publicado. Pendente revisar documentacao de escala, componente imobiliario, historico das razoes, snapshot CAPAG e QA editorial.
