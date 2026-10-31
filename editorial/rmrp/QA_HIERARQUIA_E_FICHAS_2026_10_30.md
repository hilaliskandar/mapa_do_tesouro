# RMRP — Revisão da hierarquia editorial e quebras das fichas — 30/10/2026

Documento editável: https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit

## Escopo e evidências
- Inspeção de PDF de trabalho com PyMuPDF para 34 fichas e quebras de página (complementada por leitura dos títulos e tabelas nativas no Google Docs).
- As tabelas das fichas municipais aparecem, em vários casos, divididas entre páginas; as páginas de continuação apresentam cabeçalho «Indicador | 2023 | 2024 | 2025». Não se constatou ausência de linha na extração textual, mas isto não equivale a homologação visual exaustiva de 52 tabelas.
- Foi identificada uma inconsistência editorial objetiva: nos capítulos 10, 11, 12 e 13, os títulos de subseção eram numerados novamente como 1., 2. etc., apesar de integrarem a mesma sequência do livro.
- Correção aplicada na cópia de trabalho: 27 títulos HEADING_2 transformados, por exemplo, em **10.1**, **11.1**, **12.1**, **13.1**, sem alteração do texto dos títulos além do prefixo, nem dos dados ou comentários fiscais. Modificações protegidas por revisão Google Docs e confirmação de 27 substituições únicas.
- Leitura após a escrita confirmou 27 títulos com numeração hierárquica e zero remanescentes com prefixo simples nos subtítulos pesquisados. Preservadas 52 tabelas nativas e 16 imagens.
- Nova prova PDF: **73 páginas** (a anterior tinha 72). A paginação ampliou-se em uma página pela expansão de títulos; páginas 72–73 contêm séries e comentários da seção de fichas, sem folha em branco ou cauda isolada. Optou-se por não reduzir tipos para forçar 72 páginas.
- O documento original consolidado não foi editado. Não houve publicação nem homologação.

## Pendências editoriais identificadas
1. A seção 9 apresenta fontes e metodologia antes das análises complementares 10–13; a colocação é conceitualmente defensável como método da parte inicial, mas pode parecer fechamento prematuro. A eventual mudança requer reposicionamento e revisão de todas as referências internas, não apenas renomeação.
2. A indicação «Orientações para a leitura das fichas fiscais» aparece antes das análises complementares, embora as fichas venham depois do capítulo 13. Seria preferível deslocar a orientação para a abertura das fichas, mediante verificação de índices e quebra de página.
3. Diferenciar duplicação de informação relevante (síntese inicial x aprofundamento dos capítulos 10–13) de repetição editorial desnecessária. Não suprimir fundamentos e ressalvas úteis.
4. Necessária revisão gráfica visual minuciosa de linhas e limites em tabelas continuadas, e conferência impressa dos detalhes cartográficos.

**Status**: hierarquia normalizada; demais ajustes sugeridos ainda não realizados.


## Continuidade — reposicionamento das orientações (30/10/2026)
- Na cópia editável `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`, o bloco `ORIENTAÇÕES PARA A LEITURA DAS FICHAS FISCAIS` e seu parágrafo explicativo foram deslocados do intervalo após o capítulo 9 para a posição imediatamente anterior a `SUB-REGIÃO 1 — RIBEIRÃO PRETO`.
- Edição efetuada por API Google Docs com controle de revisão; leitura posterior confirmou ocorrência única do título e sequência `ANÁLISES COMPLEMENTARES` → capítulos 10–13 → `ORIENTAÇÕES` → `SUB-REGIÃO 1`.
- Texto de orientação preservado, sem alterações deliberadas de números, tabelas, mapas ou análises individuais. O estilo de título no novo local foi lido como `HEADING_1`.
- **Ainda não concluído:** exportação e inspeção visual da nova prova PDF, QA de quebras de tabelas e legibilidade cartográfica, avaliação de redundâncias substantivas, homologação e publicação.
- A contagem de páginas anterior (73) permanece referência histórica: não atribuir essa paginação à versão atual sem nova exportação.


## Lote ampliado de normalização estrutural — 30/10/2026
- Auditoria de todos os títulos da versão editável por API Google Docs: identificados 12 subtítulos explicativos sem prefixo numérico, indevidamente no mesmo nível (`HEADING_2`) das subseções numeradas dos capítulos 12 e 13. Convertidos conjuntamente a `HEADING_3`, preservando todo o texto.
- O título `Quadro comparativo — Variação real das médias anuais, 2020–2022 para 2023–2025 (%)` foi retirado de `HEADING_1` e convertido a parágrafo normal, por não constituir capítulo.
- O parágrafo explicativo imediatamente após `ORIENTAÇÕES PARA A LEITURA DAS FICHAS FISCAIS`, que após o deslocamento havia herdado `HEADING_1`, foi corrigido para `NORMAL_TEXT`.
- Total: 14 correções de estilo realizadas em uma chamada de edição com controle de revisão. Leitura posterior confirmou os 12 títulos em `HEADING_3`, os dois parágrafos em `NORMAL_TEXT`, 52 tabelas nativas, 34 títulos de fichas e ocorrência única das orientações.
- Os mapas e as linhas contábeis não foram editados intencionalmente neste lote. A preservação das 16 figuras na exportação e a paginação resultante continuam pendentes de prova PDF.
- Status: normalização estrutural efetiva; publicação e homologação não autorizadas.


