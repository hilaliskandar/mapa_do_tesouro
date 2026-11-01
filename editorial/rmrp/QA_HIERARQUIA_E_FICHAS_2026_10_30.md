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


## RMRP — lote de QA cartografico e tabelas continuadas (01/11/2026)
- Prova PDF: 73 paginas, 16 figuras em paginas 5, 7, 10, 14, 16, 17, 19, 30, 31, 33, 34, 35, 36, 37, 38 e 40. As imagens conservam 240–332 dpi de resolucao efetiva; foi gerada folha de contato e examinado em escala nativa o mapa da pagina 14, incluindo legenda de classes, intervalos e escala cromatica.
- A legenda do mapa da pagina 14 encontra-se completa (cinco classes e categoria sem dado), sem recorte. Como o mapa impresso ocupa 384,8 pt de largura para imagem de 1500 px, textos de legenda integrados ao raster podem apresentar corpo pequeno em A4; qualidade de resolucao nao equivale automaticamente a legibilidade em papel. Recomenda-se teste de impressao das legendas antes da homologacao de todas as figuras, sem alterar valores ou classificacoes.
- Varredura programatica em todas as paginas das fichas encontrou 29 paginas contendo tabelas municipais com cabecalho `Indicador | 2023 | 2024 | 2025`; em paginas com duas fichas, o cabecalho ocorre duas vezes. A procura por bordas inferiores de texto muito proximas ao limite fisico da pagina nao gerou ocorrencias (limiar de 32 pt). Nenhuma linha foi demonstrada perdida por essa verificacao. A pagina 72 nao contem cabecalho tabular, pois continua comentario municipal da pagina precedente; a ultima ficha com tabela integra a pagina 73.
- Arquivos auxiliares de QA gerados localmente: `rmrp_audit_data.json`, `rmrp_legendas_16.png` e `rmrp_map14_full.png` (nao presumir que estejam persistidos no GitHub/Drive).
- Nenhuma modificacao no Google Docs realizada neste lote: o trabalho foi de verificacao visual e programatica. Permanecem como pendencia a prova impressa das 16 legendas e a conferencia grafica integral de limites/alinhamentos de todas as 52 tabelas. Relatorio ainda nao homologado nem publicado.


## RMRP — homologação técnica consolidada para divulgação digital (01/11/2026)
- **Prova de referência congelada para QA:** `RMRP — Trabalho cartográfico 16 indicadores — 28-10-2026.pdf`, 73 páginas, 4.063.462 bytes, SHA-256 `d52d35bcc2ffc94bc8f55394b1b38862f305db71b15256692fbf92475263812b`. O nome histórico do arquivo não equivale à data da revisão; a versão editorial atual é a consolidada após as intervenções de 31/10.
- Auditoria abrangente em PDF via PyMuPDF: **34 títulos municipais únicos**, distribuição sub-regional **15/6/6/7**, cada ficha contendo exatamente uma ocorrência de cada uma das seis rubricas `Receita corrente nominal`, `Receita tributária nominal`, `Despesa corrente nominal`, `Despesa total nominal`, `Investimento nominal`, `Investimento real, set./2026` (**204 linhas de indicadores identificadas, sem falta ou duplicação**). Cabeçalhos repetidos nas fichas com tabelas continuadas foram reconhecidos e não constituem erro editorial.
- **16 imagens cartográficas presentes**. As auditorias anteriores verificaram DPI e presença das classes e legendas nos arquivos; não foi comprovada supressão, recorte ou deformação. Limitação residual: a prova física impressa em papel não foi realizada; eventual edição impressa requer esse controle próprio.
- **Decisão técnica:** versão **apta ao fechamento para divulgação digital em PDF**, não obstante inspeção impressa integral ainda pendente. As checagens programáticas e as inspeções visuais por amostra não equivalem a perícia visual individual de cada célula de todas as 52 tabelas. Para o escopo de divulgação digital, não existe defeito material conhecido e aberto que justifique reedição das 34 fichas ou reconstrução dos mapas. O status de publicação efetiva permanece **NÃO PUBLICADO**; preparar versão definitiva com nome/data atualizados, conferir hash e registrar destino/URL antes da divulgação.
- **Regra de congelamento:** não reabrir itens encerrados nem modificar dados, análises, gráficos ou paginação sem defeito material novo comprovado. Manter o Google Docs de trabalho `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI` e o original consolidado separados. Próximo passo é a emissão do artefato final identificado e a autorização de publicação; **nenhuma publicação externa foi executada neste fechamento**.


