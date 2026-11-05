# RMRP — G16: auditoria dos oito mapas temáticos do Volume II, Lote 98
**Data:** 05/11/2026. **Versão de referência:** DOCX congelado, SHA-256 `fffd21bb65251d89caee484c2cabf7b813a7884760f60943c95919e608249df4`. Nenhum original alterado.

## Resultado
Foram reproduzidos os oito indicadores territoriais a partir da FINBRA/DCA canônica SP645 e conferidas as cores das 34 feições municipais em cada imagem, mediante geometria IBGE 2022, EPSG:4674, chaves `CD_MUN` textuais e limites publicados nas legendas. **272/272 correspondências município × mapa × classe conformes**, sem erros de classificação segundo o limite exibido.

- Mapa 1: IPTU principal + ISS principal + ITBI principal sobre receita corrente bruta de 2025 — 34/34 conforme.
- Mapa 2: FPM cota mensal + ICMS + IPVA sobre receita corrente bruta de 2025 — 34/34 conforme.
- Mapa 3: FPM cota mensal por habitante em 2025 — 34/34 conforme.
- Mapa 4: Receita corrente por habitante em 2025 — 34/34 conforme.
- Mapa 5: Investimento liquidado por habitante em 2025 — 34/34 conforme.
- Mapa 6: Variação real do investimento médio anual, triênios 2020–2022 e 2023–2025 — 34/34 conforme.
- Mapa 7: Coeficiente de variação dos investimentos reais 2021–2025 — 34/34 conforme.
- Mapa 8: ISS principal por habitante em 2025 — 34/34 conforme.

## Achados metodológicos
**Denominador:** os limites dos mapas 3, 4, 5 e 8 são reproduzidos exatamente com a população estimada **IBGE SIDRA 6579 em 2025**, anteriormente arquivada em `G13_AUDITORIA_POPULACAO_DCA_VS_IBGE_2024_2025.csv`. Não coincidem quando se usa `populacao_dca`, que é o denominador de tabelas e SWOT do Volume II. Portanto, cada mapa é internamente consistente, mas a diversidade de denominadores entre os componentes do relatório exige nota metodológica e harmonização editorial justificada. Nenhuma pesquisa populacional adicional foi feita.

**Deflação:** mapas 6 e 7 utilizam IPCA de dezembro de cada exercício; indicadores longitudinais de SWOT utilizam IPCA médio anual. O método de dezembro do mapa 15 já foi auditado no G15.

**Precisão:** no mapa 7, o quantil de 80% recalculado é 59,9496634%, cujo arredondamento convencional a uma casa é 59,9%, ante 60,0% na legenda. A diferença não altera as classes municipais. No mapa 3, Serra Azul registra FPM per capita aproximadamente R$ 2.286,64 e pertence à classe até R$ 2.287 conforme a legenda arredondada; a utilização de limites não arredondados produz classificação artificialmente diferente para esse caso de fronteira.

## Alcance e reserva
O procedimento usa a classe da cor de preenchimento em um ponto interior da geometria municipal, conferida contra as quatro quebras impressas; **não** é inspeção exaustiva de todos os pixels, nem homologação das seis figuras complementares, da paginação ou de interpretações jurídicas. O Lote 98 permanece intacto.

**Encaminhamento:** não refazer mapas conformes; explicitar a série de população e o método de IPCA em cada seção, corrigir apenas rotulagem/precisão comprovadamente necessária e conferir as imagens 9 a 14 e remissões na versão editorial derivada.

**Evidência:** pacote técnico local `RMRP_G16_AUDITORIA_OITO_MAPAS_2026_11_05.zip` com 272 testes nominativos, indicadores e scripts.