## Revisão ampliada das fichas e prova PDF — 30/10/2026
- Reexaminados integralmente os oito comentários previamente sinalizados: Barrinha, Brodowski, Pontal, Pradópolis, Santa Rita do Passa Quatro, Cajuru, Nuporanga e Orlândia. Todos já abordam a despesa corrente liquidada, embora nem sempre usem a expressão exata procurada no teste anterior. Oito alertas da triagem textual foram, portanto, considerados falsos positivos; nenhuma reescrita fiscal foi realizada.
- Exportada a versão de trabalho para PDF: **73 páginas**, **16 páginas com mapas**, **52 tabelas nativas** (contagem Google Docs). A página 25 contém apenas o título `12.2 O movimento entre 2023 e 2025 foi disseminado`, enquanto a tabela inicia na página 26: problema concreto de paginação.
- Aplicada a propriedade `keepWithNext=true` ao título 12.2, com leitura de retorno confirmando a propriedade. Uma nova exportação manteve 73 páginas e **não eliminou o título isolado na página 25**. Portanto, a falha segue aberta; não considerá-la resolvida.
- A estrutura nativa também contém um parágrafo vazio entre título e legenda da tabela; é necessário examinar a cadeia de propriedades keepWithNext e a eventual quebra antes da tabela, com alteração localizada e nova prova.
- Páginas cartográficas com baixa densidade textual (5, 7, 34, 36 e 37) contêm mapas, não devem ser eliminadas automaticamente.
- A homologação visual integral de todas as tabelas e mapas segue pendente, assim como a correção demonstrada da página 25 e a revisão conclusiva de redundâncias.


## Nova correção localizada de paginação — 30/10/2026
- Retomada a quebra entre o título 12.2 e a primeira tabela. Inspeção nativa confirmou a sequência: título, parágrafo vazio, título de tabela distribuído em dois parágrafos, outro parágrafo vazio, tabela nativa.
- Lote inicial alterou `keepWithNext=true` nos dois parágrafos finais anteriores à tabela. A prova PDF disponibilizada pelo exportador continuou apresentando título isolado na página 25.
- Aplicado então `pageBreakBefore=true` ao parágrafo `12.2 O movimento entre 2023 e 2025 foi disseminado`, preservando `keepWithNext=true`; leitura de retorno da API Google Docs confirmou ambas as propriedades e a revisão da edição.
- **QA pendente**: embora o exportador tenha respondido com arquivo PDF, o material local recuperado permaneceu com o mesmo tamanho e a mesma paginação da prova anterior; não há comprovação de que os bytes verificados correspondam à revisão mais recente. Portanto a correção está aplicada no documento nativo, mas **não homologada graficamente**. Exigir uma prova independente efetivamente atualizada antes de encerrar a ocorrência.
- A alteração foi exclusivamente de propriedades de parágrafo; não houve edição deliberada dos dados, das 52 tabelas ou das 16 imagens.


## RMRP — Revisão editorial da seção 12.2 — 30/10/2026
- **Cópia de trabalho:** Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`. Frente de QA: `editorial/rmrp/QA_HIERARQUIA_E_FICHAS_2026_10_30.md`.
- A prova anterior evidenciou título da subseção 12.2 isolado na página 25 e primeira tabela na página 26. A inspeção da API Docs identificou dois parágrafos de legenda, dois separadores vazios e uma tabela nativa.
- **Correção desta rodada, confirmada pela API:** removida a propriedade `pageBreakBefore` do título 12.2 (agora `false`); preservado `keepWithNext=true` no título; removidos os espaçamentos acima/abaixo do primeiro parágrafo separador; ativado `keepWithNext=true` no segundo parágrafo da legenda, de modo a manter a cadeia até a tabela. Aplicado com controle de revisão.
- **Status de prova:** ajuste nativo persistido; a paginação final após essa rodada ainda requer nova exportação e inspeção gráfica independente. Não declarar resolvido nem homologado sem confirmar PDF. Não houve alteração de dados, mapas ou texto fiscal.
- Os números **73 páginas, 52 tabelas nativas e 16 mapas** são referência da última prova analisada, não certificação automática da versão agora editada. Permanecem pendentes a inspeção integral das tabelas e das legendas cartográficas e a homologação.

- **Verificação adicional após a edição (30/10, 12h):** exportação PDF novamente executada; arquivo disponibilizado com **4.063.202 bytes**, 73 páginas. Inspeção local com PyMuPDF constatou que a **página 25 ainda contém apenas o título 12.2 (54 caracteres extraídos)** e que a **página 26 começa pela legenda e tabela**. Logo, **não foi demonstrada correção gráfica**. A API nativa confirma as novas propriedades, mas a exportação apresenta a mesma composição; investigar atualização/cache do exportador ou a interação com a estrutura nativa. Não homologar.


## RMRP — correção homologada da quebra 12.2 — 31/10/2026
- **Defeito resolvido em prova PDF:** o título `12.2 O movimento entre 2023 e 2025 foi disseminado`, a legenda `Tabela 1 – Municípios segundo direção...` e a tabela nativa estão agora na **mesma página 25**.
- Intervenção: exclusão cirúrgica de um caractere separador de parágrafo imediatamente depois do título 12.2 (`deleteContentRange` no índice correspondente, com proteção por revisão); a tentativa anterior de remover integralmente dois parágrafos em lote falhou e não modificou o arquivo. A edição bem-sucedida preservou conteúdo fiscal e estrutura da tabela.
- **Nova prova realmente alterada:** PDF exportado com **4.062.467 bytes e 72 páginas** (a prova precedente tinha 4.063.202 bytes e 73 páginas). PyMuPDF localizou título e legenda da primeira tabela na página 25, com 1.843 caracteres extraídos nessa página: deixou de existir título isolado.
- **Status:** problema gráfico 12.2 encerrado com verificação textual de página e nova exportação. A homologação integral de 52 tabelas e 16 mapas, sobretudo legibilidade de legendas e quebras das fichas, continua pendente. Documento ainda não publicado. Cópia de trabalho Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`.


