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
