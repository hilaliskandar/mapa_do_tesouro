# RMRP — QA da prova de 72 páginas — 29/10/2026

## Evidência verificada
Origem: exportação PDF da cópia de trabalho Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`; 72 páginas. Auditoria automatizada por PyMuPDF e inspeção visual renderizada das páginas 39 e 40.

### Cartografia
16 páginas com uma imagem cartográfica e a legenda identificada na **mesma página**: 5, 7, 11, 15, 17, 18, 20, 31, 32, 34, 35, 36, 37, 38, 39 e 40. As 16 imagens sobreviveram à repaginação, sem perda detectada nessa verificação. Esse controle garante co-localização, não certifica a leitura impressa de todas as classes.

### Ocorrência editorial concreta — páginas 39–40
No trecho **“Exemplos de trajetórias contrastantes”**, os elementos que deveriam formar um quadro comparativo não são uma tabela nativa Google Docs. São nove parágrafos comuns consecutivos: cabeçalho partido entre dois parágrafos e seis linhas municipais sem delimitação de colunas. A linha **Sertãozinho (+18,8%, +29,0%, −48,3%)** ficou isolada no início da página 40; as demais cinco linhas estão na página 39. O problema está presente na renderização, não apenas no fluxo textual. A figura de coeficiente de oscilação segue na página 40.

**Correção proposta:** converter este trecho para tabela nativa de quatro colunas (Município; Saúde — variação real; Educação — variação real; Investimentos — variação real), com seis linhas: Dumont (+30,2%; +63,7%; +255,0%); Batatais (+21,7%; +33,3%; +196,7%); Mococa (+11,4%; +24,4%; +181,7%); Orlândia (+54,8%; +51,4%; +163,2%); Altinópolis (+23,9%; +37,9%; −68,5%); Sertãozinho (+18,8%; +29,0%; −48,3%). Preservar os valores, verificar agrupamento do quadro e página, repetir cabeçalho se houver quebra legítima. Realizar operação com índices nativos e revisão protegida, seguida de nova exportação e inspeção.

### Outros controles
- As páginas 34–38 demonstram agrupamento das figuras da seção de despesas; continuam necessárias inspeções visuais de impressão das legendas cromáticas.
- No mapa da página 39, a classe intermediária continua atravessando zero (−10,6% a +16,7%); preservar ressalva até reconstrução vetorial baseada em valores e geometria.
- Nas páginas 41–42 ocorre continuação de tabela de evolução das médias trienais com repetição de cabeçalho; não presumir defeito somente pela divisão entre páginas.
- Nenhuma alteração no Google Docs decorrente desta rodada. Nenhuma publicação.

**Status:** QA estrutural/cartográfico de 72 páginas realizado; ocorrência de quadro editorial comprovada; correção e nova prova pendentes.