## RMRP — lote de auditoria gráfica, 31/10/2026
- Prova PDF de 72 páginas auditada em lote com PyMuPDF: **16 imagens cartográficas** em páginas temáticas; fichas municipais com tabelas nativas e cabeçalhos repetidos nas continuações. Não confundir as páginas cartográficas pouco textuais com páginas vazias.
- Inspeção de páginas 43, 71 e 72 detectou duas quebras editoriais: orientações de leitura iniciadas na página 43, com continuação na 44; e última ficha municipal, Santo Antônio da Alegria, com somente duas linhas da tabela na penúltima página e restante na última.
- Na cópia Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`, aplicadas em lote propriedades `pageBreakBefore=true` aos títulos `ORIENTAÇÕES PARA A LEITURA DAS FICHAS FISCAIS` e `Santo Antônio da Alegria — sub-região 4`, usando controle de revisão.
- **Prova reexportada e confirmada**: **73 páginas**, 16 imagens cartográficas. Orientações inteiras e início da sub-região 1 na página 44; ficha final, com tabela e comentário completos, começa na página 73. Imagens renderizadas das páginas 44 e 73 para inspeção de acabamento. A elevação de 72 para 73 páginas é deliberada para preservar blocos intactos sem reduzir a tipografia.
- Nenhum dado fiscal, comentário municipal, tabela ou mapa foi alterado deliberadamente; mudanças apenas de paginação. Não corresponde à homologação visual exaustiva das 52 tabelas e das 16 legendas impressas. Pendências: inspecionar visualmente todas as tabelas continuadas e os 16 mapas em tamanho de impressão, corrigir anomalias verificadas, registrar QA final antes de publicar.


## RMRP — auditoria gráfica ampliada de 31/10/2026 — 73 páginas
- Fonte examinada: prova PDF mais recente da cópia de trabalho Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`. Inspeção programática integral com PyMuPDF e prancha de contato das 16 páginas cartográficas.
- **73 páginas**; **52 tabelas nativas** verificadas no Google Docs; **16 imagens cartográficas raster**, distribuídas nas páginas **5, 7, 10, 14, 16, 17, 19, 30, 31, 33, 34, 35, 36, 37, 38 e 40**. Uma imagem por página listada, sem ausência de figura entre as 16 catalogadas.
- Dimensões das figuras: 15 arquivos 1500 px de largura e mapa 15 (variação real dos investimentos entre triênios) em 2048 px; resolução efetiva em página de **240–332 dpi**. Não foi observada deformação evidente na prancha geral. Todavia o tamanho impresso das legendas, por serem parte das imagens raster, exige conferência ampliada caso a caso: DPI suficiente não comprova legibilidade de fontes pequenas.
- Varredura das fichas municipais, páginas 44–73: tabelas divididas aparecem com cabeçalho de continuação `Indicador | 2023 | 2024 | 2025`; nenhuma ausência de linha foi comprovada nessa análise textual. A divisão em páginas deve ser mantida quando a alternativa criaria espaços em branco excessivos. Não se detectou página final em branco: a ficha de Santo Antônio da Alegria ocupa a página 73.
- **Nenhuma alteração nativa efetuada nesta rodada**, pois não se comprovou defeito específico cuja correção fosse mais segura do que o arranjo existente. Resultado é auditoria ampliada, não homologação visual integral das 52 tabelas.
- Pendência para homologação: inspeção das legendas e dos limites das 16 figuras em escala física de impressão; inspeção focada das tabelas continuadas por página, inclusive alinhamento das linhas e repetição exata dos cabeçalhos. Preservar redação fiscal, 34 fichas e séries DCA. Publicação não autorizada.
