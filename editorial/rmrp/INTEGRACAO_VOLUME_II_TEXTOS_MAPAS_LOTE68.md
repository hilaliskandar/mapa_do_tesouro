# Lote 68 — Edição integrada do Volume II com mapas do Volume I

**Data:** 02/11/2026. **Resultado:** o manuscrito integral do Volume II (Lote 64B, 111.619 caracteres) foi recuperado via conexão ao GitHub e transportado em cópia de trabalho no Google Docs (ID `1_tjANrNDMWBj1B4QGhHLILN6qtF_75PFJlzjvnSRWdw`) para o ambiente de diagramação. A partir do texto exportado e dos mapas do Lote 65, foi montada a primeira edição integrada em DOCX e PDF.

## Produtos efetivos

- `RMRP_VOLUME_II_INTEGRADO_TEXTO_MAPAS_LOTE68.docx`: edição textual editável; 45 tabelas estruturadas, com os capítulos originais e 8 mapas.
- `RMRP_VOLUME_II_INTEGRADO_TEXTO_MAPAS_LOTE68.pdf`: edição de prova com **54 páginas**, tamanho Letter; mesmo conteúdo da versão editável, com imagens incorporadas.
- Os dois arquivos foram salvos na Biblioteca, em `/RMRP/Volume_II/`, com IDs `libfile_b81246355ae88191b3b980f850f09bc7` (DOCX) e `libfile_2120f7d897ac8191af9cd1ac07ec86df` (PDF).
- Mapas integrados próximos aos temas: M02, M03 e M08 na seção de estrutura de financiamento; M01 na composição municipal; M14, M15 e M16 na seção de investimentos; M06 no início das SWOT. Não há atlas anexo.

## QA e limites

A renderização via `render_docx.py` gerou 54 páginas; a página 8 foi inspecionada visualmente, confirmando mapa, legenda, título e texto. O PDF foi conferido com `pdfinfo`, e a extração de texto identificou as quatro partes e oito títulos de mapas. A edição **ainda não passou por conferência visual de todas as páginas** e, portanto, não está homologada.

O documento integral preservou os itens substantivos da origem e suas notas operacionais. Gráficos fiscais F2, F3 e F4 do Lote 63 permanecem **como referências textuais** aos arquivos SVG do GitHub, pois as imagens SVG não foram transportadas nesta montagem. F1, F5 e F6 ainda dependem de produção. Os mapas M06 e M15 mantêm ressalvas: ISS observado não é efeito líquido IBS; M15 inclui classe cruzando zero.

A prova integra texto e mapas; **não** deve ser chamada de edição final ilustrada integral, dado o estado dos gráficos e a necessidade de QA jurídico-editorial.

## Próxima ação

1. Incorporar efetivamente F2, F3 e F4 (SVG do Lote 63) ou PNG renderizados com equivalência visual, junto às seções atuais.
2. Produzir e revisar F1, F5 e F6.
3. Realizar QA de páginas, tabelas e quadros SWOT e resolver metadados editoriais residuais.
4. Conferir equivalência textual entre o manuscrito canônico e a conversão para DOCX, sem regressão de conteúdo.
