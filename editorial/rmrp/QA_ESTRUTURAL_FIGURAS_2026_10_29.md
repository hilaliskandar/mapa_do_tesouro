# RMRP — Auditoria estrutural das figuras e preparação do QA gráfico — 29/10/2026

## Escopo e evidência
Documento de trabalho: https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit

Inspeção direta da estrutura nativa Google Docs em 29/10/2026, sem alteração do conteúdo. Resultado: 646 elementos estruturais de corpo, 51 tabelas nativas e 16 ocorrências de imagens inline. O total de 74 páginas corresponde à última prova PDF documentada no README, não a uma exportação nova nesta diligência.

## Ocorrências observadas
1. Os mapas iniciais em posições de corpo 28 e 52 aparecem em parágrafo de imagem isolado com legenda textual anterior. Verificar visualmente se a apresentação e as remissões são claras; não inverter automaticamente sem inspecionar a página.
2. Nas posições 34 e 274, o parágrafo que contém a imagem também contém texto de legenda ou sua continuação. Esse padrão exige conferência de separação visual e de possível quebra de linha/página.
3. Em pelo menos sete ocorrências dos mapas inseridos nas seções de composição fiscal, pessoal, saúde, educação e investimentos (posições 82, 96, 295, 297, 305, 307, 309, 315, 331), a figura usa estilo de parágrafo HEADING_2. Conferir efeito no sumário/navegação, espaçamento e paginação; eventualmente normalizar somente os parágrafos de imagem e legenda, sem alterar títulos substantivos.
4. As demais figuras inspecionadas apresentam legenda textual imediatamente posterior no fluxo nativo (ex.: ITBI, ISS, FPM, séries de investimento). A proximidade estrutural não comprova que imagem e legenda estejam na mesma página.
5. Mapa de variação real entre triênios: classe de -10,6% a +16,7% cruza zero; permanece pendência de reclassificação a partir dos valores municipais, não de simples recoloração raster.

## Controle de qualidade pendente
- Exportar a revisão atual em PDF e inspecionar as 74 páginas efetivas, atentando a imagens/legendas separadas, excesso de vazios, quebras de tabelas, tipografia e escala impressa.
- Documentar cada ocorrência por número real de página, natureza, evidência e intervenção proposta antes de mudar a cópia de trabalho.
- Preservar 51 tabelas, 34 fichas e 16 mapas após quaisquer intervenções.
- Revisar em etapa separada os argumentos das 34 fichas municipais conforme auditoria substantiva; não tomar ausência de erro aritmético aparente como homologação editorial.
- Não alterar relatório consolidado de origem nem publicação em produção sem homologação.

## Situação
QA estrutural realizado; **QA visual de 74 páginas ainda não concluído**. Não afirmar homologação gráfica nem inventar páginas críticas sem verificar a renderização.

## Confronto com QA anterior já registrado no inventário (29/10/2026)
Após a inspeção estrutural, foi localizado registro mais recente no `INVENTARIO_16_MAPAS_2026_10_28.md`: auditoria automatizada de PDF de **74 páginas** por PyMuPDF, com **16 páginas contendo mapas e legendas na mesma página** (5, 7, 11, 16, 18, 19, 21, 32, 33, 35, 36, 37, 38, 39, 40, 42). Foram identificadas **cinco páginas com baixa densidade textual**: 5, 7, 35, 37 e 38. O inventário também registra correção textual pontual sobre a classe cartográfica cruzando zero, seguida de reexportação de 74 páginas. Portanto, a auditoria automatizada já está **concluída**; não deve ser refeita como se estivesse pendente. Continuam pendentes inspeção visual manual das figuras em tamanho de impressão, decisões localizadas de paginação e a reclassificação do mapa de evolução com base nos dados municipais.

As ocorrências de estrutura apontadas acima são **candidatas a controle de estilo**, não defeitos gráficos comprovados: a auditoria automatizada anterior demonstrou que todas as figuras têm legenda na mesma página.
