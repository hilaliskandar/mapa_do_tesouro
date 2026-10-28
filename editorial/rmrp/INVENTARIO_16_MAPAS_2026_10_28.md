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


## Prova gráfica com orientação intuitiva — 28/10/2026
- Geradas **16 figuras derivadas** (1500×1332 px), prova PDF de 16 páginas, pacote ZIP e manifesto SHA-256. Mantida integralmente a região cartográfica e a legenda até a coordenada vertical 1180 px dos PNGs de origem; removido apenas o rodapé compartilhado que estava truncado pelo recorte em quadrantes. Adicionada faixa ordenada de cinco cores (azul-claro → vinho) com títulos extremos 'menor valor' e 'maior valor' sem depender da consulta à legenda para orientar a leitura. Para os mapas 15 e 16, faixas rotuladas respectivamente como 'redução mais intensa → aumento mais intenso' e 'menor oscilação → maior oscilação'.
- A prova foi visualmente inspecionada no mapa 15. **Limite:** no mapa de evolução dos investimentos o intervalo central vai de -10,6% a 16,7% e contém zero; uma paleta verdadeiramente divergente, com centro em zero, **exigiria reclassificação a partir da base vetorial e dos valores municipais**. A faixa é apenas orientação relativa fiel às cinco classes existentes, não alteração dos limites.
- Os arquivos desta edição estão disponíveis no ambiente da conversa como `RMRP_16_MAPAS_LEITURA_INTUITIVA_2026_10_28.zip` e `.pdf`, acompanhados de `build_rmrp_cores.py`. **Ainda não inseridos no Google Docs**; antes disso validar os outros 15 painéis, impressão e eventual reclassificação dos indicadores com sinal. Não presumir que editar raster remapeia as classes numéricas.


## Primeiro mapa adicional integrado em cópia — 28/10/2026
- Na [cópia nativa experimental](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit), adicionado **ISS principal por habitante (2025)** após o trecho que compara as bases de IPTU, ISS e ITBI, antes da explicação sobre o FPM. Figura com 420×420 pt e legenda textual separada em parágrafo próprio. Fonte: imagem 06 do pacote de leitura intuitiva de 28/10.
- Readback da API Docs após inserção e correção de quebra de parágrafo: **51 tabelas, 5 imagens**, sem perda de objeto prévio; posicionamento verificado no corpo do documento. Exportação intermediária em PDF registrou 65 páginas e revelou, na inspeção da página 30, legenda compartilhada do mapa pequena e uma concatenação inicial da legenda textual com a imagem, posteriormente separada por quebra de parágrafo. Ainda não foi realizada nova prova PDF após essa correção.
- **Ressalva gráfica:** a imagem ISS extraída por quadrante deve passar por reconstituição/validação da margem inferior da legenda de classes; as legendas pequenas e potencialmente truncadas não autorizam homologação gráfica. Não propagar o método em lote antes de corrigir essa questão. Os dados e polígonos não foram recalculados nem recoloridos; gradiente frio-quente é o da matriz original, com régua intuitiva suplementar.
- O relatório consolidado de referência e a prova de 25/10 permanecem intactos. A cópia 28/10 é experimental e não publicada.
