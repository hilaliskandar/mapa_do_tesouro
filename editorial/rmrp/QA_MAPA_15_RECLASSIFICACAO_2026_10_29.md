# RMRP — Mapa 15 reclassificado com separação de sinais — 29/10/2026

Base de 34 municípios e seis exercícios de investimentos liquidados (2020–2025), da DCA canônica (Drive ID 1BtXY_FxydMREEbMACJtaoW2n24ohVH33). Investimentos corrigidos pelo índice IPCA de dezembro de cada exercício para setembro/2026; variação percentual da média anual real do triênio 2023–2025 sobre o triênio 2020–2022.

Geometria: arquivos originais `SP_Municipios_2022.shp/shx/dbf/prj/cpg` recuperados do Drive, pasta `135bW7V-5agl3HjRW4M52CjENR12KJF3o`. EPSG:4674 verificado, 645 polígonos com códigos únicos, recorte exato de 34 municípios da RMRP, nenhum nulo ou inválido no recorte; nenhuma simplificação geométrica. Alternativa oficial 2025 identificada no GeoFTP IBGE, mas a transferência direta foi bloqueada no ambiente; usar 2022 é explicitado na fonte, sem inventar atualização da divisão territorial.

Distribuição apurada por classe cromática, com zero como quebra obrigatória:
- Queda superior a 50%: 3 municípios (azul intenso)
- Queda de 20% a 50%: 9 municípios (azul intermediário)
- Queda inferior a 20%: 7 municípios (azul claro)
- Alta de 0% a 50%: 5 municípios (rosa claro)
- Alta superior a 50%: 10 municípios (vinho)
Total = 34, sendo 19 quedas e 15 altas. Valores extremos: -68,5332% e +254,9829%.

Arquivos produzidos nesta sessão: `/mnt/data/RMRP_mapa_15_reclassificado.png`, `RMRP_mapa_15_reclassificado.pdf`, `RMRP_mapa_15_valores_auditados.csv`, `RMRP_mapa_15_geometrias.gpkg`. O arquivo de código reprodutível está em `/mnt/data/rmrp_map15/build_map.py`. Esses caminhos são locais à sessão, não arquivos incorporados ao repositório ou Drive.

**Status**: figura alternativa criada e examinada visualmente; **ainda não incorporada à cópia Google Docs**. Antes da troca, preservar a legenda/metodologia do documento e verificar legibilidade e paginação após substituir somente a imagem 15. Original preservado e nenhuma publicação efetuada.

## Integração efetiva na cópia de trabalho — 29/10/2026
- Substituída **somente** a imagem 15 do Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`, no mesmo parágrafo; novo inline object `kix.e70il9pmah9m`, com largura solicitada de 445 pt.
- Atualizados dois trechos textuais: legenda imediata do mapa e explicação geral das cores, eliminando a ressalva obsoleta de classe que cruzava zero.
- Nova prova PDF exportada: **73 páginas**. Conferência nativa: **16 figuras e 52 tabelas**. Conferência PDF: mapa 15 e legenda presentes juntos na **página 39**, mapa 16 ainda na página **41**.
- A página 39 foi renderizada em 1,7× e inspecionada: mapa e legenda cromática numérica legíveis, legenda textual abaixo da figura, título subsequente sem sobreposição. A figura reconstruída preserva contornos vetoriais originais sem simplificação; a imagem incorporada ao Docs é raster de apresentação, com a fonte vetorial e os valores municipais preservados em arquivos auxiliares locais.
- Relatório original de consolidação não alterado; publicação e homologação permanecem suspensas até QA final das demais páginas e tabelas.
