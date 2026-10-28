# Inventário dos 16 mapas temáticos RMRP — 28/10/2026

**Fonte integral verificada:** [volume cartográfico RMRP de 19/10/2026](https://drive.google.com/file/d/10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN/view), PDF de 9 páginas, quatro mosaicos nas páginas 2, 3, 6 e 7, cada matriz 3000×2500 pixels. Fonte interna dos mapas: FINBRA/Siconfi e IBGE, exercício 2025, com indicadores temporais quando especificado.

**Procedimento realizado:** os quatro objetos de imagem foram extraídos diretamente do PDF e subdivididos por quadrantes, sem interpolação ou reamostragem. Criados 16 PNG de 1500×1250 pixels, manifesto JSON com SHA-256 individual, prova PDF de 16 páginas e pacote ZIP. Artefatos de trabalho entregues na conversa de 28/10/2026. A divisão por quadrantes deve ser submetida a QA visual de cada mapa antes de incorporação ao Google Doc; os arquivos não são a edição homologada.

| Nº | Indicador conforme matriz | Tema editorial | Página matriz PDF |
|---:|---|---|---:|
| 1 | Receita corrente por habitante | Receitas | 2 |
| 2 | IPTU, ISS e ITBI na receita corrente | Receitas | 2 |
| 3 | FPM, ICMS e IPVA na receita corrente | Receitas | 2 |
| 4 | Saúde / receita corrente | Despesas | 2 |
| 5 | IPTU por habitante | Tributação | 3 |
| 6 | ISS por habitante | Tributação | 3 |
| 7 | ITBI por habitante | Tributação | 3 |
| 8 | FPM por habitante | Transferências | 3 |
| 9 | Despesa corrente por habitante | Despesas | 6 |
| 10 | Pessoal e encargos por habitante | Pessoal | 6 |
| 11 | Pessoal e encargos / receita corrente | Pessoal | 6 |
| 12 | Educação por habitante | Educação | 6 |
| 13 | Educação / receita corrente | Educação | 7 |
| 14 | Investimento liquidado por habitante | Investimentos | 7 |
| 15 | Evolução real dos investimentos entre triênios | Investimentos | 7 |
| 16 | Oscilação de investimentos 2021–2025 | Investimentos | 7 |

## Encaminhamento de integração
Os quatro mapas já ampliados na cópia nativa são: receita corrente por habitante, despesa corrente por habitante, investimento por habitante e IPTU por habitante. Os outros 12 devem ser integrados seletivamente ao texto segundo tema e associação com tabela ou argumento correspondente. **Não substituir os quatro existentes com os recortes recém-gerados sem conferir dimensões, legendas e paginação.** Manter o documento principal, a prova original e a cópia de trabalho intactos até a verificação visual de cada inserção.

Documento de trabalho: [RMRP — Trabalho cartográfico 16 indicadores — 28/10](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit).

**Portão editorial:** preservar 51 tabelas, 34 fichas e 16 indicadores; preferir dois mapas por bloco para leitura e economia de páginas, com legendas independentes e mesma fonte. A adequação de escala para impressão e a decisão de quais mapas terão figura própria precisam ser verificadas. Não foi efetuada inserção de imagem no Google Doc nem publicação.

## Regra cromática editorial aprovada — 28/10/2026
**Diretriz expressa:** adotar orientação cromática intuitiva **frio → quente** e escala ordenada, sem depender da legenda para reconhecer onde o indicador é menor ou maior. Para magnitude/razão positiva, usar **azul frio (baixo) → tons intermediários → vinho/vermelho quente (alto)**, assegurando contraste e legibilidade em impressão. Manter rótulos de cada classe e valores numéricos verificáveis; cores iguais em mapas diferentes representam posição relativa, e não montantes idênticos. `Sem dado` precisa de cor neutra inequivocamente distinta; nunca equiparar ausente a zero.

**Casos não monotônicos:**
- Variação com valores negativos e positivos: usar centro neutro em **zero**, divergindo do frio (negativo) ao quente (positivo); se a classificação original não tiver ponto de corte zero, reconstruir a legenda e as classes a partir dos dados originais, não da cor dos pixels.
- Oscilação/volatilidade: frio representa **menor oscilação** e quente **maior oscilação**; evitar sugestão de mérito/qualidade fiscal.
- Para todas as figuras: preservar ordem cromática, contrastes entre municípios e legenda; não usar simples remapeamento RGB se alterar classes, contornos, textos, linhas ou símbolos.

**Implementação registrada:** alterado o parágrafo 'Como interpretar as cores' exclusivamente na [cópia nativa de trabalho](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit), com confirmação de 1 ocorrência substituída e readback de 51 tabelas/4 imagens. Os PNGs/figuras existentes **não foram recoloridos** nesta operação. A matriz original já utiliza a direção frio → quente (azul-claro até vinho), mas ainda é necessário QA específico da classe neutra/zero na evolução dos investimentos e da separação de 'Sem dado'. A correção cartográfica de fato depende da base geográfica/valores, não apenas de edição de legenda.