## RMRP — disponibilização do PDF no Drive e limite de acesso (01/11/2026)
- PDF congelado em 01/11/2026 enviado ao Google Drive: `RMRP_Financas_Municipais_Relatorio_Analitico_2026-11-01_v1.pdf`, ID `1LSQYFzO9N-sxHfBJD4MYqSvIt4dygSFk`, URL `https://drive.google.com/file/d/1LSQYFzO9N-sxHfBJD4MYqSvIt4dygSFk/view?usp=drivesdk`. Upload concluído; metadados conferidos: MIME `application/pdf`, **4.063.462 bytes**, owner da conta conectada, `shared=false` e única permissão registrada `owner`.
- O conector disponível para compartilhamento oferece usuário específico ou domínio da organização; **não permite habilitar acesso público irrestrito** nesta interface. Logo, arquivo disponível no Drive da conta, **AINDA NÃO PUBLICADO PUBLICAMENTE**. Não circular o link como acesso anônimo validado.
- Para publicidade externa, configurar manualmente no Drive `Compartilhar > Acesso geral > Qualquer pessoa com o link > Leitor` (quando permitido pelo administrador), depois verificar abertura sem autenticação. Alternativamente escolher o destino público/editorial para deploy e validar HTTP/PDF/hash. Nenhuma alteração ao site público nem anúncio em redes foi feita.
- Conservar distinção entre homologação para divulgação digital e publicação efetivamente acessível; preservar o documento nativo e as 34 fichas, 52 tabelas e 16 mapas.


## Publicação editorial RMRP no Emdash — 01/11/2026
- Destino editorial confirmado no CMS do Radar Regulatório: coleção `posts`, categoria `estudos-e-analises` (Estudos e Análises, pt-BR). Não existe necessidade de criar nova seção apenas para este relatório.
- **Rascunho editorial efetivamente criado no Emdash e relido**: ID `01M6AN17PNGPDKP3YRHA77H3SG`, slug `financas-rmrp-receitas-investimentos-desigualdades-territoriais-2026`, status `draft`, título `Finanças municipais na Região Metropolitana de Ribeirão Preto: receitas, investimentos e desigualdades territoriais`. Conteúdo: síntese dos resultados, distinção entre comparações 2023/2025 e triênios, metodologia, 16 mapas e 34 fichas, ressalvas e metadados SEO. URL projetada pelo esquema `/posts/{slug}`, **não afirmar que já é pública**.
- PDF homologado 73p identificado no Drive pelo ID `1LSQYFzO9N-sxHfBJD4MYqSvIt4dygSFk`, porém metadados indicaram `shared=false`. A biblioteca do Emdash já contém PDFs (ex.: RMJ), mas a ferramenta MCP `media_upload` requer conteúdo binário como base64, não aceita diretamente referência `file_uri` exportada do Drive; a conexão disponível não fornece publicação de PDF por referência remota. **Não foi anexado PDF da RMRP ao Emdash.**
- **Estado: RASCUNHO, NÃO PUBLICADO.** Gate para publicação: carregar a cópia exata do PDF congelado no Emdash/R2, obter URL pública funcional e validar a resposta HTTP PDF; substituir na matéria o aviso de disponibilização pendente por link público; conferir persistência do vínculo e publicar o item. Não divulgar um link de Drive privado ao leitor. Nenhuma alteração no relatório-fonte nem no conteúdo fiscal.


## 01/11/2026 — Emdash PDF upload
A tentativa de envio do PDF final da RMRP ao Emdash pela operação media_upload falhou duas vezes por erro HTTP/2 de transporte do payload base64 (5,4 milhões de caracteres). Consulta subsequente da biblioteca mostrou apenas dois PDFs RMJ, sem o arquivo RMRP. Rascunho Emdash 01M6AN17PNGPDKP3YRHA77H3SG permanece sem publicação. Recomendado envio pela interface administrativa da biblioteca, preservando os bytes e conferindo URL pública antes de publicar a matéria.
