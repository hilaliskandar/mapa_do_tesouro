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


## Correção objetiva de legendas e atualização da cópia — 28/10/2026
- Recuperadas as quatro matrizes originais de 3000×2500 pixels e recompostos **16 painéis** sem perda da quinta classe numérica: a extração de prova anterior cortava o limite inferior dos quadrantes; a atual conserva toda a legenda de cada mapa. Adicionada faixa cromática fria→quente abaixo da legenda, sem alterar a cor ou os valores de nenhum polígono. Foram gerados `RMRP_MAPAS_LEGENDAS_COMPLETAS_20261028.zip`, `RMRP_MAPAS_LEGENDAS_COMPLETAS_20261028.pdf` e `rebuild_maps.py` na conversa atual. O mapa ISS foi inspecionado e exibe todas as cinco categorias, incluindo 'Muito alto | 529–949', antes cortada.
- Na [cópia Google Docs de trabalho](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit), **substituído o mapa ISS** originalmente inserido por versão de legenda completa. Operação `deleteContentRange` + `insertInlineImage`, imagem nativa nova `kix.5crngjipf2n7`, 420×390 pt; a legenda textual mantém parágrafo separado. Conferência API Docs após edição: **51 tabelas e 5 imagens**, sem perda estrutural dos objetos restantes; original consolidado intacto.
- **Limite de homologação:** a reprodução com legenda completa e a leitura visual do PNG não dispensam exportação PDF e inspeção gráfica da página após substituição; os 15 outros PNGs necessitam inspeção individual antes de uso. A transição vermelho/azul nos mapas de variação é ordenação relativa, não reclassificação com zero como corte. Não publicar.


## Prova de paginação do mapa ISS — 29/10/2026
- Exportada e inspecionada a cópia nativa após correção das classes de legenda. O primeiro PDF possuía 64 páginas: o mapa ISS estava completo na página 29, mas a legenda textual havia passado à página 30.
- Ajustado **apenas o tamanho da imagem ISS** na cópia de trabalho, de 420×390 pt para **385×358 pt**, preservando os pixels e a classificação. Reexportado PDF de 64 páginas; verificação objetiva por extração de páginas do PDF confirmou **imagem do ISS e legenda textual reunidas na página 29**. A nova escala é menor, portanto é necessária inspeção final em tamanho de impressão para homologar a legibilidade dos números.
- Google Docs [cópia experimental](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit): **51 tabelas e 5 imagens** verificadas após intervenção. Relatório principal não alterado. O lote remanescente só poderá avançar respeitando relação entre tamanho da figura, legenda e paginação.


## Integração de ITBI e FPM — 29/10/2026
- Inseridos na **cópia experimental Google Docs** (`19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`) os mapas **ITBI principal/habitante** e **FPM/habitante**, derivados do pacote com legendas completas. Inserções temáticas: ITBI após a tabela regional de ITBI e antes do parágrafo de cobertura da série; FPM após a interpretação do padrão territorial de transferências. Cada imagem configurada em 385×358 pt, com legenda textual e fonte em parágrafo separado.
- Readback da estrutura nativa: **51 tabelas e sete imagens**; PDF reexportado: **65 páginas**. Inspeção programática do PDF identificou mapa e legenda textual de ITBI na página **19**, ISS na **30** e FPM na **31**. A página 31 foi renderizada e visualmente conferida: mapa FPM, cinco intervalos da escala, régua frio→quente, legenda e início da seção seguinte coexistem sem sobreposição aparente.
- Ressalva: o intervalo cromático numérico é pequeno na prova em A4 e a qualidade final de impressão exige inspeção de todos os mapas em resolução adequada; não são artefatos homologados. A cópia principal da edição anterior permanece intocada. Restam nove indicadores não incorporados como mapas individuais, além de possível substituição pelas legendas recompostas dos mapas mais antigos.


## Nova rodada de integração — 29/10/2026
- Inseridos na [cópia de trabalho nativa](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit) os mapas 13 **Educação/receita corrente** e 11 **pessoal e encargos/receita corrente**, com imagem original recomposta com legenda de cinco classes e barra frio→quente; dimensões 385×358 pt e legendas de fonte explicitando que NÃO são indicadores legais da aplicação mínima em Educação nem do limite de pessoal da LRF.
- QA após inserção: 51 tabelas nativas e **9 imagens**. Exportação PDF intermediária de **67 páginas**; inspeção visual das páginas **33 e 34**, confirmando mapa e legenda na mesma página, sem corte ou sobreposição. Após inspeção, legendas novas reformatadas em fonte de 10 pt; **essa formatação posterior ainda exige nova prova gráfica de impressão**. Relatório consolidado de referência permaneceu intocado. Restam sete mapas originais ainda não incorporados de forma individual (incluindo variação e oscilação de investimentos, cujo ponto zero requer QA e eventual classificação pela base de dados). Nenhum deploy/publicação realizado.


## Integração Saúde e pessoal por habitante — 29/10/2026
- Adicionados à [cópia de trabalho RMRP](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit) os mapas **4 — Despesa em Saúde/receita corrente** (na seção 13.4, antes do mapa de Educação/receita corrente) e **10 — Pessoal e encargos/habitante** (na seção 13.5, depois de pessoal/receita corrente). Cada imagem tem 385×358 pt, com cinco classes de magnitude e sentido frio→quente, fonte e ressalva interpretativa.
- Exportação PDF da cópia após a edição: **69 páginas**. Verificadas visualmente **página 33 (Saúde)** e **página 36 (pessoal/habitante)**, com mapas, legendas completas e texto próximos, sem cortes ou sobreposição visível. Readback de documento nativo: **51 tabelas, 11 imagens**; originais intactos, nenhuma publicação.
- Observação editorial: o mapa de Saúde ficou isolado em página relativamente vazia na prova. Não é erro de clipping, mas pode justificar recomposição após a inserção de todos os mapas, para evitar páginas pouco ocupadas. Restam **cinco** mapas do conjunto de 16 não integrados individualmente: 2 (três impostos/receita), 3 (três cotas/receita), 12 (Educação/habitante), 15 (evolução real entre triênios) e 16 (oscilação investimentos). Os dois últimos requerem validação semântica das cores do zero e da volatilidade.
